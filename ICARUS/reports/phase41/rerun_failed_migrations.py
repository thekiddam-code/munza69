import os,subprocess,sys,json
from pathlib import Path
base=Path(__file__).resolve().parent
files={
'phase4a':'/workspace/work/phase4a_reports/campaigns/normal_1001/backup_1001_30.json',
'phase1':'/workspace/work/lite_build/reports/soak/backup_1001_7.json',
'phase2':'/workspace/work/phase2_reports/campaigns/normal_1001/backup_1001_30.json',
'phase3':'/workspace/work/phase3_reports/campaigns/normal_1001/backup_1001_30.json',
'phase3_memorial':'/workspace/work/phase3_reports/campaigns/normal_4807/backup_4807_30.json',
'phase35':'/workspace/work/phase35_reports/campaigns/normal_1001/backup_1001_30.json'}
env=dict(os.environ,ICARUS_BACKUP_TIMEOUT='600000',ICARUS_CHROMIUM='/usr/bin/chromium');results=[]
for name,path in files.items():
 if name=='phase4a':continue
 with (base/'reports'/f'migrate_{name}.txt').open('w') as out:r=subprocess.run([sys.executable,str(base/'migrate.py'),path,'--report',str(base/'reports'/f'migrate_{name}.json')],env=env,stdout=out,stderr=subprocess.STDOUT)
 results.append({'name':name,'returncode':r.returncode});print(name,r.returncode,flush=True)
(base/'reports/migrations.json').write_text(json.dumps(results,indent=2));raise SystemExit(any(r['returncode'] for r in results))
