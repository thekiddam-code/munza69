"""Summarize actual Living Frontier campaigns and audit cross-system provenance."""
import argparse, collections, csv, hashlib, json, re, subprocess
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);ap.add_argument('--seeds',default='1001,2026');args=ap.parse_args();root=args.directory;seeds=[int(x) for x in args.seeds.split(',')];stats=[];balances=[];audits={};errors=[];milestones=[];integrity={};research={};living_metrics={}
    for seed in seeds:
        for days in (7,30,90,180,365):
            path=root/f'seed_{seed}_{days}day.json'
            if not path.exists():errors.append(f'Missing {path.name}');continue
            d=json.loads(path.read_text());row=d['checkpoints'][-1];jobs=collections.Counter(j['type'] for j in d['missions']);nav=d['navigation'];e=d['resource_balances'];milestones.append({'seed':seed,'days':days,'passed':d['passed'],'errors':d['errors']})
            if not d['passed']:errors.append(f'{path.name}: {d["errors"]}')
            stats.append({'seed':seed,'days':days,'minutes':row['tick'],'weekly_archives':row['archives'],'arrivals':nav['arrivals'],'visited':d['universe_statistics']['visited'],'known_destinations':d['universe_statistics']['known_destinations'],'systems':row['systems'],'entities':len(d['living_frontier']['entities']['registry']),'encounters':len(d['living_frontier']['entities']['encounters']),'contact_outcomes':json.dumps(d['living_frontier']['entities']['stats'],sort_keys=True),'emergency_outcomes':json.dumps(d['living_frontier']['emergencyOps']['stats'],sort_keys=True),'memories':len(d['living_frontier']['experiences']['records']),'indexed_history_rows':d['durable']['history_count'],'indexeddb_bytes':d['durable']['estimate']['usage'],'legacy_jobs':len(d['legacy_missions']),'legacy_mission_types':json.dumps(dict(collections.Counter(j['type'] for j in d['legacy_missions'])),sort_keys=True),'frontier_jobs':len(d['missions']),'completed':d['frontier_statistics']['completed'],'failed':d['frontier_statistics']['failed'],'mission_types':json.dumps(dict(jobs),sort_keys=True),'natural_frontier_samples':d['frontier_statistics']['samples'],'science_cases':d['science']['cases'],'experiments':d['science']['experiments'],'confirmed_families':len(d['science']['conclusions']),'survivors':len(d['crew_outcomes']['survivors']),'deceased':len(d['crew_outcomes']['deceased']),'travel_fuel':nav['fuelUsed'],'remaining_fuel':e['feedstock']['fuel'],'acquired':json.dumps(d['resource_provenance']['credited'],sort_keys=True),'event_diversity':len(d['frontier_statistics']['eventKinds']),'events':json.dumps(d['frontier_statistics']['eventKinds'],sort_keys=True),'logical_save_bytes':d['persistence']['state_bytes'],'physical_core_slots_bytes':d['persistence']['storage']['physical_bytes'],'save_mismatches':len(d['persistence']['mismatched_fields'])})
            ledger=list(e.get('ledger',{}).values());ledger_errors=[]
            for category,kind in [('produced','produce'),('consumed','consume'),('disposed','loss'),('feedstockUsed','feedstock_use'),('feedstockImported','recover')]:
                for key,total in e.get(category,{}).items():
                    recorded=sum(r['amount'] for r in ledger if r['kind']==kind and r['key']==key)
                    if abs(total-recorded)>1e-6:ledger_errors.append({'category':category,'key':key,'cumulative':total,'source_recorded':recorded})
            differences={}
            for key,actual in row['stores'].items():
                initial=e['initial'].get(key,0);produced=e['produced'].get(key,0);imported=e['imports'].get(key,0);consumed=e['consumed'].get(key,0);lost=e['disposed'].get(key,0);expected=initial+produced+imported-consumed-lost;differences[key]=actual-expected
                balances.append({'seed':seed,'days':days,'pool':'stores','resource':key,'initial':initial,'produced':produced,'imported_recovered':imported,'consumed_used':consumed,'lost':lost,'expected':expected,'actual':actual,'difference':actual-expected})
            for key,actual in e['feedstock'].items():
                initial=e['feedstockInitial'].get(key,0);imported=e['feedstockImported'].get(key,0);used=e['feedstockUsed'].get(key,0);expected=initial+imported-used
                balances.append({'seed':seed,'days':days,'pool':'feedstock','resource':key,'initial':initial,'produced':0,'imported_recovered':imported,'consumed_used':used,'lost':0,'expected':expected,'actual':actual,'difference':actual-expected})
            daily_errors=[{'day':r['day'],'resources':r['resource_errors'],'frontier':r['frontier_errors'],'issues':r['issues']} for r in d['checkpoints'] if r['resource_errors'] or r['frontier_errors'] or r['issues']]
            audits[f'{seed}/{days}']={'daily_errors':daily_errors,'final_resource_errors':d['resource_audit'],'final_frontier_errors':d['frontier_audit'],'ledger_source_mismatches':ledger_errors,'source_rows':len(ledger),'stock_differences':differences,'extracted':d['resource_provenance']['extracted'],'credited':d['resource_provenance']['credited'],'lost':d['resource_provenance']['lost']}
            if ledger_errors or daily_errors:errors.append(f'Conservation/source audit failed: {seed}/{days}')
    for seed in seeds:
        path=root/f'voyage_seed_{seed}.json'
        if not path.exists():errors.append('Missing portable year-end save '+path.name);continue
        state=json.loads(path.read_text())['state'];domains={'destinations':[d['id'] for sy in state['universe']['systems'].values() for d in sy['bodies']],'frontier_jobs':[j['id'] for j in state['frontier']['jobs']],'legacy_jobs':[j['id'] for j in state['remoteCore']['director']['registry']],'journal':[r['id'] for r in state['chronicle']['records']]}
        duplicates={k:len(v)-len(set(v)) for k,v in domains.items()};known=set(domains['destinations']);lost_targets=[j['id'] for j in state['frontier']['jobs'] if j['destination'] not in known];integrity[str(seed)]={'duplicate_ids':duplicates,'lost_mission_destinations':lost_targets,'retained_journal_records':len(domains['journal']),'weekly_archives':len(state['archived'])}
        if any(duplicates.values()) or lost_targets:errors.append('Final identity graph failed '+str(seed))
        sc=state['remoteCore']['director']['science'];research[str(seed)]={'cases':len(sc['cases']),'experiment_outcomes':dict(collections.Counter(e['status'] for e in sc.get('experiments',[]))),'programs':len(sc.get('programs',[])),'lazarus':sc.get('lazarusProgram'),'conclusions':sc.get('conclusions',[])}
    (root/'identity_integrity.json').write_text(json.dumps(integrity,indent=2));(root/'research_outcomes.json').write_text(json.dumps(research,indent=2))
    for seed in seeds:
        path=root/f'voyage_seed_{seed}.json'
        if not path.exists():continue
        backup=json.loads(path.read_text());state=backup['state'];actors=state['entities'];ex=state['experiences'];ops=state['emergencyOps'];history={r['id']:r for r in backup.get('history',[])};source_ids=set(history)|{j['id'] for j in state['frontier']['jobs']}|{j['id'] for j in state['remoteCore']['director']['registry']}|{i['id'] for i in ops['incidents']};issues=[]
        if len({r['id'] for r in ex['records']})!=len(ex['records']):issues.append('Duplicate personal memory IDs')
        if len({r['id'] for r in actors['encounters']})!=len(actors['encounters']):issues.append('Duplicate encounter IDs')
        for m in ex['records']:
            if m['sourceId'] not in source_ids:issues.append('Unknown memory source '+m['id'])
        for week in state['chronicles']['weeks'].values():
            for source in week['sourceIds']:
                if source not in history:issues.append('Lost indexed chronicle source '+source)
            for card in week['segments']:
                if card['sourceId'] in history and card['message']!=history[card['sourceId']].get('message'):issues.append('Chronicle message differs from source '+card['sourceId'])
        encounter_ids={r['id'] for r in actors['encounters']};actor_audits={};ledger=list(state['economy']['ledger'].values())
        for n in actors['registry'].values():
            difference={k:n['initial'].get(k,0)+n['received'].get(k,0)-n['spent'].get(k,0)-v for k,v in n['stock'].items()}
            if any(v<-1e-7 for v in n['stock'].values()) or any(abs(v)>1e-6 for v in difference.values()) or any(i not in encounter_ids for i in n['history']):issues.append('Actor inventory/history '+n['id'])
            trades=[r for r in actors['encounters'] if r['entityId']==n['id'] and r['kind']=='trade'];trade_differences={}
            for key in ('fuel','waterIce','nutrients'):
                given=sum(r['amount'] for r in trades if r['key']==key);credited=sum(r['amount'] for r in ledger if r['kind']=='recover' and r['key']==key and r['source']=='trade from '+n['id']);trade_differences[key]=credited-given
            paid=sum(r['paidOre'] for r in trades);debited=sum(r['amount'] for r in ledger if r['kind']=='feedstock_use' and r['key']=='ore' and r['source']=='trade to '+n['id']);trade_differences['ore_payment']=debited-paid
            if any(abs(v)>1e-6 for v in trade_differences.values()):issues.append('Nonbilateral trade '+n['id'])
            actor_audits[n['id']]={'inventory_differences':difference,'trade_differences':trade_differences}
        active=[m for m in state['remoteCore']['missions'].values() if m];members=[name for m in active for name in m.get('members',[m['crew']]) if any(p['name']==name for p in state['crew'])]
        if len(members)!=len(set(members)):issues.append('Simultaneous crew assignment')
        sizes=dict(collections.Counter(str(len(j['members'])) for j in state['frontier']['jobs']));stage_records=sum(len(j.get('stageHistory',[])) for j in state['frontier']['jobs']);willingness={p['name']:max(.4,min(1.2,1+p['career']['confidence']*.01-p['career']['caution']*.015)) for p in state['crew']}
        living_metrics[str(seed)]={'simulated_event_kinds':dict(collections.Counter(r.get('kind') for r in history.values() if r.get('kind') not in ('crew_memory','encounter_history','mission_history'))),'entity_types':dict(collections.Counter(n['type'] for n in actors['registry'].values())),'contact_outcomes':actors['stats'],'actor_inventory_trade_audits':actor_audits,'expedition_team_sizes':sizes,'completed_stage_records':stage_records,'incident_outcomes':dict(collections.Counter(i.get('outcome',i['status']) for i in ops['incidents'])),'rescue_statistics':ops['stats'],'personal_memories':len(ex['records']),'mission_willingness':willingness,'indexed_history_records':len(history),'history_bytes':len(json.dumps(backup.get('history',[])).encode()),'source_graph_errors':issues}
        if issues:errors.append('Living frontier source/conservation graph failed '+str(seed))
        if not actors['encounters'] or not stage_records or not ex['records']:errors.append('Inactive new systems '+str(seed))
    if living_metrics and sum(v['rescue_statistics']['rescueAttempts'] for v in living_metrics.values())==0:errors.append('No naturally observed rescue operation demonstrated')
    if living_metrics and sum(v['contact_outcomes']['trades'] for v in living_metrics.values())==0:errors.append('No naturally observed bilateral trade demonstrated')
    (root/'living_frontier_audit.json').write_text(json.dumps(living_metrics,indent=2))
    for name,rows in [('campaign_statistics.csv',stats),('resource_balances.csv',balances)]:
        if rows:
            with (root/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (root/'conservation_audit.json').write_text(json.dumps(audits,indent=2))
    automated={}
    unit_path=root/'unit_results.txt'
    if unit_path.exists():
        unit=unit_path.read_text();counts={k:int(re.search(r'ℹ '+k+r' (\d+)',unit).group(1)) for k in ('tests','pass','fail','skipped')};automated['unit']=counts
        if counts['fail'] or counts['skipped'] or counts['tests']!=counts['pass']:errors.append('Unit suite not fully passing')
    else:errors.append('Missing unit_results.txt')
    for name in ('living_integration.json','bridge_results.json','legacy_runner_7day.json','v12_upgrade.json','backup_roundtrip.json','adverse_campaigns.json','syntax_checks.json'):
        path=root/name
        if not path.exists():errors.append('Missing '+name);continue
        result=json.loads(path.read_text());automated[name]={'passed':result.get('passed'),'tests':result.get('tests_run',result.get('tests'))}
        if not result.get('passed'):errors.append('Failed '+name)
    source=Path(__file__).resolve().parent;runtime={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((source/'web').rglob('*')) if p.is_file()}
    summary={'version':'1.3','source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip(),'runtime_sha256':runtime,'campaign_seeds':seeds,'natural_living_systems_active':bool(living_metrics),'milestones':milestones,'acceptance_verified':not errors,'automated_tests':automated,'errors':errors,'test_reports':['unit_results.txt','living_integration.json','bridge_results.json','legacy_runner_7day.json','v12_upgrade.json','backup_roundtrip.json','adverse_campaigns.json','syntax_checks.json'],'limitations':'See KNOWN_LIMITATIONS_v1.2.md. Test reports are authoritative for their individual results; physical devices and non-Chromium browsers were not tested.'}
    (root/'validation_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps({'milestones':len(milestones),'passed':not errors,'errors':errors},indent=2));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
