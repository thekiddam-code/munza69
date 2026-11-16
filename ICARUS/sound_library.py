"""Bounded, atomic local sound library. Independent of ICARUS and microphone configuration."""
import base64,copy,hashlib,io,json,math,os,re,threading,uuid,wave
from pathlib import Path
class SoundError(ValueError):
 def __init__(self,message,status=400):super().__init__(message);self.status=status
MAX_BYTES=1440044
ICON_NAMES={'none','play','game','timer','connection','info','camera','crew','power','volume'}
def text(value,label,limit):
 if not isinstance(value,str) or not 1<=len(value.strip())<=limit or any(ord(c)<32 for c in value):raise SoundError(label+' is invalid')
 return value.strip()
def metadata(data):
 if not isinstance(data,dict):raise SoundError('Sound fields required')
 name=text(data.get('name'),'Name',48);category=text(data.get('category','General'),'Category',32);icon=data.get('icon','play');volume=data.get('volume',.35);favorite=data.get('favorite',False)
 if icon not in ICON_NAMES or type(volume) not in (float,int) or not math.isfinite(volume) or not 0<=volume<=1 or type(favorite)!=bool:raise SoundError('Invalid icon, volume or favorite')
 return {'name':name,'category':category,'icon':icon,'volume':volume,'favorite':favorite}
def validate_audio(raw):
 if not isinstance(raw,bytes) or not 44<=len(raw)<=MAX_BYTES:raise SoundError('Canonical WAV must be at most 30 seconds / 1.44 MB')
 try:
  with wave.open(io.BytesIO(raw),'rb') as w:
   if (w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getcomptype())!=(1,2,24000,'NONE'):raise SoundError('Use canonical 24 kHz mono PCM16 WAV')
   count=w.getnframes();frames=w.readframes(count)
   if not 1<=count<=720000 or len(frames)!=count*2:raise SoundError('Empty, truncated or oversized WAV')
 except (wave.Error,EOFError) as e:raise SoundError('Invalid WAV: '+str(e))
 return {'duration':count/24000,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'format':'24 kHz mono PCM16 WAV'}
class SoundLibrary:
 def __init__(self,root):self.root=Path(root);self.lock=threading.RLock()
 def _load(self):
  p=self.root/'library.json'
  if not p.exists():return {'version':1,'revision':0,'sounds':[],'output':None}
  try:
   d=json.loads(p.read_text('utf8'))
   if d.get('version')!=1 or not isinstance(d.get('sounds'),list) or len(d['sounds'])>64:raise ValueError('Unsupported library format')
   if type(d.get('revision'))!=int or d['revision']<0:raise ValueError('Invalid library revision')
   ids=set()
   for item in d['sounds']:
    if not isinstance(item,dict) or not re.fullmatch(r'[a-f0-9]{32}',str(item.get('id',''))) or item['id'] in ids:raise ValueError('Invalid sound identity')
    ids.add(item['id']);metadata(item)
    if not re.fullmatch(r'[a-f0-9]{64}',str(item.get('sha256',''))) or type(item.get('bytes'))!=int or not 44<=item['bytes']<=MAX_BYTES:raise ValueError('Invalid stored audio metadata')
   return d
  except (OSError,ValueError,TypeError) as e:raise SoundError('Library unreadable; preserve files and restore a backup: '+str(e),500)
 def _save(self,data):
  self.root.mkdir(parents=True,exist_ok=True);tmp=self.root/'library.json.tmp'
  with tmp.open('w',encoding='utf8') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
  os.replace(tmp,self.root/'library.json')
 def view(self):
  with self.lock:return copy.deepcopy(self._load())
 def _revision(self,data,revision):
  if type(revision)!=int or revision!=data['revision']:raise SoundError('Library changed on another terminal. Refresh and retry your edit.',409)
 def get(self,ident):
  if not isinstance(ident,str) or not re.fullmatch(r'[a-f0-9]{32}',ident):raise SoundError('Unknown sound',404)
  with self.lock:
   item=next((s for s in self._load()['sounds'] if s['id']==ident),None)
   if not item:raise SoundError('Sound was deleted or is unavailable',404)
   try:raw=(self.root/(ident+'.wav')).read_bytes()
   except OSError:raise SoundError('Sound file missing; restore library backup or reimport',404)
   if hashlib.sha256(raw).hexdigest()!=item['sha256']:raise SoundError('Stored sound checksum failed; preserve original and reimport',500)
   return raw,copy.deepcopy(item)
 def add(self,fields,raw,revision,permission,source):
  if permission is not True:raise SoundError('Confirm you have permission to store and use this audio')
  m=metadata(fields);info=validate_audio(raw)
  if not isinstance(source,str) or len(source)>400 or any(ord(c)<32 for c in source):raise SoundError('Invalid source description')
  with self.lock:
   data=self._load();self._revision(data,revision)
   if len(data['sounds'])>=64 or sum(s['bytes'] for s in data['sounds'])+len(raw)>64*1024*1024:raise SoundError('Library limit: 64 sounds / 64 MiB',413)
   self.root.mkdir(parents=True,exist_ok=True);ident=uuid.uuid4().hex;path=self.root/(ident+'.wav');temp=path.with_suffix('.tmp')
   with temp.open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
   os.replace(temp,path);data['sounds'].append({'id':ident,**m,**info,'source':source});data['revision']+=1
   try:self._save(data)
   except Exception:path.unlink(missing_ok=True);raise
   return copy.deepcopy(data)
 def edit(self,ident,fields,revision):
  m=metadata(fields)
  with self.lock:
   data=self._load();self._revision(data,revision);item=next((s for s in data['sounds'] if s['id']==ident),None)
   if not item:raise SoundError('Unknown sound',404)
   item.update(m);data['revision']+=1;self._save(data);return copy.deepcopy(data)
 def delete(self,ident,revision):
  with self.lock:
   data=self._load();self._revision(data,revision)
   if not any(s['id']==ident for s in data['sounds']):raise SoundError('Unknown sound',404)
   data['sounds']=[s for s in data['sounds'] if s['id']!=ident];data['revision']+=1;self._save(data)
   # Metadata commit first: a crash can leave an unreferenced file, never erase another clip.
   (self.root/(ident+'.wav')).unlink(missing_ok=True);return copy.deepcopy(data)
 def reorder(self,ids,revision):
  with self.lock:
   data=self._load();self._revision(data,revision)
   if not isinstance(ids,list) or not all(isinstance(i,str) for i in ids) or len(ids)!=len(data['sounds']) or set(ids)!={s['id'] for s in data['sounds']}:raise SoundError('Reorder must contain every sound exactly once')
   lookup={s['id']:s for s in data['sounds']};data['sounds']=[lookup[i] for i in ids];data['revision']+=1;self._save(data);return copy.deepcopy(data)
 def output(self,device,revision):
  with self.lock:
   data=self._load();self._revision(data,revision);data['output']=device;data['revision']+=1;self._save(data);return copy.deepcopy(data)
