"""Isolated imported-voyage production-pump benchmark; never edits the input backup.
Requires Playwright and a Chromium executable (ICARUS_CHROMIUM). Pass the same
backup, horizon, ticks and seed to original/fixed runtime trees. Aggregate results
contain state hashes, not raw voyage state. CPU sampling adds measurement overhead.
"""
import sys,os,json,time,argparse,hashlib,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import test_umbra_browser as H
ap=argparse.ArgumentParser();ap.add_argument('--runtime',type=Path,required=True);ap.add_argument('--backup',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--ticks',type=int,default=30);ap.add_argument('--horizon-seconds',type=int,default=16000);ap.add_argument('--profile',action='store_true');ap.add_argument('--drain',action='store_true');a=ap.parse_args();a.output.parent.mkdir(exist_ok=True,parents=True)
backup=a.backup.resolve();original=json.loads(backup.read_text());anchor=original['state']['calendar']['wallCursor'];H.ROOT=a.runtime.resolve();H.UmbraBrowser.setUpClass();t=H.UmbraBrowser();t.setUp();report={'runtime':str(a.runtime),'input_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'input_tick':original['state']['tick'],'requested_ticks':a.ticks,'catchup_wall_seconds':a.horizon_seconds,'instrumentation':'Read-only counters, CDP sampling and explicit fixed-work stop on isolated imported copy; actual production pump/step/save/telemetry/UI. Date horizon is fixed, performance timer and writer protections are real.'}
try:
 c=t.browser.new_context(viewport={'width':1280,'height':800});t.contexts.append(c)
 c.add_init_script('''(()=>{const ActualDate=Date;window.__benchNow='''+str(anchor)+''';window.Date=class extends ActualDate{constructor(...args){super(...(args.length?args:[window.__benchNow]));}static now(){return window.__benchNow;}};window.__icarusSeed=10101;const perf={active:false,finished:false,groups:{},windows:[],publish:[]};perf.measure=(name,fn)=>{const t=performance.now();try{return fn();}finally{const d=performance.now()-t,g=perf.groups[name]||(perf.groups[name]={calls:0,ms:0,max_ms:0});g.calls++;g.ms+=d;g.max_ms=Math.max(g.max_ms,d);}};window.__bench=perf;})();''')
 html=(a.runtime/'web/icarus.html').read_text()
 html=html.replace("if(new URLSearchParams(location.search).get('icarus_soak')==='1'){", "if(new URLSearchParams(location.search).has('icarus_soak')||new URLSearchParams(location.search).has('icarus_benchmark')){")
 html=html.replace("if(__icarusSoakMode||!canWriteWorld()", "if((__icarusSoakMode&&!window.__bench.active)||!canWriteWorld()")
 # Expose diagnostics only in this intercepted benchmark document; no save or runtime file is modified.
 hook="""benchmarkRaw:()=>JSON.stringify(state),benchmarkStatus:()=>({tick:state.tick,paused,calendar:state.calendar,writer:canWriteWorld(),bridge:document.querySelector('#rd-bridge-status').textContent}),benchmarkStart:(target)=>{window.__benchNow=target;window.__bench.active=true;window.__bench.targetTick=state.tick+window.__bench.work;window.__bench.started=performance.now();paused=false;pumpRealTime(target);},"""
 html=html.replace('window.__icarusSoak={','window.__icarusSoak={'+hook)
 # Time core functions without changing their implementation or return values.
 wrap="""const measured=(name,fn)=>(...args)=>window.__bench.active?window.__bench.measure(name,()=>fn(...args)):fn(...args);for(const pair of [['step',step],['field',fieldTick],['save',save],['render',render],['renderUnifiedClock',renderUnifiedClock]]){const [n,f]=pair;if(n==='step')step=measured(n,f);else if(n==='field')fieldTick=measured(n,f);else if(n==='save')save=measured(n,f);else if(n==='render')render=measured(n,f);else renderUnifiedClock=measured(n,f);}for(const [key,methods] of Object.entries({ICARUSForwardOps:['tick','work','job'],ICARUSDroneEscort:['tick'],ICARUSDroneOps:['tick','work','job','fitTelemetry'],ICARUSExpeditionOps:['tick'],ICARUSKnowledge:['tick'],ICARUSCrewLife:['tick'],ICARUSOperationalView:['project'],ICARUSObservation:['project'],ICARUSClassified:['project']})){const m=window[key];if(m)for(const n of methods)if(typeof m[n]==='function')m[n]=measured(key+'.'+n,m[n]);}const adv=ICARUSCalendar.advance;ICARUSCalendar.advance=(s,now,env,opts)=>{if(window.__bench.finished||window.__bench.aborted)return {ticks:0,backlogMs:Math.max(0,now-s.calendar.wallCursor)};if(!window.__bench.active)return adv(s,now,env,opts);const b=window.__bench;opts={...opts,maxTicks:b.drain?opts.maxTicks:Math.min(opts.maxTicks,b.targetTick-s.tick)};const r=adv(s,now,env,opts);b.windows.push({at:performance.now()-b.started,tick:s.tick,returnedTicks:r.ticks,backlogMs:r.backlogMs});if(b.drain?r.backlogMs===0:s.tick>=b.targetTick){b.finished=true;b.active=false;b.elapsed=performance.now()-b.started;b.finalTick=s.tick;}return r;};"""
 html=html.replace('window.__icarusSoak={',wrap+'window.__icarusSoak={')
 c.route('**/icarus.html?*',lambda route:route.fulfill(status=200,content_type='text/html',body=html))
 p=c.new_page();p.set_default_timeout(180000);report['console_errors']=[];report['page_errors']=[]
 p.on('console',lambda m:report['console_errors'].append(m.text[:400]) if m.type=='error' else None);p.on('pageerror',lambda e:report['page_errors'].append(str(e)))
 p.on('response',lambda r:report.setdefault('publish',[]).append({'status':r.status,'bytes':len((r.request.post_data or '').encode())}) if r.request.method=='POST' and r.url.endswith('/api/icarus/host/publish') else None)
 p.goto(t.url+'/icarus.html?icarus_soak=1');p.wait_for_function('window.__icarusSoak&&ICARUSHost.canWrite()');p.locator('.boot-observe').click();p.on('dialog',lambda d:d.accept());p.locator('#backupfile').set_input_files(str(backup));p.wait_for_function('tick=>__icarusSoak.time()===tick&&!ICARUSBackupUI.busy()',arg=original['state']['tick']);p.evaluate('ICARUSDurable.flush({cache:true})');p.wait_for_timeout(1500)
 initial=json.loads(p.evaluate('__icarusSoak.benchmarkRaw()'));report['before_world_sha256']=hashlib.sha256(json.dumps(initial,sort_keys=True,separators=(',',':')).encode()).hexdigest();report['before']=p.evaluate('__icarusSoak.benchmarkStatus()');p.evaluate('args=>{window.__bench.work=args.work;window.__bench.drain=args.drain;window.__bench.groups={};}',{'work':a.ticks,'drain':a.drain})
 cdp=c.new_cdp_session(p)
 if a.profile:cdp.send('Profiler.enable');cdp.send('Profiler.setSamplingInterval',{'interval':1000});cdp.send('Profiler.start')
 p.evaluate('target=>__icarusSoak.benchmarkStart(target)',anchor+a.horizon_seconds*1000)
 deadline=time.monotonic()+180
 while time.monotonic()<deadline:
  if p.evaluate('__bench.finished'):break
  p.wait_for_timeout(250)
 if not p.evaluate('__bench.finished'):p.evaluate('__bench.aborted=true;__bench.active=false;__bench.elapsed=performance.now()-__bench.started;__bench.finalTick=__icarusSoak.time();')
 report['benchmark']=p.evaluate('({finished:__bench.finished,aborted:!!__bench.aborted,elapsedMs:__bench.elapsed,finalTick:__bench.finalTick,groups:__bench.groups,windows:__bench.windows})');report['after']=p.evaluate('__icarusSoak.benchmarkStatus()');q=time.monotonic();p.evaluate('ICARUSDurable.flush()');report['durable_flush_seconds']=time.monotonic()-q;report['durable_status']=p.evaluate('({...ICARUSDurable.status})');report['runtime_diagnostics']=p.evaluate('window.ICARUSRuntimeDiagnostics?.snapshot()||null');final=json.loads(p.evaluate('__icarusSoak.benchmarkRaw()'));report['after_world_sha256']=hashlib.sha256(json.dumps(final,sort_keys=True,separators=(',',':')).encode()).hexdigest();report['after_domain_hashes']={k:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest() for k,v in final.items()};report['recording_counts']={'records':len(final.get('droneOperations',{}).get('archive',[])),'original_records_preserved':all(any(old==row for row in final.get('droneOperations',{}).get('archive',[])) for old in original['state']['droneOperations']['archive'])}
 if a.profile:
  profile=cdp.send('Profiler.stop')['profile'];nodes={n['id']:n for n in profile['nodes']};totals=collections.Counter()
  for node,dt in zip(profile.get('samples',[]),profile.get('timeDeltas',[])):
   f=nodes[node]['callFrame'];totals[(f['functionName'] or '(anonymous)',f['url'].split('/')[-1].split('?')[0],f['lineNumber'])]+=dt/1000
  report['cpu_self_ms']=[{'function':n,'file':f,'line':line+1,'ms':round(ms,3)} for (n,f,line),ms in totals.most_common(35)]
 elapsed=report['benchmark'].get('elapsedMs');ticks=report['after']['tick']-report['before']['tick'];report['measured_ticks']=ticks
 if elapsed:report.update(simulated_seconds_per_real_second=ticks*60000/elapsed,pending_wall_seconds_per_real_second=(report['after']['calendar']['wallCursor']-report['before']['calendar']['wallCursor'])/elapsed,avg_elapsed_ms_per_tick=elapsed/ticks)
 q=time.monotonic();p.evaluate('ICARUSDurable.flush({cache:true})');report['mirror_flush_seconds']=time.monotonic()-q;report['cache_consistency']=p.evaluate('(()=>{const raw=localStorage.getItem("icarus-v02"),physical=ICARUSSaveStore.encodedGet?ICARUSSaveStore.decode(ICARUSSaveStore.encodedGet("icarus-v02")):raw;return {equal:raw===physical,pending:ICARUSDurable.status.pending,cachePending:ICARUSDurable.status.cachePending||0,cacheWarning:ICARUSDurable.status.cacheWarning||null};})()');report['saved_input_unchanged']=hashlib.sha256(backup.read_bytes()).hexdigest()==report['input_sha256']
 print(json.dumps({k:report[k] for k in ['runtime','measured_ticks','simulated_seconds_per_real_second','pending_wall_seconds_per_real_second','avg_elapsed_ms_per_tick'] if k in report},indent=2))
finally:
 a.output.write_text(json.dumps(report,indent=2));t.tearDown();H.UmbraBrowser.tearDownClass()

if not report.get('benchmark',{}).get('finished'):raise SystemExit('Benchmark did not complete within the 180-second processing ceiling; see partial report.')
