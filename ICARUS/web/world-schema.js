/* Nonmutating structural checks. Optional old domains remain migratable. */
(function(root){'use strict';
const object=x=>!!x&&typeof x==='object'&&!Array.isArray(x),array=Array.isArray,finiteMap=x=>object(x)&&Object.values(x).every(n=>Number.isFinite(n)&&n>=-1e-7);
function valid(s,requireModern=false,requireAnthology=false,requireUnified=false){
 if(!object(s)||!array(s.crew)||!Number.isFinite(s.tick)||s.tick<0||!Number.isInteger(s.episode)||s.episode<1)return false;
 if(requireAnthology&&s.anthology===undefined)return false;
 if(requireUnified&&!s.unifiedWorld)return false;
 if(s.knowledge!==undefined&&s.knowledge!==null){const k=s.knowledge;if(!object(k)||k.version!==1||!object(k.facts)||!object(k.byKey)||!object(k.actors)||!array(k.messages)||!Number.isInteger(k.nextFact)||k.nextFact<1||!Number.isInteger(k.nextMessage)||k.nextMessage<1)return false;for(const [id,f] of Object.entries(k.facts))if(!object(f)||f.id!==id||typeof f.sourceId!=='string'||typeof f.text!=='string'||!Number.isFinite(f.confidence)||f.confidence<0||f.confidence>1)return false;for(const a of Object.values(k.actors)){if(!object(a)||!object(a.entries))return false;for(const [id,e] of Object.entries(a.entries))if(!k.facts[id]||!object(e)||e.sourceId!==k.facts[id].sourceId||!Number.isFinite(e.acquiredAt)||e.acquiredAt<0||e.acquiredAt>s.tick)return false;}for(const m of k.messages)if(!object(m)||!k.facts[m.factId]||!['pending','delivered'].includes(m.status)||typeof m.from!=='string'||typeof m.to!=='string')return false;}

 if(s.calendar!==undefined&&s.calendar!==null){const c=s.calendar;if(!object(c)||c.version!==1||c.mode!=='wall'||typeof c.timeZone!=='string'||!Number.isFinite(c.wallCursor)||!Number.isFinite(c.lastSeen)||!Number.isFinite(c.displayMs)||!Number.isFinite(c.carry)||c.carry<0||c.carry>=60000||!object(c.occurrences)||!object(c.visitedWeeks)||!array(c.pending)||!array(c.corrections)||!object(c.recovery)||!Number.isFinite(c.maxCatchupMs)||c.maxCatchupMs<1||c.maxCatchupMs>604800000)return false;try{new Intl.DateTimeFormat('en',{timeZone:c.timeZone}).format(0);}catch{return false;}}
 if(s.unifiedWorld!==undefined&&s.unifiedWorld!==null){const w=s.unifiedWorld;if(!object(w)||w.version!==1||!object(w.canon)||Object.values(w.canon).some(x=>typeof x!=='string'||x.length>6000)||!array(w.archives)||!object(w.items)||!object(w.preferences)||!object(w.military)||!object(w.organisms)||!object(w.infections)||!Number.isFinite(w.military.reservePower)||w.military.reservePower<0||!array(w.military.visited)||!object(w.military.doors)||!object(w.seen))return false;for(const o of Object.values(w.organisms))if(!object(o)||typeof o.id!=='string'||!['adult','egg','spent egg','juvenile'].includes(o.stage)||typeof o.dormant!=='boolean')return false;}

 if(s.anthology!==undefined){const a=s.anthology;if(!object(a)||a.version!==1||!array(a.arcs)||!object(a.seen)||!array(a.traditions)||!object(a.config)||!Number.isFinite(a.config.frequency)||a.config.frequency<0||a.config.frequency>3||!finiteMap(a.config.weights)||a.arcs.some(r=>!object(r)||typeof r.id!=='string'||!array(r.sources)||!array(r.history)||!Number.isFinite(r.started)||!Number.isFinite(r.progress)))return false;}
 const domains=['entities','experiences','emergencyOps','chronicles'],modern=requireModern||domains.some(k=>s[k]!==undefined);
 if(!modern)return true;
 if(domains.some(k=>!object(s[k])||s[k].version!==1))return false;
 const e=s.entities,m=s.experiences,o=s.emergencyOps,c=s.chronicles;
 if(!object(e.registry)||!array(e.encounters)||!array(e.organizations)||!object(e.stats)||!array(m.records)||!object(m.seen)||!object(m.assessments)||!array(o.incidents)||!object(o.transport)||!Number.isFinite(o.transport.condition)||!object(o.stats)||!object(c.weeks)||!object(c.seen))return false;
 for(const [id,n] of Object.entries(e.registry))if(!object(n)||id!==n.id||typeof n.name!=='string'||typeof n.location!=='string'||!Number.isFinite(n.reputation)||!finiteMap(n.stock)||!finiteMap(n.initial)||!finiteMap(n.received)||!finiteMap(n.spent)||!array(n.crew)||!array(n.history))return false;
 for(const w of Object.values(c.weeks))if(!object(w)||!array(w.sourceIds)||!array(w.segments))return false;
 for(const r of m.records)if(!object(r)||typeof r.id!=='string'||typeof r.sourceId!=='string'||typeof r.person!=='string')return false;
 if(!object(s.navigation)||!object(s.navigation.position)||!Number.isFinite(s.navigation.position.x)||!Number.isFinite(s.navigation.position.y)||!['orbit','transit','drift'].includes(s.navigation.phase))return false;
 if(!object(s.universe?.systems)||!array(s.frontier?.jobs)||!array(s.logistics?.receipts)||!finiteMap(s.economy?.stock)||!finiteMap(s.economy?.feedstock))return false;
 return true;
}
const api={valid};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSWorldSchema=api;
})(globalThis);
