"""OS measurements outside the simulation; no browser or world mutation."""
import subprocess,time,json,re
from pathlib import Path
out=Path(__file__).resolve().parent/'reports/campaign_memory.json';report={'limits':'Sum of Linux RSS across each campaign process tree, shared pages can be counted more than once. Not JS retained-heap or target-hardware certification. Sampling starts after campaign initialization.','samples':[]}
while True:
 rows=[]
 for line in subprocess.check_output(['ps','-eo','pid,ppid,rss,args'],text=True).splitlines()[1:]:
  bits=line.strip().split(None,3)
  if len(bits)==4:rows.append((int(bits[0]),int(bits[1]),int(bits[2]),bits[3]))
 roots=[r for r in rows if r[3].startswith('python unified_soak.py ')];sample={'unix_time':time.time(),'campaigns':{}}
 for pid,parent,rss,cmd in roots:
  children={pid}
  while True:
   new={p for p,pp,r,c in rows if pp in children}-children
   if not new:break
   children|=new
  sample['campaigns'][cmd]={'processes':len(children),'sum_rss_kib':sum(r for p,pp,r,c in rows if p in children),'renderer_rss_kib':sum(r for p,pp,r,c in rows if p in children and '--type=renderer' in c)}
 report['samples'].append(sample);out.write_text(json.dumps(report,indent=2))
 if not roots:break
 time.sleep(15)
