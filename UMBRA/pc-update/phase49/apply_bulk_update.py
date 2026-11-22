"""Apply only the four reviewed Phase 4.9 soundboard files; preserve all private data."""
import argparse,datetime,hashlib,json,os,socket,subprocess,sys,uuid
from pathlib import Path

HERE=Path(__file__).resolve().parent

def normalized(data):return data.removeprefix(b'\xef\xbb\xbf').replace(b'\r\n',b'\n')
def digest(data):return hashlib.sha256(normalized(data)).hexdigest()
def server_running():
 try:
  with socket.create_connection(('127.0.0.1',8765),timeout=1):return True
 except OSError:return False

def preflight(root):
 root=Path(root).resolve();manifest=json.loads((HERE/'manifest.json').read_text('utf8'))
 if not (root/'server.py').is_file():raise ValueError('Select the original ICARUS installation folder containing server.py, not its web folder.')
 modes=[]
 for name,hashes in manifest['files'].items():
  target=(root/name).resolve()
  if not target.is_relative_to(root) or (root/name).is_symlink():raise ValueError('Refusing a linked path outside the selected installation.')
  if digest((HERE/'payload'/name).read_bytes())!=hashes['after']:raise ValueError('Update payload checksum failed: '+name)
  current=digest(target.read_bytes())
  if current==hashes['before']:modes.append('old')
  elif current==hashes['after']:modes.append('new')
  else:raise ValueError('Source differs from the verified Phase 4.9 file: '+name+'. Nothing was changed. Retain this installation and request a matching patch.')
 if len(set(modes))!=1:raise ValueError('Partial update detected. Restore a coherent code backup before retrying; no private files were changed.')
 return root,manifest,modes[0]

def atomic_write(path,data):
 temporary=path.with_name(path.name+'.umbra-update-'+uuid.uuid4().hex+'.tmp')
 try:
  with temporary.open('wb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
  os.replace(temporary,path)
 finally:temporary.unlink(missing_ok=True)

def apply(root,new_library=False):
 root,manifest,mode=preflight(root)
 if mode=='new':return 'Already applied; no files or sound settings were changed.'
 if server_running():raise ValueError('Stop the existing companion normally before applying this Python update. Do not terminate it forcibly or clear browser storage.')
 library=root/'soundboard_data'/'library.json'
 if new_library:
  if library.exists() and json.loads(library.read_text('utf8')).get('sounds'):raise ValueError('--new-library is only for an intentionally empty library. Existing sounds require the verified backup path.')
 elif not library.is_file():raise ValueError('Existing library not found. Locate the original soundboard_data folder. Use --new-library only if you have never imported sounds.')
 backup=root/'umbra_bulk_code_backups'/(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8]);backup.mkdir(parents=True)
 originals={name:(root/name).read_bytes() for name in manifest['files']}
 for name,data in originals.items():
  destination=backup/name;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(data)
 (backup/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 if library.is_file():
  command=[sys.executable,str(root/'sound_backup.py'),'--root',str(library.parent)]
  if not new_library:command.append('--require-existing')
  result=subprocess.run(command,capture_output=True,text=True)
  (backup/'sound-preservation.log').write_text(result.stdout+'\n'+result.stderr,encoding='utf8')
  if result.returncode:raise ValueError('Verified sound-library backup did not complete. Original code and data retained. See '+str(backup/'sound-preservation.log'))
 changed=[]
 try:
  for name in manifest['files']:
   atomic_write(root/name,(HERE/'payload'/name).read_bytes());changed.append(name)
  for name,hashes in manifest['files'].items():
   if digest((root/name).read_bytes())!=hashes['after']:raise ValueError('Installed checksum failed: '+name)
 except Exception:
  for name in reversed(changed):atomic_write(root/name,originals[name])
  raise
 return 'Applied four soundboard files. Code backup: '+str(backup)+'. Sound library, profiles, pairing and world files were not replaced. Restart the same installation and hard-refresh the UMBRA page.'

def restore(root,backup):
 root=Path(root).resolve();backup=Path(backup).resolve()
 if server_running():raise ValueError('Stop the companion normally before restoring code.')
 data=root/'soundboard_data'/'library.json'
 if data.is_file():
  lib=json.loads(data.read_text('utf8'));sounds=lib.get('sounds')
  if lib.get('version')!=1 or not isinstance(sounds,list) or len(sounds)>64 or sum(s['bytes'] for s in sounds)>64*1024*1024:raise ValueError('Old code cannot read this larger library. Restore a verified pre-import library backup separately while stopped; never discard the current library.')
 manifest=json.loads((backup/'manifest.json').read_text('utf8'));originals={}
 for name,hashes in manifest['files'].items():
  if name not in json.loads((HERE/'manifest.json').read_text('utf8'))['files']:raise ValueError('Unknown restore path')
  if not (root/name).resolve().is_relative_to(root):raise ValueError('Linked restore path refused')
  original=(backup/name).read_bytes()
  if digest(original)!=hashes['before'] or digest((root/name).read_bytes())!=hashes['after']:raise ValueError('Restore checksum mismatch; no files changed.')
  originals[name]=original
 for name,data in originals.items():atomic_write(root/name,data)
 return 'Original code restored. Sound data, output and profiles were not changed.'

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);parser.add_argument('--check',action='store_true');parser.add_argument('--new-library',action='store_true');parser.add_argument('--restore-code',type=Path);args=parser.parse_args()
 try:
  if args.check:print('Verified matching Phase 4.9 '+preflight(args.root)[2]+' files; check only, nothing changed.')
  elif args.restore_code:print(restore(args.root,args.restore_code))
  else:print(apply(args.root,args.new_library))
 except Exception as error:print('UPDATE STOPPED: '+str(error),file=sys.stderr);sys.exit(1)
