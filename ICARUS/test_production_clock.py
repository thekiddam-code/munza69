"""Exercise the ordinary page timer, without deterministic simulation hooks."""
import argparse,functools,http.server,json,os,threading,unittest
from pathlib import Path
from datetime import datetime,timezone
from playwright.sync_api import sync_playwright
from test_continuity import RecordedResult
ROOT=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
class ProductionClock(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'web')));threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(executable_path=os.environ.get('ICARUS_CHROMIUM') or None)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop();cls.server.shutdown()
    def start(self,date):
        self.context=self.browser.new_context(timezone_id='America/Chicago');p=self.context.new_page();self.errors=[];p.on('pageerror',lambda e:self.errors.append(str(e)));p.clock.install(time=datetime.fromisoformat(date).replace(tzinfo=timezone.utc));p.goto(f'http://127.0.0.1:{self.server.server_port}/icarus.html');p.wait_for_function('document.querySelector("#status").textContent.includes("LIVE")');self.assertEqual(p.evaluate('typeof __icarusSoak'),'undefined');return p
    def state(self,p):p.evaluate('document.querySelector("#save").click()');p.evaluate('ICARUSDurable.flush()');return p.evaluate('JSON.parse(localStorage.getItem("icarus-v02"))')
    def tearDown(self):self.context.close();self.assertEqual(self.errors,[])
    def test_actual_normal_timer_is_four_times_and_pause_drops_elapsed_time(self):
        p=self.start('2026-11-09T12:00:00');p.clock.fast_forward(15000);self.assertEqual(self.state(p)['tick'],1);self.assertIn('4×',p.locator('#speed').inner_text());p.locator('#pause').click();p.clock.fast_forward(60000);self.assertEqual(self.state(p)['tick'],1);p.locator('#pause').click();p.clock.fast_forward(15000);self.assertEqual(self.state(p)['tick'],2)
    def test_actual_holiday_timer_is_one_times_and_ignores_old_speed_button(self):
        p=self.start('2026-11-11T12:00:00');p.locator('#speed').click();p.clock.fast_forward(60000);s=self.state(p);self.assertEqual(s['tick'],1);self.assertIn('1×',p.locator('#speed').inner_text());self.assertEqual(len(s['calendar']['occurrences']),1)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report',default='production_clock.json');args=ap.parse_args();r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(ProductionClock));Path(args.report).write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
