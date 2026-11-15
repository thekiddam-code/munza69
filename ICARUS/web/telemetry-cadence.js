/* Preview scheduling only; commands and lease heartbeats do not wait for a preview. */
(function(root){'use strict';
function create(clock=()=>performance.now()){let at=-Infinity,wasCatchup=false,retryAt=0,failures=0,packet=null,packetKey=null,generated=-Infinity;return {
 due(catchup){const now=clock(),ending=wasCatchup&&!catchup;wasCatchup=catchup;return now>=retryAt&&(ending||now-at>=(catchup?3000:1100));},
 prepare(key,build){const now=clock();at=now;if(packet&&packetKey===key&&now-generated<5000)return packet;packet=build();packetKey=key;generated=now;return packet;},
 success(){failures=0;retryAt=0;},failure(){packet=null;failures++;retryAt=clock()+Math.min(15000,1200*2**Math.min(failures,4));},
 get status(){return {failures,retryInMs:Math.max(0,retryAt-clock()),cached:!!packet};}};}
const api={create};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSTelemetryCadence=api;
})(globalThis);
