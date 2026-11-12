"""Collect executed final evidence; fail closed if any required run is missing or failed."""
import argparse,hashlib,json,re,shutil
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('validation',type=Path);args=ap.parse_args();base=args.validation;reports=base/'reports';project=Path(__file__).resolve().parent;out=project/'reports/phase42/accepted';out.mkdir(parents=True,exist_ok=True);manifest=json.loads((base/'tested/ICARUS_Phase4_2_Living_Ship_Lite/BUILD_MANIFEST.json').read_text())
 node=(reports/'node.txt').read_text();assert re.search(r'pass 311\b',node) and re.search(r'fail 0\b',node)
 expected={'living_ship':55,'phase41':31,'production':2};cases={}
 for name,count in expected.items():
  d=json.loads((reports/(name+'.json')).read_text());assert d['passed'] and d['tests_run']==count and not d['failures'] and not d['errors'],name;assert d['runtime_source_commit']==manifest['source_commit'];cases[name]=count
 services=(reports/'service_units.txt').read_text();assert 'Ran 15 tests' in services and services.rstrip().endswith('OK')
 checks={}
 for name,count in [('mobile_functional',15),('tablet_touch',11)]:
  d=json.loads((reports/(name+'.json')).read_text());assert d['passed'] and len(d['checks'])==count and not d['errors'];checks[name]=count
 campaigns=json.loads((reports/'campaign_summary.json').read_text());assert campaigns['passed']
 for folder,row in campaigns['campaigns'].items():
  c=json.loads(next((base/'campaigns'/folder).glob('campaign_*.json')).read_text());assert c['passed'] and c['source_commit']==manifest['source_commit'];assert all(manifest['runtime_files'][n]==h for n,h in c['runtime_sha256'].items())
  assert not row['audit_errors'] and not row['simulation_errors']
 for name in ['preservation_security','registry_performance']:assert json.loads((reports/(name+'.json')).read_text())['passed']
 for p in reports.iterdir():
  if p.is_file():shutil.copy2(p,out/p.name)
 for folder in (base/'campaigns').iterdir():
  dest=out/'campaigns'/folder.name;dest.mkdir(parents=True,exist_ok=True)
  for p in folder.glob('campaign_*.json'):shutil.copy2(p,dest/p.name)
 for name in ['run_suite.py','mobile_functional.py','tablet_touch.py','run_devices.py']:shutil.copy2(base/name,out/name)
 donor=Path('/workspace/work/phase41_final_validation/campaigns/normal_1001/backup_1001_30.json')
 r={'passed':True,'tested_runtime_commit':manifest['source_commit'],'runtime_files':len(manifest['runtime_files']),'node_tests':311,'browser_http_executions':cases,'service_unit_tests':15,'executed_cases_total':311+sum(cases.values())+15,'functional_emulation_checks':checks,'counts_note':'Executed cases include inherited regressions repeated by suites; functional checks and benchmark samples counted separately. Not a count of unique requirements.','historical_phase41_donor_sha256':hashlib.sha256(donor.read_bytes()).hexdigest(),'campaigns':campaigns['campaigns'],'package_policy':'Final documentation packaging may use a later commit; all 106 runtime hashes must match this tested extraction.','unavailable':['Physical Windows laptop','Physical Android phone/Samsung Tab S5e/native APK rebuild (original Studio source pending recovery)','Physical Samsung TV','Real Wi-Fi/Tailscale interruption','Antivirus scan/certification','Human screen-reader/usability/GPU-FPS evaluation'],'driver_limits':['Chromium Linux and phone/tablet emulation; paired desktop/TV I/O stubbed in HTTP tests','Long campaigns disable per-step autosave in deterministic driver, test explicit durable checkpoints and exact reloads','100 registered with 20 active fixture/component benchmark, not 100 active actors','No 365-real-day Phase 4.2 campaign'],'remaining_refinement':'See PHASE42_LIMITATIONS.md; no final ICARUS release completion claim.'};(out/'accepted_summary.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if k not in ['campaigns']},indent=2))
if __name__=='__main__':main()
