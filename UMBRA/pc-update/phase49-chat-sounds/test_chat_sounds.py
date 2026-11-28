import importlib.util,json,os,sys,tempfile,threading,types,unittest,urllib.request,urllib.error,uuid
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'payload'))
from umbra_chat_sounds import ChatSounds
import apply_chat_sounds as installer
class FakeSounds:
 def __init__(self,events):self.events=events;self.fail=False
 def post(self,operation,data,owner):
  self.events.append(('sound',operation,data['id'],owner))
  if self.fail:raise ValueError('Removed sound / missing output')
  return {'state':'playing','id':data['id']}
class SequenceTests(unittest.TestCase):
 def setUp(self):
  self.events=[];self.sounds=FakeSounds(self.events);self.runner=ChatSounds(self.action,self.sounds,threading.RLock())
 def action(self,d):self.events.extend(['type','enter']);return 'Text input finished'
 def data(self):return {'action':'text','text':'Nice shot!','channel':'team','speed':'safe','sound_id':'a'*32,'requestId':str(uuid.uuid4())}
 def test_sound_follows_enter_and_same_request_does_not_replay(self):
  d=self.data();r=self.runner.run('paired',d);self.assertTrue(r['sound_started']);self.assertEqual(['type','enter'],self.events[:2]);self.assertEqual('sound',self.events[2][0]);self.assertEqual(r,self.runner.run('paired',d));self.assertEqual(3,len(self.events))
 def test_failed_input_never_plays_or_retries(self):
  def fail(d):self.events.append('partial input');raise RuntimeError('Failsafe')
  self.runner.action=fail;d=self.data();r=self.runner.run('paired',d);self.assertFalse(r['chat_input_completed']);self.assertFalse(r['sound_started']);self.runner.run('paired',d);self.assertEqual(['partial input'],self.events)
 def test_missing_sound_preserves_successful_chat_and_does_not_resend(self):
  self.sounds.fail=True;d=self.data();r=self.runner.run('paired',d);self.assertTrue(r['chat_input_completed']);self.assertFalse(r['sound_started']);self.assertIn('not resent',r['message']);self.runner.run('paired',d);self.assertEqual(3,len(self.events))
 def test_reused_uuid_with_changed_sound_is_rejected(self):
  d=self.data();self.runner.run('paired',d);d['sound_id']='b'*32
  with self.assertRaises(ValueError):self.runner.run('paired',d)
  self.assertEqual(3,len(self.events))
 def test_only_chat_and_library_ids_allowed_before_input(self):
  for fields in [{'action':'macro'},{'sound_id':'../file.wav'},{'script':'x'},{'requestId':'invalid'}]:
   d=self.data();d.update(fields)
   with self.assertRaises(ValueError):self.runner.run('paired',d)
  self.assertEqual([],self.events)
 def test_quick_chat_also_sequences_sound(self):
  d={'action':'quick','name':'Nice shot!','sound_id':'a'*32,'requestId':str(uuid.uuid4())};self.assertTrue(self.runner.run('paired',d)['sound_started'])
class HttpTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();cls.root=Path(cls.tmp.name);source=cls.root/'server.py';source.write_bytes((HERE/'payload/server.py').read_bytes())
  reference=Path(os.environ.get('ICARUS_PHASE49_REFERENCE','/workspace/icarus-bulk-reference'))/'ICARUS'
  sys.path.insert(0,str(reference));sys.path.insert(0,str(HERE.parent/'phase49-host-actions/payload'))
  cls.events=[]
  def record(kind):return lambda *a,**k:cls.events.append((kind,a))
  sys.modules['pyautogui']=types.SimpleNamespace(**{n:record(n) for n in ['press','hotkey','keyUp','mouseUp','mouseDown','keyDown','write']})
  spec=importlib.util.spec_from_file_location('chat_sound_http_fixture',source);cls.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.m);cls.m.TOKENS={cls.m.token_hash('paired')}
  cls.fake=FakeSounds(cls.events);cls.m.CHAT_SOUNDS=ChatSounds(cls.m.action,cls.fake,cls.m.LOCK)
  cls.server=cls.m.http.server.ThreadingHTTPServer(('127.0.0.1',0),cls.m.Handler);threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.url=f'http://127.0.0.1:{cls.server.server_port}'
 @classmethod
 def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.m.TV_SERVICE.close();cls.m.WINDOWS_MONITOR.stop_event.set();cls.tmp.cleanup()
 def setUp(self):self.events.clear()
 def req(self,d,token='paired',origin=None,path='/api/rocket/chat-sound'):
  headers={'Content-Type':'application/json','Authorization':'Bearer '+token}
  if origin:headers['Origin']=origin
  req=urllib.request.Request(self.url+path,data=json.dumps(d).encode(),headers=headers)
  try:
   with urllib.request.urlopen(req,timeout=5) as r:return r.status,json.load(r)
  except urllib.error.HTTPError as e:return e.code,json.load(e)
 def data(self):return {'action':'text','text':'Fixture only','channel':'team','speed':'balanced','sound_id':'a'*32,'requestId':str(uuid.uuid4())}
 def test_actual_text_handler_orders_open_write_enter_then_existing_sound_service(self):
  with patch.object(self.m.time,'sleep',return_value=None):code,data=self.req(self.data())
  self.assertEqual(200,code);self.assertTrue(data['chat_input_completed']);self.assertEqual([('press',('y',)),('write',('Fixture only',)),('press',('enter',))],self.events[:3]);self.assertEqual('sound',self.events[3][0])
 def test_auth_origin_and_invalid_chat_never_play_sound(self):
  self.assertEqual(401,self.req(self.data(),token='wrong')[0]);self.assertEqual(403,self.req(self.data(),origin='http://other.invalid')[0]);d=self.data();d['channel']='bad';code,result=self.req(d);self.assertEqual(200,code);self.assertFalse(result['chat_input_completed']);self.assertEqual([],self.events)
 def test_no_sound_original_action_is_unchanged(self):
  with patch.object(self.m.time,'sleep',return_value=None):code,data=self.req({'action':'quick','name':'Nice shot!'},path='/api/action')
  self.assertEqual(200,code);self.assertEqual('Quick chat sent',data['message']);self.assertEqual([('press',('1',)),('press',('1',))],self.events)
class InstallerTests(unittest.TestCase):
 def test_matching_host33_install_idempotence_and_code_restore_preserve_settings(self):
  with tempfile.TemporaryDirectory() as temp,patch.object(installer,'running',return_value=False):
   root=Path(temp);original=(HERE.parent/'phase49-host-actions/payload/server.py').read_bytes();(root/'server.py').write_bytes(original);(root/'config.json').write_text('{"private":"retain"}')
   installer.apply(root);self.assertEqual('new',installer.preflight(root)[2]);self.assertIn('Already installed',installer.apply(root));backup=next((root/'umbra_host_code_backups').iterdir());installer.restore(root,backup);self.assertEqual(original,(root/'server.py').read_bytes());self.assertEqual('{"private":"retain"}',(root/'config.json').read_text());self.assertFalse((root/'umbra_chat_sounds.py').exists())
 def test_changed_source_is_refused(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);(root/'server.py').write_text('changed')
   with self.assertRaises(ValueError):installer.apply(root)
if __name__=='__main__':unittest.main(verbosity=2)
