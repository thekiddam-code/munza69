/* Local decisions around existing controllers, not a second task scheduler. */
(function(root){'use strict';
function choose(s,p,env){if(!root.ICARUSCrewLife.available(p)||p.route?.length||root.ICARUSSpatial.position(p).kind!=='room')return null;
 const room=env.room(p.room);if(room?.debris>12&&room.air>=60&&!env.emergency(p.room))return {task:'Clearing debris',goal:'Clearing debris',dest:p.room,duration:12};
 if(p.followupInspection&&!p.followupInspection.completedAt){const f=p.followupInspection;return {task:'Inspecting completed repair',goal:'Inspecting completed repair',dest:f.room,duration:8};}return null;}
function perform(s,p,env){if(root.ICARUSSpatial.position(p).kind!=='room'||p.route?.length||p.room!==p.target||p.interaction!=='working'&&p.interaction!==null||p.survivalIncapacitated||p.expeditionAway)return;
 if(p.task==='Clearing debris'){const room=env.room(p.room),before=room.debris;room.debris=Math.max(0,before-.8);if(before>12&&room.debris<=12)env.record('maintenance',p.name+' cleared a passable area in '+p.room+'.',[p.name],{activity:'cleanup',room:p.room,debris:room.debris});}
 if(/recreation break|quiet break|Watching the stars/.test(p.task||''))p.stress=Math.max(0,(p.stress||0)-.08);
 if(p.task==='Inspecting completed repair'&&p.taskMinutes===0&&p.followupInspection&&!p.followupInspection.completedAt){const f=p.followupInspection;f.completedAt=s.tick;const eq=env.equipment(f.room);env.record('maintenance',p.name+' physically rechecked the completed repair in '+f.room+'.',[p.name],{activity:'inspection',room:f.room,repairSourceId:f.sourceId,condition:eq?.condition??null});}
}
function concerns(s,env){const c=root.ICARUSCrewSocial.init(s);for(const p of s.crew){const m=c.people[p.name],activity=s.crewLife?.people[p.name]?.activity;if(!activity||activity.waitingMinutes<30||activity.phase!=='waiting'||s.tick-m.lastConcern<1440||p.expeditionAway||p.survivalIncapacitated)continue;
 const key=activity.id+':'+p.interaction;if(m.concernKey===key)continue;const r=env.record('operation',p.name+' requested assistance: '+String(p.task||'assignment blocked')+'. Completion remains unconfirmed.',[p.name],{activity:'assistance-request',activityId:activity.id,room:p.room,waitMinutes:activity.waitingMinutes,reported:true},{confidence:.75});if(r?.id){m.lastConcern=s.tick;m.concernKey=key;m.concernSourceId=r.id;}
 if((p.energy??100)<28&&!p.emergencyId&&!p.responseAssignment&&!p.rescuePatient&&!env.critical()){env.release(p);p.taskMinutes=0;}
 }}
const api={choose,perform,concerns};if(typeof module==='object'&&module.exports){root.ICARUSSpatial=require('./spatial');root.ICARUSCrewLife=require('./crew-life');root.ICARUSCrewSocial=require('./crew-social');module.exports=api;}else root.ICARUSCrewDecisions=api;
})(globalThis);
