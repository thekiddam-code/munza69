"""Stabilization campaigns with paid repair, forecast, incident and source metrics."""
import argparse, functools, hashlib, http.server, json, os, threading, time, traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--frequency',type=float,default=1);ap.add_argument('--seed',type=int,default=1001);ap.add_argument('--days',type=int,default=365);ap.add_argument('--milestones',default='7,30,90,180,365');ap.add_argument('--output',default='frontier_reports');args=ap.parse_args()
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True);milestones={int(x) for x in args.milestones.split(',') if int(x)<=args.days};milestones.add(args.days)
    report={'version':'1.4.1-stability','seed':args.seed,'checkpoint_profile':sorted(milestones),'initialization':'Production codec order; only seed injected','status':'starting','passed':False,'last_day':0,'checkpoints':[],'errors':[],'milestones':[]};started=time.monotonic()
    def write():
        target=out/f'campaign_seed_{args.seed}.json';temp=target.with_suffix('.tmp');temp.write_text(json.dumps(report,indent=2));temp.replace(target)
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'web')));threading.Thread(target=server.serve_forever,daemon=True).start();write()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True,executable_path=os.environ.get('ICARUS_CHROMIUM') or None)
            ctx=browser.new_context();ctx.add_init_script('window.__icarusSeed='+str(args.seed));page=ctx.new_page();page.set_default_timeout(120000);page.set_default_navigation_timeout(120000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(f'http://127.0.0.1:{server.server_port}/icarus.html?icarus_soak=1');page.wait_for_function('!!window.__icarusSoak')
            page.evaluate('f=>__icarusSoak.configureAnthology(f)',args.frequency)
            initial=json.loads(page.evaluate('JSON.stringify(window.__icarusSoak.snapshot())'));previous_destinations=set();previous_cases=set();previous_jobs=set();initial_systems=len(initial['universe']['systems']);report['status']='running';report['frequency']=args.frequency
            for day in range(1,args.days+1):
                row=page.evaluate('''() => {
                  for(let i=0;i<12;i++)window.__icarusSoak.advance(120);
                  return window.__icarusSoak.daily();
                }''')
                issues=[]
                if row['systems']!=initial_systems:issues.append('Core generated more systems')
                ids=[p['name'] for p in row['crew']]+row['dead']
                if len(ids)!=20 or len(set(ids))!=20:issues.append('Crew identity census failed')
                if row['tick']!=initial['tick']+day*1440 or row['minute']!=initial['minute']+day*1440:issues.append('Continuous clock failed')
                if any(not 0<=p['health']<=100 or not 0<=p['fatigue']<=100 for p in row['crew']):issues.append('Invalid crew condition')
                if row['resource_errors'] or row['frontier_errors']:issues.append('Conservation or domain audit failed')
                if row['durable_backend']!='indexeddb':issues.append('IndexedDB primary unavailable')
                if row['chronicle_errors']:issues.append('Chronicle provenance failed')
                page.evaluate('ICARUSDurable.flush()')
                if row['fuel']<0:issues.append('Negative fuel')
                if not previous_destinations<=set(row['destination_ids']):issues.append('Discovered destinations disappeared')
                if not previous_cases<=set(row['case_ids']):issues.append('Research cases disappeared')
                job_ids={j['id'] for j in row['frontier_jobs']}
                if not previous_jobs<=job_ids:issues.append('Frontier mission records disappeared')
                if any(j['status']=='active' and row['tick']-j['started']>(3600 if row['open_incidents'] else 1800) for j in row['frontier_jobs']):issues.append('Mission deadlock')
                previous_destinations=set(row.pop('destination_ids'));previous_cases=set(row.pop('case_ids'));previous_jobs=job_ids
                jobs=row.pop('frontier_jobs');row['mission_count']=len(jobs);row['outcomes']={k:sum(j['status']==k for j in jobs) for k in ('completed','failed','active')};row['issues']=issues
                report['checkpoints'].append(row);report['last_day']=day;report['errors'].extend('Day '+str(day)+': '+e for e in issues)
                if errors:report['errors'].extend(errors);errors.clear()
                if day in milestones:
                    before=json.loads(page.evaluate('JSON.stringify(window.__icarusSoak.snapshot())'));saved=page.evaluate('window.__icarusSoak.save()');raw=page.evaluate("localStorage.getItem('icarus-v02')");history_json=page.evaluate('ICARUSDurable.history().then(rows=>JSON.stringify(rows))');(out/f'checkpoint_seed_{args.seed}_{day}.json').write_text('{"format":"ICARUS_SAVE","formatVersion":1,"appVersion":"1.4.1","state":'+raw+',"ideas":[],"history":'+history_json+'}')
                    reload_started=time.monotonic();page.reload();page.wait_for_function('!!window.__icarusSoak');reload_seconds=time.monotonic()-reload_started;after=json.loads(page.evaluate('JSON.stringify(window.__icarusSoak.snapshot())'))
                    mismatches=[k for k in before if before[k]!=after.get(k)]
                    if not saved or mismatches:report['errors'].append('Day '+str(day)+': save/reload failed '+str(mismatches))
                    if day>=7 and before['navigation']['arrivals']==0:report['errors'].append('No actual ship travel demonstrated')
                    # Core does not require extraction without a measured shortage; conservation remains mandatory.
                    if before['universe']['coreContext']['version']!=1:report['errors'].append('Missing bounded core context')
                    if day>=30 and (row['anthology']['arcs']==0 or row['memories']==0 or row['staged_jobs']==0):report['errors'].append('Core systems inactive in natural campaign')
                    if day>=30 and row['visited']<3:report['errors'].append('Multiple persistent destinations not demonstrated')
                    if day>=30 and len(jobs)>day*6:report['errors'].append('Excessive mission cadence')
                    payload={'version':report['version'],'seed':args.seed,'requested_days':day,'status':'finished','passed':not report['errors'],'errors':list(report['errors']),'continuous_campaign':True,'milestone_day':day,'checkpoints':list(report['checkpoints']),'navigation':before['navigation'],'universe_statistics':{'systems':row['systems'],'known_destinations':len(previous_destinations),'visited':row['visited']},'frontier_statistics':before['frontier']['stats'],'missions':before['frontier']['jobs'],'legacy_missions':before['director']['registry'],'resource_provenance':before['logistics'],'resource_balances':before['economy'],'resource_audit':before['resourceAudit'],'frontier_audit':before['frontierAudit'],'science':before['director']['science'],'persistence':{'reload_seconds':reload_seconds,'timeout_seconds':120,'saved':saved,'mismatched_fields':mismatches,'state_bytes':len((raw or '').encode()),'storage':page.evaluate('ICARUSSaveStore.stats()'),'sha256':hashlib.sha256((raw or '').encode()).hexdigest()},'repair_control':before['repairControl'],'native_equipment':before['world']['equipment'],'native_incidents':before['world']['emergencies'],'maintenance':before['world']['maintenance'],'anthology':before['anthology'],'living_frontier':{'entities':before['entities'],'emergencyOps':before['emergencyOps'],'experiences':before['experiences'],'chronicles':before['chronicles']},'durable':{'status':page.evaluate('ICARUSDurable.status'),'estimate':page.evaluate('ICARUSDurable.estimate()'),'history_count':page.evaluate('ICARUSDurable.history().then(r=>r.length)')},'crew_outcomes':{'survivors':row['crew'],'deceased':row['dead']},'elapsed_seconds':time.monotonic()-started}
                    history_ids={r['id'] for r in json.loads(history_json)}
                    for arc in before['anthology']['arcs']:
                        if not set(arc['sources'])<=history_ids:payload['errors'].append('Missing story source '+arc['id'])
                    if payload['errors']:payload['passed']=False;report['errors']=list(payload['errors'])
                    if payload['persistence']['state_bytes']>64_000_000 or payload['durable']['estimate']['usage']>512_000_000:payload['errors'].append('Save growth exceeded tested storage budget');payload['passed']=False;report['errors'].append('Save size budget exceeded')
                    (out/f'seed_{args.seed}_{day}day.json').write_text(json.dumps(payload,indent=2))
                    report['milestones'].append({'day':day,'passed':payload['passed'],'arrivals':row['arrivals'],'visited':row['visited'],'jobs':len(jobs),'acquired':row['acquired'],'state_bytes':payload['persistence']['state_bytes']})
                    print('Seed',args.seed,'day',day,'PASS' if payload['passed'] else 'FAIL','arrivals',row['arrivals'],'jobs',len(jobs),'acquired',row['acquired'],flush=True)
                    if day==args.days and saved:
                        (out/f'voyage_seed_{args.seed}.json').write_text('{"format":"ICARUS_SAVE","formatVersion":1,"appVersion":"1.4.1","state":'+raw+',"ideas":[],"history":'+history_json+'}')
                write()
                if report['errors']:break
            report['browser_errors']=errors;report['status']='finished';report['passed']=not report['errors'] and report['last_day']==args.days;browser.close()
    except Exception as e:report['status']='failed';report['errors'].append(str(e));report['traceback']=traceback.format_exc()
    finally:server.shutdown();report['elapsed_seconds']=time.monotonic()-started;write()
    return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
