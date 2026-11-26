"""Temporary-library installer safety checks; never point these at a live installation."""
import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
from unittest.mock import patch,Mock
from sound_library import SoundLibrary
from sound_backup import inventory
from test_sound_services import clip,FIELDS
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('volume_installer',HERE/'apply_volume_fix.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class VolumeInstaller(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'PC';self.root.mkdir();(self.root/'server.py').write_text('# isolated fixture')
  for name in ['web/umbra/soundboard.js','sound_library.py','sound_backup.py','sound_service.py']:
   dest=self.root/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(HERE.parent/'phase49/payload'/name,dest)
  self.original=(self.root/mod.SCRIPT).read_bytes();self.lib=SoundLibrary(self.root/'soundboard_data')
  for i in range(65):self.lib.add({**FIELDS,'name':f'Sound {i}'},clip(.001),self.lib.view()['revision'],True,'Installer fixture')
  self.lib.output({'id':3,'name':'Retained headphones'},self.lib.view()['revision']);(self.lib.root/'audio_profile.json').write_text('{"fixture":"unchanged","enabled":false}')
  self.before=inventory(self.lib.root);(self.root/'voyage-private.json').write_bytes(b'untouched voyage fixture')
 def tearDown(self):self.tmp.cleanup()
 def unchanged(self):
  self.assertEqual(inventory(self.lib.root),self.before);self.assertEqual((self.root/'voyage-private.json').read_bytes(),b'untouched voyage fixture')
 def test_install_real_verified_backup_repeat_and_rollback_with_65_sounds(self):
  with patch.object(mod,'server_running',return_value=False):
   self.assertIn('Applied soundboard.js only',mod.apply(self.root));self.assertEqual(mod.preflight(self.root)[2],'new');self.unchanged()
   archives=list((self.root/'soundboard_backups').glob('*.zip'));self.assertEqual(len(archives),1)
   from sound_backup import verify_archive
   self.assertEqual(verify_archive(archives[0])['source'],self.before)
   self.assertIn('Already applied',mod.apply(self.root));self.assertEqual(len(list((self.root/'soundboard_backups').glob('*.zip'))),1)
   backup=next((self.root/'umbra_volume_code_backups').iterdir());self.assertIn('restored',mod.restore(self.root,backup));self.assertEqual((self.root/mod.SCRIPT).read_bytes(),self.original);self.unchanged()
 def test_preflight_read_only_running_server_and_unknown_code_refused(self):
  self.assertEqual(mod.preflight(self.root)[2],'old');self.assertFalse((self.root/'umbra_volume_code_backups').exists())
  with patch.object(mod,'server_running',return_value=True):
   with self.assertRaisesRegex(ValueError,'Stop'):mod.apply(self.root)
  (self.root/'sound_service.py').write_text('unknown implementation')
  with self.assertRaisesRegex(ValueError,'Unrecognized'):mod.preflight(self.root)
  self.assertEqual((self.root/mod.SCRIPT).read_bytes(),self.original);self.unchanged()
 def test_missing_corrupt_and_failed_backup_never_replace_code(self):
  with patch.object(mod,'server_running',return_value=False):
   with patch.object(mod.subprocess,'run',return_value=Mock(returncode=1,stdout='',stderr='controlled disk failure')):
    with self.assertRaisesRegex(ValueError,'backup failed'):mod.apply(self.root)
   self.unchanged();self.assertEqual((self.root/mod.SCRIPT).read_bytes(),self.original)
   library=self.lib.root/'library.json';original=library.read_bytes();library.write_bytes(b'not json')
   with self.assertRaisesRegex(ValueError,'backup failed'):mod.apply(self.root)
   self.assertEqual(library.read_bytes(),b'not json');library.write_bytes(original)
   library.unlink()
   with self.assertRaisesRegex(ValueError,'not found'):mod.apply(self.root)
   library.write_bytes(original);self.unchanged()
 def test_linked_path_and_tampered_restore_refused(self):
  script=self.root/mod.SCRIPT;outside=Path(self.tmp.name)/'outside.js';outside.write_bytes(self.original);script.unlink();script.symlink_to(outside)
  with self.assertRaisesRegex(ValueError,'Linked'):mod.preflight(self.root)
  script.unlink();script.write_bytes(self.original)
  with patch.object(mod,'server_running',return_value=False):
   mod.apply(self.root);backup=next((self.root/'umbra_volume_code_backups').iterdir());(backup/mod.SCRIPT).write_bytes(b'bad backup')
   with self.assertRaisesRegex(ValueError,'checksum'):mod.restore(self.root,backup)
  self.assertEqual(mod.preflight(self.root)[2],'new');self.unchanged()
 def test_failed_atomic_install_restores_original_script(self):
  real=mod.atomic_write
  def fail(path,data):
   if data!=self.original:raise OSError('controlled code write failure')
   return real(path,data)
  with patch.object(mod,'server_running',return_value=False),patch.object(mod,'atomic_write',side_effect=fail):
   with self.assertRaisesRegex(OSError,'controlled'):mod.apply(self.root)
  self.assertEqual((self.root/mod.SCRIPT).read_bytes(),self.original);self.unchanged()
if __name__=='__main__':unittest.main(verbosity=2)
