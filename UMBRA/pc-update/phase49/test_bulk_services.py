import base64,tempfile,unittest
from pathlib import Path
from sound_library import SoundLibrary,SoundError,MAX_SOUNDS,MAX_LIBRARY_BYTES
from sound_service import SoundService
from test_sound_services import clip,FIELDS

class BulkServices(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'soundboard_data';self.service=SoundService(self.root)
 def tearDown(self):self.tmp.cleanup()
 def body(self,revision=0,skip=True):return {'fields':FIELDS,'audio':base64.b64encode(clip()).decode(),'revision':revision,'permission':True,'source':'Bulk fixture','skip_duplicate':skip}
 def test_duplicate_skip_preserves_original_mapping_revision_and_output(self):
  original=self.service.post('import',self.body(),'fixture');ident=original['sounds'][0]['id'];self.service.library.output({'id':3,'name':'Fixture headphones'},original['revision']);before=self.service.library.view()
  body=self.body(before['revision']);body['fields']={**FIELDS,'name':'Different label'}
  result=self.service.post('import',body,'fixture')
  self.assertEqual(result['duplicate_id'],ident);self.assertEqual(self.service.library.view(),before)
  allow=self.service.post('import',self.body(before['revision'],False),'fixture');self.assertEqual(len(allow['sounds']),2);self.assertNotEqual(allow['sounds'][0]['id'],allow['sounds'][1]['id']);self.assertEqual(allow['output'],before['output'])
 def test_duplicate_skip_still_checks_revision_permission_and_types(self):
  original=self.service.post('import',self.body(),'fixture');before=self.service.library.view()
  for body in [self.body(0),{**self.body(original['revision']),'permission':False},{**self.body(original['revision']),'skip_duplicate':'yes'}]:
   with self.assertRaises(SoundError):self.service.post('import',body,'fixture')
  self.assertEqual(self.service.library.view(),before)
 def test_limits_are_advertised_and_old_import_contract_remains_valid(self):
  self.assertEqual(self.service.view()['limits'],{'max_sounds':512,'max_audio_bytes':256*1024*1024})
  old=self.body();del old['skip_duplicate'];result=self.service.post('import',old,'fixture');self.assertEqual(len(result['sounds']),1)
  self.assertEqual(MAX_SOUNDS,512);self.assertEqual(MAX_LIBRARY_BYTES,256*1024*1024)
