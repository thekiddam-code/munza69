"""Private supplied-voyage archive access; input contents are never published."""
import argparse,json,unittest,hashlib
from pathlib import Path
import test_startup_size as B
from test_continuity import RecordedResult
class Voyage47(B.StartupSize):
 def test_47_retained_archive_and_first_twelve_are_accessible_without_mutation(self):
  p=self.existing();p.wait_for_function('document.querySelector("#rd-bridge-status").textContent.includes("LINKED")');p.evaluate("ICARUSCommandUI.navigate('missions','active')");expected=self.original['state']['droneOperations']['archive'];p.wait_for_function('n=>document.querySelectorAll(".drone-record option").length===n',arg=len(expected));self.assertEqual(p.locator('.drone-record option').evaluate_all('(els)=>els.map(e=>e.value)'),[c['id'] for c in expected]);p.locator('.drone-ops details').nth(2).locator('summary').click()
  for c in expected[:12]:
   p.locator('.drone-record').select_option(c['id']);self.assertIn(c['id'],p.locator('.drone-record-label').inner_text());self.assertEqual(int(p.locator('.drone-frame').get_attribute('max')),len(c['frames'])-1)
  p.locator('.drone-record').select_option(expected[0]['id']);p.locator('.drone-restart').click();p.wait_for_timeout(650);p.locator('.drone-pause').click();self.assertGreater(int(p.locator('.drone-frame').input_value()),0);self.assertTrue(p.evaluate('__icarusSoak.snapshot().droneOperations')==self.original['state']['droneOperations'],'Reading or playback changed the source archive');self.assertTrue(p.evaluate('ICARUSHost.canWrite()&&ICARUSDurable.canWrite()'));self.assertTrue(all(r['status']==200 and r['bytes']<=110000 for r in self.requests))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--backup',type=Path,required=True);ap.add_argument('--runtime',type=Path);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args();B.BACKUP=a.backup.resolve()
 if a.runtime:
  import test_umbra_browser
  test_umbra_browser.ROOT=a.runtime.resolve()
 r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite([Voyage47('test_47_retained_archive_and_first_twelve_are_accessible_without_mutation')]));a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'private_input_sha256':hashlib.sha256(B.BACKUP.read_bytes()).hexdigest(),'failures':[{'test':str(t),'detail':d[:4000]} for t,d in r.failures],'errors':[{'test':str(t),'detail':d[:4000]} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
