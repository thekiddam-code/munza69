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
    def test_preventive_repair_is_paid_and_survives_an_interrupted_worker(self):
        p=self.page();self.configure(p,"""
        s.remoteCore.autonomyEnabled=false;s.frontier.enabled=false;s.navigation.hold=true;s.anthology.config.frequency=0;s.equipment.C07.condition=60;
        """);self.advance(p,600);s=self.snap(p);self.assertGreater(s['repairControl']['stats'].get('preventiveCompleted',0),0);self.assertTrue(any(r['source']=='maintenance repair C07' for r in s['economy']['ledger'].values()));self.assertEqual(s['resourceAudit'],[])
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report',default='stability_integration.json');args=ap.parse_args();r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(StabilityIntegration));Path(args.report).write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
