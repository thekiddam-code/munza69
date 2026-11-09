"""Continuing Living Frontier campaigns with indexed history, contacts and rescue metrics."""
import argparse, functools, hashlib, http.server, json, os, threading, time, traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=1001);ap.add_argument('--days',type=int,default=365);ap.add_argument('--milestones',default='7,30,90,180,365');ap.add_argument('--output',default='frontier_reports');args=ap.parse_args()
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True);milestones={int(x) for x in args.milestones.split(',') if int(x)<=args.days};milestones.add(args.days)
    report={'version':'1.3-living-frontier','seed':args.seed,'status':'starting','passed':False,'last_day':0,'checkpoints':[],'errors':[],'milestones':[]};started=time.monotonic()
    def write(): (out/f'campaign_seed_{args.seed}.json').write_text(json.dumps(report,indent=2))
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'web')));threading.Thread(target=server.serve_forever,daemon=True).start();write()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True,executable_path=os.environ.get('ICARUS_CHROMIUM') or None)
            ctx=browser.new_context();ctx.add_init_script((ROOT/'web/vendor/lz-string.min.js').read_text()+';'+(ROOT/'web/save-store.js').read_text()+';window.__icarusSeed='+str(args.seed));page=ctx.new_page();page.set_default_timeout(120000);page.set_default_navigation_timeout(120000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(f'http://127.0.0.1:{server.server_port}/icarus.html?icarus_soak=1');page.wait_for_function('!!window.__icarusSoak')
            initial=page.evaluate('window.__icarusSoak.snapshot()');previous_destinations=set();previous_cases=set();previous_jobs=set();report['status']='running'
            for day in range(1,args.days+1):
                row=page.evaluate('''() => {
                  for(let i=0;i<12;i++)window.__icarusSoak.advance(120);
                  const s=window.__icarusSoak.snapshot(),ds=Object.values(s.universe.systems).flatMap(x=>x.bodies);
                  return {day:Math.floor(s.tick/1440),tick:s.tick,minute:s.minute,episode:s.episode,archives:s.archived.length,crew:s.crew.map(p=>({name:p.name,health:p.vitals.health,fatigue:p.vitals.fatigue,morale:p.vitals.morale,energy:p.energy})),dead:s.living.deceased.map(p=>p.name),resource_errors:s.resourceAudit,frontier_errors:s.frontierAudit,destination_ids:ds.map(d=>d.id),visited:ds.filter(d=>d.visited).length,systems:Object.keys(s.universe.systems).length,phase:s.navigation.phase,position:s.navigation.position,target:s.navigation.target,arrivals:s.navigation.arrivals,fuel:s.economy.feedstock.fuel,travel_fuel:s.navigation.fuelUsed,stores:s.resourceTotals,acquired:s.logistics.credited,frontier_jobs:s.frontier.jobs.map(j=>({id:j.id,type:j.type,status:j.status,started:j.started})),case_ids:s.director.science.cases.map(c=>c.id),samples:s.frontier.stats.samples,event_kinds:s.frontier.stats.eventKinds,entities:Object.keys(s.entities.registry).length,encounters:s.entities.stats,interaction_count:s.entities.encounters.length,emergencies:s.emergencyOps.stats,open_incidents:s.emergencyOps.incidents.filter(i=>i.status==='open').map(i=>({id:i.id,created:i.created})),memories:s.experiences.records.length,staged_jobs:s.frontier.jobs.filter(j=>j.stages).length,team_sizes:[...new Set(s.frontier.jobs.map(j=>j.members.length))],chronicle_errors:ICARUSChronicles.audit(s),durable_backend:ICARUSDurable.status.backend};
                }''')
                issues=[];ids=[p['name'] for p in row['crew']]+row['dead']
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
                    before=page.evaluate('window.__icarusSoak.snapshot()');saved=page.evaluate('window.__icarusSoak.save()');raw=page.evaluate("localStorage.getItem('icarus-v02')")
                    reload_started=time.monotonic();page.reload();page.wait_for_function('!!window.__icarusSoak');reload_seconds=time.monotonic()-reload_started;after=page.evaluate('window.__icarusSoak.snapshot()')
                    mismatches=[k for k in before if before[k]!=after.get(k)]
                    if not saved or mismatches:report['errors'].append('Day '+str(day)+': save/reload failed '+str(mismatches))
                    if day>=7 and before['navigation']['arrivals']==0:report['errors'].append('No actual ship travel demonstrated')
                    if day>=90 and sum(before['logistics']['credited'].values())<=0:report['errors'].append('No actual resource acquisition demonstrated')
                    if day>=90 and row['arrivals']<=report['checkpoints'][-31]['arrivals']:report['errors'].append('No actual travel in the final thirty days')
                    if day>=30 and (row['interaction_count']==0 or row['memories']==0 or row['staged_jobs']==0):report['errors'].append('New systems inactive in natural campaign')
                    if day>=30 and row['visited']<3:report['errors'].append('Multiple persistent destinations not demonstrated')
                    if day>=30 and len(jobs)>day*6:report['errors'].append('Excessive mission cadence')
                    payload={'version':report['version'],'seed':args.seed,'requested_days':day,'status':'finished','passed':not report['errors'],'errors':list(report['errors']),'continuous_campaign':True,'milestone_day':day,'checkpoints':list(report['checkpoints']),'navigation':before['navigation'],'universe_statistics':{'systems':row['systems'],'known_destinations':len(previous_destinations),'visited':row['visited']},'frontier_statistics':before['frontier']['stats'],'missions':before['frontier']['jobs'],'legacy_missions':before['director']['registry'],'resource_provenance':before['logistics'],'resource_balances':before['economy'],'resource_audit':before['resourceAudit'],'frontier_audit':before['frontierAudit'],'science':{'cases':len(before['director']['science']['cases']),'experiments':len(before['director']['science'].get('experiments',[])),'conclusions':before['director']['science'].get('conclusions',[])},'persistence':{'reload_seconds':reload_seconds,'timeout_seconds':120,'saved':saved,'mismatched_fields':mismatches,'state_bytes':len((raw or '').encode()),'storage':page.evaluate('ICARUSSaveStore.stats()'),'sha256':hashlib.sha256((raw or '').encode()).hexdigest()},'living_frontier':{'entities':before['entities'],'emergencyOps':before['emergencyOps'],'experiences':before['experiences'],'chronicles':before['chronicles']},'durable':{'status':page.evaluate('ICARUSDurable.status'),'estimate':page.evaluate('ICARUSDurable.estimate()'),'history_count':page.evaluate('ICARUSDurable.history().then(r=>r.length)')},'crew_outcomes':{'survivors':row['crew'],'deceased':row['dead']},'elapsed_seconds':time.monotonic()-started}
                    if payload['persistence']['state_bytes']>64_000_000 or payload['durable']['estimate']['usage']>512_000_000:payload['errors'].append('Save growth exceeded tested storage budget');payload['passed']=False;report['errors'].append('Save size budget exceeded')
                    (out/f'seed_{args.seed}_{day}day.json').write_text(json.dumps(payload,indent=2))
                    report['milestones'].append({'day':day,'passed':payload['passed'],'arrivals':row['arrivals'],'visited':row['visited'],'jobs':len(jobs),'acquired':row['acquired'],'state_bytes':payload['persistence']['state_bytes']})
                    print('Seed',args.seed,'day',day,'PASS' if payload['passed'] else 'FAIL','arrivals',row['arrivals'],'jobs',len(jobs),'acquired',row['acquired'],flush=True)
                    if day==args.days and saved:(out/f'voyage_seed_{args.seed}.json').write_text(json.dumps({'format':'ICARUS_SAVE','formatVersion':1,'appVersion':'1.3','state':json.loads(raw),'ideas':[],'history':page.evaluate('ICARUSDurable.history()')}))
                write()
                if report['errors']:break
            report['browser_errors']=errors;report['status']='finished';report['passed']=not report['errors'] and report['last_day']==args.days;browser.close()
    except Exception as e:report['status']='failed';report['errors'].append(str(e));report['traceback']=traceback.format_exc()
    finally:server.shutdown();report['elapsed_seconds']=time.monotonic()-started;write()
    return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
