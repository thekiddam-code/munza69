/* Local simulation domain: durable crew, clinical consequences and continuity. */
(function(root){'use strict';
const clamp=(n,a=0,b=100)=>Math.max(a,Math.min(b,n));
function random(entropy){entropy.seed=(entropy.seed+0x6D2B79F5)>>>0;let t=entropy.seed;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return ((t^t>>>14)>>>0)/4294967296;}
function init(s){
 if(!s.living)s.living={deceased:[],medical:[],lastTick:-1};
 for(const p of s.crew){if(!p.vitals)p.vitals={health:100,fatigue:0,morale:p.mood??60,injuries:[],missions:0,treatmentPaid:false};}
 return s.living;
}
function ready(p){const v=p.vitals;return !p.survivalIncapacitated&&(!v||(v.health>=60&&v.fatigue<75&&v.morale>=20));}
function risk(p,peers=[]){const v=p.vitals||{health:100,fatigue:0,morale:60,missions:0};const trust=peers.reduce((n,q)=>n+(p.relationships?.[q.name]||0),0)/Math.max(1,peers.length);
 return clamp(.08+(100-v.health)/400+v.fatigue/500+(p.stress||0)/700-(v.morale/1500)-Math.min(20,v.missions)/500-trust/500,.01,.8);
}
function hurt(s,p,amount,cause,emit){
 init(s);if(amount<=0)return;
 const v=p.vitals,before=v.health;v.health=clamp(v.health-amount);
 if(!v.injuries.some(x=>x.cause===cause&&x.active)){
  const injury={cause,at:s.clock?.elapsed??s.tick??0,active:true};v.injuries.push(injury);v.injuries=v.injuries.slice(-20);
  emit('injury',p.name+' injured: '+cause,[p.name],{cause,damage:amount});
 }
 if(before>=60&&v.health<60)emit('medical',p.name+' requires medical recovery',[p.name],{health:v.health});
}
function tick(s,env){
 const life=init(s);if(life.lastTick===env.now)return;life.lastTick=env.now;
 for(const p of s.crew){
  const v=p.vitals; if(v.health<=0)continue; const air=env.air(p.room),safe=!air.fire&&!air.breach&&air.pressure>=70&&air.oxygen>=16&&air.temperature<45&&air.smoke<25;
  const resting=/rest|recover|sleep|quiet break/i.test(p.task||'');
  v.fatigue=clamp(v.fatigue+(resting?-.18:p.expeditionAway?.045:.018));
  if(!p.expeditionAway&&!safe){
   const damage=(air.pressure<30||air.oxygen<8?1:0)+(air.fire&&air.temperature>60?.4:0)+(air.smoke>60?.25:0);
   if(damage)hurt(s,p,damage,'hazardous atmosphere in '+p.room,env.emit);
  }
  if(env.now%30===0){
   const ties=Object.values(p.relationships||{}),social=ties.reduce((a,b)=>a+b,0)/Math.max(1,ties.length);
   const target=clamp((p.mood??60)*.35+(p.energy??60)*.25+(100-(p.stress||0))*.15+(100-(p.hunger??35))*.25+social*.5-(100-v.health)*.25-v.fatigue*.15);
   v.morale=clamp(v.morale+(target-v.morale)*.1);
  }
  if(v.health<60&&v.health>0&&!p.expeditionAway){p.goal='Medical recovery';if(v.health<20)p.survivalIncapacitated=true;}
  if(v.health<95&&p.room==='A08'&&!p.expeditionAway&&safe&&env.power>=35){
   const medic=s.crew.find(q=>q!==p&&q.job==='Medic'&&q.room==='A08'&&!q.expeditionAway&&!q.survivalIncapacitated&&q.vitals.health>=40);
   const unit=env.tissue;
   if(medic&&unit.condition>=25&&(v.treatmentPaid||unit.cartridges>0)){
    if(!v.treatmentPaid){unit.cartridges--;if(env.consume)env.consume('medical',1);v.treatmentPaid=true;life.medical.push({patient:p.name,medic:medic.name,at:env.now});life.medical=life.medical.slice(-100);p.relationships[medic.name]=clamp((p.relationships[medic.name]||0)+3,-20,20);env.emit('medical',medic.name+' began injury treatment for '+p.name,[medic.name,p.name],{cartridge:1});}
    v.health=clamp(v.health+.22);unit.condition=Math.max(0,unit.condition-.002);
    if(v.health>=60)p.survivalIncapacitated=false;
    if(v.health>=95){v.treatmentPaid=false;for(const injury of v.injuries)injury.active=false;env.emit('recovery',p.name+' completed injury recovery',[p.name],{health:v.health});}
   }
  }else if(safe&&resting&&v.health>=60&&v.health<95)v.health=clamp(v.health+.005);
 }
 for(const p of [...s.crew].filter(p=>p.vitals.health<=0)){
  const record={name:p.name,job:p.job,at:env.now,cause:p.vitals.injuries.at(-1)?.cause||'critical injury',crew:p};
  life.deceased.push(record);s.crew=s.crew.filter(q=>q!==p);
  env.emit('death',p.name+' died from '+record.cause,[p.name],{cause:record.cause,lethal:true,encounter:false});
  for(const q of s.crew){const rel=q.relationships?.[p.name]||0;q.stress=clamp((q.stress||0)+5+Math.max(0,rel)/2);q.vitals.morale=clamp(q.vitals.morale-5-Math.max(0,rel)/2);}
  for(const [loc,m] of Object.entries(s.remoteCore?.missions||{}))if(m&&(m.members||[m.crew]).includes(p.name)){
   m.casualties=m.casualties||[];if(!m.casualties.includes(p.name))m.casualties.push(p.name);
   const survivors=(m.members||[m.crew]).map(n=>s.crew.find(q=>q.name===n)).filter(Boolean);
   const job=s.remoteCore.director.registry.find(j=>j.id===m.id);
   if(survivors.length){m.crew=survivors[0].name;m.phase='returning';m.progress=0;if(job)job.completionReason='team_casualty';}
   else{if(job){job.status='failed';job.outcome='Expedition crew lost';job.completed=env.now;}const intel=s.remoteCore.director.intelligence?.[loc];if(intel){intel.attempts=(intel.attempts||0)+1;intel.pendingSurvey=false;intel.pendingLead=0;}if(env.lossMission)env.lossMission(m);if(s.teamLog)s.teamLog.lostSuits+=(m.suits||0);s.remoteCore.missions[loc]=null;}
  }
 }
}
const durable=['living','operations','entropy','chronicle','socialDynamics','socialFear','lazarus','tissueRepair','specimenCustody','remoteExploration','asteroidExploration'];
function capture(s){const saved={crew:s.crew};for(const k of durable)if(s[k]!==undefined)saved[k]=s[k];return saved;}
function restore(s,saved){for(const [k,v] of Object.entries(saved))s[k]=v;for(const p of s.crew)if(!p.expeditionAway){p.route=[];p.nav=null;p.emergencyId=null;p.maintenanceRoom=null;p.interaction=null;p.rescuePatient=null;p.rescueMedic=null;p.rescueStage=null;p.taskMinutes=0;}}
const api={random,init,ready,risk,hurt,tick,capture,restore};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSLife=api;
})(typeof globalThis!=='undefined'?globalThis:this);
