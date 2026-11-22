"""Local library/import/render control tests; no microphone or Sonar fixtures are opened."""
import base64,ctypes,io,json,struct,tempfile,threading,types,unittest,wave
from pathlib import Path
from unittest.mock import patch,Mock
from sound_library import SoundLibrary,SoundError,MAX_SOUNDS,validate_audio
from sound_service import SoundService
from sound_output import WaveOutput
from sound_import import allowed,import_page,public_host,Redirect

def clip(seconds=.2):
 b=io.BytesIO()
 with wave.open(b,'wb') as w:w.setparams((1,2,24000,0,'NONE','not compressed'));w.writeframes(struct.pack('<h',12000)*round(24000*seconds))
 return b.getvalue()
FIELDS={'name':'Test sound','category':'General','icon':'play','volume':.35,'favorite':False}
class Backend:
 def __init__(self):self.calls=[];self.available=[{'id':0,'name':'FIXTURE render output'}]
 def devices(self):return self.available
 def play(self,raw,device,volume,stop,started):self.calls.append((raw,device,volume));started();stop.wait(.1)
class Sounds(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'sounds';self.backend=Backend();self.service=SoundService(self.root,self.backend);self.lib=self.service.library
 def tearDown(self):self.service.player.stop();self.tmp.cleanup()
 def add(self,name='Test sound'):
  return self.lib.add({**FIELDS,'name':name},clip(),self.lib.view()['revision'],True,'fixture upload')
 def test_library_save_restart_and_exact_audio(self):
  d=self.add();item=d['sounds'][0];other=SoundLibrary(self.root);self.assertEqual(other.view(),d);self.assertEqual(other.get(item['id'])[0],clip());self.assertFalse((self.root.parent/'config.json').exists())
 def test_edits_reorder_favorites_categories_and_delete_are_persistent(self):
  self.add('First');d=self.add('Second');a,b=[x['id'] for x in d['sounds']];d=self.lib.edit(a,{**FIELDS,'name':'Changed','favorite':True,'category':'Voice','icon':'crew','volume':.7},d['revision']);d=self.lib.reorder([b,a],d['revision']);self.assertEqual(d['sounds'][1]['name'],'Changed');self.assertTrue(d['sounds'][1]['favorite']);d=self.lib.delete(b,d['revision']);self.assertEqual(len(d['sounds']),1);self.assertFalse((self.root/(b+'.wav')).exists());self.assertEqual(SoundLibrary(self.root).view(),d)
 def test_conflicting_edits_do_not_overwrite_other_terminal(self):
  d=self.add();ident=d['sounds'][0]['id'];self.lib.edit(ident,{**FIELDS,'name':'New name'},d['revision'])
  with self.assertRaisesRegex(SoundError,'another terminal'):self.lib.delete(ident,d['revision'])
  self.assertEqual(self.lib.view()['sounds'][0]['name'],'New name')
 def test_invalid_audio_permission_metadata_and_path_traversal(self):
  for audio in [b'not audio',clip(30.1),clip()[:-5]]:
   with self.assertRaises(SoundError):self.lib.add(FIELDS,audio,0,True,'fixture')
  with self.assertRaises(SoundError):self.lib.add(FIELDS,clip(),0,False,'fixture')
  for fields in [{**FIELDS,'volume':9},{**FIELDS,'icon':'<script>'},{**FIELDS,'name':''}]:
   with self.assertRaises(SoundError):self.lib.add(fields,clip(),0,True,'fixture')
  with self.assertRaises(SoundError):self.lib.get('../secret')
 def test_library_count_bound_never_evicts_existing_sounds(self):
  for i in range(MAX_SOUNDS):self.add('Sound '+str(i))
  before=self.lib.view()
  with self.assertRaisesRegex(SoundError,'Library limit'):self.add('One too many')
  self.assertEqual(self.lib.view(),before)
 def test_bad_reorder_cannot_duplicate_or_lose_clips(self):
  d=self.add();self.add('Other');before=self.lib.view();ident=d['sounds'][0]['id']
  for ids in [[ident,ident],[],['../secret']]:
   with self.assertRaises(SoundError):self.lib.reorder(ids,before['revision'])
  self.assertEqual(self.lib.view(),before)
 def test_corrupt_library_is_reported_never_reset(self):
  self.root.mkdir();p=self.root/'library.json';p.write_bytes(b'BROKEN PRIVATE LIBRARY')
  with self.assertRaises(SoundError):self.lib.view()
  self.assertEqual(p.read_bytes(),b'BROKEN PRIVATE LIBRARY')
 def test_import_metadata_commit_failure_keeps_previous_library(self):
  before=self.add();replace=__import__('os').replace
  def fail(source,target):
   if str(target).endswith('library.json'):raise OSError('Controlled disk failure')
   return replace(source,target)
  with patch('sound_library.os.replace',side_effect=fail):
   with self.assertRaises(OSError):self.add('Will fail')
  self.assertEqual(self.lib.view(),before);self.assertEqual(len(list(self.root.glob('*.wav'))),1)
 def test_checksum_detects_modified_audio_without_destroying_it(self):
  d=self.add();ident=d['sounds'][0]['id'];p=self.root/(ident+'.wav');p.write_bytes(b'changed')
  with self.assertRaisesRegex(SoundError,'checksum'):self.lib.get(ident)
  self.assertEqual(p.read_bytes(),b'changed')
 def test_play_requires_explicit_valid_output_and_deduplicates(self):
  d=self.add();ident=d['sounds'][0]['id'];data={'id':ident,'requestId':'request_001'}
  with self.assertRaisesRegex(SoundError,'explicit'):self.service.post('play',data,'paired')
  self.service.post('output',{'device':self.backend.available[0],'revision':d['revision']},'paired');self.service.post('play',data,'paired');self.assertTrue(self.service.post('play',data,'paired')['duplicate']);self.assertEqual(len(self.backend.calls),1);self.assertEqual(self.backend.calls[0][2],.35);self.service.post('stop',{},'paired');self.assertEqual(self.service.player.view()['state'],'idle')
 def test_output_identity_changes_cannot_silently_use_another_device(self):
  d=self.add();self.lib.output(self.backend.available[0],d['revision']);self.backend.available=[{'id':0,'name':'Different device'}]
  with self.assertRaisesRegex(SoundError,'unavailable'):self.service.post('play',{'id':d['sounds'][0]['id'],'requestId':'request_002'},'paired')
  self.assertEqual(self.backend.calls,[])
 def test_new_api_rejects_unknown_fields_and_freeform_paths(self):
  for op,data in [('play',{'id':'x','requestId':'request_001','path':'secret.wav'}),('output',{'device':{'id':-1,'name':'Default'},'revision':0}),('shell',{}),('import',{})]:
   with self.assertRaises(SoundError):self.service.post(op,data,'paired')
 def test_playback_error_has_actionable_status_and_keeps_library(self):
  d=self.add();self.lib.output(self.backend.available[0],d['revision']);self.backend.play=Mock(side_effect=OSError('Controlled device removal'))
  with self.assertRaisesRegex(SoundError,'removal'):self.service.post('play',{'id':d['sounds'][0]['id'],'requestId':'request_003'},'paired')
  self.assertEqual(self.service.view()['player']['state'],'error');self.assertEqual(len(self.lib.view()['sounds']),1)
 def test_import_base64_is_validated(self):
  data={'fields':FIELDS,'audio':'invalid!!!','revision':0,'permission':True,'source':'test'}
  with self.assertRaises(SoundError):self.service.post('import',data,'paired')
  data['audio']=base64.b64encode(clip()).decode();self.assertEqual(len(self.service.post('import',data,'paired')['sounds']),1)
 def test_import_url_allowlist_rejects_nonpublic_hosts_credentials_and_redirects(self):
  for url in ['http://www.myinstants.com/en/instant/test/','https://localhost/en/instant/test/','https://www.myinstants.com@127.0.0.1/en/instant/test/','https://www.myinstants.com/en/instant/test/?x=file','https://www.myinstants.com/media/sounds/../private.mp3']:
   with self.assertRaises(SoundError):allowed(url)
  with self.assertRaises(SoundError):Redirect(True).redirect_request(None,None,302,'',{},'https://evil.invalid/clip.mp3')
  with patch('sound_import.socket.getaddrinfo',return_value=[(None,None,None,None,('127.0.0.1',443))]):
   with self.assertRaises(SoundError):public_host('https://www.myinstants.com/en/instant/test/')
 def test_supported_public_page_import_and_clear_failure(self):
  with patch('sound_import.fetch',side_effect=[(b'<title>Actual sound - Myinstants</title><audio src="/media/sounds/test.mp3"></audio>','text/html'),(b'fixture-audio','audio/mpeg')]):
   d=import_page('https://www.myinstants.com/en/instant/test/',True);self.assertEqual(d['name'],'Actual sound');self.assertEqual(base64.b64decode(d['audio']),b'fixture-audio')
  with patch('sound_import.fetch',return_value=(b'<html>No permitted audio</html>','text/html')):
   with self.assertRaisesRegex(SoundError,'No supported'):import_page('https://www.myinstants.com/en/instant/test/',True)
 def test_related_page_buttons_are_never_mistaken_for_the_requested_sound(self):
  body=b'<button class="small-button" onclick="play(\'/media/sounds/unrelated.mp3\')"></button>'
  with patch('sound_import.fetch',return_value=(body,'text/html')):
   with self.assertRaisesRegex(SoundError,'No supported'):import_page('https://www.myinstants.com/en/instant/test/',True)
  body=b'<meta property="og:audio" content="https://www.myinstants.com/media/sounds/main.mp3">'+body
  with patch('sound_import.fetch',side_effect=[(body,'text/html'),(b'main-clip','audio/mpeg')]) as fetch:
   import_page('https://www.myinstants.com/en/instant/test/',True);self.assertTrue(fetch.call_args.args[0].endswith('/main.mp3'))
 def test_url_usage_permission_and_import_rate_limits(self):
  with self.assertRaises(SoundError):import_page('https://www.myinstants.com/en/instant/test/',False)
  with patch('sound_service.import_page',return_value={'fixture':True}):
   for _ in range(4):self.service.post('link',{'url':'fixture','permission':True},'paired')
   with self.assertRaisesRegex(SoundError,'rate limit'):self.service.post('link',{'url':'fixture','permission':True},'paired')
 def test_native_render_flow_gain_cleanup_and_failure_use_no_input_api(self):
  from sound_output import WaveOutput
  api=types.SimpleNamespace();calls=[];pcm=[]
  def opened(handle,*args):handle._obj.value=123;return 0
  def write(handle,header,size):pcm.extend(struct.unpack('<'+'h'*(header._obj.length//2),ctypes.string_at(header._obj.data,header._obj.length)));header._obj.flags=1;return 0
  api.waveOutOpen=opened;api.waveOutPrepareHeader=lambda *a:0;api.waveOutWrite=write;api.waveOutReset=lambda *a:calls.append('reset') or 0;api.waveOutUnprepareHeader=lambda *a:calls.append('unprepare') or 0;api.waveOutClose=lambda *a:calls.append('close') or 0
  backend=WaveOutput();backend.api=lambda:api;backend.devices=lambda:self.backend.available;started=Mock();backend.play(clip(),self.backend.available[0],.35,threading.Event(),started);started.assert_called_once();self.assertLessEqual(max(pcm),4200);self.assertEqual(pcm[0],0);self.assertEqual(calls,['reset','unprepare','close'])
  api.waveOutWrite=lambda *a:7
  with self.assertRaisesRegex(SoundError,'rejected'):backend.play(clip(),self.backend.available[0],.35,threading.Event(),Mock())
  self.assertEqual(calls[-3:],['reset','unprepare','close'])
if __name__=='__main__':unittest.main(verbosity=2)
