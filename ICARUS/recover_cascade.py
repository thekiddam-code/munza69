"""Counterfactual: replay an unchanged captured pre-collapse world with old or repaired mechanics."""
import argparse,functools,http.server,json,os,threading,time,traceback,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
from replay_server import handler
ROOT=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--web-root',type=Path,default=ROOT/'web');ap.add_argument('--state',type=Path,required=True);ap.add_argument('--history',type=Path,required=True);ap.add_argument('--days',type=int,default=12);ap.add_argument('--report',type=Path,required=True);args=ap.parse_args();args.report.parent.mkdir(parents=True,exist_ok=True);raw=args.state.read_text();state=json.loads(raw);history=[x for x in json.loads(args.history.read_text()) if x.get('minute',0)<=state['minute']];report={'classification':'Captured-world counterfactual: unchanged inventory, equipment and crew; no synthetic supplies','input_state_sha256':hashlib.sha256(raw.encode()).hexdigest(),'initial_tick':state['tick'],'initial_crew':len(state['crew']),'web_root':str(args.web_root),'passed':False,'errors':[],'daily':[]};start=time.monotonic()
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler(args.web_root));threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as w:
            b=w.chromium.launch(executable_path=os.environ.get('ICARUS_CHROMIUM') or None);c=b.new_context();p=c.new_page();p.set_default_timeout(120000);p.on('pageerror',lambda e:report['errors'].append(str(e)));p.goto(f'http://127.0.0.1:{server.server_port}/icarus.html?icarus_soak=1');p.wait_for_function('!!window.__icarusSoak');p.on('dialog',lambda d:d.accept());payload={'format':'ICARUS_SAVE','formatVersion':1,'appVersion':'1.4','state':state,'history':history,'ideas':[]};input_path=args.report.with_suffix('.input.json');input_path.write_text(json.dumps(payload,separators=(',',':')));p.locator('#backupfile').set_input_files(str(input_path.resolve()));p.wait_for_function('(tick)=>__icarusSoak.time()===tick',arg=state['tick']);p.evaluate('ICARUSDurable.flush()');p.reload();p.wait_for_function('!!window.__icarusSoak');before=json.loads(p.evaluate('()=>{const x=__icarusSoak.snapshot();return JSON.stringify({crew:x.crew,economy:x.economy})}'));assert before['crew']==state['crew'];assert before['economy']==state['economy'];report['unchanged_initial_inventory_and_crew']=True
            for day in range(args.days):
                p.evaluate('()=>{for(let i=0;i<12;i++)__icarusSoak.advance(120)}');d=p.evaluate('__icarusSoak.daily()');report['daily'].append(d);args.report.with_suffix('.progress.json').write_text(json.dumps({'day':day+1,'crew':len(d['crew']),'errors':report['errors']}))
                if d['resource_errors'] or d['frontier_errors']:report['errors'].append({'day':day+1,'resource':d['resource_errors'],'frontier':d['frontier_errors']})
            final=p.evaluate('__icarusSoak.stability()');report['final']=final;report['passed']=not report['errors'];p.evaluate('__icarusSoak.save()');report['after_reload_saved']=p.evaluate('ICARUSDurable.flush()');b.close()
    except Exception as e:report['errors'].append(str(e));report['traceback']=traceback.format_exc()
    finally:server.shutdown();report['seconds']=time.monotonic()-start;args.report.write_text(json.dumps(report,indent=2));print(json.dumps({'passed':report['passed'],'errors':report['errors'],'final_crew':len(report.get('final',{}).get('crew',[]))},indent=2))
    return not report['passed']
if __name__=='__main__':raise SystemExit(main())
