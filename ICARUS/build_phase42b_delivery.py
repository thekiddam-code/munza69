"""Publishable source/evidence artifacts; development-only, excluded from Lite."""
import argparse,hashlib,json,shutil,subprocess,zipfile
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('evidence',type=Path);a=ap.parse_args();base=a.evidence;source=Path(__file__).resolve().parent;repo=source.parent;release=base/'release';dest=repo/'downloads/phase42b';dest.mkdir(parents=True,exist_ok=True);package=release/'ICARUS_Phase4_2B_Living_Personalities_Lite.zip';smoke=json.loads((release/'final_zip_smoke.json').read_text());assert smoke['passed'] and smoke['tests_run']==4
 with zipfile.ZipFile(package) as z:
  assert z.testzip() is None;root='ICARUS_Phase4_2B_Living_Personalities_Lite/';m=json.loads(z.read(root+'BUILD_MANIFEST.json'));assert len(m['runtime_files'])==118 and len(z.namelist())==164
  for n,h in m['files'].items():
   raw=z.read(root+n);assert hashlib.sha256(raw).hexdigest()==h;assert raw==subprocess.check_output(['git','show',m['source_commit']+':ICARUS/'+n],cwd=repo)
  assert not any('/test_' in n or '/reports/' in n or '/__pycache__/' in n or 'package_phase' in n or n.endswith('.pyc') or 'paired_devices' in n for n in z.namelist())
  for n,h in m['runtime_files'].items():assert hashlib.sha256((source/n).read_bytes()).hexdigest()==h,n
 assert m['source_commit']==smoke['source_commit']
 summary=json.loads((source/'reports/phase42b/accepted/accepted_summary.json').read_text());assert summary['passed'] and summary['accepted_case_executions']==465
 result={'passed':True,'source_commit':m['source_commit'],'zip':package.name,'sha256':hashlib.sha256(package.read_bytes()).hexdigest(),'bytes':package.stat().st_size,'runtime_files':118,'all_archive_files':164,'crc_passed':True,'every_file_matches_committed_source':True,'runtime_matches_tested_candidate_with_recorded_provenance':True,'accepted_case_executions':465,'additional_exact_final_zip_cases':4,'phase_complete':False,'test_provenance':summary['runtime_provenance'],'scope_limits':summary['limits'],'not_run':summary['not_run']};(release/'release_verification.json').write_text(json.dumps(result,indent=2))
 evidence=release/'ICARUS_Phase4_2B_Verification.zip';files={}
 for folder in ['reports/phase42b/accepted','reports/phase42b/development','reports/phase42b/baseline','reports/phase42b/milestone1','reports/phase42b/milestone2']:
  for p in (source/folder).rglob('*'):
   if p.is_file():files['source_evidence/'+str(p.relative_to(source))]=p
 for name in ['PHASE42B_VALIDATION.md','PHASE42B_ARCHITECTURE.md','PHASE42B_CHANGELOG.md','PHASE42B_LIMITATIONS.md','README_PHASE42B.md','PHASE42B_PROGRESS.md','PHASE42B_LIVING_PERSONALITIES_PLAN.md','observe_personalities.py','personality_campaign.py','verify_phase42b.py','collect_phase42b.py','package_phase42b.py','build_phase42b_delivery.py','test_personalities_integration.py','test_personalities_remote.py','test_personalities_clock.py','test_phase42b_transit.js','test_phase42b_personalities.js','test_phase42b_service.py']:
  files['source_evidence/'+name]=source/name
 for p in (base/'campaigns').glob('*/backup_*.json'):files['isolated_test_worlds/'+p.parent.name+'/'+p.name]=p
 for label in ['timed_watch','delivery_watch']:files['isolated_test_worlds/'+label+'.json']=base/label/'isolated_test_world.json'
 for name in ['release_verification.json','package_verification.json','final_zip_smoke.json','final_zip_smoke.txt','final_zip_pixel.png']:files['final_package/'+name]=release/name
 files['final_package/final_zip_smoke.py']=base/'final_zip_smoke.py'
 with zipfile.ZipFile(evidence,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,p in sorted(files.items()):z.write(p,name)
  z.writestr('README.txt','Actual executed evidence. All save files are ISOLATED TEST WORLDS, not the user voyage. Do not import them over your voyage. 465 accepted case executions plus four exact-final-ZIP browser checks. Original source commits preserved; long watch/full suite and final provenance corrections are explicitly distinguished. No organic romance/private event observed in campaigns; seeded source-generated mechanics fixtures cover positive paths. No physical/native/antivirus claim. Lite runtime is a separate source-based ZIP.\n')
 assert zipfile.ZipFile(evidence).testzip() is None
 for p in [package,evidence,release/'release_verification.json',release/'final_zip_smoke.json']:shutil.copy2(p,dest/p.name)
 for p in [package,evidence]:(dest/(p.name+'.sha256')).write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n')
 print(json.dumps({'source_commit':m['source_commit'],'lite_sha256':result['sha256'],'evidence_bytes':evidence.stat().st_size,'destination':str(dest)},indent=2))
if __name__=='__main__':main()
