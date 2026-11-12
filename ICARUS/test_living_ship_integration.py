"""Phase 4.2 first milestone: actual physical activity and preserved world/clock contracts."""
import unittest
import test_living_world_integration as base
class LivingShipIntegration(base.LivingWorldIntegration):
 def test_existing_world_gains_private_activity_continuity_and_exact_reload(self):
  p=self.page();self.advance(p,120);s=self.snap(p);self.assertEqual(len(s['crew']),20);self.assertEqual(s['crewLife']['activityTick'],s['tick']);self.assertTrue(all(x.get('activity') for x in s['crewLife']['people'].values()));self.assertTrue(all(len(x.get('activityHistory',[]))<=16 for x in s['crewLife']['people'].values()));self.assertEqual(s['resourceAudit'],[]);self.assertEqual(s['knowledgeAudit'],[]);p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),s)
 def test_real_week_boundary_preserves_shift_and_activities_without_world_reset(self):
  p=self.page();self.advance(p,5);before=self.snap(p);p.evaluate('__icarusSoak.realStart(Date.parse("2026-06-07T23:59Z"),"UTC")');p.evaluate('__icarusSoak.realAdvance(Date.parse("2026-06-08T00:01Z"))');after=self.snap(p);self.assertEqual(after['episode'],before['episode']+1);self.assertGreater(after['tick'],before['tick']);self.assertEqual([x['name'] for x in after['crew']],[x['name'] for x in before['crew']]);self.assertEqual({n:x['shift'] for n,x in after['crewLife']['people'].items()},{n:x['shift'] for n,x in before['crewLife']['people'].items()});self.assertEqual(after['resourceAudit'],[])
 def test_views_do_not_advance_activity_or_invent_progress(self):
  p=self.page();self.advance(p,10);before=self.snap(p);p.evaluate("ICARUSCommandUI.navigate('operations','watch')");p.evaluate('__icarusSoak.phase3("render")');p.set_viewport_size({'width':1280,'height':800});self.assertEqual(self.snap(p),before)
 def test_full_phase41_backup_import_retains_existing_crew_routines_and_history(self):
  import json
  from pathlib import Path
  donor=Path('/workspace/work/phase41_final_validation/campaigns/normal_1001/backup_1001_30.json');self.assertTrue(donor.exists(),'Genuine Phase 4.1 migration fixture is required');old=json.loads(donor.read_text())['state'];p=self.page();p.set_default_timeout(600000);p.on('dialog',lambda d:d.accept());p.locator('#backupfile').set_input_files(str(donor));p.wait_for_function('(tick)=>__icarusSoak.time()===tick',arg=old['tick']);s=self.snap(p);self.assertEqual(s['tick'],old['tick']);self.assertEqual([q['name'] for q in s['crew']],[q['name'] for q in old['crew']]);self.assertEqual(s['economy'],old['economy']);self.assertEqual(s['navigation'],old['navigation']);
  for name,person in old['crewLife']['people'].items():
   for key in ['memories','recent','decisions','lastSocial','peerAt','preferredWork']:self.assertEqual(s['crewLife']['people'][name][key],person[key])
  self.assertTrue(all(x.get('shift') for x in s['crewLife']['people'].values()));p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),s)
if __name__=='__main__':unittest.main()
