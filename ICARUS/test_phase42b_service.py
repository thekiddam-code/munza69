import unittest
from bridge_service import BridgeService,BridgeError
class ClassifiedService(unittest.TestCase):
 def test_classified_payload_is_separate_and_returned_copies_cannot_mutate_authority(self):
  b=BridgeService();g=b.claim('host-instance')['generation'];b.publish('host-instance',g,{'tick':1},[],classified={'tick':1,'rooms':[{'id':'COV-A05'}]});self.assertNotIn('classified',b.view()['telemetry']);view=b.classified_view();view['telemetry']['rooms'].clear();self.assertEqual(len(b.classified_view()['telemetry']['rooms']),1)
 def test_replacement_host_clears_private_payload_and_stale_is_marked(self):
  now=[0];b=BridgeService(clock=lambda:now[0]);g=b.claim('host-instance')['generation'];b.publish('host-instance',g,{'tick':1},[],classified={'tick':1});now[0]=10;self.assertFalse(b.classified_view()['online']);now[0]=13;b.claim('new-instance');self.assertIsNone(b.classified_view()['telemetry'])
 def test_classified_public_routing_and_oversized_payloads_are_rejected(self):
  b=BridgeService();g=b.claim('host-instance')['generation']
  with self.assertRaises(BridgeError):b.publish('host-instance',g,{'classified':{}},[])
  with self.assertRaises(BridgeError):b.publish('host-instance',g,{},[],classified={'blob':'x'*25000})
