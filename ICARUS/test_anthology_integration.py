"""Default-core browser tests. Legacy compatibility is a separate suite, never a substitute."""
import argparse,json,unittest,os
from pathlib import Path
from test_integration import Integration,Quiet,ROOT
from test_continuity import RecordedResult
V13_WEB=Path(os.environ.get('ICARUS_V13_WEB',ROOT.parents[1]/'v13_package/ICARUS/web'))
class CoreIntegration(Integration):
    @classmethod
    def setUpClass(cls):
        super().setUpClass();cls.codec=cls.codec.replace('window.__icarusExtendedTest=true;','')
        class Editions(Quiet):
            def translate_path(self,path):
                if path.startswith('/extended/'):
                    old=self.directory;self.directory=str(V13_WEB)
                    try:return super().translate_path(path.removeprefix('/extended'))
                    finally:self.directory=old
                return super().translate_path(path)
        import functools
        cls.server.RequestHandlerClass=functools.partial(Editions,directory=str(ROOT/'web'))
    def page(self):
        c=self.browser.new_context();self.contexts.append(c);c.add_init_script('window.__icarusSeed=10101;');p=c.new_page();p.on('pageerror',lambda e:self.errors.append(str(e)));p.goto(self.url);p.wait_for_function('!!window.__icarusSoak');return p
    def configure(self,p,code):
        self.assertTrue(p.evaluate('__icarusSoak.save()'));p.evaluate('ICARUSDurable.flush()')
        script=(ROOT/'web/vendor/lz-string.min.js').read_text()+";(()=>{if(sessionStorage.getItem('fixture'))return;sessionStorage.setItem('fixture','1');const raw=localStorage.getItem('icarus-anthology-v14');const s=JSON.parse(raw.startsWith('ICARUS-LZ1:')?LZString.decompressFromUTF16(raw.slice(11)):raw);"+code+";if(s.clock){s.clock.elapsed=s.minute-480;s.tick=s.clock.elapsed;}localStorage.setItem('icarus-anthology-v14',JSON.stringify(s));})();"
        p.add_init_script(script);p.reload();p.wait_for_function('!!window.__icarusSoak')
    def deck(self,p,page,tab=None):
        if page=='settings' and tab in ('testing','advanced') and p.locator('body').get_attribute('data-bridge-mode')!='creator':p.keyboard.press('Control+Shift+F12')
        p.locator('#icarus-menu button[data-page="'+page+'"]').click()
        if tab:p.locator('#page-'+page+' [data-subtab="'+tab+'"]').click()
    def operations(self,p):p.locator('#icarus-menu button[data-page="operations"]').click()
    def test_core_replaces_stellar_dashboard_and_remains_tablet_usable(self):
        p=self.page();p.set_viewport_size({'width':768,'height':1024});self.operations(p);self.assertEqual(p.locator('#star-map').count(),0);self.assertIn('SOL DIRECTIVES',p.locator('#frontier-controls').inner_text());self.assertLessEqual(p.locator('#frontier-controls').bounding_box()['width'],768);self.assertEqual(p.locator('#frontier-target option').count(),6)
    def test_quiet_preferences_and_positive_only_channel_use_actual_nonlethal_outcomes(self):
        p=self.page();self.deck(p,'settings','general');p.locator('summary').filter(has_text='Encounter preferences').click();p.locator('#encounter-frequency').select_option('0');p.locator('#encounter-apply').click();self.advance(p,1440);self.assertEqual(len([a for a in self.snap(p)['anthology']['arcs'] if 'signalHour'in a]),0)
        self.deck(p,'settings','general');p.locator('#encounter-frequency').select_option('3')
        for e in p.locator('[data-tone]').all():e.fill('5' if e.get_attribute('data-tone')=='joyful' else '0')
        p.locator('#encounter-apply').click();self.advance(p,4320);s=self.snap(p);external=[a for a in s['anthology']['arcs'] if 'signalHour'in a];self.assertGreater(len(external),0);self.assertTrue(all(a['category']=='joyful' for a in external));self.assertTrue(any(a.get('outcome')=='shared_moment' for a in external));self.assertEqual(s['resourceAudit'],[])
    def test_core_durable_commit_abort_keeps_previous_acknowledged_snapshot(self):
        p=self.page();self.advance(p,360);p.evaluate('__icarusSoak.save()');p.evaluate('ICARUSDurable.flush()');before=self.snap(p);p.evaluate('window.__icarusAbortAllWrites=true');self.advance(p,120);p.evaluate('__icarusSoak.save()');self.assertFalse(p.evaluate('ICARUSDurable.flush().then(()=>true).catch(()=>false)'));p.reload();self.assertEqual(self.snap(p),before)
    def test_full_backup_roundtrip_keeps_story_sources_memories_and_preferences(self):
        p=self.page();self.advance(p,3000);p.evaluate('__icarusSoak.save()');p.evaluate('ICARUSDurable.flush()');before=self.snap(p)
        self.deck(p,'settings','data')
        with p.expect_download() as dl:p.locator('#durable-export').click()
        payload=Path(dl.value.path()).read_bytes();backup=json.loads(payload);self.assertEqual(backup['appVersion'],'1.8.0-phase4');self.assertTrue(backup['historyComplete']);history={r['id'] for r in backup['history']};self.assertTrue(all(set(a['sources'])<=history for a in before['anthology']['arcs']))
        q=self.page();q.on('dialog',lambda d:d.accept());q.locator('#backupfile').set_input_files({'name':'core.json','mimeType':'application/json','buffer':payload});q.wait_for_function("document.querySelector('#backupmessage').textContent.includes('Restored')");q.evaluate('ICARUSDurable.flush()');after=self.snap(q)
        for key in ['crew','anthology','economy','universe','navigation','director','experiences']:self.assertEqual(after[key],before[key],key)
        q.reload();self.assertEqual(self.snap(q),after)
    def test_true_v13_import_is_explicit_preserves_active_world_and_does_not_overwrite_extended_save(self):
        self.assertTrue((V13_WEB/'icarus.html').exists(),'Supply archived v1.3 for migration test')
        p=self.page();p.goto(self.url.replace('/icarus.html?','/extended/icarus.html?'));p.wait_for_function('!!window.__icarusSoak');self.advance(p,720);p.evaluate('__icarusSoak.save()');p.evaluate('ICARUSDurable.flush()');old=self.snap(p);oldraw=p.evaluate("localStorage['icarus-v02']");payload=p.evaluate("JSON.stringify({format:'ICARUS_SAVE',formatVersion:1,appVersion:'1.3',state:JSON.parse(localStorage.getItem('icarus-v02')),ideas:[]})")
        p.goto(self.url);p.wait_for_function('!!window.__icarusSoak');self.assertEqual(self.snap(p)['tick'],0);self.assertEqual(p.evaluate("localStorage['icarus-v02']"),oldraw)
        p.on('dialog',lambda d:d.accept());p.locator('#backupfile').set_input_files({'name':'v13.json','mimeType':'application/json','buffer':payload.encode()});p.wait_for_function("document.querySelector('#backupmessage').textContent.includes('Restored')");p.evaluate('ICARUSDurable.flush()');new=self.snap(p)
        for key in ['crew','navigation','economy','director','missions','experiences','emergencyOps']:self.assertEqual(new[key],old[key],key)
        for key,sys in old['universe']['systems'].items():self.assertEqual(new['universe']['systems'][key],sys)
        self.assertEqual(p.evaluate("localStorage['icarus-v02']"),oldraw);self.advance(p,1500);self.assertEqual(len(self.snap(p)['universe']['systems']),len(new['universe']['systems']));self.assertEqual(self.snap(p)['frontierAudit'],[])
    def test_sealed_hatch_blocks_medical_retrieval_without_crash_or_teleportation(self):
        p=self.page();self.configure(p,"""s.remoteCore.autonomyEnabled=false;const p=s.crew[0];p.room='C04';p.target='C04';p.route=[];p.energy=0;p.vitals.health=40;p.survivalIncapacitated=true;p.taskMinutes=999;s.physicalWorld.rooms.C04.door='sealed';""");self.advance(p,6);s=self.snap(p);patient=s['crew'][0];self.assertEqual(patient['room'],'C04');self.assertTrue(patient['survivalIncapacitated']);self.assertFalse(patient.get('rescueMedic'));self.assertEqual(s['resourceAudit'],[])
    def test_sealed_fire_compartment_does_not_crash_evacuation_or_dispatch_unreachable_engineers(self):
        p=self.page();self.configure(p,"""s.remoteCore.autonomyEnabled=false;const p=s.crew[0];p.room='C04';p.target='C04';p.route=[];p.energy=90;p.taskMinutes=999;s.physicalWorld.rooms.C04.door='sealed';Object.assign(s.physicalWorld.rooms.C04.atmosphere,{fire:true,pressure:70,oxygen:18,temperature:60,smoke:10});""");self.advance(p,8);s=self.snap(p);self.assertEqual(s['crew'][0]['room'],'C04');self.assertFalse(any(q.get('emergencyId')=='C04' for q in s['crew'] if q['room']!='C04'));self.assertEqual(s['resourceAudit'],[])
    def test_unsaved_encounter_preferences_survive_live_panel_refresh(self):
        p=self.page();self.deck(p,'settings','general');p.locator('summary').filter(has_text='Encounter preferences').click();p.locator('[data-tone="joyful"]').fill('2.75');p.locator('[data-tone="social"]').fill('0');self.deck(p,'settings','data');p.locator('#save').click();self.deck(p,'settings','general');self.assertEqual(p.locator('[data-tone="joyful"]').input_value(),'2.75');self.assertEqual(p.locator('[data-tone="social"]').input_value(),'0');self.assertEqual(self.snap(p)['anthology']['config']['weights']['joyful'],1);p.locator('#encounter-apply').click();self.assertEqual(self.snap(p)['anthology']['config']['weights']['joyful'],2.75)
    def test_actual_reserve_deficit_triggers_finite_local_extraction(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;
        const d=Object.values(s.universe.systems).flatMap(x=>x.bodies).find(d=>d.id==='LOCAL-RELAY');d.visited=true;d.surveyed=true;d.observedHazard=.05;s.navigation.current=d.id;s.navigation.position={x:d.x,y:d.y};
        const used=s.economy.feedstock.fuel-20;s.economy.feedstock.fuel=20;s.economy.feedstockUsed.fuel=(s.economy.feedstockUsed.fuel||0)+used;
        const source='explicit core adverse fuel depletion';s.economy.ledger=s.economy.ledger||{};s.economy.ledger[JSON.stringify(['feedstock_use','fuel',source])]={kind:'feedstock_use',key:'fuel',source,amount:used,count:1,first:s.tick,last:s.tick};
        """);before=self.snap(p);self.advance(p,2500);after=self.snap(p);self.assertGreater(after['logistics']['credited'].get('fuel',0),0);self.assertEqual(after['resourceAudit'],[]);self.assertEqual(after['frontierAudit'],[]);self.assertTrue(any(j.get('resource')=='fuel' and 'reserve deficit' in j['reason'] for j in after['frontier']['jobs']))
        dest=next(d for sys in after['universe']['systems'].values() for d in sys['bodies'] if d['id']=='LOCAL-RELAY');self.assertLess(dest['deposits']['fuel'],600)
    def test_nonmodal_chronicle_cards_include_recorded_story_sources(self):
        p=self.page();self.advance(p,3000);s=self.snap(p);self.assertTrue(s['anthology']['arcs']);ids={r['id'] for r in p.evaluate('ICARUSDurable.history()')};self.assertTrue(all(set(a['sources'])<=ids for a in s['anthology']['arcs']));self.deck(p,'records','sunday');p.locator('#area-records-sunday summary').filter(has_text='Sunday chronicle').click();self.assertIn('NOT CAMERA FOOTAGE',p.locator('#area-records-sunday').inner_text());before=s['tick'];p.locator('[data-chronicle="next"]').click();self.assertEqual(self.snap(p)['tick'],before)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report',default='anthology_integration.json');args=ap.parse_args();r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(CoreIntegration));Path(args.report).write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
