"""Real HTTP host and browser terminals; emulation does not certify physical devices."""
import json,unittest,argparse
from pathlib import Path
from test_drone_remote import DroneRemote
from test_anthology_integration import CoreIntegration
from test_continuity import RecordedResult
class SpecimenRemote(DroneRemote):
 def test_bio_remote_actual_shared_camera_and_inspection_request(self):
  pc=self.page(pc=True);pc.wait_for_function('document.querySelector("#rd-bridge-status").textContent.includes("LINKED")');CoreIntegration.configure(self,pc,'s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;');CoreIntegration.deck(self,pc,'missions','active');pc.locator('.field-request').click()
  for _ in range(12):
   pc.evaluate('__icarusSoak.advance(60)')
   if pc.evaluate('Object.values(__icarusSoak.snapshot().unifiedWorld.biologicalLife49.enclosures).some(e=>e.occupant)'):break
  self.assertTrue(pc.evaluate('Object.values(__icarusSoak.snapshot().unifiedWorld.biologicalLife49.enclosures).some(e=>e.occupant)'))
  phone=self.page(width=390,height=844);self.tab(phone,'icarus');phone.wait_for_function('document.querySelector(".specimen-ops")?.textContent.includes("BIO49-")');self.assertEqual(phone.evaluate('typeof ICARUSSpecimenLife'),'undefined');self.assertEqual(phone.evaluate('typeof __icarusSoak'),'undefined');self.assertNotIn('habitats',phone.locator('.specimen-ops').inner_text());button=phone.locator('.specimen-ops [data-enclosure]:enabled').first;ident=button.get_attribute('data-enclosure');button.click();pc.wait_for_function('(id)=>__icarusSoak.snapshot().unifiedWorld.biologicalLife49.requests[id]!==undefined',arg=ident);self.assertLessEqual(phone.evaluate('document.documentElement.scrollWidth'),390)
  phone.locator('.bio-camera').click();phone.wait_for_function('document.querySelector(".obs-select").value==="B03"');self.assertEqual(pc.evaluate('__icarusSoak.snapshot().biologyAudit'),[])
 def test_bio_remote_command_allowlist_authentication_and_deduplication(self):
  pc=self.page(pc=True);pc.wait_for_function('document.querySelector("#rd-bridge-status").textContent.includes("LINKED")');auth={'Authorization':'Bearer test-client'}
  for cmd in ['biology:release:BIO-1','biology:inspect:BIO-99','biology:inspect:../../x','biology:spawn:defender']:
   code,_=self.req('/api/icarus/dispatch',{'command':cmd,'requestId':'invalid-bio-'+str(len(cmd))},auth);self.assertEqual(code,400)
  self.assertEqual(self.req('/api/icarus/dispatch',{'command':'biology:inspect:BIO-1','requestId':'bio-auth-test'}, {})[0],401)
  request={'command':'biology:inspect:BIO-1','requestId':'bio-dedup-test'};a,one=self.req('/api/icarus/dispatch',request,auth);b,two=self.req('/api/icarus/dispatch',request,auth);self.assertEqual((a,b),(200,200));self.assertEqual(one['queued'],two['queued'])
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path,required=True);args=ap.parse_args();names=[n for n in unittest.defaultTestLoader.getTestCaseNames(SpecimenRemote) if n.startswith('test_bio_')];r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite(SpecimenRemote(n) for n in names));args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[(str(t),d) for t,d in r.failures],'errors':[(str(t),d) for t,d in r.errors],'skipped':[(str(t),d) for t,d in r.skipped]},indent=2));raise SystemExit(not r.wasSuccessful())
