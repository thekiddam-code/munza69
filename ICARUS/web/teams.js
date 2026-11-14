/* Multi-person manifests, physical supplies, field decisions and return custody. */
(function(root){'use strict';
function migrate(s){
 const missions=Object.entries(s.remoteCore?.missions||{}).filter(([,m])=>m);
 if(!s.teamLog)s.teamLog={suits:6-missions.reduce((n,[,m])=>n+(m.members||[m.crew]).length,0),lostSuits:0,launches:0,decisions:[]};
 for(const [loc,m] of missions){
  if(!m.members){m.members=[m.crew];m.suits=1;}
  if(!m.id){m.id='IMPORTED-'+loc+'-'+s.tick;s.remoteCore.director.registry.push({id:m.id,type:'imported',location:loc,crew:m.crew,members:m.members,status:'active',reason:'Imported existing legacy field operation',objective:'Complete and debrief the already dispatched expedition',created:s.tick});}
 }
}
function names(m){return m.members||[m.crew];}
function select(s,job,candidates,life,preferred){
 const count=Math.max(2,Math.min(4,job.teamSize||2)),chosen=[],roles=job.type==='resource'?['Engineer','Scientist']:job.location==='derelict'?['Scientist','Security']:['Scientist','Engineer'];
 const score=p=>(p.vitals?.health??100)+(p.vitals?.morale??60)*.2-(p.vitals?.fatigue??0)-p.stress*.3+(p.vitals?.missions||0)*2+((p.career?.confidence||0)-(p.career?.caution||0))*2+chosen.reduce((n,q)=>n+(p.relationships?.[q.name]||0),0);
 const canSpare=p=>!['Medic','Engineer'].includes(p.job)||s.crew.filter(q=>q.job===p.job&&!q.expeditionAway&&!chosen.includes(q)&&life.ready(q)).length>1;
 const eligible=candidates.filter(p=>life.ready(p)&&(p.hunger??0)<75&&!p.systemAssignment&&!p.maintenanceRoom&&!p.expeditionAway&&!p.expeditionId&&!p.responseAssignment&&!p.emergencyId&&!p.researchAssignment&&!p.rescuePatient&&!p.rescueMedic);
 if(preferred){const p=eligible.find(p=>p.name===preferred);if(p&&canSpare(p))chosen.push(p);}
 for(const role of roles){const list=eligible.filter(p=>!chosen.includes(p)&&p.job===role&&canSpare(p)).sort((a,b)=>score(b)-score(a)||a.name.localeCompare(b.name));if(chosen.length<count&&list.length)chosen.push(list[0]);}
 for(const p of eligible.sort((a,b)=>score(b)-score(a)||a.name.localeCompare(b.name)))if(chosen.length<count&&!chosen.includes(p)){
  // Never remove the last available clinical or engineering specialist from the ship.
  if(['Medic','Engineer'].includes(p.job)&&s.crew.filter(q=>q.job===p.job&&!q.expeditionAway&&!chosen.includes(q)).length<=1)continue;chosen.push(p);
 }
 return chosen.length===count?chosen:[];
}
function stage(p){p.interaction=null;p.activityKind=null;p.neededSupply=null;p.workRoom=null;p.waitLogged=false;}
function launch(s,job,members,economy){
 const e=economy.init(s);if(job.location!=='derelict'&&s.emergencyOps&&(s.emergencyOps.transport.unrecovered||s.emergencyOps.transport.condition<65))return {allowed:false,reason:'primary transport unavailable'};s.teamLog=s.teamLog||{suits:6,lostSuits:0,launches:0,decisions:[]};
 if(!e.allowLaunch&&e.allowLaunch!==undefined)return {allowed:false,reason:'ship resource priority'};
 const need={food:members.length*.6,water:members.length*2,oxygen:members.length*1.2};
 const loadout=job.loadout||{},totals=(economy.available||economy.totals)(s);if(Object.entries(loadout).some(([k,n])=>totals[k]<n))return {allowed:false,reason:'objective-specific field equipment'};if(s.teamLog.suits<members.length||totals.energy<8||Object.entries(need).some(([k,n])=>totals[k]<n))return {allowed:false,reason:'expedition equipment or supplies'};
 const m={members:members.map(p=>p.name),crew:members[0].name,cargo:{},suits:members.length,conditions:{},decisions:[],launched:s.tick,lastTick:-1};
 for(const [k,n] of Object.entries(need))economy.moveToCargo(s,m.cargo,k,n);
 economy.consume(s,'energy',8,'shuttle launch '+job.id);for(const [k,n] of Object.entries(loadout))economy.moveToCargo(s,m.cargo,k,n);s.teamLog.suits-=members.length;s.teamLog.launches++;
 for(const p of members)stage(p);
 m.averageExperience=members.reduce((n,p)=>n+(p.vitals?.missions||0),0)/members.length;
 const relationship=members[0].relationships?.[members[1].name]||0;
 m.cohesion=relationship;m.workRate=Math.max(.5,Math.min(1.3,1+relationship*.01+m.averageExperience*.015));
 return {allowed:true,manifest:m};
}
function field(s,m,job,env){
 if(m.lastTeamTick===s.tick||m.phase==='boarding')return;m.lastTeamTick=s.tick;
 const members=names(m).map(n=>s.crew.find(p=>p.name===n)).filter(Boolean);
 if(!members.length)return;
 m.conditions=m.conditions||{};m.decisions=m.decisions||[];
 let emergency=false;
 for(const p of members){
  p.expeditionAway=job.location;p.energy=Math.max(0,p.energy-.025);
  for(const [k,rate] of [['food',.0007],['water',.0014],['oxygen',.001]])if(m.cargo&&env.economy.cargoUse(s,m,k,rate)<rate-1e-9)emergency=true;
  if(!env.groundedHazards&&m.phase==='onsite'&&s.tick%60===0&&env.random()<env.life.risk(p,members.filter(q=>q!==p))*.12)env.life.hurt(s,p,8+env.random()*12,'team field accident at '+job.location,env.emit);
  if(p.vitals.health<60||p.vitals.fatigue>85||p.energy<25)emergency=true;
  m.conditions[p.name]={health:p.vitals.health,fatigue:p.vitals.fatigue,morale:p.vitals.morale,energy:p.energy,at:s.tick};
 }
 if(m.phase==='onsite'&&m.cohesion<-6&&!m.disagreementRecorded){m.disagreementRecorded=true;m.decisions.push({at:s.tick,kind:'disagreement',people:members.map(p=>p.name),reason:'Documented relationship tension slowed field decisions'});m.workRate=Math.max(.4,m.workRate*.75);env.emit('mission','Expedition '+m.id+' slowed by team disagreement',members.map(p=>p.name),{});}
 if(emergency&&m.phase!=='returning'){
  const injured=members.filter(p=>p.vitals.health<60);m.rescue={at:s.tick,assisting:members.filter(p=>!injured.includes(p)).map(p=>p.name),patients:injured.map(p=>p.name)};
  m.decisions.push({at:s.tick,kind:'emergency_return',reason:injured.length?'injury and buddy rescue':'fatigue or carried supplies',people:members.map(p=>p.name)});m.decisions=m.decisions.slice(-30);
  job.completionReason='team_safety';m.phase='returning';m.progress=0;env.emit('mission','Team '+m.id+' initiated safety return with buddy assistance',members.map(p=>p.name),{missionId:m.id});
 }
}
function returned(s,m,job,env){
 if(m.returnedAt!==undefined)return;m.returnedAt=s.tick;s.remoteCore.director.crewReadyAt=s.remoteCore.director.crewReadyAt||{};
 env.economy.returnCargo(s,m);s.teamLog=s.teamLog||{suits:0,lostSuits:0,launches:0,decisions:[]};s.teamLog.suits+=m.suits||0;m.suits=0;
 const returns=[];
 for(const name of names(m)){const p=s.crew.find(p=>p.name===name);if(!p)continue;p.expeditionAway=false;p.room=m.returnRoom||(m.transfer==='collar'?'C02':'C01');p.route=[];p.taskMinutes=20;p.task='Returned with expedition team';p.vitals.missions++;p.energy=Math.max(0,p.energy-5);returns.push({...m.conditions?.[name],name,health:p.vitals.health});if(job)s.remoteCore.director.crewReadyAt[name]=s.tick+180;}
 if(job){job.members=[...names(m)];job.teamDebrief={members:returns,decisions:m.decisions||[],rescue:m.rescue||null,casualties:m.casualties||[],cargoReturned:true};}
}
const api={migrate,names,select,stage,launch,field,returned};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSTeams=api;
})(typeof globalThis!=='undefined'?globalThis:this);
