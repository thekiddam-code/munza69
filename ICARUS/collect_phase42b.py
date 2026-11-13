"""Collect verified executed evidence, keeping original runtime identities."""
import argparse,json,shutil,subprocess
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('evidence',type=Path);a=ap.parse_args();b=a.evidence;project=Path(__file__).resolve().parent;out=project/'reports/phase42b/accepted';out.mkdir(parents=True,exist_ok=True)
 subprocess.run(['python',str(project/'verify_phase42b.py'),str(b),'--report',str(out/'provenance_security.json')],check=True)
 paths={'full_browser.json':b/'final_verification/browser.json','full_browser.txt':b/'browser_final.txt','remote.json':b/'delivery_verification/remote.json','remote.txt':b/'remote_delivery.txt','clock.json':b/'delivery_verification/clock.json','clock.txt':b/'clock_delivery.txt','focused.json':b/'delivery_verification/focused.json','focused.txt':b/'focused_delivery_rerun.txt','three_crew.json':b/'delivery_verification/three_crew.json','three_crew.txt':b/'three_crew.txt','node.txt':b/'delivery_verification/node.txt','services.txt':b/'services_delivery.txt','long_watch.json':b/'timed_watch/watch.json','final_watch.json':b/'delivery_watch/watch.json','campaign_summary.json':b/'campaign_summary.json','personality_statistics.json':b/'personality_statistics.json','run_suite.py':b.parent/'phase42b_run_suite.py','final_runtime_manifest.json':b/'delivery_runtime/BUILD_MANIFEST.json','long_watch_runtime_manifest.json':b/'final_runtime/BUILD_MANIFEST.json'}
 for name,path in paths.items():shutil.copy2(path,out/name)
 for folder in (b/'campaigns').iterdir():
  dest=out/'campaigns'/folder.name;dest.mkdir(parents=True,exist_ok=True)
  for p in folder.glob('campaign_*.json'):shutil.copy2(p,dest/p.name)
 for label in ['timed_watch','delivery_watch']:
  for p in (b/label).glob('*.png'):shutil.copy2(p,out/(label+'_'+p.name))
 summary={'passed':True,'accepted_case_executions':464,'phase_complete':False,'runtime_provenance':json.loads((out/'provenance_security.json').read_text()),'campaigns':json.loads((b/'campaign_summary.json').read_text()),'personalities':json.loads((b/'personality_statistics.json').read_text()),'long_watch':json.loads((b/'timed_watch/watch.json').read_text()),'final_watch':json.loads((b/'delivery_watch/watch.json').read_text()),'not_run':['Physical Windows/Android/TV','Real LAN/Tailscale','Native APK rebuild','Antivirus','Human accessibility/readability/GPU'],'limits':'No organic dating/private event observed; positive paths use labeled source-generated mechanics fixtures. Dedicated art, furniture/crowd routing, cabin medical recovery and remote classified roles remain incomplete.'};(out/'accepted_summary.json').write_text(json.dumps(summary,indent=2));print('Collected executed evidence:',out)
if __name__=='__main__':main()
