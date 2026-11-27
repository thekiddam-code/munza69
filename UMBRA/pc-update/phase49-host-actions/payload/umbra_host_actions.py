"""Paired-only Sonar playback routing and observable Moments capture requests.
No driver, recording engine, microphone/VoiceMeeter controls, or arbitrary commands.
"""
import ctypes,json,os,re,ssl,threading,time,urllib.request,urllib.parse,urllib.error,uuid
from pathlib import Path

OUTPUTS=('game','chat','media','aux')
class HostActionError(Exception):
 def __init__(self,message,status=400,details=None):super().__init__(message);self.status=status;self.details=details or {}

def valid_id(value):return isinstance(value,str) and 0<len(value)<=512 and not any(ord(c)<32 for c in value)
def atomic_json(path,data):
 temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
 try:
  with temp.open('w',encoding='utf8') as f:json.dump(data,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
  os.replace(temp,path)
 finally:temp.unlink(missing_ok=True)

def loopback_url(value,scheme=None):
 if not isinstance(value,str):raise HostActionError('GG local address unavailable.',503)
 if any(ord(c)<=32 for c in value):raise HostActionError('Malformed local GG address.',503)
 if '://' not in value:value=(scheme or 'http')+'://'+value
 try:
  u=urllib.parse.urlsplit(value)
  if u.scheme not in ('http','https') or u.hostname not in ('localhost','127.0.0.1','::1') or not u.port or u.username or u.password or u.path not in ('','/') or u.query or u.fragment:raise ValueError()
 except ValueError:raise HostActionError('Refusing a non-loopback or malformed GG address.',503)
 return urllib.parse.urlunsplit((u.scheme,('127.0.0.1:'+str(u.port)) if u.hostname=='localhost' else u.netloc,'','',''))
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None
class LocalSonar:
 """GG's internal localhost interface; its shape is checked before any write."""
 def __init__(self,program_data=None):self.program_data=Path(program_data or os.environ.get('PROGRAMDATA',r'C:\ProgramData'))
 def request(self,base,path,method='GET'):
  base=loopback_url(base)
  # Self-signed GG Core TLS is accepted ONLY after strict loopback validation.
  opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect(),urllib.request.HTTPSHandler(context=ssl._create_unverified_context()))
  try:
   with opener.open(urllib.request.Request(base+path,method=method,data=b'' if method=='PUT' else None),timeout=1.5) as r:
    data=r.read(1048577)
    if len(data)>1048576:raise HostActionError('GG response is too large.',503)
    return json.loads(data) if data else None
  except urllib.error.HTTPError as e:raise HostActionError('GG local API returned HTTP '+str(e.code)+'.',e.code)
  except (OSError,ValueError):raise HostActionError('GG local API is unavailable or its response changed.',503)
 def discover(self):
  props=None
  for relative in ('SteelSeries/GG/coreProps.json','SteelSeries/SteelSeries Engine 3/coreProps.json'):
   path=self.program_data/relative
   if path.is_file():
    try:
     if path.stat().st_size>65536:raise ValueError()
     props=json.loads(path.read_text('utf-8-sig'));break
    except (ValueError,OSError):raise HostActionError('GG discovery file is unreadable.',503)
  if not props:raise HostActionError('SteelSeries GG is not discovered. Start GG and Sonar on the PC.',503)
  core=loopback_url(props.get('ggEncryptedAddress'),scheme='https')
  sub=self.request(core,'/subApps')
  try:
   sonar=sub['subApps']['sonar']
   if any(sonar.get(k) is False for k in ('isEnabled','isReady','isRunning')):raise ValueError()
   base=loopback_url(sonar['metadata']['webServerAddress'])
  except (KeyError,TypeError,ValueError):raise HostActionError('Sonar is not ready in GG.',503)
  if self.request(base,'/mode')!='classic':raise HostActionError('Four per-channel playback routes require Sonar Classic mode. No mode or stream settings were changed.',409)
  prefix=None
  for candidate in ('/classicRedirections','/ClassicRedirections'):
   try:routes=self.request(base,candidate);prefix=candidate;break
   except HostActionError as e:
    if e.status!=404:raise
  if prefix is None:raise HostActionError('This GG version does not expose the known playback routing API.',503)
  return base,prefix,self.routes(routes),self.request(base,'/audioDevices')
 @staticmethod
 def routes(rows):
  if not isinstance(rows,list) or len(rows)>32:raise HostActionError('Sonar routing response changed; nothing will be guessed.',503)
  result={}
  for r in rows:
   if not isinstance(r,dict) or not isinstance(r.get('id'),str) or r['id'] in result:raise HostActionError('Invalid Sonar route response.',503)
   result[r['id']]=r.get('deviceId')
  if not all(valid_id(result.get(k)) for k in OUTPUTS+('mic',)):raise HostActionError('Sonar must report all four outputs and microphone before routing can be verified.',503)
  return result
 def read_routes(self,base,prefix):return self.routes(self.request(base,prefix))
 def set_route(self,base,prefix,channel,device):
  if channel not in OUTPUTS or not valid_id(device):raise HostActionError('Only the four playback routes are writable.')
  self.request(base,prefix+'/'+channel+'/deviceId/'+urllib.parse.quote(device,safe=''),'PUT')

def candidates(rows):
 if not isinstance(rows,list) or len(rows)>512:raise HostActionError('Sonar playback device response changed.',503)
 result=[]
 for row in rows:
  if not isinstance(row,dict):raise HostActionError('Invalid Sonar device response.',503)
  name=row.get('friendlyName');ident=row.get('id')
  if row.get('dataFlow')=='render' and row.get('role')=='none' and valid_id(ident) and isinstance(name,str) and 'arctis' in name.lower() and not any(s in name.lower() for s in ('voicemeeter','sonar','microphone')):
   if row.get('state','active') not in ('active','Active',1) or row.get('isAvailable') is False:continue
   result.append({'id':ident,'name':name[:120]})
 if len({r['id'] for r in result})!=len(result):raise HostActionError('Duplicate Sonar device identities.',503)
 return result

KEYS={'ctrl':0x11,'ctrlleft':0xA2,'ctrlright':0xA3,'shift':0x10,'shiftleft':0xA0,'shiftright':0xA1,'alt':0x12,'altleft':0xA4,'altright':0xA5,'win':0x5B,'winleft':0x5B,'winright':0x5C,'enter':0x0D,'space':0x20,'tab':0x09,'esc':0x1B,'left':0x25,'up':0x26,'right':0x27,'down':0x28}
KEYS.update({chr(i).lower():i for i in range(0x41,0x5B)});KEYS.update({str(i):0x30+i for i in range(10)});KEYS.update({'f'+str(i):0x6F+i for i in range(1,25)})
def binding(cfg):
 keys=cfg.get('macros',{}).get('Save Clip')
 if not isinstance(keys,list) or not 1<=len(keys)<=4 or any(not isinstance(k,str) or k.lower() not in KEYS for k in keys) or len(set(k.lower() for k in keys))!=len(keys):raise HostActionError('Configure the Save Clip macro in the existing PC config/editor with 1–4 supported keyboard keys. Its binding is read from the host on every request.',409)
 return [k.lower() for k in keys]
class ScanCodeSender:
 def send(self,keys):
  if os.name!='nt':raise HostActionError('Moments input requires the Windows companion.',503)
  user32=ctypes.WinDLL('user32',use_last_error=True)
  class Mouse(ctypes.Structure):_fields_=[('dx',ctypes.c_int32),('dy',ctypes.c_int32),('mouseData',ctypes.c_uint32),('flags',ctypes.c_uint32),('time',ctypes.c_uint32),('extra',ctypes.c_size_t)]
  class Key(ctypes.Structure):_fields_=[('vk',ctypes.c_uint16),('scan',ctypes.c_uint16),('flags',ctypes.c_uint32),('time',ctypes.c_uint32),('extra',ctypes.c_size_t)]
  class Hardware(ctypes.Structure):_fields_=[('msg',ctypes.c_uint32),('low',ctypes.c_uint16),('high',ctypes.c_uint16)]
  class Union(ctypes.Union):_fields_=[('mouse',Mouse),('key',Key),('hardware',Hardware)]
  class Input(ctypes.Structure):_fields_=[('type',ctypes.c_uint32),('data',Union)]
  if ctypes.sizeof(Input)!=(40 if ctypes.sizeof(ctypes.c_void_p)==8 else 28):raise HostActionError('Unsupported Windows input structure.',503)
  user32.SendInput.argtypes=(ctypes.c_uint,ctypes.POINTER(Input),ctypes.c_int);user32.SendInput.restype=ctypes.c_uint
  user32.MapVirtualKeyW.argtypes=(ctypes.c_uint,ctypes.c_uint);user32.MapVirtualKeyW.restype=ctypes.c_uint
  user32.GetAsyncKeyState.argtypes=(ctypes.c_int,);user32.GetAsyncKeyState.restype=ctypes.c_short
  if any(user32.GetAsyncKeyState(v)&0x8000 for v in set([0x10,0x11,0x12,0x5B,0x5C]+[KEYS[k] for k in keys])):raise HostActionError('Release the shortcut keys and modifiers before requesting a clip.',409)
  scans=[]
  for key in keys:
   value=user32.MapVirtualKeyW(KEYS[key],4)
   if not value:raise HostActionError('Windows cannot map this saved key binding.',409)
   scans.append((value&255,1 if value>>8==0xE0 else 0))
  def send(events):
   entries=(Input*len(events))(*(Input(1,Union(key=Key(0,scan,8|extended|(2 if up else 0),0,0))) for scan,extended,up in events))
   return user32.SendInput(len(entries),entries,ctypes.sizeof(Input))
  inserted=0
  try:
   inserted=send([(scan,ext,False) for scan,ext in scans])
   if inserted!=len(scans):raise HostActionError('Windows rejected some input. Check the PC session and matching GG/game/companion integrity levels; no elevation was attempted.',503)
   time.sleep(.08)
  finally:
   releases=[(scan,ext,True) for scan,ext in reversed(scans[:inserted])]
   if releases:
    released=send(releases)
    if released<len(releases) and send(releases[released:])!=len(releases)-released:raise HostActionError('Windows did not acknowledge all shortcut key releases. Inspect the physical keyboard state.',503)

class HostActions:
 def __init__(self,root,get_cfg,config_lock,sonar=None,sender=None,clip_timeout=30,poll_interval=1):
  self.root=Path(root);self.file=self.root/'umbra_host_actions.json';self.get_cfg=get_cfg;self.config_lock=config_lock
  self.sonar=sonar or LocalSonar();self.sender=sender or ScanCodeSender();self.timeout=clip_timeout;self.interval=poll_interval
  self.lock=threading.RLock();self.results={};self.clip_active=False
 def settings(self):
  if not self.file.exists():return {}
  try:
   if self.file.is_symlink() or self.file.stat().st_size>65536:raise ValueError()
   result=json.loads(self.file.read_text('utf8'));assert isinstance(result,dict);return result
  except (OSError,ValueError,AssertionError):raise HostActionError('Host action settings are unreadable. Retain the file and repair it locally.',409)
 def remember(self,device):
  with self.config_lock:
   data=self.settings();data['arctis_output']=device;atomic_json(self.file,data)
 def route_arctis(self,data):
  base,prefix,before,devices=self.sonar.discover();choices=candidates(devices)
  if not choices:raise HostActionError('No available physical Arctis playback output was reported by Sonar. No route changed.',409)
  selected=data.get('output_id');saved=self.settings().get('arctis_output',{})
  if not isinstance(saved,dict):raise HostActionError('Saved Arctis identity is invalid. Repair local host settings first.',409)
  target=next((c for c in choices if c['id']==selected),None) if selected is not None else next((c for c in choices if c['id']==saved.get('id')),None)
  if selected is not None and target is None:raise HostActionError('The selected Arctis output is no longer available. Refresh and choose again.',409,{'state':'selection_required','outputs':choices})
  if target is None and len(choices)==1:target=choices[0]
  if target is None:return {'state':'selection_required','outputs':choices,'verified':False,'message':'Choose an Arctis playback output. No routes changed.'}
  changed=[]
  try:
   for channel in OUTPUTS:
    if before[channel]!=target['id']:
     # Record the attempt before sending: a transport timeout can occur after GG applied it.
     changed.append(channel);self.sonar.set_route(base,prefix,channel,target['id'])
   after=self.sonar.read_routes(base,prefix)
   if after['mic']!=before['mic']:raise HostActionError('Microphone route changed externally during routing; UMBRA never writes it.',409)
   if not all(after[k]==target['id'] for k in OUTPUTS):raise HostActionError('Sonar did not confirm all four playback routes.',503)
  except Exception as error:
   rollback={}
   try:
    current=self.sonar.read_routes(base,prefix)
    for channel in reversed(changed):
     if current[channel]==target['id']:
      try:self.sonar.set_route(base,prefix,channel,before[channel]);rollback[channel]='restored'
      except Exception:rollback[channel]='unconfirmed'
     else:rollback[channel]='not overwritten (changed externally or not applied)'
   except Exception:rollback={'status':'unconfirmed; inspect Sonar'}
   try:current=self.sonar.read_routes(base,prefix)
   except Exception:current={}
   raise HostActionError(str(error) if isinstance(error,HostActionError) else 'Sonar routing failed. Inspect its current output routes.',503,{'verified':False,'routes':{k:current.get(k) for k in OUTPUTS},'rollback':rollback})
  remembered=True
  try:self.remember(target)
  except (OSError,HostActionError):remembered=False
  return {'state':'verified','verified':True,'output':target,'routes':{k:after[k] for k in OUTPUTS},'microphone_preserved':True,'remembered':remembered,'message':'Sonar confirmed Game, Chat, Media and Aux on '+target['name']+'.'+(' Output remembered.' if remembered else ' Output preference could not be saved.')}
 def _prune(self):
  cutoff=time.monotonic()-600
  for key,item in list(self.results.items()):
   if item['time']<cutoff and item['result'].get('state')!='pending':self.results.pop(key)
  while len(self.results)>32:
   key=next((k for k,v in self.results.items() if v['result'].get('state')!='pending'),None)
   if key is None:break
   self.results.pop(key)
 def post(self,path,data,owner):
  if not isinstance(data,dict):raise HostActionError('Expected a command object.')
  if path=='/api/host-actions/status':
   if data:raise HostActionError('Status accepts no fields.')
   settings=self.settings()
   try:binding(self.get_cfg());configured=True
   except HostActionError:configured=False
   return {'version':1,'save_clip_macro_configured':configured,'clip_verification_configured':bool(settings.get('moments_clip_directory')),'capture_active':None}
  if set(data)-({'requestId','output_id'} if path=='/api/sonar/arctis' else {'requestId'}):raise HostActionError('Unknown command fields.')
  try:ident=data['requestId'];uuid.UUID(ident);assert isinstance(ident,str) and len(ident)==36
  except (KeyError,ValueError,TypeError,AttributeError,AssertionError):raise HostActionError('A UUID requestId is required.')
  if not isinstance(owner,str) or not owner:raise HostActionError('Pair first.',401)
  key=(owner,ident)
  with self.lock:
   self._prune()
   if path=='/api/moments/clip-status':
    item=self.results.get(key)
    if not item or item['path']!='/api/moments/save-clip':raise HostActionError('Clip request is unknown or expired. No hotkey was replayed.',404)
    return dict(item['result'])
   old=self.results.get(key)
   if old:
    if old['path']!=path or old['data']!=data:raise HostActionError('Request ID already belongs to a different command.',409)
    return dict(old['result'])
   if path=='/api/sonar/arctis':
    if 'output_id' in data and not valid_id(data['output_id']):raise HostActionError('Invalid output identity.')
    try:result=self.route_arctis(data)
    except HostActionError as e:
     result={'state':'error','verified':False,'error':str(e),**e.details}
     self.results[key]={'time':time.monotonic(),'path':path,'data':dict(data),'result':result}
     return result
   elif path=='/api/moments/save-clip':
    if self.clip_active:raise HostActionError('A clip request is still being checked. No second shortcut was sent.',429)
    keys=binding(self.get_cfg());settings=self.settings();directory=settings.get('moments_clip_directory')
    if not isinstance(directory,str) or not directory:raise HostActionError('Set the Moments storage folder with configure_host_actions.py on the PC before clip verification. No shortcut was sent.',409)
    folder=Path(directory)
    if not folder.is_absolute() or not folder.is_dir() or folder.is_symlink():raise HostActionError('The configured Moments storage folder is unavailable. No shortcut was sent.',409)
    baseline=self.snapshot(folder)
    self.sender.send(keys)
    result={'request_id':ident,'state':'pending','hotkey_sent':True,'clip_file_verified':False,'capture_active':None,'message':'Saved host binding sent through Windows scan-code input. Waiting for a new Moments clip file; capture must already be active.'}
    self.clip_active=True
    self.results[key]={'time':time.monotonic(),'path':path,'data':dict(data),'result':result}
    threading.Thread(target=self.watch,args=(key,folder,baseline),daemon=True).start()
    return dict(result)
   else:raise HostActionError('Unknown host action.',404)
   self.results[key]={'time':time.monotonic(),'path':path,'data':dict(data),'result':result};self._prune();return dict(result)
 @staticmethod
 def snapshot(folder):
  result={};seen=0;stack=[(folder,0)]
  while stack:
   parent,depth=stack.pop()
   try:
    with os.scandir(parent) as entries:
     for entry in entries:
      seen+=1
      if seen>20000:raise HostActionError('Moments folder verification limit reached. Choose the actual clip folder rather than a larger parent.',409)
      stat=entry.stat(follow_symlinks=False)
      if entry.is_symlink() or getattr(stat,'st_file_attributes',0)&0x400:continue
      if entry.is_dir(follow_symlinks=False):
       if depth>=5:raise HostActionError('Moments folder is too deeply nested to verify safely.',409)
       stack.append((Path(entry.path),depth+1))
      elif entry.is_file(follow_symlinks=False) and Path(entry.name).suffix.lower() in ('.mp4','.mkv','.webm'):
       result[str(Path(entry.path).relative_to(folder))]=(stat.st_size,stat.st_mtime_ns)
   except OSError:raise HostActionError('Moments clip directory could not be inspected completely.',503)
  return result
 def watch(self,key,folder,baseline):
  deadline=time.monotonic()+self.timeout;stable={};result=None
  try:
   while time.monotonic()<deadline:
    time.sleep(self.interval)
    current=self.snapshot(folder)
    for name,signature in current.items():
     if name in baseline or signature[0]<24:continue
     if stable.get(name)==signature:
      candidate=(folder/name).resolve()
      if not candidate.is_relative_to(folder.resolve()) or candidate.is_symlink():continue
      with candidate.open('rb') as stream:header=stream.read(12)
      if not (header[4:8]==b'ftyp' or header[:4]==b'\x1aE\xdf\xa3'):continue
      result={'request_id':key[1],'state':'clip_detected','hotkey_sent':True,'clip_file_verified':True,'capture_active':None,'clip':{'name':Path(name).name,'bytes':signature[0]},'message':'New stable video file detected in the configured Moments folder. Confirm the clip in Moments; an overlapping automatic clip cannot be attributed to this request.'};return
    stable=current
   result={'request_id':key[1],'state':'unverified','hotkey_sent':True,'clip_file_verified':False,'capture_active':None,'message':'No new stable clip file was detected. Check active Moments capture, saved binding, storage location and session/integrity levels. Input acknowledgment is not clip confirmation.'}
  except Exception:
   result={'request_id':key[1],'state':'unverified','hotkey_sent':True,'clip_file_verified':False,'capture_active':None,'message':'Clip verification could not finish. Inspect Moments; no shortcut will be replayed automatically.'}
  finally:
   with self.lock:
    if key in self.results:self.results[key]['result']=result or {'state':'unverified','clip_file_verified':False,'message':'Clip status unknown.'}
    self.clip_active=False
