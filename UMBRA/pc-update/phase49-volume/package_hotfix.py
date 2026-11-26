"""Source-only reproducible ZIP; never include local libraries or backups."""
import argparse,hashlib,json,subprocess,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
FILES=['README.md','VERIFICATION.md','CHANGES.patch','apply_volume_fix.py','apply_volume_fix.bat','manifest.json','payload/web/umbra/soundboard.js']
def build(destination):
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip();prefix='UMBRA/pc-update/phase49-volume/'
 content={n:subprocess.check_output(['git','show',commit+':'+prefix+n],cwd=HERE) for n in FILES}
 manifest=json.loads(content['manifest.json']);assert hashlib.sha256(content['payload/web/umbra/soundboard.js']).hexdigest()==manifest['after']
 content['SOURCE.json']=(json.dumps({'source_commit':commit,'files':{n:hashlib.sha256(b).hexdigest() for n,b in content.items()}},indent=2)+'\n').encode()
 destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in content.items():
   info=zipfile.ZipInfo('UMBRA_Phase49_Volume_Fix/'+name,(2026,11,26,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,data)
 with zipfile.ZipFile(destination) as z:
  assert z.testzip() is None
  assert len(z.namelist())==len(content)
  for name,data in content.items():assert z.read('UMBRA_Phase49_Volume_Fix/'+name)==data
 checksum=hashlib.sha256(destination.read_bytes()).hexdigest();destination.with_suffix('.zip.sha256').write_text(checksum+'  '+destination.name+'\n');return {'source_commit':commit,'zip':destination.name,'bytes':destination.stat().st_size,'sha256':checksum,'files':list(content),'crc_verified':True,'source_bytes_verified':True}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('destination',type=Path);a=p.parse_args();print(json.dumps(build(a.destination),indent=2))
