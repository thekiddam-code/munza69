"""Actual touch input in emulated tablet Chromium against independent extracted Lite."""
import functools,http.server,json,threading,traceback
from datetime import datetime,timezone
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=Path(__file__).resolve().parent;LITE=BASE/'tested/ICARUS_SOL_Command_Interface_Phase4_Lite';r={'passed':False,'checks':[],'errors':[],'limit':'1280x800 CSS landscape, touch/mobile Chromium emulation. No physical Tab S5e/Android/Windows validation.'}
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(LITE/'web')));threading.Thread(target=server.serve_forever,daemon=True).start()
def check(label,value):
 assert value,label;r['checks'].append(label)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium');c=b.new_context(viewport={'width':1280,'height':800},device_scale_factor=2,has_touch=True,is_mobile=True);p=c.new_page();p.on('pageerror',lambda e:r['errors'].append(str(e)));at=datetime(2026,11,9,12,tzinfo=timezone.utc);p.clock.install(time=at);p.clock.pause_at(at);p.goto(f'http://127.0.0.1:{server.server_port}/icarus.html');p.wait_for_function('ICARUSCommandUI.active');check('Ordinary page has no deterministic test hooks',p.evaluate('typeof __icarusSoak')=='undefined')
  def saved():p.evaluate('document.querySelector("#save").click()');p.evaluate('ICARUSDurable.flush()');return p.evaluate('JSON.parse(localStorage.getItem("icarus-v02"))')
  before=saved();p.locator('#icarus-menu [data-page=operations]').tap();check('Touch Bridge has one actual camera',p.locator('#camera-scene').is_visible() and p.locator('#camera-scene').count()==1);p.locator('#icarus-menu [data-page=missions]').tap();p.locator('#page-missions [data-subtab=destinations]').tap();p.locator('[data-location=derelict]').tap();check('Touch destination selector opens retained field console',p.locator('#remote-workspace').is_visible());check('Interior location segment is straight and touch sized',p.locator('[data-location=derelict]').evaluate('e=>getComputedStyle(e).clipPath')=='none' and p.locator('[data-location=derelict]').bounding_box()['height']>=44)
  p.locator('#icarus-menu [data-page=personnel]').tap();p.locator('#page-personnel [data-subtab=social]').tap();check('Touch Crew Social is isolated',p.locator('#area-personnel-social').is_visible() and not p.locator('#remote-workspace').is_visible());p.locator('#icarus-menu [data-page=settings]').tap();p.locator('#hud-density').select_option('touch');check('Existing touch density preference persists',p.evaluate("localStorage.getItem('icarus-hud-density-v088')")=='touch');p.locator('#icarus-menu [data-page=home]').tap();p.locator('#home-edit').tap();p.locator('#home-editor label').filter(has_text='Security cameras').tap();check('Touch custom Home mounts the same single camera',p.locator('.home-widget[data-widget-id=cameras] #camera-scene').count()==1 and p.locator('#camera-scene').count()==1);p.locator('#icarus-menu [data-page=operations]').tap();check('Camera returns to Bridge after touching navigation',p.locator('#area-operations-watch #camera-scene').is_visible());check('Tablet page has no horizontal document overflow',p.evaluate('document.documentElement.scrollWidth')<=1280)
  after=saved();check('Touch observation preserves physical crew, resources, navigation and tick',all(before[k]==after[k] for k in ['crew','economy','navigation','tick']));check('No browser errors',not r['errors']);p.screenshot(path='/workspace/work/phase4_reports/screenshots/tablet_touch_bridge.png');r['passed']=True;b.close()
except Exception as e:r['errors'].append(str(e));r['traceback']=traceback.format_exc()
finally:server.shutdown();(BASE/'reports/tablet_touch.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
raise SystemExit(not r['passed'])
