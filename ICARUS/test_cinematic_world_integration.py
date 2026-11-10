"""Explicit fixture tests for Phase 3 plus the preserved Phase 2 browser contract."""
import argparse,json,unittest
from pathlib import Path
from test_living_world_integration import LivingWorldIntegration
from test_continuity import RecordedResult
class CinematicWorldIntegration(LivingWorldIntegration):
    def test_individual_routines_and_interaction_memories_survive_reload(self):
        p=self.page();self.advance(p,240);s=self.snap(p);self.assertEqual(s['crewLife']['version'],1);self.assertEqual(len(s['crewLife']['people']),20);self.assertTrue(any(x['recent'] for x in s['crewLife']['people'].values()));self.assertTrue(all(len(x['recent'])<=12 and len(x['memories'])<=24 for x in s['crewLife']['people'].values()));p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),s)
    def test_actual_conversation_has_source_memory_and_visible_pose(self):
        p=self.page();self.configure(p,"""for(const i of [0,6]){const q=s.crew[i];q.room='C05';q.route=[];q.nav=null;q.social=20;q.energy=90;q.stress=20;q.task='Taking a break';q.taskMinutes=20;q.interaction=null;}""");r=p.evaluate('__icarusSoak.phase3("talk",{from:"Frank Morrow",to:"Jules Mercer"})');self.assertTrue(r['id']);s=self.snap(p);self.assertEqual(s['crewLife']['people']['Frank Morrow']['memories'][-1]['sourceId'],r['id']);self.operations(p);self.assertEqual(p.locator('#campeople .cam-person.hero').get_attribute('data-pose'),'talk');self.assertEqual(self.snap(p),s)
    def test_social_action_cannot_use_an_away_person_old_room_label(self):
        p=self.page();self.field(p);self.assertIsNone(p.evaluate('__icarusSoak.phase3("talk",{from:"Frank Morrow",to:"Jules Mercer"})'))
    def test_spectator_and_repeated_camera_refresh_are_observer_only(self):
        p=self.page();self.operations(p);s=self.snap(p);p.locator('#spectator-next').click();self.assertIn('LIVE STATE PROJECTION',p.locator('#spectator-status').inner_text());before=p.evaluate('__icarusSoak.phase3("render")');after=p.evaluate('()=>{let r;for(let i=0;i<20;i++)r=__icarusSoak.phase3("render");return r;}');self.assertEqual(before['actorRebuilds'],after['actorRebuilds']);self.assertEqual(self.snap(p),s)
    def test_spectator_layout_and_recording_provenance_on_tablet_landscape(self):
        p=self.page();p.set_viewport_size({'width':1280,'height':800});self.advance(p,120);self.operations(p);p.locator('#spectator-next').click();s=self.snap(p);self.assertTrue(s['cinema']['recordings']);self.assertTrue(all('not video' in r['label'] for r in s['cinema']['recordings']));self.assertLessEqual(p.locator('.spectator-controls').bounding_box()['width'],1280);p.locator('#camera-scene').screenshot(path='/workspace/work/phase3_reports/tablet_camera.png');self.assertEqual(self.snap(p),s)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report',default='cinematic_world.json');args=ap.parse_args();r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(CinematicWorldIntegration));Path(args.report).write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
