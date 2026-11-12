"""Independent audit of retained full-history campaign artifacts. No outcomes are synthesized."""
import argparse,collections,hashlib,json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('campaigns',type=Path);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();out={'passed':True,'campaigns':{}}
 for folder in sorted(args.campaigns.iterdir()):
  path=next(folder.glob('campaign_*.json'));c=json.loads(path.read_text());assert c['status']=='finished' and c['passed'],(folder,c['status'],c['errors']);seed=c['seed'];days=c['real_days'];backup=folder/f'backup_{seed}_{days}.json';b=json.loads(backup.read_text());s=b['state'];history=b['history'];by={r['id']:r for r in history};errors=[];last=c['daily'][-1]
  names=[p['name'] for p in s['crew']]+[p['name'] for p in s['living']['deceased']]
  if len(names)!=20 or len(set(names))!=20:errors.append('Lost or duplicated crew identity')
  for w in s['chronicles']['weeks'].values():
   for sid in w['sourceIds']:
    if sid not in by or by[sid].get('data',{}).get('privateKnowledge'):errors.append('Private/missing public chronicle source '+sid)
  for voice in s['solVoice']['entries']:
   r=by.get(voice['sourceId']);
   if not r or r.get('data',{}).get('privateKnowledge'):errors.append('Missing/private SOL source '+voice['sourceId'])
  for film in s['cinema']['films'].values():
   for segment in film['segments']:
    if segment['kind'] not in ['highlight','award','legendary']:continue
    for sid in segment['sourceIds']:
     if sid not in by or by[sid].get('data',{}).get('privateKnowledge'):errors.append('Missing/private cinematic source '+sid)
  experience_sources={r['sourceId'] for r in s['experiences']['records']}
  for name,person in s['crewSocial']['people'].items():
   if len(person['memories'])>32:errors.append('Unbounded social memory '+name)
   for memory in person['memories']:
    if memory['sourceId'] not in by and memory['sourceId'] not in experience_sources:errors.append('Unsourced social memory '+name)
  for name,person in s['crewLife']['people'].items():
   if len(person.get('activityHistory',[]))>16:errors.append('Unbounded activity history '+name)
   for memory in person['memories']:
    if memory['sourceId'] not in by:errors.append('Missing conversation source '+name)
  for fid in s['knowledge']['actors']['SOL']['entries']:
   if s['knowledge']['facts'][fid]['disclosure']=='private':errors.append('Private fact leaked to SOL '+fid)
  originals=[r for r in history if not r.get('data',{}).get('knowledgeDelivery')];activities=collections.Counter(r.get('data',{}).get('activity') for r in originals if r.get('data',{}).get('activity'));kinds=collections.Counter(r['kind'] for r in originals)
  for daily in c['daily']:
   for key in ['resource_errors','frontier_errors','chronicle_errors','knowledge_errors','creature_errors','cinematic_errors']:
    errors.extend(daily.get(key,[]))
  for checkpoint in c['checkpoints']:
   if not checkpoint['exact_reload']:errors.append('Checkpoint mismatch')
  row={'passed':not errors,'seed':seed,'scenario':c['scenario'],'real_days':days,'ship_days':s['tick']/1440,'ticks':s['tick'],'episode':s['episode'],'alive':len(s['crew']),'deaths':last['dead'],'arrivals':last['arrivals'],'field_missions':len(s['remoteCore']['director']['registry']),'science_cases':len(s['remoteCore']['director']['science']['cases']),'conversations':s['crewLife']['conversations'],'source_activities':dict(activities),'source_kinds':dict(kinds),'retained_social':last['livingShip'],'weekly_films':len(s['cinema']['films']),'legendary_segments':sum(x['kind']=='legendary' for f in s['cinema']['films'].values() for x in f['segments']),'maintenance_statistics':s.get('repairControl',{}),'resources_final':last['stores'],'acquisition':last['acquired'],'fuel_used':last['travel_fuel'],'history_records':len(history),'snapshot_bytes_first':c['daily'][0]['snapshot_bytes'],'snapshot_bytes_last':last['snapshot_bytes'],'checkpoint_reload_days':[p['real_day'] for p in c['checkpoints'] if p['exact_reload']],'audit_errors':errors,'simulation_errors':c['errors'],'backup_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'source_commit':c['source_commit'],'elapsed_seconds':c['elapsed_seconds'],'evidence_note':'Only actual campaign results. No generated extra crew; romances/claims need not occur. Checkpoint time is measured using unchanged production calendar including synchronized holidays.'}
  out['campaigns'][folder.name]=row;out['passed']&=row['passed']
 args.output.write_text(json.dumps(out,indent=2));print(json.dumps({name:{k:row[k] for k in ['passed','real_days','ship_days','alive','deaths','arrivals','conversations','weekly_films','audit_errors']} for name,row in out['campaigns'].items()},indent=2));return not out['passed']
if __name__=='__main__':raise SystemExit(main())
