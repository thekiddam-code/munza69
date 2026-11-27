"""Local PC setup: preserve existing config, select the real Moments storage folder and saved macro."""
import argparse,json,socket,sys,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'payload'))
from umbra_host_actions import atomic_json,binding,HostActionError

def configure(root,directory=None,shortcut=None):
 root=Path(root).resolve()
 if not (root/'server.py').is_file():raise ValueError('Select the original ICARUS installation folder.')
 try:
  with socket.create_connection(('127.0.0.1',8765),timeout=1):raise ValueError('Stop the companion normally before editing local settings.')
 except OSError:pass
 config=root/'config.json';settings=root/'umbra_host_actions.json'
 if config.is_symlink() or settings.is_symlink():raise ValueError('Linked settings files are refused.')
 original_config=config.read_bytes();original_settings=settings.read_bytes() if settings.exists() else None
 data=json.loads(original_config.decode('utf-8-sig'));preferences=json.loads(original_settings.decode('utf-8-sig')) if original_settings else {}
 if directory is not None:
  folder=Path(directory).resolve()
  if not Path(directory).is_absolute() or not folder.is_dir():raise ValueError('Use the existing Moments Storage Location shown in GG, not a new or guessed directory.')
  preferences['moments_clip_directory']=str(folder)
 if shortcut is not None:
  keys=[k.strip().lower() for k in shortcut.split('+')]
  macros=data.get('macros');
  if not isinstance(macros,dict):raise ValueError('Existing macro configuration is not an object. Retain and repair it first.')
  macros['Save Clip']=keys;binding(data)
 backup=root/'umbra_host_settings_backups'/uuid.uuid4().hex;backup.mkdir(parents=True)
 (backup/'config.json').write_bytes(original_config)
 if original_settings is not None:(backup/'umbra_host_actions.json').write_bytes(original_settings)
 try:
  if shortcut is not None:atomic_json(config,data)
  if directory is not None:atomic_json(settings,preferences)
 except Exception:
  config.write_bytes(original_config)
  if original_settings is None:settings.unlink(missing_ok=True)
  else:settings.write_bytes(original_settings)
  raise
 return 'Settings saved locally; existing macros/Arctis selection retained. No GG, microphone, VoiceMeeter, capture or driver settings were changed. Backup: '+str(backup)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--clip-directory');p.add_argument('--binding');a=p.parse_args()
 if a.clip_directory is None and a.binding is None:
  a.clip_directory=input('Existing GG Moments Storage Location (blank keeps current): ').strip() or None
  a.binding=input('Save Clip saved binding, e.g. alt+s (blank keeps current): ').strip() or None
 try:print(configure(a.root,a.clip_directory,a.binding))
 except Exception as e:p.exit(1,'SETUP STOPPED: '+str(e)+'\n')
