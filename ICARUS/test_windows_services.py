"""Deterministic Windows API fixtures; these do not certify physical Windows hardware."""
import json,socket,tempfile,time,types,unittest
from pathlib import Path
from unittest.mock import Mock,patch
from windows_monitor import WindowsProbe,MonitorService
from windows_control import WindowsControl,HOTKEYS,usable,discover_windows
from windows_icons import png,installed_icon
class WindowsServices(unittest.TestCase):
 def control(self,**kw):
  return WindowsControl(Mock(),system='Windows',discover=lambda:[{'name':'Google Chrome','kind':'link','path':'fixture.lnk','target':'fixture.exe'}],validate=lambda r:True,icon=lambda *a:png(1,1,b'\xff\x00\x00\xff'),launch=Mock(),**kw)
 def test_predefined_hotkeys_release_keys_and_deduplicate(self):
  c=self.control();r=c.command('paired','request01','hotkey','task_manager');self.assertEqual(r['status'],'sent');self.assertTrue(c.command('paired','request01','hotkey','task_manager')['duplicate']);c.pg.hotkey.assert_called_once_with('ctrl','shift','esc');self.assertEqual(c.pg.keyUp.call_count,3)
 def test_failed_hotkey_releases_modifiers(self):
  c=self.control();c.pg.hotkey.side_effect=OSError('Denied')
  with self.assertRaises(OSError):c.command('p','request01','hotkey','snip')
  self.assertEqual(c.pg.keyUp.call_count,3)
 def test_command_allowlist_and_request_identity(self):
  c=self.control()
  for request,kind,ident in [('bad','hotkey','snip'),('request01','shell','calc.exe'),('request01','hotkey','win+r+evil')]:
   with self.assertRaises(ValueError):c.command('p',request,kind,ident)
  c.command('p','request01','hotkey','snip')
  with self.assertRaises(ValueError):c.command('p','request01','hotkey','run')
 def test_app_discovery_icons_launch_and_unavailable(self):
  c=self.control();c.scan();v=c.view();self.assertEqual([a['id'] for a in v['apps'] if a['installed']],['chrome']);self.assertTrue(c.image('chrome').startswith(b'\x89PNG'));self.assertNotIn('fixture.exe',json.dumps(v));c.command('p','request01','launch','chrome');c.command('p','request01','launch','chrome');c.launch.assert_called_once()
  with self.assertRaisesRegex(ValueError,'not discovered'):c.command('p','request02','launch','fortnite')
 def test_launch_revalidates_moved_target(self):
  c=self.control();c.scan();c.validate=lambda r:False
  with self.assertRaisesRegex(ValueError,'moved'):c.command('p','request01','launch','chrome')
  c.launch.assert_not_called()
 def test_discovery_failure_retains_last_valid_catalog(self):
  c=self.control();c.scan();c.discover=Mock(side_effect=OSError('discovery denied'));c.scan();self.assertIn('denied',c.view()['error']);self.assertIn('chrome',c.records)
 def test_no_fake_windows_values_or_commands_on_other_os(self):
  self.assertFalse(WindowsProbe(system='Linux').sample()['supported']);c=WindowsControl(Mock(),system='Linux');self.assertFalse(c.view()['supported'])
  with self.assertRaisesRegex(ValueError,'unavailable'):c.command('p','request01','hotkey','run')
 def test_missing_optional_psutil_graceful(self):self.assertIn('psutil unavailable',WindowsProbe(lib=None,system='Windows').sample()['reason'])
 def test_counters_rates_process_bounds_and_history(self):
  timer=[100];counter=[1000];ns=types.SimpleNamespace
  p=Mock();p.cpu_count.side_effect=lambda **kw:4 if kw else 8;p.cpu_percent.side_effect=lambda **kw:[25,50] if kw.get('percpu') else 37.5;p.cpu_freq.return_value=ns(current=2700);p.virtual_memory.return_value=ns(total=16000,used=8000,available=8000,percent=50);p.disk_partitions.return_value=[ns(device='C:',mountpoint='C:\\',fstype='NTFS')];p.disk_usage.return_value=ns(total=20000,used=15000,free=5000,percent=75);p.net_if_stats.return_value={'Ethernet':ns(isup=True)};p.net_if_addrs.return_value={'Ethernet':[ns(family=socket.AF_INET,address='192.168.1.10')]};p.net_io_counters.side_effect=lambda **k:{'Ethernet':ns(bytes_sent=counter[0],bytes_recv=counter[0]*2)};p.disk_io_counters.side_effect=lambda:ns(read_bytes=counter[0]*4,write_bytes=counter[0]*2);p.sensors_battery.return_value=ns(percent=83,power_plugged=True);p.boot_time.return_value=time.time()-3600;p.sensors_temperatures.side_effect=AttributeError();p.process_iter.return_value=[ns(info={'pid':i,'name':'proc','cpu_percent':i,'memory_info':ns(rss=i*100)}) for i in range(40)]
  probe=WindowsProbe(lib=p,system='Windows',clock=lambda:timer[0]);probe.extras=lambda:{'gpus':[],'power_scheme':None}
  first=probe.sample();self.assertTrue(first['warming_up']);self.assertIsNone(first['interfaces'][0]['upload_bytes_sec']);timer[0]+=2;counter[0]+=200;second=probe.sample();self.assertEqual(second['interfaces'][0]['upload_bytes_sec'],100);self.assertEqual(second['disk_activity']['read_bytes_sec'],400);self.assertEqual(second['memory']['used'],8000);self.assertIsNone(second['cpu_temperature_c']);self.assertEqual(len(second['processes']),20);self.assertEqual(second['processes'][0]['pid'],39)
  service=MonitorService(probe);service.started=True
  for _ in range(70):service.collect()
  self.assertEqual(len(service.view()['history']),60);copy=service.view();copy['sample']['memory']['used']=0;self.assertEqual(service.view()['sample']['memory']['used'],8000)
 def test_monitor_failure_marks_stale_and_keeps_previous_sample(self):
  probe=Mock();probe.sample.return_value={'supported':True,'cpu_percent':42};m=MonitorService(probe);m.started=True;m.collect();probe.sample.side_effect=RuntimeError('denied');m.collect();self.assertEqual(m.view()['sample']['cpu_percent'],42);self.assertIn('denied',m.view()['error'])
 def test_optional_gpu_values_and_read_only_command_cache(self):
  p=WindowsProbe(system='Windows');r=Mock(returncode=0,stdout='Power Scheme GUID: fixture');g=Mock(returncode=0,stdout='NVIDIA fixture, 25, 1024, 4096, 65, 1300, 50\n')
  with patch('windows_monitor.subprocess.run',side_effect=[r,g]) as run,patch('windows_monitor.shutil.which',return_value='nvidia-smi'):
   a=p.extras();p.extras();self.assertEqual(run.call_count,2);self.assertEqual(a['gpus'][0]['vram_used_bytes'],1073741824);self.assertEqual(run.call_args_list[0].args[0][-1],'/getactivescheme');self.assertIn('--query-gpu=',run.call_args_list[1].args[0][1])
 def test_unavailable_gpu_sensors_are_null(self):
  p=WindowsProbe(system='Windows');r=Mock(returncode=0,stdout='scheme');g=Mock(returncode=0,stdout='NVIDIA fixture, [N/A], [N/A], 4096, [N/A], [N/A], [N/A]\n')
  with patch('windows_monitor.subprocess.run',side_effect=[r,g]),patch('windows_monitor.shutil.which',return_value='nvidia-smi'):
   a=p.extras()['gpus'][0];self.assertIsNone(a['temperature_c']);self.assertIsNone(a['utilization_percent'])
 def test_local_url_allowlist_rejects_shell_and_network(self):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/'Fortnite.url'
   for url,expected in [('https://evil.invalid/run',False),('file:///C:/evil.exe',False),('steam://rungameid/252950',True),('com.epicgames.launcher://apps/Fortnite?action=launch&silent=true',True)]:
    path.write_text('[InternetShortcut]\nURL='+url);self.assertEqual(usable({'kind':'url','path':str(path)}),expected)
  self.assertFalse(usable({'kind':'store','app_id':'evil;Start-Process bad'}));self.assertTrue(usable({'kind':'store','app_id':'Microsoft.Minecraft_fixture!App'}))
 def test_discovery_does_not_execute_remote_input(self):
  with patch('windows_control.platform.system',return_value='Windows'),patch('windows_control.subprocess.run',return_value=Mock(returncode=0,stdout=b'[]')) as run:
   self.assertEqual(discover_windows(),[]);args=run.call_args.args[0];self.assertIn('-NoProfile',args);self.assertNotIn('-ExecutionPolicy',args);self.assertNotIn('shell',run.call_args.kwargs)
 def test_receipt_cache_bounded(self):
  c=self.control()
  for i in range(280):c.command('p','request_%04d'%i,'hotkey','start')
  self.assertLessEqual(len(c.receipts),256)
 def test_png_encoder_and_no_fabricated_icon(self):
  self.assertTrue(png(1,1,b'\0\0\0\0').startswith(b'\x89PNG'))
  if not hasattr(__import__('ctypes'),'WinDLL'):self.assertIsNone(installed_icon('not-installed.exe'))
if __name__=='__main__':unittest.main(verbosity=2)
