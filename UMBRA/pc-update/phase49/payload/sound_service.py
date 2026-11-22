"""Authenticated-handler operations; caller owns existing pairing/origin checks."""
import base64,threading,time
from sound_library import SoundLibrary,SoundError,MAX_SOUNDS,MAX_LIBRARY_BYTES
from sound_output import SoundPlayer
from sound_import import import_page
from sound_backup import backup,inventory
class SoundService:
 def __init__(self,root,backend=None):self.library=SoundLibrary(root);self.player=SoundPlayer(self.library,backend);self.commands=threading.Lock();self.imports=threading.BoundedSemaphore(2);self.rates={};self.rate_lock=threading.Lock();self.preservation_lock=threading.RLock();self.preservation=None
 def preserve_existing(self):
  with self.preservation_lock:
   if self.preservation is None:
    try:
     result=backup(self.library.root)
     if result['source']['errors']:raise ValueError('; '.join(result['source']['errors']))
     self.preservation=result if result['created'] else None
    except Exception as e:raise SoundError('Verified backup required before changes: '+str(e),409)
   return self.preservation
 def make_backup(self):
  with self.commands,self.library.lock:
   try:
    result=backup(self.library.root)
    if not result['source']['errors']:self.preservation=result if result['created'] else None
    return result
   except Exception as e:raise SoundError('Backup failed; originals kept: '+str(e),409)
 def view(self):
  try:devices=self.player.backend.devices();error=None
  except Exception as e:devices=[];error=str(e)[:160]
  extra={}
  if getattr(self.player,'profile_reader',None):
   try:extra={'audio_profile':self.player.profile_reader()}
   except SoundError as e:extra={'audio_profile':{'enabled':False,'invalid':True},'audio_error':str(e)}
  return {'limits':{'max_sounds':MAX_SOUNDS,'max_audio_bytes':MAX_LIBRARY_BYTES},**extra,**self.library.view(),'devices':devices,'player':self.player.view(),'deviceError':error,'storage':{'authority':'Windows companion server','folder':'soundboard_data','metadata':'library.json','library_present':(self.library.root/'library.json').is_file(),'audio':'<sound-id>.wav','browser':'cache only','backup':self.preservation},'routing':'Normal playback: explicit Windows render output. Private preview: current terminal only. Game-chat injection pending 4.8C.'}
 def post(self,operation,data,owner):
  if not isinstance(data,dict):raise SoundError('Sound request object required')
  fields={'backup':set(),'import':{'fields','audio','revision','permission','source'},'edit':{'id','fields','revision'},'delete':{'id','revision'},'reorder':{'ids','revision'},'output':{'device','revision'},'play':{'id','requestId'},'stop':set(),'link':{'url','permission'}}
  allowed=fields.get(operation,set())|({'skip_duplicate'} if operation=='import' and 'skip_duplicate' in data else set())
  if operation not in fields or set(data)!=allowed:raise SoundError('Unknown operation or unsupported sound fields')
  lib=self.library
  if operation=='backup':return self.make_backup()
  if operation in ('import','edit','delete','reorder','output'):
   with self.library.lock:self.preserve_existing()
  if operation=='import':
   if not isinstance(data['audio'],str) or len(data['audio'])>1920060:raise SoundError('Audio import too large',413)
   try:raw=base64.b64decode(data['audio'],validate=True)
   except Exception:raise SoundError('Invalid audio encoding')
   return lib.add(data['fields'],raw,data['revision'],data['permission'],data['source'],data.get('skip_duplicate',False))
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
