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
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report',default='unified_integration.json');args=ap.parse_args();r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(UnifiedIntegration));Path(args.report).write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
