/* Same-world host fencing. Companions never execute the simulation bootstrap. */
(function(root){'use strict';
const local=['127.0.0.1','localhost','[::1]'].includes(location.hostname);
let instance=crypto.randomUUID?.()||Math.random().toString(36).slice(2)+Date.now();
try{instance=sessionStorage.getItem('icarus-host-instance-v2')||instance;sessionStorage.setItem('icarus-host-instance-v2',instance);}catch{}
let active=false,standalone=false,key='',generation=0,boot='',deadline=0,lost=false;
let verified=false,lastError=null,claimRequested=false,claimPromise=null;
async function request(path,payload){const r=await fetch('/api/icarus/'+path,{method:payload?'POST':'GET',headers:{'X-Icarus-Key':key,'X-Icarus-Instance':instance,'X-Icarus-Generation':String(generation),...(payload?{'Content-Type':'application/json'}:{})},...(payload?{body:JSON.stringify(payload)}:{}),signal:AbortSignal.timeout(5000)});const d=await r.json().catch(()=>({}));if(!r.ok){const e=Error(d.error||'HTTP '+r.status);e.status=r.status;throw e;}return d;}
function credentials(detail){verified=true;root.ICARUSBoot?.stage('authorization','ready',detail);}
const ready=(async()=>{
 if(location.protocol==='file:'){location.replace('http://127.0.0.1:8765/host.html');throw Error('Use the Windows server host launcher');}
 try{const b=await request('bootstrap');key=b.key;credentials('Local bootstrap key verified; remote terminals still require pairing');return true;}
 catch(e){
  if(e.status===404&&local){standalone=true;active=true;return true;}
  if(e.status===403||!local&&e.status===404){location.replace('/?terminal=icarus');throw Error('Remote terminal only');}
  // A separately verified key may have succeeded while bootstrap was pending.
  if(verified)return true;lastError=e.message;return false;
 }
})();
async function acquire(){
 claimRequested=true;
 if(standalone||lost||!verified||!root.ICARUSDurable?.canWrite())return;
 if(claimPromise)return claimPromise;
 root.ICARUSBoot?.stage('writer','waiting','Waiting for the protected server writer lease');
 claimPromise=(async()=>{try{const lease=await request('host/claim',{instance});generation=lease.generation;boot=lease.boot;renewed();}catch(e){failed(e);}finally{claimPromise=null;}})();
 return claimPromise;
}
function canWrite(){return !lost&&(standalone||active&&performance.now()<deadline);}
function renewed(){active=true;lastError=null;deadline=performance.now()+7000;root.ICARUSBoot?.stage('connection','ready','Companion server responded');root.ICARUSBoot?.stage('writer','ready','Server lease and exclusive storage ownership confirmed');}
function failed(e){
 active=false;lastError=e.message;
 // Initial contention is a wait, not loss of a generation we never owned.
 // Once a generation has been held, a conflict remains fenced until reload.
 if(e.status===409&&generation>0)lost=true;
 if(e.status===403){verified=false;root.ICARUSBoot?.stage('authorization','failed',e.message);}
 root.ICARUSBoot?.stage('connection',e.status===409||e.status===425?'ready':'degraded',e.status===409||e.status===425?'Companion reachable; writer not acquired':e.message);
 root.ICARUSBoot?.stage('writer',lost?'failed':'waiting',e.message+(lost?' · Reload to restore the current voyage before retrying ownership':''));
}
async function authorize(candidate){
 try{
  if(!candidate)throw Error('Enter the host key from the Windows server');
  const r=await fetch('/api/icarus/host/auth',{headers:{'X-Icarus-Key':candidate},signal:AbortSignal.timeout(5000)});
  if(!r.ok)throw Error(r.status===403?'Authorization rejected; no writer access granted':'Authentication service unavailable (HTTP '+r.status+')');
  const d=await r.json();if(d.authorized!==true)throw Error('Server did not confirm authorization');
  key=candidate;sessionStorage.setItem('icarusHostKey',candidate);credentials('Host key verified independently of writer ownership');
  root.ICARUSBoot?.stage('connection','ready','Authorization service responded');
  if(!canWrite()&&root.ICARUSDurable?.canWrite()&&!lost)await acquire();return d;
 }catch(e){if(!verified)root.ICARUSBoot?.stage('authorization','failed',e.message);throw e;}
}
root.ICARUSHost={ready,acquire,request,authorize,canWrite,renewed,failed,get credentialVerified(){return verified;},get lastError(){return lastError;},get standalone(){return standalone;},get lost(){return lost;},get generation(){return generation;},get instance(){return instance;},get session(){return boot+':'+generation;}};
root.ICARUSBoot?.stage('connection','pending','Host transport loaded; awaiting companion bootstrap');
ready.then(ok=>root.ICARUSBoot?.stage('connection',ok?'ready':'failed',ok?(standalone?'Local static development server; no companion authority':'Companion bootstrap responded'):lastError||'Host transport unavailable; check server/address'));
let heartbeatBusy=false;
setInterval(async()=>{
 if(lost||heartbeatBusy)return;
 if(!generation){
  // Retry only the initial claim, with the SAME identity, through both original
  // protections. Never acquire storage, expire another lease or resume a lost host.
  if(claimRequested&&verified&&root.ICARUSDurable?.canWrite())await acquire();
  return;
 }
 heartbeatBusy=true;try{await request('host/heartbeat',{});renewed();}catch(e){failed(e);}finally{heartbeatBusy=false;}
},2000);
})(globalThis);
