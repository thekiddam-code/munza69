"""Bounded existing-TV transport and explicit, volatile UMBRA sleep countdown.
No native TV timer, power-on, application launch, host shutdown or arbitrary keys.
"""
import threading,time

class TVService:
 def __init__(self,connect,settings,keys,clock=time.monotonic,timer_factory=threading.Timer):
  self.connect=connect;self.settings=settings;self.keys=keys;self.clock=clock;self.factory=timer_factory;self.lock=threading.RLock();self.socket=None;self.last_used=0;self.last_error=None;self.last_sent=None;self.timer=None;self.generation=0;self.countdown={'state':'none'}
 def _disconnect(self):
  if self.socket:
   try:self.socket.close()
   except Exception:pass
  self.socket=None
 def command(self,key):
  import json
  if key not in self.keys:raise ValueError('Unknown TV control')
  with self.lock:
   if self.socket and self.clock()-self.last_used>120:self._disconnect()
   try:
    if not self.socket:self.socket=self.connect()
    self.socket.send(json.dumps({'method':'ms.remote.control','params':{'Cmd':'Click','DataOfCmd':self.keys[key],'Option':'false','TypeOfRemote':'SendRemoteKey'}}))
    self.last_used=self.clock();self.last_sent=key;self.last_error=None
   except Exception as exc:
    self.last_error=str(exc)[:120];self._disconnect();raise ValueError('TV connection failed: '+self.last_error)
  return 'TV: '+key.replace('_',' ')+' sent; execution not acknowledged by this protocol'
 def cancel(self,reason='Cancelled',owner=None):
  with self.lock:
   if owner is not None and self.countdown.get('owner')!=owner:return
   self.generation+=1
   if self.timer:self.timer.cancel();self.timer=None
   if self.countdown.get('state')=='scheduled':self.countdown={**self.countdown,'state':'cancelled','reason':reason}
 def start(self,minutes,owner):
  if type(minutes) is not int or minutes not in (15,30,60,90,120):raise ValueError('Choose 15, 30, 60, 90 or 120 minutes')
  with self.lock:
   ip=self.settings().get('ip')
   if not ip:raise ValueError('Configure the TV first')
   self.cancel('Replaced');generation=self.generation
   self.countdown={'state':'scheduled','deadline':self.clock()+minutes*60,'minutes':minutes,'owner':owner,'ip':ip,'mechanism':'UMBRA-managed Power Off; server must remain running/connected; cancelled on restart'}
   self.timer=self.factory(minutes*60,lambda:self._fire(generation));self.timer.daemon=True;self.timer.start()
   return self.status()['timer']
 def _fire(self,generation):
  with self.lock:
   if generation!=self.generation or self.countdown.get('state')!='scheduled':return
   self.timer=None
   if self.settings().get('ip')!=self.countdown['ip']:
    self.countdown={**self.countdown,'state':'cancelled','reason':'TV address changed'};return
   self.countdown={**self.countdown,'state':'sending'}
   try:self.command('power_off');self.countdown={**self.countdown,'state':'sent','reason':'Power Off sent once; TV execution not acknowledged'}
   except ValueError as exc:self.countdown={**self.countdown,'state':'failed','reason':str(exc)+'; no delayed retry'}
 def reconfigure(self):
  with self.lock:self.cancel('TV configuration changed');self._disconnect()
 def close(self):
  with self.lock:self.cancel('Server stopped; timer not restored on restart');self._disconnect()
 def status(self):
  with self.lock:
   timer={k:v for k,v in self.countdown.items() if k not in ('owner','ip','deadline')}
   timer['remaining_seconds']=max(0,round(self.countdown.get('deadline',self.clock())-self.clock())) if self.countdown.get('state')=='scheduled' else 0
   return {'configured':bool(self.settings().get('ip')),'transport_connected':self.socket is not None,'last_sent':self.last_sent,'last_error':self.last_error,'execution_acknowledged':False,'timer':timer,'capabilities':{'keys':list(self.keys),'native_sleep_timer':False,'managed_sleep_timer':True,'power_on':False,'app_launch':False,'picture_sound_modes':False,'tv_plus_shortcuts':False,'long_press_protocol':False,'device_validation':'Not performed; allowlisted existing Tizen key transport only'}}
