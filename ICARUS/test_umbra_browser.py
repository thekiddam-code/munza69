"""Real HTTP/Chromium companion, TV socket and host input explicitly stubbed."""
import argparse,importlib.util,json,os,sys,tempfile,threading,types,unittest
from pathlib import Path
from playwright.sync_api import sync_playwright
from test_continuity import RecordedResult
ROOT=Path(__file__).resolve().parent
class UmbraBrowser(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.calls=[];sys.modules['pyautogui']=types.SimpleNamespace(**{n:(lambda *a,_n=n,**k:cls.calls.append((_n,a))) for n in ['press','hotkey','keyUp','mouseUp','mouseDown','keyDown','write']});spec=importlib.util.spec_from_file_location('umbra_test_host',ROOT/'server.py');cls.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.m);cls.tmp=tempfile.TemporaryDirectory();cls.m.TV_FILE=Path(cls.tmp.name)/'tv.json';cls.m.TV_FILE.write_text('{"ip":"192.168.1.99","token":"fixture"}');cls.m.DEVICES_FILE=Path(cls.tmp.name)/'tokens.json';cls.m.ICARUS_KEY='test-host';cls.m.TOKENS={cls.m.token_hash('test-client')};cls.m.PIN='fixture';
  class WS:
   def settimeout(self,*args):pass
   def recv(self):return '{"event":"ms.channel.connect","data":{"token":"fixture"}}'
   def send(self,msg):cls.calls.append(('tv',json.loads(msg)))
   def close(self):pass
  cls.m.create_connection=lambda *a,**k:WS();cls.server=cls.m.http.server.ThreadingHTTPServer(('127.0.0.1',0),cls.m.Handler);threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url=f'http://127.0.0.1:{cls.server.server_port}';cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(executable_path=os.environ.get('ICARUS_CHROMIUM') or None)
 @classmethod
 def tearDownClass(cls):cls.m.TV_SERVICE.close();cls.browser.close();cls.pw.stop();cls.server.shutdown();cls.tmp.cleanup()
 def setUp(self):self.contexts=[];self.errors=[];self.calls.clear();self.m.ICARUS_BRIDGE.update(telemetry=None,updated=0,commands=[],next_id=1);self.m.TV_SERVICE.reconfigure()
 def tearDown(self):
  for c in self.contexts:c.close()
  self.assertEqual(self.errors,[])
 def page(self,width=1280,height=800,pc=False):
  c=self.browser.new_context(viewport={'width':width,'height':height},has_touch=True);self.contexts.append(c);c.add_init_script("localStorage.setItem('remoteDeckToken','test-client');sessionStorage.setItem('icarusHostKey','test-host');window.__icarusSeed=10101;");p=c.new_page();p.on('pageerror',lambda e:self.errors.append(str(e)));p.goto(self.url+('/icarus.html?icarus_soak=1' if pc else '/'));p.wait_for_function('!!window.__icarusSoak' if pc else '!!window.UmbraApp');
  if not pc:p.wait_for_function('UmbraApp.online');p.wait_for_function('document.querySelector("#umbra-tv-capabilities").textContent.includes("TV configured")')
  return p
 def tab(self,p,name):p.locator(f'nav [data-tab="{name}"]').click()
 def test_preserved_departments_offline_icons_and_adaptive_screenshots(self):
  p=self.page();out=Path('/workspace/work/phase4a_reports/screenshots');out.mkdir(parents=True,exist_ok=True)
  for size,label in [({'width':1280,'height':800},'tablet'),({'width':393,'height':851},'phone'),({'width':851,'height':393},'phone_landscape'),({'width':820,'height':900},'intermediate')]:
   p.set_viewport_size(size)
   for tab in ['home','monitor','icarus','tv','macros','settings']:
    self.tab(p,tab);p.screenshot(path=str(out/(label+'_'+tab+'.png')));self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'),size['width']);self.assertGreater(p.locator('svg.umbra-icon').count(),15)
  self.assertEqual(p.locator('script[src*="http"],link[href*="http"]').count(),0)
 def test_existing_authenticated_tv_commands_and_managed_timer_cancel(self):
  p=self.page();self.tab(p,'tv');p.locator('#umbra-remote-grid [data-tv=home]').tap();p.wait_for_function('document.querySelector("#tvStatus").textContent.includes("sent")');self.assertEqual(self.calls[-1][1]['params']['DataOfCmd'],'KEY_HOME');p.on('dialog',lambda d:d.accept());p.locator('#umbra-timer-start').click();p.wait_for_function('document.querySelector("#umbra-timer-status").textContent.includes("scheduled")');p.locator('#umbra-timer-cancel').click();p.wait_for_function('document.querySelector("#umbra-timer-status").textContent.includes("cancelled")');self.assertEqual(len(self.calls),1)
 def test_profile_edit_save_cancel_undo_resize_remap_reload_and_invalid_overlap(self):
  p=self.page();self.tab(p,'tv');p.locator('#umbra-layout-edit').click();p.locator('#edit-label').fill('Quiet TV');p.locator('#edit-key').select_option('mute');p.locator('#edit-icon').select_option('mute');p.locator('#umbra-layout-apply').click();self.assertEqual(self.calls,[]);p.locator('#umbra-layout-undo').click();self.assertEqual(p.locator('#edit-label').input_value(),'Power Off');p.locator('#edit-label').fill('Quiet TV');p.locator('#edit-key').select_option('mute');p.locator('#edit-w').fill('1');p.locator('#umbra-layout-apply').click();p.locator('#umbra-profile-name').fill('Tablet one');p.locator('#umbra-layout-save').click();self.assertEqual(p.locator('#umbra-profile').input_value(),'Tablet one');p.reload();p.wait_for_function('!!window.UmbraApp');self.tab(p,'tv');self.assertEqual(p.locator('#umbra-profile').input_value(),'Tablet one');self.assertTrue(p.locator('#umbra-remote-grid [data-tv=mute]').first.is_visible());p.locator('#umbra-layout-edit').click();p.locator('#edit-x').fill('100');p.locator('#umbra-layout-apply').click();self.assertIn('bounds',p.locator('#umbra-layout-status').inner_text());p.locator('#umbra-layout-cancel').click();self.assertEqual(self.calls,[]);p.set_viewport_size({'width':393,'height':851});self.assertEqual(p.locator('#umbra-profile').input_value(),'Factory')
 def test_right_hand_cluster_stays_fixed_when_secondary_panel_expands(self):
  p=self.page();self.tab(p,'tv');b=p.locator('#umbra-remote-grid [data-tv=ok]');before=b.bounding_box();self.assertGreater(before['x'],640);p.locator('.lounge-secondary details summary').click();after=b.bounding_box();self.assertEqual((before['x'],before['y']),(after['x'],after['y']));self.assertGreaterEqual(before['height'],52)
 def test_real_camera_styles_follow_and_stale_unknown_without_source_mutation(self):
  pc=self.page(pc=True);t=self.page();self.tab(t,'icarus');t.wait_for_function('document.querySelector("#umbra-camera-source").textContent.includes("LIVE STATE PROJECTION")');before=pc.evaluate('__icarusSoak.snapshot()');t.locator('#umbra-crew-query').fill('Frank');t.locator('[data-follow="Frank Morrow"]').click();t.locator('#umbra-camera-style').select_option('state51');self.assertIn('51ST STATE STYLE',t.locator('#umbra-camera-source').inner_text());self.assertEqual(t.locator('#umbra-camera-frame .canadian-art').count(),4);t.locator('#umbra-camera-expand').click();self.assertTrue(t.locator('.camera-enlarged').is_visible());t.keyboard.press('Escape');self.assertEqual(t.locator('.camera-enlarged').count(),0);self.assertEqual(pc.evaluate('__icarusSoak.snapshot()'),before);self.m.ICARUS_BRIDGE['updated']=0;t.evaluate('icarusPoll()');t.wait_for_function('document.querySelector("#umbra-camera-source").textContent.includes("NO FRESH CAMERA")');self.assertEqual(t.locator('#umbra-camera-frame .camera-actor').count(),0)
 def test_arcade_loads_local_gifs_reduced_motion_and_separate_off_defaults(self):
  p=self.page();self.tab(p,'settings');self.assertFalse(p.locator('#umbra-anomalies').is_checked());self.assertFalse(p.locator('#umbra-arcade').is_checked());p.locator('#umbra-arcade-archive summary').click();p.wait_for_selector('#umbra-arcade-gallery button');self.assertEqual(p.locator('#umbra-arcade-gallery button').count(),6);p.locator('#umbra-arcade-gallery button').first.click();self.assertTrue(p.locator('#umbra-arcade-preview').get_attribute('src').endswith('.gif'));p.wait_for_function('document.querySelector("#umbra-arcade-preview").naturalWidth===128');p.emulate_media(reduced_motion='reduce');p.wait_for_function('document.querySelector("#umbra-arcade-preview").src.endsWith(".png")');p.locator('#umbra-anomalies').check();p.locator('#umbra-arcade').check();p.reload();p.wait_for_function('!!window.UmbraApp');self.tab(p,'settings');self.assertTrue(p.locator('#umbra-anomalies').is_checked());self.assertTrue(p.locator('#umbra-arcade').is_checked());self.assertEqual(self.calls,[]);self.assertEqual(self.m.ICARUS_BRIDGE['commands'],[])
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--report',default='umbra_browser.json');args=ap.parse_args();r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(UmbraBrowser));Path(args.report).write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
