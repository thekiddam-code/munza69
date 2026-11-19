"""Preservation/DSP/capture fixtures. No actual Windows or user library is available."""
import io,json,math,struct,tempfile,threading,unittest,wave,zipfile
from pathlib import Path
from unittest.mock import patch
from sound_library import SoundLibrary,SoundError
from sound_service import SoundService
from sound_backup import backup,inventory,verify_archive
from audio_loudness import measure,normalize,pcm
from audio_service import AudioService
F={'name':'Existing sound','category':'Crew','icon':'play','favorite':True,'volume':.35}
def tone(seconds=1,amp=.1):
 b=io.BytesIO()
 with wave.open(b,'wb') as w:w.setparams((1,2,24000,0,'NONE','none'));w.writeframes(b''.join(struct.pack('<h',round(amp*32767*math.sin(2*math.pi*1000*i/24000))) for i in range(round(seconds*24000))))
 return b.getvalue()
class Input:
 def __init__(self):self.calls=0
 def devices(self):return [{'id':0,'name':'Fixture physical mic','kind':'fixture'}]
 def sample(self,device,seconds,cancel):self.calls+=1;return tone(seconds,.1)
class AudioFoundation(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'soundboard_data';self.sounds=SoundService(self.root);self.capture=Input();self.audio=AudioService(self.sounds,self.capture)
 def tearDown(self):self.sounds.player.stop();self.tmp.cleanup()
 def seed(self):return self.sounds.library.add(F,tone(.5),0,True,'Existing B fixture')
 def test_backup_preserves_metadata_audio_order_and_unknown_files(self):
  d=self.seed();(self.root/'original-notes.txt').write_text('Keep this file too');before=inventory(self.root);r=backup(self.root);self.assertTrue(r['verified']);self.assertEqual(inventory(self.root),before);m=verify_archive(self.root.parent/'soundboard_backups'/r['file']);self.assertEqual(m['source'],before);self.assertEqual(SoundLibrary(self.root).view(),d)
 def test_backup_failure_blocks_edits_preserves_all_original_bytes(self):
  d=self.seed();before=inventory(self.root)
  with patch('sound_service.backup',side_effect=OSError('Controlled disk full')):
   with self.assertRaisesRegex(SoundError,'backup required'):self.sounds.post('edit',{'id':d['sounds'][0]['id'],'fields':{**F,'name':'New'},'revision':d['revision']},'owner')
  self.assertEqual(inventory(self.root),before)
 def test_missing_clip_is_backed_up_as_found_but_writes_blocked(self):
  d=self.seed();(self.root/(d['sounds'][0]['id']+'.wav')).unlink()
  with self.assertRaisesRegex(SoundError,'Missing clip'):self.sounds.preserve_existing()
  self.assertTrue(list((self.root.parent/'soundboard_backups').glob('*.zip')));self.assertEqual(self.sounds.library.view(),d)
 def test_backup_rejects_nested_destination_and_detects_archive_tampering(self):
  self.seed()
  with self.assertRaises(ValueError):backup(self.root,self.root/'backups')
  r=backup(self.root);p=self.root.parent/'soundboard_backups'/r['file']
  with zipfile.ZipFile(p,'a') as z:z.writestr('soundboard_data/'+next(n for n in inventory(self.root)['files'] if n.endswith('.wav')),b'corrupt')
  with self.assertRaises(ValueError):verify_archive(p)
 def test_server_backup_precedes_calibration_and_profiles_do_not_migrate_v1(self):
  d=self.seed();before={n:(self.root/n).read_bytes() for n in inventory(self.root)['files']};result=self.audio.calibrate(self.capture.devices()[0],True);self.assertEqual(self.capture.calls,1);self.assertFalse(result['profile']['enabled']);self.assertEqual(self.sounds.library.view(),d);self.assertTrue(list((self.root.parent/'soundboard_backups').glob('*.zip')))
  for n,b in before.items():self.assertEqual((self.root/n).read_bytes(),b)
  other=SoundService(self.root);self.assertEqual(other.library.view(),d);self.assertEqual(AudioService(other,self.capture).profile(),self.audio.profile())
 def test_no_input_sampling_on_status_or_missing_consent(self):
  self.audio.view();self.assertEqual(self.capture.calls,0)
  with self.assertRaises(SoundError):self.audio.calibrate(self.capture.devices()[0],False)
  self.assertEqual(self.capture.calls,0)
 def test_k_weighted_integrated_reference_and_gating(self):
  d=measure(tone(2,.1));self.assertAlmostEqual(d['integrated_lufs'],-23.0,delta=.2);self.assertAlmostEqual(d['sample_peak_dbfs'],-20,delta=.02)
  raw=tone(2,.1)
  with wave.open(io.BytesIO(raw),'rb') as w:samples=w.readframes(w.getnframes())
  b=io.BytesIO()
  with wave.open(b,'wb') as w:w.setparams((1,2,24000,0,'NONE','none'));w.writeframes(samples+b'\0\0'*72000)
  self.assertAlmostEqual(measure(b.getvalue())['integrated_lufs'],d['integrated_lufs'],delta=.8)
 def test_silence_cannot_calibrate_or_receive_unbounded_gain(self):
  self.seed();self.capture.sample=lambda *a:tone(5,0)
  with self.assertRaisesRegex(SoundError,'silent'):self.audio.calibrate(self.capture.devices()[0],True)
  processed,metrics=normalize(tone(.5,0),-23);self.assertEqual(max(map(abs,pcm(processed))),0);self.assertLessEqual(metrics['applied_gain_db'],0)
 def test_normalization_target_boost_and_peak_ceiling(self):
  raw=tone(1,.1);processed,d=normalize(raw,-20,offset=-3);self.assertAlmostEqual(measure(processed)['integrated_lufs'],-23,delta=.3);self.assertLessEqual(d['applied_gain_db'],6)
  processed,d=normalize(tone(.5,.9),-10,volume=1);self.assertLessEqual(max(map(abs,pcm(processed))),10**(-1/20)+1/32768)
  _,d=normalize(tone(1,.0005),-15);self.assertLessEqual(d['applied_gain_db'],6)
 def test_new_processing_is_opt_in_and_original_bytes_and_volumes_never_change(self):
  d=self.seed();item=d['sounds'][0];raw=self.sounds.library.get(item['id'])[0];self.assertEqual(self.audio.processed(raw,item),(raw,.35,None));self.audio.calibrate(self.capture.devices()[0],True);self.audio.update({'enabled':True,'offset_db':-3,'ceiling_dbfs':-1,'max_boost_db':6});out,gain,metrics=self.audio.processed(raw,item);self.assertEqual(gain,1);self.assertIsNotNone(metrics);self.assertEqual(self.sounds.library.get(item['id'])[0],raw);self.assertEqual(self.sounds.library.view(),d)
 def test_reset_cancels_only_owned_resources_and_does_not_create_empty_library(self):
  self.audio.reset();self.assertFalse(self.root.exists());self.assertTrue(self.audio.cancel.is_set());self.assertFalse(self.audio.profile()['enabled'])
 def test_missing_server_library_blocks_calibration_without_recording_or_creation(self):
  with self.assertRaisesRegex(SoundError,'library.json is missing'):self.audio.calibrate(self.capture.devices()[0],True)
  self.assertEqual(self.capture.calls,0);self.assertFalse(self.root.exists())
 def test_native_capture_flow_is_bounded_and_releases_only_owned_handles(self):
  import ctypes,types
  from audio_capture import CaptureInput
  calls=[];state={};a=types.SimpleNamespace()
  def opened(handle,*args):handle._obj.value=321;return 0
  def prepare(handle,hdr,size):state['header']=hdr._obj;return 0
  def start(handle):
   raw=tone(5)
   with wave.open(io.BytesIO(raw),'rb') as w:pcm=w.readframes(w.getnframes())
   ctypes.memmove(state['header'].data,pcm,len(pcm));state['header'].recorded=len(pcm);state['header'].flags=1;return 0
  a.waveInOpen=opened;a.waveInPrepareHeader=prepare;a.waveInAddBuffer=lambda *args:0;a.waveInStart=start
  for name in ['waveInStop','waveInReset','waveInUnprepareHeader','waveInClose']:setattr(a,name,lambda *args,n=name:calls.append(n) or 0)
  c=CaptureInput();c.api=lambda:a;devices=[{'id':0,'name':'Fixture input','kind':'fixture'}];c.devices=lambda:devices
  raw=c.sample(devices[0],5,threading.Event());self.assertAlmostEqual(measure(raw)['duration_seconds'],5);self.assertEqual(calls,['waveInStop','waveInReset','waveInUnprepareHeader','waveInClose'])
  cancelled=threading.Event();cancelled.set()
  with self.assertRaisesRegex(SoundError,'cancelled'):c.sample(devices[0],5,cancelled)
  self.assertEqual(calls[-4:],['waveInStop','waveInReset','waveInUnprepareHeader','waveInClose'])
 def test_shutdown_preserves_enabled_profile_while_emergency_reset_disables_it(self):
  self.seed();self.audio.calibrate(self.capture.devices()[0],True);self.audio.update({'enabled':True,'offset_db':-3,'ceiling_dbfs':-1,'max_boost_db':6});before=self.audio.path.read_bytes();self.audio.close();self.assertEqual(self.audio.path.read_bytes(),before);self.assertTrue(self.audio.profile()['enabled']);self.audio.reset();self.assertFalse(self.audio.profile()['enabled'])
 def test_corrupt_optional_profile_keeps_library_visible_and_exportable(self):
  d=self.seed();self.audio.path.write_text('BROKEN PROFILE');self.sounds.player.profile_reader=self.audio.profile;view=self.sounds.view();self.assertEqual(view['sounds'],d['sounds']);self.assertTrue(view['audio_profile']['invalid']);self.assertIn('unreadable',view['audio_error']);self.assertTrue(self.sounds.make_backup()['verified'])
 def test_profile_validation_rejects_unsafe_settings(self):
  for offset,ceiling,boost in [(5,-1,6),(-3,0,6),(-3,-1,99)]:
   with self.assertRaises(SoundError):self.audio.update({'enabled':False,'offset_db':offset,'ceiling_dbfs':ceiling,'max_boost_db':boost})
  with self.assertRaises(SoundError):self.audio.update({'enabled':True,'offset_db':-3,'ceiling_dbfs':-1,'max_boost_db':6})
if __name__=='__main__':unittest.main(verbosity=2)
