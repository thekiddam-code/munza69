"""Physical freight/camp tests in explicit isolated technical worlds, never the live voyage."""
import argparse,json,unittest
from pathlib import Path
from test_drone_integration import DroneIntegration
from test_continuity import RecordedResult
OUT=Path('/workspace/work/phase47a/screenshots')
class DeploymentIntegration(DroneIntegration):
 def base(self):
  p=self.page();self.configure(p,"s.frontier.enabled=false;s.navigation.hold=true;s.remoteCore.autonomyEnabled=false;");return p
 def brief(self,p):
  return p.evaluate("(()=>{const s=__icarusSoak.snapshot();return {tick:s.tick,forward:s.forwardOperations,mission:s.missions.asteroid,crew:s.crew.filter(q=>q.expeditionId||q.forwardAssignment).map(q=>({name:q.name,room:q.room,route:q.route,task:q.task,forward:q.forwardAssignment})),history:s.expeditionOperations.history,resourceAudit:s.resourceAudit};})()")
 def wait(self,p,predicate,limit=1200):
  for _ in range(limit):
   self.advance(p,1);s=self.brief(p)
   if predicate(s):return s
  self.fail('Physical objective timed out: '+json.dumps(s)[:5000])
 def deploy(self,p):
  self.deck(p,'missions','active');p.locator('.forward-deploy').click();self.assertEqual(self.snap(p)['forwardOperations']['deployment']['requested'],'deployment');return self.wait(p,lambda s:s['forward']['vehicle']['stage']=='deployed')
 def test_deployment_real_loading_travel_setup_and_reload(self):
  p=self.base();before=self.snap(p);self.assertEqual(before['forwardOperations']['vehicle']['room'],'C03')
  self.deck(p,'missions','active');p.locator('.forward-deploy').click();self.assertEqual(self.snap(p)['forwardOperations']['deployment']['requested'],'deployment');seen=set();reload_done=False;empty_captured=False
  for _ in range(1500):
   self.advance(p,1);s=self.brief(p);seen.add(s['forward']['vehicle']['stage']);m=s['mission']
   if m and m['ops44'].get('freight') and m['ops44']['freight']['load']==4 and not reload_done:
    full=self.snap(p);p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),full);reload_done=True
   if s['forward']['vehicle']['stage']=='outbound' and not empty_captured:
    self.deck(p,'operations','watch');p.wait_for_function('ICARUSObservationLive.camera.tick===__icarusSoak.time()');before_view=self.snap(p);p.evaluate("ICARUSObservationLive.camera.pick('C03');ICARUSObservationLive.camera.draw(true)");OUT.mkdir(parents=True,exist_ok=True);p.locator('#observation-primary').screenshot(path=str(OUT/'actual_empty_cargo_parking.png'));self.assertEqual(self.snap(p),before_view);self.deck(p,'missions','active');empty_captured=True
   if s['mission'] and s['mission']['ops44'].get('action')=='camp-setup' and s['forward']['vehicle']['stage']=='setting-up':
    actors=p.evaluate('__icarusSoak.observation().rooms.filter(r=>r.kind==="field"&&r.available).flatMap(r=>r.actors)');self.assertTrue(actors);self.assertTrue(all(q['state']=='repair' for q in actors))
   if s['forward']['vehicle']['stage']=='deployed':
    self.assertEqual(s['forward']['deployment']['camp']['node'],0);self.assertGreater(len(s['forward']['deployment']['camp']['objects']),10);self.assertIsNotNone(m);self.assertEqual(m['ops44']['node'],0);OUT.mkdir(parents=True,exist_ok=True);views=p.evaluate('__icarusSoak.observation().rooms.filter(r=>r.kind==="field"&&r.available)');self.assertTrue(any((v.get('forward') or {}).get('camp') for v in views));p.evaluate('v=>{const c=document.createElement("canvas");c.id="camp-capture";document.body.append(c);ICARUSPixelCamera.draw(c,v,{paused:true,reduced:true});}',next(v for v in views if (v.get('forward') or {}).get('camp')));p.locator('#camp-capture').screenshot(path=str(OUT/'actual_camp_body_camera.png'));break
  else:self.fail(json.dumps(s)[:5000])
  self.assertTrue({'parked','loading','loaded','outbound','unloading','setting-up','deployed'}.issubset(seen),seen);self.assertTrue(reload_done);self.assertTrue(empty_captured);full=self.snap(p);self.assertEqual(full['resourceAudit'],[]);self.assertEqual(full['expeditionAudit'],[]);self.assertTrue(p.evaluate('__icarusSoak.save()'));p.reload();self.assertEqual(self.snap(p),full);self.wait(p,lambda s:not s['mission']);self.assertEqual([q['name'] for q in self.snap(p)['crew']],[q['name'] for q in before['crew']]);self.assertTrue(self.snap(p)['unifiedWorld']['organisms']['XENO-INITIAL']['dormant'])
 def test_deployment_recovery_packing_real_return_and_no_repeat_loop(self):
  p=self.base();initial=self.snap(p)['forwardOperations']['vehicle'];self.deploy(p);self.wait(p,lambda s:not s['mission']);self.deck(p,'missions','active');p.locator('.forward-recover').click();seen=set()
  for _ in range(1400):
   self.advance(p,1);s=self.brief(p);seen.add(s['forward']['vehicle']['stage'])
   if s['forward']['vehicle']['stage']=='parked' and not s['mission']:break
  else:self.fail(json.dumps(s)[:5000])
  self.assertIn('loading-field',seen);self.assertIn('homebound',seen);self.assertIn('securing',seen);self.assertEqual(s['forward']['vehicle']['equipment'],initial['equipment']);self.assertEqual(s['forward']['vehicle']['stock'],initial['stock']);self.assertIsNone(s['forward']['deployment']['camp']);self.assertEqual(s['resourceAudit'],[]);full=self.snap(p);p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),full);self.advance(p,90);self.assertIsNone(self.snap(p)['forwardOperations']['deployment']['requested'])
 def test_deployment_recall_during_partial_loading_preserves_vehicle_and_cargo(self):
  p=self.base();self.deck(p,'missions','active');p.locator('.forward-deploy').click();s=self.wait(p,lambda s:s['mission'] is not None and s['mission']['ops44'].get('freight',{}).get('load')==3);mid=self.snap(p);p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),mid);p.evaluate('id=>document.querySelector(".field-recall").click()',s['mission']['id']);s=self.wait(p,lambda s:not s['mission'] and s['forward']['vehicle']['stage']=='parked');self.assertIsNone(s['forward']['deployment']['camp']);self.assertEqual(s['forward']['vehicle']['room'],'C03');self.assertEqual(s['resourceAudit'],[])
 def test_deployment_power_interruption_holds_loading_without_teleport_or_free_power(self):
  p=self.base();self.deck(p,'missions','active');p.locator('.forward-deploy').click();s=self.wait(p,lambda s:s['mission'] is not None and s['mission']['ops44'].get('freight',{}).get('load')==3);self.deck(p,'ship','systems');p.locator('.systems-zone').select_option('cargo');p.locator('[data-op="circuit"]').click();self.advance(p,20);after=self.brief(p);self.assertEqual(after['mission']['ops44']['freight']['load'],3);self.assertEqual(after['forward']['vehicle']['room'],'C03');self.assertIsNone(after['forward']['deployment']['camp']);self.assertEqual(after['resourceAudit'],[]);p.locator('[data-op="circuit"]').click();self.wait(p,lambda s:s['forward']['vehicle']['stage']=='deployed')
 def test_deployment_week_transition_preserves_loaded_vehicle_and_active_flight(self):
  p=self.base();self.deck(p,'missions','active');p.locator('.forward-deploy').click();self.wait(p,lambda s:s['forward']['vehicle']['stage']=='outbound' and s['mission']['ops44']['flight']==10);start=1794808785000;p.evaluate('t=>__icarusSoak.realStart(t,"America/Chicago")',start);before=self.snap(p);p.evaluate('t=>__icarusSoak.realAdvance(t+30000,120)',start);after=self.snap(p);self.assertEqual(after['tick']-before['tick'],2);self.assertEqual(after['episode'],before['episode']+1);self.assertEqual(after['missions']['asteroid']['id'],before['missions']['asteroid']['id']);self.assertEqual(after['forwardOperations']['vehicle']['stage'],'outbound');self.assertEqual(after['missions']['asteroid']['ops44']['freight'],before['missions']['asteroid']['ops44']['freight']);self.assertTrue(p.evaluate('__icarusSoak.save()'));p.reload();self.assertEqual(self.snap(p),after)
 def test_deployment_field_report_waits_for_real_radio_or_returned_crew(self):
  p=self.base();self.deck(p,'missions','active');p.locator('.forward-deploy').click();self.wait(p,lambda s:s['forward']['vehicle']['stage']=='outbound' and s['mission']['ops44']['flight']==40);self.deck(p,'ship','systems');p.locator('.systems-zone').select_option('science');p.locator('[data-op="circuit"]').click();self.wait(p,lambda s:s['forward']['vehicle']['stage']=='deployed');projection=p.evaluate('ICARUSForwardOps.project(__icarusSoak.snapshot())');self.assertIsNone(projection['camp']);self.assertIsNone(projection['vehicle']['condition']);self.assertFalse(any(r['available'] for r in p.evaluate('__icarusSoak.observation().rooms.filter(r=>r.kind==="field")')));p.locator('[data-op="circuit"]').click();self.wait(p,lambda s:not s['mission']);projection=p.evaluate('ICARUSForwardOps.project(__icarusSoak.snapshot())');self.assertIsNotNone(projection['camp']);self.assertEqual(projection['camp']['stage'],'deployed')
 def test_deployment_unreported_site_change_is_found_on_approach_without_landing(self):
  p=self.base();self.deck(p,'missions','active');p.locator('.forward-deploy').click();self.wait(p,lambda s:s['forward']['vehicle']['stage']=='outbound' and s['mission']['ops44']['flight']==10);self.change(p,"s.asteroidExploration.rooms[0].field.stability=.2;");s=self.wait(p,lambda s:s['forward']['vehicle']['stage']=='homebound');self.assertIsNone(s['mission']['ops44']['node']);self.assertIsNone(s['forward']['deployment']['camp']);self.assertEqual(s['mission']['ops44']['returnReason'],'landing_site_unsafe');self.assertTrue(s['mission']['ops44']['freight']['loaded']);s=self.wait(p,lambda s:not s['mission'] and s['forward']['vehicle']['stage']=='parked');self.assertEqual(s['resourceAudit'],[]);self.assertIsNone(s['forward']['deployment']['camp'])
 def test_deployment_autonomous_decision_uses_a_real_completed_sortie(self):
  p=self.base();self.start_field(p);s=self.wait(p,lambda s:not s['mission'] and any(len(h['visited'])>=5 for h in s['history']));basis=next(h['id'] for h in reversed(s['history']) if len(h['visited'])>=5);self.assertIsNone(s['forward']['deployment']['requested']);self.change(p,"s.remoteCore.autonomyEnabled=true;");s=self.wait(p,lambda s:s['forward']['deployment']['requested']=='deployment' or s['forward']['deployment'].get('missionId'));self.assertEqual(s['forward']['deployment']['lastNeedBasis'],basis);self.assertEqual(s['forward']['vehicle']['room'],'C03');s=self.wait(p,lambda s:s['forward']['vehicle']['stage']=='deployed',limit=2000);self.assertEqual(s['forward']['deployment']['camp']['node'],0);self.assertEqual(s['resourceAudit'],[])
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path);ap.add_argument('--case');ap.add_argument('--report',type=Path,required=True);a=ap.parse_args()
 if a.runtime:
  import sys
  for m in list(sys.modules.values()):
   if getattr(m,'__name__','').startswith('test_') and hasattr(m,'ROOT'):m.ROOT=a.runtime.resolve()
 names=[a.case] if a.case else [n for n in unittest.defaultTestLoader.getTestCaseNames(DeploymentIntegration) if n.startswith('test_deployment_')];r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite(DeploymentIntegration(n) for n in names));a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
