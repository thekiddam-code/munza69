"""Bulk UI runs against the real paired handler with generated audio and fake Windows render."""
import json,unittest,os
from sound_service import SoundService
from test_soundboard_browser import SoundboardBrowser,audio
from test_continuity import RecordedResult

class BulkSoundboard(SoundboardBrowser):
 def start_bulk(self,p,files):
  p.locator('#sb-bulk-add').click();p.locator('#sb-bulk-files').set_input_files(files);p.locator('#sb-bulk-rights').check();p.locator('#sb-bulk-start').click()
 def wait_bulk(self,p):p.wait_for_function("!document.querySelector('#sb-bulk-start').disabled",timeout=90000)
 def test_bulk_many_files_duplicates_errors_and_existing_output_survive(self):
  p=self.page();self.open(p);self.upload(p,'Original')
  lib=self.m.SOUND_SERVICE.library;original=lib.view();ident=original['sounds'][0]['id'];raw=lib.get(ident)[0]
  lib.output(self.m.SOUND_SERVICE.player.backend.devices()[0],original['revision']);p.evaluate('UmbraSoundboard.sync()');p.wait_for_function('UmbraSoundboard.library.output!==null')
  profile=self.m.SOUND_SERVICE.library.root/'audio_profile.json';profile.write_text('{"version":1,"enabled":false,"offset_db":-3,"ceiling_dbfs":-1,"max_boost_db":6,"speech":null}')
  profile_bytes=profile.read_bytes()
  files=[{'name':f'Batch {i}.wav','mimeType':'audio/wav','buffer':audio(.01+i*.0002)} for i in range(70)]
  files += [{'name':'Duplicate.wav','mimeType':'audio/wav','buffer':audio(.01)}, {'name':'Broken.wav','mimeType':'audio/wav','buffer':b'not wave audio'}]
  self.start_bulk(p,files);self.wait_bulk(p)
  self.assertIn('70 saved',p.locator('#sb-bulk-status').inner_text());self.assertIn('1 duplicates skipped',p.locator('#sb-bulk-status').inner_text());self.assertIn('1 failed',p.locator('#sb-bulk-status').inner_text())
  current=lib.view();self.assertEqual(len(current['sounds']),71);self.assertEqual(lib.get(ident)[0],raw);self.assertEqual(current['output'],self.m.SOUND_SERVICE.player.backend.devices()[0]);self.assertEqual(profile.read_bytes(),profile_bytes)
  restarted=SoundService(lib.root,self.m.SOUND_SERVICE.player.backend);self.assertEqual(restarted.library.view(),current)
  self.assertEqual(self.calls,[]);self.assertTrue(list((lib.root.parent/'soundboard_backups').glob('*.zip')))
  p.locator('#sb-bulk-status').scroll_into_view_if_needed();p.screenshot(path=os.environ.get('UMBRA_BULK_SCREENSHOT','bulk-soundboard-test.png'))
 def test_bulk_conflict_stops_without_replay_or_output_changes(self):
  p=self.page();self.open(p);self.upload(p,'Existing');before=self.m.SOUND_SERVICE.library.view()
  p.route('**/api/sounds/import',lambda r:r.fulfill(status=409,content_type='application/json',body=json.dumps({'error':'Another terminal changed the library'})))
  files=[{'name':f'Pending {i}.wav','mimeType':'audio/wav','buffer':audio(.01+i*.001)} for i in range(3)]
  self.start_bulk(p,files);self.wait_bulk(p)
  self.assertIn('0 saved',p.locator('#sb-bulk-status').inner_text());self.assertIn('2 not imported',p.locator('#sb-bulk-status').inner_text());self.assertEqual(self.m.SOUND_SERVICE.library.view(),before);self.assertEqual(self.calls,[])
 def test_bulk_cancel_before_save_and_permission_gate_preserve_library(self):
  p=self.page();self.open(p);before=self.m.SOUND_SERVICE.library.view()
  p.locator('#sb-bulk-add').click();p.locator('#sb-bulk-files').set_input_files([{'name':'A.wav','mimeType':'audio/wav','buffer':audio(.01)},{'name':'B.wav','mimeType':'audio/wav','buffer':audio(.02)}])
  p.locator('#sb-bulk-start').click();self.assertIn('Confirm permission',p.locator('#sb-bulk-status').inner_text());self.assertEqual(self.m.SOUND_SERVICE.library.view(),before)
  pending=[]
  def hold_first(route):
   if pending:route.continue_()
   else:pending.append(route)
  p.route('**/api/sounds/library',hold_first)
  p.locator('#sb-bulk-rights').check();p.locator('#sb-bulk-start').click();p.wait_for_timeout(100);p.locator('#sb-bulk-cancel').click()
  self.assertEqual(len(pending),1);pending[0].fulfill(status=200,content_type='application/json',body=json.dumps(self.m.SOUND_SERVICE.view()));self.wait_bulk(p)
  self.assertIn('0 saved',p.locator('#sb-bulk-status').inner_text());self.assertEqual(self.m.SOUND_SERVICE.library.view(),before);self.assertEqual(self.calls,[])

if __name__=='__main__':
 names=[n for n in unittest.defaultTestLoader.getTestCaseNames(BulkSoundboard) if n.startswith(('test_bulk_','test_sound_'))]
 result=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite(BulkSoundboard(n) for n in names))
 from pathlib import Path
 Path(os.environ.get('UMBRA_BULK_RESULTS','bulk-soundboard-results.json')).write_text(json.dumps({'passed':result.wasSuccessful(),'tests_run':result.testsRun,'passed_cases':result.successes,'failures':[{'test':str(t),'detail':d} for t,d in result.failures],'errors':[{'test':str(t),'detail':d} for t,d in result.errors]},indent=2))
 raise SystemExit(not result.wasSuccessful())
