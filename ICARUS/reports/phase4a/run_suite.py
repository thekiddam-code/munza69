"""External harness: unmodified pinned suites, all runtime roots point to the extracted Lite ZIP."""
import sys,os,importlib,json,unittest
from pathlib import Path
BASE=Path(__file__).resolve().parent
SOURCE=Path('/workspace/work/munza69/ICARUS');LITE=Path(os.environ.get('ICARUS_LITE_ROOT',str(BASE/'tested/ICARUS_SOL_Command_Interface_Phase4_Lite')))
sys.path[:0]=[str(LITE),str(SOURCE)];os.environ['ICARUS_V13_WEB']='/workspace/work/v13_package/ICARUS/web'
import test_integration
assert (LITE/'web/icarus.html').is_file();test_integration.ROOT=LITE
from test_continuity import RecordedResult
suites={'umbra':('test_umbra_browser','UmbraBrowser'),'tv_service':('test_tv_service','TVServiceTests'),'interface':('test_command_interface','CommandInterface'),'cinematic':('test_refinement_integration','RefinementIntegration'),'living_world':('test_living_world_integration','LivingWorldIntegration'),'stability':('test_stability_integration','StabilityIntegration'),'compatibility':('test_living_frontier_integration','LivingFrontierIntegration'),'production':('test_production_clock','ProductionClock'),'bridge':('test_frontier_bridge','FrontierBridge')}
name=sys.argv[1];mod,cls=suites[name];m=importlib.import_module(mod)
for loaded in list(sys.modules.values()):
 if getattr(loaded,'__name__','').startswith('test_') and hasattr(loaded,'ROOT'):loaded.ROOT=LITE
result=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(getattr(m,cls)))
r={'suite':name,'runtime_root':str(LITE),'runtime_source_commit':json.loads((LITE/'BUILD_MANIFEST.json').read_text())['source_commit'],'harness_source_commit':__import__('subprocess').check_output(['git','rev-parse','HEAD'],cwd=SOURCE,text=True).strip(),'harness':'Pinned source tests outside Lite; runtime ROOT rebound to independent ZIP extraction. No runtime source patches. Desktop input stubbed in bridge tests.','passed':result.wasSuccessful(),'tests_run':result.testsRun,'passed_cases':result.successes,'failures':[{'test':str(t),'detail':d} for t,d in result.failures],'errors':[{'test':str(t),'detail':d} for t,d in result.errors]};(BASE/'reports'/f'{name}.json').write_text(json.dumps(r,indent=2));raise SystemExit(not result.wasSuccessful())
