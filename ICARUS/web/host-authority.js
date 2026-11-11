/* Same-world host fencing. Companions never execute the simulation bootstrap. */
(function(root){'use strict';
const local=['127.0.0.1','localhost','[::1]'].includes(location.hostname),instance=crypto.randomUUID?.()||Math.random().toString(36).slice(2)+Date.now();let active=false,standalone=false,key='',generation=0,deadline=0,lost=false;
async function request(path,payload){const r=await fetch('/api/icarus/'+path,{method:payload?'POST':'GET',headers:{'X-Icarus-Key':key,'X-Icarus-Instance':instance,'X-Icarus-Generation':String(generation),...(payload?{'Content-Type':'application/json'}:{})},...(payload?{body:JSON.stringify(payload)}:{}),signal:AbortSignal.timeout(5000)});const d=await r.json().catch(()=>({}));if(!r.ok){const e=Error(d.error||'HTTP '+r.status);e.status=r.status;throw e;}return d;}
const ready=(async()=>{if(!local){location.replace(location.protocol==='file:'?'http://127.0.0.1:8765/icarus.html':'/?terminal=icarus');throw Error('Remote terminal only; open UMBRA, not a simulation');}
 try{const b=await request('bootstrap');key=b.key;return true;}catch(e){if(e.status===404){standalone=true;active=true;return true;}if(e.status===409)lost=true;return false;}})();
async function acquire(){if(standalone||lost)return;try{const lease=await request('host/claim',{instance});generation=lease.generation;renewed();}catch(e){failed(e);}}
function canWrite(){return !lost&&(standalone||active&&performance.now()<deadline);}
function renewed(){active=true;deadline=performance.now()+7000;}
function failed(e){active=false;if(e.status===409)lost=true;}
root.ICARUSHost={ready,acquire,request,canWrite,renewed,failed,get standalone(){return standalone;},get lost(){return lost;},get generation(){return generation;},get instance(){return instance;}};
let heartbeatBusy=false;setInterval(async()=>{if(!generation||lost||heartbeatBusy)return;heartbeatBusy=true;try{await request('host/heartbeat',{});renewed();}catch(e){failed(e);}finally{heartbeatBusy=false;}},2000);
})(globalThis);
