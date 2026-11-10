/* Per-actor evidence, not omniscient world state. All channels are local simulation callbacks. */
(function(root){'use strict';
const clamp=x=>Math.max(0,Math.min(1,Number.isFinite(x)?x:.6));
function init(s){
 if(s.knowledge)return s.knowledge;
 const k=s.knowledge={version:1,nextFact:1,nextMessage:1,facts:{},byKey:{},actors:{SOL:{entries:{}}},messages:[],lastTick:-1,stats:{observed:0,delivered:0,blocked:0},migration:{at:s.tick,legacyPublished:0}};
 for(const p of s.crew||[])k.actors[p.name]={entries:{}};
 // Existing published archives are legitimate legacy records, not reconstructed witnesses.
 for(const a of s.unifiedWorld?.archives||[]){if(!a.sourceId)continue;const f={id:'FACT-'+k.nextFact++,key:'archive:'+a.id,sourceId:a.sourceId,text:a.text,kind:'recorded-evidence',at:a.at??s.tick,location:'ship-records',confidence:.6,disclosure:'shareable',data:{archiveId:a.id},legacy:true};k.facts[f.id]=f;k.byKey[f.key]=f.id;k.actors.SOL.entries[f.id]={sourceId:f.sourceId,acquiredAt:s.tick,observedAt:f.at,location:'ship-records',method:'legacy-published-record',confidence:.6,disclosure:'shareable',receivedFrom:null,deliveredAt:s.tick};a.knowledgeId=f.id;k.migration.legacyPublished++;}
 for(const [loc,w] of [['asteroid',s.asteroidExploration],['derelict',s.remoteExploration]])for(const room of w?.rooms||[])if(room.known||room.visited){const f={id:'FACT-'+k.nextFact++,key:'legacy-map:'+loc+':'+room.id,sourceId:'LEGACY-CHART:'+loc+':'+room.id,text:'Existing chart: '+room.name,kind:'recorded-evidence',at:s.tick,location:'ship-records',confidence:.6,disclosure:'shareable',legacy:true,data:{map:{location:loc,cell:room.id,name:room.name,visited:!!room.visited,blocked:!!room.blocked,hazard:room.hazard||null}}};k.facts[f.id]=f;k.byKey[f.key]=f.id;k.actors.SOL.entries[f.id]={sourceId:f.sourceId,acquiredAt:s.tick,observedAt:s.tick,location:'ship-records',method:'legacy-chart',confidence:.6,disclosure:'shareable',receivedFrom:null,deliveredAt:s.tick};}
 return k;
}
function actor(s,name){if(name==='SOL')return {name,sol:true};return (s.crew||[]).find(p=>p.name===name&&(p.vitals?.health??100)>0)||Object.values(s.entities?.registry||{}).find(p=>'NPC:'+p.id===name)||null;}
function position(s,name){const p=actor(s,name);if(!p)return null;if(p.sol)return {domain:'ship',node:'SOL',stationary:true};if(name.startsWith('NPC:'))return {domain:'contact:'+p.location,node:p.id,stationary:true};
 if(p.expeditionAway){const loc=p.expeditionAway,m=s.remoteCore?.missions?.[loc]||s.remoteCore?.missions?.frontier;if(!m||m.phase!=='onsite')return {domain:'transit:'+loc,node:null,stationary:false};const w=loc==='asteroid'?s.asteroidExploration:loc==='derelict'?s.remoteExploration:null;return {domain:loc,node:p.fieldPosition??w?.position??('mission:'+m.id),stationary:true};}
 return {domain:'ship',node:p.nav?.at||'R:'+p.room,stationary:!p.route?.length};
}
function entry(s,name,id){return s.knowledge?.actors[name]?.entries[id]||null;}
function known(s,name,id){return !!entry(s,name,id);}
function learn(s,name,f,method,from=null,at=s.tick){const k=init(s);if(!actor(s,name)||known(s,name,f.id))return false;const a=k.actors[name]||(k.actors[name]={entries:{}});a.lastPosition=position(s,name);a.entries[f.id]={sourceId:f.sourceId,acquiredAt:at,observedAt:f.at,location:position(s,name),method,confidence:f.confidence,disclosure:f.disclosure,receivedFrom:from,deliveredAt:from?at:null};return true;}
function observe(s,source,witnesses,options={}){
 const k=init(s),canonical=(s.chronicle?.records||[]).find(x=>x.id===source?.id);if(!canonical||canonical.message!==source.message||canonical.data?.creatorAuthored||options.method==='creator-canon')return null;
 const valid=[...new Set(witnesses||[])].filter(name=>{const p=position(s,name);if(!p)return false;if(options.location)return p.domain===options.location.domain&&(options.location.node===undefined||p.node===options.location.node);return true;});if(!valid.length)return null;
 const key=options.key||source.id;let f=k.facts[k.byKey[key]];
 if(!f){f={id:'FACT-'+k.nextFact++,key,sourceId:source.id,text:source.message,kind:options.kind||'observation',at:s.tick,location:options.location||position(s,valid[0]),confidence:clamp(options.confidence),disclosure:options.disclosure||'shareable',data:JSON.parse(JSON.stringify(options.data||source.data||{}))};k.facts[f.id]=f;k.byKey[key]=f.id;k.stats.observed++;}
 for(const n of valid)learn(s,n,f,options.method||'direct-observation');return f;
}
function can(s,from,to,channel,env={}){const a=position(s,from),b=position(s,to);if(!a||!b)return false;
 if(channel==='conversation')return a.domain===b.domain&&a.node!==null&&a.node===b.node&&a.stationary&&b.stationary&&!['SOL'].includes(from)&&to!=='SOL';
 if(channel==='debrief')return a.domain==='ship'&&b.domain==='ship'&&a.stationary&&b.stationary&&env.recordsAvailable?.(from,to)!==false;
 if(channel==='radio')return env.radio?.(from,to,a,b)===true;
 return false;
}
function queue(s,from,to,id,channel='radio',options={}){const k=init(s),f=k.facts[id];if(!f||!known(s,from,id)||!actor(s,from)||!actor(s,to)||known(s,to,id)||f.disclosure==='private'&&!options.consent)return null;let m=k.messages.find(x=>x.factId===id&&x.from===from&&x.to===to&&x.channel===channel&&x.status==='pending');if(m)return m;m={id:'MSG-'+k.nextMessage++,factId:id,from,to,channel,queuedAt:s.tick,transmittedAt:null,deliveredAt:null,status:'pending',lastAttempt:-1,blockedReason:null};k.messages.push(m);return m;}
function deliver(s,m,env){const k=init(s);if(m.status!=='pending'||!can(s,m.from,m.to,m.channel,env))return false;const f=k.facts[m.factId];m.transmittedAt=s.tick;m.deliveredAt=s.tick;m.status='delivered';m.blockedReason=null;if(learn(s,m.to,f,m.channel==='conversation'?'overheard-report':m.channel==='debrief'?'recorded-evidence':'received-report',m.from)){const e=entry(s,m.to,f.id);e.transmittedAt=m.transmittedAt;k.stats.delivered++;env.delivered?.(m,f);}return true;}
function tick(s,env={}){const k=init(s);if(k.lastTick===s.tick)return 0;k.lastTick=s.tick;for(const name of Object.keys(k.actors)){const p=position(s,name);if(p)k.actors[name].lastPosition=p;}let delivered=0;
 for(const m of k.messages){if(m.status!=='pending'||m.lastAttempt===s.tick)continue;m.lastAttempt=s.tick;if(!actor(s,m.from)||!actor(s,m.to)){m.blockedReason='actor unavailable; record remains with its carrier';continue;}if(!can(s,m.from,m.to,m.channel,env)){m.blockedReason='physical channel or equipment unavailable';continue;}if(delivered>=8)break;if(deliver(s,m,env))delivered++;}
 if(k.messages.length>256)k.messages=k.messages.filter(x=>x.status==='pending').concat(k.messages.filter(x=>x.status!=='pending').slice(-128));return delivered;
}
function debrief(s,name,env={}){if(!can(s,name,'SOL','debrief',env))return 0;let n=0;for(const f of view(s,name)){if(f.disclosure==='private'||known(s,'SOL',f.id))continue;const m=queue(s,name,'SOL',f.id,'debrief');if(m&&deliver(s,m,env))n++;}return n;}

function read(s,name,id,env={}){const f=s.knowledge?.facts[id];if(!f||!known(s,'SOL',id)||f.disclosure==='private'||!can(s,name,'SOL','debrief',env))return false;return learn(s,name,f,'recorded-evidence','SOL');}
function recover(s,deadName,reader,env={}){const dead=(s.living?.deceased||[]).find(p=>p.name===deadName),p=actor(s,reader);if(!dead?.crew||!p)return 0;const carrier=dead.crew,a=position(s,reader),loc=carrier.expeditionAway,world=loc==='asteroid'?s.asteroidExploration:loc==='derelict'?s.remoteExploration:null;const node=loc?(carrier.fieldPosition??dead.fieldPosition??s.knowledge?.actors[deadName]?.lastPosition?.node??null):(carrier.nav?.at||'R:'+carrier.room);if(node===null||!a?.stationary||a.domain!==(loc||'ship')||a.node!==node)return 0;let n=0;
 for(const id of Object.keys(s.knowledge?.actors[deadName]?.entries||{})){const f=s.knowledge.facts[id];if(learn(s,reader,f,'recovered-record',deadName)){n++;env.recovered?.(f,reader,deadName);}}return n;
}
function infer(s,name,source,premises,text,confidence=.4){if(!premises?.length||premises.some(id=>!known(s,name,id)))return null;return observe(s,source,[name],{kind:'inference',method:'inference',confidence:Math.min(clamp(confidence),...premises.map(id=>entry(s,name,id).confidence)),data:{premises,text},disclosure:'private'});}
function view(s,name){const k=s.knowledge,a=k?.actors[name];if(!a)return [];return Object.entries(a.entries).map(([id,e])=>({...k.facts[id],acquisition:{...e}}));}
function mapCell(s,name,loc,id){return view(s,name).reverse().find(f=>f.data?.map?.location===loc&&f.data.map.cell===id)?.data.map||null;}
function audit(s){const k=s.knowledge;if(!k)return [];const errors=[];for(const [name,a] of Object.entries(k.actors))for(const [id,e] of Object.entries(a.entries))if(!k.facts[id]||e.sourceId!==k.facts[id].sourceId||e.acquiredAt<0||e.acquiredAt>s.tick)errors.push('Invalid knowledge '+name+'/'+id);for(const m of k.messages)if(!k.facts[m.factId]||!known(s,m.from,m.factId))errors.push('Unfounded transmission '+m.id);return errors;}
const api={init,actor,position,observe,entry,known,queue,tick,debrief,can,read,recover,infer,view,mapCell,audit};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSKnowledge=api;
})(globalThis);
