"""ICARUS v0.94.3 weekly continuity and persistence soak test.
Run: python soak_test.py --days 7
Requires: pip install playwright && python -m playwright install chromium
"""
import argparse
import functools
import http.server
import json
import threading
import traceback
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--days',type=int,default=7)
    parser.add_argument('--seed',type=int,default=1001)
    parser.add_argument('--seed-science',action='store_true',help='Use explicitly synthetic recovered evidence')
    parser.add_argument('--report',default='soak_report.json')
    args=parser.parse_args()
    report_path=Path(args.report).resolve()
    report={'version':'1.1-continuous-voyage','requested_days':args.days,'status':'starting','passed':False,'checkpoints':[],'errors':[],'started_at':datetime.now(timezone.utc).isoformat()}
    def write(): report_path.write_text(json.dumps(report,indent=2,default=str),encoding='utf-8')
    write()
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args): pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'web')))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True, executable_path=__import__("os").environ.get("ICARUS_CHROMIUM") or None)
            context=browser.new_context()
            context.add_init_script('window.__icarusSeed='+str(args.seed))
            report['seed']=args.seed
            page=context.new_page()
            js_errors=[]
            page.on('pageerror',lambda error:js_errors.append({'message':str(error),'stack':getattr(error,'stack',None)}))
            page.goto(f'http://127.0.0.1:{server.server_port}/icarus.html?icarus_soak=1',wait_until='load',timeout=30000)
            page.wait_for_function('typeof window.__icarusSoak === "object"',timeout=15000)
            report['synthetic_science_fixture']=args.seed_science
            if args.seed_science:
                page.evaluate('window.__icarusSoak.save()')
                page.add_init_script('''(() => {
                    if(sessionStorage.getItem('fixture-seeded'))return;
                    sessionStorage.setItem('fixture-seeded','1');
                    const s=JSON.parse(localStorage.getItem('icarus-v02'));
                    s.specimenCustody={items:[],history:[],nextId:10};
                    s.remoteCore.director.science={cases:[],nextCase:10,lastTick:-1};
                    for(let i=0;i<3;i++){
                      s.specimenCustody.items.push({id:'TEST-S'+i,name:'mineral fixture '+i,origin:'asteroid',status:'stored',location:'B10',integrity:i===2?10:100,contamination:i===1?10:0,volatile:false,biological:false,concealed:false,age:0});
                      s.remoteCore.director.science.cases.push({id:'SCI-TEST'+i,key:'fixture'+i,location:'asteroid',item:'mineral fixture '+i,specimenId:'TEST-S'+i,status:'queued',progress:0});
                    }
                    localStorage.setItem('icarus-v02',JSON.stringify(s));
                })();''')
                page.reload(wait_until='load')
                page.wait_for_function('typeof window.__icarusSoak === "object"')
            initial=page.evaluate('window.__icarusSoak.snapshot()')
            page.wait_for_timeout(1100)
            report['paused_clock_check']=page.evaluate('window.__icarusSoak.snapshot()')==initial
            if not report['paused_clock_check']:report['errors'].append('Clock advanced while diagnostic timer paused')
            report['start']={k:initial[k] for k in ('minute','tick','episode')}
            report['status']='running';write()
            last=initial
            elapsed=0
            last_checkpoint=initial
            for day in range(args.days):
                for _ in range(12):
                    result=page.evaluate('window.__icarusSoak.advance(120)')
                    elapsed+=120
                    if args.seed_science and elapsed==120:
                        pending=page.evaluate('window.__icarusSoak.snapshot()')
                        history_so_far=page.evaluate('window.__icarusSoak.missionHistory')
                        page.evaluate('window.__icarusSoak.save()')
                        page.reload(wait_until='load')
                        page.wait_for_function('typeof window.__icarusSoak === "object"')
                        report['early_persistence_check']=pending==page.evaluate('window.__icarusSoak.snapshot()')
                        report['early_experiment_states']=[e['status'] for e in pending['director']['science'].get('experiments',[])]
                        if not report['early_persistence_check']:report['errors'].append('Early science save/reload mismatch')
                        page.evaluate('(history)=>window.__icarusSoak.missionHistory=history',history_so_far)
                    if result['episode']<last['episode'] or result['episode']>last['episode']+1:
                        report['errors'].append('Unexpected episode transition')
                    if result['episode']==last['episode'] and result['tick']<last['tick']:
                        report['errors'].append('Unexpected tick reset without episode transition')
                    last=result
                snap=page.evaluate('window.__icarusSoak.snapshot()')
                issues=[]
                deceased=(snap.get('living') or {}).get('deceased',[])
                if len(snap['crew'])+len(deceased)!=20: issues.append('Crew census (survivors plus recorded deceased) not 20')
                identities=[p['name'] for p in snap['crew']]+[p['name'] for p in deceased]
                if len(set(identities))!=20:issues.append('Crew identity duplication or resurrection')
                for p in snap['crew']:
                    for field in ('health','fatigue','morale'):
                        if not 0<=p.get('vitals',{}).get(field,-1)<=100:issues.append('Invalid crew '+field)
                audit=page.evaluate('window.__icarusSoak.snapshot().resourceAudit')
                if audit:issues.append('Resource conservation violation: '+str(audit))
                if snap['tick']!=initial['tick']+elapsed:issues.append('Monotonic tick mismatch')
                for loc,m in snap['missions'].items():
                    if not m:continue
                    if snap['tick']-m.get('launched',snap['tick'])>2000:issues.append('Expedition deadlock '+loc)
                    members=m.get('members',[m['crew']])
                    if len(set(members))!=len(members):issues.append('Duplicate expedition members')
                    if any(n not in identities for n in members):issues.append('Disappearing expedition crew')
                old_science=last_checkpoint.get('director',{}).get('science',{})
                new_science=snap.get('director',{}).get('science',{})
                if not {c['id'] for c in old_science.get('cases',[])}<={c['id'] for c in new_science.get('cases',[])}:issues.append('Science case lost across checkpoint')
                if not {e['id'] for e in old_science.get('experiments',[])}<={e['id'] for e in new_science.get('experiments',[])}:issues.append('Experiment history lost across checkpoint')
                last_checkpoint=snap
                if any(not isinstance(p.get('energy'),(int,float)) or not 0<=p['energy']<=100 for p in snap['crew']): issues.append('Invalid crew energy')
                report['checkpoints'].append({'day':day+1,'elapsed_minutes':elapsed,'episode':snap['episode'],'minute':snap['minute'],'tick':snap['tick'],'archives':len(snap['archived']),'events':len(snap['events']),'issues':issues,'surviving_crew':len(snap['crew']),'recorded_deaths':len(deceased),'stores':page.evaluate('window.__icarusSoak.snapshot().resourceTotals'),'feedstock':snap['economy']['feedstock'],'conservation_errors':audit,'science_cases':len(snap['director']['science']['cases']),'experiments':len(snap['director']['science'].get('experiments',[])),'mission_count':len(snap['director']['registry']),'state_bytes':len(json.dumps(snap)),'missions':{k:(v or {}).get('phase') for k,v in (snap.get('missions') or {}).items()}})
                report['errors'].extend('Day '+str(day+1)+': '+x for x in issues)
                write()
            history=page.evaluate('window.__icarusSoak.missionHistory')
            director=page.evaluate('window.__icarusSoak.snapshot().director')
            report['mission_registry']=[{'id':m.get('id'),'type':m.get('type'),'location':m.get('location'),'reason':m.get('reason'),'status':m.get('status'),'outcome':m.get('outcome'),'evidence':m.get('evidence'),'objective':m.get('objective'),'completion_reason':m.get('completionReason'),'members':m.get('members'),'team_debrief':m.get('teamDebrief'),'risk_assessment':m.get('riskAssessment')} for m in director.get('registry',[])]
            report['mission_summary']={'created':len(director.get('registry',[])),'completed':sum(m.get('status')=='completed' for m in director.get('registry',[])),'unjustified':sum(not m.get('reason') or not m.get('objective') for m in director.get('registry',[]))}
            if report['mission_summary']['unjustified']:report['errors'].append('Director created missions without documented objectives')
            report['mission_intelligence']=director.get('intelligence',{})
            science=director.get('science',{}).get('cases',[])
            report['science_cases']=[{k:c.get(k) for k in ('id','location','item','mission','status','progress','classification','hazard','analyst','assessment')} for c in science]
            report['research_programs']=director.get('science',{}).get('programs',[])
            report['specimen_custody']=page.evaluate('window.__icarusSoak.snapshot().specimenCustody')
            report['research_experiments']=director.get('science',{}).get('experiments',[])
            case_ids={c['id'] for c in science}
            for p in report['research_programs']:
                if any(cid not in case_ids for cid in p['caseIds']):report['errors'].append('Research program evidence reference missing')
                for h in p['hypotheses']:
                    if not h['unknowns'] or h['confidence']>0.45:report['errors'].append('Research uncertainty lost')
                    if any(e['caseId'] not in case_ids for e in h['evidenceFor']+h['evidenceAgainst']):report['errors'].append('Hypothesis provenance missing')
            if args.seed_science:
                if len((report['specimen_custody'] or {}).get('items',[]))<3:report['errors'].append('Weekly custody continuity lost')
                outcomes={e['status'] for e in report['research_experiments']}
                if not {'complete','failed','no_result'}<=outcomes:report['errors'].append('Seeded experiment outcomes missing')
                if not any(len(p['caseIds'])==3 for p in report['research_programs']):report['errors'].append('Related cases not grouped')
            report['science_summary']={'intake':len(science),'completed':sum(c.get('status')=='complete' for c in science),'held':sum(c.get('status')=='held' for c in science),'pending':sum(c.get('status') not in ('complete','held') for c in science)}
            if len({c.get('id') for c in science})!=len(science):report['errors'].append('Duplicate science case IDs')
            if any(c.get('status')=='complete' and not c.get('classification') for c in science):report['errors'].append('Completed science case missing classification')
            report['mission_consequences']={'completion_reasons':{reason:sum(m.get('completion_reason')==reason for m in report['mission_registry']) for reason in sorted(set(m.get('completion_reason') for m in report['mission_registry'] if m.get('completion_reason')))},'zero_progress':sum(m.get('status')=='completed' and (m.get('evidence') or {}).get('surveyedNew',0)==0 and (m.get('evidence') or {}).get('findingsNew',0)==0 for m in report['mission_registry']),'crew_recovery_reservations':len(director.get('crewReadyAt',{}))}
            report['mission_diversity']={'types':sorted(set(m.get('type') for m in report['mission_registry'])),'locations':sorted(set(m.get('location') for m in report['mission_registry'])),'completed_with_evidence':sum(bool(m.get('evidence')) for m in report['mission_registry'])}
            report['expedition_transitions']=history
            report['expedition_summary']={loc:{'departures':sum(1 for e in history if e['location']==loc and e['from'] is None and e['to'] is not None),'arrivals':sum(1 for e in history if e['location']==loc and e['to']=='onsite'),'returns_started':sum(1 for e in history if e['location']==loc and e['to']=='returning'),'completed':sum(1 for e in history if e['location']==loc and e['from']=='returning' and e['to'] is None)} for loc in ('derelict','asteroid')}
            for loc,stats in report['expedition_summary'].items():
                if stats['arrivals'] and not stats['completed']:
                    report['errors'].append(f'{loc}: arrived onsite but never completed a return during seven-day test')
            before=page.evaluate('window.__icarusSoak.snapshot()')
            saved=page.evaluate('window.__icarusSoak.save()')
            if not saved: report['errors'].append('Browser save returned false')
            page.reload(wait_until='load')
            page.wait_for_function('typeof window.__icarusSoak === "object"',timeout=15000)
            after=page.evaluate('window.__icarusSoak.snapshot()')
            differences=[key for key in before if before[key]!=after.get(key)]
            crew_changes=[]
            if before.get('crew')!=after.get('crew'):
                a={p.get('name'):p for p in before.get('crew',[])}
                b={p.get('name'):p for p in after.get('crew',[])}
                for name in sorted(set(a)|set(b)):
                    if a.get(name)!=b.get(name):
                        fields=sorted(k for k in set((a.get(name) or {}))|set((b.get(name) or {})) if (a.get(name) or {}).get(k)!=(b.get(name) or {}).get(k))
                        crew_changes.append({'name':name,'fields':fields,'before':{k:(a.get(name) or {}).get(k) for k in fields},'after':{k:(b.get(name) or {}).get(k) for k in fields}})
            report['crew_differences']=crew_changes[:30]
            report['persistence']={'saved':saved,'mismatched_fields':differences,'before':{k:before[k] for k in ('episode','minute','tick')},'after':{k:after[k] for k in ('episode','minute','tick')}}
            if differences: report['errors'].append('Save/reload mismatched: '+', '.join(differences))
            final_minute=initial['minute']+elapsed
            boundary=initial['clock']['nextEpisodeAt']
            rollover_count=0 if final_minute<boundary else 1+(final_minute-boundary)//10080
            expected_episode=initial['episode']+rollover_count
            report['long_duration_clock']={'expected_episode':expected_episode,'actual_episode':before['episode'],'expected_minute':final_minute,'actual_minute':before['minute'],'expected_tick':initial['tick']+elapsed,'actual_tick':before['tick']}
            report['clock_diagnostic']=report['long_duration_clock'].copy()
            if (before['episode'],before['minute'],before['tick'])!=(expected_episode,final_minute,initial['tick']+elapsed):report['errors'].append('Continuous simulation clock mismatch')
            if len(before['archived'])!=len(initial['archived'])+rollover_count:report['errors'].append('Archive count mismatch')
            report['crew_continuity']={'survivors':before['crew'],'deceased':(before.get('living') or {}).get('deceased',[])}
            report['research_lazarus']=director.get('science',{}).get('lazarusProgram')
            report['operations']=before.get('operations')
            report['economy']=before['economy']
            report['resource_audit']=page.evaluate('window.__icarusSoak.snapshot().resourceAudit')
            if report['resource_audit']:report['errors'].append('Final resource conservation failure')
            report['scientific_conclusions']=director.get('science',{}).get('conclusions',[])
            report['discovery_statistics']={'programs':len(report['research_programs']),'experiment_outcomes':{status:sum(e['status']==status for e in report['research_experiments']) for status in ('complete','no_result','failed','running')},'confirmed_conclusions':sum(c.get('status')=='confirmed' for c in report['scientific_conclusions']),'contested_conclusions':sum(c.get('status')=='contested' for c in report['scientific_conclusions']),'sampled_cells':sum(bool(room.get('scientificSurvey')) for key in ('remoteExploration','asteroidExploration') for room in (before['world'].get(key) or {}).get('rooms',[]))}
            report['team_statistics']={'launches':(before.get('teamLog') or {}).get('launches',0),'suits':(before.get('teamLog') or {}).get('suits',0),'lost_suits':(before.get('teamLog') or {}).get('lostSuits',0),'failed_missions':sum(j.get('status')=='failed' for j in report['mission_registry']),'team_sizes':[len(j.get('members') or []) for j in report['mission_registry']]}
            report['natural_discovery_count']=sum(bool(i.get('source')) for i in (before.get('specimenCustody') or {}).get('items',[]))
            if args.days>=7 and not args.seed_science and report['natural_discovery_count']==0:report['errors'].append('No natural specimen discovery demonstrated')
            report['weekly_recaps']=[a.get('recap') for a in before['archived']]
            report['bounds']={'cases':len(science),'experiments':len(report['research_experiments']),'missions':len(report['mission_registry']),'journal_records':len((before.get('chronicle') or {}).get('records',[])),'state_bytes':len(json.dumps(before))}
            if report['bounds']['cases']>100 or report['bounds']['experiments']>600 or report['bounds']['missions']>100:report['errors'].append('Unbounded domain state growth')
            if args.days>=30:
                recent=[p['mission_count'] for p in report['checkpoints'][-7:]]
                report['late_mission_growth']=max(recent)-min(recent)
                if report['late_mission_growth']>4:report['errors'].append('Repetitive late-voyage mission growth')
            report['browser_errors']=js_errors[:20]
            report['timer_isolation']='Live simulation timer paused in diagnostic mode; only explicit advance() changes simulation time'
            if 'clock_diagnostic' in report: report['clock_diagnostic']['timer_isolation']='enabled'
            report['mission_diagnostic']={'derelict_phases':[x['missions'].get('derelict') for x in report['checkpoints']],'asteroid_phases':[x['missions'].get('asteroid') for x in report['checkpoints']]}
            if js_errors:report['errors'].append('Browser JavaScript errors occurred')
            report['status']='finished';report['passed']=not report['errors']
            browser.close()
    except Exception as exc:
        report['status']='failed';report['errors'].append(str(exc));report['traceback']=traceback.format_exc()
    finally:
        server.shutdown();write()
    print('Report:',report_path,'\nResult:', 'PASS' if report['passed'] else 'FAIL')
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
