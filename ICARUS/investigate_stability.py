"""Replay an actual build with read-only instrumentation and retain fine-grained cascade evidence."""
import argparse,functools,http.server,json,os,threading,time,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
from replay_server import handler
ROOT=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--web-root',type=Path,default=ROOT/'web');ap.add_argument('--output',type=Path,required=True);ap.add_argument('--seed',type=int,default=1001);ap.add_argument('--original-checkpoints',action='store_true');ap.add_argument('--days',type=int,default=365);ap.add_argument('--detail-from',type=int,default=320);args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler(args.web_root));threading.Thread(target=server.serve_forever,daemon=True).start();report={'seed':args.seed,'days':args.days,'status':'starting','completed':False,'errors':[],'daily':[]};started=time.monotonic()
    try:
        with sync_playwright() as w:
            b=w.chromium.launch(executable_path=os.environ.get('ICARUS_CHROMIUM') or None);ctx=b.new_context();ctx.add_init_script(((args.web_root/'vendor/lz-string.min.js').read_text()+';'+(args.web_root/'save-store.js').read_text()+';' if args.original_checkpoints else '')+'window.__icarusSeed='+str(args.seed));p=ctx.new_page();p.set_default_timeout(120000);p.on('pageerror',lambda e:report['errors'].append(str(e)));p.goto(f'http://127.0.0.1:{server.server_port}/icarus.html?icarus_soak=1');p.wait_for_function('!!window.__icarusSoak');report['status']='running'
            with (args.output/'detail.jsonl').open('w') as f:
                for day in range(1,args.days+1):
                    if day>=args.detail_from:
                        for block in range(48):
                            row=p.evaluate('()=>{__icarusSoak.advance(30);return __icarusSoak.stability()}');f.write(json.dumps(row)+'\n')
                    else:p.evaluate('()=>{for(let n=0;n<12;n++)__icarusSoak.advance(120)}')
                    d=p.evaluate('__icarusSoak.daily()');report['daily'].append(d);report['last_day']=day
                    if d['resource_errors'] or d['frontier_errors']:report['errors'].append({'day':day,'resource':d['resource_errors'],'frontier':d['frontier_errors']})
                    if day in [300,320,330,335,338,339,340,341,342,343,344,345,346,347,args.days]:
                        p.evaluate('__icarusSoak.save()');raw=p.evaluate("localStorage.getItem('icarus-v02')");(args.output/f'state_day_{day}.json').write_text(raw)
                    if args.original_checkpoints and day in (30,90):
                        before=p.evaluate('JSON.stringify(__icarusSoak.snapshot())');p.evaluate('__icarusSoak.save()');p.reload();p.wait_for_function('!!window.__icarusSoak');after=p.evaluate('JSON.stringify(__icarusSoak.snapshot())');assert before==after,'Original checkpoint world changed on reload';report.setdefault('reloads',[]).append({'day':day,'status':p.evaluate('ICARUSDurable.status')})
                    if day%30==0 or day>=330:print('Replay day',day,'living',len(d['crew']),'energy',d['stores']['energy'],flush=True)
                    (args.output/'progress.json').write_text(json.dumps({'last_day':day,'errors':report['errors']}))
            p.evaluate('__icarusSoak.save()');history=p.evaluate('ICARUSDurable.history().then(x=>JSON.stringify(x))');(args.output/'history.json').write_text(history);report['completed']=True;report['status']='finished';b.close()
    except Exception as e:report['errors'].append(str(e));report['traceback']=traceback.format_exc();report['status']='failed'
    finally:server.shutdown();report['seconds']=time.monotonic()-started;(args.output/'reproduction.json').write_text(json.dumps(report,indent=2))
    return not report['completed'] or bool(report['errors'])
if __name__=='__main__':raise SystemExit(main())
