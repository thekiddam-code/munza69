"""Calendar production integration and preserved core behavior in a real browser."""
import argparse,json,unittest
from pathlib import Path
from test_anthology_integration import CoreIntegration
from test_continuity import RecordedResult
class UnifiedIntegration(CoreIntegration):
    def test_real_calendar_day_advances_four_days_without_four_episode_resets(self):
        p=self.page();start=1780376400000 # 2026-06-02 05Z, ordinary Chicago day
        p.evaluate('t=>__icarusSoak.realStart(t,"America/Chicago")',start)
        for h in range(1,25):p.evaluate('t=>__icarusSoak.realAdvance(t)',start+h*3600000)
        s=self.snap(p);self.assertEqual(s['tick'],5760);self.assertEqual(s['episode'],1);self.assertEqual(s['resourceAudit'],[]);self.assertEqual(len(s['crew'])+len(s['living']['deceased']),20)
    def test_real_monday_boundary_keeps_work_and_full_calendar_after_reload(self):
        p=self.page();p.evaluate('__icarusSoak.realStart(Date.parse("2026-06-07T23:59Z"),"UTC")');before=self.snap(p);p.evaluate('__icarusSoak.realAdvance(Date.parse("2026-06-08T00:01Z"))');s=self.snap(p);self.assertEqual(s['episode'],2);self.assertEqual(s['tick'],8);self.assertEqual(s['archived'][-1]['realWeek'],'2026-06-01');p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),s)
    def test_holiday_correction_does_not_change_crew_inventory_or_complete_missions(self):
        p=self.page();p.evaluate('__icarusSoak.realStart(Date.parse("2026-12-24T12:00Z"),"UTC")');before=self.snap(p);p.evaluate('__icarusSoak.realAdvance(Date.parse("2026-12-24T12:00Z"))');after=self.snap(p)
        for key in ['crew','economy','missions','director','tick']:self.assertEqual(after[key],before[key],key)
        self.assertEqual(len(after['calendar']['occurrences']),1);p.evaluate('__icarusSoak.realAdvance(Date.parse("2026-12-24T12:01Z"))');self.assertEqual(self.snap(p)['tick'],1)
    def test_real_calendar_boundary_preserves_active_mission_research_medical_and_fire(self):
        from test_continuity import Continuous
        original=self.advance
        def real_boundary(page,count):
            self.assertEqual(count,1)
            page.evaluate('__icarusSoak.realStart(Date.parse("2026-06-07T23:59:45Z"),"UTC")')
            page.evaluate('__icarusSoak.realAdvance(Date.parse("2026-06-08T00:00Z"))')
        self.advance=real_boundary
        try:Continuous.test_transition_during_mission_research_treatment_and_emergency(self)
        finally:self.advance=original
    def test_creator_lore_does_not_leak_to_the_acquired_archive(self):
        p=self.page();self.deck(p,'settings','advanced');p.locator('summary').filter(has_text='CREATOR LORE EDITOR').click();p.locator('#canon-key').select_option('military');self.assertIn('dormant adult',p.locator('#canon-text').input_value());p.locator('#canon-text').fill('PRIVATE CANON TEST');p.locator('#canon-save').click();self.assertEqual(self.snap(p)['unifiedWorld']['canon']['military'],'PRIVATE CANON TEST');self.assertEqual(self.snap(p)['unifiedWorld']['archives'],[]);self.deck(p,'research','evidence');p.locator('summary').filter(has_text='IN-GAME ARCHIVES').click();self.assertNotIn('PRIVATE CANON TEST',p.locator('#acquired-lore').inner_text())
    def test_initial_biology_and_personal_inventory_persist_without_fabricated_history(self):
        p=self.page();s=self.snap(p);w=s['unifiedWorld'];self.assertEqual(sum(o['stage']=='adult' for o in w['organisms'].values()),1);self.assertTrue(w['organisms']['XENO-INITIAL']['dormant']);self.assertEqual(len(w['items']),20);self.assertTrue(all(not x['history'] for x in w['items'].values()));p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),s)
    def test_follow_camera_uses_corridor_node_without_room_occupancy(self):
        p=self.page();self.configure(p,"""const q=s.crew[0];q.room='A01';q.target='C05';q.route=['C05'];q.nav={destination:'C05',at:'H:B:2',steps:['H:B:3'],index:0,progress:.5,wait:0};q.task='Walking through corridor';""");self.operations(p);self.assertIn('H:B:2',p.locator('#camstatus').inner_text());self.assertIn('CORRIDOR',p.locator('#camstatus').inner_text());self.assertEqual(self.snap(p)['crew'][0]['room'],'A01');self.assertEqual(p.locator('#campeople .cam-person').count(),1)
    def test_wheelchair_never_teleports_or_uses_ladders_when_lift_is_offline(self):
        p=self.page();self.configure(p,"""s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;const q=s.crew[0];q.body={locomotion:'wheelchair',species:'human'};q.room='A01';q.target='C05';q.route=['C05'];q.nav=null;q.goal='Physical accessibility test';q.taskMinutes=999;s.navSystem={elevator:'offline',lastChange:s.tick};""");self.advance(p,30);q=self.snap(p)['crew'][0];self.assertEqual(q['room'],'A01');self.assertEqual(q['task'],'Waiting for accessible route');self.assertFalse(any(x.startswith('V:') for x in (q.get('nav',{}).get('steps') or [])))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report',default='unified_integration.json');args=ap.parse_args();r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(UnifiedIntegration));Path(args.report).write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
