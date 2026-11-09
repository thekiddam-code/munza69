"""Full browser regressions plus transactional storage and constrained rescue fixtures."""
import argparse,json,unittest
from pathlib import Path
from test_frontier_integration import FrontierIntegration,RecordedResult
class LivingFrontierIntegration(FrontierIntegration):
    def test_unavailable_database_warns_and_retains_uncommitted_history_for_export(self):
        c=self.browser.new_context();self.contexts.append(c);c.add_init_script("Object.defineProperty(window,'indexedDB',{value:{open(){throw Error('Explicit unavailable-storage fixture')}}});window.__icarusSeed=10101;")
        p=c.new_page();p.on('pageerror',lambda e:self.errors.append(str(e)));p.goto(self.url);p.wait_for_function('!!window.__icarusSoak');self.advance(p,1500)
        self.assertEqual(p.evaluate('ICARUSDurable.status.backend'),'local-fallback');self.assertIn('unavailable',p.evaluate('ICARUSDurable.status.warning'));self.assertFalse(p.evaluate('window.__icarusSoak.save()'))
        history=p.evaluate('ICARUSDurable.history()');ids={r['id'] for r in history};self.assertGreater(len(history),64);self.assertTrue(all(r['id'] in ids for r in self.snap(p)['chronicle']['records']))
    def test_daily_metrics_match_full_world_audits_and_clock_without_mutation(self):
        p=self.page();self.advance(p,2000);before=self.snap(p);daily=p.evaluate('window.__icarusSoak.daily()');self.assertEqual(daily['tick'],before['tick']);self.assertEqual(daily['resource_errors'],before['resourceAudit']);self.assertEqual(daily['frontier_errors'],before['frontierAudit']);self.assertEqual(daily['stores'],before['resourceTotals']);self.assertEqual(daily['case_ids'],[c['id'] for c in before['director']['science']['cases']]);self.assertEqual(self.snap(p),before)
    def test_incomplete_modern_backup_is_rejected_before_replacing_world(self):
        p=self.page();self.advance(p,360);p.evaluate('window.__icarusSoak.save()');before=self.snap(p);payload=p.evaluate("({format:'ICARUS_SAVE',formatVersion:1,appVersion:'1.3',state:JSON.parse(localStorage.getItem('icarus-v02')),ideas:[]})");del payload['state']['entities'];dialogs=[];p.on('dialog',lambda d:(dialogs.append(d.message),d.dismiss()))
        p.locator('#backupfile').set_input_files({'name':'incomplete-modern.json','mimeType':'application/json','buffer':json.dumps(payload).encode()});p.wait_for_function("document.getElementById('backupmessage').textContent.includes('Unsupported or invalid')");self.assertEqual(self.snap(p),before);self.assertEqual(dialogs,[])
    def test_indexeddb_primary_restores_world_when_cache_is_removed(self):
        p=self.page();self.advance(p,1440);self.assertTrue(p.evaluate('window.__icarusSoak.save()'));before=self.snap(p)
        p.add_init_script(self.codec+";localStorage.removeItem('icarus-v02');")
        p.reload();after=self.snap(p);self.assertEqual(after,before);self.assertEqual(p.evaluate('ICARUSDurable.status.backend'),'indexeddb');self.assertGreater(p.evaluate('ICARUSDurable.status.recoveries'),0)
    def test_interrupted_transaction_retains_previous_verified_revision(self):
        p=self.page();self.advance(p,240);self.assertTrue(p.evaluate('window.__icarusSoak.save()'));before=self.snap(p);self.advance(p,120)
        p.evaluate('window.__icarusAbortAllWrites=true');self.assertFalse(p.evaluate('window.__icarusSoak.save()'));self.assertIn('Previous committed',p.evaluate('ICARUSDurable.status.warning'))
        p.reload();after=self.snap(p);self.assertEqual(after,before);self.assertGreater(p.evaluate('ICARUSDurable.status.recoveries'),0)
    def test_recovery_preserves_archived_future_when_new_events_are_recorded(self):
        p=self.page();self.advance(p,240);p.evaluate('window.__icarusSoak.save()');self.advance(p,300);old=p.evaluate('ICARUSDurable.history()');p.evaluate('window.__icarusAbortAllWrites=true');self.assertFalse(p.evaluate('window.__icarusSoak.save()'));p.reload();self.snap(p);self.advance(p,1200);p.evaluate('window.__icarusSoak.save()');history={r['id']:r for r in p.evaluate('ICARUSDurable.history()')};self.assertTrue(all(history[r['id']].get('message')==r.get('message') for r in old));self.assertIn('Q',self.snap(p)['chronicle']['namespace'])
    def test_corrupt_committed_snapshot_falls_back_to_valid_database_revision(self):
        p=self.page();self.advance(p,240);p.evaluate('window.__icarusSoak.save()');before=self.snap(p);self.advance(p,120);p.evaluate('window.__icarusSoak.save()')
        p.evaluate('''async()=>{window.__icarusAbortAllWrites=true;const db=await new Promise(ok=>{const r=indexedDB.open('icarus-voyage',1);r.onsuccess=()=>ok(r.result)});await new Promise((ok,no)=>{const tx=db.transaction('saves','readwrite'),store=tx.objectStore('saves'),r=store.getAll();r.onsuccess=()=>{const records=r.result.sort((a,b)=>b.revision-a.revision);records[0].hash='corrupted by explicit adverse fixture';store.put(records[0]);};tx.oncomplete=ok;tx.onerror=no;});db.close();}''')
        p.reload();self.assertEqual(self.snap(p),before);self.assertGreater(p.evaluate('ICARUSDurable.status.recoveries'),0)
    def test_orphan_snapshot_without_transaction_head_is_never_restored(self):
        p=self.page();self.advance(p,240);p.evaluate('window.__icarusSoak.save()');before=self.snap(p)
        p.evaluate("""async()=>{window.__icarusAbortAllWrites=true;const db=await new Promise(ok=>{const r=indexedDB.open('icarus-voyage',1);r.onsuccess=()=>ok(r.result)});await new Promise((ok,no)=>{const tx=db.transaction('saves','readwrite'),store=tx.objectStore('saves'),r=store.getAll();r.onsuccess=()=>{const last=r.result.sort((a,b)=>b.revision-a.revision)[0],state=JSON.parse(ICARUSSaveStore.decode(last.raw));state.tick=99999;const raw=JSON.stringify(state);store.put({...last,revision:last.revision+10,tick:99999,raw:ICARUSSaveStore.encode(raw),hash:ICARUSDurable.hash(raw),complete:true});};tx.oncomplete=ok;tx.onerror=no;});db.close();}""")
        p.reload();self.assertEqual(self.snap(p),before);self.assertGreater(p.evaluate('ICARUSDurable.status.recoveries'),0)
    def test_indexed_history_retains_provenance_after_live_journal_window_rolls(self):
        p=self.page();self.advance(p,10000);p.evaluate('window.__icarusSoak.save()');snap=self.snap(p);history=p.evaluate('ICARUSDurable.history()');ids={r['id'] for r in history};self.assertGreaterEqual(len(history),len(snap['chronicle']['records']));self.assertTrue(all(r['id'] in ids for r in snap['chronicle']['records']))
        for week in snap['chronicles']['weeks'].values():self.assertTrue(set(week['sourceIds'])<=ids)
        actor=snap['crew'][0]['name'];personal=p.evaluate('(actor)=>ICARUSDurable.history({actor})',actor);self.assertTrue(all(actor in r['people'] for r in personal))
    def test_registry_and_personal_memories_survive_week_and_database_reload(self):
        p=self.page();self.advance(p,12000);before=self.snap(p);self.assertGreater(len(before['entities']['registry']),0);self.assertGreater(len(before['experiences']['records']),0);self.assertTrue(any(j.get('stages') for j in before['frontier']['jobs']));self.assertTrue(p.evaluate('window.__icarusSoak.save()'));p.reload();self.assertEqual(self.snap(p),before)
    def test_missing_capability_blocks_rescue_without_spending_or_teleporting(self):
        p=self.page();self.configure(p,"""
        s.navigation.hold=true;s.remoteCore.autonomyEnabled=false;
        s.emergencyOps.incidents=[{id:'SOS-FIXTURE',missionId:'F-FIXTURE',destination:'HOME',status:'open',created:s.tick,deadline:s.tick+1000,attempts:0,decisions:[],cause:'Explicit missing-capability fixture'}];
        s.remoteCore.missions.frontier={id:'F-FIXTURE',crew:s.crew[0].name,members:[s.crew[0].name],phase:'stranded',stranded:true,incidentId:'SOS-FIXTURE',suits:1,cargo:{},extracted:{},fieldProgress:0};s.teamLog.suits=5;
        s.frontier.jobs=[{id:'F-FIXTURE',status:'active',destination:'HOME',members:[s.crew[0].name],started:s.tick,evidence:[]}];s.frontier.active='F-FIXTURE';s.crew[0].expeditionAway='HOME';s.crew[0].expeditionId='F-FIXTURE';
        for(const person of s.crew.filter(p=>p.job==='Engineer'))person.energy=0;
        """)
        self.open_map(p);before=self.snap(p);p.locator('[data-rescue="SOS-FIXTURE"]').click();after=self.snap(p);self.assertIsNone(after['missions'].get('rescue'));self.assertEqual(after['resourceTotals'],before['resourceTotals']);self.assertEqual(after['crew'][0]['expeditionAway'],'HOME')
    def test_active_eva_rescue_and_stranded_team_cross_week_and_reload_without_reset(self):
        p=self.page();self.configure(p,"""
        s.minute=10079;s.tick=9599;s.clock.elapsed=9599;s.clock.nextEpisodeAt=10080;s.remoteCore.autonomyEnabled=false;s.navigation.hold=true;
        const names=s.crew.slice(0,2).map(p=>p.name),engineer=s.crew.find(p=>p.job==='Engineer'&&!names.includes(p.name));
        for(const p of s.crew.slice(0,2)){p.expeditionId='F-SOS';p.expeditionAway='HOME';p.route=[];}
        engineer.expeditionId='RESCUE-SOS-1';engineer.expeditionAway='RESCUE-SOS-1';engineer.responseAssignment='SOS-1';engineer.route=[];
        s.frontier.active='F-SOS';s.frontier.jobs=[{id:'F-SOS',members:names,destination:'HOME',location:'HOME',type:'survey',duration:240,status:'active',started:9580,evidence:[],progress:40}];
        s.remoteCore.missions.frontier={id:'F-SOS',crew:names[0],members:names,suits:2,phase:'stranded',stranded:true,incidentId:'SOS-1',cargo:{food:1,water:2,oxygen:2},extracted:{},fieldProgress:40,progress:0,conditions:{},decisions:[],plan:{stage:0,stages:[],history:[],loadout:{spares:0},kitCondition:80,exposure:0}};
        s.remoteCore.missions.rescue={id:'RESCUE-SOS-1',crew:engineer.name,members:[engineer.name],suits:1,phase:'outbound',incidentId:'SOS-1',cargo:{food:.4,water:1.2,oxygen:.7},progress:20,conditions:{},decisions:[],started:9580};
        s.teamLog.suits=3;s.economy.initial.food+=1.4;s.economy.initial.water+=3.2;s.economy.initial.oxygen+=2.7;
        s.emergencyOps.incidents=[{id:'SOS-1',missionId:'F-SOS',destination:'HOME',cause:'Explicit interrupted-EVA regression fixture',status:'open',created:9580,deadline:11000,attempts:1,decisions:[]}];s.emergencyOps.stats.stranded=1;s.emergencyOps.stats.rescueAttempts=1;
        """)
        self.advance(p,1);snap=self.snap(p);self.assertEqual(snap['episode'],2);self.assertEqual(snap['missions']['rescue']['progress'],21);self.assertEqual(snap['missions']['frontier']['phase'],'stranded');self.assertEqual(snap['resourceAudit'],[]);self.assertTrue(p.evaluate('window.__icarusSoak.save()'));p.reload();self.assertEqual(self.snap(p),snap)
        self.advance(p,140);after=self.snap(p);self.assertEqual(after['resourceAudit'],[]);self.assertEqual(after['frontierAudit'],[]);self.assertTrue(after['emergencyOps']['incidents'][0]['decisions'])
    def test_ship_repairs_never_use_an_off_ship_engineer_and_release_his_reservation(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.navigation.hold=true;const away=s.crew.find(p=>p.job==='Engineer');away.expeditionId='AWAY';away.expeditionAway='derelict';away.emergencyId='C07';away.room='C07';away.route=[];
        s.remoteCore.missions.derelict={id:'AWAY',crew:away.name,members:[away.name],suits:1,phase:'transit',progress:0,kit:1,cargo:{food:.2,water:.3,oxygen:.3},conditions:{},decisions:[],launched:s.tick};s.teamLog.suits=5;
        s.remoteCore.director.registry=[{id:'AWAY',status:'active',type:'survey',location:'derelict',members:[away.name],crew:away.name,created:s.tick,baseline:{surveyed:1,findings:0}}];s.economy.initial.food+=.2;s.economy.initial.water+=.3;s.economy.initial.oxygen+=.3;
        s.equipment.C07.condition=35;s.emergencies.C07={id:'C07',room:'C07',label:'Explicit off-ship responder regression',status:'active',progress:0,age:1,responders:[],severity:'critical',frames:[],startedAt:'fixture'};
        """)
        self.advance(p,1);after=self.snap(p);away=next(q for q in after['crew'] if q['name']=='Frank Morrow');self.assertNotEqual(away.get('emergencyId'),'C07');self.assertEqual(after['world']['emergencies']['C07']['progress'],0);self.assertEqual(after['resourceAudit'],[])
    def test_chronicle_playback_is_skippable_nonmodal_and_source_grounded(self):
        p=self.page();self.advance(p,1500);self.open_map(p);p.locator('summary').filter(has_text='Sunday chronicle archive').click();before=self.snap(p)['tick'];p.locator('[data-chronicle="play"]').click();p.locator('[data-chronicle="next"]').click();self.assertIn('source CHR-',p.locator('#chronicle-card').inner_text());self.assertEqual(self.snap(p)['tick'],before);self.assertIn('NOT CAMERA FOOTAGE',p.locator('#living-frontier-controls').inner_text())
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report',default='living_frontier_integration.json');args=ap.parse_args();r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(LivingFrontierIntegration));Path(args.report).write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
