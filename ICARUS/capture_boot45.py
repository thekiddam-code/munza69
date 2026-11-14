"""Real startup with explicitly held network reply, not fabricated readiness."""
import argparse,json
from pathlib import Path
import test_umbra_browser as H
ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True);H.ROOT=a.runtime;T=H.UmbraBrowser;T.setUpClass();t=T();t.setUp()
try:
 c=T.browser.new_context(viewport={'width':1440,'height':1000});t.contexts.append(c);p=c.new_page();held=[];p.route('**/api/icarus/bootstrap',lambda r:held.append(r));p.goto(T.url+'/icarus.html',wait_until='domcontentloaded');p.screenshot(path=str(a.output/'startup.png'));(a.output/'startup.json').write_text(json.dumps({'label':'Actual startup with test-held bootstrap response; no readiness fabricated','bootstrap_responses_held':len(held),'boot':p.locator('#icarus-boot').count(),'writer':p.locator('#writer-status').all_text_contents()},indent=2))
finally:
 for r in held:
  try:r.continue_()
  except Exception:pass
 try:p.wait_for_timeout(100)
 except Exception:pass
 t.tearDown();T.tearDownClass()
