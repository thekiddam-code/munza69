/* Staged field objectives layered over existing transport/custody manifests. */
(function(root){'use strict';
function profile(op,d){const teamSize=op.risk>.68?4:op.resource||op.risk>.4?3:2;return {teamSize,loadout:{tools:op.resource?2:1,spares:2,...(op.type==='survey'?{lab:.5}:{}),...(op.type==='distress'?{medical:.25}:{})},distance:d.landingDistance??25,stages:[{id:'assess',end:30},{id:'objective',end:op.duration+30},{id:'secure',end:op.duration+60}],duration:op.duration+60};}
function attach(m,job,p){m.plan={version:1,stage:0,stages:p.stages,history:[],distance:p.distance,loadout:{...p.loadout},kitCondition:100,exposure:0};job.stages=p.stages;job.duration=p.duration;}
function advance(s,m,job,d,env){if(!m.plan)return;const p=m.plan;p.exposure+=(d.observedHazard||d.hazard||0)*.01;p.kitCondition=Math.max(0,p.kitCondition-.005);while(p.stage<p.stages.length&&m.fieldProgress>=p.stages[p.stage].end){const stage=p.stages[p.stage++];p.history.push({stage:stage.id,at:s.tick,progress:m.fieldProgress});if(env.emit)env.emit('expedition_stage',job.id+' completed field stage '+stage.id+'.',{missionId:job.id,stage:stage.id});}
 if(p.exposure>1&&s.tick%120===0){const names=m.members.filter(n=>s.crew.some(q=>q.name===n)),name=names[Math.floor(env.random()*names.length)],person=s.crew.find(q=>q.name===name);if(person)env.life.hurt(s,person,1+(d.observedHazard||0)*2,'measured environmental exposure '+job.destination,(k,msg,people)=>env.emit(k,msg,{people,missionId:job.id}));}
}
const api={profile,attach,advance};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSExpeditions=api;
})(globalThis);
