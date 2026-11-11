"""Read-only control inventory and before/after screenshots; no simulated incidents."""
import json,re
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT=Path('/workspace/work/phase4_reports');ROOT=Path(__file__).resolve().parent
routes={'operations':['watch'],'ship':['overview','systems','cameras'],'personnel':['roster','activity','medical','social'],'missions':['active','destinations','logistics'],'research':['projects','evidence','lazarus'],'records':['timeline','sunday','archives'],'settings':['general','data','testing','advanced']}
with sync_playwright() as w:
 b=w.chromium.launch(executable_path='/usr/bin/chromium');p=b.new_page(viewport={'width':1920,'height':1080});p.goto('http://127.0.0.1:8874/icarus.html?icarus_soak=1');p.wait_for_function('!!window.__icarusSoak');before=p.evaluate('__icarusSoak.snapshot()');seen={}
 for page,tabs in routes.items():
  for tab in tabs:
   p.locator(f'#icarus-menu [data-page={page}]').click();p.locator(f'#page-{page} [data-subtab={tab}]').click()
   for e in p.locator(f'#area-{page}-{tab} details').all():
    if not e.evaluate('e=>e.open') and e.is_visible():e.locator(':scope > summary').click()
   for el in p.evaluate('''()=>[...document.querySelectorAll('button,input,select,textarea')].filter(e=>e.id&&e.getBoundingClientRect().height>0).map(e=>({id:e.id,label:(e.textContent||e.getAttribute('aria-label')||e.type).trim().slice(0,100),handler:!!(e.onclick||e.onchange||e.oninput)}))'''):
    seen.setdefault(el['id'],{**el,'page':page,'subtab':tab})
 after=p.evaluate('__icarusSoak.snapshot()');assert before==after,'Inspecting all pages changed simulation state'
 p.locator('[data-page=home]').click();p.screenshot(path=str(OUT/'after_home.png'));p.locator('[data-page=operations]').click();p.locator('.directive-toolbar').screenshot(path=str(OUT/'after_directive_toolbar.png'));p.locator('[data-page=missions]').click();p.locator('#page-missions [data-subtab=destinations]').click();p.locator('.location-nav').screenshot(path=str(OUT/'after_locations.png'))
 # All old DOM controls remain, including deliberately hidden compatibility/closed-dialog nodes.
 old=json.loads((OUT/'baseline_controls.json').read_text());missing=[];rows=[]
 for el in old:
  if not el['id']:continue
  id=el['id'];n=p.locator('[id="'+id+'"]');record=seen.get(id);exists=n.count()>0
  if not exists:missing.append(id)
  rows.append({'id':id,'baseline_label':el['text'][:65],'present':exists,'location':record or 'Home/live widget, closed replay/director/legacy compatibility, or dynamically selected content; see grouped map'})
 (OUT/'control_inventory.json').write_text(json.dumps({'unchanged_world_during_full_inventory':True,'existing_controls':rows,'missing_ids':missing,'reachable_ids':seen},indent=2));b.close()
print(json.dumps({'baseline_id_controls':len(rows),'seen_id_controls':len(seen),'missing':missing}))
