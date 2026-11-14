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
