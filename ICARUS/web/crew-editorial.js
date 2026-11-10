/* Descriptions of actual interaction, not invented spoken quotations or beliefs. */
(function(root){'use strict';
function interaction(s,p,q,a,b,topic,fact){const room=root.ICARUSSpatial.position(p).room,prior=a.memories.find(m=>m.peer===q.name),roles=p.job===q.job?'their shared '+p.job+' duties':p.job+' and '+q.job+' routines';
 if(topic==='report')return p.name+' shared a '+Math.round(fact.confidence*100)+'%-confidence report with '+q.name+': '+fact.text.slice(0,180);
 const variation=(a.memories.length+b.memories.length)%3;
 if(topic==='support')return p.name+' and '+q.name+' paused together in '+room+' while '+(p.stress>45?p.name:q.name)+' was under recorded stress.';
 return p.name+' and '+q.name+(variation===0?' took a shared break in '+room:variation===1?' made time for a conversation between '+roles:' paused their current routines together in '+room)+(prior?' after an earlier recorded interaction.':'.');
}
function disputeSignature(s,a,b,label,context){const K=root.ICARUSKnowledge,shared=(K?.view(s,a.name)||[]).filter(f=>!f.legacy&&f.disclosure!=='private'&&['research','medical','mission','death','recovery','observation'].includes(f.kind)&&K.known(s,b.name,f.id)).at(-1);return [label,context,shared?.sourceId||'existing relationship'].join('|');}
function permitted(s,a,b,label,context){const key=[a.name,b.name].sort().join('|')+'|'+label,signature=disputeSignature(s,a,b,label,context),prior=s.conflict?.considered?.[key];return (!prior||prior.signature!==signature&&s.tick-prior.at>=1440)?{key,signature}:null;}
const api={interaction,permitted};if(typeof module==='object'&&module.exports){root.ICARUSSpatial=require('./spatial');root.ICARUSKnowledge=require('./knowledge');module.exports=api;}else root.ICARUSCrewEditorial=api;
})(globalThis);
