"""Actual canvas CPU cost and view purity; not physical-device GPU/FPS certification."""
import argparse,json,os
from pathlib import Path
import test_integration
from test_observation_integration import ObservationIntegration

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();test_integration.ROOT=a.runtime;T=ObservationIntegration;T.setUpClass();t=T();t.setUp()
 try:
  p=t.page();t.advance(p,120);before=t.snap(p);r=p.evaluate('''()=>{const rooms=__icarusSoak.observation().rooms.filter(r=>r.available).sort((a,b)=>b.actors.length-a.actors.length),canvases=Array.from({length:5},()=>document.createElement('canvas')),n=240,heapBefore=performance.memory?.usedJSHeapSize??null,start=performance.now();for(let i=0;i<n;i++)ICARUSPixelCamera.draw(canvases[0],rooms[0],{time:i*66});const mainMs=performance.now()-start,previewStart=performance.now();for(let i=0;i<n;i++)for(let j=1;j<5;j++)ICARUSPixelCamera.draw(canvases[j],rooms[j%rooms.length],{time:i*250});const previewsMs=performance.now()-previewStart;return {mainFrames:n,previewFrames:n*4,mainTotalMs:mainMs,mainMeanMs:mainMs/n,fourPreviewsMeanMs:previewsMs/n,heapBefore,heapAfter:performance.memory?.usedJSHeapSize??null,pixelMetrics:{...ICARUSPixelCamera.metrics},actualActors:rooms.slice(0,5).map(r=>({room:r.id,count:r.actors.length})),logicalResolution:[384,216],worldTick:__icarusSoak.time()};}''');assert t.snap(p)==before;r.update(passed=not t.errors,runtime=str(a.runtime),world_unchanged=True,limit='Synchronous Canvas CPU microbenchmark under Linux headless Chromium. No GPU, physical Samsung or real-network performance certification.');a.output.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
 finally:t.tearDown();T.tearDownClass()
if __name__=='__main__':main()
