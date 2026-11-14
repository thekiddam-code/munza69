/* Individual ordinary choices and actual conversations; operational priorities stay upstream. */
(function(root){'use strict';
const clamp=(n,a=0,b=100)=>Math.max(a,Math.min(b,n));
function shiftSpec(s,p){const peers=s.crew.filter(q=>q.job===p.job).map(q=>q.name).sort(),count=Math.min(3,Math.max(1,peers.length)),index=Math.max(0,peers.indexOf(p.name));return {start:(480+(index%count)*Math.floor(1440/count))%1440,minutes:480,rotationDays:7};}
function shift(s,p){const spec=init(s).people[p.name].shift,elapsed=(s.clock?.elapsed??s.tick??0)+480,day=Math.floor(elapsed/1440),start=(spec.start+Math.floor(day/spec.rotationDays)*480)%1440,minute=((elapsed%1440)+1440)%1440;return {start,minutes:spec.minutes,onDuty:(minute-start+1440)%1440<spec.minutes,day};}
function init(s){const c=s.crewLife||(s.crewLife={version:1,people:{},conversations:0});for(const p of s.crew){if(c.people[p.name]){if(!c.people[p.name].shift)c.people[p.name].shift=shiftSpec(s,p);continue;}const seed=s.universe?.seed??s.entropy?.seed??1,r=k=>root.ICARUSUniverse.draw(seed,'routine:'+p.name+':'+k);c.people[p.name]={shift:shiftSpec(s,p),preferredWork:Math.floor(r('work')*5),quietRoom:r('room')<.5?'A03':'A09',sociability:r('social'),curiosity:r('curiosity'),lastSocial:-10000,peerAt:{},recent:[],memories:[],decisions:0};}return c;}
function available(p){return !!p&&!p.systemAssignment&&!p.liftRide&&!p.privateEventId&&(p.vitals?.health??100)>=60&&(p.vitals?.fatigue??0)<75&&(p.energy??100)>=28&&!p.survivalIncapacitated&&!p.expeditionAway&&!p.expeditionId&&!p.emergencyId&&!p.maintenanceRoom&&!p.researchAssignment&&!p.responseAssignment&&!p.rescuePatient&&!p.rescueMedic&&!p.medicalTreatment;}
function choose(s,p,work,env){if(!available(p)||!work.length)return null;const c=init(s).people[p.name],t=env.traits?.(p)||{},options=work.map((v,i)=>({task:v[0],dest:v[1],weight:1+(i===c.preferredWork%work.length?2:0)}));
 const duty=shift(s,p);if(!duty.onDuty){options.splice(0,options.length,{task:'Resting off shift',dest:c.quietRoom==='A03'?'A05':'A06',weight:1+(p.vitals?.fatigue||0)/20},{task:'Taking a recreation break',dest:'A09',weight:1});}
 if((p.hunger||0)>45)options.push({task:'Eating a meal',dest:'A04',weight:1+(p.hunger||0)/20});
 if((p.vitals?.fatigue||0)>50)options.push({task:'Resting',dest:'A05',weight:1+p.vitals.fatigue/15});
 if((p.stress||0)>35||(p.social??60)<40)options.push({task:c.sociability<.45?'Taking a quiet break':'Seeking a conversation',dest:c.sociability<.45?c.quietRoom:'A09',weight:1+(p.stress||0)/40});
 if(c.curiosity>.6&&(p.energy??80)>50)options.push({task:'Watching the stars',dest:'A03',weight:.5+(t.curiosity??50)/100});
 root.ICARUSPersonalities?.options(s,p,options);
 const choices=options.filter(o=>env.reachable(p,o.dest));if(!choices.length)return null;
 for(const o of choices){const n=c.recent.filter(x=>x.task===o.task).length;o.weight/=1+n;o.weight*=root.ICARUSCrewSocial?.preference(s,p,o.dest)??1;}
 const total=choices.reduce((n,o)=>n+o.weight,0);let x=env.draw(s.universe?.seed??1,p.name+':choice:'+c.decisions++)*total,selected=choices.at(-1);for(const o of choices){x-=o.weight;if(x<0){selected=o;break;}}
 c.recent.push({at:s.tick,task:selected.task,dest:selected.dest,onDuty:duty.onDuty,reason:'Assigned shift, job, individual preference, needs, recent activity and reachable route'});c.recent=c.recent.slice(-12);
 return {task:selected.task,goal:selected.task,dest:selected.dest,duration:18+Math.floor(env.draw(s.universe?.seed??1,p.name+':duration:'+c.decisions)*23)};
}
function talk(s,p,q,env){if(!available(p)||!available(q)||!env.coLocated(p,q)||(p.energy??0)<30||(q.energy??0)<30)return null;if(s.crew.some(x=>x.vitals?.treatmentPaid&&x.room===p.room&&(p.job==='Medic'||q.job==='Medic')))return null;const c=init(s),a=c.people[p.name],b=c.people[q.name];if(s.tick-a.lastSocial<90||s.tick-b.lastSocial<90||s.tick-(a.peerAt[q.name]??-10000)<300)return null;
 const offered=env.report?.(p,q),fact=offered?.data?.activity==='conversation'?null:offered,strained=(p.relationships?.[q.name]||0)<-5&&Math.max(p.stress||0,q.stress||0)>60;
 if(strained||!fact&&(p.social??100)>=60&&(q.social??100)>=60)return null;
 const shared=fact?env.share(p,q,fact):false;if(fact&&!shared)return null;
 let topic=shared?'report':(p.stress>45||q.stress>45)?'support':'company';topic=root.ICARUSPersonalities?.topic(s,p,q,topic,s.tick+':'+a.memories.length)??topic;
 const text=root.ICARUSCrewEditorial.interaction(s,p,q,a,b,topic,shared?fact:null);
 const r=shared?.record||env.record('social',text,[p.name,q.name],{activity:'conversation',topic,quotedFactId:shared?fact.id:null,quotedSourceId:shared?fact.sourceId:null,confidence:shared?fact.confidence:null,location:env.position(p),publicAcknowledgment:topic==='company'&&a.sociability>.65&&b.sociability>.65},{disclosure:topic==='company'&&a.sociability>.65&&b.sociability>.65?'shareable':'private'});if(!r?.id)return null;
 for(const [person,m,peer] of [[p,a,q],[q,b,p]]){m.lastSocial=s.tick;m.peerAt[peer.name]=s.tick;m.memories.push({sourceId:r.id,at:s.tick,peer:peer.name,topic});m.memories=m.memories.slice(-24);person.social=clamp((person.social??50)+(topic==='disagreement'?-1:5));person.stress=clamp((person.stress??0)-(topic==='support'?2:topic==='joke'?1:topic==='disagreement'?-1:.5));person.relationships=person.relationships||{};person.relationships[peer.name]=clamp((person.relationships[peer.name]||0)+(topic==='disagreement'?-.5:.5),-100,100);}
 p.conversation={with:q.name,sourceId:r.id,until:s.tick+2};q.conversation={with:p.name,sourceId:r.id,until:s.tick+2};c.conversations++;env.courtship?.(p,q);return r;
}
// A private activity ledger observes existing controllers; it never assigns or advances time.
function activityPhase(p,position,now=Infinity){
 if((p.vitals?.health??100)<=0)return 'deceased';
 if(p.survivalIncapacitated)return 'incapacitated';
 if(p.expeditionAway||p.expeditionId)return 'expedition';
 if(position.kind==='corridor'||position.kind==='vertical')return 'travelling';
 if(p.route?.length||String(p.interaction||'').startsWith('waiting')||position.kind!=='room')return 'waiting';
 if(p.target&&position.room!==p.target)return 'waiting';
 if(p.interaction==='collecting'||p.interaction==='returning')return 'logistics';
 if(p.conversation?.until>0&&p.conversation.until>now)return 'conversation';
 if(p.medicalTreatment||p.vitals?.treatmentPaid)return 'treatment';
 if(p.researchAssignment||p.responseAssignment)return 'committed';
 if(/rest|sleep|quiet break|recover/i.test(p.task||''))return 'resting';
 return p.interaction==='working'?'working':'occupied';
}
function observeActivities(s,env){const c=init(s);if(c.activityTick===s.tick)return;c.activityTick=s.tick;
 for(const p of s.crew){const m=c.people[p.name];m.activityHistory=m.activityHistory||[];m.activitySerial=m.activitySerial||0;
  const at=env.position(p),signature=JSON.stringify([p.goal||p.task||'',p.workRoom||p.target||null,p.expeditionId||null,p.emergencyId||null,p.researchAssignment||null,p.maintenanceRoom||null,p.responseAssignment||null]);
  let activity=m.activity;
  if(!activity||activity.signature!==signature||activity.status==='completed'&&(p.taskMinutes||0)>0){
   if(activity){activity.status=activity.status==='completed'?'completed':'interrupted';activity.endedAt=s.tick;activity.reason=activity.status==='completed'?'Existing task budget completed at its destination':'Existing controller changed assignment';m.activityHistory.push(activity);m.activityHistory=m.activityHistory.slice(-16);}
   activity=m.activity={id:'ACT-'+p.name+'-'+(++m.activitySerial),signature,goal:p.goal||p.task||'Unspecified activity',destination:p.workRoom||p.target||null,startedAt:s.tick,lastAt:s.tick,remaining:Math.max(0,p.taskMinutes||0),activeMinutes:0,waitingMinutes:0,travelMinutes:0,status:'active',adopted:m.activitySerial===1};
  }
  const elapsed=Math.max(0,Math.min(1,s.tick-activity.lastAt));
  const phase=activityPhase(p,at,s.tick);activity.phase=phase;activity.node=at.node;activity.lastAt=s.tick;
  if(phase==='travelling')activity.travelMinutes+=elapsed;
  else if(phase==='waiting')activity.waitingMinutes+=elapsed;
  else if(['working','resting','occupied','logistics','conversation'].includes(phase))activity.activeMinutes+=elapsed;
  const remaining=Math.max(0,p.taskMinutes||0);
  if(activity.status!=='completed'&&activity.remaining>0&&activity.remaining<=elapsed&&remaining===0&&phase!=='waiting'&&phase!=='travelling'&&phase!=='incapacitated'&&phase!=='deceased'&&(!activity.destination||at.node==='R:'+activity.destination)){activity.status='completed';activity.endedAt=s.tick;}
  activity.remaining=remaining;root.ICARUSPersonalities?.completed(s,p,activity);
  if(phase==='deceased'){activity.status='deceased';activity.endedAt=s.tick;activity.reason='Recorded crew death';}
 }
 for(const death of s.living?.deceased||[]){const activity=c.people[death.name]?.activity;if(activity&&activity.status==='active'){activity.status='deceased';activity.phase='deceased';activity.endedAt=Number.isFinite(death.at)?death.at:s.tick;activity.reason='Recorded crew death';}}
}
function completeActivity(s,p,source){const a=s.crewLife?.people[p.name]?.activity,canonical=(s.chronicle?.records||[]).find(r=>r.id===source?.id&&r.message===source.message&&!r.data?.creatorAuthored);if(!a||a.status!=='active'||!canonical||canonical.data?.activity!=='repair-complete'||canonical.data?.room!==a.destination||p.room!==a.destination||p.route?.length)return false;a.status='completed';a.endedAt=s.tick;a.completionSourceId=source.id;a.reason='Existing paid repair controller recorded actual completion';return true;}
function audit(s){const c=s.crewLife;if(!c)return [];const errors=[];for(const [name,p] of Object.entries(c.people)){if(p.recent.length>12||p.memories.length>24)errors.push('Unbounded crew routine '+name);if(p.memories.some(m=>!m.sourceId))errors.push('Unsourced interaction '+name);if((p.activityHistory||[]).length>16)errors.push('Unbounded activity history '+name);if(p.activity&&[p.activity.activeMinutes,p.activity.waitingMinutes,p.activity.travelMinutes].some(v=>!Number.isFinite(v)||v<0))errors.push('Invalid activity accounting '+name);}return errors;}
const api={init,shift,available,choose,talk,observeActivities,activityPhase,completeActivity,audit};if(typeof module==='object'&&module.exports){root.ICARUSCharacterDesign=require('./character-design');root.ICARUSCrewEditorial=require('./crew-editorial');root.ICARUSUniverse=require('./universe');module.exports=api;}else root.ICARUSCrewLife=api;
})(globalThis);
