import os,subprocess,sys
from pathlib import Path
b=Path(__file__).resolve().parent;root=b/'tested/ICARUS_Phase4_2_Living_Ship_Lite';env=dict(os.environ,PYTHONPATH=str(root),ICARUS_CHROMIUM='/usr/bin/chromium')
for script,name in [('tablet_touch.py','tablet_console'),('run_suite.py','production')]:
 cmd=[sys.executable,str(b/script)]+(['production'] if script=='run_suite.py' else [])
 with (b/'reports'/f'{name}.txt').open('w') as f:
  r=subprocess.run(cmd,cwd='/workspace/work/munza69/ICARUS',env=env,stdout=f,stderr=subprocess.STDOUT)
 if r.returncode:raise SystemExit(r.returncode)
