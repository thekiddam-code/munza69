"""Physical native repair regressions plus the default-core anthology preservation suite."""
import argparse,json,unittest
from pathlib import Path
from test_anthology_integration import CoreIntegration
from test_continuity import RecordedResult
class StabilityIntegration(CoreIntegration):
    def test_read_only_failure_diagnostics_do_not_change_world_or_random_state(self):
        p=self.page();self.advance(p,600);before=self.snap(p);p.evaluate('__icarusSoak.stability()');p.evaluate('__icarusSoak.stability()');self.assertEqual(self.snap(p),before)
    def test_native_jammed_galley_is_repaired_from_corridor_with_finite_supplies(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.navigation.hold=true;s.anthology.config.frequency=0;
        s.equipment.A04.condition=30;s.physicalWorld.rooms.A04.door='jammed';s.localSystems.galley=20;
        for(const p of s.crew){p.task='Standby';p.goal='Standby';p.taskMinutes=999;p.route=[];p.interaction=null;p.maintenanceRoom=null;p.emergencyId=null;}
        """);self.advance(p,300);s=self.snap(p);self.assertEqual(s['world']['physicalWorld']['rooms']['A04']['door'],'open');self.assertEqual(s['world']['emergencies']['A04']['status'],'resolved');self.assertGreaterEqual(s['repairControl']['stats']['hatchesCleared'],1);self.assertEqual(s['resourceAudit'],[]);self.assertTrue(any('hatch repair A04'==r['source'] for r in s['economy']['ledger'].values()));self.assertLessEqual(sum(q.get('emergencyId')=='A04' for q in s['crew']),1)
    def test_unrecoverable_zero_materials_cannot_repair_or_create_resources(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.navigation.hold=true;s.anthology.config.frequency=0;s.economy.feedstock.ore=0;s.economy.feedstockUsed.ore=s.economy.feedstockInitial.ore;
        for(const key of ['tools','spares']){const amount=(s.operations.reserve[key]||0)+(s.interactions.supplies[key]||0);s.economy.consumed[key]=(s.economy.consumed[key]||0)+amount;s.operations.reserve[key]=0;s.interactions.supplies[key]=0;}
        s.equipment.C07.condition=0;s.physicalWorld.rooms.C07.door='jammed';for(const p of s.crew){p.task='Standby';p.goal='Standby';p.taskMinutes=999;p.route=[];p.interaction=null;}
        """);self.advance(p,300);s=self.snap(p);self.assertEqual(s['world']['physicalWorld']['rooms']['C07']['door'],'jammed');self.assertEqual(s['world']['equipment']['C07']['condition'],0);self.assertEqual(s['repairControl']['stats'].get('hatchesCleared',0),0);self.assertEqual(s['resourceAudit'],[])
    def test_emergency_crew_queue_yields_to_rest_and_stale_maintenance_reopens(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.navigation.hold=true;s.anthology.config.frequency=0;
        const p=s.crew[0];p.room='A04';p.target='A04';p.route=[];p.energy=10;p.vitals.fatigue=90;p.interaction='waiting-station';p.task='Waiting for workstation';p.goal='Eat a meal';p.taskMinutes=999;p.maintenanceRoom='C07';s.maintenance=s.maintenance||{orders:{},history:[],lastScan:0};s.maintenance.orders.C07={room:'C07',name:'Power distribution panel',assigned:p.name,status:'assigned',progress:20,sparePaid:true};
        """);self.advance(p,10);s=self.snap(p);person=s['crew'][0];self.assertIsNone(person.get('maintenanceRoom'));self.assertNotEqual(person.get('interaction'),'waiting-station');self.assertLess(person['vitals']['fatigue'],90);self.assertEqual(s['resourceAudit'],[])
    def test_save_reload_mid_hatch_work_preserves_paid_progress_and_next_outcome(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.navigation.hold=true;s.anthology.config.frequency=0;s.equipment.A04.condition=30;s.physicalWorld.rooms.A04.door='jammed';
        for(const p of s.crew){p.task='Standby';p.goal='Standby';p.taskMinutes=999;p.route=[];p.interaction=null;}
        """);found=False
        for _ in range(24):
            self.advance(p,5);s=self.snap(p);e=s['world']['emergencies'].get('A04',{})
            if 0<e.get('hatchProgress',0)<100:found=True;break
        self.assertTrue(found);before=self.snap(p);p.evaluate('__icarusSoak.save()');p.reload();self.assertEqual(self.snap(p),before);self.advance(p,200);after=self.snap(p);self.assertEqual(after['world']['emergencies']['A04']['status'],'resolved');self.assertEqual(after['resourceAudit'],[])
    def test_completed_machine_work_does_not_hide_a_still_jammed_hatch(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.navigation.hold=true;s.anthology.config.frequency=0;
        const p=s.crew[0];p.room='A04';p.target='A04';p.route=[];p.emergencyId='A04';p.energy=80;p.vitals.fatigue=0;p.vitals.morale=80;
        s.equipment.A04.condition=84;s.physicalWorld.rooms.A04.door='jammed';s.emergencies.A04={id:'A04',room:'A04',status:'active',label:'Explicit post-repair jam fixture',progress:100,age:5,severity:'warning',frames:[],hatchProgress:0};
        """);self.advance(p,15);s=self.snap(p);self.assertEqual(s['world']['emergencies']['A04']['status'],'active');self.assertEqual(s['world']['physicalWorld']['rooms']['A04']['door'],'jammed');self.advance(p,40);s=self.snap(p);self.assertEqual(s['world']['physicalWorld']['rooms']['A04']['door'],'open');self.assertEqual(s['world']['emergencies']['A04']['status'],'resolved');self.assertEqual(s['resourceAudit'],[])
    def test_queued_preventive_worker_acquires_parts_before_admitted_work(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.navigation.hold=true;s.anthology.config.frequency=0;
        for(const q of s.crew){q.task='Standby';q.goal='Standby';q.taskMinutes=999;q.route=[];q.interaction=null;}
        const q=s.crew[0];q.room='A04';q.target='A04';q.energy=80;q.goal='Repairing Galley unit';q.task='Waiting for workstation';q.interaction='waiting-station';q.maintenanceRoom='A04';q.carrying=null;s.equipment.A04.condition=60;s.maintenance={orders:{A04:{room:'A04',name:'Galley unit',assigned:q.name,status:'assigned',progress:0}},history:[],lastScan:0};
        """);self.advance(p,1);q=self.snap(p)['crew'][0];self.assertEqual(q.get('neededSupply'),'spares');self.assertEqual(q['interaction'],'collecting')
    def test_returning_paid_repair_worker_waits_for_real_station_capacity(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.navigation.hold=true;s.anthology.config.frequency=0;
        for(const q of s.crew){q.task='Standby';q.goal='Standby';q.taskMinutes=999;q.route=[];q.interaction=null;}
        for(const q of s.crew.slice(1,4)){q.room='A04';q.target='A04';q.activityKind='meal';q.goal='Eat a meal';q.task=q.goal;q.interaction='working';q.carrying='food';}s.interactions.supplies.food-=3;s.economy.consumed.food=3;
        const q=s.crew[0];q.room='A04';q.target='A04';q.workRoom='A04';q.energy=80;q.goal='Repairing Galley unit';q.task='Returning with spares';q.interaction='returning';q.carrying='spares';q.maintenanceRoom='A04';s.interactions.supplies.spares--;s.economy.consumed.spares=1;s.equipment.A04.condition=60;s.maintenance={orders:{A04:{room:'A04',name:'Galley unit',assigned:q.name,status:'assigned',progress:0,sparePaid:true}},history:[],lastScan:0};
        """);self.advance(p,1);q=self.snap(p)['crew'][0];self.assertEqual(q['interaction'],'waiting-station');self.assertEqual(q['carrying'],'spares');self.assertEqual(self.snap(p)['resourceAudit'],[])
    def test_actual_paid_social_meal_satisfies_the_recovery_goal(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.navigation.hold=true;s.anthology.config.frequency=0;
        const q=s.crew[1];q.room='A04';q.target='A04';q.route=[];q.task='Recover social needs';q.goal=q.task;q.taskMinutes=30;q.interaction='working';q.activityKind='meal';q.carrying='food';q.social=5;q.energy=80;s.interactions.supplies.food--;s.economy.consumed.food=1;
        """);self.advance(p,5);self.assertGreater(self.snap(p)['crew'][1]['social'],5);self.assertEqual(self.snap(p)['resourceAudit'],[])
    def test_queued_routine_equipment_work_cannot_bypass_empty_tools(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.navigation.hold=true;s.anthology.config.frequency=0;
        for(const q of s.crew){q.task='Standby';q.goal='Standby';q.taskMinutes=999;q.route=[];q.interaction=null;}
        const q=s.crew[0];q.room='A04';q.target='A04';q.route=[];q.energy=80;q.goal='Maintaining galley equipment';q.task='Waiting for workstation';q.interaction='waiting-station';q.carrying=null;q.maintenanceRoom=null;s.equipment.A04.condition=60;
        const tools=s.operations.reserve.tools+s.interactions.supplies.tools;s.operations.reserve.tools=0;s.interactions.supplies.tools=0;s.economy.consumed.tools=tools;s.economy.feedstock.ore=0;s.economy.feedstockUsed.ore=s.economy.feedstockInitial.ore;
        """);self.advance(p,10);s=self.snap(p);self.assertLessEqual(s['world']['equipment']['A04']['condition'],60);self.assertEqual(s['crew'][0]['interaction'],'waiting-supply');self.assertEqual(s['resourceAudit'],[])
    def test_preventive_repair_is_paid_and_survives_an_interrupted_worker(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.navigation.hold=true;s.anthology.config.frequency=0;s.equipment.C07.condition=60;
        """);self.advance(p,600);s=self.snap(p);self.assertGreater(s['repairControl']['stats'].get('preventiveCompleted',0),0);self.assertTrue(any(r['source']=='maintenance repair C07' for r in s['economy']['ledger'].values()));self.assertEqual(s['resourceAudit'],[])
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report',default='stability_integration.json');args=ap.parse_args();r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(StabilityIntegration));Path(args.report).write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
