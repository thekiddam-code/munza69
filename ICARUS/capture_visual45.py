"""Live camera comparisons in identical isolated technical fixtures, never original recorded footage."""
import argparse,json,sys
from pathlib import Path
import test_expedition_integration as M

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 for m in list(sys.modules.values()):
  if getattr(m,'__name__','').startswith('test_') and hasattr(m,'ROOT'):m.ROOT=a.runtime.resolve()
 T=M.ExpeditionIntegration;T.setUpClass();t=T();t.setUp()
 try:
  pass # Each comparison gets an independent one-use fixture context.
  cases=[('lounge','A09','Taking a recreation break',False),('observation','A03','Watching the stars',False),('engineering','C07','Inspecting distribution circuits',False),('medical','A08','Checking medical supplies',False),('science','B01','Reviewing research',False),('bridge','A01','Reviewing ship operations',False),('cargo','C03','Checking manifests',False),('security','B07','Monitoring surveillance',False),('corridor','COR-B-0','Walking',False),('character','A09','Standing by',False),('wheelchair','A09','Taking a recreation break',True),('wheelchair-moving','A09','Taking a recreation break',True),('wheelchair-turning','A09','Taking a recreation break',True),('seated','A09','Taking a recreation break',False)]
  for label,room,task,chair in cases:
   p=t.page();p.set_viewport_size({'width':1440,'height':1000});t.configure(p,"s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;const p=s.crew[0];p.room=p.target="+json.dumps(room if len(room)==3 else 'B01')+";p.nav=null;p.route=[];p.task=p.goal="+json.dumps(task)+";p.interaction='working';p.taskMinutes=999;p.body={...(p.body||{}),build:'medium',locomotion:"+json.dumps('wheelchair' if chair else 'walk')+"};")
   if label in ('wheelchair-moving','wheelchair-turning','seated'):
    if not p.evaluate('typeof ICARUSRoomInteractions!=="undefined"'):continue
    if label=='wheelchair-turning':t.change(p,"s.crew[0].roomPlacement={room:'A09',x:320,y:195};")
    t.advance(p,11 if label=='seated' else 1)
   t.operations(p);p.locator('.obs-select').select_option(room);p.wait_for_function('id=>ICARUSObservationLive.camera.selected===id',arg=room);p.locator('#camera-scene').scroll_into_view_if_needed();p.evaluate('ICARUSObservationLive.camera.draw(true)');p.locator('#camera-scene').screenshot(path=str(a.output/(label+'.png')));view=p.evaluate('id=>__icarusSoak.observation().rooms.find(r=>r.id===id)',room);
   if chair:assert any(q['body']['locomotion']=='wheelchair' for q in view['actors'])
   (a.output/(label+'.json')).write_text(json.dumps({'source_commit':json.loads((a.runtime/'BUILD_MANIFEST.json').read_text()).get('source_commit') if (a.runtime/'BUILD_MANIFEST.json').exists() else None,'label':'Actual active camera; isolated technical placement fixture, not natural event/video','viewport':[1440,1000],'canvas':[384,216],'camera':view},indent=2))
  print('Captured live camera comparisons',len(cases),flush=True)
 finally:t.tearDown();T.tearDownClass()
if __name__=='__main__':main()
