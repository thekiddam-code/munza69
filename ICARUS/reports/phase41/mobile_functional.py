"""External functional check against the actual Lite server and web assets. No physical input/TV I/O."""
import importlib.util,sys,types,json,threading,urllib.request,urllib.error,tempfile,traceback,os
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=Path(__file__).resolve().parent;LITE=Path(os.environ.get('ICARUS_LITE_ROOT',str(BASE/'tested/ICARUS_Phase4_1_Command_Bridge_Lite')));calls=[]
pg=types.SimpleNamespace(**{name:(lambda *a,_n=name,**k:calls.append({'operation':_n,'args':list(a)})) for name in ['press','hotkey','keyUp','mouseUp','mouseDown','keyDown','write']});sys.modules['pyautogui']=pg
spec=importlib.util.spec_from_file_location('lite_mobile_host',LITE/'server.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
r={'passed':False,'runtime_root':str(LITE),'checks':[],'errors':[],'limits':'Android Chrome mobile/touch emulation on Chromium through real HTTP pairing/bridge. PyAutoGUI and television socket stubbed. No physical Android, Windows desktop input, Wi-Fi or Samsung device used.'}
def check(name,condition):
 assert condition,name;r['checks'].append(name)
with tempfile.TemporaryDirectory(prefix='lite-pair-') as td:
 m.DEVICES_FILE=Path(td)/'paired_devices.json';m.TV_FILE=Path(td)/'samsung_tv.json';m.PIN='lite-fixture';m.ICARUS_KEY='lite-fixture-host';m.TOKENS=set()
 class TV:
  def settimeout(self,n):pass
  def recv(self):return json.dumps({'event':'ms.channel.connect','data':{'token':'fixture-tv-token'}})
  def send(self,v):calls.append({'operation':'tv_send','payload':json.loads(v)})
  def close(self):pass
 def tvsocket(url,**kw):calls.append({'operation':'tv_connect','url':url,'certificate_validation':kw.get('sslopt',{}).get('cert_reqs')});return TV()
 m.create_connection=tvsocket
 server=m.http.server.ThreadingHTTPServer(('127.0.0.1',0),m.Handler);threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}'
 def request(path,payload=None,token=None,origin=None):
  headers={'Content-Type':'application/json'}
  if token:headers['Authorization']='Bearer '+token
  if origin:headers['Origin']=origin
  req=urllib.request.Request(url+path,data=json.dumps(payload).encode() if payload is not None else None,headers=headers)
  try:
   with urllib.request.urlopen(req) as response:return response.status,json.load(response)
  except urllib.error.HTTPError as e:return e.code,json.load(e)
 try:
  check('Unpaired telemetry denied',request('/api/icarus/telemetry')[0]==401)
  check('Wrong pairing PIN denied',request('/api/pair',{'pin':'wrong'})[0]==403)
  with sync_playwright() as pw:
   b=pw.chromium.launch(executable_path=os.environ.get('ICARUS_CHROMIUM') or None);pc=b.new_context();pc.add_init_script("sessionStorage.setItem('icarusHostKey','lite-fixture-host')");p=pc.new_page();p.on('pageerror',lambda e:r['errors'].append(str(e)));p.goto(url+'/icarus.html?icarus_soak=1');p.wait_for_function('!!window.__icarusSoak')
   phone=b.new_context(**pw.devices['Pixel 5']);t=phone.new_page();t.on('pageerror',lambda e:r['errors'].append(str(e)));t.goto(url);t.locator('#pin').fill(m.PIN);t.locator('#pairBtn').tap();t.locator('#app').wait_for(state='visible');token=t.evaluate("localStorage.getItem('remoteDeckToken')");stored=json.loads(m.DEVICES_FILE.read_text());check('Touch pairing persists only token hash on PC',bool(token) and m.token_hash(token) in stored['token_hashes'] and token not in m.DEVICES_FILE.read_text())
   t.locator('[data-tab="icarus"]').tap();t.wait_for_selector('#tablet-frontier-target option',state='attached');target='LOCAL-RELAY';t.locator('#tablet-frontier-target').select_option(target);t.locator('[data-tablet-nav="course"]').tap();p.wait_for_function('(x)=>__icarusSoak.snapshot().navigation.target===x',arg=target);check('Android-layout course reaches authoritative PC simulation',p.evaluate('__icarusSoak.snapshot().navigation.phase')=='transit');t.locator('[data-tablet-nav="hold"]').tap();p.wait_for_function('__icarusSoak.snapshot().navigation.hold');check('Touch hold reaches PC',True)
   check('Phone remains a thin client',t.evaluate('typeof __icarusSoak')=='undefined');check('Mobile panel fits viewport',t.locator('#tablet-frontier').bounding_box()['width']<=393)
   t.reload();t.locator('#app').wait_for(state='visible');check('Paired phone reconnects after reload',t.evaluate("localStorage.getItem('remoteDeckToken')")==token)
   check('Foreign POST Origin denied',request('/api/action',{'action':'stop'},token,'https://invalid.example')[0]==403)
   check('Predefined keyboard macro routes to stub only',request('/api/action',{'action':'macro','name':'Copy'},token)[0]==200 and any(x['operation']=='hotkey' for x in calls))
   check('Emergency stop routes to input release',request('/api/action',{'action':'stop'},token)[0]==200)
   check('TV public address rejected',request('/api/tv/config',{'ip':'8.8.8.8'},token)[0]==400)
   check('TV private address config and allowlisted key contract',request('/api/tv/config',{'ip':'192.168.1.99'},token)[0]==200 and request('/api/tv/key',{'key':'home'},token)[0]==200 and any(x['operation']=='tv_send' and x['payload']['params']['DataOfCmd']=='KEY_HOME' for x in calls))
   check('Unpair invalidates persisted device token',request('/api/unpair',{},token)[0]==200 and request('/api/status',token=token)[0]==401)
   b.close()
  check('No browser script errors',not r['errors']);r['passed']=True
 except Exception as e:r['errors'].append(str(e));r['traceback']=traceback.format_exc()
 finally:server.shutdown();m.release();r['stubbed_io_calls']=calls;(BASE/'reports/mobile_functional.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
raise SystemExit(not r['passed'])
