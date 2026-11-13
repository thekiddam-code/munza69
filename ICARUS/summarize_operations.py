"""Independent full-history, conservation and operational audit of actual campaign artifacts."""
import argparse,json,subprocess,sys
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('campaigns',type=Path);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 subprocess.run([sys.executable,str(Path(__file__).with_name('summarize_phase42.py')),str(a.campaigns),'--output',str(a.output)],check=True)
 report=json.loads(a.output.read_text())
 for name,row in report['campaigns'].items():
  folder=a.campaigns/name;c=json.loads(next(folder.glob('campaign_*.json')).read_text());s=json.loads((folder/f'backup_{c["seed"]}_{c["real_days"]}.json').read_text())['state'];sy=s['shipSystems'];errors=row['audit_errors']
  for d in c['daily']:
   errors.extend(d['phase43']['systems_errors']);errors.extend(d['phase43']['gravity_errors'])
  if len(sy['history'])>80:errors.append('Unbounded operational summary')
  if any(len(x['history'])>16 for x in sy['components'].values()):errors.append('Unbounded component history')
  for comp in sy['components'].values():
   for h in comp['history']:
    if not h.get('sourceId'):errors.append('Repair outcome lacks a recorded source')
  row['operational']={'generator_condition':sy['components']['GRAVITY-CORE']['health'],'generator_service_isolated':sy['components']['GRAVITY-CORE']['serviceIsolated'],'component_conditions':{k:v['health'] for k,v in sy['components'].items()},'component_repairs':sum(len(v['history']) for v in sy['components'].values()),'component_history':{k:v['history'] for k,v in sy['components'].items() if v['history']},'gravity_actual':{k:v['g'] for k,v in sy['zones'].items()},'gravity_targets':{k:v['targetG'] for k,v in sy['zones'].items()},'main_bus':sy['bus'],'open_orders':s['maintenance']['systemOrders'],'component_energy_ledger':[x for x in s['economy']['ledger'].values() if 'gravity fields' in x['source'] or 'systems work' in x['source']],'new_summary_entries':len(sy['history'])}
  row['passed']=not errors and not c['errors'];report['passed']&=row['passed']
 a.output.write_text(json.dumps(report,indent=2));print(json.dumps({k:{'alive':r['alive'],'deaths':r['deaths'],'ship_days':r['ship_days'],'component_repairs':r['operational']['component_repairs'],'errors':r['audit_errors']} for k,r in report['campaigns'].items()},indent=2));return not report['passed']
if __name__=='__main__':raise SystemExit(main())
