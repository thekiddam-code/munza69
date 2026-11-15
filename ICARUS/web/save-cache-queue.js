/* Optional compatibility mirror only. Canonical IndexedDB commits never depend on this worker. */
(function(root){'use strict';
function create(options){const clock=options.clock||(()=>performance.now()),delay=options.delay??500;let worker=null,active=null,pending=null,timer=null,serial=0,disabled=false,waiters=[];const stats={requests:0,coalesced:0,completed:0,skipped:0,errors:0,pending:0,lastWorkerMs:0};
 function state(){stats.pending=Number(!!active)+Number(!!pending);options.onState?.({...stats});}
 function settle(){state();if(!active&&!pending){for(const ok of waiters)ok();waiters=[];}}
 function fail(error){disabled=true;clearTimeout(timer);timer=null;active=pending=null;worker?.terminate();worker=null;stats.errors++;options.onError?.(error);settle();}
 function start(){clearTimeout(timer);timer=null;if(active||!pending||disabled)return;active=pending;pending=null;try{if(!worker){worker=options.createWorker();worker.onmessage=e=>{if(!active||e.data?.id!==active.id)return;if(typeof e.data.encoded!=='string'||typeof active.context.previousRaw==='string'&&typeof e.data.previousEncoded!=='string'){fail(Error('Invalid compatibility-cache worker response'));return;}const job=active;active=null;stats.lastWorkerMs=Number(e.data.elapsedMs)||0;try{if(options.onEncoded(job.raw,e.data.encoded,e.data.previousEncoded,job.context)!==false)stats.completed++;else stats.skipped++;}catch(error){options.onError?.(error);stats.errors++;}if(pending)timer=setTimeout(start,delay);settle();};worker.onerror=e=>fail(Error(e.message||'Compatibility-cache worker failed'));}worker.postMessage({id:active.id,raw:active.raw,previousRaw:active.context.previousRaw});state();}catch(error){fail(error);}}
 function request(raw,context={}){stats.requests++;if(disabled)return false;if(pending)stats.coalesced++;pending={id:++serial,raw,context,at:clock()};clearTimeout(timer);timer=null;if(!active)timer=setTimeout(start,delay);state();return true;}
 function flush(){if(disabled||!active&&!pending)return Promise.resolve();const done=new Promise(ok=>waiters.push(ok));if(!active)start();return done;}
 function close(){clearTimeout(timer);worker?.terminate();active=pending=null;disabled=true;settle();}
 return {request,flush,close,stats};}
const api={create};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSSaveCacheQueue=api;
})(globalThis);
