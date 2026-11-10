"""Static source/manifest verification; a development tool, excluded from Lite."""
import argparse,ast,hashlib,json,re,subprocess
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args();root=a.root;checks=[]
 for p in root.rglob('*.js'):
  subprocess.run(['node','--check',str(p)],check=True,capture_output=True);checks.append(str(p.relative_to(root)))
 for p in root.glob('*.py'):ast.parse(p.read_text());checks.append(p.name)
 html=(root/'web/icarus.html').read_text()
 for script in re.findall(r'<script(?:\s[^>]*)?>([\s\S]*?)</script>',html):
  if script.strip():subprocess.run(['node','--check','--input-type=commonjs'],input=script,text=True,check=True,capture_output=True)
 scripts=re.findall(r'<script[^>]+src="([^"]+)"',html);assert all((root/'web'/s).is_file() for s in scripts)
 manifest=json.loads((root/'BUILD_MANIFEST.json').read_text());assert all(hashlib.sha256((root/n).read_bytes()).hexdigest()==h for n,h in manifest['files'].items())
 for n in ['server.py','config.json','requirements.txt','Start_Remote_Deck.bat']:
  old=subprocess.check_output(['git','show','113e79b:ICARUS/'+n],cwd=Path(__file__).resolve().parent.parent);assert old==(root/n).read_bytes()
 new=['crew-life.js','cinema.js','cinema-ui.js','sol-voice.js','chronicle-film.js','film-ui.js','animation.js','crew-editorial.js','chronicle-evidence.js','backup-codec.js','backup-transfer.js','backup-ui.js','writer-ui.js'];pattern=r'fetch\s*\(|XMLHttpRequest|WebSocket|eval\s*\(|new Function|child_process|exec\s*\('
 assert all(not re.search(pattern,(root/'web'/n).read_text()) for n in new)
 result={'passed':True,'syntax_files':len(checks),'local_scripts':len(scripts),'manifest_files':len(manifest['files']),'runtime_files':len(manifest['runtime_files']),'host_files_unchanged_from_phase2':True,'new_module_network_execution_pattern_hits':0,'source_commit':manifest['source_commit'],'limits':'Static source checks, not antivirus certification or penetration test.'};a.report.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
