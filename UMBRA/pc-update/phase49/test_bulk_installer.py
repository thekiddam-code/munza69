import importlib.util,tempfile,unittest,subprocess,json,shutil,os
from pathlib import Path
from unittest.mock import patch
src=Path(__file__).resolve().parent
if 'ICARUS_PHASE49_REFERENCE' not in os.environ:raise SystemExit('Set ICARUS_PHASE49_REFERENCE to the isolated Phase 4.9 git checkout root; never run against the live installation.')
ref=Path(os.environ['ICARUS_PHASE49_REFERENCE']).resolve()
spec=importlib.util.spec_from_file_location('bulk_update',src/'apply_bulk_update.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Installer(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'ICARUS';self.root.mkdir();(self.root/'server.py').write_text('# isolated fixture')
  for name in json.loads((src/'manifest.json').read_text())['files']:
   target=self.root/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(subprocess.check_output(['git','show','HEAD:ICARUS/'+name],cwd=ref))
  self.original={name:(self.root/name).read_bytes() for name in json.loads((src/'manifest.json').read_text())['files']}
 def tearDown(self):self.tmp.cleanup()
 def seed(self,empty=False):
  import sys;sys.path.insert(0,str(ref/'ICARUS'))
  from sound_library import SoundLibrary
  from test_sound_services import clip,FIELDS
  lib=SoundLibrary(self.root/'soundboard_data')
  if not empty:lib.add(FIELDS,clip(),0,True,'Installer fixture')
  lib.output({'id':2,'name':'Retained output'},lib.view()['revision'])
  (lib.root/'audio_profile.json').write_text('{"enabled":false,"fixture":"preserve exactly"}')
  return {p.name:p.read_bytes() for p in lib.root.iterdir() if p.is_file()}
 def test_apply_preserves_audio_profiles_output_and_is_idempotent_then_restores_code(self):
  before=self.seed()
  with patch.object(module,'server_running',return_value=False):
   self.assertIn('Applied four',module.apply(self.root));self.assertEqual(module.preflight(self.root)[2],'new');self.assertIn('Already applied',module.apply(self.root))
   self.assertEqual(before,{p.name:p.read_bytes() for p in (self.root/'soundboard_data').iterdir() if p.is_file()})
   backup=next((self.root/'umbra_bulk_code_backups').iterdir());self.assertIn('restored',module.restore(self.root,backup))
   self.assertEqual(self.original,{name:(self.root/name).read_bytes() for name in self.original})
 def test_mismatch_running_server_and_missing_library_never_change_code(self):
  with patch.object(module,'server_running',return_value=True):
   with self.assertRaisesRegex(ValueError,'Stop'):module.apply(self.root)
  with patch.object(module,'server_running',return_value=False):
   with self.assertRaisesRegex(ValueError,'not found'):module.apply(self.root)
  (self.root/'sound_service.py').write_text('different user source')
  with self.assertRaisesRegex(ValueError,'differs'):module.preflight(self.root)
  for name,data in self.original.items():
   if name!='sound_service.py':self.assertEqual(data,(self.root/name).read_bytes())
 def test_explicit_empty_library_keeps_output_metadata(self):
  before=self.seed(True)
  with patch.object(module,'server_running',return_value=False):self.assertIn('Applied four',module.apply(self.root,new_library=True))
  self.assertEqual(before,{p.name:p.read_bytes() for p in (self.root/'soundboard_data').iterdir() if p.is_file()})
 def test_rollback_refuses_large_library(self):
  self.seed()
  with patch.object(module,'server_running',return_value=False):
   module.apply(self.root);backup=next((self.root/'umbra_bulk_code_backups').iterdir());library=self.root/'soundboard_data/library.json';data=json.loads(library.read_text());data['sounds']=data['sounds']*65;library.write_text(json.dumps(data))
   with self.assertRaisesRegex(ValueError,'larger library'):module.restore(self.root,backup)
   self.assertEqual(module.preflight(self.root)[2],'new')
if __name__=='__main__':unittest.main(verbosity=2)
