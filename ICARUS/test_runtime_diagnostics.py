"""Read-only diagnostics in the ordinary page, with a controlled production clock."""
import argparse,json,unittest
from pathlib import Path
from test_production_clock import ProductionClock,RecordedResult
class RuntimeDiagnostics(ProductionClock):
 def test_perf_metrics_show_selected_rate_and_do_not_mutate_the_voyage(self):
  p=self.start('2026-11-12T12:00:00',fixed=True);p.locator('[aria-label="Ship pacing"]').select_option('20');p.clock.fast_forward(30000);before=self.state(p);self.assertEqual(before['tick'],10)
  p.evaluate("ICARUSCommandUI.navigate('settings','general')");p.locator('.runtime-diagnostics summary').click();p.clock.run_for(1);p.wait_for_function('document.querySelector(".runtime-diagnostics").textContent.includes("Configured: 20×")');text=p.locator('.runtime-diagnostics').inner_text();self.assertIn('Configured: 20×',text);self.assertIn('Throughput:',text);self.assertIn('Average tick logic:',text);self.assertIn('IndexedDB commit:',text);d=p.evaluate('ICARUSRuntimeDiagnostics.snapshot()');self.assertEqual(d['configuredRate'],20);self.assertEqual(d['groups']['tick']['calls'],10);self.assertGreaterEqual(d['groups']['save']['calls'],1);self.assertEqual(p.evaluate('JSON.parse(localStorage.getItem("icarus-v02"))'),before)
  if SCREENSHOT:SCREENSHOT.parent.mkdir(parents=True,exist_ok=True);p.locator('.runtime-diagnostics').screenshot(path=str(SCREENSHOT))
SCREENSHOT=None
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path,required=True);ap.add_argument('--report',type=Path,required=True);ap.add_argument('--screenshot',type=Path);a=ap.parse_args();SCREENSHOT=a.screenshot
 import test_production_clock
 test_production_clock.ROOT=a.runtime.resolve()
 r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite([RuntimeDiagnostics('test_perf_metrics_show_selected_rate_and_do_not_mutate_the_voyage')]));a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
