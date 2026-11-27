"""Actual companion Handler/authentication; isolated files and explicitly fake GG/input."""
import importlib.util,json,os,sys,tempfile,threading,time,types,unittest,urllib.request,urllib.error,uuid
from pathlib import Path
from test_host_actions import FakeSonar,FakeSender
from umbra_host_actions import HostActions
HERE=Path(__file__).resolve().parent
REFERENCE=Path(os.environ.get('ICARUS_PHASE49_REFERENCE','/workspace/icarus-bulk-reference'))/'ICARUS'
class HttpTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();cls.root=Path(cls.tmp.name)
  cls.source=cls.root/'server.py';cls.source.write_bytes((HERE/'payload/server.py').read_bytes())
  sys.path.insert(0,str(REFERENCE));sys.path.insert(0,str(HERE/'payload'))
  sys.modules['pyautogui']=types.SimpleNamespace(**{n:lambda *a,**k:None for n in ['press','hotkey','keyUp','mouseUp','mouseDown','keyDown','write']})
  spec=importlib.util.spec_from_file_location('umbra_actions_http_fixture',cls.source);cls.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.m)
  cls.m.TOKENS={cls.m.token_hash('paired-fixture')}
  cls.server=cls.m.http.server.ThreadingHTTPServer(('127.0.0.1',0),cls.m.Handler);threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url=f'http://127.0.0.1:{cls.server.server_port}'
 @classmethod
 def tearDownClass(cls):
  cls.server.shutdown();cls.server.server_close();cls.m.TV_SERVICE.close();cls.m.WINDOWS_MONITOR.stop_event.set();cls.tmp.cleanup()
 def setUp(self):
  (self.root/'umbra_host_actions.json').unlink(missing_ok=True)
  self.sonar=FakeSonar(True);self.sender=FakeSender()
  self.m.HOST_ACTIONS=HostActions(self.root,self.m.cfg,self.m.LOCK,self.sonar,self.sender,clip_timeout=.08,poll_interval=.01)
 def req(self,path,data=None,token='paired-fixture',origin=None):
  headers={'Content-Type':'application/json'}
  if token:headers['Authorization']='Bearer '+token
  if origin:headers['Origin']=origin
  req=urllib.request.Request(self.url+path,data=json.dumps(data or {'requestId':str(uuid.uuid4())}).encode(),headers=headers)
  try:
   with urllib.request.urlopen(req,timeout=3) as r:return r.status,json.load(r)
  except urllib.error.HTTPError as e:return e.code,json.load(e)
 def test_auth_origin_and_exact_field_guards_precede_any_device_action(self):
  self.assertEqual(401,self.req('/api/sonar/arctis',token=None)[0]);self.assertEqual(403,self.req('/api/sonar/arctis',origin='http://unrelated.invalid')[0]);self.assertEqual(400,self.req('/api/sonar/arctis',{'requestId':str(uuid.uuid4()),'microphone':'x'})[0]);self.assertEqual([],self.sonar.calls)
 def test_actual_paired_route_endpoint_returns_choices_then_four_route_readback(self):
  code,data=self.req('/api/sonar/arctis');self.assertEqual(200,code);self.assertEqual('selection_required',data['state']);self.assertEqual([],self.sonar.calls)
  code,data=self.req('/api/sonar/arctis',{'requestId':str(uuid.uuid4()),'output_id':'arctis-b'});self.assertEqual(200,code);self.assertTrue(data['verified']);self.assertEqual({k:'arctis-b' for k in ('game','chat','media','aux')},data['routes']);self.assertTrue(data['microphone_preserved'])
 def test_clip_endpoint_reads_saved_macro_and_returns_unverified_without_a_new_clip(self):
  config=self.m.cfg();config['macros']['Save Clip']=['ctrl','f8'];self.m.CONFIG.write_text(json.dumps(config))
  folder=self.root/'moments';folder.mkdir(exist_ok=True);self.m.HOST_ACTIONS.file.write_text(json.dumps({'moments_clip_directory':str(folder)}))
  request={'requestId':str(uuid.uuid4())};code,data=self.req('/api/moments/save-clip',request);self.assertEqual(200,code);self.assertEqual('pending',data['state']);self.assertEqual([['ctrl','f8']],self.sender.calls)
  time.sleep(.12);code,data=self.req('/api/moments/clip-status',request);self.assertEqual('unverified',data['state']);self.assertFalse(data['clip_file_verified']);self.assertEqual(1,len(self.sender.calls))
  self.assertEqual(401,self.req('/api/moments/clip-status',request,token=None)[0])
if __name__=='__main__':unittest.main(verbosity=2)
