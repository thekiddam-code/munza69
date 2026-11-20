"""Standalone preservation tool: copies and verifies; never migrates/deletes source files."""
import argparse,hashlib,json,os,sys,tempfile,time,uuid,zipfile
from pathlib import Path
MAX_TOTAL=128*1024*1024

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def inventory(root):
 root=Path(root)
 if not root.is_dir():return {'exists':False,'files':{},'sounds':0,'errors':[]}
 files={};total=0
 for p in sorted(root.rglob('*')):
  if p.is_symlink():raise ValueError('Backup refuses symbolic links; preserve them manually before upgrading')
  if p.is_file():
   total+=p.stat().st_size
   if total>MAX_TOTAL:raise ValueError('Sound folder exceeds 128 MiB backup limit; no source was changed')
   files[p.relative_to(root).as_posix()]={'bytes':p.stat().st_size,'sha256':digest(p)}
 errors=[];sounds=0
 if 'library.json' in files:
  try:
   data=json.loads((root/'library.json').read_text('utf8'));sounds=len(data['sounds'])
   for s in data['sounds']:
    ident=s.get('id','')
    if not isinstance(ident,str) or len(ident)!=32 or any(c not in '0123456789abcdef' for c in ident):errors.append('Invalid sound identity');continue
    name=ident+'.wav'
    if name not in files:errors.append('Missing clip '+ident)
    elif files[name]['sha256']!=s.get('sha256'):errors.append('Checksum mismatch '+ident)
  except Exception as e:errors.append('Metadata unreadable: '+str(e)[:160])
 elif files:errors.append('Files exist but library.json is missing; originals preserved, automatic writes blocked')
 return {'exists':True,'files':files,'sounds':sounds,'errors':errors}

def verify_archive(path):
 with zipfile.ZipFile(path) as z:
  if z.testzip() is not None:raise ValueError('Backup CRC failed')
  manifest=json.loads(z.read('BACKUP_MANIFEST.json'))
  for name,item in manifest['source']['files'].items():
   h=hashlib.sha256();size=0
   with z.open('soundboard_data/'+name) as f:
    for block in iter(lambda:f.read(1024*1024),b''):h.update(block);size+=len(block)
   if h.hexdigest()!=item['sha256'] or size!=item['bytes']:raise ValueError('Backup hash/size verification failed')
 return manifest

def backup(root,destination=None):
 root=Path(root).resolve();before=inventory(root)
 if not before['exists'] or not before['files']:return {'created':False,'verified':True,'reason':'No existing server library files to copy','source':before}
 folder=Path(destination).resolve() if destination else root.parent/'soundboard_backups'
 if folder==root or root in folder.parents:raise ValueError('Backups must be outside the source folder')
 folder.mkdir(parents=True,exist_ok=True);ident=time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())+'_'+uuid.uuid4().hex[:12];target=folder/(ident+'.zip');tmp=target.with_suffix('.partial')
 try:
  with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as z:
   for name in before['files']:z.write(root/name,'soundboard_data/'+name)
   z.writestr('BACKUP_MANIFEST.json',json.dumps({'version':1,'created_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'source':before},indent=2))
  verify_archive(tmp)
  if inventory(root)!=before:raise ValueError('Library changed during backup; retry while server is stopped. Originals were not removed.')
  os.replace(tmp,target)
  return {'created':True,'verified':True,'id':ident,'file':target.name,'sha256':digest(target),'source':before}
 except Exception:
  tmp.unlink(missing_ok=True);raise

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).parent/'soundboard_data');ap.add_argument('--destination',type=Path);ap.add_argument('--verify',type=Path);ap.add_argument('--require-existing',action='store_true',help='Fail if imported sounds were not found; never call an empty folder a verified library backup');args=ap.parse_args()
 try:
  if args.verify:print(json.dumps({'verified':True,'manifest':verify_archive(args.verify)},indent=2))
  else:
   result=backup(args.root,args.destination);print(json.dumps(result,indent=2))
   if args.require_existing and (not result['created'] or result['source']['sounds']==0):print('EXISTING IMPORTED LIBRARY NOT FOUND: stop and locate the original soundboard_data folder; do not upgrade.',file=sys.stderr);sys.exit(3)
   sys.exit(2 if result['source']['errors'] else 0)
 except Exception as e:print('BACKUP FAILED: '+str(e),file=sys.stderr);sys.exit(1)
