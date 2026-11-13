"""Normal-time observation of the actual host; no accelerated clock or forced incidents."""
import argparse,hashlib,json,os,time,traceback
from pathlib import Path
import test_umbra_browser as host_tests

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--minutes',type=float,default=30);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--runtime',type=Path,default=Path(__file__).resolve().parent);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True);host_tests.ROOT=a.runtime;T=host_tests.UmbraBrowser;T.setUpClass();t=T();t.setUp();r={'requested_minutes':a.minutes,'elapsed_seconds':0,'mode':'NORMAL production timer, actual elapsed monotonic time; no soak hooks, speed override, event injection or scripted dialogue','runtime_sha256':{str(p.relative_to(a.runtime)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((a.runtime/'web').rglob('*')) if p.is_file()},'samples':[],'reloads':[],'errors':[],'passed':False,'limits':'Linux Chromium actual server with desktop/TV I/O stubbed; no physical Windows/Android/TV or real Tailscale. Camera selections and a save/reload are observer/operator actions.'};start=time.monotonic()
 try:
  c=T.browser.new_context(viewport={'width':1440,'height':1000},timezone_id='America/Chicago');t.contexts.append(c);c.add_init_script('window.__icarusSeed=1001;');p=c.new_page();p.on('pageerror',lambda e:r['errors'].append(str(e)));p.goto(T.url+'/icarus.html');p.wait_for_function('!!window.ICARUSObservationLive');assert p.evaluate('typeof __icarusSoak')=='undefined';p.evaluate("ICARUSCommandUI.navigate('operations','watch')");p.locator('#camera-scene').scroll_into_view_if_needed();start=time.monotonic();last=-1;reloaded=False
  while time.monotonic()-start<a.minutes*60:
   p.wait_for_timeout(1000);elapsed=time.monotonic()-start;minute=int(elapsed//60)
   if minute==last:continue
   last=minute;sample=p.evaluate('''()=>({tick:ICARUSObservationLive.camera.tick,camera:ICARUSObservationLive.camera.selected,stats:{...ICARUSObservationLive.camera.stats},heap:performance.memory?.usedJSHeapSize??null,status:document.querySelector('#status').textContent,creator:ICARUSBridgeMode.creator})''');sample['elapsed_seconds']=elapsed;r['samples'].append(sample);p.locator('.obs-preview .obs-promote').nth(minute%4).click();p.locator('#camera-scene').scroll_into_view_if_needed()
   if minute in [0,10,20]:p.locator('#camera-scene').screenshot(path=str(a.output/f'camera_minute_{minute}.png'))
   if elapsed>=a.minutes*30 and not reloaded:
    p.evaluate("document.getElementById('save').click()");p.evaluate('ICARUSDurable.flush()');before=p.evaluate('JSON.parse(localStorage.getItem("icarus-v02"))');p.reload();p.wait_for_function('!!window.ICARUSObservationLive');p.evaluate("ICARUSCommandUI.navigate('operations','watch')");p.locator('#camera-scene').scroll_into_view_if_needed();p.wait_for_timeout(500);tick=p.evaluate('ICARUSObservationLive.camera.tick');assert tick>=before['tick'];r['reloads'].append({'at_seconds':elapsed,'saved_tick':before['tick'],'resumed_tick':tick,'saved_names':[q['name'] for q in before['crew']]});reloaded=True
   r['elapsed_seconds']=elapsed;(a.output/'observation.json').write_text(json.dumps(r,indent=2));print('Observed real minute',minute,'ship tick',sample['tick'],'camera',sample['camera'],flush=True)
  p.evaluate("document.getElementById('save').click()");p.evaluate('ICARUSDurable.flush()');s=p.evaluate('JSON.parse(localStorage.getItem("icarus-v02"))');r['final']={'tick':s['tick'],'crew':[q['name'] for q in s['crew']],'dead':[d['name'] for d in s['living']['deceased']],'conversations':s['crewLife']['conversations'],'activities':{p['name']:p['task'] for p in s['crew']},'events':len(s['chronicle']['records']),'calendar':s.get('calendar'),'room_lighting':s.get('roomLighting',{})};(a.output/'final_test_world.json').write_text(json.dumps(s));assert len(s['crew'])+len(s['living']['deceased'])==20;r['passed']=not r['errors'] and len(r['reloads'])==1 and s['tick']>0
 except Exception as e:r['errors'].append(str(e));r['traceback']=traceback.format_exc()
 finally:r['elapsed_seconds']=time.monotonic()-start;r['errors'].extend(t.errors);r['passed']=r['passed'] and not r['errors'];(a.output/'observation.json').write_text(json.dumps(r,indent=2));t.errors=[];t.tearDown();T.tearDownClass()
 return not r['passed']
if __name__=='__main__':raise SystemExit(main())
