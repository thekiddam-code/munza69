"""Fixture routes/files/input only. Does not certify Windows, GG or actual clips."""
import json,tempfile,threading,time,unittest,uuid,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'payload'))
from umbra_host_actions import *
class FakeSonar:
 def __init__(self,multiple=False):
  self.state={k:'old-'+k for k in OUTPUTS+('mic',)};self.original=dict(self.state);self.calls=[];self.fail=None;self.noop=False
  self.devices=[{'id':'arctis-a','friendlyName':'Arctis A','role':'none','dataFlow':'render'}]+([{'id':'arctis-b','friendlyName':'Arctis B','role':'none','dataFlow':'render'}] if multiple else [])
 def discover(self):return 'http://127.0.0.1:1','/classicRedirections',dict(self.state),self.devices
 def read_routes(self,*args):return dict(self.state)
 def set_route(self,base,prefix,c,device):
  self.calls.append((c,device))
  if c==self.fail and device.startswith('arctis'):self.state[c]=device;raise HostActionError('Transport failed after applying route.',503)
  if not self.noop:self.state[c]=device
class FakeSender:
 def __init__(self):self.calls=[]
 def send(self,keys):self.calls.append(list(keys))
class HostTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.folder=self.root/'clips';self.folder.mkdir();self.config={'macros':{'Save Clip':['alt','s'],'Copy':['ctrl','c']},'untouched':True}
  self.sonar=FakeSonar();self.sender=FakeSender();self.service=HostActions(self.root,lambda:self.config,threading.RLock(),self.sonar,self.sender,clip_timeout=.18,poll_interval=.02)
  atomic_json(self.service.file,{'moments_clip_directory':str(self.folder),'other_setting':'preserve'})
 def tearDown(self):
  deadline=time.monotonic()+2
  while self.service.clip_active and time.monotonic()<deadline:time.sleep(.01)
  self.tmp.cleanup()
 def call(self,path='sonar/arctis',data=None,owner='paired-owner'):
  return self.service.post('/api/'+path,data or {'requestId':str(uuid.uuid4())},owner)
 def test_four_routes_readback_mic_preserved_remembered_and_idempotent(self):
  request={'requestId':str(uuid.uuid4())};result=self.call(data=request)
  self.assertTrue(result['verified']);self.assertEqual({k:'arctis-a' for k in OUTPUTS},result['routes']);self.assertEqual('old-mic',self.sonar.state['mic'])
  self.assertEqual([(k,'arctis-a') for k in OUTPUTS],self.sonar.calls);self.assertEqual('preserve',self.service.settings()['other_setting'])
  self.assertEqual(result,self.call(data=request));self.assertEqual(4,len(self.sonar.calls));self.assertEqual(['alt','s'],self.config['macros']['Save Clip'])
  restarted=HostActions(self.root,lambda:self.config,threading.RLock(),FakeSonar(True),self.sender)
  result=restarted.post('/api/sonar/arctis',{'requestId':str(uuid.uuid4())},'paired-owner');self.assertEqual('arctis-a',result['output']['id'])
 def test_multiple_outputs_require_choice_without_writes_and_selected_identity_is_retained(self):
  self.service.sonar=FakeSonar(True)
  result=self.call();self.assertEqual('selection_required',result['state']);self.assertEqual([],self.service.sonar.calls)
  result=self.call(data={'requestId':str(uuid.uuid4()),'output_id':'arctis-b'});self.assertTrue(result['verified']);self.assertEqual('arctis-b',self.service.settings()['arctis_output']['id'])
 def test_input_virtual_and_voicemeeter_candidates_are_never_selected(self):
  rows=[{'id':'mic','friendlyName':'Arctis Microphone','role':'none','dataFlow':'capture'},{'id':'virtual','friendlyName':'Arctis Sonar','role':'game','dataFlow':'render'},{'id':'vm','friendlyName':'Arctis VoiceMeeter','role':'none','dataFlow':'render'}]
  self.assertEqual([],candidates(rows));self.service.sonar.devices=rows
  result=self.call();self.assertEqual('error',result['state']);self.assertEqual([],self.sonar.calls)
 def test_partial_transport_failure_is_not_success_and_rolls_back_attempted_outputs(self):
  self.sonar.fail='media';result=self.call();self.assertFalse(result['verified']);self.assertEqual('error',result['state']);self.assertEqual(self.sonar.original,self.sonar.state)
  self.assertFalse(any(c=='mic' for c,_ in self.sonar.calls))
 def test_acknowledged_noop_does_not_claim_verified_switch(self):
  self.sonar.noop=True;result=self.call();self.assertEqual('error',result['state']);self.assertFalse(result['verified'])
 def test_arbitrary_fields_and_reused_command_identity_are_rejected(self):
  with self.assertRaises(HostActionError):self.call(data={'requestId':str(uuid.uuid4()),'channel':'mic'})
  data={'requestId':str(uuid.uuid4())};self.call(data=data)
  with self.assertRaises(HostActionError):self.call('moments/save-clip',data)
  with self.assertRaises(HostActionError):self.call(data={'requestId':'not-uuid'})
 def test_clip_uses_fresh_saved_binding_and_sent_is_not_saved(self):
  data={'requestId':str(uuid.uuid4())};result=self.call('moments/save-clip',data);self.assertEqual('pending',result['state']);self.assertFalse(result['clip_file_verified']);self.assertIsNone(result['capture_active'])
  self.assertEqual([['alt','s']],self.sender.calls);self.call('moments/save-clip',data);self.assertEqual(1,len(self.sender.calls))
  time.sleep(.25);result=self.call('moments/clip-status',data);self.assertEqual('unverified',result['state']);self.assertFalse(result['clip_file_verified'])
  self.config['macros']['Save Clip']=['ctrl','f8'];self.call('moments/save-clip');self.assertEqual(['ctrl','f8'],self.sender.calls[-1])
 def test_new_stable_video_file_is_observed_but_existing_growing_file_is_not(self):
  (self.folder/'old.mp4').write_bytes(b'\x00\x00\x00\x20ftypisom'+b'0'*64)
  data={'requestId':str(uuid.uuid4())};self.call('moments/save-clip',data)
  (self.folder/'old.mp4').write_bytes(b'\x00\x00\x00\x20ftypisom'+b'1'*200)
  (self.folder/'new.mp4').write_bytes(b'\x00\x00\x00\x20ftypisom'+b'2'*100)
  time.sleep(.12);result=self.call('moments/clip-status',data)
  self.assertEqual('clip_detected',result['state']);self.assertTrue(result['clip_file_verified']);self.assertEqual('new.mp4',result['clip']['name']);self.assertIsNone(result['capture_active'])
  with self.assertRaises(HostActionError):self.call('moments/clip-status',data,owner='another-phone')
 def test_invalid_or_missing_storage_and_macro_never_send(self):
  self.config['macros'].pop('Save Clip')
  with self.assertRaises(HostActionError):self.call('moments/save-clip')
  self.config['macros']['Save Clip']=['alt','s'];atomic_json(self.service.file,{})
  with self.assertRaises(HostActionError):self.call('moments/save-clip')
  self.assertEqual([],self.sender.calls)
 def test_overlapping_new_request_does_not_send_again(self):
  self.call('moments/save-clip')
  with self.assertRaises(HostActionError) as error:self.call('moments/save-clip')
  self.assertEqual(429,error.exception.status);self.assertEqual(1,len(self.sender.calls))
 def test_local_discovery_rejects_remote_addresses_credentials_redirect_targets_and_paths(self):
  for url in ['http://10.0.0.132:123','http://127.0.0.1:123/private','https://user:pass@localhost:123','http://localhost:123/?q=1','http://localhost\n:123']:
   with self.assertRaises(HostActionError):loopback_url(url)
  self.assertEqual('https://127.0.0.1:123',loopback_url('localhost:123',scheme='https'))
  with self.assertRaises(HostActionError):LocalSonar.routes([{'id':'game','deviceId':'x'}])
if __name__=='__main__':unittest.main(verbosity=2)
