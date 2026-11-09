"""Audit actual core campaigns and summarize diversity without treating uptime as content quality."""
import argparse,collections,csv,hashlib,json,math,re,statistics,subprocess
from pathlib import Path

def load(p):return json.loads(p.read_text())
def distribution(arcs,now):
    durations=sorted((a.get('ended',now)-a['started'])/1440 for a in arcs)
    return {'count':len(arcs),'categories':dict(collections.Counter(a['category'] for a in arcs)),'outcomes':dict(collections.Counter(a.get('outcome','open') for a in arcs)),'duration_days':{'median':statistics.median(durations) if durations else 0,'p95':durations[min(len(durations)-1,math.floor(len(durations)*.95))] if durations else 0,'maximum':max(durations,default=0)},'multi_day':sum(d>=1 for d in durations),'at_least_week':sum(d>=7 for d in durations),'crossed_episode_boundary':sum((a['started']+480)//10080!=(a.get('ended',now)+480)//10080 for a in arcs)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);args=ap.parse_args();r=args.directory;rows=[];errors=[];diversity={};audits={};science={};examples={};resource_rows=[]
    for seed in (1001,2026):
        for day in (30,90,365):
            d=load(r/f'seed_{seed}_{day}day.json');a=d['anthology'];arcs=a['arcs'];ext=[x for x in arcs if 'signalHour'in x];stats=distribution(arcs,day*1440)
            if not d['passed'] or d['errors'] or d['resource_audit'] or d['frontier_audit']:errors.append(f'{seed}/{day} report/audit failure')
            if d['universe_statistics']['systems']!=2 or d['universe_statistics']['known_destinations']!=6:errors.append(f'{seed}/{day} core context grew')
            if len(d['crew_outcomes']['survivors'])+len(d['crew_outcomes']['deceased'])!=20:errors.append(f'{seed}/{day} crew census')
            rows.append({'seed':seed,'days':day,'stories':len(arcs),'external_encounters':len(ext),'category_count':len(stats['categories']),'overlap_max':a['maxOverlap'],'multi_day':stats['multi_day'],'at_least_week':stats['at_least_week'],'shared_moments':sum(x.get('outcome')=='shared_moment' for x in arcs),'traditions':len(a['traditions']),'systems':d['universe_statistics']['systems'],'known_venues':d['universe_statistics']['known_destinations'],'survivors':len(d['crew_outcomes']['survivors']),'deaths':len(d['crew_outcomes']['deceased']),'science_cases':len(d['science']['cases']),'experiments':len(d['science']['experiments']),'snapshot_bytes':d['persistence']['state_bytes'],'reload_seconds':d['persistence']['reload_seconds'],'indexeddb_bytes':d['durable']['estimate']['usage']})
            e=d['resource_balances'];ledger=collections.defaultdict(float)
            for item in e['ledger'].values():ledger[(item['kind'],item['key'])]+=item['amount']
            ea=[]
            for name,kind in [('produced','produce'),('consumed','consume'),('disposed','loss'),('feedstockImported','recover'),('feedstockUsed','feedstock_use')]:
                for key,n in e[name].items():
                    actual=ledger[(kind,key)]
                    if abs(actual-n)>1e-5:ea.append(f'{name}/{key}: aggregate ledger differs by {actual-n}')
            for key,n in e['feedstock'].items():
                expected=e['feedstockInitial'].get(key,0)+e['feedstockImported'].get(key,0)-e['feedstockUsed'].get(key,0);resource_rows.append({'seed':seed,'day':day,'pool':'feedstock','resource':key,'initial':e['feedstockInitial'].get(key,0),'incoming':e['feedstockImported'].get(key,0),'used':e['feedstockUsed'].get(key,0),'remaining':n,'difference':expected-n})
                if abs(expected-n)>1e-5 or n<0:ea.append('Feed balance '+key)
            audits[f'{seed}/{day}']={'errors':ea,'runtime_audit':d['resource_audit'],'ledger_sources':len(e['ledger']),'frozen_systems':d['universe_statistics']['systems']}
            errors.extend(f'{seed}/{day}: '+x for x in ea)
        backup=load(r/f'voyage_seed_{seed}.json');s=backup['state'];history={x['id']:x for x in backup['history']};a=s['anthology'];arc_errors=[];history_ids=set(history)
        if len(history)!=len(backup['history']):arc_errors.append('Duplicate indexed history IDs')
        known=set(history)|{j['id'] for j in s['frontier']['jobs']}|{j['id'] for j in s['remoteCore']['director']['registry']}|{i['id'] for i in s['emergencyOps']['incidents']}
        for x in a['arcs']:
            if not set(x['sources'])<=history_ids:arc_errors.append('Missing arc sources '+x['id'])
            for h in x['history']:
                if history.get(h['sourceId'],{}).get('message')!=h['text']:arc_errors.append('Reconstruction text mismatch '+x['id'])
        for m in s['experiences']['records']:
            if m['sourceId'] not in known:arc_errors.append('Orphan memory '+m['id'])
        for n in s['entities']['registry'].values():
            for key,stock in n['stock'].items():
                if stock<0 or abs(n['initial'].get(key,0)+n['received'].get(key,0)-n['spent'].get(key,0)-stock)>1e-6:arc_errors.append('Actor inventory '+n['id'])
        for w in s['chronicles']['weeks'].values():
            if not set(w['sourceIds'])<=history_ids:arc_errors.append('Weekly source missing '+str(w['episode']))
            for card in w['segments']:
                if history.get(card['sourceId'],{}).get('message')!=card['message']:arc_errors.append('Weekly invented text '+card['sourceId'])
        ext=[x for x in a['arcs'] if 'signalHour'in x];extdist=distribution(ext,s['tick']);allstats=distribution(a['arcs'],s['tick'])
        if len(extdist['categories'])<6:arc_errors.append('Insufficient actual external variety')
        if not allstats['at_least_week'] or a['maxOverlap']<2:arc_errors.append('No actual long/overlapping threads')
        if not any(x.get('outcome')=='shared_moment' for x in ext):arc_errors.append('No actual positive external consequence')
        diversity[str(seed)]={'all_stories':allstats,'external_encounters':extdist,'max_overlap':a['maxOverlap'],'traditions':a['traditions'],'linked_followups':sum(bool(x.get('links')) for x in a['arcs']),'memories':len(s['experiences']['records']),'shared_moment_memories':sum(x['kind']=='shared_moment' for x in s['experiences']['records']),'persistent_actors':len(s['entities']['registry']),'history_records':len(history),'weekly_tones':dict(collections.Counter(max(w.get('tones',{}),key=w['tones'].get) if w.get('tones') else 'quiet' for w in s['chronicles']['weeks'].values())),'source_graph_errors':arc_errors}
        examples[str(seed)]={}
        for category in extdist['categories']:
            x=next(x for x in ext if x['category']==category and x.get('ended')) if any(x['category']==category and x.get('ended') for x in ext) else next(x for x in ext if x['category']==category)
            examples[str(seed)][category]=x
        sc=s['remoteCore']['director']['science'];science[str(seed)]={'cases':len(sc['cases']),'programs':len(sc['programs']),'experiments':dict(collections.Counter(e['status'] for e in sc['experiments'])),'conclusions':sc['conclusions'],'lazarus':sc.get('lazarusProgram'),'research_story_outcomes':dict(collections.Counter(x.get('outcome','open') for x in a['arcs'] if x['kind']=='research'))}
        errors.extend(f'{seed}: '+x for x in arc_errors)
    tests={};unit=(r/'unit_results.txt').read_text();counts={key:int(re.search(r'ℹ '+key+r' (\d+)',unit).group(1)) for key in ('tests','pass','fail','skipped')};tests['unit']=counts
    if counts['fail'] or counts['skipped'] or counts['tests']!=counts['pass']:errors.append('Unit suite failure/skip')
    for name in ['core_integration.json','compatibility_integration.json','bridge_results.json','syntax_checks.json','backup_roundtrip.json']:
        d=load(r/name);tests[name]={'passed':d['passed'],'count':d.get('tests_run',d.get('tests'))}
        if not d['passed']:errors.append('Failed '+name)
    variants={}
    for name in ('quiet','busy'):
        p=r/name/'seed_3303_30day.json';d=load(p);ext=[x for x in d['anthology']['arcs'] if 'signalHour'in x];variants[name]={'passed':d['passed'],'frequency':d['anthology']['config']['frequency'],'external':distribution(ext,43200),'crew_stories':len(d['anthology']['arcs'])-len(ext),'operational_contacts':d['living_frontier']['entities']['stats']['contacts']}
        if not d['passed']:errors.append('Failed frequency variant '+name)
    if variants['quiet']['external']['count'] or variants['busy']['external']['count']<=variants['quiet']['external']['count']:errors.append('Frequency variation not demonstrated')
    for name,obj in [('story_diversity.json',diversity),('story_examples.json',examples),('resource_conservation.json',audits),('science_lazarus.json',science),('frequency_variants.json',variants)]:
        (r/name).write_text(json.dumps(obj,indent=2))
    for name,data in [('campaign_statistics.csv',rows),('resource_balances.csv',resource_rows)]:
        with (r/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    src=Path(__file__).resolve().parent;provenance=load(r/'campaign_source.json');current={str(p.relative_to(src)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((src/'web').rglob('*')) if p.is_file()}
    if current!=provenance['runtime_sha256']:errors.append('Packaged runtime differs from frozen accepted campaign source')
    viability={str(seed):{'survivors_at_365':next(x['survivors'] for x in rows if x['seed']==seed and x['days']==365),'all_founders_accounted_for':True} for seed in (1001,2026)};viability_issues=[f'Seed {seed} has no surviving crew at day 365: long-term autonomous recovery/balance remains unresolved' for seed,v in viability.items() if not v['survivors_at_365']]
    summary={'version':'1.4','source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=src,text=True).strip(),'campaign_source_commit':provenance['source_commit'],'runtime_sha256':current,'mechanical_checks_passed':not errors,'autonomous_viability':viability,'acceptance_verified':not errors and not viability_issues,'unresolved_viability_issues':viability_issues,'final_release_ready':False,'automated_tests':tests,'milestones':rows,'errors':errors,'quality_gate':'Actual diversity, source links, positive consequences, overlap and multiweek threads are audited; long-form human review, content depth and visual/audio polish still remain. See FINAL_RELEASE_ROADMAP.md.'};(r/'validation_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps({'mechanical_checks_passed':not errors,'acceptance_verified':summary['acceptance_verified'],'errors':errors,'unresolved_viability_issues':viability_issues,'milestones':len(rows)},indent=2));return bool(errors or viability_issues)
if __name__=='__main__':raise SystemExit(main())
