"""Actual browser expedition regressions. Any changed initial conditions are explicit technical fixtures."""
from test_operations_integration import OperationsIntegration
class ExpeditionIntegration(OperationsIntegration):
 def start_field(self,p):
  self.configure(p,"s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;")
  self.deck(p,'missions','active');p.locator('.field-request').click();self.assertTrue(self.snap(p)['missions']['asteroid'].get('ops44'))
 def test_field_physical_preparation_route_return_and_source_records(self):
  p=self.page();self.start_field(p);seen=set();ship_nodes=set();first_id=self.snap(p)['missions']['asteroid']['id'];observed=False
  for i in range(1000):
   self.advance(p,1);s=self.snap(p);m=s['missions']['asteroid']
   if m:
    seen.add(m['ops44']['stage']);ship_nodes.update(q['room'] for q in s['crew'] if q.get('expeditionId')==first_id and not q.get('expeditionAway'))
    if m['ops44']['stage']=='field' and m['ops44']['edge']:
     views=p.evaluate('__icarusSoak.observation().rooms.filter(r=>r.kind==="field"&&r.available)');observed|=bool(views and views[0]['actors']);self.assertEqual(s['expeditionAudit'],[])
   if s['expeditionOperations']['history']:break
  self.assertTrue(s['expeditionOperations']['history']);self.assertTrue({'collect','stage','airlock','depressurizing','outbound','field','homebound','repressurizing'}.issubset(seen),seen);self.assertTrue({'C04','C01','C02'}.issubset(ship_nodes),ship_nodes);self.assertTrue(observed);self.assertTrue(s['fieldEvidence']['archive']);self.assertEqual(s['resourceAudit'],[]);self.assertEqual(s['expeditionAudit'],[]);self.assertTrue(all(q['status']=='stored' for q in s['fieldEvidence']['devices'].values()));self.assertEqual(s['unifiedWorld']['organisms']['XENO-INITIAL']['dormant'],True)
 def test_field_save_inside_real_segment_preserves_exact_future(self):
  p=self.page();self.start_field(p)
  for i in range(500):
   self.advance(p,1);s=self.snap(p);o=s['missions']['asteroid']['ops44']
   if o['edge'] and o['edge']['elapsed']>1:break
  self.assertIsNotNone(o['edge']);before=self.snap(p);p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),before);self.advance(p,40);s=self.snap(p);self.assertEqual(s['resourceAudit'],[]);self.assertEqual(s['expeditionAudit'],[])
 def test_field_two_sorties_physically_link_industrial_and_cavern_terrain(self):
  p=self.page();self.start_field(p)
  for sortie in range(2):
   for i in range(70):
    self.advance(p,20);s=self.snap(p)
    if len(s['expeditionOperations']['history'])>=sortie+1:break
   self.assertGreaterEqual(len(s['expeditionOperations']['history']),sortie+1)
   if sortie==0:self.deck(p,'missions','active');p.locator('.field-request').click();self.assertIsNotNone(self.snap(p)['missions']['asteroid'])
  visited=[r for r in s['world']['asteroidExploration']['rooms'] if r['visited']];self.assertIn('industrial',[r['field']['kind'] for r in visited]);self.assertIn('cavern',[r['field']['kind'] for r in visited]);self.assertEqual(s['unifiedWorld']['military']['doors']['23'],'sealed');self.assertEqual(s['resourceAudit'],[]);self.assertEqual(len(s['fieldEvidence']['devices']),2,'Returned physical cameras should be reused, not conjured/rebuilt')
 def test_field_powered_receiver_loss_hides_live_views_and_local_records(self):
  p=self.page();self.start_field(p)
  for i in range(30):
   self.advance(p,10);s=self.snap(p);m=s['missions']['asteroid']
   if m and m['ops44']['stage']=='field':break
  self.assertEqual(m['ops44']['stage'],'field');self.deck(p,'ship','systems');p.locator('.systems-zone').select_option('science');p.locator('[data-op="circuit"]').click();self.advance(p,1);before=len(self.snap(p)['fieldEvidence']['archive']);self.advance(p,30);s=self.snap(p);self.assertGreater(sum(len(d['clips']) for d in s['fieldEvidence']['devices'].values()),0);self.assertEqual(len(s['fieldEvidence']['archive']),before);views=p.evaluate('__icarusSoak.observation().rooms.filter(r=>r.kind==="field")');self.assertTrue(views);self.assertTrue(all(not r['available'] and not r['actors'] for r in views));p.locator('[data-op="circuit"]').click();self.advance(p,5);self.assertGreater(len(self.snap(p)['fieldEvidence']['archive']),before);self.assertEqual(self.snap(p)['resourceAudit'],[])
 def test_field_mid_passage_obstruction_reverses_actual_progress_without_teleport(self):
  p=self.page();self.start_field(p)
  for i in range(300):
   self.advance(p,1);o=self.snap(p)['missions']['asteroid']['ops44']
   if o['edge'] and o['edge']['elapsed']>=2:break
  self.assertIsNotNone(o['edge']);e=o['edge'];key='-'.join(str(i) for i in sorted([e['from'],e['to']]));self.change(p,"s.asteroidExploration.operationsGeometry.edges["+__import__('json').dumps(key)+"].closed=true;");self.advance(p,1);after=self.snap(p)['missions']['asteroid']['ops44'];self.assertEqual(after['node'],e['from']);self.assertTrue(after['edge']['retreat']);self.assertEqual(after['edge']['elapsed'],e['elapsed']-1);self.assertEqual(self.snap(p)['expeditionAudit'],[])
 def test_field_paid_repair_tests_actual_lift_power_without_creating_energy(self):
  p=self.page();self.start_field(p)
  for sortie in range(2):
   for i in range(80):
    self.advance(p,20);s=self.snap(p)
    if len(s['expeditionOperations']['history'])>=sortie+1:break
   self.assertGreaterEqual(len(s['expeditionOperations']['history']),sortie+1)
   if sortie==0:self.deck(p,'missions','active');p.locator('.field-request').click()
  before=s['world']['asteroidExploration']['rooms'][5]['field']['utility'];self.assertLess(before['condition'],60);self.deck(p,'missions','active');p.locator('.field-category').select_option('repair');p.locator('.field-target').select_option('5');p.locator('.field-request').click()
  for wait in range(60):
   if self.snap(p)['missions']['asteroid']:break
   self.advance(p,20);self.deck(p,'missions','active');p.locator('.field-request').click()
  self.assertIsNotNone(self.snap(p)['missions']['asteroid'],p.locator('.field-feedback').inner_text())
  for i in range(80):
   self.advance(p,20);s=self.snap(p)
   if len(s['expeditionOperations']['history'])>=3:break
  utility=s['world']['asteroidExploration']['rooms'][5]['field']['utility'];self.assertGreaterEqual(utility['condition'],86);self.assertGreater(utility['battery'],0);self.assertEqual(s['expeditionOperations']['history'][-1]['reason'],'objective_met');self.assertEqual(s['resourceAudit'],[]);self.assertTrue(any('powered post-test' in c['reason'] for c in s['fieldEvidence']['archive']));self.assertEqual(s['expeditionAudit'],[])
 def test_field_lost_recording_requires_physical_recovery_and_powered_ingestion(self):
  p=self.page();self.configure(p,"s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.shipSystems.zones.science.circuitIsolated=true;");self.deck(p,'missions','active');p.locator('.field-request').click()
  for i in range(40):
   self.advance(p,5);s=self.snap(p);m=s['missions']['asteroid']
   if m and m['ops44']['stage']=='field':break
  self.assertEqual(m['ops44']['stage'],'field');device=m['ops44']['devices'][0];self.assertTrue(s['fieldEvidence']['devices'][device]['clips']);self.assertEqual(s['fieldEvidence']['archive'],[])
  # Explicit technical dropped-device fixture; every stored frame already came from this real sortie.
  self.change(p,"const m=s.remoteCore.missions.asteroid,d=s.fieldEvidence.devices["+__import__('json').dumps(device)+"];d.status='lost';d.location=m.ops44.node;d.carrier=null;m.ops44.devices=m.ops44.devices.filter(id=>id!==d.id);")
  for i in range(60):
   self.advance(p,10);s=self.snap(p)
   if s['expeditionOperations']['history']:break
  self.assertTrue(s['expeditionOperations']['history']);self.assertEqual(s['fieldEvidence']['devices'][device]['status'],'stored');self.assertTrue(s['fieldEvidence']['devices'][device]['clips']);self.assertEqual(s['fieldEvidence']['archive'],[])
  self.deck(p,'ship','systems');p.locator('.systems-zone').select_option('science');p.locator('[data-op="circuit"]').click();self.advance(p,3);s=self.snap(p);self.assertTrue(s['fieldEvidence']['archive']);self.assertEqual(s['fieldEvidence']['devices'][device]['clips'],[]);self.assertTrue(s['director']['intelligence']['asteroid']['pendingSurvey']);by={r['id']:r for r in s['chronicle']['records']};self.assertTrue(all(r['sourceId'] in by and not by[r['sourceId']].get('data',{}).get('privateKnowledge') for r in s['fieldEvidence']['archive']));self.assertEqual(s['resourceAudit'],[]);self.assertEqual(s['expeditionAudit'],[])
 def test_field_recall_waits_for_actual_communications(self):
  p=self.page();self.start_field(p)
  for i in range(40):
   self.advance(p,5);m=self.snap(p)['missions']['asteroid']
   if m and m['ops44']['stage']=='field':break
  self.assertEqual(m['ops44']['stage'],'field');self.deck(p,'ship','systems');p.locator('.systems-zone').select_option('science');p.locator('[data-op="circuit"]').click();self.advance(p,1);self.deck(p,'missions','active');p.locator('.field-recall').click();self.advance(p,4);m=self.snap(p)['missions']['asteroid'];self.assertTrue(m['ops44']['pendingRecall']);self.assertFalse(m['ops44']['returning']);self.deck(p,'ship','systems');p.locator('.systems-zone').select_option('science');p.locator('[data-op="circuit"]').click();self.advance(p,4);m=self.snap(p)['missions']['asteroid'];self.assertIsNone(m['ops44']['pendingRecall']);self.assertTrue(m['ops44']['returning']);self.assertEqual(m['ops44']['returnReason'],'authorized_recall');self.assertEqual(self.snap(p)['resourceAudit'],[])
