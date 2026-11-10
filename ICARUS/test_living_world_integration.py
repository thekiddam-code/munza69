"""Phase 2 explicit adverse fixtures plus inherited clock/crew/save regression coverage."""
import argparse,json,unittest
from pathlib import Path
from test_knowledge_integration import KnowledgeIntegration
from test_continuity import RecordedResult
class LivingWorldIntegration(KnowledgeIntegration):
    def test_sealed_chamber_cannot_attack_actual_field_crew(self):
        p=self.page();self.field(p);self.advance(p,5);s=self.snap(p);o=s['unifiedWorld']['organisms']['XENO-INITIAL'];self.assertEqual(o['location'],'asteroid:23');self.assertEqual(o['behavior']['state'],'contained');self.assertFalse(any(e['data'].get('organismId')=='XENO-INITIAL' and e['kind']=='encounter' for e in s['chronicle']['records']))
    def test_local_creature_attack_has_private_source_and_causal_injury(self):
        p=self.page();self.field(p);self.change(p,"""s.tick=4;s.clock.elapsed=4;const q=s.crew[0];q.fieldPosition=23;const o=s.unifiedWorld.organisms['XENO-INITIAL'];o.sealed=false;o.dormant=false;s.unifiedWorld.military.doors[23]='open';s.entropy.seed=9; /* fixed seed whose first local attack draw is below .35 */""");self.advance(p,1);s=self.snap(p);hits=[e for e in s['chronicle']['records'] if e['kind']=='encounter' and e['data'].get('organismId')=='XENO-INITIAL'];self.assertEqual(len(hits),1);self.assertTrue(hits[0]['data']['privateKnowledge']);self.assertTrue(any(e['data'].get('encounterSourceId')==hits[0]['id'] for e in s['chronicle']['records']));self.assertFalse(any(f['id'] in s['knowledge']['actors']['SOL']['entries'] for f in s['knowledge']['facts'].values() if f['data'].get('organismId')=='XENO-INITIAL'));self.assertLess(s['crew'][0]['vitals']['health'],100)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--report',default='living_world_integration.json');args=ap.parse_args();r=unittest.TextTestRunner(verbosity=2,resultclass=RecordedResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(LivingWorldIntegration));Path(args.report).write_text(json.dumps({'passed':r.wasSuccessful(),'tests_run':r.testsRun,'passed_cases':r.successes,'failures':[{'test':str(t),'detail':d} for t,d in r.failures],'errors':[{'test':str(t),'detail':d} for t,d in r.errors]},indent=2));raise SystemExit(not r.wasSuccessful())
