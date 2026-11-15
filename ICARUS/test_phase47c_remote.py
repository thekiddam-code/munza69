"""Authorized emulated Remote Deck, actual HTTP host; no physical-device claims."""
import argparse,json,unittest
from pathlib import Path
from test_drone_remote import DroneRemote
from test_continuity import RecordedResult
class SurveillanceRemote(DroneRemote):
 def test_c_original_archive_loads_on_demand_and_remains_receive_only(self):
  self.test_drone_live_and_recovered_frames_cross_real_http_without_second_world();pc=self.pc;phone=self.phone;phone.locator('.drone-ops details').nth(2).locator('summary').click();ids=pc.evaluate('__icarusSoak.snapshot().droneOperations.archive.map(c=>c.id)');self.assertGreater(len(ids),1);phone.locator('.drone-record').select_option(ids[0]);phone.locator('.drone-load').click();phone.wait_for_function('document.querySelector(".drone-record-label").textContent.includes("CAPTURED PROCEDURAL FRAME")',timeout=30000);self.assertEqual(int(phone.locator('.drone-frame').get_attribute('max')),pc.evaluate('id=>__icarusSoak.snapshot().droneOperations.archive.find(c=>c.id===id).frames.length-1',ids[0]));self.assertEqual(phone.evaluate('typeof ICARUSDroneOps'),'undefined');self.assertEqual(self.req('/api/icarus/record?id='+ids[0])[0],401)
 def page(self,*args,**kwargs):
  p=super().page(*args,**kwargs)
  if kwargs.get('pc'):self.pc=p
  else:self.phone=p
  return p
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args()
 if a.runtime:
  import test_umbra_browser
  test_umbra_browser.ROOT=a.runtime.resolve()
 r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite([SurveillanceRemote('test_c_original_archive_loads_on_demand_and_remains_receive_only')]));a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
