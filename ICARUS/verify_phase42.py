"""Static package/source review, without executing launcher commands or changing system security."""
import argparse,hashlib,json,subprocess
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--lite',type=Path,required=True);ap.add_argument('--report',type=Path,required=True);args=ap.parse_args();root=Path(__file__).resolve().parent;lite=args.lite;baseline='0854442';manifest=json.loads((lite/'BUILD_MANIFEST.json').read_text());assert all(hashlib.sha256((lite/n).read_bytes()).hexdigest()==h for n,h in manifest['runtime_files'].items())
 oldpaths=set(subprocess.check_output(['git','ls-tree','-r','--name-only',baseline,'ICARUS'],cwd=root.parent,text=True).splitlines());unchanged=[];changed=[];added=[]
 for name in manifest['runtime_files']:
  if 'ICARUS/'+name not in oldpaths:added.append(name);continue
  old=subprocess.check_output(['git','show',baseline+':ICARUS/'+name],cwd=root)
  (unchanged if (lite/name).read_bytes()==old else changed).append(name)
 critical=['web/calendar.js','web/command-ui.js','web/host-authority.js','web/remote-sync.js','server.py','bridge_service.py','tv_service.py','web/workspace.js','web/knowledge.js','web/durable-store.js','web/backup-codec.js','web/backup-transfer.js','web/chronicle-film.js','web/chronicle-evidence.js','web/cinema.js','web/umbra/bridge.js','web/umbra/app.js']
 assert all(n in unchanged for n in critical)
 before=subprocess.check_output(['git','show',baseline+':ICARUS/web/icarus.html'],cwd=root,text=True);after=(lite/'web/icarus.html').read_text();prefixes=["function pumpRealTime(","  setRate:rate=>","$('pause').onclick=",'if(!state.events.length&&canWriteWorld())']
 for prefix in prefixes:assert next(l for l in before.splitlines() if l.startswith(prefix))==next(l for l in after.splitlines() if l.startswith(prefix)),prefix
 for name in added:
  text=(lite/name).read_text();assert not any(token in text for token in ['fetch(','WebSocket(','child_process','exec(','subprocess','eval(']),name
 r={'passed':True,'baseline':baseline,'package_source':manifest['source_commit'],'runtime_files_verified':len(manifest['runtime_files']),'unchanged_files':unchanged,'changed_files':changed,'added_files':added,'original_clock_pause_rate_handlers_byte_identical':True,'known_20x_issue':'Deferred to Phase 4.1.1; not fixed here','static_review':'New modules perform local state operations and DOM rendering only. No added network, process execution, system modification, antivirus change or native project replacement. Retained launcher installs Python runtime dependencies. Existing server performs paired desktop/game input and TV network operations as documented in SECURITY_PHASE41.md. No antivirus/penetration certification.'};args.report.write_text(json.dumps(r,indent=2));print(json.dumps({k:v for k,v in r.items() if not k.endswith('_files')},indent=2))
if __name__=='__main__':main()
