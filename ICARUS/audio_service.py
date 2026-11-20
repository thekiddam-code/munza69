"""Conservative Sonar-compatible diagnostics and clip DSP, not a serial voice mixer."""
import collections,copy,json,math,os,threading,time
from sound_library import SoundError
from audio_capture import CaptureInput
from audio_loudness import measure,normalize
class AudioService:
 def __init__(self,sounds,capture=None):
  self.sounds=sounds;self.capture=capture or CaptureInput();self.lock=threading.RLock();self.capture_lock=threading.Lock();self.cancel=threading.Event();self.cache=collections.OrderedDict();self.path=sounds.library.root/'audio_profile.json';self.memory_disabled=False
 def profile(self):
  default={'version':1,'enabled':False,'offset_db':-3,'ceiling_dbfs':-1,'max_boost_db':6,'speech':None}
  if self.path.exists():
   try:
    value=json.loads(self.path.read_text('utf8'))
    if value.get('version')!=1:raise ValueError('Unsupported audio profile')
    default.update(value);self.validate(default)
   except Exception as e:raise SoundError('Audio profile unreadable; originals retained: '+str(e),409)
  if self.memory_disabled:default['enabled']=False
  return default
 def validate(self,p):
  if type(p.get('enabled'))!=bool:raise SoundError('Enabled must be boolean')
  for k,lo,hi in [('offset_db',-12,0),('ceiling_dbfs',-12,-1),('max_boost_db',0,6)]:
   v=p.get(k)
   if type(v) not in (int,float) or not math.isfinite(v) or not lo<=v<=hi:raise SoundError('Unsafe '+k)
  if p.get('speech') is not None:
   speech=p['speech']
   if not isinstance(speech,dict) or type(speech.get('integrated_lufs')) not in (int,float) or not math.isfinite(speech['integrated_lufs']) or not -60<=speech['integrated_lufs']<=-5:raise SoundError('Invalid speech calibration')
  if p['enabled'] and not p.get('speech'):raise SoundError('Measure a representative speaking sample before enabling normalization')
 def require_library(self):
  if not (self.sounds.library.root/'library.json').is_file():raise SoundError('Server soundboard_data/library.json is missing. Preserve/copy the existing library before calibration or profile changes.',409)
 def save(self,p):
  self.require_library()
  with self.sounds.library.lock:self.sounds.preserve_existing()
  self.validate(p);self.path.parent.mkdir(parents=True,exist_ok=True);tmp=self.path.with_suffix('.tmp')
  with tmp.open('w',encoding='utf8') as f:json.dump(p,f,indent=2);f.flush();os.fsync(f.fileno())
  os.replace(tmp,self.path);self.cache.clear()
 def view(self):
  inputs=self.capture.devices();outputs=self.sounds.player.backend.devices();sonar_in=[d for d in inputs if 'sonar' in d['name'].lower()];sonar_out=[d for d in outputs if 'sonar' in d['name'].lower()]
  return {'profile':self.profile(),'inputs':inputs,'outputs':outputs,'sonar_detected':bool(sonar_in or sonar_out),'sonar_inputs':sonar_in,'sonar_outputs':sonar_out,'capture_active':self.capture_lock.locked(),'game_chat_input':'User reports SteelSeries Sonar - Microphone; actual per-app input is not readable here.','windows_defaults':'Not modified; actual Windows defaults are not measured by this legacy endpoint API.','route_state':'Unverified / unchanged. Sonar Stream Mix can mix Mic and Aux independently of UMBRA; it requires an explicit external setup and per-app Sonar Stream input. UMBRA does not apply those persistent changes.','injection_verified':False,'device_note':'Legacy Windows device names can be truncated. No automatic physical/virtual source switching or default fallback.'}
 def update(self,data):
  if set(data)!={'enabled','offset_db','ceiling_dbfs','max_boost_db'}:raise SoundError('Unknown profile fields')
  with self.lock:
   p=self.profile();p.update(data);self.validate(p);self.save(p);self.memory_disabled=False;return self.profile()
 def calibrate(self,device,consent,save=True):
  if consent is not True:raise SoundError('Explicit local consent to a five-second microphone sample is required')
  self.require_library()
  if not self.capture_lock.acquire(blocking=False):raise SoundError('An input sample is already active',409)
  self.cancel=threading.Event()
  try:
   with self.sounds.library.lock:self.sounds.preserve_existing()
   if self.cancel.is_set():raise SoundError('Measurement cancelled before microphone opened',409)
   raw=self.capture.sample(device,5,self.cancel);metrics=measure(raw);del raw
   if self.cancel.is_set():raise SoundError('Measurement cancelled; no profile saved',409)
   if not save:return {'profile':self.profile(),'metrics':metrics,'privacy':'Level-only input/mix measurement. Calibration unchanged; samples discarded. A nonzero signal alone does not prove both voice and clips reached game chat.'}
   level=metrics['integrated_lufs']
   if level is None or level<-60 or level>-5 or metrics['gated_blocks']<5 or metrics['clipped_samples']>120:raise SoundError('Sample is silent, too quiet, clipped or unrepresentative. Speak normally and retry; previous calibration retained.',409)
   with self.lock:
    if self.cancel.is_set():raise SoundError('Measurement cancelled',409)
    p=self.profile();p['speech']={'integrated_lufs':level,'sample_peak_dbfs':metrics['sample_peak_dbfs'],'device':device,'measured_utc_seconds':time.time(),'method':metrics['method']};self.save(p)
   return {'profile':self.profile(),'metrics':metrics,'privacy':'Voice samples were analyzed in memory, not saved or transmitted. This does not change Sonar input selection or verify combined game chat.'}
  finally:self.capture_lock.release()
 def processed(self,raw,item,volume=None):
  p=self.profile()
  if not p['enabled']:return raw,item['volume'] if volume is None else volume,None
  value=item['volume'] if volume is None else volume
  key=(item['sha256'],json.dumps(p,sort_keys=True),value)
  with self.lock:
   if key in self.cache:self.cache.move_to_end(key);return self.cache[key]
  result,metrics=normalize(raw,p['speech']['integrated_lufs'],p['offset_db'],value,p['ceiling_dbfs'],p['max_boost_db']);out=(result,1.,metrics)
  with self.lock:
   self.cache[key]=out
   while len(self.cache)>4:self.cache.popitem(last=False)
  return out
 def close(self):
  self.cancel.set();self.sounds.player.stop()
  acquired=self.capture_lock.acquire(timeout=2)
  if acquired:self.capture_lock.release()
  with self.lock:self.cache.clear()
  return {'capture_cleanup_completed':acquired,'profile_preserved':True}
 def reset(self):
  self.cancel.set();self.memory_disabled=True;self.sounds.player.stop()
  with self.lock:
   p=self.profile();p['enabled']=False
   try:
    if self.path.exists():self.save(p)
    self.cache.clear();error=None
   except Exception as e:error=str(e)
  return {'stopped':True,'normalization_disabled':True,'capture_cancellation_requested':True,'settings_error':error,'voice_route':'No Windows/Sonar/default setting was ever owned or changed. External manual routing is not reverted.'}
