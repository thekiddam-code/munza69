import unittest
from tv_service import TVService
class Timer:
 def __init__(self,seconds,callback):self.seconds=seconds;self.callback=callback;self.cancelled=False
 def start(self):pass
 def cancel(self):self.cancelled=True
class Socket:
 def __init__(self):self.sent=[];self.closed=False;self.fail=False
 def send(self,text):
  if self.fail:raise OSError('offline')
  self.sent.append(text)
 def close(self):self.closed=True
class TVServiceTests(unittest.TestCase):
 def setUp(self):self.s=Socket();self.ip={'ip':'192.168.1.99'};self.connects=0;self.now=0;self.service=TVService(self.connect,lambda:self.ip,{'home':'KEY_HOME','power_off':'KEY_POWEROFF'},lambda:self.now,Timer)
 def connect(self):self.connects+=1;return self.s
 def test_reuses_pairing_transport_and_denies_arbitrary_keys(self):
  for _ in range(4):self.service.command('home')
  self.assertEqual(self.connects,1);self.assertEqual(len(self.s.sent),4)
  with self.assertRaises(ValueError):self.service.command('KEY_SHUTDOWN_HOST')
 def test_countdown_is_explicit_and_fires_exactly_once(self):
  self.service.start(15,'owner');callback=self.service.timer.callback;self.assertEqual(self.service.status()['timer']['remaining_seconds'],900);callback();callback();self.assertEqual(len(self.s.sent),1);self.assertEqual(self.service.status()['timer']['state'],'sent');self.assertFalse(self.service.status()['execution_acknowledged'])
 def test_cancel_replacement_unpair_and_reconfigure_invalidate_callbacks(self):
  for action in [lambda:self.service.cancel(),lambda:self.service.start(30,'owner'),lambda:self.service.cancel(owner='owner'),lambda:self.service.reconfigure(),lambda:self.service.close()]:
   self.service.start(15,'owner');old=self.service.timer.callback;action();old();self.assertEqual(self.s.sent,[])
 def test_failure_no_late_retry(self):
  self.service.start(15,'owner');cb=self.service.timer.callback;self.s.fail=True;cb();self.assertEqual(self.service.status()['timer']['state'],'failed');self.s.fail=False;cb();self.assertEqual(self.s.sent,[])
 def test_changed_target_never_powers_off_new_tv(self):
  self.service.start(15,'owner');cb=self.service.timer.callback;self.ip['ip']='192.168.1.100';cb();self.assertEqual(self.s.sent,[]);self.assertEqual(self.service.status()['timer']['state'],'cancelled')
 def test_late_wake_never_sends_surprise_power_off(self):
  self.service.start(15,'owner');cb=self.service.timer.callback;self.now=961;cb();self.assertEqual(self.s.sent,[]);self.assertEqual(self.service.status()['timer']['state'],'expired')
 def test_validation_and_restart(self):
  for value in [True,1,'15',16,None,0,-1]:
   with self.assertRaises(ValueError):self.service.start(value,'owner')
  self.ip['ip']=''
  with self.assertRaises(ValueError):self.service.start(15,'owner')
  self.assertEqual(self.service.status()['timer']['state'],'none')
if __name__=='__main__':unittest.main(verbosity=2)
