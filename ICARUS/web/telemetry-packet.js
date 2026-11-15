/* Bounded disposable wire previews, never world/save mutation or permission changes. */
(function(root){'use strict';
const bytes=x=>new TextEncoder().encode(JSON.stringify(x)).length;
function prepare(payload,limit=110000){
 const packet=JSON.parse(JSON.stringify(payload));for(const c of packet.telemetry?.exploration?.records||[])if(c.motion){c.motionAvailable=true;delete c.motion;c.framesDeferred=true;}if(bytes(packet)<=limit)return packet;
 const telemetry=packet.telemetry||{},counts={images:0,frames:0,records:0};
 const metadata={version:1,limited:true,policy:'Bounded remote preview; complete history and captured recordings remain on the authoritative host',omitted:counts};telemetry.transport=metadata;
 function fits(){return bytes(packet)<=limit;}
 const images=[];for(const group of [telemetry.exploration?.records,telemetry.expeditions?.records])for(const c of group||[])for(const f of c.frames||[])if(f.image)images.push(f);
 const retainedImage=images.at(-1);
 function omitImage(f){delete f.image;f.presentation='SOURCE-STATE RECONSTRUCTION · captured pixels deferred from this telemetry preview';counts.images++;}
 for(const f of images){if(fits())return packet;if(f!==retainedImage)omitImage(f);}
 // Keep identities, live conditions, all known map sectors, commands and receipts.
 // Only reduce duplicated historical previews, in newest-first/oldest-first order as appropriate.
 function trim(holder,key,n,newestFirst=false){const a=holder?.[key];if(!Array.isArray(a)||a.length<=n)return;counts.records+=a.length-n;holder[key]=n===0?[]:newestFirst?a.slice(0,n):a.slice(-n);}
 for(const n of [3,2,1]){
  for(const person of telemetry.operations?.crew||[]){for(const key of ['reports','assessments','relationships','missions'])trim(person,key,n,['reports','assessments'].includes(key));}
  if(fits())return packet;trim(telemetry.operations,'situation',Math.max(2,n),true);trim(telemetry.operations,'missions',Math.max(2,n));trim(telemetry.operations,'research',Math.max(1,n));
  trim(telemetry.exploration,'history',Math.max(2,n));trim(telemetry.expeditions,'history',Math.max(2,n));
 }
 for(const group of [telemetry.exploration?.records,telemetry.expeditions?.records])for(const c of group||[]){if(fits())return packet;const frames=c.frames||[];if(frames.length>1){c.frameCount=c.frameCount||frames.length;counts.frames+=frames.length-1;c.frames=frames.includes(retainedImage)?[retainedImage]:frames.slice(-1);}}
 if(fits())return packet;
 if(retainedImage?.image)omitImage(retainedImage);
 if(fits())return packet;
 // If even bounded source-state evidence is too big, retain record provenance and
 // advertise that this packet is metadata-only; do not delete the actual recording.
 for(const group of [telemetry.exploration?.records,telemetry.expeditions?.records])for(const c of group||[]){if(fits())return packet;if(c.frames?.length){c.frameCount=c.frameCount||c.frames.length;counts.frames+=c.frames.length;c.frames=[];c.previewUnavailable='Preview deferred to the host; original recording is retained';}}
 if(fits())return packet;
 for(const person of telemetry.operations?.crew||[]){for(const key of ['reports','assessments','relationships','missions'])trim(person,key,0);person.previewLimited=true;}
 if(fits())return packet;
 const error=Error('Remote telemetry preview exceeds its '+limit+' byte budget ('+bytes(packet)+' bytes); saved voyage and recordings are unchanged');error.name='TelemetryPreviewError';throw error;
}
const api={prepare,bytes};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSTelemetryPacket=api;
})(globalThis);
