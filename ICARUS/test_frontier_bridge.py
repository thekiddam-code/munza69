"""Paired Remote Deck integration, without invoking desktop input devices."""
import argparse, importlib.util, json, os, sys, threading, types, unittest, urllib.request, urllib.error
from pathlib import Path
from playwright.sync_api import sync_playwright
from test_continuity import RecordedResult
ROOT=Path(__file__).resolve().parent

class FrontierBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Simulation HTTP paths do not need desktop keyboard/mouse access.
        sys.modules['pyautogui']=types.SimpleNamespace()
        spec=importlib.util.spec_from_file_location('bridge_under_test',ROOT/'server.py');cls.mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.mod)
        cls.mod.ICARUS_KEY='test-host';cls.mod.TOKENS={cls.mod.token_hash('test-tablet')}
        cls.server=cls.mod.http.server.ThreadingHTTPServer(('127.0.0.1',0),cls.mod.Handler);threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url=f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close()
    def setUp(self):self.mod.ICARUS_BRIDGE.update(telemetry=None,updated=0,commands=[],next_id=1)
    def request(self,path,payload=None,headers=None):
        req=urllib.request.Request(self.url+'/api/icarus/'+path,data=json.dumps(payload).encode() if payload is not None else None,headers={'Content-Type':'application/json',**(headers or {})})
        try:
            with urllib.request.urlopen(req) as r:return r.status,json.load(r)
        except urllib.error.HTTPError as e:return e.code,json.load(e)
    def test_authentication_command_validation_and_exactly_once_queue_drain(self):
        auth={'Authorization':'Bearer test-tablet'};host={'X-Icarus-Key':'test-host'}
        self.assertEqual(self.request('command',{'command':'nav:hold'})[0],401)
        for command in ('nav:hold','nav:resume','nav:recall','nav:course:SYS:-3:2/1','frontier:rescue:SOS-12','frontier:shelter:SOS-3'):
            self.assertEqual(self.request('command',{'command':command},auth)[0],200)
        for command in ('frontier:rescue:garbage','nav:course:unknown','nav:course:SYS:1:2/0;alert(1)',[],None):
            self.assertEqual(self.request('command',{'command':command},auth)[0],400)
        self.assertEqual(self.request('commands',headers=auth)[0],403)
        self.assertEqual(len(self.request('commands',headers=host)[1]['commands']),6)
        self.assertEqual(self.request('commands',headers=host)[1]['commands'],[])
    def test_expanded_telemetry_requires_host_auth_and_stays_bounded(self):
        payload={'frontier':{'reason':'x'*5000}}
        self.assertEqual(self.request('telemetry',payload,{'Authorization':'Bearer test-tablet'})[0],403)
        self.assertEqual(self.request('telemetry',payload,{'X-Icarus-Key':'test-host'})[0],200)
        self.assertEqual(self.request('telemetry')[0],401)
        self.assertEqual(self.request('telemetry',headers={'Authorization':'Bearer test-tablet'})[1]['telemetry'],payload)
        self.assertEqual(self.request('telemetry',{'large':'x'*17000},{'X-Icarus-Key':'test-host'})[0],413)
    def test_paired_tablet_map_sends_navigation_to_authoritative_pc(self):
        with sync_playwright() as pw:
            b=pw.chromium.launch(headless=True,executable_path=os.environ.get('ICARUS_CHROMIUM') or None)
            pc=b.new_context();pc.add_init_script("sessionStorage.setItem('icarusHostKey','test-host');window.__icarusSeed=10101;")
            p=pc.new_page();p.goto(self.url+'/icarus.html?icarus_soak=1');p.wait_for_function('!!window.__icarusSoak')
            tablet=b.new_context(viewport={'width':768,'height':1024});tablet.add_init_script("localStorage.setItem('remoteDeckToken','test-tablet');")
            t=tablet.new_page();t.goto(self.url+'/');t.evaluate("showApp();umbraOpenTab('icarus');")
            t.wait_for_selector('#tablet-frontier-target option',state='attached');target=t.locator('#tablet-frontier-target option').evaluate_all('(els)=>els.map(e=>e.value).find(x=>x!=="HOME")')
            t.locator('#tablet-frontier-target').select_option(target);t.locator('[data-tablet-nav="course"]').click()
            p.wait_for_function('(id)=>window.__icarusSoak.snapshot().navigation.target===id',arg=target)
            self.assertEqual(p.evaluate('window.__icarusSoak.snapshot().navigation.phase'),'transit')
            t.locator('[data-tablet-nav="hold"]').click();p.wait_for_function('window.__icarusSoak.snapshot().navigation.hold')
            self.assertFalse(t.evaluate('!!window.__icarusSoak'));self.assertLessEqual(t.locator('#tablet-frontier svg').bounding_box()['width'],768)
            t.evaluate('icarusPoll()');t.wait_for_timeout(300);self.assertEqual(t.locator('#tablet-frontier-target').input_value(),target)
            b.close()

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='bridge_results.json');args=ap.parse_args();suite=unittest.defaultTestLoader.loadTestsFromTestCase(FrontierBridge)
    runner=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult);result=runner.run(suite)
    Path(args.output).write_text(json.dumps({'passed':result.wasSuccessful(),'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed_cases':result.successes,'details':[str(t)+' '+d for t,d in result.failures+result.errors]},indent=2));sys.exit(0 if result.wasSuccessful() else 1)
