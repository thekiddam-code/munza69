"""Real paired browser/handler; controlled backup latency, generated audio, fake render endpoint."""
import json,os,threading,time,unittest
from pathlib import Path
from unittest.mock import patch
from test_bulk_soundboard import BulkSoundboard
from test_soundboard_browser import audio
from test_continuity import RecordedResult
from sound_backup import backup as real_backup,inventory
from sound_service import SoundService

class VolumeBrowser(BulkSoundboard):
 def imported(self,p):
  self.open(p);self.start_bulk(p,[{'name':f'Imported {i}.wav','mimeType':'audio/wav','buffer':audio(.018+i*.001)} for i in range(3)]);self.wait_bulk(p)
  lib=self.m.SOUND_SERVICE.library;view=lib.view();lib.output(self.m.SOUND_SERVICE.player.backend.devices()[0],view['revision']);p.evaluate('UmbraSoundboard.sync()');p.wait_for_function('UmbraSoundboard.library.output!==null')
  profile=lib.root/'audio_profile.json';profile.write_text('{"version":1,"enabled":false,"offset_db":-3,"ceiling_dbfs":-1,"max_boost_db":6,"speech":null}')
  return lib,lib.view(),profile.read_bytes()
 def edit_volume(self,p,ident,value):
  p.locator(f'.sb-card:has([data-sound="{ident}"]) .sb-edit').click();p.locator('#sb-volume').fill(str(value))
 def test_volume_slow_verified_backup_confirms_one_bulk_sound_and_survives_devices_restart(self):
  p=self.page();lib,before,profile=self.imported(p);item=before['sounds'][1];ident=item['id'];raw={s['id']:lib.get(s['id'])[0] for s in before['sounds']};self.m.SOUND_SERVICE.preservation=None;done=threading.Event();seen=[]
  def slow(root):
   try:
    time.sleep(11);seen.append(lib._load()['sounds'][1]['volume']);return real_backup(root)
   finally:done.set()
  self.edit_volume(p,ident,72)
  try:
   with patch('sound_service.backup',side_effect=slow):
    p.locator('#sb-save').click();p.wait_for_function('document.querySelector("#sb-editor").hidden||document.querySelector("#sb-import-status").textContent.toLowerCase().includes("abort")',timeout=25000)
    self.assertTrue(p.locator('#sb-editor').is_hidden(),p.locator('#sb-import-status').inner_text())
  finally:self.assertTrue(done.wait(15),'Controlled backup must finish before cleanup')
  self.assertEqual(seen,[item['volume']],'Metadata must not change before verified backup');after=lib.view();self.assertEqual(after['revision'],before['revision']+1);self.assertEqual(after['output'],before['output']);self.assertEqual((lib.root/'audio_profile.json').read_bytes(),profile)
  for old,new in zip(before['sounds'],after['sounds']):self.assertEqual(new,{**old,**({'volume':.72} if old['id']==ident else {})});self.assertEqual(lib.get(old['id'])[0],raw[old['id']])
  restarted=SoundService(lib.root,self.m.SOUND_SERVICE.player.backend);self.assertEqual(restarted.library.view(),after)
  p.reload();p.wait_for_function('!!window.UmbraSoundboard');self.open(p);p.wait_for_function('UmbraSoundboard.library.sounds.some(s=>s.volume===.72)')
  phone=self.page(width=390,height=844);self.open(phone);phone.wait_for_function('UmbraSoundboard.library.sounds.some(s=>s.volume===.72)');self.edit_volume(phone,ident,19);phone.locator('#sb-save').click();phone.wait_for_function('document.querySelector("#sb-editor").hidden');self.assertEqual(lib.view()['sounds'][1]['volume'],.19);self.assertEqual(self.calls,[])
  phone.locator(f'[data-sound="{ident}"]').click();phone.wait_for_function('document.querySelector("#sb-status").textContent.includes("PLAYING")');self.assertEqual(self.calls,[('sound-play',.19)])
 def test_volume_failed_backup_keeps_draft_library_audio_and_routing(self):
  p=self.page();lib,before,profile=self.imported(p);files=inventory(lib.root);self.m.SOUND_SERVICE.preservation=None;self.edit_volume(p,before['sounds'][0]['id'],81)
  with patch('sound_service.backup',side_effect=OSError('Controlled backup failure')):
   p.locator('#sb-save').click();p.wait_for_function('document.querySelector("#sb-import-status").textContent.includes("Verified backup required")')
  self.assertEqual(p.locator('#sb-volume').input_value(),'81');self.assertTrue(p.locator('#sb-editor').is_visible());self.assertEqual(lib.view(),before);self.assertEqual(inventory(lib.root),files);self.assertEqual((lib.root/'audio_profile.json').read_bytes(),profile);self.assertEqual(self.calls,[])
 def test_volume_timeout_is_honest_preserves_draft_and_never_replays_write(self):
  p=self.page();lib,before,profile=self.imported(p);ident=before['sounds'][0]['id'];self.m.SOUND_SERVICE.preservation=None;done=threading.Event();writes=[];p.on('request',lambda req:writes.append(req.url) if req.url.endswith('/api/sounds/edit') else None)
  p.evaluate('''()=>{const original=setTimeout;window.setTimeout=(fn,delay,...args)=>original(fn,delay===180000?30:delay,...args);}''')
  def held(root):
   try:time.sleep(.2);return real_backup(root)
   finally:done.set()
  self.edit_volume(p,ident,62)
  with patch('sound_service.backup',side_effect=held):
   p.locator('#sb-save').click();p.wait_for_function('document.querySelector("#sb-import-status").textContent.includes("not confirmed")');self.assertTrue(done.wait(5))
  self.assertTrue(p.locator('#sb-editor').is_visible());self.assertEqual(p.locator('#sb-volume').input_value(),'62');self.assertIn('Refresh',p.locator('#sb-import-status').inner_text());p.wait_for_timeout(350);self.assertEqual(len(writes),1)
  p.locator('#sb-cancel').click();p.locator('#sb-refresh').click();p.wait_for_function('UmbraSoundboard.library.sounds.some(s=>s.volume===.62)');self.assertEqual(lib.view()['revision'],before['revision']+1);self.assertEqual((lib.root/'audio_profile.json').read_bytes(),profile);self.assertEqual(self.calls,[])

if __name__=='__main__':
 names=[n for n in unittest.defaultTestLoader.getTestCaseNames(VolumeBrowser) if n.startswith('test_volume_')];r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite(VolumeBrowser(n) for n in names));Path(os.environ.get('UMBRA_VOLUME_RESULTS','volume-results.json')).write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[(str(t),d) for t,d in r.failures],'errors':[(str(t),d) for t,d in r.errors],'skipped':[(str(t),d) for t,d in r.skipped]},indent=2));raise SystemExit(not r.wasSuccessful())
