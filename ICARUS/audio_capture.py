"""Explicit, bounded parallel input sampling; never a serial microphone path or recording archive."""
import ctypes,io,platform,time,wave
from ctypes import wintypes as W
from sound_output import Format,Header,Caps
from sound_library import SoundError
class CaptureInput:
 def api(self):
  if platform.system()!='Windows':raise SoundError('Windows input measurement unavailable on this host',503)
  a=ctypes.WinDLL('winmm');a.waveInGetNumDevs.restype=W.UINT;a.waveInGetDevCapsW.argtypes=[ctypes.c_size_t,ctypes.POINTER(Caps),W.UINT];a.waveInOpen.argtypes=[ctypes.POINTER(W.HANDLE),W.UINT,ctypes.POINTER(Format),ctypes.c_size_t,ctypes.c_size_t,W.DWORD]
  for name in ('waveInPrepareHeader','waveInAddBuffer','waveInUnprepareHeader'):getattr(a,name).argtypes=[W.HANDLE,ctypes.POINTER(Header),W.UINT]
  for name in ('waveInStart','waveInStop','waveInReset','waveInClose'):getattr(a,name).argtypes=[W.HANDLE]
  return a
 def devices(self):
  if platform.system()!='Windows':return []
  a=self.api();out=[]
  for i in range(min(a.waveInGetNumDevs(),64)):
   caps=Caps()
   if a.waveInGetDevCapsW(i,ctypes.byref(caps),ctypes.sizeof(caps))==0:
    name=caps.name;virtual=any(k in name.lower() for k in ('sonar','virtual','cable','voicemeeter'));out.append({'id':i,'name':name,'kind':'known virtual name' if virtual else 'unclassified input; confirm physical device locally'})
  return out
 def sample(self,device,seconds,cancel):
  if device not in self.devices():raise SoundError('Selected capture endpoint changed; reselect it',409)
  if seconds!=5:raise SoundError('Calibration uses a fixed five-second sample')
  if getattr(self,'retained',None):raise SoundError('Input driver retained a buffer; restart required',503)
  if cancel.is_set():raise SoundError('Input measurement cancelled before opening',409)
  a=self.api();handle=W.HANDLE();fmt=Format(1,1,24000,48000,2,16,0);buffer=ctypes.create_string_buffer(seconds*48000);hdr=Header(ctypes.cast(buffer,ctypes.c_void_p),seconds*48000,0,0,0,0,None,0);prepared=False
  def check(code):
   if code:raise SoundError('Windows input sampling failed ('+str(code)+'); existing voice settings were not changed',503)
  check(a.waveInOpen(ctypes.byref(handle),device['id'],ctypes.byref(fmt),0,0,0))
  try:
   if cancel.is_set():raise SoundError('Input measurement cancelled',409)
   check(a.waveInPrepareHeader(handle,ctypes.byref(hdr),ctypes.sizeof(hdr)));prepared=True;check(a.waveInAddBuffer(handle,ctypes.byref(hdr),ctypes.sizeof(hdr)));
   if cancel.is_set():raise SoundError('Input measurement cancelled',409)
   check(a.waveInStart(handle));deadline=time.monotonic()+seconds+2
   while not hdr.flags&1:
    if cancel.wait(.02):raise SoundError('Input measurement cancelled; voice sample discarded',409)
    if time.monotonic()>deadline:raise SoundError('Input measurement timed out',503)
   if cancel.is_set():raise SoundError('Input measurement cancelled',409)
   if hdr.recorded<seconds*48000:raise SoundError('Incomplete microphone sample; no calibration saved',409)
   raw=bytes(buffer.raw[:seconds*48000]);b=io.BytesIO()
   with wave.open(b,'wb') as f:f.setparams((1,2,24000,0,'NONE','not compressed'));f.writeframes(raw)
   return b.getvalue()
  finally:
   a.waveInStop(handle);a.waveInReset(handle)
   if prepared:
    code=1
    for _ in range(50):
     code=a.waveInUnprepareHeader(handle,ctypes.byref(hdr),ctypes.sizeof(hdr))
     if code==0:break
     time.sleep(.02)
    if code:self.retained=(a,handle,hdr,buffer);raise SoundError('Input driver retained a buffer; further measurement disabled',503)
   if a.waveInClose(handle):self.retained=(a,handle,hdr,buffer);raise SoundError('Input driver did not close; restart before sampling again',503)
