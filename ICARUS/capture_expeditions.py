"""Technical visual example from actual source-backed expedition; not original recorded video."""
import argparse,json,os
from pathlib import Path
import test_expedition_integration as M

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 import sys
 for m in list(sys.modules.values()):
  if getattr(m,'__name__','').startswith('test_') and hasattr(m,'ROOT'):m.ROOT=a.runtime
 T=M.ExpeditionIntegration;T.setUpClass();t=T();t.setUp();saved=[]
 try:
  p=t.page();t.start_field(p)
  for i in range(1000):
   t.advance(p,1);s=t.snap(p);m=s['missions']['asteroid']
   if m and m['ops44']['stage']=='field':
    views=p.evaluate('__icarusSoak.observation().rooms.filter(r=>r.kind==="field"&&r.available)')
    if views:
     v=views[0];kind=v['terrain']['kind']
     if kind not in saved:
      t.operations(p);p.locator('.obs-follow').select_option(m['crew']);p.locator('#camera-scene').scroll_into_view_if_needed();p.locator('#camera-scene').screenshot(path=str(a.output/(kind+'.png')));(a.output/(kind+'.json')).write_text(json.dumps({'label':'Technical deterministic controller example; legitimate request, actual elapsed controller steps, no injected discoveries/creatures, reconstruction not video','source_commit':json.loads((a.runtime/'BUILD_MANIFEST.json').read_text())['source_commit'],'camera':v},indent=2));saved.append(kind)
   if len(saved)==3:break
   if s['expeditionOperations']['history'] and not m:
    t.deck(p,'missions','active');p.locator('.field-request').click()
  assert {'surface','industrial','cavern'}.issubset(saved),saved
 finally:t.tearDown();T.tearDownClass()
if __name__=='__main__':main()
