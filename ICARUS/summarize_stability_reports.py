"""Audit stability, coherent recovery/failure and preserved anthology; survival alone is insufficient."""
import argparse,collections,csv,hashlib,json,re,subprocess
from pathlib import Path
from summarize_anthology_reports import distribution

def load(p):return json.loads(p.read_text())
def write_csv(p,rows):
    with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);args=ap.parse_args();r=args.directory;errors=[];rows=[];balances=[];graphs={};narrative={};science={};operations={};navigation={};cautions=[]
    for seed in (1001,2026,7331):
        campaign=load(r/f'campaign_seed_{seed}.json')
        if not campaign['passed'] or campaign['last_day']!=365 or campaign.get('browser_errors') or campaign['errors']:errors.append(str(seed)+' incomplete campaign or browser error')
        for day in (30,90,180,365):
            d=load(r/f'seed_{seed}_{day}day.json');e=d['resource_balances'];stats=d['repair_control']['stats'];label=f'{seed}/{day}'
            if not d['passed'] or d['errors'] or d['resource_audit'] or d['frontier_audit']:errors.append(label+' runtime audit failure')
            if d['universe_statistics']['systems']!=2 or d['universe_statistics']['known_destinations']!=6:errors.append(label+' core context expansion')
            if len(d['crew_outcomes']['survivors'])+len(d['crew_outcomes']['deceased'])!=20:errors.append(label+' lost founder identity')
            aggregate=collections.defaultdict(float)
            for item in e['ledger'].values():aggregate[(item['kind'],item['key'])]+=item['amount']
            for pool,kind in [('produced','produce'),('consumed','consume'),('disposed','loss'),('feedstockUsed','feedstock_use'),('feedstockImported','recover')]:
                for k,n in e[pool].items():
                    if abs(aggregate[(kind,k)]-n)>1e-5:errors.append(label+' ledger mismatch '+pool+'/'+k)
            scrap=sum(x['amount'] for x in e['ledger'].values() if x['kind']=='recover' and x['source']=='recovered process scrap')
            if scrap>sum(e['consumed'].get(k,0) for k in ['tools','spares','lab'])*.98+1e-5:errors.append(label+' process scrap exceeds actual consumed material yield')
            for k,n in e['feedstock'].items():
                expected=e['feedstockInitial'].get(k,0)+e['feedstockImported'].get(k,0)-e['feedstockUsed'].get(k,0);balances.append({'seed':seed,'days':day,'resource':k,'initial':e['feedstockInitial'].get(k,0),'incoming':e['feedstockImported'].get(k,0),'consumed':e['feedstockUsed'].get(k,0),'remaining':n,'difference':expected-n})
                if n<0 or abs(expected-n)>1e-5:errors.append(label+' finite feedstock balance '+k)
            backup=load(r/f'checkpoint_seed_{seed}_{day}.json');s=backup['state'];claims=collections.Counter(p.get('emergencyId') for p in s['crew'] if p.get('emergencyId') and not s['emergencies'].get(p['emergencyId'],{}).get('atmospheric'))
            if any(n>1 for n in claims.values()):errors.append(label+' over-reserved native fault')
            if any(p.get('emergencyId') and (p.get('expeditionAway') or p.get('expeditionId') or p.get('responseAssignment')) for p in s['crew']):errors.append(label+' phantom/double emergency assignment')
            low_samples=sum(any(x['stores'][k]<v for k,v in [('water',5),('oxygen',5),('energy',10),('food',10)]) for x in d['checkpoints'])
            rows.append({'seed':seed,'days':day,'survivors':len(d['crew_outcomes']['survivors']),'deaths':len(d['crew_outcomes']['deceased']),'native_failures':stats.get('nativeFaults',0),'maintenance_assignments':stats.get('preventiveStarted',0),'preventive_completed':stats.get('preventiveCompleted',0),'emergency_dispatches':stats.get('dispatches',0),'native_repairs_completed':stats.get('emergencyCompleted',0),'hatches_cleared':stats.get('hatchesCleared',0),'unfunded_work_deferrals':stats.get('unfundedWork',0),'released_assignments':stats.get('releasedAssignments',0),'day_end_low_reserve_samples':low_samples,'stories':len(d['anthology']['arcs']),'channels':sum('signalHour'in x for x in d['anthology']['arcs']),'science_cases':len(d['science']['cases']),'arrivals':d['navigation']['arrivals'],'logical_snapshot_bytes':d['persistence']['state_bytes'],'reload_seconds':d['persistence']['reload_seconds'],'indexeddb_bytes':d['durable']['estimate']['usage']})
            if stats.get('preventiveCompleted',0)==0 or d['navigation']['arrivals']==0:errors.append(label+' surviving uptime without maintenance/travel evidence')
        b=load(r/f'voyage_seed_{seed}.json');s=b['state'];history={x['id']:x for x in b['history']};ids=set(history);a=s['anthology'];issues=[]
        if len(ids)!=len(b['history']):issues.append('duplicate indexed IDs')
        known=ids|{x['id'] for x in s['frontier']['jobs']}|{x['id'] for x in s['remoteCore']['director']['registry']}|{x['id'] for x in s['emergencyOps']['incidents']}
        for arc in a['arcs']:
            if not set(arc['sources'])<=ids:issues.append('missing arc source '+arc['id'])
            for h in arc['history']:
                if history.get(h['sourceId'],{}).get('message')!=h['text']:issues.append('invented arc text '+arc['id'])
        for m in s['experiences']['records']:
            if m['sourceId'] not in known:issues.append('missing personal-memory source '+m['id'])
        for w in s['chronicles']['weeks'].values():
            if not set(w['sourceIds'])<=ids:issues.append('missing weekly source '+str(w['episode']))
            for card in w['segments']:
                if history.get(card['sourceId'],{}).get('message')!=card['message']:issues.append('invented chronicle card')
        for actor in s['entities']['registry'].values():
            for k,n in actor['stock'].items():
                if n<0 or abs(actor['initial'].get(k,0)+actor['received'].get(k,0)-actor['spent'].get(k,0)-n)>1e-6:issues.append('actor stock imbalance '+actor['id'])
        sc=s['remoteCore']['director']['science'];science[str(seed)]={'cases':len(sc['cases']),'programs':len(sc['programs']),'experiments':dict(collections.Counter(x['status'] for x in sc['experiments'])),'lazarus':sc.get('lazarusProgram'),'conclusions':sc['conclusions']}
        external=[x for x in a['arcs'] if 'signalHour'in x];dist=distribution(external,s['tick']);narrative[str(seed)]={'external':dist,'all_stories':distribution(a['arcs'],s['tick']),'max_overlap':a['maxOverlap'],'memories':len(s['experiences']['records']),'traditions':len(a['traditions']),'open_stories':sum(x['status']=='open' for x in a['arcs'])}
        if len(dist['categories'])<6 or not any(x.get('outcome')=='shared_moment' for x in external):issues.append('meaningful diverse/positive anthology activity missing')
        life_alarms=[h for h in history.values() if h.get('message','').startswith('ALARM:') and any(k in h['message'] for k in ['Power distribution fault','Air scrubber malfunction','Cooling controller fault'])]
        shortages=[h for h in history.values() if h.get('message','').startswith('SOL resource priority: survival')]
        navigation[str(seed)]={'arrivals':s['navigation']['arrivals'],'fuel_used':s['navigation']['fuelUsed'],'recent_routes':s['navigation']['history'],'last_decision':s['navigation'].get('lastDecision'),'objective_failures':dict(collections.Counter(j['destination']+'/'+j['type'] for j in s['frontier']['jobs'] if j['status']=='failed')),'transport':s['emergencyOps']['transport']}
        long_incidents={k:{'age':x.get('age'),'label':x['label']} for k,x in s['emergencies'].items() if x['status']=='active' and x.get('age',0)>1440}
        if long_incidents:cautions.append({'seed':seed,'review':'Long unresolved incidents require causal interpretation, not automatic success from survival','incidents':long_incidents})
        decision_sources=[h for h in history.values() if h.get('message','').startswith(('SOL: Measured','SOL: Released','SOL: Retained','SOL: Retired','SOL: Suspended','SOL: Removed','SOL: Emergency','SOL resource priority:')) or 'manually repairing distribution' in h.get('message','') or 'cleared ' in h.get('message','') and 'hatch after physical' in h.get('message','')]
        operations[str(seed)]={'major_decision_source_count':len(decision_sources),'major_decision_examples':decision_sources[:12]+decision_sources[-12:] if len(decision_sources)>24 else decision_sources,'stats':s['repairControl']['stats'],'final_forecasts':s['repairControl']['forecast'],'recent_actual_decisions':s['repairControl']['decisions'],'last_native_incidents':{k:{'status':v['status'],'age':v['age'],'progress':v['progress'],'label':v['label']} for k,v in s['emergencies'].items()},'recorded_life_support_alarms':len(life_alarms),'recorded_survival_mode_entries':len(shortages),'unresolved_long_incidents':long_incidents,'source_accounting':{'frontier_credited':s['logistics']['credited'],'all_recovered_feedstock':s['economy']['feedstockImported'],'process_scrap_ore':sum(x['amount'] for x in s['economy']['ledger'].values() if x['kind']=='recover' and x['source']=='recovered process scrap')},'deaths':s['living']['deceased'],'remaining_orders':s['maintenance']['orders']}
        graphs[str(seed)]={'history_records':len(history),'errors':issues};errors.extend(str(seed)+': '+x for x in issues)
    old=load(r/'counterfactual_old.json');fixed=load(r/'counterfactual_repaired.json');counter={'same_input_state':old['input_state_sha256']==fixed['input_state_sha256'],'old_final_survivors':len(old['final']['crew']),'repaired_final_survivors':len(fixed['final']['crew']),'both_initial_inventory_verified':old['unchanged_initial_inventory_and_crew'] and fixed['unchanged_initial_inventory_and_crew'],'repaired_stats':fixed['final']['repairControl']['stats']}
    if not counter['same_input_state'] or not counter['both_initial_inventory_verified'] or counter['old_final_survivors']!=0 or counter['repaired_final_survivors']!=20 or not old['passed'] or not fixed['passed']:errors.append('Captured-state causal recovery not demonstrated')
    reproduction=load(r/'baseline_reproduction.json')
    if not reproduction['completed'] or reproduction['errors'] or len(reproduction['daily'][-1]['dead'])!=20:errors.append('Original failure not reproduced')
    adverse=load(r/'adverse.json')
    if not adverse['passed'] or not all(x.get('initial_conditions_verified') and x['exact_reload'] for x in adverse['scenarios']):errors.append('Adverse setup/outcome/persistence failed')
    tests={};unit=(r/'unit_results.txt').read_text();counts={k:int(re.search(r'ℹ '+k+r' (\d+)',unit).group(1)) for k in ('tests','pass','fail','skipped')};tests['unit']=counts
    if counts['fail'] or counts['skipped'] or counts['pass']!=counts['tests']:errors.append('Unit suite failure/skip')
    for name in ['stability_integration.json','compatibility.json','bridge.json','backup_roundtrip.json','syntax.json']:
        d=load(r/name);tests[name]={'passed':d['passed'],'count':d.get('tests_run',d.get('tests'))}
        if not d['passed']:errors.append('Failed '+name)
    source=Path(__file__).resolve().parent;provenance=load(r/'campaign_source.json');runtime={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((source/'web').rglob('*')) if p.is_file()}
    if runtime!=provenance['runtime_sha256']:errors.append('Accepted runtime differs from packaged runtime')
    for name,data in [('resource_conservation.json',{'audited_milestones':len(rows),'ledger_and_inventory_errors':[x for x in errors if 'ledger' in x or 'balance' in x]}),('source_graphs.json',graphs),('anthology_preservation.json',narrative),('science_lazarus.json',science),('operations_and_recovery.json',operations),('causal_counterfactual.json',counter),('navigation_review.json',navigation)]: (r/name).write_text(json.dumps(data,indent=2))
    write_csv(r/'campaign_statistics.csv',rows);write_csv(r/'resource_balances.csv',balances)
    summary={'version':'1.4.1','source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip(),'campaign_source_commit':provenance['source_commit'],'runtime_sha256':runtime,'mechanical_checks_passed':not errors,'targeted_stabilization_verified':not errors and not cautions,'acceptance_verified':not errors and not cautions,'final_release_ready':False,'tests':tests,'milestones':rows,'causal_counterfactual':counter,'errors':errors,'review_cautions':cautions,'interpretation':'Survival alone is insufficient. Physical paid recovery, source integrity, bounded assignments, preserved autonomous activity, unchanged captured-state inputs and coherent unrecoverable adverse cases are required. No general invulnerability/final-release claim.'};(r/'validation_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps({'verified':summary['acceptance_verified'],'errors':errors,'cautions':cautions,'milestones':len(rows)},indent=2));return not summary['acceptance_verified']
if __name__=='__main__':raise SystemExit(main())
