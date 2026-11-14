"""Portable full-source verification driver; intentionally excluded from Lite."""
import argparse,importlib,json,os,sys,unittest
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--suite',choices=['browser','remote','clock','legacy','focused','expedition','field','field-remote','expedition-remote'],required=True);ap.add_argument('--report',type=Path,required=True);ap.add_argument('--v13-web',type=Path);ap.add_argument('--phase41-backup',type=Path);ap.add_argument('--phase4-backup',type=Path);ap.add_argument('--chromium',type=Path);ap.add_argument('--case',help='Optional exact test method; never removes assertions');a=ap.parse_args();root=a.runtime.resolve()
 for value,key in [(a.v13_web,'ICARUS_V13_WEB'),(a.phase41_backup,'ICARUS_PHASE41_BACKUP'),(a.phase4_backup,'ICARUS_PHASE4_BACKUP'),(a.chromium,'ICARUS_CHROMIUM')]:
  if value is not None:os.environ[key]=str(value.resolve())
 # Test modules come from this full source tree; runtime service imports prefer the selected export.
 sys.path.insert(0,str(root));module,classname={'browser':('test_operations_integration','OperationsIntegration'),'focused':('test_operations_integration','OperationsIntegration'),'remote':('test_operations_remote','OperationsRemote'),'clock':('test_personalities_clock','PersonalitiesClock'),'legacy':('test_continuity','Continuous'),'expedition':('test_expedition_integration','ExpeditionIntegration'),'field':('test_expedition_integration','ExpeditionIntegration'),'field-remote':('test_expedition_remote','ExpeditionRemote'),'expedition-remote':('test_expedition_remote','ExpeditionRemote')}[a.suite];m=importlib.import_module(module)
 for mod in list(sys.modules.values()):
  if getattr(mod,'__name__','').startswith('test_') and hasattr(mod,'ROOT'):mod.ROOT=root
 from test_continuity import RecordedResult
 cls=getattr(m,classname);names=unittest.defaultTestLoader.getTestCaseNames(cls)
 if a.case:
  if a.case not in names:ap.error('Unknown case: '+a.case)
  names=[a.case]
 elif a.suite in ('field','field-remote'):names=[n for n in names if n.startswith('test_field_')]
 elif a.suite=='focused':names=[n for n in names if n.startswith('test_ops_')]
 result=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite(cls(n) for n in names));manifest=root/'BUILD_MANIFEST.json';r={'passed':result.wasSuccessful(),'tests_run':result.testsRun,'passed_cases':result.successes,'runtime_root':str(root),'source_commit':json.loads(manifest.read_text())['source_commit'] if manifest.exists() else None,'errors':[{'test':str(t),'detail':d} for t,d in result.errors],'failures':[{'test':str(t),'detail':d} for t,d in result.failures]};a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(r,indent=2));return not result.wasSuccessful()
if __name__=='__main__':raise SystemExit(main())
