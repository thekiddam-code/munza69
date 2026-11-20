"""Full-browser 4.9 voyage campaigns. Reports actual prefix checkpoints; no organism injections."""
import argparse,hashlib,json,os,sys,time
from pathlib import Path
from test_specimen_integration import SpecimenIntegration

def summarize(s,seconds,seed,days,reload_exact):
 b=s['unifiedWorld']['biologicalLife49'];org=[o for o in s['unifiedWorld']['organisms'].values() if o.get('life49')]
 audits={k:s[k] for k in ['biologyAudit','resourceAudit','creatureAudit','systemsAudit','expeditionAudit','droneAudit','knowledgeAudit','transitAudit']}
 return {'scope':'Full existing browser engine; autonomous production logic in accelerated isolated technical voyage. No specimens/findings/incidents injected. 7/30/90 are prefixes of the same seeded run.','seed':seed,'days':days,'tick':s['tick'],'wall_seconds':seconds,'effective_simulated_seconds_per_real_second':s['tick']*60/max(.001,seconds),'crew_alive':len(s['crew']),'crew_deceased':len(s['living'].get('deceased',[])),'biological_stats':b['stats'],'habitats_examined':sum(h['examined'] for h in b['habitats'].values()),'enclosures_occupied':sum(bool(c['occupant']) for c in b['enclosures'].values()),'organisms_registered':len(org),'organism_conditions':[{'id':o['id'],'health':o['behavior']['health'],'location':o['location'],'sealed':o['sealed']} for o in org if o['life49'].get('custodyId')],'mission_launches':s['teamLog']['launches'],'mission_statuses':{k:sum(j['status']==k for j in s['director']['registry']) for k in set(j['status'] for j in s['director']['registry'])},'asteroid_locations_visited':sum(r.get('visited',False) for r in s['world']['asteroidExploration']['rooms']),'science_cases':len(s['director']['science']['cases']),'experiments_complete':sum(e['status']=='complete' for e in s['director']['science'].get('experiments',[])),'event_kinds':sorted(set(r['kind'] for r in s['chronicle']['records'])),'biological_state_bytes':len(json.dumps(b)),'diagnostic_snapshot_bytes':len(json.dumps(s)),'resource_stock':s['economy']['stock'],'audits':audits,'save_reload_exact':reload_exact,'passed':all(not e for e in audits.values()) and reload_exact and len(s['crew'])+len(s['living'].get('deceased',[]))==20,'initial_canonical_adult_dormant':s['unifiedWorld']['organisms']['XENO-INITIAL']['dormant']}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--seeds',type=int,nargs='+',default=[10101,4242,2026]);ap.add_argument('--days',type=int,nargs='+',default=[7,30,90]);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);SpecimenIntegration.setUpClass();results=[]
 try:
  for seed in a.seeds:
   t=SpecimenIntegration('test_bio_natural_acquisition_camera_research_and_restart');t.setUp();start=time.monotonic()
   try:
    c=t.browser.new_context();t.contexts.append(c);c.add_init_script(t.codec+';window.__icarusSeed='+str(seed)+';');p=c.new_page();p.on('pageerror',lambda e:t.errors.append(str(e)));p.goto(t.url);p.wait_for_function('!!window.__icarusSoak');ticks=0
    for day in sorted(a.days):
     target=day*1440
     while ticks<target:
      n=min(120,target-ticks);p.evaluate('n=>__icarusSoak.advance(n)',n);ticks+=n
      if ticks%10080==0:print('PROGRESS',seed,round(ticks/1440,2),round(time.monotonic()-start,1),flush=True)
     before=p.evaluate('JSON.stringify(__icarusSoak.snapshot())');p.evaluate('__icarusSoak.save()');p.evaluate('ICARUSDurable.flush({cache:true})');p.reload();p.wait_for_function('!!window.__icarusSoak');after=p.evaluate('JSON.stringify(__icarusSoak.snapshot())');s=json.loads(after);r=summarize(s,time.monotonic()-start,seed,day,before==after);r['simulation_errors']=list(t.errors);r['passed']=r['passed'] and not t.errors;results.append(r);(a.out/(str(seed)+'_'+str(day)+'d.json')).write_text(json.dumps(r,indent=2));print('CHECKPOINT',json.dumps({k:r[k] for k in ['seed','days','passed','crew_alive','biological_stats','wall_seconds']}),flush=True)
   finally:t.tearDown()
 finally:SpecimenIntegration.tearDownClass()
 (a.out/'summary.json').write_text(json.dumps({'campaigns':results,'passed':all(r['passed'] for r in results)},indent=2));return not all(r['passed'] for r in results)
if __name__=='__main__':raise SystemExit(main())
