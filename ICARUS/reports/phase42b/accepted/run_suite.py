import sys,os,unittest,importlib,json
from pathlib import Path
source=Path('/workspace/work/munza69/ICARUS');root=Path(os.environ.get('ICARUS_RUNTIME_ROOT',str(source)));out=Path(os.environ.get('ICARUS_REPORT_ROOT','/workspace/work/phase42b/verification'));out.mkdir(parents=True,exist_ok=True);sys.path[:0]=[str(root),str(source)];os.environ['ICARUS_V13_WEB']='/workspace/work/v13_package/ICARUS/web'
name=sys.argv[1];mod,cls={'focused':('test_personalities_integration','PersonalitiesIntegration'),'browser':('test_personalities_integration','PersonalitiesIntegration'),'remote':('test_personalities_remote','PersonalitiesRemote'),'clock':('test_personalities_clock','PersonalitiesClock')}[name];m=importlib.import_module(mod)
for module in list(sys.modules.values()):
 if getattr(module,'__name__','').startswith('test_') and hasattr(module,'ROOT'):module.ROOT=root
from test_continuity import RecordedResult
case=getattr(m,cls);suite=unittest.TestSuite(case(n) for n in unittest.defaultTestLoader.getTestCaseNames(case) if n.startswith('test_phase42b_')) if name=='focused' else unittest.defaultTestLoader.loadTestsFromTestCase(case)
r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(suite)
report={'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'runtime_root':str(root),'source_commit':json.loads((root/'BUILD_MANIFEST.json').read_text())['source_commit'] if (root/'BUILD_MANIFEST.json').exists() else None,'errors':[{'test':str(t),'detail':d} for t,d in r.errors],'failures':[{'test':str(t),'detail':d} for t,d in r.failures]};(out/(name+'.json')).write_text(json.dumps(report,indent=2));raise SystemExit(not r.wasSuccessful())
