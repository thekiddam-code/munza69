"""Real-browser deterministic and adverse-condition tests; isolated local saves only."""
import argparse
import functools
import http.server
import json
import os
from pathlib import Path
import threading
import unittest
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
class Integration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT/'web')))
        threading.Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.codec='window.__icarusExtendedTest=true;'+(ROOT/'web/vendor/lz-string.min.js').read_text()+';'+(ROOT/'web/save-store.js').read_text()
        cls.pw=sync_playwright().start()
        cls.browser=cls.pw.chromium.launch(headless=True,executable_path=os.environ.get('ICARUS_CHROMIUM') or None)
        cls.url=f'http://127.0.0.1:{cls.server.server_port}/icarus.html?icarus_soak=1'
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop();cls.server.shutdown()
    def setUp(self):self.contexts=[];self.errors=[]
    def tearDown(self):
        for c in self.contexts:c.close()
        self.assertEqual(self.errors,[])
    def page(self):
        c=self.browser.new_context();self.contexts.append(c);c.add_init_script(self.codec+';window.__icarusSeed=10101;')
        p=c.new_page();p.on('pageerror',lambda e:self.errors.append(str(e)));p.goto(self.url);p.wait_for_function('!!window.__icarusSoak');return p
    def snap(self,p):
        p.wait_for_function('!!window.__icarusSoak');return p.evaluate('window.__icarusSoak.snapshot()')
    def advance(self,p,n):
        while n:p.evaluate('n=>window.__icarusSoak.advance(n)',min(120,n));n-=min(120,n)
    def configure(self,p,code):
        self.assertTrue(p.evaluate('window.__icarusSoak.save()'))
        p.add_init_script(self.codec+";"+"""(()=>{if(sessionStorage.getItem('fixture'))return;sessionStorage.setItem('fixture','1');const s=JSON.parse(localStorage.getItem('icarus-v02'));"""+code+";if(s.clock){s.clock.elapsed=s.minute-480;s.tick=s.clock.elapsed;}localStorage.setItem('icarus-v02',JSON.stringify(s));})();")
        p.reload();p.wait_for_function('!!window.__icarusSoak')
    def test_seeded_full_engine_reproduces(self):
        a=self.page();b=self.page();self.advance(a,360);self.advance(b,360);self.assertEqual(self.snap(a),self.snap(b))
    def test_mid_simulation_reload_then_future_is_identical(self):
        a=self.page();b=self.page();self.advance(a,240);self.advance(b,240)
        self.assertTrue(a.evaluate('window.__icarusSoak.save()'));before=self.snap(a);a.reload();self.assertEqual(before,self.snap(a))
        self.advance(a,240);self.advance(b,240);self.assertEqual(self.snap(a),self.snap(b))
    def test_weekly_casualty_and_personality_continuity(self):
        p=self.page();self.configure(p,"""s.minute=10079;s.tick=9599;s.crew[0].vitals.health=0;s.crew[1].memories.push('continuity marker');s.crew[1].relationships[s.crew[2].name]=7;s.crew[1].vitals.missions=9;""")
        self.advance(p,1);snap=self.snap(p);self.assertEqual(snap['episode'],2);self.assertEqual(len(snap['crew']),19);self.assertEqual(snap['living']['deceased'][0]['name'],'Frank Morrow')
        survivor=next(x for x in snap['crew'] if x['name']=='Mara Chen');self.assertIn('continuity marker',survivor['memories']);self.assertEqual(survivor['vitals']['missions'],9);self.assertEqual(survivor['relationships']['Dr. Voss'],7)
        self.assertTrue(p.evaluate('window.__icarusSoak.save()'));p.reload();self.assertEqual(snap,self.snap(p))
    def test_extinction_remains_saved_and_does_not_repopulate_next_week(self):
        p=self.page();self.configure(p,'s.minute=10079;s.tick=9599;for(const p of s.crew)p.vitals.health=0;');self.advance(p,3);snap=self.snap(p);self.assertEqual(len(snap['crew']),0);self.assertEqual(len(snap['living']['deceased']),20);self.assertEqual(snap['episode'],2)
        self.assertTrue(p.evaluate('window.__icarusSoak.save()'));p.reload();self.assertEqual(snap,self.snap(p))
    def test_legacy_save_migrates_without_losing_research(self):
        p=self.page();self.configure(p,"delete s.entities;delete s.experiences;delete s.emergencyOps;delete s.chronicles;delete s.universe;delete s.navigation;delete s.logistics;delete s.frontier;delete s.clock;delete s.economy;delete s.teamLog;delete s.living;delete s.entropy;delete s.chronicle;delete s.operations;for(const p of s.crew)delete p.vitals;s.remoteCore.director.science.cases=[];delete s.remoteCore.director.science.programs;delete s.remoteCore.director.science.experiments;")
        self.advance(p,1);self.assertEqual(len(self.snap(p)['crew']),20);self.assertTrue(all(x['vitals']['health']==100 for x in self.snap(p)['crew']));self.assertTrue(p.evaluate('window.__icarusSoak.save()'))
    def test_recap_options_have_real_sources_and_survive_reload(self):
        p=self.page();self.advance(p,240);p.locator('#credits').click();p.locator('#recap-anthology').check();p.locator('#recap-killcam').check();text=p.locator('#recap').inner_text();self.assertIn('not recorded camera footage',text);self.assertIn('No extraordinary lethal encounter',text)
        snap=self.snap(p);ids={e['id'] for e in snap['chronicle']['records']};self.assertTrue(ids);self.assertTrue(snap['chronicle']['options']['anthology']);self.assertTrue(p.evaluate('window.__icarusSoak.save()'));p.reload();self.assertEqual(snap,self.snap(p))
    def test_unsafe_medbay_cannot_heal_injuries_or_spend_cartridges(self):
        p=self.page();self.configure(p,"""s.tissueRepair={cartridges:12,condition:96,cycles:0,activePatient:null};s.crew[0].room='A08';s.crew[0].vitals.health=40;s.crew[0].route=[];s.crew[0].taskMinutes=999;s.power=0;s.physicalWorld.rooms.A08.atmosphere={pressure:20,oxygen:3,temperature:90,smoke:90,fire:true,breach:true};""")
        before=self.snap(p)['crew'][0]['vitals']['health'];p.evaluate('window.__icarusSoak.save()');cartridges=p.evaluate("JSON.parse(localStorage.getItem('icarus-v02')).tissueRepair.cartridges");self.advance(p,1);after=self.snap(p)['crew'][0]['vitals']['health'];self.assertLess(after,before);p.evaluate('window.__icarusSoak.save()');self.assertEqual(cartridges,p.evaluate("JSON.parse(localStorage.getItem('icarus-v02')).tissueRepair.cartridges"))

    def test_critical_atmosphere_emergency_blocks_new_launches(self):
        p=self.page();self.configure(p,"s.physicalWorld.rooms.C07.atmosphere={pressure:20,oxygen:7,temperature:90,smoke:90,fire:true,breach:true};")
        self.advance(p,1);snap=self.snap(p);self.assertTrue(all(m is None for m in snap['missions'].values()))
    def test_exhausted_reserves_cannot_fund_research(self):
        p=self.page();self.configure(p,"""s.operations={reserve:{food:0,tools:0,spares:0,lab:0},transfers:[]};s.economy.feedstock.ore=0;for(const k of Object.keys(s.interactions.supplies))s.interactions.supplies[k]=0;s.specimenCustody={items:[{id:'FIXTURE',status:'stored',name:'synthetic mineral',origin:'asteroid',integrity:100,contamination:0,volatile:false}],history:[]};s.remoteCore.director.science={cases:[{id:'FIXTURE-CASE',specimenId:'FIXTURE',location:'asteroid',item:'synthetic mineral',status:'complete',classification:'geological material',progress:100}],nextCase:2,lastTick:-1};""")
        self.advance(p,120);snap=self.snap(p);self.assertEqual(snap['director']['science']['experiments'],[]);self.assertEqual(snap['director']['science']['programs'][0]['blocker'],'lab');self.assertEqual(snap['operations']['reserve']['lab'],0)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--report',default='integration_report.json');args=parser.parse_args()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Integration)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    Path(args.report).write_text(json.dumps({'passed':result.wasSuccessful(),'tests_run':result.testsRun,'failures':[{'test':str(t),'detail':d} for t,d in result.failures],'errors':[{'test':str(t),'detail':d} for t,d in result.errors]},indent=2))
    raise SystemExit(not result.wasSuccessful())
