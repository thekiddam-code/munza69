"""Explicit policy/adverse fixtures; these are NOT natural-voyage acceptance runs."""
import argparse,collections,functools,http.server,json,os,threading,time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
SCENARIOS=[('fuel_shortage',6067,"const fuel=s.economy.feedstock.fuel;s.economy.feedstock.fuel=0;s.economy.feedstockUsed.fuel=(s.economy.feedstockUsed.fuel||0)+fuel;const source='explicit adverse initial fuel depletion';s.economy.ledger=s.economy.ledger||{};s.economy.ledger[JSON.stringify(['feedstock_use','fuel',source])]={kind:'feedstock_use',key:'fuel',source,amount:fuel,count:1,first:0,last:0};"),('high_contact_density',3037,"s.entities.density=1;"),('low_contact_density',4049,"s.entities.density=0;"),('zero_discovery_hold',5051,"s.remoteCore.autonomyEnabled=false;s.navigation.hold=true;")]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--days',type=int,default=14);ap.add_argument('--report',type=Path,default=Path('living_adverse_results.json'));args=ap.parse_args();report={'passed':True,'classification':'explicit synthetic initial conditions and policy variants','scenarios':[]}
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'web')));threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as pw:
            b=pw.chromium.launch(headless=True,executable_path=os.environ.get('ICARUS_CHROMIUM') or None)
            for name,seed,code in SCENARIOS:
                row={'scenario':name,'seed':seed,'days':args.days,'passed':False,'errors':[],'injected_initial_conditions':code,'daily':[]};started=time.monotonic();ctx=b.new_context();ctx.add_init_script('window.__icarusSeed='+str(seed));p=ctx.new_page();js_errors=[];p.on('pageerror',lambda e:js_errors.append(str(e)))
                try:
                    url=f'http://127.0.0.1:{server.server_port}/icarus.html?icarus_soak=1';p.goto(url);p.wait_for_function('!!window.__icarusSoak');assert p.evaluate('window.__icarusSoak.save()');codec=(ROOT/'web/vendor/lz-string.min.js').read_text()+';'+(ROOT/'web/save-store.js').read_text();p.add_init_script(codec+';(()=>{if(sessionStorage.getItem("adverse"))return;sessionStorage.setItem("adverse","1");const s=JSON.parse(localStorage.getItem("icarus-v02"));'+code+';localStorage.setItem("icarus-v02",JSON.stringify(s));})();');p.reload();p.wait_for_function('!!window.__icarusSoak')
                    for day in range(1,args.days+1):
                        for _ in range(12):p.evaluate('window.__icarusSoak.advance(120)')
                        r=p.evaluate('''()=>{const s=window.__icarusSoak.snapshot();return {tick:s.tick,crew:s.crew.length,deceased:s.living.deceased.length,arrivals:s.navigation.arrivals,fuel:s.economy.feedstock.fuel,resource_errors:s.resourceAudit,domain_errors:s.frontierAudit,cases:s.director.science.cases.length,entities:Object.keys(s.entities.registry).length,contacts:s.entities.stats,memories:s.experiences.records.length,emergencies:s.emergencyOps.stats};}''');row['daily'].append(r)
                        if r['tick']!=day*1440 or r['crew']+r['deceased']!=20 or r['resource_errors'] or r['domain_errors'] or r['fuel']<0:row['errors'].append({'day':day,'state':r})
                    before=p.evaluate('window.__icarusSoak.snapshot()');assert p.evaluate('window.__icarusSoak.save()');p.reload();p.wait_for_function('!!window.__icarusSoak');assert before==p.evaluate('window.__icarusSoak.snapshot()')
                    if name=='fuel_shortage':assert row['daily'][-1]['arrivals']==0
                    if name=='zero_discovery_hold':assert row['daily'][-1]['cases']==0
                    row['javascript_errors']=js_errors;row['durable']=p.evaluate('ICARUSDurable.status');row['passed']=not row['errors'] and not js_errors
                except Exception as e:row['errors'].append(str(e))
                finally:ctx.close();row['seconds']=time.monotonic()-started;report['scenarios'].append(row);report['passed']=report['passed'] and row['passed'];print(name,'PASS' if row['passed'] else 'FAIL',flush=True)
            b.close()
    finally:server.shutdown();args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2))
    return not report['passed']
if __name__=='__main__':raise SystemExit(main())
