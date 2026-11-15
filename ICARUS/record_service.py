"""Bounded, volatile public-record transfer. Never stores the world or onboard/private clips."""
import base64,json,secrets,time,threading
from bridge_service import BridgeError
class RecordService:
 def __init__(self,clock=time.monotonic):self.clock=clock;self.generation=None;self.jobs={};self.lock=threading.RLock()
 def prune(self,generation):
  if generation!=self.generation:self.jobs={};self.generation=generation
  self.jobs={k:v for k,v in self.jobs.items() if self.clock()-v['created']<60}
 def request(self,record,generation):
  with self.lock:
   self.prune(generation)
   if record not in self.jobs:
    if len(self.jobs)>=4:
     old=next((k for k,v in self.jobs.items() if v['result'] or v.get('error')),None)
     if old is None:raise BridgeError(429,'Archive transfer queue busy; retry shortly')
     del self.jobs[old]
    self.jobs[record]={'id':record,'token':secrets.token_hex(12),'created':self.clock(),'chunks':{},'result':None}
   j=self.jobs[record]
   if j.get('error'):raise BridgeError(410,j['error'])
   return {'ready':bool(j['result']),'record':j['result']} if j['result'] else {'ready':False,'id':record}
 def pending(self,generation):
  with self.lock:
   self.prune(generation);return [{'id':j['id'],'token':j['token']} for j in self.jobs.values() if not j['result'] and not j.get('error')]
 def chunk(self,generation,data):
  with self.lock:
   self.prune(generation);j=self.jobs.get(data.get('id'))
   if not j or j['token']!=data.get('token'):raise BridgeError(409,'Expired archive request')
   if data.get('error'):j['error']=str(data['error'])[:200] if isinstance(data['error'],str) else 'Original unavailable through remote transfer; inspect host archive';return {'ok':True}
   index,total,piece=data.get('index'),data.get('total'),data.get('chunk')
   if type(index)!=int or type(total)!=int or not 1<=total<=16 or not 0<=index<total or not isinstance(piece,str) or len(piece)>48000:raise BridgeError(400,'Invalid bounded archive chunk')
   if j.get('total',total)!=total:raise BridgeError(409,'Archive generation changed during transfer')
   j['total']=total;j['chunks'][index]=piece
   if len(j['chunks'])==total:
    try:
     raw=base64.b64decode(''.join(j['chunks'][i] for i in range(total)),validate=True)
     if len(raw)>524288:raise ValueError('Record exceeds on-demand transfer limit; use host archive')
     record=json.loads(raw)
     if not isinstance(record,dict) or record.get('id')!=j['id'] or not isinstance(record.get('frames'),list):raise ValueError('Record identity mismatch')
    except Exception as e:j['error']=str(e);raise BridgeError(422,str(e))
    j['result']=record;j['chunks']={}
   return {'ok':True}
