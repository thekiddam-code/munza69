"""Actual local restricted camera, source-labeled technical example. No ordinary privacy bypass."""
import argparse,json,time
from pathlib import Path
import test_umbra_browser as H
ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True);H.ROOT=a.runtime;T=H.UmbraBrowser;T.setUpClass();t=T();t.setUp()
try:
 p=t.page(pc=True);p.evaluate('__icarusSoak.advance(1)');
 deadline=time.monotonic()+30
 while time.monotonic()<deadline:
  code,data=t.req('/api/icarus/classified',headers={'X-Icarus-Key':'test-host'}) if hasattr(t,'req') else (200,p.evaluate("ICARUSHost.request('classified')"))
  if data.get('telemetry') and data['telemetry'].get('tick',-1)>=1 and data['telemetry']['rooms']:break
  p.wait_for_timeout(100)
 assert data.get('telemetry',{}).get('rooms'),data
 p.set_viewport_size({'width':1440,'height':1000});p.locator('#icarus-menu [data-page="settings"]').click();p.locator('#page-settings [data-subtab="general"]').click();p.locator('.classified-terminal summary').click();p.locator('.classified-unlock').click();p.wait_for_function('document.querySelector(".classified-status").textContent.includes("CLASSIFIED HOST CONNECTED")')
 for room in ['COV-A05','COV-A06']:
  p.locator('.classified-camera').select_option(room);p.wait_for_function('r=>document.querySelector(".classified-camera").value===r',arg=room);p.locator('.classified-terminal canvas').scroll_into_view_if_needed();p.locator('.classified-terminal canvas').screenshot(path=str(a.output/(room+'.png')))
 data=p.evaluate("ICARUSHost.request('classified')");(a.output/'restricted_sources.json').write_text(json.dumps({'label':'Actual localhost restricted non-explicit procedural sensors in isolated test voyage. No ordinary public/private camera policy change; not recorded footage.','telemetry':data},indent=2))
finally:t.tearDown();T.tearDownClass()
