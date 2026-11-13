"""Volatile fenced host lease and bounded acknowledged command delivery; no world storage."""
import collections,copy,secrets,threading,time
class BridgeError(ValueError):
 def __init__(self,status,message):self.status=status;super().__init__(message)
class BridgeService:
 def __init__(self,clock=time.monotonic):
  self.clock=clock;self.lock=threading.RLock();self.changed=threading.Condition(self.lock);self.owner=None;self.expires=0;self.generation=0;self.revision=0;self.data=None;self.classified=None;self.updated=None;self.queue=[];self.receipts=collections.OrderedDict();self.next_id=1;self.boot=secrets.token_hex(8)
 def active(self):return self.owner is not None and self.clock()<self.expires
 def claim(self,owner):
  if not isinstance(owner,str) or not 8<=len(owner)<=80:raise BridgeError(400,'Invalid host instance')
  with self.lock:
   if self.active() and self.owner!=owner:raise BridgeError(409,'Another authoritative simulation owns this server')
   if self.owner!=owner or not self.active():
    self.generation+=1;self.queue=[];self.data=None;self.classified=None;self.updated=None
   self.owner=owner;self.expires=self.clock()+12;self.revision+=1;self.changed.notify_all();return {'generation':self.generation,'boot':self.boot,'lease_seconds':12}
 def check(self,owner,generation):
  if owner!=self.owner or generation!=self.generation:raise BridgeError(409,'Host ownership lost; reload the authoritative page')
  if not self.active():raise BridgeError(425,'Lease expired; heartbeat required')
 def heartbeat(self,owner,generation):
  with self.lock:
   if owner!=self.owner or generation!=self.generation:raise BridgeError(409,"Host ownership lost")
   self.expires=self.clock()+12;return {"ok":True}
 def publish(self,owner,generation,data,acks=(),classified=None):
  with self.lock:
   self.check(owner,generation)
   if not isinstance(data,dict):raise BridgeError(400,'Invalid telemetry')
   if any(k in data for k in ('classified','classifiedOps')):raise BridgeError(400,'Classified payload belongs on the restricted channel')
   if classified is not None and (not isinstance(classified,dict) or len(__import__('json').dumps(classified))>24576):raise BridgeError(400,'Invalid classified payload')
   if not isinstance(acks,list) or len(acks)>256 or any(type(x) is not int for x in acks):raise BridgeError(400,'Invalid acknowledgments')
   self.queue=[x for x in self.queue if x['id'] not in acks and x['expires']>self.clock()]
   self.data=copy.deepcopy(data);self.classified=copy.deepcopy(classified);self.updated=self.clock();self.expires=self.clock()+12;self.revision+=1;self.changed.notify_all();return {'ok':True,'revision':self.revision}
 def pending(self,owner,generation):
  with self.lock:
   self.check(owner,generation);self.queue=[x for x in self.queue if x['expires']>self.clock()];return [{'id':x['id'],'command':x['command']} for x in self.queue]
 def enqueue(self,token,request,command):
  if not isinstance(request,str) or not 8<=len(request)<=80:raise BridgeError(400,'Request ID required')
  with self.lock:
   now=self.clock()
   while self.receipts and next(iter(self.receipts.values()))['at']<now-600:self.receipts.popitem(last=False)
   key=(token,request)
   if key in self.receipts:
    r=self.receipts[key]
    if r['command']!=command:raise BridgeError(409,'Request ID reused for a different command')
    return {'queued':r['id'],'duplicate':True}
   if not self.active() or self.updated is None or now-self.updated>8:raise BridgeError(409,'No fresh authoritative host; command not queued')
   if command.startswith('speed'):
    if not self.data.get('creator',False):raise BridgeError(403,'Creator Mode required on the authoritative host')
   self.queue=[x for x in self.queue if x['expires']>now]
   if len(self.queue)>=25:raise BridgeError(429,'Command queue full')
   cid=self.next_id;self.next_id+=1;self.queue.append({'id':cid,'command':command,'expires':now+30});self.receipts[key]={'id':cid,'command':command,'at':now}
   while len(self.receipts)>256:self.receipts.popitem(last=False)
   return {'queued':cid,'duplicate':False}
 def classified_view(self):
  with self.lock:
   age=None if self.updated is None else max(0,self.clock()-self.updated)
   return {'online':self.active() and age is not None and age<8,'paused':bool(self.data and self.data.get('paused')),'telemetry':copy.deepcopy(self.classified),'age':age}
 def view(self):
  with self.lock:
   age=None if self.updated is None else max(0,self.clock()-self.updated);online=self.active() and age is not None and age<8
   state='SIMULATION PAUSED' if online and self.data.get('paused') else 'HOST CONNECTED' if online else 'RECONNECTING' if self.active() else 'HOST OFFLINE'
   return {'online':online,'state':state,'age':age,'revision':self.revision,'session':self.boot+':'+str(self.generation),'telemetry':copy.deepcopy(self.data),'stale':not online}
