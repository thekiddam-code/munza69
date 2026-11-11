import unittest
from bridge_service import BridgeService,BridgeError
class BridgeServiceTests(unittest.TestCase):
 def setUp(self):self.now=0;self.s=BridgeService(lambda:self.now);self.g=self.s.claim('host-instance')['generation']
 def publish(self,**extra):return self.s.publish('host-instance',self.g,{'paused':False,**extra},[])
 def test_single_owner_expiry_and_generation_fencing(self):
  with self.assertRaises(BridgeError):self.s.claim('other-instance')
  self.now=13;g=self.s.claim('other-instance')['generation'];self.assertGreater(g,self.g)
  with self.assertRaises(BridgeError):self.publish()
 def test_paused_is_connected_without_tick_movement(self):
  self.publish(paused=True,tick=100);self.assertEqual(self.s.view()['state'],'SIMULATION PAUSED');self.now=5;self.s.heartbeat('host-instance',self.g);self.assertTrue(self.s.view()['online'])
 def test_duplicate_request_cannot_execute_twice_or_change_payload(self):
  self.publish();a=self.s.enqueue('token','request-one','save');b=self.s.enqueue('token','request-one','save');self.assertEqual(a['queued'],b['queued']);self.assertTrue(b['duplicate']);self.assertEqual(len(self.s.pending('host-instance',self.g)),1)
  with self.assertRaises(BridgeError):self.s.enqueue('token','request-one','nav:hold')
 def test_delivery_retains_until_ack_and_expires(self):
  self.publish();cid=self.s.enqueue('token','request-one','save')['queued'];self.assertEqual(self.s.pending('host-instance',self.g),self.s.pending('host-instance',self.g));self.s.publish('host-instance',self.g,{},[cid]);self.assertEqual(self.s.pending('host-instance',self.g),[])
 def test_creator_controls_denied_by_default_and_offline_never_queues(self):
  self.publish()
  with self.assertRaises(BridgeError):self.s.enqueue('t','request-one','pause')
  self.publish(creator=True);self.s.enqueue('t','request-one','pause');self.now=9
  with self.assertRaises(BridgeError):self.s.enqueue('t','request-two','save')
  self.assertTrue(self.s.view()['stale']);self.assertEqual(self.s.view()['state'],'RECONNECTING')
 def test_new_host_cannot_receive_old_commands_or_old_telemetry(self):
  self.publish();self.s.enqueue('t','request-one','save');self.now=13;g=self.s.claim('next-instance')['generation'];self.assertEqual(self.s.pending('next-instance',g),[]);self.assertIsNone(self.s.view()['telemetry'])
 def test_bounds_and_snapshot_isolation(self):
  self.publish(crew=[{'name':'Frank'}]);v=self.s.view();v['telemetry']['crew'][0]['name']='changed';self.assertEqual(self.s.view()['telemetry']['crew'][0]['name'],'Frank')
  for i in range(25):self.s.enqueue('t',f'request-{i:03}','save')
  with self.assertRaises(BridgeError):self.s.enqueue('t','request-over','save')
if __name__=='__main__':unittest.main()
