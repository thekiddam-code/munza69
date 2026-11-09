"""Real-browser frontier controls and interrupted-travel regressions."""
import argparse,json,unittest
from pathlib import Path
from test_continuity import Continuous,RecordedResult
class FrontierIntegration(Continuous):
    def open_map(self,p):p.locator('#icarus-menu button[data-page="operations"]').click()
    def test_captain_course_hold_and_inflight_reload_preserve_actual_coordinates(self):
        p=self.page();self.configure(p,"s.remoteCore.autonomyEnabled=false;");self.open_map(p)
        options=p.locator('#frontier-target option').evaluate_all('(els)=>els.map(e=>e.value).filter(x=>x!=="HOME")');self.assertTrue(options)
        p.locator('#frontier-target').select_option(options[0]);p.locator('[data-nav="course"]').click();self.advance(p,10);snap=self.snap(p)
        self.assertEqual(snap['navigation']['phase'],'transit');self.assertNotEqual(snap['navigation']['position'],{'x':0,'y':0});self.assertGreater(snap['navigation']['fuelUsed'],0)
        self.assertTrue(p.evaluate('window.__icarusSoak.save()'));p.reload();self.assertEqual(snap,self.snap(p));self.open_map(p);p.locator('[data-nav="hold"]').click();before=self.snap(p);self.advance(p,1);after=self.snap(p);self.assertTrue(after['navigation']['hold']);self.assertNotEqual(before['navigation']['position'],after['navigation']['position'])
    def test_weekly_boundary_during_ship_transit_keeps_leg_and_cooldown(self):
        p=self.page();self.configure(p,"s.remoteCore.autonomyEnabled=false;s.minute=10079;s.tick=9599;s.clock.elapsed=9599;s.clock.nextEpisodeAt=10080;");self.open_map(p)
        target=p.locator('#frontier-target option').evaluate_all('(els)=>els.map(e=>e.value).find(x=>x!=="HOME")');p.locator('#frontier-target').select_option(target);p.locator('[data-nav="course"]').click();before=self.snap(p)
        self.advance(p,1);after=self.snap(p);self.assertEqual(after['episode'],before['episode']+1);self.assertEqual(after['navigation']['leg']['id'],before['navigation']['leg']['id']);self.assertEqual(after['navigation']['leg']['elapsed'],1);self.assertGreater(after['navigation']['fuelUsed'],0);self.assertEqual(after['frontierAudit'],[])
        p.evaluate('window.__icarusSoak.save()');p.reload();self.assertEqual(after,self.snap(p))
    def test_weekly_boundary_does_not_replace_frontier_contacts_or_receipts(self):
        p=self.page();self.advance(p,9000);before=self.snap(p);self.advance(p,650);after=self.snap(p)
        self.assertGreater(after['episode'],before['episode']);before_ids={d['id'] for sy in before['universe']['systems'].values() for d in sy['bodies']};after_ids={d['id'] for sy in after['universe']['systems'].values() for d in sy['bodies']};self.assertTrue(before_ids<=after_ids)
        self.assertEqual(before['universe']['seed'],after['universe']['seed']);self.assertGreaterEqual(after['navigation']['arrivals'],before['navigation']['arrivals']);self.assertEqual(after['frontierAudit'],[]);self.assertEqual(after['resourceAudit'],[])
        p.evaluate('window.__icarusSoak.save()');p.reload();self.assertEqual(after,self.snap(p))
    def test_fuel_shortage_rejects_departure_without_teleportation(self):
        p=self.page();self.configure(p,"s.remoteCore.autonomyEnabled=false;s.economy.feedstockUsed.fuel=s.economy.feedstockInitial.fuel;s.economy.feedstock.fuel=0;");self.open_map(p)
        target=p.locator('#frontier-target option').evaluate_all('(els)=>els.map(e=>e.value).find(x=>x!=="HOME")');p.locator('#frontier-target').select_option(target);p.locator('[data-nav="course"]').click();snap=self.snap(p)
        self.assertEqual(snap['navigation']['current'],'HOME');self.assertEqual(snap['navigation']['position'],{'x':0,'y':0});self.assertEqual(snap['resourceAudit'],[])
    def test_star_map_is_usable_on_tablet_and_does_not_advance_clock(self):
        p=self.page();p.set_viewport_size({'width':768,'height':1024});self.open_map(p);before=self.snap(p)['tick'];self.assertTrue(p.locator('#star-map').is_visible());p.locator('[data-star]').nth(1).click();self.assertEqual(self.snap(p)['tick'],before);self.assertLessEqual(p.locator('#star-map').bounding_box()['width'],768)
    def test_ship_damage_interrupts_travel_at_real_position_then_repair_can_resume(self):
        p=self.page();self.configure(p,"s.remoteCore.autonomyEnabled=false;");self.open_map(p);target=p.locator('#frontier-target option').evaluate_all('(els)=>els.map(e=>e.value).find(x=>x!=="HOME")');p.locator('#frontier-target').select_option(target);p.locator('[data-nav="course"]').click();self.advance(p,10)
        # A new isolated save edit represents an explicitly adverse damaged drive.
        p.evaluate('window.__icarusSoak.save()')
        p.add_init_script(self.codec+";"+"(()=>{if(sessionStorage.getItem('drive-damage'))return;sessionStorage.setItem('drive-damage','1');const s=JSON.parse(localStorage.getItem('icarus-v02'));s.equipment.C08.condition=0;localStorage.setItem('icarus-v02',JSON.stringify(s));})();")
        p.reload();before=self.snap(p)['navigation']['position'];self.advance(p,1);snap=self.snap(p);self.assertEqual(snap['navigation']['phase'],'drift');self.assertEqual(snap['navigation']['position'],before);self.assertEqual(snap['navigation']['arrivals'],0)
    def test_paid_meal_activity_reduces_hunger_after_supply_collection(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.navigation.hold=true;
        const p=s.crew[0];p.room='A04';p.target='A04';p.route=[];p.hunger=100;p.task='Eat a meal';p.goal='Eat a meal';p.activityKind='meal';p.interaction='working';p.carrying='food';p.taskMinutes=24;
        s.interactions.supplies.food-=1;s.economy.consumed.food=1;
        """)
        self.advance(p,10);snap=self.snap(p);self.assertLess(snap['crew'][0]['hunger'],90);self.assertEqual(snap['resourceAudit'],[])
    def test_large_compressed_voyage_remains_plain_json_to_game_and_reload(self):
        p=self.page();self.configure(p,"s.navigation.testPadding='ICARUS 🔬 archive '.repeat(100000);")
        snap=self.snap(p);self.assertTrue(p.evaluate('window.__icarusSoak.save()'));stats=p.evaluate('ICARUSSaveStore.stats()');self.assertTrue(stats['compressed']);self.assertLess(stats['primary_bytes'],300000)
        p.reload();self.assertEqual(snap,self.snap(p))
    def test_failed_mining_creates_recoverable_cache_without_crediting_ship_stock(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.minute=481;s.tick=1;s.clock.elapsed=1;s.entropy.seed=7;
        for(const p of s.crew){p.task='Standby';p.goal='Standby';p.taskMinutes=999;p.route=[];}
        const d=Object.values(s.universe.systems).flatMap(x=>x.bodies).find(d=>d.deposits.fuel>=3);d.visited=true;d.observedHazard=.8;d.deposits.fuel-=2;d.extracted.fuel=2;
        s.navigation.current=d.id;s.navigation.position={x:d.x,y:d.y};s.navigation.phase='orbit';s.frontier.enabled=false;s.frontier.lastWeatherKey=d.id+':0';
        const names=s.crew.slice(0,2).map(p=>p.name);for(const p of s.crew.slice(0,2)){p.expeditionId='F-TEST';p.expeditionAway=d.id;}
        s.frontier.active='F-TEST';s.frontier.jobs=[{id:'F-TEST',type:'extract_fuel',destination:d.id,location:d.id,resource:'fuel',requested:10,duration:180,status:'active',started:0,progress:179.9,members:names,objective:'Explicit adverse mining fixture',reason:'Known reserve deficit',evidence:[]}];
        s.remoteCore.missions.frontier={id:'F-TEST',members:names,crew:names[0],suits:2,phase:'onsite',fieldProgress:179.9,progress:0,workRate:1,cargo:{food:1,water:2,oxygen:2},extracted:{fuel:2},conditions:{},decisions:[],cohesion:0};
        s.teamLog.suits=4;s.logistics.extracted.fuel=2;s.economy.initial.food+=1;s.economy.initial.water+=2;s.economy.initial.oxygen+=2;
        """)
        self.advance(p,60);snap=self.snap(p);job=snap['frontier']['jobs'][0];self.assertEqual(job['status'],'failed');self.assertEqual(snap['logistics']['credited'].get('fuel',0),0);self.assertTrue(any(d.get('cache',{}).get('fuel',0)>0 for sys in snap['universe']['systems'].values() for d in sys['bodies']));self.assertEqual(snap['frontierAudit'],[]);self.assertEqual(snap['resourceAudit'],[])
    def test_compressed_primary_corruption_recovers_the_verified_previous_snapshot(self):
        p=self.page();self.advance(p,240);p.evaluate('window.__icarusSoak.save()');checkpoint=p.evaluate("localStorage.getItem('icarus-v02')");self.advance(p,120);p.evaluate('window.__icarusSoak.save()')
        p.add_init_script(self.codec+";(()=>{if(sessionStorage.getItem('corrupt-once'))return;sessionStorage.setItem('corrupt-once','1');Storage.prototype.__icarusOriginalSet.call(localStorage,'icarus-core-recovery-v0941',ICARUSSaveStore.encode("+json.dumps(checkpoint)+"));Storage.prototype.__icarusOriginalSet.call(localStorage,'icarus-v02','ICARUS-LZ1:broken');})();")
        p.reload();p.wait_for_function('!!window.__icarusSoak');snap=self.snap(p);self.assertEqual(snap['tick'],360);self.assertGreaterEqual(p.evaluate('ICARUSDurable.status.recoveries'),1)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report',default='frontier_integration.json');args=ap.parse_args()
    result=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(FrontierIntegration))
    Path(args.report).write_text(json.dumps({'passed':result.wasSuccessful(),'tests_run':result.testsRun,'passed_cases':result.successes,'failures':[{'test':str(t),'detail':d} for t,d in result.failures],'errors':[{'test':str(t),'detail':d} for t,d in result.errors]},indent=2));raise SystemExit(not result.wasSuccessful())
