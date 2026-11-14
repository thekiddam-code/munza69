"""Independent expedition source, custody, bounded-state and conservation audit of actual artifacts."""
import argparse,json,subprocess,sys
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('campaigns',type=Path);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 subprocess.run([sys.executable,str(Path(__file__).with_name('summarize_operations.py')),str(a.campaigns),'--output',str(a.output)],check=True)
 report=json.loads(a.output.read_text())
 for name,row in report['campaigns'].items():
  folder=a.campaigns/name;c=json.loads(next(folder.glob('campaign_*.json')).read_text());b=json.loads((folder/f'backup_{c["seed"]}_{c["real_days"]}.json').read_text());s=b['state'];by={r['id']:r for r in b['history']};errors=row['audit_errors'];ev=s['fieldEvidence'];ops=s['expeditionOperations'];rooms=s['asteroidExploration']['rooms']
  for d in c['daily']:errors.extend(d['phase44']['errors'])
  if len(ev['archive'])>64 or len(ev['devices'])>32 or len(ops['history'])>40:errors.append('Unbounded expedition state')
  for clip in ev['archive']:
   source=by.get(clip['sourceId'])
   if not source or source.get('data',{}).get('privateKnowledge'):errors.append('Missing/private received field-record source '+clip['id'])
   if not clip.get('originalSourceId') or clip['originalSourceId'] not in by:errors.append('Missing original field-record source '+clip['id'])
   if 'no recorded video' not in clip['recordingAvailability']:errors.append('Unlabeled reconstruction '+clip['id'])
   if len(clip['frames'])>6:errors.append('Unbounded field clip '+clip['id'])
   for frame in clip['frames']:
    if frame['tick']>s['tick']:errors.append('Future field snapshot '+clip['id'])
    if any(p['name']==clip['carrier'] for p in frame['view']['actors']):errors.append('Body camera sees its own wearer '+clip['id'])
  for d in ev['devices'].values():
   if len(d['clips'])>12 or len(d['ring'])>3:errors.append('Unbounded device '+d['id'])
  utilities=[]
  for r in rooms:
   u=r['field'].get('utility')
   if not u:continue
   if abs(u['battery']+u.get('totalDrawn',0)-u.get('totalTransferred',0))>1e-6:errors.append('Unaccounted utility power '+str(r['id']))
   utilities.append({'cell':r['id'],**u})
  if not s['unifiedWorld']['organisms']['XENO-INITIAL']['dormant'] or s['unifiedWorld']['military']['doors']['23']!='sealed':errors.append('Unrequested containment activation')
  row['expeditions']={'history':ops['history'],'visited':[{'id':r['id'],'kind':r['field']['kind']} for r in rooms if r['visited']],'records_received':len(ev['archive']),'frames_received':sum(len(x['frames']) for x in ev['archive']),'devices':list(ev['devices'].values()),'utilities':utilities,'suits':s['teamLog'].get('fieldSuits',{}),'ledger':[v for v in s['economy']['ledger'].values() if any(t in v['source'].lower() for t in ['cargo','expedition','recovered bulk'])],'military_visited':s['unifiedWorld']['military']['visited'],'dormant':s['unifiedWorld']['organisms']['XENO-INITIAL']['dormant']}
  row['passed']=not errors and not c['errors'];report['passed']&=row['passed']
 a.output.write_text(json.dumps(report,indent=2));print(json.dumps({n:{'passed':r['passed'],'arrivals':r['arrivals'],'sorties':len(r['expeditions']['history']),'records':r['expeditions']['records_received'],'errors':r['audit_errors']} for n,r in report['campaigns'].items()},indent=2));return not report['passed']
if __name__=='__main__':raise SystemExit(main())
