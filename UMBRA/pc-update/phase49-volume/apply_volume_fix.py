"""Web-only timeout hotfix for the verified Phase 4.9 bulk-import companion."""
import argparse,datetime,hashlib,json,os,socket,subprocess,sys,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent
SCRIPT='web/umbra/soundboard.js'
def digest(data):return hashlib.sha256(data.removeprefix(b'\xef\xbb\xbf').replace(b'\r\n',b'\n')).hexdigest()
def safe(root,name):
 path=root/name
 if not path.resolve().is_relative_to(root) or any(p.is_symlink() for p in (path,*path.parents) if p!=root and p.is_relative_to(root)):raise ValueError('Linked installation path refused: '+name)
 return path

def server_running():
 try:
  with socket.create_connection(('127.0.0.1',8765),timeout=1):return True
 except OSError:return False

def preflight(root):
 root=Path(root).resolve();m=json.loads((HERE/'manifest.json').read_text('utf8'))
 if not safe(root,'server.py').is_file():raise ValueError('Select the original installation folder containing server.py.')
 for name,expected in m['required_backend'].items():
  if digest(safe(root,name).read_bytes())!=expected:raise ValueError('Unrecognized bulk-import backend: '+name+'. No changes made; request a matching patch.')
 if digest((HERE/'payload'/SCRIPT).read_bytes())!=m['after']:raise ValueError('Payload checksum mismatch')
 current=digest(safe(root,SCRIPT).read_bytes())
 if current not in (m['before'],m['after']):raise ValueError('Unrecognized soundboard.js; no changes made. Request a matching patch.')
 return root,m,'new' if current==m['after'] else 'old'

def atomic_write(path,data):
 temp=path.with_name(path.name+'.volume-'+uuid.uuid4().hex+'.tmp')
 try:
  with temp.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(temp,path)
 finally:temp.unlink(missing_ok=True)

def apply(root):
 root,m,mode=preflight(root)
 if mode=='new':return 'Already applied; no changes made.'
 if server_running():raise ValueError('Stop the companion normally before installing. Never force-stop or clear browser storage.')
 library=safe(root,'soundboard_data/library.json')
 if not library.is_file():raise ValueError('Existing library not found. Locate the original installation; do not create a replacement library.')
 folder=safe(root,'umbra_volume_code_backups');folder.mkdir(exist_ok=True)
 backup=folder/(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8]);backup.mkdir()
 original=(root/SCRIPT).read_bytes();code=backup/SCRIPT;code.parent.mkdir(parents=True);code.write_bytes(original)
 (backup/'manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf8')
 safe(root,'soundboard_backups')
 result=subprocess.run([sys.executable,str(root/'sound_backup.py'),'--root',str(library.parent),'--require-existing'],capture_output=True,text=True)
 (backup/'sound-preservation.log').write_text(result.stdout+'\n'+result.stderr,encoding='utf8')
 if result.returncode:raise ValueError('Verified library backup failed. Original code and sounds retained. See '+str(backup/'sound-preservation.log'))
 report=json.loads(result.stdout)
 if not report.get('created') or not report.get('verified') or report.get('source',{}).get('errors') or report.get('source',{}).get('sounds',0)<1:raise ValueError('No verified populated library backup; original code retained.')
 # Detect a concurrent code replacement rather than overwriting it.
 preflight(root)
 if (root/SCRIPT).read_bytes()!=original:raise ValueError('Source changed during backup; no code overwritten.')
 try:
  atomic_write(root/SCRIPT,(HERE/'payload'/SCRIPT).read_bytes())
  if digest((root/SCRIPT).read_bytes())!=m['after']:raise ValueError('Installed checksum mismatch')
 except Exception:
  atomic_write(root/SCRIPT,original);raise
 return 'Applied soundboard.js only. Code backup: '+str(backup)+'. Verified library backup: '+report['file']+'. Restart the same companion and hard-refresh UMBRA. Audio, routing, pairing and world data were not replaced.'

def restore(root,backup):
 root,m,mode=preflight(root);backup=Path(backup).resolve()
 if server_running():raise ValueError('Stop the companion normally before restoring code.')
 if not backup.is_relative_to(root/'umbra_volume_code_backups'):raise ValueError('Select this installation\'s volume code backup.')
 original=safe(backup,SCRIPT).read_bytes()
 if digest(original)!=m['before']:raise ValueError('Backup checksum mismatch; code retained.')
 if mode=='old':return 'Original code already present; no changes made.'
 atomic_write(root/SCRIPT,original)
 return 'Original bulk-import web script restored. All sounds, larger-library backend and settings retained.'

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--check',action='store_true');p.add_argument('--restore-code',type=Path);a=p.parse_args()
 try:
  if a.check:print('Verified '+preflight(a.root)[2]+' installation; read-only check, nothing changed.')
  elif a.restore_code:print(restore(a.root,a.restore_code))
  else:print(apply(a.root))
 except Exception as e:print('UPDATE STOPPED: '+str(e),file=sys.stderr);sys.exit(1)
