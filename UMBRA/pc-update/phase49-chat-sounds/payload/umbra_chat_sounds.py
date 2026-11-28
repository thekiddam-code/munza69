"""Sequence existing Rocket League input and existing SoundService playback; no audio engine."""
import re,time,uuid
from collections import OrderedDict

class ChatSounds:
 def __init__(self,action,sounds,lock):
  self.action=action;self.sounds=sounds;self.lock=lock;self.receipts=OrderedDict()
 def run(self,owner,data):
  if not isinstance(data,dict):raise ValueError('Chat request object required')
  kind=data.get('action')
  fields={'quick':{'name'},'text':{'text','channel','speed'}}.get(kind)
  if fields is None or set(data)!=fields|{'action','sound_id','requestId'}:raise ValueError('Only quick chat or text with one sound is supported')
  sound=data['sound_id'];request=data['requestId']
  if not isinstance(sound,str) or not re.fullmatch('[a-f0-9]{32}',sound):raise ValueError('Select an existing sound ID')
  if not isinstance(request,str) or str(uuid.UUID(request))!=request:raise ValueError('Valid request UUID required')
  command={k:data[k] for k in fields|{'action'}}
  # Validation in the original action runs before any key is pressed.
  key=(owner,request)
  with self.lock:
   now=time.monotonic()
   self.receipts=OrderedDict((k,v) for k,v in self.receipts.items() if now-v[0]<600)
   if key in self.receipts:
    _,prior,result=self.receipts[key]
    if prior!=data:raise ValueError('Request ID already used for another command')
    return dict(result)
   # Claim before input so a partial keyboard failure cannot be replayed by a retry.
   result={'chat_input_completed':False,'sound_started':False,'message':'Input outcome unconfirmed; do not replay automatically.'}
   self.receipts[key]=(now,dict(data),result)
   if len(self.receipts)>128:self.receipts.popitem(last=False)
   try:
    message=self.action(command)
   except Exception:
    result['message']='Chat input failed or was interrupted; sound skipped. Delivery is unconfirmed.'
    return dict(result)
   result.update(chat_input_completed=True,message=message+'. Game delivery is not confirmed.')
   try:
    player=self.sounds.post('play',{'id':sound,'requestId':request},owner)
    if player.get('state') not in ('starting','playing','idle'):raise ValueError('Playback did not start')
    result.update(sound_started=True,player=player,message=result['message']+' Soundboard playback accepted.')
   except Exception:
    result['message']='Chat input completed; sound unavailable or playback failed. Chat was not resent. Game delivery is unconfirmed.'
   return dict(result)
