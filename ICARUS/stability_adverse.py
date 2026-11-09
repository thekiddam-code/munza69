"""Explicit adverse initial worlds, including legitimate unrecoverable mortality."""
import argparse,functools,http.server,json,os,threading,time,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
SCENARIOS={
 'funded_black_start':"s.equipment.C07.condition=0;ICARUSEconomy.consume(s,'energy',ICARUSEconomy.available(s).energy,'explicit initial blackout');s.power=0;",
 'unfunded_sealed_life_support':"for(const id of ['C07','C09']){s.equipment[id].condition=0;s.physicalWorld.rooms[id].door='sealed';}for(const k of ['tools','spares','energy'])ICARUSEconomy.consume(s,k,ICARUSEconomy.available(s)[k],'explicit adverse depletion');ICARUSEconomy.burnFeed(s,'ore',s.economy.feedstock.ore,'explicit initial ore depletion');s.power=0;",
 'injured_repair_crew':"for(const p of s.crew.filter(p=>p.job==='Engineer').slice(0,2)){p.vitals.health=45;p.vitals.injuries.push({cause:'explicit initial injury',at:0,active:true});p.room='A08';p.target='A08';p.route=[];}for(const p of s.crew.filter(p=>p.job==='Medic')){p.room='A08';p.target='A08';p.route=[];}s.equipment.C07.condition=36;s.equipment.C09.condition=42;",
 'unsafe_pressure_and_jam':"s.equipment.C07.condition=0;s.physicalWorld.rooms.C07.door='jammed';Object.assign(s.physicalWorld.rooms.C07.atmosphere,{pressure:0,oxygen:0,fire:true,breach:true,temperature:100,smoke:90});ICARUSEconomy.consume(s,'energy',ICARUSEconomy.available(s).energy,'explicit initial energy depletion');s.power=0;"
}
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path,required=True);args=ap.parse_args();report={'classification':'Explicit adverse initial conditions; not natural campaign events','passed':False,'scenarios':[]};server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'web')));threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as w:
            b=w.chromium.launch(executable_path=os.environ.get('ICARUS_CHROMIUM') or None)
            for name,code in SCENARIOS.items():
                d={'name':name,'seed':1001,'initial_conditions':code,'days':9,'errors':[],'daily':[]};c=b.new_context();c.add_init_script('window.__icarusSeed=1001');p=c.new_page();p.set_default_timeout(120000);p.on('pageerror',lambda e:d['errors'].append(str(e)));p.goto(f'http://127.0.0.1:{server.server_port}/icarus.html?icarus_soak=1');p.wait_for_function('!!window.__icarusSoak');p.evaluate('__icarusSoak.save()');fixture=p.evaluate("code=>{const s=JSON.parse(localStorage.getItem('icarus-v02'));new Function('s',code)(s);return JSON.stringify(s);}",code);p.add_init_script("(()=>{if(sessionStorage.getItem('adverse-applied'))return;sessionStorage.setItem('adverse-applied','1');localStorage.setItem('icarus-anthology-v14',"+json.dumps(fixture)+");})();");p.reload();p.wait_for_function('!!window.__icarusSoak');actual=json.loads(p.evaluate('JSON.stringify(__icarusSoak.snapshot())'));expected=json.loads(fixture);assert actual['economy']==expected['economy'],'Adverse inventory was overwritten before startup';assert actual['world']['equipment']==expected['equipment'],'Adverse hardware was overwritten';d['initial_conditions_verified']=True
                for day in range(1,10):
                    p.evaluate('()=>{for(let i=0;i<12;i++)__icarusSoak.advance(120)}');row=p.evaluate('__icarusSoak.daily()');d['daily'].append(row)
                    if row['resource_errors'] or row['frontier_errors'] or len(row['crew'])+len(row['dead'])!=20:d['errors'].append('World/conservation/identity error at day '+str(day))
                final=p.evaluate('__icarusSoak.stability()');d['final']=final;p.evaluate('__icarusSoak.save()');before=p.evaluate('JSON.stringify(__icarusSoak.snapshot())');p.reload();p.wait_for_function('!!window.__icarusSoak');d['exact_reload']=before==p.evaluate('JSON.stringify(__icarusSoak.snapshot())')
                if not d['exact_reload']:d['errors'].append('Emergency/death persistence mismatch')
                if name=='funded_black_start' and not(final.get('repairControl',{}).get('stats',{}).get('emergencyCompleted') and final['equipment']['C07']['condition']>40 and len(final['crew'])==20):d['errors'].append('Funded physical cold restart was not demonstrated')
                if name=='unfunded_sealed_life_support' and (len(final['crew']) or len(final['dead'])!=20 or any(v.get('progress',0)>0 for v in final['emergencies'].values())):d['errors'].append('Unfunded inaccessible catastrophe was incorrectly rescued')
                d['passed']=not d['errors'];report['scenarios'].append(d);c.close();print(name,'PASS' if d['passed'] else 'FAIL','survivors',len(final['crew']),flush=True)
            b.close();report['passed']=all(x['passed'] for x in report['scenarios']) and len(report['scenarios'])==4
    except Exception as e:report['error']=str(e);report['traceback']=traceback.format_exc()
    finally:server.shutdown();args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2))
    return not report['passed']
if __name__=='__main__':raise SystemExit(main())
