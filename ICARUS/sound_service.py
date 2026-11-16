"""Authenticated-handler operations; caller owns existing pairing/origin checks."""
import base64,threading,time
from sound_library import SoundLibrary,SoundError
from sound_output import SoundPlayer
from sound_import import import_page
class SoundService:
 def __init__(self,root,backend=None):self.library=SoundLibrary(root);self.player=SoundPlayer(self.library,backend);self.commands=threading.Lock();self.imports=threading.BoundedSemaphore(2);self.rates={};self.rate_lock=threading.Lock()
 def view(self):
  try:devices=self.player.backend.devices();error=None
  except Exception as e:devices=[];error=str(e)[:160]
  return {**self.library.view(),'devices':devices,'player':self.player.view(),'deviceError':error,'routing':'Normal playback: explicit Windows render output. Private preview: current terminal only. Game-chat injection pending 4.8C.'}
 def post(self,operation,data,owner):
  if not isinstance(data,dict):raise SoundError('Sound request object required')
  fields={'import':{'fields','audio','revision','permission','source'},'edit':{'id','fields','revision'},'delete':{'id','revision'},'reorder':{'ids','revision'},'output':{'device','revision'},'play':{'id','requestId'},'stop':set(),'link':{'url','permission'}}
  if operation not in fields or set(data)!=fields[operation]:raise SoundError('Unknown operation or unsupported sound fields')
  lib=self.library
  if operation=='import':
   if not isinstance(data['audio'],str) or len(data['audio'])>1920060:raise SoundError('Audio import too large',413)
   try:raw=base64.b64decode(data['audio'],validate=True)
   except Exception:raise SoundError('Invalid audio encoding')
   return lib.add(data['fields'],raw,data['revision'],data['permission'],data['source'])
  if operation=='edit':return lib.edit(data['id'],data['fields'],data['revision'])
  if operation=='delete':return lib.delete(data['id'],data['revision'])
  if operation=='reorder':return lib.reorder(data['ids'],data['revision'])
  if operation=='link':
   with self.rate_lock:
    now=time.monotonic();self.rates={k:v for k,v in self.rates.items() if now-v[-1]<60};times=[t for t in self.rates.get(owner,[]) if now-t<60]
    if len(times)>=4 or len(self.rates)>128:raise SoundError('Import rate limit reached; wait a minute',429)
    self.rates[owner]=times+[now]
   if not self.imports.acquire(blocking=False):raise SoundError('Two imports already active; retry shortly',429)
   try:return import_page(data['url'],data['permission'])
   finally:self.imports.release()
  with self.commands:
   if operation=='play':return self.player.play(data['id'],owner,data['requestId'])
   if operation=='stop':self.player.stop();return self.player.view()
   device=data['device']
   if not isinstance(device,dict) or set(device)!={'id','name'} or type(device['id'])!=int or device not in self.player.backend.devices():raise SoundError('Select an available Windows render output')
   self.player.stop();return lib.output(device,data['revision'])
