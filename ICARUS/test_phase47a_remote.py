"""Authorized emulated Remote Deck, actual HTTP host; no physical-device claims."""
import argparse,json,unittest
from pathlib import Path
from test_drone_remote import DroneRemote
from test_continuity import RecordedResult
class FreightRemote(DroneRemote):
 def test_freight_remote_authority_dedup_and_unreported_transit(self):
  pc=self.page(pc=True);pc.wait_for_function('document.querySelector("#rd-bridge-status").textContent.includes("LINKED")');phone=self.page(width=390,height=844);self.tab(phone,'icarus');phone.wait_for_selector('.forward-deploy');phone.locator('.forward-deploy').click();pc.wait_for_function('__icarusSoak.snapshot().forwardOperations.deployment?.requested==="deployment"');phone.wait_for_function('document.querySelector(".drone-feedback").textContent.includes("Accepted:")');self.assertEqual(pc.evaluate('__icarusSoak.time()'),0);self.assertEqual(phone.evaluate('typeof ICARUSForwardDeployment'),'undefined');self.assertEqual(phone.evaluate('typeof __icarusSoak'),'undefined')
  auth={'Authorization':'Bearer test-client'};payload={'command':'forward:hold','requestId':'freight-hold-dedup'};a,x=self.req('/api/icarus/dispatch',payload,auth);b,y=self.req('/api/icarus/dispatch',payload,auth);self.assertEqual((a,b),(200,200));self.assertEqual(x['queued'],y['queued']);pc.wait_for_function('__icarusSoak.snapshot().forwardOperations.deployment.requested===null');self.assertEqual(pc.evaluate('__icarusSoak.snapshot().forwardOperations.vehicle.stage'),'parked');self.assertEqual(self.req('/api/icarus/dispatch',{'command':'forward:teleport','requestId':'invalid-freight'},auth)[0],400)
  pc.evaluate("ICARUSCommandUI.navigate('missions','active')");pc.locator('.forward-deploy').click()
  for _ in range(400):
   pc.evaluate('__icarusSoak.advance(1)')
   if pc.evaluate('__icarusSoak.snapshot().forwardOperations.vehicle.stage==="outbound"'):break
  else:self.fail('Freight did not physically depart')
  phone.wait_for_function('document.querySelector(".forward-status").textContent.includes("unreported")');self.assertLessEqual(phone.evaluate('document.documentElement.scrollWidth'),392);self.assertTrue(pc.evaluate('ICARUSHost.canWrite()&&ICARUSDurable.canWrite()'))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args()
 if a.runtime:
  import test_umbra_browser
  test_umbra_browser.ROOT=a.runtime.resolve()
 r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite([FreightRemote('test_freight_remote_authority_dedup_and_unreported_transit')]));a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
