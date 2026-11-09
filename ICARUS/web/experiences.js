/* Event-linked individual memory; identity and base personality are never replaced. */
(function(root){'use strict';
function init(s){if(!s.experiences)s.experiences={version:1,nextId:1,records:[],seen:{},assessments:{}};for(const p of s.crew)if(!p.career)p.career={confidence:0,caution:0,memoryIds:[],rescues:0};return s.experiences;}
function remember(s,p,source,kind,peers=[]){const e=init(s),key=source+':'+p.name+':'+kind;if(e.seen[key])return null;e.seen[key]=true;const negative=['failure','injury','loss','stranded'].includes(kind),temper=(p.stress||0)/100,delta=negative?-(1+temper):.5+(p.mood||0)/200;
 const r={id:'MEM-'+e.nextId++,at:s.tick,sourceId:source,person:p.name,kind,peers:peers.filter(n=>n!==p.name),confidenceDelta:delta};e.records.push(r);p.career.memoryIds.push(r.id);p.career.confidence=Math.max(-20,Math.min(20,p.career.confidence+delta));p.career.caution=Math.max(0,Math.min(20,p.career.caution+(negative?1+temper:-.2)));if(kind==='rescued')p.career.rescues++;
 for(const name of r.peers)if(p.relationships&&s.crew.some(q=>q.name===name))p.relationships[name]=Math.max(-100,Math.min(100,(p.relationships[name]||0)+(kind==='rescued'?2:negative?-.3:.5)));
 e.assessments[p.name]={at:s.tick,evidenceCount:p.career.memoryIds.length,missionWillingness:Math.max(.4,Math.min(1.2,1+p.career.confidence*.01-p.career.caution*.015)),reason:'Recorded personal mission and emergency experience'};return r;}
function mission(s,job,kind){init(s);for(const name of job.members||[]){const p=s.crew.find(p=>p.name===name);if(p)remember(s,p,job.id,kind,job.members);}}
function willingness(p){return Math.max(.4,Math.min(1.2,1+(p.career?.confidence||0)*.01-(p.career?.caution||0)*.015));}
function audit(s){const e=init(s),ids=new Set(e.records.map(r=>r.id)),known=new Set([...s.crew.map(p=>p.name),...(s.living?.deceased||[]).map(p=>p.name)]);return e.records.filter(r=>!r.sourceId||!known.has(r.person)||!ids.has(r.id)).map(r=>'Invalid memory '+r.id);}
const api={init,remember,mission,willingness,audit};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSExperiences=api;
})(globalThis);
