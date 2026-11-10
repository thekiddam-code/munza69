import sys,os,json,threading,http.server,functools,statistics
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=Path(__file__).resolve().parent;ROOT=BASE/'tested/ICARUS_Cinematic_Living_World_Phase3_Lite'
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'web')));threading.Thread(target=server.serve_forever,daemon=True).start();r={}
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium');p=b.new_page(viewport={'width':1280,'height':800});p.goto(f'http://127.0.0.1:{server.server_port}/icarus.html?icarus_soak=1');p.wait_for_function('!!window.__icarusSoak');p.evaluate('__icarusSoak.advance(240)');cdp=p.context.new_cdp_session(p);cdp.send('Performance.enable');r['heap_before']={x['name']:x['value'] for x in cdp.send('Performance.getMetrics')['metrics'] if 'Heap' in x['name']};r.update(p.evaluate('''()=>{const before=JSON.stringify(__icarusSoak.snapshot()),times=[],perf0=__icarusSoak.phase3('render');for(let i=0;i<1000;i++){const t=performance.now();__icarusSoak.phase3('render');times.push(performance.now()-t);}times.sort((a,b)=>a-b);return {samples:1000,mean_ms:times.reduce((a,b)=>a+b,0)/times.length,p95_ms:times[949],max_ms:times.at(-1),before:perf0,after:__icarusSoak.phase3('render'),observer_unchanged:before===JSON.stringify(__icarusSoak.snapshot())};}'''));r['heap_after']={x['name']:x['value'] for x in cdp.send('Performance.getMetrics')['metrics'] if 'Heap' in x['name']};r['limits']='Headless Linux Chromium synchronous camera JS/DOM update timings, not GPU/compositor frame rate or native tablet certification. Heap sampling may include unreclaimed temporary allocations.';assert r['observer_unchanged'];assert r['before']['actorRebuilds']==r['after']['actorRebuilds'];b.close();r['passed']=True
finally:server.shutdown();server.server_close();(BASE/'reports/performance.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
