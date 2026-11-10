"""Audit actual accelerated campaign artifacts; no simulated outcomes are synthesized."""
import argparse,collections,hashlib,json,re
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('campaigns',type=Path);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();result={'campaigns':{},'passed':True}
 for folder in sorted(a.campaigns.iterdir()):
  p=next(folder.glob('campaign_*.json'));c=json.loads(p.read_text());assert c['passed'],(folder,c['errors']);seed=c['seed'];day=c['real_days'];backup=folder/f'backup_{seed}_{day}.json';b=json.loads(backup.read_text());s=b['state'];history=b['history'];by={r['id']:r for r in history};last=c['daily'][-1];films=list(s['cinema']['films'].values());errors=[]
  names=[p['name'] for p in s['crew']]+[p['name'] for p in s['living']['deceased']]
  if len(names)!=20 or len(set(names))!=20:errors.append('Crew identity loss/duplication')
  for w in s['chronicles']['weeks'].values():
   for sid in w['sourceIds']:
    if sid not in by or by[sid].get('data',{}).get('privateKnowledge'):errors.append('Private/missing public chronicle source '+sid)
  for x in s['solVoice']['entries']:
   if x['sourceId'] not in by or by[x['sourceId']].get('data',{}).get('privateKnowledge'):errors.append('Missing/private SOL source '+x['sourceId'])
  for person in s['crewLife']['people'].values():
   for m in person['memories']:
    if m['sourceId'] not in by:errors.append('Missing interaction memory source')
  for f in films:
   for x in f['segments']:
    if x['kind']=='highlight' and any(sid not in by or by[sid].get('data',{}).get('privateKnowledge') for sid in x['sourceIds']):errors.append('Private/missing film source')
    if x.get('frame'):
     v=x['frame'];r=by[x['sourceIds'][0]];d=r.get('data',{});sid=d.get('observedSourceId',r['id']);at=d.get('observedAt',r['minute']-480)
     if sid not in v['sourceIds'] or v['at']!=at or not all(p['node']=='R:'+v['room'] for p in v['actors']):errors.append('Invalid saved frame provenance')
  realdeaths=[r for r in history if r['kind']=='death' and not r.get('data',{}).get('knowledgeDelivery')];death_details=[]
  for r in realdeaths:
   nearby=[x for x in history if x['minute']<=r['minute'] and x['minute']>=r['minute']-180 and set(x.get('people',[]))&set(r.get('people',[])) and x['kind'] in ['injury','medical','emergency','encounter','rescue','mission','death'] and not x.get('data',{}).get('knowledgeDelivery')]
   death_details.append({'death':r,'causal_window':nearby[-30:]})
  originals=[r for r in history if not r.get('data',{}).get('knowledgeDelivery')];kinds=collections.Counter(r['kind'] for r in originals);sc=s['remoteCore']['director']['science'];experiments=sc.get('experiments',[]);normalized=collections.Counter(re.sub(r'\b\d+(?:\.\d+)?\b','N',r['message']) for r in originals if r['kind']=='social')
  row={'passed':not errors,'seed':seed,'scenario':c['scenario'],'real_days':day,'sim_days':s['tick']/1440,'alive':len(s['crew']),'dead':last['dead'],'arrivals':last['arrivals'],'field_missions':len(s['remoteCore']['director']['registry']),'local_jobs':len(s['frontier']['jobs']),'science_cases':len(sc['cases']),'experiment_statuses':dict(collections.Counter(e['status'] for e in experiments)),'confirmed_conclusions':sum(x.get('status')=='confirmed' for x in sc.get('conclusions',[])),'conversations':s['crewLife']['conversations'],'retained_visual_frames':len(s['cinema']['recordings']),'captured_state_frames':s['cinema']['framesCaptured'],'weekly_films':len(films),'film_durations_seconds':[f['duration'] for f in films],'film_recorded_segments':sum(bool(x.get('frame')) for f in films for x in f['segments']),'film_legendary_segments':sum(x['kind']=='legendary' for f in films for x in f['segments']),'public_source_audit_errors':errors,'history_records':len(history),'source_kind_counts':dict(kinds),'most_repeated_social_text':normalized.most_common(5),'death_details':death_details,'resources':last['stores'],'resource_acquisition':last['acquired'],'travel_fuel':last['travel_fuel'],'storage_first':c['daily'][0]['storage'],'storage_last':last['storage'],'snapshot_bytes_first':c['daily'][0]['snapshot_bytes'],'snapshot_bytes_last':last['snapshot_bytes'],'checkpoints':c['checkpoints'],'backup_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'runtime_sha256':c['runtime_sha256'],'elapsed_seconds':c['elapsed_seconds']}
  if last['arrivals']<=0:row['passed']=False;errors.append('No actual travel')
  result['campaigns'][folder.name]=row;result['passed']&=row['passed']
 a.output.write_text(json.dumps(result,indent=2));print(json.dumps({k:{x:v[x] for x in ['passed','sim_days','alive','dead','arrivals','conversations','weekly_films','public_source_audit_errors']} for k,v in result['campaigns'].items()},indent=2));return not result['passed']
if __name__=='__main__':raise SystemExit(main())
