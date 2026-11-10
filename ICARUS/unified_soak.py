"""Real-wall-calendar accelerated campaign: hourly real intervals, actual production simulation steps."""
import argparse,functools,http.server,json,os,threading,time,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=1001);ap.add_argument('--days',type=int,default=30);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    r={'seed':args.seed,'real_days':args.days,'start':'2026-10-28T00:00:00Z','zone':'America/Chicago','status':'running','passed':False,'errors':[],'daily':[],'checkpoints':[],'initialization':'Fixed seed and explicit wall clock. Simulation uses production step+field controllers; per-step autosave disabled in deterministic test driver; save/reload checked explicitly.'};start=time.monotonic();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'web')));threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as pw:
            b=pw.chromium.launch(executable_path=os.environ.get('ICARUS_CHROMIUM') or None);c=b.new_context();c.add_init_script('window.__icarusSeed='+str(args.seed));p=c.new_page();p.set_default_timeout(120000);p.on('pageerror',lambda e:r['errors'].append(str(e)));p.goto(f'http://127.0.0.1:{server.server_port}/icarus.html?icarus_soak=1');p.wait_for_function('!!window.__icarusSoak');t=p.evaluate('()=>{const t=Date.parse("2026-10-28T00:00Z");__icarusSoak.realStart(t,"America/Chicago");return t;}')
            for day in range(1,args.days+1):
                for hour in range(1,25):p.evaluate('t=>__icarusSoak.realAdvance(t)',t+((day-1)*24+hour)*3600000)
                row=p.evaluate('__icarusSoak.daily()');cal=p.evaluate('__icarusSoak.snapshot().calendar');row['calendar']=cal;r['daily'].append(row)
                if row['resource_errors'] or row['frontier_errors'] or row['chronicle_errors']:r['errors'].append('World audit failed day '+str(day))
                if len(row['crew'])+len(row['dead'])!=20:r['errors'].append('Crew identity count failed')
                if cal['recovery']['discardedMs'] or cal['recovery']['rollbackCount']:r['errors'].append('Uninterrupted campaign lost or rolled back wall time')
                p.evaluate('__icarusSoak.save()')
                if day in {7,30,args.days}:
                    before=p.evaluate('JSON.stringify(__icarusSoak.snapshot())');history=p.evaluate('ICARUSDurable.history().then(x=>JSON.stringify(x))');p.reload();p.wait_for_function('!!window.__icarusSoak');after=p.evaluate('JSON.stringify(__icarusSoak.snapshot())');same=before==after
                    if not same:r['errors'].append('Exact checkpoint reload mismatch day '+str(day))
                    snapshot=json.loads(after);r['checkpoints'].append({'real_day':day,'sim_days':row['tick']/1440,'episode':row['episode'],'exact_reload':same,'crew':len(row['crew']),'dead':len(row['dead']),'stories':row['anthology']['arcs'],'resources':row['stores'],'arrivals':row['arrivals'],'calendar_occurrences':list(cal['occurrences']),'organisms':snapshot['unifiedWorld']['organisms']})
                    raw=p.evaluate('localStorage.getItem("icarus-v02")')
                    (args.output/f'backup_{args.seed}_{day}.json').write_text('{"format":"ICARUS_SAVE","formatVersion":1,"appVersion":"1.5.0-phase1","state":'+raw+',"history":'+history+',"ideas":[]}')
                    # Save actual full in-memory snapshot and source history for independent audit, without pretending it is the serialized world envelope.
                    (args.output/f'snapshot_{args.seed}_{day}.json').write_text(after);(args.output/f'history_{args.seed}_{day}.json').write_text(history)
                (args.output/f'campaign_{args.seed}.json').write_text(json.dumps(r,indent=2));print(args.seed,'real day',day,'sim day',round(row['tick']/1440,3),'crew',len(row['crew']),'errors',r['errors'],flush=True)
                if r['errors']:break
            r['passed']=not r['errors'] and len(r['daily'])==args.days;r['status']='finished';b.close()
    except Exception as e:r['errors'].append(str(e));r['traceback']=traceback.format_exc();r['status']='failed'
    finally:server.shutdown();r['elapsed_seconds']=time.monotonic()-start;(args.output/f'campaign_{args.seed}.json').write_text(json.dumps(r,indent=2))
    return not r['passed']
if __name__=='__main__':raise SystemExit(main())
