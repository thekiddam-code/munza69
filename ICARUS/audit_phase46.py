"""Independent exported-state/provenance audit; never mutates a world."""
import argparse,base64,hashlib,json,subprocess
from pathlib import Path

def audit(path):
 s=json.loads(path.read_text());history=json.loads(path.with_name(path.name.replace('snapshot_','history_')).read_text());ids={r['id'] for r in history};o=s['droneOperations'];errors=[]
 def check(ok,message):
  if not ok:errors.append(message)
 check(len(o['drones'])<=2 and len(o['archive'])<=24 and len(o['history'])<=40,'Working set bounds')
 for d in o['drones'].values():
  check(abs(d['charged']-d['used']-d['battery'])<1e-6,'Battery conservation '+d['id']);check(0<=d['battery']<=100,'Battery range');check(len(d['ring'])<=3 and len(d['clips'])<=8,'Local recorder bounds')
  if d.get('edge'):
   e=d['edge'];check(d['node']==e['from'] and 0<=e['elapsed']<=e['duration'],'Physical segment progress')
 for m in o['known'].values():check(m['sourceId'] in ids and m['observedAt']<=m['receivedAt']<=s['tick'],'Map source/timestamps')
 check(len({c['id'] for c in o['archive']})==len(o['archive']),'Duplicate received record IDs')
 images=0
 for c in o['archive']:
  check(c['sourceId'] in ids,'Recording receipt source');check(c['at']<=c['receivedAt']<=s['tick'],'Record receipt order');check(1<=len(c['frames'])<=5,'Record frame bound')
  for f in c['frames']:
   check(c['at']-2<=f['tick']<=c['at']+2,'Event pre/post duration');check(f['location']==f['view']['location'],'Actual captured sector')
   if f.get('image'):
    raw=base64.b64decode(f['image'].split(',',1)[1],validate=True);check(raw.startswith(b'\x89PNG\r\n\x1a\n'),'Captured PNG signature');images+=1
 # Independently account the same finite ship pools, without calling JS audit code.
 eco=s['economy'];actual={k:0 for k in ['food','water','oxygen','energy','medical','spares','tools','lab']}
 pools=[eco['stock'],s['operations']['reserve'],s['world']['interactions']['supplies'],{'medical':s['world']['tissueRepair']['cartridges']}]+[m.get('cargo',{}) for m in s['missions'].values() if m]
 for pool in pools:
  for k in actual:actual[k]+=pool.get(k,0)
 for k,value in actual.items():
  expected=sum(eco.get(n,{}).get(k,0) for n in ['initial','produced','imports'])-sum(eco.get(n,{}).get(k,0) for n in ['consumed','disposed']);check(value>=-1e-7 and abs(expected-value)<1e-6,'Resource conservation '+k)
 check(s['unifiedWorld']['military']['doors']['23']=='sealed','Initial military seal');check(s['unifiedWorld']['organisms']['XENO-INITIAL']['dormant'],'Initial dormant organism')
 check(not any(s.get(k) for k in ['droneAudit','resourceAudit','knowledgeAudit','creatureAudit','transitAudit','systemsAudit','gravityAudit']),'Engine reported audit errors')
 return {'snapshot':path.name,'passed':not errors,'errors':errors,'tick':s['tick'],'episode':s['episode'],'crew':len(s['crew']),'drones':len(o['drones']),'completed_drone_missions':len(o['history']),'received_sectors':len(o['known']),'received_records':len(o['archive']),'received_frame_images':images,'battery':[{k:d[k] for k in ['id','charged','used','battery','condition','missions']} for d in o['drones'].values()],'independent_resource_totals':actual,'history_records':len(history),'snapshot_bytes':path.stat().st_size}

def main():
 p=argparse.ArgumentParser();p.add_argument('--campaigns',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args();results=[audit(x) for x in sorted(a.campaigns.glob('*/snapshot_*.json'))];assert results,'No actual snapshots';r={'passed':all(x['passed'] for x in results),'campaigns':results};a.report.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));return not r['passed']
if __name__=='__main__':raise SystemExit(main())
