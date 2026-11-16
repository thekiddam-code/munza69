"""Real browser audio graph/HTTP and persistence; host render device is an explicit fixture."""
import argparse,base64,io,json,math,struct,tempfile,unittest,wave,urllib.request,urllib.error,subprocess,shutil
from pathlib import Path
from unittest.mock import patch
from test_umbra_browser import UmbraBrowser
from test_continuity import RecordedResult
from sound_service import SoundService

def audio(seconds=2):
 b=io.BytesIO()
 with wave.open(b,'wb') as w:w.setparams((1,2,24000,0,'NONE','not compressed'));w.writeframes(b''.join(struct.pack('<h',round(5000*math.sin(i*.1))) for i in range(int(24000*seconds))))
 return b.getvalue()
class SoundboardBrowser(UmbraBrowser):
 def setUp(self):
  super().setUp();self.soundtmp=tempfile.TemporaryDirectory();self.old=self.m.SOUND_SERVICE
  class Output:
   def devices(s):return [{'id':0,'name':'FIXTURE Windows render output'}]
   def play(s,raw,device,volume,stop,started):self.calls.append(('sound-play',volume));started();stop.wait(.1)
  self.m.SOUND_SERVICE=SoundService(Path(self.soundtmp.name)/'soundboard',Output());self.audio=audio()
 def tearDown(self):self.m.SOUND_SERVICE.player.stop();self.m.SOUND_SERVICE=self.old;self.soundtmp.cleanup();super().tearDown()
 def open(self,p):
  p.locator('#simulatorNav').click();self.tab(p,'rocket');p.locator('#soundboard-toggle').click();p.wait_for_function('document.querySelector("#sb-status").textContent.includes("synchronized")')
 def upload(self,p,name='Test sound',preview=False):
  p.locator('#sb-add').click();p.locator('#sb-file').set_input_files({'name':name+'.wav','mimeType':'audio/wav','buffer':self.audio});p.wait_for_function('document.querySelector("#sb-import-status").textContent.includes("Ready to preview")');p.locator('#sb-rights').check()
  if preview:
   p.locator('#sb-preview').click();p.wait_for_function('UmbraSoundboard.previewing');p.locator('#sb-preview').click();p.wait_for_function('!UmbraSoundboard.previewing');self.assertEqual(self.calls,[])
  p.locator('#sb-save').click();p.wait_for_function('document.querySelector("#sb-editor").hidden');p.wait_for_function('document.querySelectorAll(".sb-sound").length>0')
 def req(self,path,data=None,paired=True):
  h={'Authorization':'Bearer test-client'} if paired else {}
  if data is not None:h['Content-Type']='application/json'
  r=urllib.request.Request(self.url+path,data=None if data is None else json.dumps(data).encode(),headers=h)
  try:
   with urllib.request.urlopen(r) as response:return response.status,response.read()
  except urllib.error.HTTPError as e:return e.code,e.read()
 def test_sound_upload_edit_move_delete_and_restart_without_chrome_dependency(self):
  p=self.page();self.open(p);self.upload(p,'First',preview=True);self.upload(p,'Second');p.locator('.sb-edit').first.click();p.locator('#sb-name').fill('Renamed');p.locator('#sb-edit-category').fill('Crew');p.locator('#sb-icon').select_option('crew');p.locator('#sb-favorite').check();p.locator('#sb-volume').fill('60');p.locator('#sb-save').click();p.wait_for_function('document.querySelector("#sb-editor").hidden');p.locator('.sb-edit').first.click();p.locator('#sb-down').click();p.wait_for_function('document.querySelector("#sb-import-status").textContent.includes("Order saved")');p.locator('#sb-cancel').click();self.assertIn('Second',p.locator('.sb-sound').first.inner_text());p.reload();p.wait_for_function('!!window.UmbraSoundboard');p.locator('#soundboard-toggle').click();p.wait_for_function('document.querySelector("#sb-status").textContent.includes("synchronized")');self.assertIn('Renamed',p.locator('.sb-sound').nth(1).inner_text());p.locator('#sb-favorites').check();self.assertEqual(p.locator('.sb-sound').count(),1);self.assertIn('Renamed',p.locator('.sb-sound').inner_text());p.locator('.sb-edit').click();p.on('dialog',lambda d:d.accept());p.locator('#sb-delete').click();p.wait_for_function('document.querySelector("#sb-editor").hidden');self.assertEqual(len(self.m.SOUND_SERVICE.library.view()['sounds']),1);self.assertEqual(self.calls,[])
 def test_sound_tap_plays_host_hold_previews_local_only_and_cancellation_stops(self):
  p=self.page();self.open(p);self.upload(p);p.locator('#soundboard details').locator('summary').click();p.locator('#sb-output-save').click();p.wait_for_function('document.querySelector("#sb-status").textContent.includes("output selected")');b=p.locator('.sb-sound');b.click();p.wait_for_function('document.querySelector("#sb-status").textContent.includes("PLAYING")');self.assertEqual(len([c for c in self.calls if c[0]=='sound-play']),1);p.wait_for_timeout(300);r=b.bounding_box();p.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2);p.mouse.down();p.wait_for_function('UmbraSoundboard.previewing');p.mouse.up();p.wait_for_function('!UmbraSoundboard.previewing');self.assertEqual(len([c for c in self.calls if c[0]=='sound-play']),1)
  b.dispatch_event('pointerdown',{'pointerId':4,'pointerType':'touch','button':0,'clientX':10,'clientY':10});p.wait_for_timeout(650);b.dispatch_event('pointercancel',{'pointerId':4,'pointerType':'touch'});p.wait_for_function('!UmbraSoundboard.previewing');b.dispatch_event('click');b.dispatch_event('click');self.assertEqual(len([c for c in self.calls if c[0]=='sound-play']),1)
 def test_sound_cached_private_preview_works_offline_and_no_mic_api_is_used(self):
  p=self.page();p.evaluate("() => { window.micRequests=0;if(navigator.mediaDevices)navigator.mediaDevices.getUserMedia=()=>{micRequests++;throw Error('Microphone must never open in B');}; }");self.open(p);self.upload(p);p.locator('.sb-edit').click();p.locator('#sb-preview').click();p.wait_for_function('UmbraSoundboard.previewing');p.locator('#sb-cancel').click();p.wait_for_function('!UmbraSoundboard.previewing');p.add_init_script("window.micRequests=0;if(navigator.mediaDevices)navigator.mediaDevices.getUserMedia=()=>{micRequests++;throw Error('Microphone must never open in B');};");p.route('**/api/sounds/**',lambda r:r.abort());p.reload();p.wait_for_function('window.UmbraSoundboard && UmbraSoundboard.library.sounds.length===1');p.locator('#soundboard-toggle').click();p.wait_for_function('document.querySelector("#sb-status").textContent.includes("OFFLINE")');p.context.set_offline(True);b=p.locator('.sb-sound');r=b.bounding_box();p.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2);p.mouse.down();p.wait_for_function('UmbraSoundboard.previewing');p.mouse.up();p.wait_for_function('!UmbraSoundboard.previewing');self.assertEqual(self.calls,[]);self.assertEqual(p.evaluate('micRequests'),0);p.context.set_offline(False);p.unroute('**/api/sounds/**');p.evaluate('UmbraSoundboard.sync()');p.wait_for_function('document.querySelector("#sb-status").textContent.includes("synchronized")');p.locator('#soundboard details summary').click();p.evaluate("() => {UmbraSoundCache.clear=async()=>{throw Error('Controlled cache failure');};}");p.locator('#sb-clear').click();p.wait_for_function('document.querySelector("#sb-status").textContent.includes("was not cleared")');self.assertEqual(len(self.m.SOUND_SERVICE.library.view()['sounds']),1)
 def test_sound_available_all_simulation_tabs_and_responsive_no_overlay_elsewhere(self):
  p=self.page();self.open(p);self.upload(p);p.locator('#sb-close').click()
  for tab in ['fortnite','minecraft','icarus']:
   p.evaluate('(tab)=>umbraOpenTab(tab)',tab);self.assertTrue(p.locator('#soundboard-toggle').is_visible());p.locator('#soundboard-toggle').click();self.assertTrue(p.locator('#soundboard').is_visible());p.locator('#sb-close').click()
  for width,height in [(393,851),(851,393),(1280,800)]:
   p.set_viewport_size({'width':width,'height':height});p.locator('#soundboard-toggle').click();self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'),width);self.assertTrue(p.locator('#sb-add').is_visible());p.locator('#sb-close').click()
  self.tab(p,'monitor');self.assertFalse(p.locator('#soundboard-toggle').is_visible());self.assertFalse(p.locator('#soundboard').is_visible());self.assertEqual(p.evaluate('typeof __icarusSoak'),'undefined')
 def test_sound_supported_link_import_and_delayed_preview_release_are_safe(self):
  payload=self.audio;mime='audio/wav'
  if shutil.which('ffmpeg'):
   result=subprocess.run(['ffmpeg','-v','error','-i','pipe:0','-f','mp3','pipe:1'],input=self.audio,capture_output=True,check=True,timeout=10);payload=result.stdout;mime='audio/mpeg'
  with patch('sound_service.import_page',return_value={'name':'Linked sound','source':'https://www.myinstants.com/en/instant/test/','mime':mime,'audio':base64.b64encode(payload).decode()}):
   p=self.page();self.open(p);p.locator('#sb-add').click();p.locator('#sb-rights').check();p.locator('#sb-url').fill('https://www.myinstants.com/en/instant/test/');p.locator('#sb-link').click();p.wait_for_function('document.querySelector("#sb-import-status").textContent.includes("Ready to preview")');self.assertEqual(p.locator('#sb-name').input_value(),'Linked sound');p.locator('#sb-save').click();p.wait_for_function('document.querySelector("#sb-editor").hidden')
  other=self.page();self.open(other);pending=[];other.route('**/api/sounds/audio?*',lambda r:pending.append(r));b=other.locator('.sb-sound');r=b.bounding_box();other.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2);other.mouse.down();other.wait_for_timeout(700);self.assertEqual(len(pending),1);other.mouse.up();pending[0].fulfill(status=200,content_type='audio/wav',body=self.audio);other.wait_for_timeout(300);self.assertFalse(other.evaluate('UmbraSoundboard.previewing'));self.assertEqual(self.calls,[])
  pending_import=[];p.route('**/api/sounds/link',lambda r:pending_import.append(r));p.locator('#sb-add').click();p.locator('#sb-rights').check();p.locator('#sb-url').fill('https://www.myinstants.com/en/instant/test/');p.locator('#sb-link').click();p.wait_for_timeout(200);self.assertEqual(len(pending_import),1);p.locator('#sb-add').click();self.assertFalse(p.locator('#sb-save').is_disabled());self.assertFalse(p.locator('#sb-link').is_disabled());pending_import[0].fulfill(status=200,content_type='application/json',body=json.dumps({'name':'Obsolete request','source':'https://www.myinstants.com/en/instant/test/','mime':'audio/wav','audio':base64.b64encode(self.audio).decode()}));p.wait_for_timeout(600);self.assertEqual(p.locator('#sb-name').input_value(),'')
 def test_sound_import_memory_cache_is_bounded_without_evicting_the_library(self):
  self.audio=audio(.1);p=self.page();self.open(p)
  for i in range(10):self.upload(p,'Tiny '+str(i))
  self.assertEqual(len(self.m.SOUND_SERVICE.library.view()['sounds']),10);self.assertEqual(p.evaluate('UmbraSoundboard.library.sounds.length'),10);self.assertLessEqual(p.evaluate('UmbraSoundboard.cacheStats.hotBlobs'),8)
 def test_sound_auth_limits_unknown_routes_and_missing_output_are_explicit(self):
  for path in ['/api/sounds/library','/api/sounds/audio?id=../../config.json']:self.assertEqual(self.req(path,paired=False)[0],401)
  self.assertEqual(self.req('/api/sounds/stop',{},paired=False)[0],401);self.assertEqual(self.req('/api/sounds/preview',{})[0],400);self.assertEqual(self.req('/api/sounds/audio?id=../../config.json')[0],404)
  p=self.page();self.open(p);self.upload(p);p.locator('.sb-sound').click();p.wait_for_function('document.querySelector("#sb-status").textContent.includes("Select an explicit")');self.assertEqual(self.calls,[])
  def fail_later(raw,device,volume,stop,started):started();stop.wait(.2);raise OSError('Controlled later output failure')
  self.m.SOUND_SERVICE.player.backend.play=fail_later;d=self.m.SOUND_SERVICE.library.view();self.m.SOUND_SERVICE.library.output(self.m.SOUND_SERVICE.player.backend.devices()[0],d['revision']);p.evaluate('UmbraSoundboard.sync()');p.wait_for_function('UmbraSoundboard.library.output!==null');p.locator('.sb-sound').click();p.wait_for_timeout(400);p.evaluate('UmbraSoundboard.sync()');p.wait_for_function('document.querySelector("#sb-status").textContent.includes("Controlled later output failure")');p.evaluate("() => {localStorage.removeItem('remoteDeckToken');umbraOpenTab('icarus');}");self.assertFalse(p.locator('#soundboard-toggle').is_visible())
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args()
 if a.runtime:
  import test_umbra_browser;test_umbra_browser.ROOT=a.runtime.resolve()
 names=[n for n in unittest.defaultTestLoader.getTestCaseNames(SoundboardBrowser) if n.startswith('test_sound_')];r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite(SoundboardBrowser(n) for n in names));a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
