"""Summarize actual continuing campaigns; never manufacture missing passes."""
import argparse, collections, csv, hashlib, json, re, subprocess
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);ap.add_argument('--seeds',default='1001,2026');args=ap.parse_args();root=args.directory;seeds=[int(x) for x in args.seeds.split(',')];stats=[];balances=[];audits={};errors=[];milestones=[]
    for seed in seeds:
        for days in (7,30,90,180,365):
            path=root/f'seed_{seed}_{days}day.json'
            if not path.exists():errors.append(f'Missing {path.name}');continue
            d=json.loads(path.read_text());row=d['checkpoints'][-1];jobs=collections.Counter(j['type'] for j in d['missions']);nav=d['navigation'];e=d['resource_balances'];milestones.append({'seed':seed,'days':days,'passed':d['passed'],'errors':d['errors']})
            if not d['passed']:errors.append(f'{path.name}: {d["errors"]}')
            stats.append({'seed':seed,'days':days,'minutes':row['tick'],'weekly_archives':row['archives'],'arrivals':nav['arrivals'],'visited':d['universe_statistics']['visited'],'known_destinations':d['universe_statistics']['known_destinations'],'systems':row['systems'],'frontier_jobs':len(d['missions']),'completed':d['frontier_statistics']['completed'],'failed':d['frontier_statistics']['failed'],'mission_types':json.dumps(dict(jobs),sort_keys=True),'natural_frontier_samples':d['frontier_statistics']['samples'],'science_cases':d['science']['cases'],'experiments':d['science']['experiments'],'confirmed_families':len(d['science']['conclusions']),'survivors':len(d['crew_outcomes']['survivors']),'deceased':len(d['crew_outcomes']['deceased']),'travel_fuel':nav['fuelUsed'],'remaining_fuel':e['feedstock']['fuel'],'acquired':json.dumps(d['resource_provenance']['credited'],sort_keys=True),'event_diversity':len(d['frontier_statistics']['eventKinds']),'events':json.dumps(d['frontier_statistics']['eventKinds'],sort_keys=True),'logical_save_bytes':d['persistence']['state_bytes'],'physical_core_slots_bytes':d['persistence']['storage']['physical_bytes'],'save_mismatches':len(d['persistence']['mismatched_fields'])})
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
    for name in ('frontier_integration.json','bridge_results.json','legacy_runner_7day.json'):
        path=root/name
        if not path.exists():errors.append('Missing '+name);continue
        result=json.loads(path.read_text());automated[name]={'passed':result.get('passed'),'tests':result.get('tests_run',result.get('tests'))}
        if not result.get('passed'):errors.append('Failed '+name)
    source=Path(__file__).resolve().parent;runtime={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((source/'web').rglob('*')) if p.is_file()}
    summary={'version':'1.2','source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip(),'runtime_sha256':runtime,'campaign_seeds':seeds,'milestones':milestones,'acceptance_verified':not errors,'automated_tests':automated,'errors':errors,'test_reports':['unit_results.txt','frontier_integration.json','bridge_results.json','legacy_runner_7day.json'],'limitations':'See KNOWN_LIMITATIONS_v1.2.md. Test reports are authoritative for their individual results; physical devices and non-Chromium browsers were not tested.'}
    (root/'validation_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps({'milestones':len(milestones),'passed':not errors,'errors':errors},indent=2));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
