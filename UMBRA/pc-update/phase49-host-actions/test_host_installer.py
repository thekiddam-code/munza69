import importlib.util,json,tempfile,unittest,subprocess,os,socket
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
REFERENCE=Path(os.environ.get('ICARUS_PHASE49_REFERENCE','/workspace/icarus-bulk-reference'))
spec=importlib.util.spec_from_file_location('installer',HERE/'apply_host_actions.py');installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
spec=importlib.util.spec_from_file_location('configure',HERE/'configure_host_actions.py');setup=importlib.util.module_from_spec(spec);spec.loader.exec_module(setup)
class InstallerTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);baseline=json.loads((HERE/'manifest.json').read_text())['baseline_commit'];self.source=subprocess.check_output(['git','show',baseline+':ICARUS/server.py'],cwd=REFERENCE)
  (self.root/'server.py').write_bytes(self.source);(self.root/'config.json').write_text('{"macros":{"Save Clip":["alt","s"],"Copy":["ctrl","c"]},"preserve":true}');(self.root/'soundboard_data').mkdir();(self.root/'soundboard_data/library.json').write_text('{"private":"unchanged fixture"}')
 def tearDown(self):self.tmp.cleanup()
 def test_install_idempotence_and_code_rollback_preserve_all_private_settings(self):
  before={p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file() and p.name!='server.py'}
  with patch.object(installer,'running',return_value=False):
   installer.apply(self.root);self.assertEqual('new',installer.preflight(self.root)[2]);self.assertIn('Already',installer.apply(self.root));backup=next((self.root/'umbra_host_code_backups').iterdir());installer.restore(self.root,backup)
  self.assertEqual(self.source,(self.root/'server.py').read_bytes());self.assertFalse((self.root/'umbra_host_actions.py').exists())
  for name,data in before.items():self.assertEqual(data,(self.root/name).read_bytes())
 def test_modified_source_running_server_or_unknown_existing_module_are_refused(self):
  with patch.object(installer,'running',return_value=True):
   with self.assertRaisesRegex(ValueError,'stop'):installer.apply(self.root)
  (self.root/'umbra_host_actions.py').write_text('user owned module')
  with self.assertRaisesRegex(ValueError,'differs'):installer.preflight(self.root)
  self.assertEqual(self.source,(self.root/'server.py').read_bytes())
 def test_local_setup_only_updates_explicit_saved_binding_and_storage(self):
  folder=self.root/'actual-clips';folder.mkdir();(self.root/'umbra_host_actions.json').write_text('{"arctis_output":{"id":"chosen","name":"Arctis"},"other":true}')
  before=(self.root/'soundboard_data/library.json').read_bytes()
  with patch.object(setup.socket,'create_connection',side_effect=OSError):setup.configure(self.root,str(folder),'ctrl+f8')
  config=json.loads((self.root/'config.json').read_text());self.assertTrue(config['preserve']);self.assertEqual(['ctrl','c'],config['macros']['Copy']);self.assertEqual(['ctrl','f8'],config['macros']['Save Clip'])
  saved=json.loads((self.root/'umbra_host_actions.json').read_text());self.assertEqual('chosen',saved['arctis_output']['id']);self.assertEqual(str(folder),saved['moments_clip_directory']);self.assertEqual(before,(self.root/'soundboard_data/library.json').read_bytes())
if __name__=='__main__':unittest.main(verbosity=2)
