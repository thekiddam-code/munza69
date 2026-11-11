import re,posixpath
from bridge_service import BridgeService,BridgeError
import http.server, json, os, secrets, socket, threading, time, urllib.parse, hashlib, ipaddress, ssl, base64
from pathlib import Path

try:
 import pyautogui as pg
except ImportError:
 raise SystemExit('Install dependencies: py -m pip install -r requirements.txt')
try:
 import psutil
except ImportError:
 psutil=None

try:
 from websocket import create_connection
except ImportError:
 create_connection=None

ROOT=Path(__file__).parent
PORT=8765
PIN=secrets.token_urlsafe(6)
ICARUS_KEY=secrets.token_urlsafe(18)
BRIDGE_SERVICE=BridgeService()
ICARUS_BRIDGE={"telemetry":None,"updated":0,"commands":[],"next_id":1}
# Store only SHA-256 hashes of approved device tokens on disk.
DEVICES_FILE=ROOT/'paired_devices.json'
def load_tokens():
 try:
  data=json.loads(DEVICES_FILE.read_text(encoding='utf8'))
  return set(x for x in data.get('token_hashes',[]) if isinstance(x,str) and len(x)==64)
 except (OSError,ValueError,TypeError): return set()
def save_tokens():
 tmp=DEVICES_FILE.with_suffix('.tmp')
 tmp.write_text(json.dumps({'token_hashes':sorted(TOKENS)},indent=2),encoding='utf8')
 os.replace(tmp,DEVICES_FILE)
def token_hash(token): return hashlib.sha256(token.encode('utf8')).hexdigest()
TOKENS=load_tokens()
LOCK=threading.RLock()
HELD=set()
TIMER=None
CONFIG=ROOT/'config.json'
DEFAULT={'quick':{'Nice shot!':['1','1'],'What a save!':['1','2'],'Great pass!':['1','3'],'Thanks!':['1','4'],'I got it!':['2','1'],'Defending...':['2','2'],'Sorry!':['3','1'],'No problem.':['3','2']},'macros':{'Copy':['ctrl','c'],'Paste':['ctrl','v'],'Screenshot':['win','shift','s']},'text_chat_open':'t'}
if not CONFIG.exists(): CONFIG.write_text(json.dumps(DEFAULT,indent=2),encoding='utf8')
pg.FAILSAFE=True
pg.PAUSE=.07

def cfg(): return json.loads(CONFIG.read_text(encoding='utf8'))
def save_custom_messages(messages):
 with LOCK:
  data=cfg()
  data['custom_messages']=messages
  tmp=CONFIG.with_suffix('.tmp')
  tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
  os.replace(tmp,CONFIG)
def valid_custom_messages(items):
 if not isinstance(items,list) or len(items)>40: raise ValueError('Maximum 40 buttons')
 cleaned=[]
 for item in items:
  if not isinstance(item,dict): raise ValueError('Invalid button')
  label=item.get('label'); message=item.get('text'); channel=item.get('channel')
  if not isinstance(label,str) or not 1<=len(label.strip())<=32 or any(ord(c)<32 for c in label): raise ValueError('Button name must be 1-32 characters')
  if not isinstance(message,str) or not 1<=len(message.strip())<=120 or any(ord(c)<32 for c in message): raise ValueError('Message must be 1-120 characters')
  if channel not in ('team','match'): raise ValueError('Choose team or match chat')
  cleaned.append({'label':label.strip(),'text':message.strip(),'channel':channel})
 return cleaned

FORTNITE_DEFAULT=[{'label':f'Emote {i+1}','key':key} for i,key in enumerate(('f6','f7','f8','f9','f10','f11','f12','f5'))]+[{'label':'Repeat Last Emote','key':'f4'}]
ALLOWED_EMOTE_KEYS={f'f{i}' for i in range(1,13)}
def get_fortnite_buttons():
 data=cfg().get('fortnite_emotes',FORTNITE_DEFAULT)
 return validate_fortnite_buttons(data)
def validate_fortnite_buttons(items):
 if not isinstance(items,list) or len(items)!=9: raise ValueError('Expected eight emote slots and Repeat Last Emote')
 cleaned=[]
 for item in items:
  if not isinstance(item,dict): raise ValueError('Invalid emote button')
  label=item.get('label'); key=item.get('key')
  if not isinstance(label,str) or not 1<=len(label.strip())<=32 or any(ord(c)<32 for c in label): raise ValueError('Invalid emote name')
  if key not in ALLOWED_EMOTE_KEYS: raise ValueError('Use F1 through F12 for emotes')
  cleaned.append({'label':label.strip(),'key':key})
 return cleaned
def save_fortnite_buttons(items):
 with LOCK:
  data=cfg();data['fortnite_emotes']=items
  tmp=CONFIG.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8');os.replace(tmp,CONFIG)

# Samsung Tizen TV LAN remote. Only explicitly configured private LAN IPs are accepted.
TV_FILE=ROOT/'samsung_tv.json'
TV_KEYS={
 'power_off':'KEY_POWEROFF','home':'KEY_HOME','back':'KEY_RETURN',
 'up':'KEY_UP','down':'KEY_DOWN','left':'KEY_LEFT','right':'KEY_RIGHT',
 'ok':'KEY_ENTER','vol_up':'KEY_VOLUP','vol_down':'KEY_VOLDOWN',
 'mute':'KEY_MUTE','ch_up':'KEY_CHUP','ch_down':'KEY_CHDOWN',
 'source':'KEY_SOURCE','play':'KEY_PLAY','pause':'KEY_PAUSE',
 'play_pause':'KEY_PLAY','stop':'KEY_STOP','rewind':'KEY_REWIND','forward':'KEY_FF',
 'menu':'KEY_MENU','info':'KEY_INFO','exit':'KEY_EXIT',
}
def tv_settings():
 try:
  data=json.loads(TV_FILE.read_text(encoding='utf8'))
  return {'ip':data.get('ip',''),'token':data.get('token','')}
 except (OSError,ValueError,TypeError): return {'ip':'','token':''}
def tv_save(data):
 tmp=TV_FILE.with_suffix('.tmp')
 tmp.write_text(json.dumps(data,indent=2),encoding='utf8')
 os.replace(tmp,TV_FILE)
def tv_ip(value):
 try: address=ipaddress.ip_address(value)
 except ValueError: raise ValueError('Enter the TV IPv4 address')
 if address.version!=4 or not address.is_private or address.is_loopback or address.is_link_local or address.is_multicast or address.is_unspecified:
  raise ValueError('TV must have a private home-network IPv4 address')
 return str(address)
def tv_connect():
 if create_connection is None: raise ValueError('Install TV dependency: py -m pip install -r requirements.txt')
 settings=tv_settings()
 if not settings['ip']: raise ValueError('Set the TV IP address first')
 ip=tv_ip(settings['ip'])
 name=base64.b64encode(b'Remote Deck').decode('ascii')
 token=settings.get('token','')
 url=f'wss://{ip}:8002/api/v2/channels/samsung.remote.control?name={name}'
 if token: url+='&token='+urllib.parse.quote(token,safe='')
 ws=create_connection(url,timeout=3,sslopt={'cert_reqs':ssl.CERT_NONE},origin=f'http://{ip}')
 # The TV sends ms.channel.connect with a reusable token after user approval.
 ws.settimeout(3)
 try:
  reply=json.loads(ws.recv())
  if reply.get('event')=='ms.channel.unauthorized': raise ValueError('TV denied access. Allow Remote Deck on the TV.')
  new_token=reply.get('data',{}).get('token')
  if new_token and isinstance(new_token,str) and len(new_token)<256 and new_token!=token:
   settings['token']=new_token;tv_save(settings)
 except (TimeoutError,ValueError):
  ws.close();raise
 except Exception:
  # Some models do not send the initial event promptly.
  pass
 return ws
# Same allowlist and authenticated endpoints; a reusable transport avoids reconnecting per key.
from tv_service import TVService
TV_SERVICE=TVService(tv_connect,tv_settings,TV_KEYS)
def tv_command(command): return TV_SERVICE.command(command)

def release():
 global TIMER
 with LOCK:
  if TIMER: TIMER.cancel(); TIMER=None
  for k in list(HELD):
   try: pg.keyUp(k) if k!='mouse_left' else pg.mouseUp()
   except Exception: pass
  HELD.clear()
def schedule_release(seconds):
 global TIMER
 if TIMER: TIMER.cancel()
 TIMER=threading.Timer(seconds,release); TIMER.daemon=True; TIMER.start()
def keyseq(seq):
 if not isinstance(seq,list) or len(seq)>6 or any(not isinstance(k,str) or len(k)>20 for k in seq): raise ValueError('Invalid keys')
 for k in seq:
  pg.press(k); time.sleep(.09)
def action(d):
 kind=d.get('action')
 with LOCK:
  if kind=='stop': release(); return 'Stopped'
  if kind=='mine_toggle':
   if 'mouse_left' in HELD: pg.mouseUp(); HELD.remove('mouse_left'); return 'Mining stopped'
   pg.mouseDown(); HELD.add('mouse_left'); schedule_release(60); return 'Mining active (60s safety timeout)'
  if kind=='forward_mine':
   secs=max(.2,min(10,float(d.get('seconds',3))))
   release(); pg.mouseDown(); pg.keyDown('w'); HELD.update(('mouse_left','w')); schedule_release(secs); return f'Forward mining for {secs:g}s'
  if kind=='fortnite_emote':
   index=d.get('index')
   if type(index) is not int or not 0<=index<9: raise ValueError('Invalid emote slot')
   item=get_fortnite_buttons()[index]
   pg.press(item['key']); return 'Emote key sent: '+item['label']
  if kind=='quick':
   name=str(d.get('name','')); seq=cfg()['quick'].get(name)
   if not seq: raise ValueError('Unknown quick chat')
   keyseq(seq); return 'Quick chat sent'
  if kind=='text':
   msg=str(d.get('text',''))
   if not 1<=len(msg)<=120 or any(ord(c)<32 for c in msg): raise ValueError('Invalid text')
   channel=str(d.get('channel','match'))
   if channel not in ('match','team'): raise ValueError('Invalid chat channel')
   opener=cfg().get('team_text_chat_open','y') if channel=='team' else cfg().get('text_chat_open','t')
   # Temporarily disable PyAutoGUI's global per-call delay for chat only.
   # Keep a small pause for the game to open its text input.
   speed=str(d.get('speed','fast'))
   if speed not in ('fast','balanced','safe'): raise ValueError('Invalid chat speed')
   # Rocket League can discard the beginning of text if chat is still opening.
   # Longer messages get more time to open and a small per-character interval.
   open_delay,letter_delay={
    'fast':((.30 if len(msg)>45 else .22),(.008 if len(msg)>45 else .004)),
    'balanced':(.38,.015),
    'safe':(.50,.030)
   }[speed]
   old_pause=pg.PAUSE
   try:
    pg.PAUSE=0
    pg.press(opener)
    time.sleep(open_delay)
    pg.write(msg,interval=letter_delay)
    time.sleep(.12)
    pg.press('enter')
   finally:
    pg.PAUSE=old_pause
   return 'Text sent to '+channel+' chat ('+speed+')' 
  if kind=='macro':
   name=str(d.get('name','')); seq=cfg()['macros'].get(name)
   if not seq: raise ValueError('Unknown macro')
   if len(seq)>4: raise ValueError('Macro too long')
   pg.hotkey(*seq); return 'Hotkey sent'
  raise ValueError('Unknown action')

def valid_icarus_command(command):
 if command in ('pause','resume','speed1','speed5','speed20','save','nav:hold','nav:resume','nav:recall'): return True
 if isinstance(command,str) and re.fullmatch(r'frontier:(rescue|shelter):SOS-\d+',command): return True
 return isinstance(command,str) and len(command)<=100 and re.fullmatch(r'nav:course:(HOME|LOCAL-(DEBRIS|ICE|RELAY|HULL|ECHO)|SYS:-?\d+:-?\d+/\d+)',command) is not None

class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT/'web'),**kwargs)
 def log_message(self,*args): pass
 def respond(self,code,data):
  body=json.dumps(data).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(body))); self.end_headers();
  try:self.wfile.write(body)
  except (BrokenPipeError,ConnectionResetError):pass
 def local_host(self):
  host=urllib.parse.urlsplit('http://'+self.headers.get('Host','')).hostname
  if self.client_address[0] in ('127.0.0.1','::1') and host in ('127.0.0.1','localhost','::1'):return True
  # Preserve an existing voyage at the laptop's own LAN-IP origin. Remote peers differ.
  try:return ipaddress.ip_address(host)==ipaddress.ip_address(self.client_address[0])==ipaddress.ip_address(self.connection.getsockname()[0])
  except ValueError:return False
 def host_auth(self):
  return secrets.compare_digest(self.headers.get('X-Icarus-Key',''),ICARUS_KEY)
 def host_identity(self):
  try:return self.headers.get('X-Icarus-Instance',''),int(self.headers.get('X-Icarus-Generation','0'))
  except ValueError:raise BridgeError(400,'Invalid generation')
 def live_view(self):
  view=BRIDGE_SERVICE.view()
  if BRIDGE_SERVICE.owner is not None:return {**view,'protocol':2}
  # Older authenticated Phase 4A host can still use its original bridge contract.
  with LOCK:data=ICARUS_BRIDGE['telemetry'];age=time.time()-ICARUS_BRIDGE['updated'] if data else None
  online=bool(data and age<8)
  return {**view,'protocol':1,'online':online,'stale':not online,'age':age,'telemetry':data,'state':'SIMULATION PAUSED' if online and data.get('paused') else 'HOST CONNECTED' if online else 'HOST OFFLINE'}
 def do_GET(self):
  if posixpath.normpath(urllib.parse.unquote(urllib.parse.urlsplit(self.path).path))=='/icarus.html' and not self.local_host():
   self.send_response(302);self.send_header('Location','/?terminal=icarus');self.send_header('Cache-Control','no-store');self.end_headers();return
  if self.path=='/api/icarus/bootstrap':
   if not self.local_host():return self.respond(403,{'error':'Open the host on this PC at http://127.0.0.1:8765/icarus.html'})
   return self.respond(200,{'key':ICARUS_KEY,'protocol':2})
  if self.path=='/api/icarus/host/commands':
   if not self.host_auth():return self.respond(403,{'error':'Invalid host key'})
   try:return self.respond(200,{'commands':BRIDGE_SERVICE.pending(*self.host_identity())})
   except BridgeError as e:return self.respond(e.status,{'error':str(e)})
  if self.path in ('/api/icarus/live','/api/icarus/events'):
   if not self.authorized():return self.respond(401,{'error':'Pair first'})
   if self.path.endswith('/live'):return self.respond(200,self.live_view())
   self.connection.settimeout(8)
   self.send_response(200);self.send_header('Content-Type','text/event-stream');self.send_header('Cache-Control','no-store');self.send_header('X-Accel-Buffering','no');self.end_headers()
   # Bounded stream lifetime allows token revocation and reconnect without a worker leak.
   try:
    for _ in range(30):
     if not self.authorized():break
     data=self.live_view();self.wfile.write(('id: '+str(data['revision'])+'\nevent: telemetry\ndata: '+json.dumps(data)+'\n\n').encode());self.wfile.flush()
     with BRIDGE_SERVICE.changed:BRIDGE_SERVICE.changed.wait(timeout=2)
   except (BrokenPipeError,ConnectionResetError,OSError):pass
   self.close_connection=True;return
  if self.path in ('/api/icarus/telemetry','/api/icarus/telemetry?companion=1'):
   if not self.authorized(): return self.respond(401,{'error':'Pair first'})
   with LOCK:
    data=ICARUS_BRIDGE['telemetry']
    age=time.time()-ICARUS_BRIDGE['updated'] if data else None
   if data and 'companion' in data and self.path=='/api/icarus/telemetry':data={k:v for k,v in data.items() if k!='companion'}
   return self.respond(200,{'online':bool(data and age<8),'age':round(age,1) if age is not None else None,'telemetry':data if data and age<8 else None})
  if self.path=='/api/icarus/commands':
   if self.headers.get('X-Icarus-Key')!=ICARUS_KEY: return self.respond(403,{'error':'Invalid host key'})
   with LOCK:
    cmds=ICARUS_BRIDGE['commands'][:]
    ICARUS_BRIDGE['commands'].clear()
   return self.respond(200,{'commands':cmds})
  if self.path=='/api/tv/status':
   if not self.authorized(): return self.respond(401,{'error':'Pair first'})
   return self.respond(200,TV_SERVICE.status())
  if self.path=='/api/status':
   if not self.authorized(): return self.respond(401,{'error':'Pair first'})
   self.respond(200,{'cpu':psutil.cpu_percent(interval=.1) if psutil else None,'ram':psutil.virtual_memory().percent if psutil else None,'mining':'mouse_left' in HELD,'quick':list(cfg()['quick']),'macros':list(cfg()['macros']),'custom_messages':cfg().get('custom_messages',[]),'fortnite_emotes':get_fortnite_buttons(),'tv_ip':tv_settings()['ip'],'tv_configured':bool(tv_settings()['ip'])}); return
  if self.path.startswith('/api/'): return self.respond(404,{'error':'Not found'})
  return super().do_GET()
 def authorized(self):
  token=self.headers.get('Authorization','').removeprefix('Bearer ')
  return bool(token) and token_hash(token) in TOKENS
 def do_POST(self):
  try:
   if self.headers.get('Content-Type','').split(';')[0]!='application/json': return self.respond(415,{'error':'JSON required'})
   if int(self.headers.get('Content-Length','0'))>(65536 if self.path=='/api/icarus/host/publish' else 16384 if self.path=='/api/icarus/telemetry' else 4096): return self.respond(413,{'error':'Too large'})
   origin=self.headers.get('Origin','')
   host=self.headers.get('Host','')
   if origin and origin not in ('http://'+host,'https://'+host): return self.respond(403,{'error':'Invalid origin'})
   data=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))))
   if self.path in ('/api/icarus/host/claim','/api/icarus/host/publish','/api/icarus/host/heartbeat'):
    if not self.host_auth():return self.respond(403,{'error':'Invalid host key'})
    try:
     if self.path.endswith('/claim'):return self.respond(200,BRIDGE_SERVICE.claim(data.get('instance')))
     owner,generation=self.host_identity()
     if self.path.endswith('/heartbeat'):return self.respond(200,BRIDGE_SERVICE.heartbeat(owner,generation))
     result=BRIDGE_SERVICE.publish(owner,generation,data.get('telemetry'),data.get('acks',[]))
     # Legacy installed Android response stays the same; extra protocol-2 fields are opt-in.
     legacy=data.get('legacy')
     if isinstance(legacy,dict) and len(json.dumps(legacy))<=14000:
      with LOCK:ICARUS_BRIDGE.update(telemetry=legacy,updated=time.time())
     return self.respond(200,result)
    except BridgeError as e:return self.respond(e.status,{'error':str(e)})
   if self.path=='/api/pair':
    if secrets.compare_digest(str(data.get('pin','')),PIN):
     token=secrets.token_urlsafe(32)
     with LOCK:
      TOKENS.add(token_hash(token)); save_tokens()
     return self.respond(200,{'token':token})
    time.sleep(.7); return self.respond(403,{'error':'Incorrect pairing code'})
   # ICARUS host publishes telemetry using its own dedicated host key.
   # Tablet endpoints below continue to require the paired-device bearer token.
   if self.path=='/api/icarus/telemetry':
    if BRIDGE_SERVICE.active():return self.respond(409,{'error':'A fenced host is already active'})
    if not secrets.compare_digest(self.headers.get('X-Icarus-Key',''),ICARUS_KEY): return self.respond(403,{'error':'Invalid host key'})
    if not isinstance(data,dict) or len(json.dumps(data))>14000: return self.respond(400,{'error':'Invalid telemetry'})
    with LOCK:
     ICARUS_BRIDGE['telemetry']=data
     ICARUS_BRIDGE['updated']=time.time()
    return self.respond(200,{'ok':True})
   if not self.authorized(): return self.respond(401,{'error':'Pair first'})
   if self.path=='/api/icarus/dispatch':
    command=data.get('command')
    if not valid_icarus_command(command):return self.respond(400,{'error':'Unknown command'})
    try:return self.respond(200,BRIDGE_SERVICE.enqueue(token_hash(self.headers.get('Authorization','')),data.get('requestId'),command))
    except BridgeError as e:return self.respond(e.status,{'error':str(e)})
   if self.path=='/api/icarus/command':
    if BRIDGE_SERVICE.active():
     if not valid_icarus_command(data.get('command')):return self.respond(400,{'error':'Unknown command'})
     try:
      result=BRIDGE_SERVICE.enqueue(token_hash(self.headers.get('Authorization','')),data.get('requestId') or secrets.token_hex(12),data['command']);return self.respond(200,{'queued':result['queued']})
     except BridgeError as e:return self.respond(e.status,{'error':str(e)})
    command=data.get('command')
    if not valid_icarus_command(command): return self.respond(400,{'error':'Unknown command'})
    with LOCK:
     if len(ICARUS_BRIDGE['commands'])>=25: return self.respond(429,{'error':'Command queue full; ICARUS offline?'})
     cid=ICARUS_BRIDGE['next_id']; ICARUS_BRIDGE['next_id']+=1
     ICARUS_BRIDGE['commands'].append({'id':cid,'command':command})
    return self.respond(200,{'queued':cid})
   if self.path=='/api/unpair':
    token=self.headers.get('Authorization','').removeprefix('Bearer ')
    with LOCK:
     TOKENS.discard(token_hash(token)); save_tokens();TV_SERVICE.cancel('Owner unpaired',token_hash(token))
    return self.respond(200,{'message':'Device forgotten'})
   if self.path=='/api/tv/timer':
    if data.get('cancel') is True:
     TV_SERVICE.cancel();return self.respond(200,TV_SERVICE.status())
    return self.respond(200,{'timer':TV_SERVICE.start(data.get('minutes'),token_hash(self.headers.get('Authorization','').removeprefix('Bearer ')))})
   if self.path=='/api/tv/config':
    ip=tv_ip(str(data.get('ip','')).strip())
    with TV_SERVICE.lock:
     TV_SERVICE.reconfigure()
     previous=tv_settings()
     tv_save({'ip':ip,'token':previous['token'] if previous['ip']==ip else ''})
    return self.respond(200,{'message':'TV address saved','ip':ip})
   if self.path=='/api/tv/key':
    return self.respond(200,{'message':tv_command(str(data.get('key','')))})
   if self.path=='/api/action': return self.respond(200,{'message':action(data)})
   if self.path=='/api/fortnite_emotes':
    items=validate_fortnite_buttons(data.get('buttons'))
    save_fortnite_buttons(items)
    return self.respond(200,{'message':'Emote buttons saved','fortnite_emotes':items})
   if self.path=='/api/custom_messages':
    items=valid_custom_messages(data.get('messages'))
    save_custom_messages(items)
    return self.respond(200,{'message':'Buttons saved','custom_messages':items})
   return self.respond(404,{'error':'Not found'})
  except Exception as exc: return self.respond(400,{'error':str(exc)[:150]})

def local_ip():
 s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 try: s.connect(('192.0.2.1',80)); return s.getsockname()[0]
 except OSError: return 'YOUR-PC-IP'
 finally: s.close()

if __name__=='__main__':
 print('\nREMOTE DECK')
 print('Phone URL: http://%s:%s'%(local_ip(),PORT))
 print('Pairing PIN:',PIN)
 print('ICARUS host key (PC only):',ICARUS_KEY)
 print('ICARUS PC URL: http://127.0.0.1:%s/icarus.html'%PORT)
 import webbrowser
 threading.Timer(.8,lambda:webbrowser.open('http://127.0.0.1:%s/host.html'%PORT)).start()
 print('Keep this window running. Ctrl+C stops the receiver.')
 try: http.server.ThreadingHTTPServer(('0.0.0.0',PORT),Handler).serve_forever()
 except KeyboardInterrupt: pass
 finally: release();TV_SERVICE.close()
