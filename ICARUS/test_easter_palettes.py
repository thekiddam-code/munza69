"""Historical component palette fidelity, not new art or trigger/state changes."""
import argparse,json,unittest
from pathlib import Path
from test_easter_visuals import EasterVisuals
from test_continuity import RecordedResult
BEFORE=False
class EasterPalettes(EasterVisuals):
 def themed(self):
  p=self.page()
  if BEFORE:p.route('**/umbra/anomaly-palette.css',lambda r:r.fulfill(content_type='text/css',body=''));p.reload();p.wait_for_function('!!window.UmbraApp')
  self.enable(p);return p
 def test_palette_original_component_colors_are_distinct_and_scoped(self):
  p=self.themed();self.assertEqual(p.locator('.umbra-specimen').evaluate('(e)=>getComputedStyle(e).opacity'),'1');self.assertEqual(p.locator('.umbra-scan').evaluate('(e)=>getComputedStyle(e).color'),'rgb(160, 228, 195)');self.assertEqual(p.locator('.wy-panel-tag').evaluate('(e)=>getComputedStyle(e).color'),'rgb(189, 167, 108)');self.assertEqual(p.locator('.wy-hazard').evaluate('(e)=>getComputedStyle(e).height'),'5px');self.assertIn('rgb(179, 154, 83)',p.locator('.wy-hazard').evaluate('(e)=>getComputedStyle(e).backgroundImage'));self.assertEqual(p.locator('body').evaluate('(e)=>getComputedStyle(e).backgroundColor'),'rgb(8, 15, 27)')
 def test_palette_survives_theme_media_reduced_motion_and_phone_layout(self):
  p=self.themed()
  for scheme in ['dark','light']:
   p.emulate_media(color_scheme=scheme,reduced_motion='reduce');p.set_viewport_size({'width':393,'height':851});self.assertEqual(p.locator('.wy-panel-tag').evaluate('(e)=>getComputedStyle(e).color'),'rgb(189, 167, 108)');self.assertEqual(p.locator('.umbra-scan').evaluate('(e)=>getComputedStyle(e).color'),'rgb(160, 228, 195)');self.assertLessEqual(p.evaluate('document.documentElement.scrollWidth'),393)
  self.tab(p,'settings');p.locator('#umbra-arcade-archive summary').click();p.wait_for_selector('#umbra-arcade-gallery img');self.assertEqual(p.locator('#umbra-arcade-gallery img').first.evaluate('(e)=>getComputedStyle(e).filter'),'none');self.assertEqual(p.evaluate('typeof __icarusSoak'),'undefined')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path,required=True);ap.add_argument('--before',action='store_true');a=ap.parse_args();BEFORE=a.before
 names=[n for n in unittest.defaultTestLoader.getTestCaseNames(EasterPalettes) if n.startswith('test_palette_')];r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.TestSuite(EasterPalettes(n) for n in names));a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
