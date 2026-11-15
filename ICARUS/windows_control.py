"""Explicit Windows shortcuts and a local, discovered five-application allowlist."""
import base64,copy,os,platform,re,subprocess,threading,time
from pathlib import Path
from windows_icons import installed_icon

# Documented Windows 11 combinations. Context-dependent actions say so in the UI.
HOTKEYS=[
 ('start','Start menu','System',['win'],None),('settings','Settings','System',['win','i'],'settings'),('explorer','File Explorer','System',['win','e'],None),('task_manager','Task Manager','System',['ctrl','shift','esc'],None),('lock','Lock PC','System',[],None),('desktop','Show desktop','System',['win','d'],None),
 ('task_view','Task View','Windows',['win','tab'],None),('switch','Switch applications','Windows',['alt','tab'],None),('snap_left','Snap left','Windows',['win','left'],None),('snap_right','Snap right','Windows',['win','right'],None),('maximize','Maximize window','Windows',['win','up'],None),('minimize','Restore / minimize window','Windows',['win','down'],None),('desktop_prev','Previous virtual desktop','Windows',['win','ctrl','left'],None),('desktop_next','Next virtual desktop','Windows',['win','ctrl','right'],None),
 ('snip','Snipping Tool','Utilities',['win','shift','s'],'camera'),('clipboard','Clipboard history','Utilities',['win','v'],None),('emoji','Emoji panel','Utilities',['win','.'],None),('search','Search','Utilities',['win','s'],None),('run','Run dialog','Utilities',['win','r'],None),
 ('volume_up','Volume up','Media',['volumeup'],'volume'),('volume_down','Volume down','Media',['volumedown'],'volume'),('mute','Mute','Media',['volumemute'],'mute'),('play_pause','Play / pause','Media',['playpause'],'play'),('next_track','Next track','Media',['nexttrack'],None),('previous_track','Previous track','Media',['prevtrack'],None)]
CONTEXT={'switch':'Switches to the previous application; foreground/focus dependent.','snap_left':'Applies to the foreground resizable window.','snap_right':'Applies to the foreground resizable window.','maximize':'Applies to the foreground window.','minimize':'Restores a maximized window first; press again to minimize.','desktop_prev':'Requires another virtual desktop to the left.','desktop_next':'Requires another virtual desktop to the right.','clipboard':'Windows clipboard history must be enabled by the user.','play_pause':'Requires an application handling Windows media keys.','next_track':'Requires an application handling Windows media keys.','previous_track':'Requires an application handling Windows media keys.','lock':'Immediately locks the PC; unlock locally.'}
APPS={'rocket_league':('Rocket League',{'rocket league'}),'fortnite':('Fortnite',{'fortnite'}),'chrome':('Google Chrome',{'google chrome','chrome'}),'bambu_studio':('Bambu Studio',{'bambu studio'}),'minecraft':('Minecraft',{'minecraft','minecraft launcher','minecraft for windows','minecraft: java edition'})}
# Fixed local discovery script: no remote paths, arguments, downloads, or policy changes.
DISCOVERY=r'''
$ErrorActionPreference='SilentlyContinue'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$rows=@(); $ws=New-Object -ComObject WScript.Shell
$roots=@([Environment]::GetFolderPath('Programs'),[Environment]::GetFolderPath('CommonPrograms'),[Environment]::GetFolderPath('Desktop'),[Environment]::GetFolderPath('CommonDesktopDirectory'))
foreach($root in $roots){if($root){Get-ChildItem -LiteralPath $root -Recurse -File -Include *.lnk,*.url | Select-Object -First 2000 | ForEach-Object {
 if($_.Extension -eq '.lnk'){$s=$ws.CreateShortcut($_.FullName);$rows+=@{name=$_.BaseName;path=$_.FullName;target=$s.TargetPath;kind='link'}}
 else{$rows+=@{name=$_.BaseName;path=$_.FullName;target='';kind='url'}}
}}}
Get-StartApps | ForEach-Object {if($_.AppID -match '^[A-Za-z0-9._-]+![A-Za-z0-9._-]+$'){$rows+=@{name=$_.Name;app_id=$_.AppID;kind='store'}}}
ConvertTo-Json -InputObject @($rows) -Compress -Depth 3
'''
def discover_windows():
 if platform.system()!='Windows':return []
 import json
 exe=Path(os.environ.get('SystemRoot',r'C:\Windows'))/'System32'/'WindowsPowerShell'/'v1.0'/'powershell.exe'
 result=subprocess.run([str(exe),'-NoLogo','-NoProfile','-NonInteractive','-Command',DISCOVERY],capture_output=True,timeout=20,creationflags=0x08000000)
 if result.returncode:raise ValueError('Windows application discovery failed; check Start menu shortcuts')
 if len(result.stdout)>2000000:raise ValueError('Application inventory exceeds safe size')
 data=json.loads(result.stdout.decode('utf-8-sig',errors='replace'))
 return data if isinstance(data,list) else [data]

def normalize_name(name):return str(name).replace('™','').replace('®','').strip().casefold()

def usable(row):
 kind=row.get('kind')
 if kind=='store':return bool(re.fullmatch(r'[A-Za-z0-9._-]+![A-Za-z0-9._-]+',row.get('app_id','')))
 path=Path(row.get('path',''))
 if not path.is_file() or str(path).startswith('\\\\'):return False
 if kind=='link':
  target=row.get('target','');return path.suffix.lower()=='.lnk' and isinstance(target,str) and target.lower().endswith('.exe') and not target.startswith(('\\\\','http:','https:')) and Path(target).is_file()
 if kind=='url' and path.suffix.lower()=='.url':
  if path.stat().st_size>8192:return False
  import configparser
  config=configparser.ConfigParser(interpolation=None);config.read(path,encoding='utf-8-sig');url=config.get('InternetShortcut','URL',fallback='')
  return bool(re.fullmatch(r'steam://rungameid/\d+|com\.epicgames\.launcher://apps/[A-Za-z0-9:%_.-]+\?action=launch(?:&silent=true)?',url))
 return False

def launch_windows(row):
 if row['kind']=='store':
  exe=Path(os.environ.get('SystemRoot',r'C:\Windows'))/'explorer.exe'
  subprocess.Popen([str(exe),'shell:AppsFolder\\'+row['app_id']],shell=False)
 else:os.startfile(row['path'])

class WindowsControl:
 def __init__(self,pg,system=None,discover=discover_windows,launch=launch_windows,icon=installed_icon,validate=usable,clock=time.monotonic):
  self.pg=pg;self.system=system or platform.system();self.discover=discover;self.launch=launch;self.icon=icon;self.validate=validate;self.clock=clock;self.lock=threading.RLock();self.records={};self.icons={};self.scanning=False;self.scanned=False;self.scan_error=None;self.receipts={}
 def scan(self):
  try:
   records={};icons={}
   for row in self.discover():
    if not isinstance(row,dict):continue
    ident=next((k for k,(_,names) in APPS.items() if normalize_name(row.get('name')) in names),None)
    if not ident or ident in records or not self.validate(row):continue
    records[ident]=row
    try:
     image=self.icon(row.get('target') or row.get('path'),row.get('app_id'))
     if image and len(image)<=65536:icons[ident]=image
    except Exception:pass
   with self.lock:self.records=records;self.icons=icons;self.scan_error=None;self.scanned=True
  except Exception as e:
   with self.lock:self.scan_error=str(e)[:180];self.scanned=True
  finally:
   with self.lock:self.scanning=False
 def refresh(self):
  with self.lock:
   if self.system!='Windows':self.scanned=True;return
   if self.scanning:return
   self.scanning=True
  threading.Thread(target=self.scan,daemon=True,name='umbra-launcher-scan').start()
 def view(self):
  with self.lock:
   if not self.scanned and not self.scanning:self.refresh()
   return {'supported':self.system=='Windows','scanning':self.scanning,'error':self.scan_error,'hotkeys':[{'id':i,'name':n,'category':c,'keys':'+'.join(keys) if keys else 'Windows LockWorkStation','icon':icon,'note':CONTEXT.get(i,'Windows 11 shortcut; may be intercepted by focused apps or policy.')} for i,n,c,keys,icon in HOTKEYS],'apps':[{'id':i,'name':n,'installed':i in self.records,'icon':i in self.icons,'method':self.records[i]['kind'] if i in self.records else None} for i,(n,_) in APPS.items()]}
 def image(self,ident):
  with self.lock:return self.icons.get(ident)
 def command(self,owner,request_id,kind,ident):
  if not isinstance(request_id,str) or not re.fullmatch(r'[A-Za-z0-9_-]{8,80}',request_id):raise ValueError('Valid requestId required')
  if not isinstance(ident,str) or kind not in ('hotkey','launch'):raise ValueError('Unknown Windows command')
  fingerprint=(kind,ident);now=self.clock();key=(owner,request_id)
  with self.lock:
   self.receipts={k:v for k,v in self.receipts.items() if now-v[0]<120}
   if key in self.receipts:
    _,prior,result=self.receipts[key]
    if prior!=fingerprint:raise ValueError('Request ID reused for a different command')
    return {**result,'duplicate':True}
   if self.system!='Windows':raise ValueError('Windows command unavailable on this host')
   if kind=='hotkey':
    spec=next((s for s in HOTKEYS if s[0]==ident),None)
    if not spec:raise ValueError('Unknown predefined Windows hotkey')
    if ident=='lock':
     import ctypes
     if not ctypes.windll.user32.LockWorkStation():raise OSError('Windows rejected LockWorkStation')
    else:
     keys=spec[3]
     try:self.pg.hotkey(*keys) if len(keys)>1 else self.pg.press(keys[0])
     finally:
      for key_name in reversed(keys):self.pg.keyUp(key_name)
    result={'message':spec[1]+' sent; effect depends on Windows focus and policy','status':'sent'}
   else:
    row=self.records.get(ident)
    if not row:raise ValueError('Application not discovered. Install it or refresh Windows Start menu discovery.')
    if not self.validate(row):raise ValueError('Application moved or its launch target is unavailable; refresh discovery')
    self.launch(row);result={'message':APPS[ident][0]+' launch requested; Windows owns startup or existing-instance activation','status':'requested'}
   if len(self.receipts)>=256:self.receipts.pop(next(iter(self.receipts)))
   self.receipts[key]=(now,fingerprint,result);return result
