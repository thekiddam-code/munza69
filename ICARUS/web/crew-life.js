/* Individual ordinary choices and actual conversations; operational priorities stay upstream. */
(function(root){'use strict';
const clamp=(n,a=0,b=100)=>Math.max(a,Math.min(b,n));
function init(s){const c=s.crewLife||(s.crewLife={version:1,people:{},conversations:0});for(const p of s.crew){if(c.people[p.name])continue;const seed=s.universe?.seed??s.entropy?.seed??1,r=k=>root.ICARUSUniverse.draw(seed,'routine:'+p.name+':'+k);c.people[p.name]={preferredWork:Math.floor(r('work')*5),quietRoom:r('room')<.5?'A03':'A09',sociability:r('social'),curiosity:r('curiosity'),lastSocial:-10000,peerAt:{},recent:[],memories:[],decisions:0};}return c;}
function available(p){return !!p&&(p.vitals?.health??100)>=60&&(p.vitals?.fatigue??0)<75&&(p.energy??100)>=28&&!p.survivalIncapacitated&&!p.expeditionAway&&!p.expeditionId&&!p.emergencyId&&!p.maintenanceRoom&&!p.researchAssignment&&!p.responseAssignment&&!p.rescuePatient&&!p.rescueMedic&&!p.medicalTreatment;}
function choose(s,p,work,env){if(!available(p)||!work.length)return null;const c=init(s).people[p.name],t=env.traits?.(p)||{},options=work.map((v,i)=>({task:v[0],dest:v[1],weight:1+(i===c.preferredWork%work.length?2:0)}));
 if((p.stress||0)>35||(p.social??60)<40)options.push({task:c.sociability<.45?'Taking a quiet break':'Seeking a conversation',dest:c.sociability<.45?c.quietRoom:'A09',weight:1+(p.stress||0)/40});
 if(c.curiosity>.6&&(p.energy??80)>50)options.push({task:'Watching the stars',dest:'A03',weight:.5+(t.curiosity??50)/100});
 const choices=options.filter(o=>env.reachable(p,o.dest));if(!choices.length)return null;
 for(const o of choices){const n=c.recent.filter(x=>x.task===o.task).length;o.weight/=1+n;}
 const total=choices.reduce((n,o)=>n+o.weight,0);let x=env.draw(s.universe?.seed??1,p.name+':choice:'+c.decisions++)*total,selected=choices.at(-1);for(const o of choices){x-=o.weight;if(x<0){selected=o;break;}}
 c.recent.push({at:s.tick,task:selected.task,dest:selected.dest,reason:'Job, individual preference, needs, recent activity and reachable route'});c.recent=c.recent.slice(-12);
 return {task:selected.task,goal:selected.task,dest:selected.dest,duration:18+Math.floor(env.draw(s.universe?.seed??1,p.name+':duration:'+c.decisions)*23)};
}
function talk(s,p,q,env){if(!available(p)||!available(q)||!env.coLocated(p,q)||(p.energy??0)<30||(q.energy??0)<30)return null;if(s.crew.some(x=>x.vitals?.treatmentPaid&&x.room===p.room&&(p.job==='Medic'||q.job==='Medic')))return null;const c=init(s),a=c.people[p.name],b=c.people[q.name];if(s.tick-a.lastSocial<90||s.tick-b.lastSocial<90||s.tick-(a.peerAt[q.name]??-10000)<300)return null;
 const fact=env.report?.(p,q),strained=(p.relationships?.[q.name]||0)<-5&&Math.max(p.stress||0,q.stress||0)>60;
 if(strained||!fact&&(p.social??100)>=60&&(q.social??100)>=60)return null;
 const shared=fact?env.share(p,q,fact):false;if(fact&&!shared)return null;
 const topic=shared?'report':(p.stress>45||q.stress>45)?'support':'company';
 const text=shared?p.name+' shared a '+Math.round(fact.confidence*100)+'%-confidence report with '+q.name+': '+fact.text.slice(0,180):topic==='support'?p.name+' and '+q.name+' took a brief supportive conversation in their shared room.':p.name+' and '+q.name+' shared a conversation during a pause in their routines.';
 const r=env.record('social',text,[p.name,q.name],{activity:'conversation',topic,quotedFactId:shared?fact.id:null,quotedSourceId:shared?fact.sourceId:null,confidence:shared?fact.confidence:null,location:env.position(p)});if(!r?.id)return null;
 for(const [person,m,peer] of [[p,a,q],[q,b,p]]){m.lastSocial=s.tick;m.peerAt[peer.name]=s.tick;m.memories.push({sourceId:r.id,at:s.tick,peer:peer.name,topic});m.memories=m.memories.slice(-24);person.social=clamp((person.social??50)+5);person.stress=clamp((person.stress??0)-(topic==='support'?2:.5));person.relationships=person.relationships||{};person.relationships[peer.name]=clamp((person.relationships[peer.name]||0)+.5,-20,20);}
 p.conversation={with:q.name,sourceId:r.id,until:s.tick+2};q.conversation={with:p.name,sourceId:r.id,until:s.tick+2};c.conversations++;return r;
}
function audit(s){const c=s.crewLife;if(!c)return [];const errors=[];for(const [name,p] of Object.entries(c.people)){if(p.recent.length>12||p.memories.length>24)errors.push('Unbounded crew routine '+name);if(p.memories.some(m=>!m.sourceId))errors.push('Unsourced interaction '+name);}return errors;}
const api={init,available,choose,talk,audit};if(typeof module==='object'&&module.exports){root.ICARUSUniverse=require('./universe');module.exports=api;}else root.ICARUSCrewLife=api;
})(globalThis);
