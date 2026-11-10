"""Package committed code, measured reports and explicit incomplete-scope manifest."""
import argparse,hashlib,io,json,shutil,subprocess,tarfile,tempfile,zipfile
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--reports',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();project=Path(__file__).resolve().parent;repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=project,text=True).strip());rel=project.relative_to(repo);commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip();summary=json.loads((args.reports/'validation_summary.json').read_text());assert summary['source_commit']==commit;assert summary['verified_implemented_scope'];args.output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='icarus-unified-') as temp:
        stage=Path(temp)
        with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',commit,str(rel)],cwd=repo))) as t:t.extractall(stage,filter='data')
        dest=stage/rel;shutil.copytree(args.reports,dest/'reports')
        for name,h in summary['runtime_sha256'].items():assert hashlib.sha256((dest/name).read_bytes()).hexdigest()==h,name
        manifest={'project':'ICARUS','version':'1.5.0-phase1','source_commit':commit,'campaign_source_commit':summary['campaign_source_commit'],'verified_implemented_scope':True,'complete_uploaded_specification':False,'final_release_ready':False,'validation':'reports/validation_summary.json','limitations':'UNIFIED_LIMITATIONS.md','runtime_sha256':summary['runtime_sha256'],'files':{str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.rglob('*')) if p.is_file()}};(dest/'BUILD_MANIFEST.json').write_text(json.dumps(manifest,indent=2));out=args.output/'ICARUS_Unified_World_Phase1.zip'
        with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in sorted(dest.rglob('*')):
                if p.is_file():z.write(p,Path('ICARUS')/p.relative_to(dest))
        with zipfile.ZipFile(out) as z:
            assert z.testzip() is None
            for name,h in manifest['files'].items():assert hashlib.sha256(z.read('ICARUS/'+name)).hexdigest()==h,name
    digest=hashlib.sha256(out.read_bytes()).hexdigest();(args.output/(out.name+'.sha256')).write_text(digest+'  '+out.name+'\n');r={'file':out.name,'bytes':out.stat().st_size,'sha256':digest,'verified_files':len(manifest['files']),'source_commit':commit,'verified_implemented_scope':True,'complete_uploaded_specification':False};(args.output/'ICARUS_Unified_package_verification.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
if __name__=='__main__':main()
