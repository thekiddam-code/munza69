"""Focused source-state and interrupted care acceptance; actual isolated running engine."""
import argparse,json,unittest
from pathlib import Path
from test_specimen_integration import SpecimenIntegration
from test_continuity import RecordedResult
class SpecimenAcceptance(SpecimenIntegration):
 def test_accept_midcare_save_reload_resumes_physical_paid_work(self):
  p=self.page();self.live(p);self.change(p,"const o=Object.values(s.unifiedWorld.organisms).find(o=>o.life49?.enclosure);o.behavior.energy=35;o.life49.lastService=-1000;");seen=False
  for _ in range(100):
   self.advance(p,5);s=self.snap(p);workers=[q for q in s['crew'] if q.get('bioAssignment',{}).get('kind')=='care']
   if workers:
    before=s;p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),before);seen=True;break
  self.assertTrue(seen,'A physical care assignment was not scheduled')
  for _ in range(80):
   self.advance(p,5);s=self.snap(p)
   if s['unifiedWorld']['biologicalLife49']['stats']['care']:break
  self.assertGreater(s['unifiedWorld']['biologicalLife49']['stats']['care'],0);self.assertEqual(s['biologyAudit'],[]);self.assertEqual(s['resourceAudit'],[])
 def test_accept_saved_camera_specimen_frame_has_sources_and_renders_without_world_mutation(self):
  p=self.page();s=self.live(p);frames=[f for f in s['cinema']['recordings'] if f.get('specimens')];self.assertTrue(frames,'The actual biological event must retain a source-state camera snapshot');frame=frames[-1];self.assertTrue(frame['sourceIds']);self.assertTrue(all(any(r['id']==key for r in s['chronicle']['records']) for key in frame['sourceIds']));before=self.snap(p)
  result=p.evaluate('''f=>{const c=document.createElement('canvas');ICARUSPixelCamera.draw(c,{id:f.room,name:'Saved specimen state',kind:'science',available:true,actors:[],specimens:f.specimens,enclosures:f.enclosures,lighting:1},{paused:true,reduced:true});return {image:c.toDataURL(),count:f.specimens.length};}''',frame);self.assertGreater(result['count'],0);self.assertTrue(result['image'].startswith('data:image/png'));self.assertEqual(self.snap(p),before)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path,required=True);a=ap.parse_args();names=[n for n in unittest.defaultTestLoader.getTestCaseNames(SpecimenAcceptance) if n.startswith('test_accept_')];r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite(SpecimenAcceptance(n) for n in names));a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[(str(t),d) for t,d in r.failures],'errors':[(str(t),d) for t,d in r.errors],'skipped':[(str(t),d) for t,d in r.skipped]},indent=2));raise SystemExit(not r.wasSuccessful())
