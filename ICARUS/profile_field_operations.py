"""Profile a real physical expedition in an isolated deterministic technical world."""
import sys,json,time,unittest,argparse
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import test_expedition_integration as E
from test_continuity import RecordedResult
ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path,required=True);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args();runtime=a.runtime.resolve();out=a.report;out.parent.mkdir(parents=True,exist_ok=True)
for m in list(sys.modules.values()):
 if getattr(m,'__name__','').startswith('test_') and hasattr(m,'ROOT'):m.ROOT=runtime
class ActiveFieldProfile(E.ExpeditionIntegration):
 def page(self):
  self.profilePage=super().page();return self.profilePage
 def test_profile_physical_expedition(self):
  self.test_field_physical_preparation_route_return_and_source_records();d=self.profilePage.evaluate('ICARUSRuntimeDiagnostics.snapshot()');self.assertGreater(d['groups']['expedition']['calls'],0);self.profile={k:v for k,v in d['groups'].items() if k in ['vehicle','escort','drones','expedition','pathfinding']}
t=ActiveFieldProfile('test_profile_physical_expedition');start=time.monotonic();r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite([t]));out.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'duration_seconds':time.monotonic()-start,'scope':'Separate explicitly controlled technical fixture: actual physical preparation, travel, sensor recording and return; not the private-voyage benchmark. Diagnostic counters are CPU call costs, not whole-campaign throughput.','groups':getattr(t,'profile',{}),'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
