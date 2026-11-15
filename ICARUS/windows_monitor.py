"""Read-only, bounded host measurements. No power/fan controls or active network probes."""
import copy,csv,io,math,os,platform,shutil,socket,subprocess,threading,time
from pathlib import Path
try:
 import psutil
except ImportError:
 psutil=None

def finite(value):
 return value if isinstance(value,(float,int)) and math.isfinite(value) else None

def safe(fn,default=None):
 try:return fn()
 except Exception:return default

class WindowsProbe:
 def __init__(self,lib=psutil,system=None,clock=time.monotonic):
  self.lib=lib;self.system=system or platform.system();self.clock=clock;self.previous=None;self.static=None;self.extra_at=-100;self.extra={};self.gpu_tool=None
 def extras(self):
  """Slow optional sensors, refreshed at most every ten seconds; fixed read-only commands."""
  now=self.clock()
  if now-self.extra_at<10:return self.extra
  self.extra_at=now;self.extra={'gpus':[],'power_scheme':None,'sensor_note':'Vendor GPU/CPU thermal sensors may be unavailable.'}
  if self.system!='Windows':return self.extra
  windir=Path(os.environ.get('SystemRoot',r'C:\Windows'))
  try:
   proc=subprocess.run([str(windir/'System32'/'powercfg.exe'),'/getactivescheme'],capture_output=True,text=True,timeout=2,creationflags=0x08000000)
   if proc.returncode==0:self.extra['power_scheme']=proc.stdout.strip()[:240]
  except (OSError,subprocess.SubprocessError):pass
  # NVIDIA's installed utility is queried only; no thermal, fan, clock or power settings are written.
  tool=shutil.which('nvidia-smi')
  if tool:
   try:
    proc=subprocess.run([tool,'--query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu,clocks.gr,power.draw','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=2,creationflags=0x08000000)
    if proc.returncode==0:
     for row in list(csv.reader(io.StringIO(proc.stdout)))[:8]:
      if len(row)!=7:continue
      def number(i):return safe(lambda:finite(float(row[i].strip())))
      self.extra['gpus'].append({'model':row[0].strip()[:160],'utilization_percent':number(1),'vram_used_bytes':None if number(2) is None else number(2)*1048576,'vram_total_bytes':None if number(3) is None else number(3)*1048576,'temperature_c':number(4),'clock_mhz':number(5),'power_w':number(6),'source':'nvidia-smi'})
   except (OSError,subprocess.SubprocessError):pass
  if not self.extra['gpus']:
   # Basic installed display names even when no vendor performance API is present.
   try:
    import winreg
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'SYSTEM\CurrentControlSet\Control\Video') as key:
     for i in range(min(winreg.QueryInfoKey(key)[0],32)):
      sub=winreg.EnumKey(key,i)
      def desc():
       with winreg.OpenKey(key,sub+r'\0000') as device:return winreg.QueryValueEx(device,'DriverDesc')[0]
      name=safe(desc)
      if isinstance(name,str) and name not in [g['model'] for g in self.extra['gpus']]:self.extra['gpus'].append({'model':name[:160],'source':'Windows display registry; performance sensors unavailable'})
   except (OSError,ImportError):pass
  return self.extra
 def sample(self):
  if self.system!='Windows':return {'supported':False,'reason':'Windows measurements unavailable on this host','platform':self.system}
  p=self.lib
  if not p:return {'supported':False,'reason':'psutil unavailable; install requirements.txt','platform':'Windows'}
  if self.static is None:
   model=platform.processor()
   try:
    import winreg
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r'HARDWARE\DESCRIPTION\System\CentralProcessor\0') as k:model=winreg.QueryValueEx(k,'ProcessorNameString')[0].strip()
   except (ImportError,OSError):pass
   self.static={'cpu_model':model or None,'cores':safe(lambda:p.cpu_count(logical=False)),'threads':safe(lambda:p.cpu_count()),'os':platform.platform()}
  now=self.clock();sample={'supported':True,'platform':'Windows',**self.static}
  sample['cpu_percent']=safe(lambda:finite(p.cpu_percent(interval=None)))
  sample['per_core_percent']=safe(lambda:[finite(v) for v in p.cpu_percent(interval=None,percpu=True)])
  freq=safe(lambda:p.cpu_freq());sample['frequency_mhz']=finite(freq.current) if freq else None
  memory=safe(lambda:p.virtual_memory());sample['memory']={k:finite(getattr(memory,k,None)) for k in ('total','used','available','percent')}
  sample['cpu_temperature_c']=safe(lambda:next(finite(x.current) for values in p.sensors_temperatures().values() for x in values if any(s in x.label.lower() for s in ('cpu','package','tctl'))))
  sample['drives']=[]
  for part in (safe(lambda:p.disk_partitions(all=False),[]) or [])[:24]:
   use=safe(lambda:p.disk_usage(part.mountpoint))
   sample['drives'].append({'name':part.device,'mount':part.mountpoint,'filesystem':part.fstype,**{k:finite(getattr(use,k,None)) for k in ('total','used','free','percent')}})
  net=safe(lambda:p.net_io_counters(pernic=True),{}) or {};disks=safe(lambda:p.disk_io_counters(),None);dt=now-self.previous[0] if self.previous else 0
  def delta(current,old,attr):
   a=getattr(current,attr,None);b=getattr(old,attr,None)
   return max(0,(a-b)/dt) if dt>0 and a is not None and b is not None else None
  links=safe(lambda:p.net_if_stats(),{}) or {};addresses=safe(lambda:p.net_if_addrs(),{}) or {};sample['interfaces']=[]
  for name,link in links.items():
   if not link.isup:continue
   ips=[a.address for a in addresses.get(name,[]) if a.family==socket.AF_INET and not a.address.startswith('127.')]
   if not ips:continue
   previous=self.previous[1].get(name) if self.previous else None
   sample['interfaces'].append({'name':name,'ipv4':ips,'link_up':True,'upload_bytes_sec':delta(net.get(name),previous,'bytes_sent'),'download_bytes_sec':delta(net.get(name),previous,'bytes_recv')})
  sample['disk_activity']={'read_bytes_sec':delta(disks,self.previous[2] if self.previous else None,'read_bytes'),'write_bytes_sec':delta(disks,self.previous[2] if self.previous else None,'write_bytes')}
  sample['network_note']='Link state and assigned IPv4 only; internet reachability is not probed.'
  battery=safe(lambda:p.sensors_battery());sample['battery']={'percent':finite(battery.percent),'charging':bool(battery.power_plugged)} if battery else None
  boot=safe(lambda:p.boot_time());sample['uptime_seconds']=max(0,time.time()-boot) if boot else None
  rows=[]
  try:
   for process in p.process_iter(['pid','name','cpu_percent','memory_info']):
    try:
     a=process.info;mem=a.get('memory_info');rows.append({'pid':a['pid'],'name':str(a.get('name') or 'Unknown')[:160],'cpu_percent':finite(a.get('cpu_percent')),'ram_bytes':getattr(mem,'rss',None)})
    except (p.NoSuchProcess,p.AccessDenied):continue
  except Exception:pass
  sample['processes']=sorted(rows,key=lambda r:(r['cpu_percent'] or 0,r['ram_bytes'] or 0),reverse=True)[:20]
  sample['process_note']='Top 20 by CPU then RAM; process CPU may exceed 100% across cores. First CPU/rate samples are warming up.'
  sample.update(self.extras());sample['warming_up']=self.previous is None
  if self.previous is None:sample['cpu_percent']=None;sample['per_core_percent']=None
  self.previous=(now,net,disks);return sample

class MonitorService:
 def __init__(self,probe=None,interval=3):
  self.probe=probe or WindowsProbe();self.interval=interval;self.lock=threading.Lock();self.started=False;self.stop_event=threading.Event();self.data=None;self.history=[];self.error=None;self.sampled=None
 def collect(self):
  try:
   data=self.probe.sample();stamp=time.time()
   with self.lock:
    self.data=data;self.sampled=stamp;self.error=None
    self.history.append({'at':stamp,'cpu_percent':data.get('cpu_percent'),'ram_percent':data.get('memory',{}).get('percent')});self.history=self.history[-60:]
  except Exception as e:
   with self.lock:self.error='Monitoring failed: '+str(e)[:180]
 def start(self):
  with self.lock:
   if self.started:return
   self.started=True
  def loop():
   while not self.stop_event.is_set():self.collect();self.stop_event.wait(self.interval)
  threading.Thread(target=loop,daemon=True,name='umbra-monitor').start()
 def view(self):
  self.start()
  with self.lock:return copy.deepcopy({'sample':self.data,'sampled_at':self.sampled,'age_seconds':None if self.sampled is None else max(0,time.time()-self.sampled),'error':self.error,'history':self.history,'interval_seconds':self.interval})
