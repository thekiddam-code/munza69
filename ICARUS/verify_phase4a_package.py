"""Independent static source checks; development only, no antivirus certification."""
import argparse,ast,hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image

def main():
 ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--report',type=Path,required=True);a=ap.parse_args();root=a.root;source=Path(__file__).resolve().parent;checks=[]
 manifest=json.loads((root/'BUILD_MANIFEST.json').read_text())
 for name,digest in manifest['files'].items():
  assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
  original=subprocess.check_output(['git','show',manifest['source_commit']+':ICARUS/'+name],cwd=source)
  assert original==(root/name).read_bytes(),name
 for p in root.rglob('*.js'):
  subprocess.run(['node','--check',str(p)],check=True,capture_output=True);checks.append(str(p.relative_to(root)))
 for p in root.glob('*.py'):ast.parse(p.read_text());checks.append(p.name)
 scripts=[]
 for name in ['icarus.html','index.html']:
  html=(root/'web'/name).read_text()
  for script in re.findall(r'<script(?:\s[^>]*)?>([\s\S]*?)</script>',html):
   if script.strip():subprocess.run(['node','--check','--input-type=commonjs'],input=script,text=True,check=True,capture_output=True)
  for s in re.findall(r'<script[^>]+src="([^"]+)"',html):
   assert (root/'web'/s).is_file(),s;scripts.append(s)
 for n in ['config.json','requirements.txt','Start_Remote_Deck.bat']:
  assert subprocess.check_output(['git','show','190cb41:ICARUS/'+n],cwd=source)==(root/n).read_bytes(),n
 old=ast.parse(subprocess.check_output(['git','show','190cb41:ICARUS/server.py'],cwd=source,text=True));new=ast.parse((root/'server.py').read_text())
 def funcs(tree):return {x.name:ast.dump(x,include_attributes=False) for x in tree.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
 of,nf=funcs(old),funcs(new);unchanged=['action','token_hash','tv_connect','tv_ip','load_tokens','save_tokens','tv_settings','tv_save','keyseq']
 assert all(of[n]==nf[n] for n in unchanged)
 def keys(tree):return next(ast.literal_eval(x.value) for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TV_KEYS' for t in x.targets))
 assert keys(old)==keys(new)
 pure=['web/companion-view.js','web/camera-sprites.js','web/umbra/layout.js','web/umbra/icons.js'];pattern=r'fetch\s*\(|XMLHttpRequest|WebSocket|eval\s*\(|new Function|child_process|exec\s*\('
 assert all(not re.search(pattern,(root/n).read_text()) for n in pure)
 gifs=[]
 for p in sorted((root/'web/umbra/arcade').glob('*.gif')):
  original=source/'UMBRA/assets/arcade-kill-cam'/p.name
  assert p.read_bytes()==original.read_bytes()
  with Image.open(p) as im:
   count=im.n_frames;duration=sum((im.seek(i) or im.info.get('duration',0)) for i in range(count));assert count==12 and duration==2880
  gifs.append({'name':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'frames':count,'duration_ms':duration})
 assert len(gifs)==6
 forbidden=['paired_devices.json','samsung_tv.json','package_phase4a.py'];assert all(not (root/n).exists() for n in forbidden)
 assert not list(root.rglob('*.apk')) and not list(root.rglob('test_*.py')) and not list(root.rglob('test_*.js'))
 result={'passed':True,'source_commit':manifest['source_commit'],'syntax_files':len(checks),'local_script_references':len(scripts),'manifest_files':len(manifest['files']),'runtime_files':len(manifest['runtime_files']),'unchanged_host_files':['config.json','requirements.txt','Start_Remote_Deck.bat'],'unchanged_server_functions':unchanged,'tv_key_allowlist_unchanged':True,'pure_modules_without_network_execution_patterns':pure,'arcade_assets':gifs,'private_files_tests_and_replacement_apk_absent':True,'security_review':'SECURITY_PHASE4A.md','limitations':'Static checks, not antivirus certification or penetration testing; no physical device or native APK rebuild.'}
 a.report.write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='arcade_assets'},indent=2))
if __name__=='__main__':main()
