"""Package committed project plus measured stability evidence; verify every archived file."""
import argparse,hashlib,io,json,shutil,subprocess,tarfile,tempfile,zipfile
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--reports',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    project=Path(__file__).resolve().parent;repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=project,text=True).strip());rel=project.relative_to(repo)
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip();summary=json.loads((args.reports/'validation_summary.json').read_text());assert summary['source_commit']==commit,'Regenerate summary for committed source'
    args.output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='icarus-release-') as temp:
        stage=Path(temp)
        with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',commit,str(rel)],cwd=repo))) as t:t.extractall(stage,filter='data')
        dest=stage/rel;shutil.copytree(args.reports,dest/'reports')
        for name,h in summary['runtime_sha256'].items():assert hashlib.sha256((dest/name).read_bytes()).hexdigest()==h,name
        manifest={'project':'ICARUS','version':'1.4.1 Stability & Survival','source_branch':'codex/v1.4.1-stability','source_commit':commit,'campaign_source_commit':summary['campaign_source_commit'],'baseline':'602b4a2','mechanical_checks_passed':summary['mechanical_checks_passed'],'acceptance_verified':summary['acceptance_verified'],'final_release_ready':False,'validation_report':'reports/validation_summary.json','runtime_sha256':summary['runtime_sha256'],'files':{str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(dest.rglob('*')) if p.is_file()}}
        (dest/'BUILD_MANIFEST.json').write_text(json.dumps(manifest,indent=2));archive=args.output/'ICARUS_v1.4.1_Stability_and_Survival.zip'
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in sorted(dest.rglob('*')):
                if p.is_file():z.write(p,Path('ICARUS')/p.relative_to(dest))
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            for name,h in manifest['files'].items():assert hashlib.sha256(z.read('ICARUS/'+name)).hexdigest()==h,name
    digest=hashlib.sha256(archive.read_bytes()).hexdigest();(args.output/(archive.name+'.sha256')).write_text(digest+'  '+archive.name+'\n')
    result={'source_commit':commit,'file':archive.name,'bytes':archive.stat().st_size,'sha256':digest,'verified_files':len(manifest['files']),'acceptance_verified':summary['acceptance_verified']};(args.output/'ICARUS_v1.4.1_package_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
