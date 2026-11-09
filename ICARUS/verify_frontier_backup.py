"""Exercise normal backup-file UI with a real campaign artifact, then resume it."""
import argparse, functools, http.server, json, os, threading,time,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('backup',type=Path);ap.add_argument('--report',type=Path,default=Path('backup_roundtrip.json'));args=ap.parse_args();report={'passed':False,'errors':[],'backup':args.backup.name,'stage':'starting','timeout_seconds':120};started=time.monotonic()
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*a):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'web')));threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        backup=json.loads(args.backup.read_text());raw=backup['state'];expected_history_ids={r['id'] for r in backup.get('history',[])};del backup
        with sync_playwright() as pw:
            b=pw.chromium.launch(headless=True,executable_path=os.environ.get('ICARUS_CHROMIUM') or None);ctx=b.new_context();p=ctx.new_page();p.set_default_timeout(120000);p.set_default_navigation_timeout(120000);report['stage']='startup';p.goto(f'http://127.0.0.1:{server.server_port}/icarus.html?icarus_soak=1');p.wait_for_function('!!window.__icarusSoak');p.on('dialog',lambda d:d.accept());report['stage']='import';import_started=time.monotonic();p.locator('#backupfile').set_input_files(str(args.backup));p.wait_for_function('(tick)=>window.__icarusSoak.time()===tick',arg=raw['tick']);snap=json.loads(p.evaluate('JSON.stringify(window.__icarusSoak.snapshot())'))
            report['import_seconds']=time.monotonic()-import_started;report['stage']='source_and_history_validation';keys=['entities','experiences','emergencyOps','chronicles','clock','crew','universe','navigation','logistics','frontier','economy','entropy','living','specimenCustody'];keys+=[k for k in ['anthology','repairControl'] if k in raw];report['mismatched_import_domains']=[k for k in keys if snap[k]!=raw[k]];assert not report['mismatched_import_domains'],report['mismatched_import_domains'];assert snap['director']['science']==raw['remoteCore']['director']['science'];assert snap['resourceAudit']==[];assert snap['frontierAudit']==[];history_ids=json.loads(p.evaluate('ICARUSDurable.history().then(rows=>JSON.stringify(rows.map(r=>r.id)))'));assert expected_history_ids<=set(history_ids);report['imported_history_records']=len(history_ids)
            report['stage']='durable_save_and_reload';assert p.evaluate('window.__icarusSoak.save()');reload_started=time.monotonic();p.reload();p.wait_for_function('!!window.__icarusSoak');after=json.loads(p.evaluate('JSON.stringify(window.__icarusSoak.snapshot())'));assert snap==after;report['reload_seconds']=time.monotonic()-reload_started
            p.evaluate('window.__icarusSoak.advance(120)');final=json.loads(p.evaluate('JSON.stringify(window.__icarusSoak.snapshot())'));assert final['tick']==raw['tick']+120;assert final['resourceAudit']==[];assert final['frontierAudit']==[];report.update(stage='finished',passed=True,imported_tick=raw['tick'],resumed_tick=final['tick'],storage=p.evaluate('ICARUSSaveStore.stats()'));b.close()
    except Exception as e:report['errors'].append(str(e));report['traceback']=traceback.format_exc()
    finally:server.shutdown();server.server_close();args.report.parent.mkdir(parents=True,exist_ok=True);report['elapsed_seconds']=time.monotonic()-started;args.report.write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2));return not report['passed']
if __name__=='__main__':raise SystemExit(main())
