"""Render-only Windows waveOut. Never opens/captures a recording device or changes defaults."""
import array,ctypes,io,platform,threading,time,wave
from ctypes import wintypes as W
from sound_library import SoundError
class Format(ctypes.Structure):_pack_=1;_fields_=[('tag',W.WORD),('channels',W.WORD),('rate',W.DWORD),('avg',W.DWORD),('align',W.WORD),('bits',W.WORD),('extra',W.WORD)]
class Header(ctypes.Structure):_fields_=[('data',ctypes.c_void_p),('length',W.DWORD),('recorded',W.DWORD),('user',ctypes.c_size_t),('flags',W.DWORD),('loops',W.DWORD),('next',ctypes.c_void_p),('reserved',ctypes.c_size_t)]
class Caps(ctypes.Structure):_fields_=[('mid',W.WORD),('pid',W.WORD),('version',W.DWORD),('name',W.WCHAR*32),('formats',W.DWORD),('channels',W.WORD),('reserved',W.WORD),('support',W.DWORD)]
class WaveOutput:
 def __init__(self):self.leaked=None
 def api(self):
  if platform.system()!='Windows':raise SoundError('Windows sound output unavailable on this host',503)
  api=ctypes.WinDLL('winmm');api.waveOutGetNumDevs.restype=W.UINT
  api.waveOutGetDevCapsW.argtypes=[ctypes.c_size_t,ctypes.POINTER(Caps),W.UINT]
  api.waveOutOpen.argtypes=[ctypes.POINTER(W.HANDLE),W.UINT,ctypes.POINTER(Format),ctypes.c_size_t,ctypes.c_size_t,W.DWORD]
  for name in ('waveOutPrepareHeader','waveOutWrite','waveOutUnprepareHeader'):getattr(api,name).argtypes=[W.HANDLE,ctypes.POINTER(Header),W.UINT]
  api.waveOutReset.argtypes=[W.HANDLE];api.waveOutClose.argtypes=[W.HANDLE];return api
 def devices(self):
  if platform.system()!='Windows':return []
  api=self.api();out=[]
  for i in range(min(api.waveOutGetNumDevs(),64)):
   caps=Caps()
   if api.waveOutGetDevCapsW(i,ctypes.byref(caps),ctypes.sizeof(caps))==0:out.append({'id':i,'name':caps.name})
  return out
 def play(self,raw,device,volume,stop,started):
  if self.leaked:raise SoundError('Windows driver did not release a previous buffer; restart the server before further playback',503)
  if device not in self.devices():raise SoundError('Selected output changed or disappeared. Select its current identity again.',409)
  if stop.is_set():return
  api=self.api();handle=W.HANDLE();fmt=Format(1,1,24000,48000,2,16,0)
  with wave.open(io.BytesIO(raw),'rb') as f:pcm=array.array('h',f.readframes(f.getnframes()))
  # Clip-local gain and short fades, not microphone/perceived-loudness normalization.
  n=len(pcm)
  for i in range(n):pcm[i]=round(pcm[i]*volume*min(1,i/240,(n-1-i)/240))
  buffer=ctypes.create_string_buffer(pcm.tobytes());header=Header(ctypes.cast(buffer,ctypes.c_void_p),n*2,0,0,0,0,None,0);prepared=False
  if stop.is_set():return
  code=api.waveOutOpen(ctypes.byref(handle),device['id'],ctypes.byref(fmt),0,0,0)
  if code:raise SoundError('Windows could not open the selected render output (MMRESULT '+str(code)+')',503)
  try:
   code=api.waveOutPrepareHeader(handle,ctypes.byref(header),ctypes.sizeof(header))
   if code:raise SoundError('Audio buffer preparation failed: '+str(code),503)
   prepared=True;code=api.waveOutWrite(handle,ctypes.byref(header),ctypes.sizeof(header))
   if code:raise SoundError('Windows rejected playback: '+str(code),503)
   started();deadline=time.monotonic()+32
   while not header.flags&1 and not stop.wait(.02):
    if time.monotonic()>deadline:raise SoundError('Audio driver completion timed out',503)
  finally:
   api.waveOutReset(handle)
   if prepared:
    for _ in range(50):
     code=api.waveOutUnprepareHeader(handle,ctypes.byref(header),ctypes.sizeof(header))
     if code==0:break
     time.sleep(.02)
    if code:self.leaked=(api,handle,header,buffer);raise SoundError('Driver retained audio buffer; playback disabled until restart',503)
   code=api.waveOutClose(handle)
   if code:self.leaked=(api,handle,header,buffer);raise SoundError('Audio output did not close; restart server',503)
class SoundPlayer:
 def __init__(self,library,backend=None):self.library=library;self.backend=backend or WaveOutput();self.lock=threading.RLock();self.thread=None;self.cancel=threading.Event();self.status={'state':'idle','error':None};self.receipts={}
 def view(self):
  with self.lock:return dict(self.status)
 def stop(self):
  with self.lock:self.cancel.set();t=self.thread
  if t and t.is_alive():t.join(timeout=2)
  if t and t.is_alive():raise SoundError('Output is still stopping; no new playback allowed',503)
  with self.lock:self.status={'state':'idle','error':None}
 def play(self,ident,owner,request):
  import re
  if not isinstance(request,str) or not re.fullmatch(r'[A-Za-z0-9_-]{8,80}',request):raise SoundError('Valid requestId required')
  with self.lock:
   now=time.monotonic();self.receipts={k:v for k,v in self.receipts.items() if now-v[0]<120};key=(owner,request)
   if key in self.receipts:
    if self.receipts[key][1]!=ident:raise SoundError('Conflicting request ID',409)
    return {**self.view(),'duplicate':True}
  raw,item=self.library.get(ident);device=self.library.view()['output']
  if not device:raise SoundError('Select an explicit Windows render output first. Game-chat injection is not configured in Phase 4.8B.',409)
  if device not in self.backend.devices():raise SoundError('Selected output is unavailable; select again',409)
  self.stop();ready=threading.Event()
  with self.lock:
   self.cancel=threading.Event();cancel=self.cancel;self.status={'state':'starting','id':ident,'output':device,'error':None}
   def started():
    with self.lock:self.status['state']='playing'
    ready.set()
   def run():
    try:
     self.backend.play(raw,device,item['volume'],cancel,started)
     with self.lock:self.status['state']='idle'
    except Exception as e:
     with self.lock:self.status.update(state='error',error=str(e)[:220])
    finally:ready.set()
   self.thread=threading.Thread(target=run,daemon=True,name='umbra-sound-render');self.thread.start()
  ready.wait(2)
  with self.lock:
   if self.status['state']=='error':raise SoundError(self.status['error'],503)
   if len(self.receipts)>=128:self.receipts.pop(next(iter(self.receipts)))
   self.receipts[key]=(now,ident);return self.view()
