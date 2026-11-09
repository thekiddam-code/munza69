/* Autonomous policy helpers. Existing captain intervention remains authoritative. */
(function(root){'use strict';
function init(s){if(!s.operations)s.operations={reserve:{food:120,lab:60,tools:60,spares:40},transfers:[],lastDecision:null};return s.operations;}
function transfer(s,key,requested,now){const o=init(s),n=Math.max(0,Math.min(requested,o.reserve[key]||0));o.reserve[key]-=n;if(n)o.transfers.push({key,amount:n,at:now});o.transfers=o.transfers.slice(-80);return n;}
function maintenancePriority(order,s){const lifeSupport=['C07','C08','C09'].includes(order.room)?40:0;return lifeSupport+(order.priority==='urgent'?100:0)+(100-(s.equipment[order.room]?.condition||0));}
function assessment(p,job,s,life){const peers=s.crew.filter(q=>q!==p&&!q.expeditionAway&&(q.job==='Comms'||q.job==='Scientist'||q.job==='Command'));
 const risk=life.risk(p,peers);return {at:s.clock?.elapsed??s.tick??0,risk,health:p.vitals?.health??100,fatigue:p.vitals?.fatigue??0,morale:p.vitals?.morale??60,experience:p.vitals?.missions??0,support:peers.map(q=>q.name),objective:job.objective,safety:'Recall for health <60, fatigue >85, low energy or stress threshold',workRate:Math.max(.5,Math.min(1.2,1-risk+(p.vitals?.missions||0)*.01))};}
function field(s,m,job,p,env){
 if(!p)return;
 const v=p.vitals;
 if(!v)return;
 const now=env.now;
 if(m.lastRiskTick===now)return;m.lastRiskTick=now;
 p.energy=Math.max(0,p.energy-.03);
 if(m.phase==='onsite'&&now%60===0){
  const risk=env.life.risk(p,s.crew.filter(q=>q!==p&&!q.expeditionAway));
  if(env.random()<risk*.1)env.life.hurt(s,p,8+env.random()*12,'field accident at '+job.location,env.emit);
 }
 if(v.health<60||v.fatigue>85){m.phase='returning';m.progress=0;job.completionReason='crew_health';env.emit('mission',job.id+' recalled for crew health',[p.name],{missionId:job.id,health:v.health});}
}
function debrief(job,p){if(!p?.vitals)return;p.vitals.missions++;job.debrief={crew:p.name,health:p.vitals.health,fatigue:p.vitals.fatigue,morale:p.vitals.morale,experience:p.vitals.missions,evidence:job.evidence,completionReason:job.completionReason};}
function criticalShip(s){return Object.values(s.emergencies||{}).some(e=>e.status==='active'&&(e.severity==='critical'||['C07','C08','C09'].includes(e.room)));}
function reconcileAssignments(s,life){const released=[];for(const order of Object.values(s.maintenance?.orders||{})){if(!order.assigned)continue;const p=s.crew.find(p=>p.name===order.assigned);if(!p||p.expeditionId||p.expeditionAway||p.responseAssignment||p.emergencyId||p.maintenanceRoom!==order.room||!life.ready(p)){released.push({kind:'maintenance',person:order.assigned,room:order.room});order.assigned=null;order.status='open';if(p?.maintenanceRoom===order.room)p.maintenanceRoom=null;}}
 for(const p of s.crew)if(p.emergencyId&&(p.expeditionId||p.expeditionAway||p.responseAssignment||p.energy<=10||!life.ready(p))){released.push({kind:'emergency',person:p.name,room:p.emergencyId});p.emergencyId=null;if(!p.expeditionAway&&!p.expeditionId)p.taskMinutes=0;}
 return released;
}
const api={criticalShip,reconcileAssignments,init,transfer,maintenancePriority,assessment,field,debrief};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSOperations=api;
})(typeof globalThis!=='undefined'?globalThis:this);
