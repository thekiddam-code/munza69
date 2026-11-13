"""Transparent source-based Lite distribution; development tool excluded from Lite."""
import argparse,hashlib,io,json,subprocess,tarfile,tempfile,zipfile
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();project=Path(__file__).resolve().parent;repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=project,text=True).strip());commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip();rel=project.relative_to(repo);args.output.mkdir(parents=True,exist_ok=True)
    docs=['PHASE42A_CHANGELOG.md','README_PHASE42A.md','PHASE42A_ARCHITECTURE.md','PHASE42A_LIMITATIONS.md','PHASE42A_VALIDATION.md','PHASE42A_PROGRESS.md','PHASE42A_OBSERVATION_PLAN.md','RENDERING_DECISION_PHASE42A.md','PHASE42_ACCEPTANCE.md','README_PHASE42.md','PHASE42_ARCHITECTURE.md','PHASE42_VALIDATION.md','PHASE42_LIMITATIONS.md','PHASE42_CHANGELOG.md','PHASE42_PROGRESS.md','PHASE42_LIVING_SHIP_PLAN.md','PHASE41_DEVICE_TESTING.md','README_PHASE41.md','PHASE41_ARCHITECTURE.md','PHASE41_VALIDATION.md','PHASE41_LIMITATIONS.md','PHASE41_CHANGELOG.md','PHASE41_PROGRESS.md','SECURITY_PHASE41.md','ENGINEERING_PHASE4A.md','README_PHASE4A.md','PHASE4A_ARCHITECTURE.md','PHASE4A_PROGRESS.md','PHASE4A_VALIDATION.md','PHASE4A_LIMITATIONS.md','SECURITY_PHASE4A.md','UMBRA_TV_CAPABILITIES.md','UMBRA_ICON_INVENTORY.md','NATIVE_ANDROID_RECOVERY.md','README_PHASE4.md','FINAL_DESIGN.md','FINAL_RELEASE_ROADMAP.md','LUNAR_MODEL.md'];host=['bridge_service.py','tv_service.py','server.py','requirements.txt','config.json','Start_Remote_Deck.bat'];root='ICARUS_Phase4_2A_Observation_Protocol_Lite';out=args.output/(root+'.zip')
    with tempfile.TemporaryDirectory(prefix='icarus-phase4-package-') as td:
        stage=Path(td)
        with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',commit,str(rel)],cwd=repo))) as tar:tar.extractall(stage,filter='data')
        source=stage/rel;runtime=host+[str(p.relative_to(source)) for p in sorted((source/'web').rglob('*')) if p.is_file()];selected=sorted(runtime+docs);hashes={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in selected};manifest={'project':'ICARUS','edition':'Phase 4.2A Observation Protocol Lite','source_repository':'thekiddam-code/munza69','source_commit':commit,'runtime_files':{name:hashes[name] for name in sorted(runtime)},'files':hashes,'policy':'Every retained source file is byte-identical to this commit; all web/runtime dependencies retained; tests, reports, development tools, generated credentials and packaging scripts excluded.','final_release_ready':False};payload=json.dumps(manifest,indent=2).encode()
        with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for name in selected:z.writestr(root+'/'+name,(source/name).read_bytes())
            z.writestr(root+'/BUILD_MANIFEST.json',payload)
        with zipfile.ZipFile(out) as z:
            assert z.testzip() is None
            assert all(hashlib.sha256(z.read(root+'/'+name)).hexdigest()==digest for name,digest in hashes.items())
    digest=hashlib.sha256(out.read_bytes()).hexdigest();(args.output/(out.name+'.sha256')).write_text(digest+'  '+out.name+'\n');result={'zip':out.name,'source_commit':commit,'sha256':digest,'bytes':out.stat().st_size,'runtime_files':len(runtime),'all_files':len(selected)+1,'crc_and_hashes_passed':True};(args.output/'package_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
