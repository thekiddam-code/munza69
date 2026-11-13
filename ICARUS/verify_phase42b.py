"""Verify runtime provenance and actual executed reports; never synthesize outcomes."""
import argparse,hashlib,json,subprocess
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('evidence',type=Path);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args();b=a.evidence;project=Path(__file__).resolve().parent;final=json.loads((b/'delivery_runtime/BUILD_MANIFEST.json').read_text());frozen=json.loads((b/'final_runtime/BUILD_MANIFEST.json').read_text());different=[]
 for n,h in final['runtime_files'].items():
  assert hashlib.sha256((project/n).read_bytes()).hexdigest()==h,n
  if frozen['runtime_files'][n]!=h:different.append(n)
 assert sorted(different)==['web/icarus.html','web/knowledge.js','web/ship-schematic.js'],different
 for name,count,path in [('full_browser',69,b/'final_verification/browser.json'),('full_remote',34,b/'delivery_verification/remote.json'),('clock',4,b/'delivery_verification/clock.json'),('focused',6,b/'delivery_verification/focused.json'),('three_crew',1,b/'delivery_verification/three_crew.json')]:
  r=json.loads(path.read_text());assert r['passed'] and r['tests_run']==count,name
 assert 'pass 332' in (b/'delivery_verification/node.txt').read_text() and 'fail 0' in (b/'delivery_verification/node.txt').read_text()
 assert 'Ran 18 tests' in (b/'services_delivery.txt').read_text() and '\nOK\n' in (b/'services_delivery.txt').read_text()
 for name in ['timed_watch','delivery_watch']:
  w=json.loads((b/name/'watch.json').read_text());assert w['passed'] and not w['errors'] and len(w['reloads'])==1
 assert json.loads((b/'campaign_summary.json').read_text())['passed']
 old='633224844fda7451f6cbeda2a3c7f571ca93ba55';critical=['web/economy.js','web/repair-policy.js','web/voyage.js','web/durable-store.js','web/save-store.js','web/backup-codec.js','web/backup-transfer.js','web/creatures.js','web/teams.js','web/research.js','web/unified-world.js','tv_service.py','requirements.txt','Start_Remote_Deck.bat']
 for n in critical:assert (project/n).read_bytes()==subprocess.check_output(['git','show',old+':ICARUS/'+n],cwd=project),n
 assert subprocess.run(['git','diff','--quiet','e0065eb','--','UMBRA'],cwd=project.parent).returncode==0
 result={'passed':True,'baseline':old,'final_runtime_commit':final['source_commit'],'long_watch_and_full_browser_commit':frozen['source_commit'],'runtime_files':len(final['runtime_files']),'unchanged_from_long_watch':len(final['runtime_files'])-len(different),'post_freeze_files':different,'post_freeze_scope':'Shared cabin occupancy/focus in schematic/hologram; acquired and injury/death source location corrected to actual cabin. Clock/social/transit controllers unchanged. Final Node/focused/remote/clock/20x campaign and shorter actual-time watch cover these fixes.','unchanged_baseline_authorities':critical,'native_source_apks_unchanged':True,'accepted_case_executions':464,'counts_note':'332 Node +69 frozen full browser +34 final remote +4 final clock +6 final focused +1 three-crew +18 service. Inherited/repeated cases, not unique requirements. Failed/superseded attempts excluded.','protocol':'128 KiB authenticated host request; classified subpayload max24 KiB, never ordinary telemetry. Legacy14000-character/command4KiB bounds retained. Restricted GET requires localhost and host capability; ordinary paired bearer insufficient.','static_review':'Original procedural art, no new dependency. Console is a fixed UI whitelist with no OS execution. New fetches are same-host bootstrap/restricted reads; restricted publication uses existing fenced host channel. No AV disabled or new system modification. Existing Windows dependencies and paired input/TV functionality retained. No AV/penetration certification.','phase_complete':False,'remaining':'Dedicated art/poses, furniture/crowd routing, full cabin medical recovery, remote classified roles and physical/human validation remain incomplete. Campaigns observed no dating/private event; seeded mechanics tests verify those paths.'};a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
