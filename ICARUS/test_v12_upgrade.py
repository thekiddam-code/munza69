"""Upgrade a save produced by the real v1.2 engine in the same browser origin."""
import argparse, functools, http.server, json, os, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--baseline',type=Path,required=True);ap.add_argument('--report',type=Path,default=Path('upgrade_results.json'));args=ap.parse_args();active=[args.baseline/'web'];report={'passed':False,'errors':[],'baseline':str(args.baseline),'simulation_minutes_before_upgrade':720}
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(active[0]),**kw)
        def log_message(self,*a):pass
        def end_headers(self):self.send_header('Cache-Control','no-store');super().end_headers()
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as pw:
            b=pw.chromium.launch(headless=True,executable_path=os.environ.get('ICARUS_CHROMIUM') or None);ctx=b.new_context();ctx.add_init_script('window.__icarusSeed=1001;');p=ctx.new_page();url=f'http://127.0.0.1:{server.server_port}/icarus.html?icarus_soak=1';p.goto(url);p.wait_for_function('!!window.__icarusSoak')
            for _ in range(6):p.evaluate('window.__icarusSoak.advance(120)')
            before=p.evaluate('window.__icarusSoak.snapshot()');assert p.evaluate('window.__icarusSoak.save()');raw=p.evaluate("localStorage.getItem('icarus-v02')");report['legacy_save_bytes']=len(raw.encode());p.close();active[0]=ROOT/'web';p=ctx.new_page();p.goto(url+'&upgrade=1');p.wait_for_function('!!window.__icarusSoak');after=p.evaluate('window.__icarusSoak.snapshot()')
            def retained(old,new):
                if isinstance(old,dict):return all(k in new and retained(v,new[k]) for k,v in old.items())
                if isinstance(old,list):return len(old)==len(new) and all(retained(a,b) for a,b in zip(old,new))
                return old==new
            domains=['clock','crew','archived','specimenCustody','living','entropy','chronicle','operations','world','director','missions','economy']
            report['changed_legacy_domains']=[k for k in domains if not retained(before[k],after[k])];assert not report['changed_legacy_domains'],report['changed_legacy_domains'];assert after['navigation']['current']=='HOME';assert after['tick']==before['tick'];assert after['frontierAudit']==[];assert after['resourceAudit']==[]
            report['crew']=len(after['crew']);report['science_cases']=len(after['director']['science']['cases']);report['active_legacy_missions']=[k for k,m in after['missions'].items() if m];report['initialized_destinations']=sum(len(s['bodies']) for s in after['universe']['systems'].values())
            for _ in range(6):p.evaluate('window.__icarusSoak.advance(120)')
            final=p.evaluate('window.__icarusSoak.snapshot()');assert final['tick']==before['tick']+720;assert final['resourceAudit']==[];assert final['frontierAudit']==[];assert p.evaluate('window.__icarusSoak.save()');p.reload();p.wait_for_function('!!window.__icarusSoak');assert final==p.evaluate('window.__icarusSoak.snapshot()');report['passed']=True;b.close()
    except Exception as e:report['errors'].append(str(e))
    finally:server.shutdown();server.server_close();args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2));return not report['passed']
if __name__=='__main__':raise SystemExit(main())
