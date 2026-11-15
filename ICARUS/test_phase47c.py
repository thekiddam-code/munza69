"""Actual dispatch controls and source-backed surveillance. Isolated technical saves."""
import argparse,json,unittest
from pathlib import Path
from test_drone_integration import DroneIntegration
from test_continuity import RecordedResult
OUT=Path('/workspace/work/phase47c/screenshots')
class Phase47C(DroneIntegration):
 def legacy(self,p):
  self.deck(p,'missions','destinations');p.locator('[data-location="asteroid"]').click();p.locator('[data-remote-tab="Expedition"]').click()
 def test_c_dispatch_selection_persistence_and_physical_departure(self):
  p=self.page();self.configure(p,'s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;');self.legacy(p);options=p.locator('#fieldcrew option').evaluate_all('(es)=>es.map(e=>({name:e.value,text:e.textContent}))');selected=next(x['name'] for x in options[1:] if 'Scientist' in x['text']);p.locator('#fieldcrew').select_option(selected);p.locator('#fieldcrew').blur();p.wait_for_timeout(2600);self.assertEqual(p.locator('#fieldcrew').input_value(),selected);p.reload();self.legacy(p);self.assertEqual(p.locator('#fieldcrew').input_value(),selected);p.locator('[data-remote-action="dispatch"]').click();self.assertIn('Accepted',p.locator('.dispatch-feedback').inner_text());m=self.snap(p)['missions']['asteroid'];self.assertIn(selected,m['members']);rooms=set()
  for _ in range(600):
   self.advance(p,1);s=self.snap(p);m=s['missions']['asteroid'];rooms.update(q['room'] for q in s['crew'] if q.get('expeditionId'))
   if m and m.get('ops44',{}).get('stage')=='field':break
  else:self.fail('Dispatched crew did not physically reach asteroid')
  self.assertIn('C04',rooms);self.assertIn('C02',rooms);self.assertEqual(s['resourceAudit'],[])
 def test_c_dispatch_rejection_is_explicit_and_does_not_allocate_resources(self):
  p=self.page();self.configure(p,'s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;for(const q of s.crew)q.energy=15;');self.legacy(p);before=self.snap(p);p.locator('[data-remote-action="dispatch"]').click();self.assertRegex(p.locator('.dispatch-feedback').inner_text(),'availability|specialist');after=self.snap(p);self.assertIsNone(after['missions']['asteroid']);self.assertEqual(after['economy'],before['economy'])
 def test_c_actual_live_event_clip_and_rover_render_preserve_world(self):
  p=self.page();self.deck(p,'operations','watch');p.wait_for_function('ICARUSObservationLive.camera.tick===__icarusSoak.time()');p.evaluate("ICARUSObservationLive.camera.pick('C03');ICARUSObservationLive.camera.draw(true)");before=self.snap(p);OUT.mkdir(parents=True,exist_ok=True);p.locator('#observation-primary').screenshot(path=str(OUT/'futuristic_rover.png'));self.assertEqual(self.snap(p),before);self.setup_drone(p);self.until(p,lambda s:any(d.get('edge') for d in s['droneOperations']['drones'].values()));p.evaluate('document.getElementById("pause").click()');self.deck(p,'missions','active');p.locator('.drone-ops details').nth(1).locator('summary').click();p.locator('.drone-live').scroll_into_view_if_needed();p.wait_for_function('document.querySelector(".drone-camera-label").textContent.includes(" · tick "+__icarusSoak.time()+" · ")');p.wait_for_timeout(1500);self.advance(p,4);p.wait_for_timeout(1000);self.deck(p,'settings','data');archive=self.snap(p)['droneOperations']['archive'];record=next((c for c in archive if c.get('motion')),None);self.assertIsNotNone(record,'An actual displayed event must retain its bounded captured clip');self.assertGreaterEqual(len(record['motion']['frames']),2);self.assertTrue(p.evaluate('__icarusSoak.save()'));p.reload();self.assertEqual(next(c for c in self.snap(p)['droneOperations']['archive'] if c['id']==record['id']),record);self.assertEqual(self.snap(p)['droneAudit'],[])
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args()
 if a.runtime:
  import sys
  for m in list(sys.modules.values()):
   if getattr(m,'__name__','').startswith('test_') and hasattr(m,'ROOT'):m.ROOT=a.runtime.resolve()
 names=[n for n in unittest.defaultTestLoader.getTestCaseNames(Phase47C) if n.startswith('test_c_')];r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite(Phase47C(n) for n in names));a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d[:4000]} for t,d in r.failures],'errors':[{'test':str(t),'detail':d[:4000]} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
