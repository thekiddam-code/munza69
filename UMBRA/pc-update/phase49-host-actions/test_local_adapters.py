"""Transport contracts and Win32 structure/input cleanup with fake native functions."""
import tempfile,json,unittest,ctypes
from pathlib import Path
from unittest.mock import patch
from test_host_actions import LocalSonar,HostActionError,ScanCodeSender
class Function:
 def __init__(self,fn):self.fn=fn
 def __call__(self,*args):return self.fn(*args)
class AdapterTests(unittest.TestCase):
 def test_discovery_mode_guard_and_exact_output_paths(self):
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp)/'SteelSeries/GG';folder.mkdir(parents=True);(folder/'coreProps.json').write_text('{"ggEncryptedAddress":"127.0.0.1:123"}')
   sonar=LocalSonar(tmp);calls=[];routes=[{'id':k,'deviceId':'old-'+k} for k in ('game','chat','media','aux','mic')]
   def request(base,path,method='GET'):
    calls.append((base,path,method))
    return {'subApps':{'sonar':{'metadata':{'webServerAddress':'http://localhost:456'}}}} if path=='/subApps' else 'classic' if path=='/mode' else routes if path=='/classicRedirections' else []
   with patch.object(sonar,'request',side_effect=request):
    base,prefix,before,devices=sonar.discover();sonar.set_route(base,prefix,'game','{device guid}')
    self.assertEqual(('http://127.0.0.1:456','/classicRedirections/game/deviceId/%7Bdevice%20guid%7D','PUT'),calls[-1])
    with self.assertRaises(HostActionError):sonar.set_route(base,prefix,'mic','anything')
   with patch.object(sonar,'request',side_effect=lambda base,path,method='GET':{'subApps':{'sonar':{'metadata':{'webServerAddress':'http://localhost:456'}}}} if path=='/subApps' else 'stream'):
    with self.assertRaisesRegex(HostActionError,'Classic'):sonar.discover()
 def fake_user(self,partial=False,held=False):
  events=[]
  def send(n,entries,size):
   accepted=1 if partial and not events else n
   events.append(([(entries[i].type,entries[i].data.key.vk,entries[i].data.key.scan,entries[i].data.key.flags) for i in range(n)],size,accepted));return accepted
  class User:pass
  user=User();user.SendInput=Function(send);user.MapVirtualKeyW=Function(lambda vk,mode:{0x12:0x38,0x53:0x1F}.get(vk,0));user.GetAsyncKeyState=Function(lambda vk:0x8000 if held else 0)
  return user,events
 def test_saved_binding_is_scancode_input_and_every_inserted_key_is_released(self):
  user,events=self.fake_user()
  with patch('umbra_host_actions.os.name','nt'),patch('umbra_host_actions.ctypes.WinDLL',return_value=user,create=True),patch('umbra_host_actions.time.sleep'):
   ScanCodeSender().send(['alt','s'])
  self.assertEqual([0x38,0x1F],[r[2] for r in events[0][0]]);self.assertTrue(all(r[1]==0 and r[3]&8 for group,_,_ in events for r in group));self.assertTrue(all(r[3]&2 for r in events[1][0]));self.assertEqual(40 if ctypes.sizeof(ctypes.c_void_p)==8 else 28,events[0][1])
 def test_partial_insertion_cleanup_and_physical_modifier_guard(self):
  user,events=self.fake_user(partial=True)
  with patch('umbra_host_actions.os.name','nt'),patch('umbra_host_actions.ctypes.WinDLL',return_value=user,create=True),patch('umbra_host_actions.time.sleep'):
   with self.assertRaises(HostActionError):ScanCodeSender().send(['alt','s'])
  self.assertEqual(1,len(events[1][0]));self.assertEqual(0x38,events[1][0][0][2]);self.assertTrue(events[1][0][0][3]&2)
  user,events=self.fake_user(held=True)
  with patch('umbra_host_actions.os.name','nt'),patch('umbra_host_actions.ctypes.WinDLL',return_value=user,create=True):
   with self.assertRaisesRegex(HostActionError,'Release'):ScanCodeSender().send(['alt','s'])
  self.assertEqual([],events)
if __name__=='__main__':unittest.main(verbosity=2)
