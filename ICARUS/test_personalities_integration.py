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
 def test_phase42b_creator_cannot_select_partners_and_presentation_does_not_rewrite_history(self):
  p=self.page();self.deck(p,'settings','general');before=self.snap(p);p.locator('[aria-label="Relationship presentation"]').select_option('off');p.locator('[aria-label="Relationship presentation"]').select_option('mature');self.assertEqual(self.snap(p),before);p.keyboard.press('Control+Shift+F12');self.deck(p,'personnel','roster');box=p.locator('#detail details').filter(has=p.get_by_text('PRIVATE PERSONALITY & ADULT METADATA / CREATOR',exact=True));box.locator('summary').click();self.assertEqual(box.locator('select').count(),0);self.assertNotIn('consent',box.locator('button').inner_text().lower())
 def test_phase42b_private_event_from_seeded_mechanics_fixture_travels_and_reloads(self):
  p=self.page();p.evaluate('__icarusSoak.save()')
  result=p.evaluate("""()=>{const s=JSON.parse(localStorage.getItem('icarus-v02'));s.remoteCore.autonomyEnabled=false;const [p,q]=s.crew;for(const x of [p,q]){x.adult=true;x.room=x.target='A04';x.route=[];x.nav=null;x.maintenanceRoom=null;x.researchAssignment=null;x.emergencyId=null;x.vitals.health=100;x.vitals.fatigue=0;}const env={channel:{},coLocated:(p,q)=>ICARUSKnowledge.can(s,p.name,q.name,'conversation'),position:p=>ICARUSKnowledge.position(s,p.name),record:(kind,text,people,data,options={})=>{const r=ICARUSStory.record(s,kind,text,people,{...data,privateKnowledge:true});ICARUSKnowledge.observe(s,r,people,{...options,data});ICARUSCrewSocial.observe(s,r,people,data);return r;},privateRoom:()=> 'A05',travel:(x,room,task,duration)=>{x.goal=x.task=task;x.target=room;x.route=[room];x.nav=null;x.privateEventId=true;x.taskMinutes=duration;}};env.courtship=(p,q)=>ICARUSCrewSocial.courtship(s,p,q,env);let attempts=0;while(attempts++<400&&!s.crewSocial.privateEvents?.some(e=>e.status==='active')){s.tick+=300;s.minute+=300;s.clock.elapsed+=300;for(const x of [p,q]){x.social=10;x.energy=95;x.stress=5;}ICARUSCrewLife.talk(s,p,q,env);}sessionStorage.setItem('private-mechanics-fixture',JSON.stringify(s));return {attempts,events:s.crewSocial.privateEvents||[],scope:'Technical source-backed contact fixture, not an organic full-world run'};}""")
  self.assertTrue(any(e['status']=='active' for e in result['events']));self.configure(p,"Object.assign(s,JSON.parse(sessionStorage.getItem('private-mechanics-fixture')));");phases=[]
  for i in range(100):
   self.advance(p,1);s=self.snap(p);event=s['crewSocial']['privateEvents'][-1];phases.append(event['phase'])
   if event['phase']=='private':
    before=s;p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),before)
   if event['status']!='active':break
  self.assertIn('private',phases);self.assertEqual(event['status'],'completed');self.assertTrue(event['effectsApplied']);self.assertEqual(s['relationshipAudit'],[]);self.assertNotIn('privacy',s['world']['physicalWorld']['rooms'][event['room']]);before=s;p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),before);self.advance(p,1);self.assertEqual(self.snap(p)['crewSocial']['privateEvents'][-1]['completionSourceId'],event['completionSourceId'])
