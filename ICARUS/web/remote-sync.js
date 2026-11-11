/* Authenticated SSE terminal: read-only telemetry and separate idempotent commands. */
(function(root){'use strict';
function connect({token,data,state}){let stop=false,controller=null,last=null,received=0,failures=0,supported=false;
 const report=(label)=>state?.(label,last);
 async function run(){while(!stop){controller=new AbortController();try{const r=await fetch('/api/icarus/events',{headers:{Authorization:'Bearer '+token()},signal:controller.signal});if(r.status===404)return;if(!r.ok)throw Error('Connection rejected: '+r.status);supported=true;failures=0;const reader=r.body.getReader(),decode=new TextDecoder();let buffer='';
  while(!stop){const part=await reader.read();if(part.done)break;buffer+=decode.decode(part.value,{stream:true});if(buffer.length>150000)throw Error('Telemetry frame too large');let end;
   while((end=buffer.indexOf('\n\n'))>=0){const event=buffer.slice(0,end);buffer=buffer.slice(end+2);const payload=event.split('\n').filter(x=>x.startsWith('data: ')).map(x=>x.slice(6)).join('\n');if(!payload)continue;const d=JSON.parse(payload);last=d;received=performance.now();data(d);report(d.state);}
  }
 }catch(e){if(stop)break;report(last?'RECONNECTING':'HOST OFFLINE');}if(!stop)await new Promise(resolve=>setTimeout(resolve,Math.min(8000,1000*2**failures++)));}}
 const offline=()=>{controller?.abort();report(last?'RECONNECTING':'HOST OFFLINE');};addEventListener('offline',offline);
 const watchdog=setInterval(()=>{if(last&&performance.now()-received>8000)report('RECONNECTING');},1000);run();return {close(){stop=true;controller?.abort();clearInterval(watchdog);removeEventListener('offline',offline);},get supported(){return supported;},get last(){return last;}};
}
async function command(token,command,requestId=(root.crypto?.randomUUID?.()||Date.now().toString(36)+'-'+Math.random().toString(36).slice(2))){const r=await fetch('/api/icarus/dispatch',{method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:JSON.stringify({command,requestId}),signal:AbortSignal.timeout(8000)});const d=await r.json();if(!r.ok)throw Error(d.error||'Command rejected');return d;}
root.ICARUSRemoteSync={connect,command};
})(globalThis);
