"""Real authenticated HTTP and Chromium UI, Windows measurements/input explicitly stubbed."""
import argparse,json,time,unittest,urllib.request,urllib.error
from pathlib import Path
from types import SimpleNamespace
from test_umbra_browser import UmbraBrowser
from test_continuity import RecordedResult
from windows_control import WindowsControl
from windows_monitor import MonitorService
from windows_icons import png
class WindowsIntegration(UmbraBrowser):
 def setUp(self):
  super().setUp();self.oldmonitor=self.m.WINDOWS_MONITOR;self.oldcontrol=self.m.WINDOWS_CONTROL
  class Probe:
   def sample(s):return {'supported':True,'platform':'Windows','cpu_model':'FIXTURE CPU — test data','cores':4,'threads':8,'os':'Windows fixture','cpu_percent':37.5,'per_core_percent':[25,50],'frequency_mhz':2700,'cpu_temperature_c':None,'memory':{'total':16000000000,'used':8000000000,'available':8000000000,'percent':50},'gpus':[{'model':'FIXTURE GPU','source':'test fixture','utilization_percent':25}],'drives':[{'name':'C:','mount':'C:\\','total':1000000000000,'used':500000000000,'free':500000000000,'percent':50}],'interfaces':[{'name':'Fixture Ethernet','ipv4':['192.168.1.10'],'link_up':True,'upload_bytes_sec':100,'download_bytes_sec':200}],'disk_activity':{'read_bytes_sec':100,'write_bytes_sec':20},'battery':{'percent':83,'charging':True},'uptime_seconds':3600,'power_scheme':None,'network_note':'Fixture link only','sensor_note':'Unsupported sensors are unavailable','process_note':'Fixture processes','processes':[{'name':'fixture','pid':i,'ram_bytes':104857600,'cpu_percent':1} for i in range(20)],'warming_up':False}
  self.m.WINDOWS_MONITOR=MonitorService(Probe(),interval=.3);self.m.WINDOWS_MONITOR.collect()
  self.m.WINDOWS_CONTROL=WindowsControl(self.m.pg,system='Windows',discover=lambda:[{'name':'Google Chrome','kind':'link','path':'fixture.lnk','target':'fixture.exe'}],validate=lambda r:True,icon=lambda *a:png(1,1,b'\0\xff\xff\xff'),launch=lambda r:self.calls.append(('launch',r['name'])));self.m.WINDOWS_CONTROL.scan()
 def tearDown(self):
  self.m.WINDOWS_MONITOR.stop_event.set();self.m.WINDOWS_MONITOR=self.oldmonitor;self.m.WINDOWS_CONTROL=self.oldcontrol;super().tearDown()
 def req(self,path,data=None,paired=True,origin=None):
  headers={'Authorization':'Bearer test-client'} if paired else {}
  if data is not None:headers['Content-Type']='application/json'
  if origin:headers['Origin']=origin
  r=urllib.request.Request(self.url+path,data=None if data is None else json.dumps(data).encode(),headers=headers)
  try:
   with urllib.request.urlopen(r) as response:return response.status,response.read()
  except urllib.error.HTTPError as e:return e.code,e.read()
 def test_win_monitor_updates_is_confined_and_responsive(self):
  p=self.page();self.tab(p,'monitor');p.wait_for_function('document.querySelector("#windows-metrics").textContent.includes("FIXTURE CPU")');self.assertIn('Unavailable',p.locator('#windows-metrics').inner_text());first=p.locator('#windows-status').inner_text();p.wait_for_timeout(3300);self.assertNotEqual(p.locator('#windows-status').inner_text(),first)
  p.locator('#windows-history').check();p.locator('#windows-history-chart').wait_for(state='visible');self.assertTrue(p.locator('#windows-history-chart').is_visible());p.reload();self.tab(p,'monitor');self.assertTrue(p.locator('#windows-history').is_checked());p.wait_for_function('document.querySelector("#windows-metrics .win-scroll")');p.locator('#windows-metrics .win-scroll').evaluate('(e)=>e.scrollTop=100');p.wait_for_timeout(3300);self.assertEqual(p.locator('#windows-metrics .win-scroll').evaluate('(e)=>e.scrollTop'),100)
  requests=[];p.on('request',lambda r:requests.append(r.url));p.locator('#simulatorNav').click();self.tab(p,'rocket');p.wait_for_timeout(3300);self.assertFalse(any('/api/windows/monitor' in u for u in requests));self.assertFalse(p.locator('#windows-engineering').is_visible())
  for width,height in [(1280,800),(393,851),(851,393)]:
   p.set_viewport_size({'width':width,'height':height})
   for tab in ['monitor','macros']:
    self.tab(p,tab);self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'),width)
  out=Path('/workspace/work/phase48/screenshots');out.mkdir(parents=True,exist_ok=True);self.tab(p,'monitor');p.screenshot(path=str(out/'engineering_fixture.png'));self.tab(p,'macros');p.screenshot(path=str(out/'hotkeys_fixture.png'))
 def test_win_hotkeys_launchers_and_legacy_macros(self):
  p=self.page();self.tab(p,'macros');p.wait_for_function('document.querySelectorAll("[data-windows-key]").length===25');app=p.locator('#windows-apps .win-app');self.assertEqual(app.count(),1);app.locator('img').wait_for();self.assertEqual(app.inner_text(),'');self.assertIn('Google Chrome',app.get_attribute('aria-label'));p.locator('[data-windows-key=settings]').click();p.wait_for_function('document.querySelector("#windows-command-status").textContent.includes("Settings sent")');self.assertIn(('hotkey',('win','i')),self.calls);app.click();p.wait_for_function('document.querySelector("#windows-command-status").textContent.includes("launch requested")');self.assertIn(('launch','Google Chrome'),self.calls);p.locator('#macroButtons button').filter(has_text='Copy').click();p.wait_for_timeout(200);self.assertIn(('hotkey',('ctrl','c')),self.calls);self.assertEqual(p.evaluate('typeof ICARUSDroneOps'),'undefined')
 def test_win_hold_description_never_executes_command(self):
  p=self.page();self.tab(p,'macros');b=p.locator('[data-windows-key=search]');b.wait_for();r=b.bounding_box();p.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2);p.mouse.down();p.wait_for_timeout(700);p.mouse.up();self.assertIn('Search',p.locator('#windows-command-status').inner_text());self.assertEqual(self.calls,[]);b.focus();b.press('Enter');p.wait_for_function('document.querySelector("#windows-command-status").textContent.includes("Search sent")');self.assertIn(('hotkey',('win','s')),self.calls)
 def test_win_authentication_allowlists_and_idempotence(self):
  for path in ['/api/windows/monitor','/api/windows/catalog','/api/windows/icon?id=chrome']:self.assertEqual(self.req(path,paired=False)[0],401)
  d={'kind':'hotkey','id':'search','requestId':'request01'};self.assertEqual(self.req('/api/windows/command',d,paired=False)[0],401);self.assertEqual(self.req('/api/windows/command',d,origin='https://untrusted.invalid')[0],403);self.assertEqual(self.req('/api/windows/command',{**d,'path':'evil.exe'})[0],400);self.assertEqual(self.req('/api/windows/command',{**d,'id':'shell'})[0],400);self.assertEqual(self.req('/api/windows/refresh',{'path':'evil.exe'})[0],400);self.assertEqual(self.calls,[])
  self.assertEqual(self.req('/api/windows/command',d)[0],200);status,raw=self.req('/api/windows/command',d);self.assertTrue(json.loads(raw)['duplicate']);self.assertEqual(len([c for c in self.calls if c[0]=='hotkey']),1);self.assertEqual(self.req('/api/windows/command',{**d,'id':'run'})[0],400);self.assertEqual(self.req('/api/windows/icon?id=../config.json')[0],404);status,raw=self.req('/api/windows/catalog');self.assertNotIn('fixture.exe',raw.decode());self.assertEqual(status,200)
 def test_win_unavailable_host_and_reconnect_preserve_preferences(self):
  self.m.WINDOWS_CONTROL.system='Linux';self.m.WINDOWS_MONITOR.probe.sample=lambda:{'supported':False,'reason':'Windows measurements unavailable on this host'};self.m.WINDOWS_MONITOR.collect();p=self.page();self.tab(p,'monitor');p.wait_for_function('document.querySelector("#windows-metrics").textContent.includes("unavailable on this host")');self.tab(p,'macros');p.wait_for_function('document.querySelector("#windows-catalog-note").textContent.includes("unavailable on this host")');self.assertTrue(p.locator('[data-windows-key=search]').is_disabled());p.route('**/api/windows/catalog',lambda route:route.abort());p.evaluate('UmbraWindows.catalog()');p.wait_for_function('document.querySelector("#windows-catalog-note").textContent.includes("RECONNECTING")');p.unroute('**/api/windows/catalog');p.evaluate('UmbraWindows.catalog()');p.wait_for_function('document.querySelector("#windows-catalog-note").textContent.includes("unavailable on this host")')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args()
 if a.runtime:
  import test_umbra_browser;test_umbra_browser.ROOT=a.runtime.resolve()
 names=[n for n in unittest.defaultTestLoader.getTestCaseNames(WindowsIntegration) if n.startswith('test_win_')];r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite(WindowsIntegration(n) for n in names));a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
