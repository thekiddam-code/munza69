import sys,json
from pathlib import Path
sys.path[:0]=['/workspace/work/phase41_final_validation/tested/ICARUS_Phase4_1_Command_Bridge_Lite','/workspace/work/munza69/ICARUS']
import test_umbra_browser as m
m.ROOT=Path('/workspace/work/phase41_final_validation/tested/ICARUS_Phase4_1_Command_Bridge_Lite');out=Path('/workspace/work/phase41_final_validation/reports/screenshots');out.mkdir(exist_ok=True)
m.UmbraBrowser.setUpClass();t=m.UmbraBrowser('test_preserved_departments_offline_icons_and_adaptive_screenshots');t.setUp()
try:
 pc=t.page(pc=True);before=pc.evaluate('__icarusSoak.snapshot()');pc.set_viewport_size({'width':1920,'height':1080});pc.screenshot(path=str(out/'desktop_home.png'));pc.evaluate("ICARUSCommandUI.navigate('operations','watch')");pc.screenshot(path=str(out/'desktop_bridge.png'),full_page=True)
 phone=t.page(width=393,height=851);t.tab(phone,'icarus');phone.wait_for_function("!!UmbraLive.current?.telemetry?.operations");phone.screenshot(path=str(out/'phone_live_terminal.png'),full_page=True);phone.set_viewport_size({'width':1280,'height':800});phone.screenshot(path=str(out/'tablet_live_terminal.png'),full_page=True);t.tab(phone,'tv');phone.screenshot(path=str(out/'tablet_retained_tv.png'));pc.keyboard.press('Control+Shift+F12');pc.screenshot(path=str(out/'creator_mode.png'));assert pc.evaluate('__icarusSoak.snapshot()')==before
 (out.parent/'screenshots.json').write_text(json.dumps({'passed':True,'actual_local_HTTP_SSE_projection':True,'world_unchanged':True,'screenshots':sorted(p.name for p in out.glob('*.png')),'physical_device':False},indent=2))
finally:t.tearDown();m.UmbraBrowser.tearDownClass()
