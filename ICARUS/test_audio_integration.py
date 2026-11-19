"""Actual HTTP/Chromium, multi-terminal shared storage; native endpoints explicitly fixture-backed."""
import argparse,json,tempfile,unittest,urllib.request,urllib.error
from pathlib import Path
from unittest.mock import patch
from test_umbra_browser import UmbraBrowser
from test_continuity import RecordedResult
from test_audio_foundation import tone,F
from sound_service import SoundService
from sound_library import SoundLibrary
from sound_backup import inventory,verify_archive
from audio_service import AudioService
class AudioIntegration(UmbraBrowser):
 def setUp(self):
  super().setUp();self.tmpaudio=tempfile.TemporaryDirectory();self.previous=self.m.SOUND_SERVICE,self.m.AUDIO_SERVICE;self.root=Path(self.tmpaudio.name)/'soundboard_data';lib=SoundLibrary(self.root);lib.add(F,tone(.5,.2),0,True,'Existing B sound');lib.add({**F,'name':'Second existing sound'},tone(.7,.15),1,True,'Existing B sound');self.original=lib.view();self.original_files={n:(self.root/n).read_bytes() for n in inventory(self.root)['files']};self.capture_calls=[];self.output_calls=[]
  class Capture:
   def devices(s):return [{'id':0,'name':'Physical microphone A fixture','kind':'fixture'}, {'id':1,'name':'Physical microphone B fixture','kind':'fixture'}, {'id':2,'name':'SteelSeries Sonar - Microphone fixture','kind':'fixture virtual'}, {'id':3,'name':'SteelSeries Sonar - Stream fixture','kind':'fixture virtual'}]
   def sample(s,device,seconds,cancel):self.capture_calls.append(device);return tone(seconds,.1)
  class Output:
   def devices(s):return [{'id':0,'name':'Headphones fixture'},{'id':1,'name':'SteelSeries Sonar - Aux fixture'}]
   def play(s,raw,device,volume,cancel,started):self.output_calls.append((raw,device,volume));started();cancel.wait(.05)
  self.m.SOUND_SERVICE=SoundService(self.root,Output());self.m.AUDIO_SERVICE=AudioService(self.m.SOUND_SERVICE,Capture());self.m.SOUND_SERVICE.player.processor=self.m.AUDIO_SERVICE.processed;self.m.SOUND_SERVICE.player.profile_reader=self.m.AUDIO_SERVICE.profile
 def tearDown(self):self.m.SOUND_SERVICE.player.stop();self.m.SOUND_SERVICE,self.m.AUDIO_SERVICE=self.previous;self.tmpaudio.cleanup();super().tearDown()
 def request(self,path,data=None,paired=True):
  headers={'Authorization':'Bearer test-client'} if paired else {}
  if data is not None:headers['Content-Type']='application/json'
  req=urllib.request.Request(self.url+path,data=None if data is None else json.dumps(data).encode(),headers=headers)
  try:
   with urllib.request.urlopen(req) as r:return r.status,r.read(),r.headers
  except urllib.error.HTTPError as e:return e.code,e.read(),e.headers
 def open(self,p):
  p.evaluate("umbraOpenTab('icarus')");p.locator('#soundboard-toggle').click();p.wait_for_function('UmbraSoundboard.library.sounds.length===2');p.locator('#audio-toggle').click();p.wait_for_function('document.querySelector("#audio-input").options.length===4')
 def test_audio_existing_library_is_shared_between_pc_tablet_phone_without_migration(self):
  pc=self.page();tablet=self.page(width=820,height=900);phone=self.page(width=393,height=851)
  for p in [pc,tablet,phone]:self.open(p);self.assertEqual(p.evaluate('UmbraSoundboard.library.sounds'),self.original['sounds']);self.assertEqual(p.evaluate('typeof __icarusSoak'),'undefined')
  tablet.locator('.sb-edit').first.click();tablet.locator('#sb-name').fill('Shared renamed sound');tablet.locator('#sb-save').click();tablet.wait_for_function('document.querySelector("#sb-editor").hidden')
  for p in [pc,phone]:p.evaluate('() => {document.activeElement.blur();UmbraSoundboard.sync();}');p.wait_for_function('UmbraSoundboard.library.sounds[0].name==="Shared renamed sound"')
  pc.on('dialog',lambda d:d.accept());pc.locator('#audio-aux').click();pc.wait_for_function('UmbraSoundboard.library.output?.name.includes("Sonar - Aux")');self.assertIn('Sonar - Aux',self.m.SOUND_SERVICE.library.view()['output']['name']);self.assertEqual(self.capture_calls,[]);archives=list((self.root.parent/'soundboard_backups').glob('*.zip'));self.assertEqual(len(archives),1);manifest=verify_archive(archives[0]);self.assertEqual(manifest['source']['sounds'],2)
  for name,raw in self.original_files.items():
   if name.endswith('.wav'):self.assertEqual((self.root/name).read_bytes(),raw)
 def test_audio_missing_server_folder_never_prunes_existing_browser_library(self):
  p=self.page();self.open(p);original=p.evaluate('UmbraSoundboard.library.sounds');(self.root/'library.json').rename(self.root/'library.original.json');p.evaluate('() => {document.activeElement.blur();UmbraSoundboard.sync();}');p.wait_for_function('document.querySelector("#sb-status").textContent.includes("STORAGE CONFLICT")');self.assertEqual(p.evaluate('UmbraSoundboard.library.sounds'),original);self.assertTrue(p.locator('#sb-add').is_disabled());(self.root/'library.original.json').rename(self.root/'library.json');p.evaluate('UmbraSoundboard.sync()');p.wait_for_function('document.querySelector("#sb-status").textContent.includes("synchronized")');self.assertEqual(self.m.SOUND_SERVICE.library.view(),self.original)
 def test_audio_verified_backup_download_is_authenticated_and_exact(self):
  self.assertEqual(self.request('/api/sounds/backup',{},paired=False)[0],401);status,body,_=self.request('/api/sounds/backup',{});d=json.loads(body);self.assertTrue(d['verified']);self.assertEqual(d['source']['sounds'],2);self.assertEqual(self.request('/api/sounds/backup?id='+d['id'],paired=False)[0],401);status,raw,_=self.request('/api/sounds/backup?id='+d['id']);self.assertEqual(status,200);path=self.root.parent/'download.zip';path.write_bytes(raw);m=verify_archive(path);self.assertEqual(m['source']['files'],inventory(self.root)['files']);self.assertEqual(self.m.SOUND_SERVICE.library.view(),self.original);self.assertEqual(self.request('/api/sounds/backup?id=../../config.json')[0],404)
 def test_audio_input_sampling_is_local_consent_only_and_status_is_not_capture(self):
  self.assertEqual(self.request('/api/audio/status',paired=False)[0],401);_,body,_=self.request('/api/audio/status');d=json.loads(body);self.assertTrue(d['sonar_detected']);self.assertFalse(d['injection_verified']);self.assertEqual(self.capture_calls,[]);device=d['inputs'][0]
  with patch.object(self.m.Handler,'local_host',return_value=False):self.assertEqual(self.request('/api/audio/calibrate',{'device':device,'consent':True})[0],403)
  self.assertEqual(self.request('/api/audio/calibrate',{'device':device,'consent':False})[0],400);self.assertEqual(self.capture_calls,[])
  status,body,_=self.request('/api/audio/calibrate',{'device':device,'consent':True});result=json.loads(body);self.assertEqual(status,200);self.assertEqual(len(self.capture_calls),1);self.assertNotIn('RIFF',body.decode());self.assertNotIn('audio',result);self.assertEqual(self.m.SOUND_SERVICE.library.view(),self.original);profile_before=self.m.AUDIO_SERVICE.path.read_bytes();status,_,_=self.request('/api/audio/measure',{'device':device,'consent':True});self.assertEqual(status,200);self.assertEqual(self.m.AUDIO_SERVICE.path.read_bytes(),profile_before)
 def test_audio_emergency_during_backup_does_not_start_a_late_capture(self):
  p=self.page();self.open(p);routes=[];p.route('**/api/audio/prepare',lambda r:routes.append(r));p.locator('#audio-consent').check();p.locator('#audio-calibrate').click();p.wait_for_timeout(200);self.assertEqual(len(routes),1);p.locator('#audio-reset').click();p.wait_for_function('document.querySelector("#audio-status").textContent.includes("processing disabled")');routes[0].fulfill(status=200,content_type='application/json',body='{"verified":true}');p.wait_for_timeout(250);self.assertEqual(self.capture_calls,[])
 def test_audio_normalized_private_preview_and_public_output_use_same_pcm(self):
  p=self.page();self.open(p);p.locator('#audio-consent').check();p.locator('#audio-calibrate').click();p.wait_for_function('document.querySelector("#audio-status").textContent.includes("Calibration saved")');p.locator('#audio-enabled').check();p.locator('#audio-save').click();p.wait_for_function('window.UmbraAudioProfile?.enabled');item=self.original['sounds'][0];status,raw,headers=self.request('/api/audio/processed?id='+item['id']);self.assertEqual(status,200);self.assertEqual(float(headers['X-Umbra-Preview-Gain']),1)
  device=self.m.SOUND_SERVICE.player.backend.devices()[0];self.m.SOUND_SERVICE.library.output(device,self.m.SOUND_SERVICE.library.view()['revision']);self.request('/api/sounds/play',{'id':item['id'],'requestId':'calibrated01'});self.assertEqual(self.output_calls[0][0],raw);self.assertEqual(self.output_calls[0][2],1);before=len(self.output_calls)
  b=p.locator('.sb-sound').first;b.scroll_into_view_if_needed();r=b.bounding_box();p.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2);p.mouse.down();p.wait_for_function('UmbraSoundboard.previewing');p.mouse.up();p.wait_for_function('!UmbraSoundboard.previewing');self.assertEqual(len(self.output_calls),before);self.assertEqual(self.m.SOUND_SERVICE.library.get(item['id'])[0],self.original_files[item['id']+'.wav']);p.locator('#audio-reset').click();p.wait_for_function('document.querySelector("#audio-status").textContent.includes("processing disabled")');self.assertFalse(self.m.AUDIO_SERVICE.profile()['enabled'])
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args()
 if a.runtime:
  import test_umbra_browser;test_umbra_browser.ROOT=a.runtime.resolve()
 names=[n for n in unittest.defaultTestLoader.getTestCaseNames(AudioIntegration) if n.startswith('test_audio_')];r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite(AudioIntegration(n) for n in names));a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
