"""Actual renderer/engine tests over isolated technical worlds, not organic voyage claims."""
import argparse,json,os,unittest
from pathlib import Path
from test_drone_integration import DroneIntegration
from test_continuity import RecordedResult
OUT=Path('/workspace/work/phase47/screenshots')
class Phase47Integration(DroneIntegration):
 def test_47_vehicle_parking_real_camera_and_physical_inspection(self):
  p=self.page();s=self.snap(p);v=s['forwardOperations']['vehicle'];self.assertEqual((v['room'],v['stage']),('C03','parked'));self.assertTrue(v['restrained']);self.deck(p,'operations','watch');p.evaluate("ICARUSObservationLive.camera.pick('C03')");OUT.mkdir(parents=True,exist_ok=True);p.locator('#observation-primary').screenshot(path=str(OUT/'cargo_foc01.png'));self.configure(p,"s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.forwardOperations.inspectionRequested=true;for(const q of s.crew.filter(p=>p.job==='Engineer')){q.taskMinutes=0;q.energy=95;q.emergencyId=null;q.maintenanceRoom=null;q.systemAssignment=null;delete q.droneAssignment;q.researchAssignment=null;}")
  self.assertTrue(self.snap(p)['forwardOperations']['inspectionRequested']);travelled=False;seen=False
  for _ in range(200):
   self.advance(p,1);s=self.snap(p)
   for q in s['crew']:
    if q.get('forwardAssignment'):travelled=travelled or bool(q['route']);seen=seen or q['room']=='C03' and not q['route']
   if s['forwardOperations']['vehicle']['inspectedAt'] is not None:break
  self.assertIsNotNone(s['forwardOperations']['vehicle']['inspectedAt'],str([(q['name'],q['room'],q['target'],q['task'],q.get('forwardAssignment'),q.get('systemAssignment'),q.get('droneAssignment'),q.get('maintenanceRoom'),q.get('expeditionId')) for q in s['crew'] if q['job']=='Engineer']));self.assertTrue(travelled);self.assertTrue(seen);self.assertEqual(s['resourceAudit'],[]);p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),s)
 def test_47_live_drone_moves_and_recorded_sequence_plays_without_world_advance(self):
  p=self.page();self.setup_drone(p);self.until(p,lambda s:any(d.get('edge') for d in s['droneOperations']['drones'].values()));self.deck(p,'missions','active');p.locator('.drone-ops details').nth(1).locator('summary').click();p.locator('.drone-live').scroll_into_view_if_needed();p.wait_for_timeout(1100);first=p.locator('.drone-live').evaluate('c=>c.toDataURL()');self.advance(p,2);p.wait_for_timeout(1100);second=p.locator('.drone-live').evaluate('c=>c.toDataURL()');self.assertNotEqual(first,second);OUT.mkdir(parents=True,exist_ok=True);p.locator('.drone-live').screenshot(path=str(OUT/'live_drone_connected_passage.png'));self.advance(p,4);self.assertTrue(self.snap(p)['droneOperations']['archive']);p.wait_for_timeout(1100);p.locator('.drone-ops details').nth(2).locator('summary').click();p.locator('.drone-record').select_option(index=0);p.wait_for_function('Number(document.querySelector(".drone-frame").max)>0');before=self.snap(p);p.locator('.drone-restart').click();p.wait_for_timeout(650);self.assertGreater(int(p.locator('.drone-frame').input_value()),0);p.locator('.drone-pause').click();at=p.locator('.drone-frame').input_value();p.wait_for_timeout(650);self.assertEqual(p.locator('.drone-frame').input_value(),at);self.assertEqual(self.snap(p),before);self.assertIn('CAPTURED PROCEDURAL FRAME',p.locator('.drone-record-label').inner_text());p.locator('.drone-replay').screenshot(path=str(OUT/'captured_event_playback.png'))
 def test_47_industrial_camera_requires_real_connected_arrival(self):
  p=self.page();self.setup_drone(p);s=self.until(p,lambda s:any(d['stage']=='field' and not d.get('edge') and d['map'].get(str(d['node']),{}).get('fieldKind')=='industrial' and d.get('signal') in ['DIRECT','RELAYED'] for d in s['droneOperations']['drones'].values()),limit=1200);self.deck(p,'missions','active');p.locator('.drone-ops details').nth(1).locator('summary').click();p.locator('.drone-live').scroll_into_view_if_needed();p.wait_for_timeout(1200);views=p.evaluate('__icarusSoak.observation().rooms.filter(r=>r.id.startsWith("DRONE-")&&r.available)');self.assertTrue(any(v['terrain']['kind']=='industrial' for v in views));before=self.snap(p);OUT.mkdir(parents=True,exist_ok=True);p.locator('.drone-live').screenshot(path=str(OUT/'industrial_drone_camera.png'));self.assertEqual(self.snap(p),before);self.assertTrue(s['unifiedWorld']['organisms']['XENO-INITIAL']['dormant'])
 def test_47_received_categories_do_not_reveal_unknown_locations(self):
  p=self.page();self.deck(p,'missions','active');before=self.snap(p);p.locator('.drone-category').select_option('facilities');self.assertIn('No matching locations',p.locator('.drone-category-list').inner_text());self.assertNotIn('military',p.locator('.drone-category-list').inner_text().lower());p.locator('.drone-category').select_option('drones');self.assertEqual(self.snap(p),before)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path,required=True);ap.add_argument('--case');ap.add_argument('--runtime',type=Path);a=ap.parse_args()
 if a.runtime:
  import sys
  for m in list(sys.modules.values()):
   if getattr(m,'__name__','').startswith('test_') and hasattr(m,'ROOT'):m.ROOT=a.runtime.resolve()
 names=[a.case] if a.case else [n for n in unittest.defaultTestLoader.getTestCaseNames(Phase47Integration) if n.startswith('test_47_')];r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite(Phase47Integration(n) for n in names));a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
