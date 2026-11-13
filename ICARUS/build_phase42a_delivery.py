import hashlib,json,zipfile,subprocess,shutil
from pathlib import Path
repo=Path('/workspace/work/munza69');source=repo/'ICARUS';base=Path('/workspace/work/phase42a');release=base/'release';dest=repo/'downloads/phase42a';dest.mkdir(parents=True,exist_ok=True)
package=release/'ICARUS_Phase4_2A_Observation_Protocol_Lite.zip'
smoke=json.loads((release/'final_package_smoke.json').read_text());assert smoke['passed'] and smoke['tests_run']==9
with zipfile.ZipFile(package) as z:
 assert z.testzip() is None
 root='ICARUS_Phase4_2A_Observation_Protocol_Lite/'
 manifest=json.loads(z.read(root+'BUILD_MANIFEST.json'))
 for name,digest in manifest['files'].items():
  raw=z.read(root+name);assert hashlib.sha256(raw).hexdigest()==digest;assert raw==subprocess.check_output(['git','show',manifest['source_commit']+':ICARUS/'+name],cwd=repo)
 assert len(manifest['runtime_files'])==112
 assert len(z.namelist())==151
 assert not any('/test_' in n or '/reports/' in n or '/__pycache__/' in n or 'package_phase' in n or n.endswith('.pyc') for n in z.namelist())
summary=json.loads((source/'reports/phase42a/accepted/accepted_summary.json').read_text())
verification=json.loads((release/'package_verification.json').read_text());verification.update({'all_archive_files_match_source_commit':True,'excluded_development_tools_tests_reports_and_credentials':True,'accepted_test_case_executions':430,'additional_exact_final_zip_browser_cases':9,'emulation_functional_checks':26,'watch_runtime_commit':summary['watch_runtime_commit'],'watch_elapsed_seconds':summary['watch']['elapsed_seconds'],'watch_provenance':summary['post_watch_ui_patch'],'phase_complete':False,'remaining':'See PHASE42A_LIMITATIONS.md; dedicated pose/art sets, furniture/crowd routing and physical validation remain incomplete.'})
(release/'release_verification.json').write_text(json.dumps(verification,indent=2))
evidence=release/'ICARUS_Phase4_2A_Verification.zip'
files={}
for folder in ['reports/phase42a/accepted','reports/phase42a/baseline','reports/phase42a/development']:
 for p in (source/folder).rglob('*'):
  if p.is_file(): files['source_evidence/'+str(p.relative_to(source))]=p
for name in ['PHASE42A_VALIDATION.md','PHASE42A_LIMITATIONS.md','PHASE42A_ARCHITECTURE.md','PHASE42A_CHANGELOG.md','README_PHASE42A.md','PHASE42A_PROGRESS.md','PHASE42A_OBSERVATION_PLAN.md','RENDERING_DECISION_PHASE42A.md','observe_shift.py','benchmark_observation.py','verify_phase42a.py','collect_phase42a.py','package_phase42a.py','test_observation_model.js','test_observation_integration.py','test_observation_remote.py']:
 files['source_evidence/'+name]=source/name
for p in (base/'verification/campaigns').glob('*/backup_*_7.json'):files['isolated_test_worlds/'+p.parent.name+'/'+p.name]=p
files['isolated_test_worlds/normal_time_watch_final_test_world.json']=base/'watchable_shift_final_runtime/final_test_world.json'
for name in ['final_package_smoke.json','final_package_smoke.txt','final_package_smoke_setup_failure.txt','final_package_smoke_selector_failure.txt','release_verification.json','package_verification.json']:
 files['final_package/'+name]=release/name
files['final_package/final_package_smoke.py']=base/'final_package_smoke.py'
with zipfile.ZipFile(evidence,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name,p in sorted(files.items()):z.write(p,name)
 z.writestr('README.txt','Actual executed evidence. Isolated generated test worlds are NOT the user voyage. Source-based Lite ZIP is separate. Initial final-package setup attempt ran zero tests because no default Playwright browser was installed; rerun used installed /usr/bin/chromium. That run then exposed a test selector matching the hidden Home menu after the added Home entry point; scoping to the intended surveillance menu fixed the driver. All nine focused cases passed on the final rerun, without runtime changes. 430 earlier cases plus 9 exact-final-package cases = 439 executions (not unique requirements), plus 26 emulation checks. Full dedicated art/crowd/physical-device scope remains partial. Reproduction uses source test suites and documented real donor fixtures. No physical/native/antivirus claim.\n')
assert zipfile.ZipFile(evidence).testzip() is None
for p in [package,Path(str(package)+'.sha256'),evidence,release/'release_verification.json',release/'final_package_smoke.json']:
 shutil.copy2(p,dest/p.name)
for p in [package,evidence]:
 digest=hashlib.sha256(p.read_bytes()).hexdigest();(dest/(p.name+'.sha256')).write_text(digest+'  '+p.name+'\n')
print(json.dumps({'destination':str(dest),'source_commit':manifest['source_commit'],'package':verification,'evidence_zip_bytes':evidence.stat().st_size},indent=2))
