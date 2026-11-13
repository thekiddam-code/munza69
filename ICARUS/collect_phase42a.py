"""Collect executed observation evidence; every required result is checked before publication."""
import argparse,hashlib,json,shutil,subprocess
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('validation',type=Path);a=ap.parse_args();b=a.validation;r=b/'verification/reports';project=Path(__file__).resolve().parent;out=project/'reports/phase42a/accepted';out.mkdir(parents=True,exist_ok=True);frozen=b/'frozen_runtime';m=json.loads((frozen/'BUILD_MANIFEST.json').read_text())
 different=[n for n,h in m['runtime_files'].items() if hashlib.sha256((project/n).read_bytes()).hexdigest()!=h];assert different==['web/icarus.html']
 without_roster=lambda p:[l for l in p.read_text().splitlines() if not l.startswith(' const tileUpdate=')]
 assert without_roster(project/'web/icarus.html')==without_roster(frozen/'web/icarus.html')
 for name,count in [('observation',62),('remote_observation',32),('production',2),('pin_classic',1)]:
  d=json.loads((r/(name+'.json')).read_text());assert d['passed'] and d['tests_run']==count,name
 assert 'pass 317' in (r/'node.txt').read_text() and 'fail 0' in (r/'node.txt').read_text()
 assert 'Ran 15 tests' in (r/'service_units.txt').read_text() and '\nOK\n' in (r/'service_units.txt').read_text()
 assert 'Ran 1 test' in (b/'home_crew_menu.txt').read_text() and '\nOK\n' in (b/'home_crew_menu.txt').read_text()
 for name,count in [('mobile_functional',15),('tablet_touch',11)]:
  d=json.loads((r/(name+'.json')).read_text());assert d['passed'] and len(d['checks'])==count and not d['errors'],name
 w=json.loads((b/'watchable_shift_final_runtime/observation.json').read_text());assert w['passed'] and w['elapsed_seconds']>=1800 and not w['errors'];assert len(w['final']['crew'])+len(w['final']['dead'])==20
 campaigns=json.loads((r/'campaign_summary.json').read_text());assert campaigns['passed'];perf=json.loads((r/'rendering_performance.json').read_text());assert perf['passed'] and perf['world_unchanged']
 for p in r.iterdir():
  if p.is_file():shutil.copy2(p,out/p.name)
 shutil.copy2(b/'home_crew_menu.txt',out/'home_crew_menu.txt');shutil.copy2(b/'watchable_shift_final_runtime/observation.json',out/'watchable_shift.json')
 for p in (b/'watchable_shift_final_runtime').glob('camera_*.png'):shutil.copy2(p,out/p.name)
 for folder in (b/'verification/campaigns').iterdir():
  dest=out/'campaigns'/folder.name;dest.mkdir(parents=True,exist_ok=True)
  for p in folder.glob('campaign_*.json'):shutil.copy2(p,dest/p.name)
 rates=[]
 for prev,row in zip(w['samples'],w['samples'][1:]):
  dt=row['elapsed_seconds']-prev['elapsed_seconds'];frames=row['stats']['mainFrames']-prev['stats']['mainFrames'];previews=row['stats']['previewFrames']-prev['stats']['previewFrames']
  if frames>=0 and dt>0:rates.append({'main_fps':frames/dt,'combined_preview_fps':previews/dt})
 summary={'passed':True,'watch_runtime_commit':m['source_commit'],'runtime_files':112,'post_watch_ui_patch':{'file':'web/icarus.html','scope':'Only the existing Home Crew Location tileUpdate line. All other lines and 111 runtime files match the watched runtime. Original Home quick-menu wiring separately passed; physics, calendar, pixel renderer, camera array and protocol unchanged.'},'node_cases':317,'browser_cases':{'observation_inherited_and_protocol':62,'pin_and_classic':1,'home_location_menu':1,'host_and_remote':32,'production_clock':2},'service_cases':15,'case_executions_total':430,'counts_note':'Executions include inherited/repeated cases, not unique requirements. Functional checks and benchmarks separate.','functional_emulation_checks':{'phone':15,'tablet':11},'watch':{'elapsed_seconds':w['elapsed_seconds'],'final_tick':w['final']['tick'],'alive':len(w['final']['crew']),'dead':w['final']['dead'],'natural_conversations':w['final']['conversations'],'actual_reload':w['reloads'],'errors':w['errors'],'observed_main_fps_range':[min(x['main_fps'] for x in rates),max(x['main_fps'] for x in rates)],'observed_main_fps_mean':sum(x['main_fps'] for x in rates)/len(rates),'combined_preview_fps_mean':sum(x['combined_preview_fps'] for x in rates)/len(rates),'js_heap_sample_range':[min(x['heap'] for x in w['samples'] if x['heap']),max(x['heap'] for x in w['samples'] if x['heap'])]},'canvas_cpu_benchmark':perf,'campaigns':campaigns,'native_tree_matches_main':subprocess.run(['git','diff','--quiet','origin/main','--','UMBRA'],cwd=project.parent).returncode==0,'not_run':['Physical Windows','Physical Samsung Android/TV','Real LAN/Tailscale','Native APK rebuild','Antivirus','Human visual/readability/screen-reader/GPU validation'],'scope_status':'Functional observation build. Full requested art/state sets and furniture/crowd routing remain partial; see PHASE42A_LIMITATIONS.md.'};(out/'accepted_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps({k:v for k,v in summary.items() if k not in ['campaigns','canvas_cpu_benchmark']},indent=2))
if __name__=='__main__':main()
