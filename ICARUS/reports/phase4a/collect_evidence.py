import hashlib,json,re,shutil,subprocess
from pathlib import Path
base=Path(__file__).resolve().parent;src=Path('/workspace/work/munza69/ICARUS');raw=Path('/workspace/work/phase4a_reports');out=src/'reports/phase4a';out.mkdir(parents=True,exist_ok=True)
expected={'cinematic':71,'stability':30,'compatibility':44,'interface':17,'production':2,'bridge':3,'umbra':16,'tv_service':7};tests={}
for n,count in expected.items():
 d=json.loads((base/'reports'/f'{n}.json').read_text());assert d['passed'] and d['tests_run']==count and not d['errors'] and not d['failures'],n;tests[n]=count
node=(base/'reports/node.txt').read_text();assert re.search(r'pass 276\b',node) and re.search(r'fail 0\b',node)
for n,count in [('mobile_functional',15),('tablet_touch',11)]:
 d=json.loads((base/'reports'/f'{n}.json').read_text());assert d['passed'] and len(d['checks'])==count,n
migrations={}
for n in ['phase1','phase2','phase3','phase3_memorial','phase35']:
 d=json.loads((base/'reports'/f'migrate_{n}.json').read_text());assert d['passed'] and not d['errors'] and not d['mismatched_import_domains'] and not d['mismatched_reload_domains'],n;migrations[n]={'history_records':d['imported_history_records'],'crew':d['crew_after'],'memorials':d['memorials_after'],'tick':d['imported_tick'],'resumed_tick':d['resumed_tick']}
c=json.loads((raw/'campaign_summary.json').read_text());assert c['passed']
m=json.loads((base/'tested/ICARUS_SOL_Command_Interface_Phase4_Lite/BUILD_MANIFEST.json').read_text());assert len(m['runtime_files'])==90
for n,h in m['runtime_files'].items():assert hashlib.sha256((src/n).read_bytes()).hexdigest()==h,n
for name,r in c['campaigns'].items():
 assert r['passed'] and not r['public_source_audit_errors']
 assert all(m['runtime_files'][n]==h for n,h in r['runtime_sha256'].items())
for p in (base/'reports').iterdir():
 if p.is_file():shutil.copy2(p,out/p.name)
for n in ['campaign_summary.json','source_gate.json','umbra_browser_option_driver_diagnostic.json','campaign7.txt','campaign30.txt']:shutil.copy2(raw/n,out/n)
for p in (raw/'campaigns').glob('*/campaign_*.json'):
 target=out/'campaigns'/p.parent.name/p.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
shutil.copytree(raw/'screenshots',out/'screenshots',dirs_exist_ok=True)
for p in Path('/workspace/work/phase4_reports/screenshots').glob('*.png'):
 if p.name.startswith(('desktop_','tablet_')):shutil.copy2(p,out/'screenshots'/('core_'+p.name))
for n in ['run_suite.py','migrate.py','run_migrations.py','mobile_functional.py','tablet_touch.py','REPRODUCE.md','collect_evidence.py']:shutil.copy2(base/n,out/n)
summary={'browser_server_scope_complete':True,'full_phase_or_final_release_complete':False,'tested_runtime_commit':m['source_commit'],'runtime_files':90,'node_tests':276,'unit_and_browser_suites':tests,'unit_and_browser_total':sum(tests.values()),'browser_server_cases':sum(v for k,v in tests.items() if k!='tv_service'),'phone_functional_checks':15,'tablet_touch_checks':11,'historical_migrations':migrations,'campaigns':{n:{k:r[k] for k in ['passed','real_days','sim_days','alive','dead','arrivals','field_missions','science_cases','conversations','weekly_films','history_records','public_source_audit_errors']} for n,r in c['campaigns'].items()},'static_review_passed':json.loads((base/'reports/static.json').read_text())['passed'],'remaining':{'native_apk_build':'Pending recovery of existing Android Studio source; installed APK preserved, not replaced','physical_windows':'NOT RUN','physical_android_tab_s5e_wifi':'NOT RUN','physical_samsung_tv':'NOT RUN; protocol/HTTP tested with stubbed socket','antivirus':'NOT RUN; no protection disabled','screen_reader_native_gpu_human_usability':'NOT RUN','actual_recorded_kill_cam_advanced_native_tv_streaming_push_voice':'Deferred/unverified'},'runtime_identity':'All 90 source/extracted runtime hashes match; campaign driver records 89 old host/web hashes, service covered independently','diagnostics':'See PHASE4A_VALIDATION.md; driver assumptions corrected, incomplete campaign audit rejected, no assertions removed.'}
(out/'accepted_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps({k:v for k,v in summary.items() if k not in ['historical_migrations','campaigns']},indent=2))
