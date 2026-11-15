import unittest,json,base64
from record_service import RecordService
from bridge_service import BridgeError
class RecordTests(unittest.TestCase):
 def test_chunks_are_bounded_ordered_and_scoped_to_host_generation(self):
  s=RecordService();self.assertFalse(s.request('DRONE-1-RECORD-1',1)['ready']);j=s.pending(1)[0];raw=base64.b64encode(json.dumps({'id':j['id'],'frames':[{'tick':1}]}).encode()).decode();s.chunk(1,{**j,'index':1,'total':2,'chunk':raw[12:]});s.chunk(1,{**j,'index':0,'total':2,'chunk':raw[:12]});self.assertTrue(s.request(j['id'],1)['ready']);self.assertFalse(s.request(j['id'],2)['ready'])
 def test_unknown_tokens_oversized_chunks_and_identity_spoof_are_rejected(self):
  s=RecordService();s.request('A',1);j=s.pending(1)[0]
  for data in [{**j,'token':'other'},{**j,'index':0,'total':1,'chunk':'A'*48001},{**j,'index':0,'total':1,'chunk':base64.b64encode(b'{"id":"B","frames":[]}').decode()}]:
   with self.assertRaises(BridgeError):s.chunk(1,data)
 def test_queue_and_lifetime_are_bounded(self):
  now=[0];s=RecordService(lambda:now[0])
  for i in range(4):s.request(str(i),1)
  with self.assertRaises(BridgeError):s.request('extra',1)
  now[0]=61;self.assertFalse(s.request('extra',1)['ready']);self.assertEqual(len(s.jobs),1)
if __name__=='__main__':unittest.main()
