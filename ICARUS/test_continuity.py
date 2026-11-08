"""Adverse and cross-boundary browser scenarios built on the common isolated harness."""
import json
import argparse
from pathlib import Path
import unittest
from test_integration import Integration
class RecordedResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.successes=[]
    def addSuccess(self,test):super().addSuccess(test);self.successes.append(str(test))
class Continuous(Integration):
    def test_transition_during_mission_research_treatment_and_emergency(self):
        p=self.page()
        self.configure(p,"""
        s.minute=10079;s.tick=9599;s.clock.elapsed=9599;s.clock.nextEpisodeAt=10080;
        s.remoteCore.autonomyEnabled=false;
        const names=[s.crew[0].name,s.crew[1].name];
        for(const p of s.crew.slice(0,2)){p.expeditionAway='asteroid';p.expeditionId='ACTIVE';p.route=[];}
        s.remoteCore.missions.asteroid={id:'ACTIVE',members:names,crew:names[0],phase:'transit',progress:40,kit:1,suits:2,cargo:{food:2,water:4,oxygen:4},launched:9590,conditions:{},decisions:[]};
        s.remoteCore.director.registry=[{id:'ACTIVE',type:'survey',location:'asteroid',crew:names[0],members:names,status:'active',reason:'Explicit adverse fixture',objective:'Active transition regression',launched:9590,baseline:{surveyed:1,findings:0}}];
        s.teamLog={suits:4,lostSuits:0,launches:1,decisions:[]};
        const analyst=s.crew[2];analyst.room='B01';analyst.route=[];analyst.energy=90;analyst.stress=0;analyst.researchAssignment='EX-ACTIVE';analyst.taskMinutes=999;
        s.specimenCustody={items:[{id:'SPEC-A',name:'synthetic boundary sample',origin:'asteroid',status:'stored',integrity:90,contamination:0,volatile:false}],history:[]};
        s.remoteCore.director.science={cases:[{id:'CASE-A',specimenId:'SPEC-A',location:'asteroid',item:'synthetic boundary sample',classification:'geological material',status:'complete',progress:100}],programs:[{id:'RES-A',group:'asteroid|geological material',location:'asteroid',subject:'geological material',caseIds:['CASE-A'],hypotheses:[],status:'running'}],experiments:[{id:'EX-ACTIVE',programId:'RES-A',caseId:'CASE-A',specimenId:'SPEC-A',method:'noninvasive_screen',cost:2,analyst:analyst.name,started:9590,duration:60,progress:10,status:'running'}],nextCase:2,lastTick:9599};
        const patient=s.crew[3];patient.room='A08';patient.route=[];patient.vitals.health=40;patient.energy=5;patient.vitals.treatmentPaid=true;patient.survivalIncapacitated=true;patient.medicalTreatment=9;patient.tissueProgress=7;patient.taskMinutes=999;
        for(const q of s.crew.filter(p=>p.job==='Medic')){q.room='A08';q.route=[];q.taskMinutes=999;}
        s.tissueRepair.cartridges=11;s.tissueRepair.activePatient=patient.name;s.economy.initial.medical=11;s.economy.initial.food+=2;s.economy.initial.water+=4;s.economy.initial.oxygen+=4;
        s.equipment.C07.condition=20;s.physicalWorld.rooms.C07.atmosphere={pressure:70,oxygen:18,temperature:90,smoke:20,fire:true,breach:false};
        """)
        self.advance(p,1);snap=self.snap(p)
        self.assertEqual(snap['tick'],9600);self.assertEqual(snap['minute'],10080);self.assertEqual(snap['episode'],2)
        self.assertEqual(snap['missions']['asteroid']['members'],['Frank Morrow','Mara Chen']);self.assertEqual(snap['missions']['asteroid']['progress'],42)
        self.assertGreaterEqual(snap['director']['science']['experiments'][0]['progress'],10)
        self.assertLess(snap['world']['equipment']['C07']['condition'],21);self.assertTrue(snap['world']['physicalWorld']['rooms']['C07']['atmosphere']['fire'])
        self.assertGreaterEqual(next(p for p in snap['crew'] if p['name']=='Derek Cole')['vitals']['health'],40)
        patient=next(q for q in snap['crew'] if q['name']=='Derek Cole');self.assertEqual(patient['medicalTreatment'],10);self.assertEqual(patient['tissueProgress'],8);self.assertTrue(any(e['status']=='active' for e in snap['world']['emergencies'].values()))
        self.assertEqual(snap['world']['tissueRepair']['cartridges'],11+(snap['economy']['produced'].get('medical',0))-(snap['economy']['consumed'].get('medical',0)));self.assertEqual(snap['resourceAudit'],[])
        self.assertTrue(p.evaluate('window.__icarusSoak.save()'));p.reload();self.assertEqual(snap,self.snap(p))
    def test_legacy_clock_migration_preserves_remaining_cooldown_and_is_idempotent(self):
        p=self.page();self.configure(p,"delete s.clock;s.episode=3;s.minute=1000;s.tick=520;s.remoteCore.director.crewReadyAt={'Frank Morrow':31360};")
        snap=self.snap(p);self.assertEqual(snap['director']['crewReadyAt']['Frank Morrow']-snap['clock']['elapsed'],120)
        self.assertTrue(p.evaluate('window.__icarusSoak.save()'));p.reload();self.assertEqual(snap,self.snap(p))
    def test_natural_samples_and_teams_have_real_field_provenance(self):
        p=self.page();self.advance(p,2200);snap=self.snap(p)
        cases=snap['director']['science']['cases'];items=(snap['specimenCustody'] or {}).get('items',[])
        natural=[i for i in items if i.get('source')];self.assertTrue(natural)
        for i in natural:self.assertIn(i['source']['missionId'],[j['id'] for j in snap['director']['registry']])
        self.assertTrue(any(len(j.get('members',[]))==2 for j in snap['director']['registry']))
        self.assertEqual(snap['resourceAudit'],[])
    def test_interrupted_research_releases_analyst_without_duplicate_payment(self):
        p=self.page();active=None
        for _ in range(24):
            self.advance(p,120);active=next((e for e in self.snap(p)['director']['science'].get('experiments',[]) if e['status']=='running'),None)
            if active:break
        self.assertIsNotNone(active);identifier=active['id'];cost=active['cost']
        self.configure(p,"const e=s.remoteCore.director.science.experiments.find(e=>e.id==="+json.dumps(identifier)+");const person=s.crew.find(p=>p.name===e.analyst);person.vitals.health=35;person.room='A08';person.route=[];person.taskMinutes=999;")
        self.advance(p,300);snap=self.snap(p);e=next(e for e in snap['director']['science']['experiments'] if e['id']==identifier)
        self.assertEqual(e['cost'],cost);self.assertTrue(e.get('interruptions'));self.assertEqual(snap['resourceAudit'],[])
        ids=[e['id'] for e in snap['director']['science']['experiments']];self.assertEqual(len(ids),len(set(ids)))
    def test_team_loss_records_failed_mission_and_disposes_cargo_without_duplication(self):
        p=self.page();self.configure(p,"""
        const names=s.crew.slice(0,2).map(p=>p.name);
        for(const p of s.crew.slice(0,2)){p.vitals.health=0;p.expeditionAway='asteroid';}
        s.remoteCore.autonomyEnabled=false;s.remoteCore.missions.asteroid={id:'LOSS',members:names,crew:names[0],phase:'onsite',progress:100,cargo:{food:1,water:2,oxygen:2},suits:2,launched:0};
        s.remoteCore.director.registry=[{id:'LOSS',location:'asteroid',status:'active',crew:names[0],members:names,reason:'Explicit casualty fixture',objective:'Adverse loss test'}];
        s.teamLog={suits:4,lostSuits:0,launches:1,decisions:[]};s.economy.initial.food+=1;s.economy.initial.water+=2;s.economy.initial.oxygen+=2;
        """)
        self.advance(p,1);snap=self.snap(p);self.assertEqual(snap['director']['registry'][0]['status'],'failed');self.assertIsNone(snap['missions']['asteroid']);self.assertEqual(len(snap['crew']),18);self.assertEqual(snap['teamLog']['lostSuits'],2);self.assertEqual(snap['resourceAudit'],[])
    def test_captain_can_cancel_staging_without_teleporting_or_duplicating_supplies(self):
        p=self.page();self.advance(p,1);snap=self.snap(p);loc,m=next((loc,m) for loc,m in snap['missions'].items() if m)
        self.assertEqual(m['phase'],'boarding');positions={q['name']:q['room'] for q in snap['crew']}
        p.locator('#icarus-menu button[data-page="operations"]').click();p.locator('[data-location="'+loc+'"]').click();p.locator('[data-remote-tab="Expedition"]').click()
        p.locator('[data-remote-action="missionrecall:'+m['id']+'"]').click();after=self.snap(p)
        self.assertIsNone(after['missions'][loc]);self.assertEqual(after['resourceAudit'],[]);self.assertEqual(after['teamLog']['suits'],6)
        for q in after['crew']:self.assertEqual(q['room'],positions[q['name']])
    def test_containment_incident_produces_actual_injury_and_recorded_failed_measurement(self):
        p=self.page();self.configure(p,"""
        s.minute=481;s.tick=1;s.clock.elapsed=1;s.entropy.seed=7;s.remoteCore.autonomyEnabled=false;s.lazarus={condition:94,containment:85,biomass:8,powerDraw:14,protocol:'conservative',subjects:[],nextId:1,active:null,history:[],quarantine:[],discoveries:0,entities:[],nextEntityId:1};
        for(const p of s.crew){p.task='Standby';p.goal='Standby';p.route=[];p.taskMinutes=999;}
        const analyst=s.crew[2];analyst.room='B05';analyst.researchAssignment='EX-RISK';analyst.energy=90;analyst.stress=0;
        s.specimenCustody={items:[{id:'RISK',name:'synthetic contained sample',origin:'derelict',status:'quarantined',biological:true,volatile:true,integrity:100,contamination:0,location:'B04'}],history:[]};
        s.remoteCore.director.science={cases:[{id:'CASE-RISK',specimenId:'RISK',location:'derelict',item:'synthetic contained sample',classification:'biological specimen',status:'complete',progress:100}],programs:[{id:'RES-RISK',group:'derelict|biological specimen',location:'derelict',subject:'biological specimen',caseIds:['CASE-RISK'],hypotheses:[],status:'running'}],experiments:[{id:'EX-RISK',programId:'RES-RISK',caseId:'CASE-RISK',specimenId:'RISK',method:'custody_review',cost:1,analyst:analyst.name,started:0,duration:30,progress:29,status:'running'}],nextCase:2,lastTick:1};
        """)
        self.advance(p,1);snap=self.snap(p);e=snap['director']['science']['experiments'][0]
        self.assertTrue(e.get('containmentIncident'),e);self.assertEqual(next(q for q in snap['crew'] if q['name']=='Dr. Voss')['vitals']['health'],92);self.assertEqual(snap['specimenCustody']['items'][0]['contamination'],5)
        self.assertTrue(any('Containment exposure' in e['message'] for e in snap['events']));self.assertEqual(snap['resourceAudit'],[])
    def test_resource_failure_injures_real_crew_and_suspends_optional_operations(self):
        p=self.page();self.configure(p,"""
        s.minute=509;s.tick=29;s.clock.elapsed=29;s.remoteCore.autonomyEnabled=false;
        s.economy.stock.oxygen=0;s.economy.initial.oxygen=0;s.economy.feedstock.co2=0;s.equipment.C09.condition=0;
        """)
        self.advance(p,1);snap=self.snap(p);self.assertEqual(snap['economy']['mode'],'survival');self.assertFalse(snap['economy']['allowResearch']);self.assertFalse(snap['economy']['allowLaunch']);self.assertTrue(all(q['vitals']['health']<100 for q in snap['crew']));self.assertEqual(snap['resourceAudit'],[])
    def test_explicit_new_voyage_initializes_new_systems_and_saves_without_stock_duplication(self):
        p=self.page();self.advance(p,240);p.on('dialog',lambda d:d.accept());p.locator('#reset').click();snap=self.snap(p)
        self.assertEqual(snap['tick'],0);self.assertEqual(snap['clock']['elapsed'],0);self.assertEqual(len(snap['crew']),20);self.assertEqual(snap['resourceAudit'],[]);self.assertEqual(snap['teamLog']['suits'],6)
        self.assertTrue(p.evaluate('window.__icarusSoak.save()'));p.reload();self.assertEqual(snap,self.snap(p))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--report',default='continuity_report.json');args=parser.parse_args()
    result=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(Continuous))
    Path(args.report).write_text(json.dumps({'passed':result.wasSuccessful(),'tests_run':result.testsRun,'passed_cases':result.successes,'failures':[{'test':str(t),'detail':d} for t,d in result.failures],'errors':[{'test':str(t),'detail':d} for t,d in result.errors]},indent=2))
    raise SystemExit(not result.wasSuccessful())
