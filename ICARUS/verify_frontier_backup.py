"""Exercise normal backup-file UI with a real campaign artifact, then resume it."""
import argparse, functools, http.server, json, os, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('backup',type=Path);ap.add_argument('--report',type=Path,default=Path('backup_roundtrip.json'));args=ap.parse_args();report={'passed':False,'errors':[],'backup':args.backup.name}
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*a):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'web')));threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        raw=json.loads(args.backup.read_text())['state']
        with sync_playwright() as pw:
            b=pw.chromium.launch(headless=True,executable_path=os.environ.get('ICARUS_CHROMIUM') or None);ctx=b.new_context();p=ctx.new_page();p.goto(f'http://127.0.0.1:{server.server_port}/icarus.html?icarus_soak=1');p.wait_for_function('!!window.__icarusSoak');p.on('dialog',lambda d:d.accept());p.locator('#backupfile').set_input_files(str(args.backup));p.wait_for_function('(tick)=>window.__icarusSoak.snapshot().tick===tick',arg=raw['tick']);snap=p.evaluate('window.__icarusSoak.snapshot()')
            keys=['clock','crew','universe','navigation','logistics','frontier','economy','entropy','living','specimenCustody'];report['mismatched_import_domains']=[k for k in keys if snap[k]!=raw[k]];assert not report['mismatched_import_domains'],report['mismatched_import_domains'];assert snap['director']['science']==raw['remoteCore']['director']['science'];assert snap['resourceAudit']==[];assert snap['frontierAudit']==[]
            assert p.evaluate('window.__icarusSoak.save()');p.reload();after=p.evaluate('window.__icarusSoak.snapshot()');assert snap==after
            p.evaluate('window.__icarusSoak.advance(120)');final=p.evaluate('window.__icarusSoak.snapshot()');assert final['tick']==raw['tick']+120;assert final['resourceAudit']==[];assert final['frontierAudit']==[];report.update(passed=True,imported_tick=raw['tick'],resumed_tick=final['tick'],storage=p.evaluate('ICARUSSaveStore.stats()'));b.close()
    except Exception as e:report['errors'].append(str(e))
    finally:server.shutdown();server.server_close();args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2));return not report['passed']
if __name__=='__main__':raise SystemExit(main())
