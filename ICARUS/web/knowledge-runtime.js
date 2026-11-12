/* Adapter over existing radio, custody, maps and event recorder; no external I/O. */
(function(root){'use strict';
function create(getState,ctx){const K=root.ICARUSKnowledge;
 function radio(from,to,a,b){if(!ctx.radioHardware())return false;if(a.domain==='ship'&&b.domain==='ship')return true;const loc=a.domain==='ship'?b.domain:b.domain==='ship'?a.domain:null;return !!loc&&['DIRECT','RELAYED'].includes(ctx.signal(loc));}
 function recordsAvailable(from,to){const s=getState(),p=s.crew.find(p=>p.name===(from==='SOL'?to:from));return !!p&&!p.expeditionAway&&!p.route?.length&&['C01','C02','A01','A02','B01','B02','B05','B06','B10'].includes(p.room)&&K.position(s,p.name)?.node==='R:'+p.room&&ctx.radioHardware();}
 function delivered(m,f){if(m.to!=='SOL')return;const s=getState();if(!f.publicationSourceId){const r=ctx.publish('Received '+(f.kind==='reported-claim'?'UNVERIFIED CLAIM via ':f.kind==='inference'?'INFERENCE via ':'')+m.channel+' report from '+m.from+': '+f.text,f.kind==='inference'?'observation':f.kind,{...f.data,privateKnowledge:false,knowledgeDelivery:true,sourceFactId:f.id,observedSourceId:f.sourceId,observedAt:f.at,confidence:f.confidence,receivedFrom:m.from},f.witnesses||[]);f.publicationSourceId=r?.id||null;}
  if(f.data.map){s.knowledge.contacts=s.knowledge.contacts||{};s.knowledge.contacts[f.data.map.location]={...f.data.map,observedAt:f.at,receivedAt:s.tick,sourceId:f.publicationSourceId||f.sourceId};}
 }
 function learned(name,f){root.ICARUSCrewCommunications?.review(getState(),name,f);if(f.kind==='death'&&f.data.deceased)ctx.grieve?.(name,f.data.deceased,f.sourceId);}
 function env(){return {radio,recordsAvailable,delivered,learned};}
 function event(kind,text,people=[],data={},options={}){const s=getState();K.init(s);const living=people.filter(n=>K.actor(s,n)),location=options.location||(living.length?K.position(s,living[0]):null);const witnesses=location?living.filter(n=>{const p=K.position(s,n);return p&&p.domain===location.domain&&p.node===location.node;}):[];
  const r=ctx.localRecord(kind,text,witnesses,{...data,privateKnowledge:true});if(!witnesses.length)return r;const f=K.observe(s,r,witnesses,{...options,location,data,confidence:options.confidence??(data.uncertain?.45:.75),learned});if(f){for(const name of witnesses)K.queue(s,name,'SOL',f.id,'radio');}return r;
 }
 function cell(loc,room,m){const s=getState(),people=(m.members||[m.crew]).filter(n=>K.position(s,n)?.domain===loc),map={location:loc,cell:room.id,name:room.name,visited:true,blocked:!!room.blocked,hazard:room.hazard||null};const r=event('observation','Field observation: '+room.name,people,{map,missionId:m.id},{location:{domain:loc,node:room.id},key:'cell:'+loc+':'+room.id+':'+m.id+':'+s.tick});for(const id of ctx.obstructions?.(loc,room.id)||[]){if(people.every(n=>K.mapCell(s,n,loc,id)?.blocked))continue;event('observation','A local survey documented an obstructed adjacent passage.',people,{map:{location:loc,cell:id,name:'Obstructed passage',visited:false,blocked:true,hazard:null},fromCell:room.id,missionId:m.id},{location:{domain:loc,node:room.id},key:'barrier:'+loc+':'+id+':'+m.id});}return r;}
 function unread(s,from,to){const k=s.knowledge,id=Object.keys(k.actors[from]?.entries||{}).find(id=>k.facts[id]?.disclosure!=='private'&&!K.known(s,to,id));return k.facts[id]||null;}
 function tick(){const s=getState();K.init(s);ctx.sensors?.();if(s.tick%5===0){for(const p of s.crew){if(p.interaction!=='working'||!/review|research|record|analyz|experiment/i.test(p.task||''))continue;const f=unread(s,'SOL',p.name);if(f)K.read(s,p.name,f.id,env());}}if(s.tick%30===0){for(const p of s.crew){if(p.expeditionAway||p.emergencyId||p.researchAssignment||p.maintenanceRoom||!/socializ|conversation|meeting|talk/i.test(p.task||''))continue;const a=K.position(s,p.name);for(const q of s.crew){if(q===p||!K.can(s,p.name,q.name,'conversation',env()))continue;const f=unread(s,p.name,q.name);if(f){K.queue(s,p.name,q.name,f.id,'conversation');break;}}}}return K.tick(s,env());}
 function debrief(m){const s=getState();for(const name of m.members||[m.crew])K.debrief(s,name,env());}
 function findingKnown(f){const s=getState();if(f.knowledgeId)return K.known(s,'SOL',f.knowledgeId);const c=(s.specimenCustody?.items||[]).find(x=>x.id===f.custodyId||x.name===f.item);return !!c&&!c.concealed&&c.status!=='field secured';}
 function knownMap(loc,id,actor='SOL'){return K.mapCell(getState(),actor,loc,id);}
 return {event,cell,tick,debrief,env,findingKnown,knownMap};
}
root.ICARUSKnowledgeRuntime={create};
})(globalThis);
