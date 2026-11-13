"""Phase 4.2B focused browser cases; fixture setup is explicitly technical, not an organic voyage claim."""
from test_observation_integration import ObservationIntegration
class PersonalitiesIntegration(ObservationIntegration):
 def test_phase42b_cross_deck_journey_uses_one_cabin_and_camera_occupancy(self):
  p=self.page();self.configure(p,"""s.remoteCore.autonomyEnabled=false;const q=s.crew[0];q.room='C05';q.target='A04';q.task=q.goal='Eating a meal';q.route=['A04'];q.nav=null;q.taskMinutes=100;q.maintenanceRoom=null;q.energy=95;""");seen=[]
  for i in range(70):
   s=self.snap(p);q=s['crew'][0];view=p.evaluate('__icarusSoak.observation()');cameras=[r['id'] for r in view['rooms'] if r.get('camera') and any(a['name']==q['name'] for a in r['actors'])];self.assertLessEqual(len(cameras),1);seen+=cameras;self.assertEqual(s['transitAudit'],[])
   if q['room']=='A04' and not q['route']:break
   self.advance(p,1)
  self.assertEqual(q['room'],'A04');self.assertIn('LIFT-01',seen);self.assertIn('COR-C-2',seen);self.assertIn('COR-A-2',seen);self.assertIn('A04',seen);self.assertEqual(s['resourceAudit'],[])
 def test_phase42b_topology_doors_and_follow_privacy_persist(self):
  p=self.page();view=p.evaluate('__icarusSoak.observation()');doors=[d['room'] for r in view['rooms'] for d in r.get('doors',[])];self.assertEqual(len(doors),30);self.assertEqual(len(set(doors)),30);self.operations(p);p.locator('.obs-follow').select_option('Frank Morrow');self.assertEqual(p.evaluate('ICARUSObservationLive.camera.following'),'Frank Morrow');self.configure(p,"const q=s.crew[0];q.room=q.target='A05';q.nav=null;q.route=[];q.taskMinutes=99;");self.operations(p);p.wait_for_timeout(1200);self.assertIsNone(p.evaluate('ICARUSObservationLive.camera.selected'));self.assertIn('PRIVACY / COVERAGE UNAVAILABLE',p.locator('.obs-status').inner_text());self.assertEqual(self.snap(p)['crew'][0]['room'],'A05');p.locator('.obs-manual').click();self.assertEqual(p.evaluate('ICARUSObservationLive.camera.following'),'')
 def test_phase42b_lift_boarded_save_load_keeps_cabin_and_future(self):
  a=self.page();b=self.page();code="""s.remoteCore.autonomyEnabled=false;const q=s.crew[0];q.room='C05';q.target='A04';q.task=q.goal='Eating a meal';q.route=['A04'];q.nav=null;q.taskMinutes=100;q.energy=95;""";self.configure(a,code);self.configure(b,code)
  for i in range(40):
   if self.snap(a)['crew'][0].get('liftRide'):break
   self.advance(a,1);self.advance(b,1)
  before=self.snap(a);self.assertIsNotNone(before['crew'][0].get('liftRide'));a.evaluate('__icarusSoak.save()');a.reload();self.assertEqual(self.snap(a),before);self.advance(a,35);self.advance(b,35);self.assertEqual(self.snap(a),self.snap(b))
