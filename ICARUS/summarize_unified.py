"""Audit actual wall-calendar campaigns and source-backed state; expose incomplete design scope."""
import argparse,collections,hashlib,json,re,subprocess
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('reports',type=Path);args=ap.parse_args();r=args.reports;errors=[];campaigns=[]
    for seed in (1001,2026):
        d=json.loads((r/'campaigns'/f'campaign_{seed}.json').read_text());s=json.loads((r/'campaigns'/f'snapshot_{seed}_30.json').read_text());history=json.loads((r/'campaigns'/f'history_{seed}_30.json').read_text());ids={x['id']:x for x in history};cal=s['calendar'];w=s['unifiedWorld'];expected={'2026-10-31','2026-11-11','2026-11-26'}
        issues=[]
        if not d['passed'] or d['errors'] or len(d['daily'])!=30:issues.append('Campaign runtime failure')
        if s['tick']!=160920:issues.append('Incorrect integrated physical time across holiday window')
        if s['episode']!=5 or len(s['archived'])!=4:issues.append('Incorrect real Monday boundaries')
        if {v['date'] for v in cal['occurrences'].values()}!=expected or len(cal['occurrences'])!=3:issues.append('Missing/duplicate holiday occurrence')
        if cal['recovery']['discardedMs'] or cal['recovery']['rollbackCount']:issues.append('Unexpected suspension or rollback')
        if any(not x['exact_reload'] for x in d['checkpoints']):issues.append('Checkpoint state mismatch')
        if len(s['crew'])+len(s['living']['deceased'])!=20:issues.append('Missing founder')
        if s['resourceAudit'] or s['frontierAudit']:issues.append('Conservation/navigation error')
        if len(ids)!=len(history):issues.append('Duplicate source ID')
        for a in s['anthology']['arcs']:
            if not set(a['sources'])<=set(ids):issues.append('Missing story source '+a['id'])
            for h in a['history']:
                if ids.get(h['sourceId'],{}).get('message')!=h['text']:issues.append('Invented story transition '+a['id'])
        for week in s['chronicles']['weeks'].values():
            for card in week['segments']:
                if ids.get(card['sourceId'],{}).get('message')!=card['message']:issues.append('Invented chronicle card')
        for a in w['archives']:
            if a['sourceId'] not in ids:issues.append('Acquired lore without recorded source')
        for i in w['items'].values():
            for h in i['history']:
                if h['sourceId'] not in ids:issues.append('Object transfer without source')
        for o in w['organisms'].values():
            if o['stage']=='adult' and o['id']!='XENO-INITIAL' and o.get('host') not in w['infections']:issues.append('Adult without causal host')
        categories=dict(collections.Counter(x['category'] for x in s['anthology']['arcs']));stats={'seed':seed,'real_days':30,'simulation_minutes':s['tick'],'simulation_days':s['tick']/1440,'episodes':s['episode'],'survivors':len(s['crew']),'deaths':s['living']['deceased'],'stories':len(s['anthology']['arcs']),'categories':categories,'history_records':len(history),'holidays':list(cal['occurrences'].values()),'acquired_records':len(w['archives']),'military_visited':w['military']['visited'],'military_power_remaining':w['military']['reservePower'],'organisms':w['organisms'],'maintenance':s['repairControl']['stats'],'checkpoints':d['checkpoints'],'errors':issues};campaigns.append(stats);errors.extend(str(seed)+': '+x for x in issues)
    tests={}
    unit=(r/'units_final.txt').read_text();counts={k:int(re.search(r'ℹ '+k+r' (\d+)',unit).group(1)) for k in ['tests','pass','fail','skipped']};tests['unit']=counts
    if counts['fail'] or counts['skipped']:errors.append('Node unit failure/skip')
    for name in ['unified_browser_frozen.json','stability_browser.json','compatibility.json','adverse.json','bridge.json','production_clock.json','syntax.json','backup_roundtrip.json']:
        d=json.loads((r/name).read_text());tests[name]={'passed':d['passed'],'count':d.get('tests_run',d.get('tests'))}
        if not d['passed']:errors.append('Failed '+name)
    source=Path(__file__).resolve().parent;frozen=json.loads((r/'runtime_source.json').read_text());now={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (source/'web').rglob('*') if p.is_file()}
    if frozen['runtime_sha256']!=now:errors.append('Tested runtime differs from delivery')
    summary={'version':'1.5.0-phase1','source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip(),'campaign_source_commit':frozen['source_commit'],'runtime_sha256':now,'verified_implemented_scope':not errors,'complete_uploaded_specification':False,'final_release_ready':False,'tests':tests,'campaigns':campaigns,'errors':errors,'incomplete_scope':['Full creature autonomy/ecology and visual variants','Natural body/prosthetic/wheelchair animation and artwork','Exact astronomical ephemeris','Authored personal cultural content and automatic religious calendar conversion','Unified radio delivery/individual knowledge across legacy views','Complete prop physics and persistent resized widget dimensions','Full cross-environment geometry consolidation and final interface polish','Physical device, multi-tab, network failure and human UX/content verification']};(r/'validation_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps({'verified_implemented_scope':not errors,'complete_uploaded_specification':False,'errors':errors},indent=2));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
