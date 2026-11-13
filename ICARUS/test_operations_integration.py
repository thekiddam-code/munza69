"""Actual physical engine tests; adverse fixtures are explicit, never presented as organic incidents."""
from test_personalities_integration import PersonalitiesIntegration
class OperationsIntegration(PersonalitiesIntegration):
 def test_ops_independent_gravity_and_saved_controls(self):
  p=self.page();self.deck(p,'ship','systems');p.locator('.systems-zone').select_option('cargo');p.locator('.systems-target').select_option('0');p.locator('[data-op="gravity"]').click();self.assertEqual(self.snap(p)['shipSystems']['zones']['cargo']['targetG'],0);self.advance(p,6);s=self.snap(p);self.assertEqual(s['shipSystems']['zones']['cargo']['g'],0);self.assertEqual(s['shipSystems']['zones']['medical']['g'],1);self.assertEqual(s['systemsAudit'],[]);self.assertEqual(s['resourceAudit'],[]);p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),s)
 def test_ops_float_actual_loose_objects_and_local_power(self):
  p=self.page();self.configure(p,"""s.remoteCore.autonomyEnabled=false;const q=s.crew[0];q.room=q.target='C03';q.route=[];q.nav=null;q.task=q.goal='Resting';q.taskMinutes=90;q.maintenanceRoom=null;s.physicalWorld.rooms.C03.objects={sample:{name:'sample container',discovered:true,condition:100,massKg:8}};s.shipSystems.zones.cargo.targetG=0;""");self.advance(p,15);s=self.snap(p);q=s['crew'][0];self.assertEqual(q['gravityMotion']['mode'],'floating');self.assertGreater(s['world']['physicalWorld']['rooms']['C03']['objects']['sample']['gravityMotion']['height'],0);view=p.evaluate('__icarusSoak.observation().rooms.find(r=>r.id==="C03")');self.assertEqual(view['actors'][0]['state'],'float');self.assertEqual(s['resourceAudit'],[])
 def test_ops_engineer_real_diagnose_collect_repair_test(self):
  p=self.page();self.configure(p,"""s.remoteCore.autonomyEnabled=false;s.shipSystems.components['GRAVITY-CORE'].health=64;for(const q of s.crew.filter(q=>q.job==='Engineer')){q.taskMinutes=0;q.energy=95;q.emergencyId=null;q.maintenanceRoom=null;}""");seen=set();poses=[]
  for i in range(420):
   self.advance(p,1);s=self.snap(p);order=s['world']['maintenance'].get('systemOrders',{}).get('GRAVITY-CORE');c=s['shipSystems']['components']['GRAVITY-CORE'];
   if order:
    seen.add(order['phase']);worker=next((q for q in s['crew'] if q.get('systemAssignment')=='GRAVITY-CORE'),None)
    if worker and worker['room']=='C07' and not worker['route'] and worker.get('interaction')=='working':poses+=p.evaluate('__icarusSoak.observation().rooms.find(r=>r.id==="C07").actors.map(a=>a.state)')
   if c['history']:break
  self.assertTrue(c['history'],'Real engineering work did not complete');self.assertGreaterEqual(c['health'],85);self.assertTrue({'diagnosing','waiting-parts','repairing','testing'}.issubset(seen));self.assertIn('repair',poses);self.assertEqual(s['resourceAudit'],[]);self.assertEqual(s['systemsAudit'],[]);self.assertTrue(c['history'][0]['sourceId'])
