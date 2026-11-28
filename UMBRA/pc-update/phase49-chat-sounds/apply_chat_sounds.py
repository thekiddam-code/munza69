"""Install chat-followed-by-sound on the stopped Phase 4.9 companion with the 3.3 host update."""
import argparse,datetime,hashlib,json,os,socket,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent

def digest(data):return hashlib.sha256(data.removeprefix(b'\xef\xbb\xbf').replace(b'\r\n',b'\n')).hexdigest()
def running():
 try:
  with socket.create_connection(('127.0.0.1',8765),timeout=1):return True
 except OSError:return False

def preflight(root):
 root=Path(root).resolve();manifest=json.loads((HERE/'manifest.json').read_text('utf8'));modes=[]
 if not (root/'server.py').is_file():raise ValueError('Choose the original ICARUS folder containing server.py.')
 for name,hashes in manifest['files'].items():
  path=root/name
  if path.is_symlink() or not path.resolve().is_relative_to(root):raise ValueError('Linked installation paths are refused.')
  if digest((HERE/'payload'/name).read_bytes())!=hashes['after']:raise ValueError('Payload checksum failed: '+name)
  actual=digest(path.read_bytes()) if path.exists() else None
  if actual==hashes['before']:modes.append('old')
  elif actual==hashes['after']:modes.append('new')
  else:raise ValueError('The installed source differs from the matching Phase 4.9 file: '+name+'. Nothing changed. Install the 3.3 host-actions update first, or request a matching patch.')
 if len(set(modes))!=1:raise ValueError('Partial update detected. Retain data and restore a coherent code backup before retrying.')
 return root,manifest,modes[0]

def atomic(path,data):
 temp=path.with_name(path.name+'.umbra-'+uuid.uuid4().hex+'.tmp')
 try:
  with temp.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(temp,path)
 finally:temp.unlink(missing_ok=True)

def apply(root):
 root,m,mode=preflight(root)
 if mode=='new':return 'Already installed; no settings or data changed.'
 if running():raise ValueError('Save the voyage and stop the companion normally first. Do not kill the process or clear browser storage.')
 backup=root/'umbra_host_code_backups'/(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8]);backup.mkdir(parents=True)
 originals={name:(root/name).read_bytes() if (root/name).exists() else None for name in m['files']}
 for name,data in originals.items():
  if data is not None:(backup/name).write_bytes(data)
 # Extra private copies are recovery evidence only. Rollback never overwrites user settings.
 for name in ['config.json','umbra_host_actions.json']:
  path=root/name
  if path.is_file() and not path.is_symlink():(backup/name).write_bytes(path.read_bytes())
 (backup/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 changed=[]
 try:
  for name in m['files']:
   atomic(root/name,(HERE/'payload'/name).read_bytes());changed.append(name)
  for name,spec in m['files'].items():
   if digest((root/name).read_bytes())!=spec['after']:raise ValueError('Installed checksum failed.')
 except Exception:
  for name in reversed(changed):
   if originals[name] is None:(root/name).unlink(missing_ok=True)
   else:atomic(root/name,originals[name])
  raise
 return 'Chat-sound API installed. Code backup: '+str(backup)+'. Restart the same companion. Sound library, audio profile, microphone, VoiceMeeter and voyage files were not replaced.'

def restore(root,backup):
 if running():raise ValueError('Stop the companion normally before code rollback.')
 root,m,mode=preflight(root)
 if mode!='new':raise ValueError('No matching installed update to roll back.')
 backup=Path(backup).resolve()
 for name,spec in m['files'].items():
  if spec['before'] is not None and digest((backup/name).read_bytes())!=spec['before']:raise ValueError('Original code backup checksum failed.')
 for name,spec in m['files'].items():
  if spec['before'] is None:(root/name).unlink()
  else:atomic(root/name,(backup/name).read_bytes())
 return 'Previous server code restored. Private settings and all data retained.'
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);parser.add_argument('--check',action='store_true');parser.add_argument('--restore-code',type=Path);a=parser.parse_args()
 try:print('Matching '+preflight(a.root)[2]+' files; check only.' if a.check else restore(a.root,a.restore_code) if a.restore_code else apply(a.root))
 except Exception as e:parser.exit(1,'UPDATE STOPPED: '+str(e)+'\n')
