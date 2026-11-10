"""Phase 3.5 real-browser fixtures plus all preserved Phase 3 coverage."""
import argparse,json,unittest
from pathlib import Path
from test_cinematic_world_integration import CinematicWorldIntegration
from test_continuity import RecordedResult
class RefinementIntegration(CinematicWorldIntegration):
    def test_animation_is_physically_sourced_and_pause_reduced_motion_are_static(self):
        p=self.page();self.operations(p);s=self.snap(p);p.evaluate('__icarusSoak.phase3("render")');self.assertEqual(p.locator('#campeople .cam-person').first.get_attribute('data-motion-active'),'false');self.assertEqual(s,self.snap(p));p.emulate_media(reduced_motion='reduce');self.assertEqual(p.locator('#campeople .cam-person .rig-art').first.evaluate('(e)=>getComputedStyle(e).animationName'),'none')
    def test_refined_camera_desktop_and_tablet_screenshots_do_not_mutate_world(self):
        p=self.page();self.advance(p,120);self.operations(p);s=self.snap(p)
        for size,label in [({'width':1440,'height':900},'desktop'),({'width':1280,'height':800},'tablet')]:
            p.set_viewport_size(size);p.locator('#camera-scene').screenshot(path='/workspace/work/phase35_reports/35a_'+label+'.png');self.assertEqual(self.snap(p),s)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report',default='refinement.json');args=ap.parse_args();r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(RefinementIntegration));Path(args.report).write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
