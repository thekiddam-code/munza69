/* Nonmutating structural checks. Optional old domains remain migratable. */
(function(root){'use strict';
const object=x=>!!x&&typeof x==='object'&&!Array.isArray(x),array=Array.isArray,finiteMap=x=>object(x)&&Object.values(x).every(n=>Number.isFinite(n)&&n>=-1e-7);
function valid(s,requireModern=false){
 if(!object(s)||!array(s.crew)||!Number.isFinite(s.tick)||s.tick<0||!Number.isInteger(s.episode)||s.episode<1)return false;
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
