"""Run from a disposable 4.9 Lite + bulk overlay, with historical 4.9 test sources."""
import argparse,json,os,sys,unittest
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime',type=Path,required=True);p.add_argument('--tests',type=Path,required=True);p.add_argument('--suite',choices=['volume','bulk','services','installer'],required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
here=Path(__file__).resolve().parent;sys.path[:0]=[str(here),str(here.parent/'phase49'),str(a.runtime.resolve()),str(a.tests.resolve())]
from test_continuity import RecordedResult
if a.suite=='volume':
 from test_volume_browser import VolumeBrowser
 suite=unittest.TestSuite(VolumeBrowser(n) for n in unittest.defaultTestLoader.getTestCaseNames(VolumeBrowser) if n.startswith('test_volume_'))
elif a.suite=='bulk':
 from test_bulk_soundboard import BulkSoundboard
 suite=unittest.TestSuite(BulkSoundboard(n) for n in unittest.defaultTestLoader.getTestCaseNames(BulkSoundboard) if n.startswith(('test_bulk_','test_sound_')))
elif a.suite=='installer':suite=unittest.defaultTestLoader.loadTestsFromName('test_volume_installer')
else:
 suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(n) for n in ['test_sound_services','test_audio_foundation','test_bulk_services'])
for module in list(sys.modules.values()):
 if getattr(module,'__name__','').startswith('test_') and hasattr(module,'ROOT'):module.ROOT=a.runtime.resolve()
r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(suite);a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[(str(t),d) for t,d in r.failures],'errors':[(str(t),d) for t,d in r.errors],'skipped':[(str(t),d) for t,d in r.skipped]},indent=2));raise SystemExit(not r.wasSuccessful())
