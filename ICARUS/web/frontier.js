/* Observed-opportunity controller. Dependencies/callbacks are explicit for testing. */
(function(root){'use strict';
function init(s,env){env.entities?.init(s);env.experiences?.init(s);env.emergencyOps?.init(s);env.chronicles?.init(s);env.universe.init(s);env.navigation.init(s);env.logistics.init(s);env.anthology?.init(s);
 if(!s.frontier)s.frontier={version:1,enabled:true,selected:'HOME',nextJob:1,jobs:[],active:null,lastTick:-1,lastPlan:-999,lastWeatherDay:-1,stats:{departures:0,arrivals:0,completed:0,failed:0,samples:0,eventKinds:{}}};return s.frontier;
}
function emit(s,env,kind,message,data={}){const f=s.frontier;f.stats.eventKinds[kind]=(f.stats.eventKinds[kind]||0)+1;if(kind==='departure')f.stats.departures++;if(kind==='arrival')f.stats.arrivals++;if(env.emit)env.emit(kind,message,data);}
function environment(s,env){const f=s.frontier,n=s.navigation,day=Math.floor(s.tick/1440);if(n.phase!=='orbit'||f.lastWeatherKey===n.current+':'+day)return;f.lastWeatherKey=n.current+':'+day;
 const d=env.universe.find(s,n.current);if(!d)return;d.observedHazard=env.universe.environment(s,d);d.conditionsRevision=(d.conditionsRevision||0)+1;
 if(d.id!=='HOME'&&d.observedHazard>.55&&env.universe.draw(s.universe.seed,d.id+':storm:'+day)<.05){
  const eq=s.equipment.C07;const damage=3+d.observedHazard*8;eq.condition=Math.max(0,eq.condition-damage);emit(s,env,'environmental_damage','A measured environmental disturbance damaged power-distribution hardware at '+d.name+'.',{destination:d.id,damage});
 }
 if(env.universe.draw(s.universe.seed,d.id+':contact:'+day)<.012){const found=env.universe.scan(s,d.x+2,d.y);if(found.length)emit(s,env,'unexpected_contact','Long-range signal processing resolved additional pre-existing sector contacts.',{systems:found});}
}
function opportunities(s,env){const n=s.navigation;if(n.phase!=='orbit'||n.current==='HOME')return [];const d=env.universe.find(s,n.current),need=env.logistics.needs(s),options=[];
 const failed=type=>s.frontier.jobs.filter(j=>j.destination===d.id&&j.type===type&&j.status==='failed').length;
 const base={destination:d.id,risk:env.universe.environment(s,d),required:{crew:2,suits:2,energy:8,food:1.2,water:4,oxygen:2.4}};
 if(!d.surveyed&&failed('survey')<2)options.push({...base,type:'survey',priority:40+d.interest*15,objective:'Measure three distinct field transects and return recorded observations',reason:'Unsurveyed sensor contact; scientific interest '+d.interest.toFixed(2),duration:180});
 if(d.distress&&!d.signalResolved&&failed('distress')<2)options.push({...base,type:'distress',priority:75,objective:'Recover and inspect the observed distress beacon telemetry',reason:'An unresolved distress carrier was detected',duration:100});
 if(Object.values(d.cache||{}).some(n=>n>0)&&failed('recovery')<2)options.push({...base,type:'recovery',priority:85,objective:'Recover the finite cargo cache left by an earlier failed field operation',reason:'Recorded abandoned cargo has known provenance',duration:120});
 if(d.visited)for(const [key,amount] of Object.entries(need))if(amount>1&&(d.deposits[key]||0)>0&&failed('extract_'+key)<2)options.push({...base,type:'extract_'+key,priority:90,resource:key,requested:Math.min(30,amount,d.deposits[key]),objective:'Extract up to '+Math.min(30,amount,d.deposits[key]).toFixed(1)+' '+key+' units and return the cargo',reason:'Projected operating reserve deficit: '+amount.toFixed(1)+' '+key,duration:180});
 return options.sort((a,b)=>b.priority-a.priority||a.type.localeCompare(b.type));
}
function begin(s,op,env){const f=s.frontier;if(env.emergencyOps&&(s.emergencyOps.transport.unrecovered||s.emergencyOps.transport.condition<65)){s.navigation.lastDecision={at:s.tick,reason:'No return-capable primary transport; field launch withheld'};return false;}if(env.operations?.criticalShip(s))return false;if(Object.values(s.remoteCore.missions).some(Boolean)||s.economy.allowLaunch===false)return false;
 if(op.resource&&env.logistics.cargoMass(s)>=s.logistics.capacity-.01)return false;
 const available=s.crew.filter(p=>!p.expeditionId&&!p.expeditionAway&&!p.researchAssignment&&!p.maintenanceRoom&&!p.emergencyId&&p.energy>=55+(1-(env.experiences?.willingness(p)||1))*20&&p.stress<68&&(s.remoteCore.director.crewReadyAt?.[p.name]||0)<=s.tick);
 const profile=env.expeditions?.profile(op,env.universe.find(s,op.destination)),type=op.resource?'resource':'survey',members=env.teams.select(s,{type,location:op.destination,teamSize:profile?.teamSize},available,env.life);if(members.length<(profile?.teamSize||2))return false;
 const id='F-'+f.nextJob,result=env.teams.launch(s,{id,location:op.destination,loadout:profile?.loadout},members,env.economy);if(!result.allowed)return false;
 f.nextJob++;const job={...op,id,episode:s.episode??null,location:op.destination,status:'active',started:s.tick,members:members.map(p=>p.name),evidence:[],progress:0};
 f.jobs.push(job);const m={...result.manifest,id,phase:'boarding',progress:0,kit:1,extracted:{},fieldProgress:0,lastSample:0};
 if(profile)env.expeditions.attach(m,job,profile);s.remoteCore.missions.frontier=m;f.active=id;
 for(const p of members){p.expeditionId=id;p.task='Frontier mission staging';p.goal=p.task;p.target='C01';p.route=env.path?env.path(p.room,'C01'):[];p.taskMinutes=999;}
 emit(s,env,'mission_authorized','SOL authorized '+id+': '+job.objective+'. '+job.reason+'.',{missionId:id,destination:op.destination,members:job.members});return true;
}
function finish(s,job,m,env){const f=s.frontier,d=env.universe.find(s,job.destination),success=!m.failed;
 if(m.plan){job.stageHistory=m.plan.history;job.equipmentDebrief={condition:m.plan.kitCondition,remainingLoadout:{...m.plan.loadout},exposure:m.plan.exposure};}job.evidence.push({rawReturned:{...(m.extracted||{})},success});env.logistics.deposit(s,d,m,env.economy,success);if(m.stagingCancelled){env.economy.returnCargo(s,m);s.teamLog.suits+=m.suits||0;m.suits=0;for(const name of m.members){const p=s.crew.find(p=>p.name===name);if(p){p.expeditionId=null;p.expeditionAway=false;p.route=[];p.taskMinutes=0;}}}else env.teams.returned(s,m,job,{economy:env.economy});
 for(const name of m.members){const p=s.crew.find(p=>p.name===name);if(p){p.expeditionId=null;if(env.learn)env.learn(p,success,job);}}
 env.experiences?.mission(s,job,success?'success':'failure');job.outcome=success?'complete':m.fieldProgress>30?'partial':'withdrawn';job.status=success?'completed':'failed';job.completed=s.tick;job.condition=m.conditions;job.result=success?'Objective completed with recorded field evidence':'Safety return; recovered material remains in the recorded field cache';
 if(success&&job.type==='distress'&&!d.signalResolved){const finding={id:'BEACON-'+d.id,room:d.name,item:'distress telemetry cartridge',status:'secured by expedition',source:{location:d.id,cell:'beacon',missionId:job.id,at:s.tick},properties:{composition:'manufactured alloy',activity:0},biological:false,integrity:80,contamination:0};d.findings=d.findings||[];d.findings.push(finding);job.evidence.push(finding.id);f.stats.samples++;if(env.acquire)env.acquire(d,job,m,finding);}
 if(success){f.stats.completed++;if(job.type==='survey')d.surveyed=true;if(job.type==='distress')d.signalResolved=true;}
 else f.stats.failed++;
 if(env.recovered)env.recovered(d,job,m);s.remoteCore.missions.frontier=null;f.active=null;
 emit(s,env,success?'mission_completed':'mission_failed',job.id+' '+job.status+': '+job.result+'.',{missionId:job.id,destination:d.id});
}
function activeTick(s,env){const f=s.frontier,job=f.jobs.find(j=>j.id===f.active);if(!job)return;let m=s.remoteCore.missions.frontier;
 if(!m){job.status='failed';job.completed=s.tick;job.result='Field team lost';f.stats.failed++;f.active=null;emit(s,env,'mission_failed',job.id+' failed: field team lost.',{missionId:job.id});return;}
 if(m.stranded&&env.emergencyOps?.strandedTick(s,m,job,env))return;
 if(!m.stranded&&env.operations?.criticalShip(s)&&['transit','onsite'].includes(m.phase)){m.failed=true;m.phase='returning';m.progress=0;emit(s,env,'safety_recall','SOL recalled '+job.id+' for a measured critical ship-system fault.',{missionId:job.id});}
 const d=env.universe.find(s,job.destination),members=m.members.map(n=>s.crew.find(p=>p.name===n)).filter(Boolean);
 if(m.phase==='boarding'){
  if(members.every(p=>p.room==='C01'&&!p.route.length)){m.phase='transit';m.progress=0;for(const p of members){p.expeditionAway=d.id;p.route=[];}}
  else if(s.tick-job.started>360){m.failed=true;m.stagingCancelled=true;finish(s,job,m,env);}return;
 }
 env.teams.field(s,m,job,{economy:env.economy,life:env.life,random:env.random,emit:(kind,msg,people,data)=>emit(s,env,kind,msg,{...data,people})});
 if(m.phase==='returning'&&m.fieldProgress<job.duration)m.failed=true;
 if(m.phase==='transit'||m.phase==='returning'){
  m.progress=Math.min(100,m.progress+100/(m.plan?Math.max(1,Math.ceil((m.plan.distance??25)/.5)):50));if(m.progress>=100){if(m.phase==='transit'){m.phase='onsite';m.fieldProgress=0;}else finish(s,job,m,env);}return;
 }
 if(m.phase!=='onsite')return;
 if(env.emergencyOps){env.emergencyOps.tick(s,env);if(m.stranded)return;}
 const condition=Math.min(s.equipment.C06?.condition||0,s.equipment.C07?.condition||0)/100;
 if(condition<.3||s.economy.stock.energy<3){m.failed=true;m.phase='returning';m.progress=0;return;}
 env.economy.consume(s,'energy',.025,'field operation '+job.id);m.fieldProgress+=Math.max(.35,condition)*(m.workRate||1)*(m.plan?.kitCondition!==undefined ? .5+.5*m.plan.kitCondition/100 : 1);job.progress=m.fieldProgress;env.expeditions?.advance(s,m,job,d,env);
 if(job.resource){const amount=env.logistics.extract(s,d,m,job.resource,Math.min(.2,job.requested-Object.values(m.extracted).reduce((a,b)=>a+b,0)));if(!amount&&m.fieldProgress>10){m.fieldProgress=job.duration;}}
 if(job.type==='recovery')env.logistics.recover(s,d,m,.2);
 if(job.type==='survey')while(m.lastSample<3&&m.fieldProgress>=(m.lastSample+1)*60){
  const cell=m.lastSample++;if(m.plan&&env.economy.cargoUse(s,m,'lab',.1,'field assay '+job.id)<.1-1e-9){emit(s,env,'sampling_blocked','Field assay withheld: no actual assay consumables remained.',{missionId:job.id});continue;}d.fieldCells=d.fieldCells||{};const room=d.fieldCells[cell]||(d.fieldCells[cell]={id:cell,name:d.name+' / transect '+cell});
  const finding=env.discovery.survey(s,d.id,room,m,env.random);if(finding){finding.properties.composition=d.composition;finding.source.missionId=job.id;d.findings=d.findings||[];d.findings.push(finding);job.evidence.push(finding.id);f.stats.samples++;if(env.acquire)env.acquire(d,job,m,finding);}
 }
 if(m.fieldProgress>=job.duration){
  if(env.random()<d.observedHazard*.07){m.failed=true;const p=members[0];if(p)env.life.hurt(s,p,15+env.random()*25,'frontier field incident at '+d.name,(k,msg,people)=>emit(s,env,'injury',msg,{people}));}
  m.phase='returning';m.progress=0;
 }
 if(s.tick-job.started>1500&&!m.incidentId){m.failed=true;m.phase='returning';m.progress=0;}
}
function tick(s,env){const f=init(s,env);if(f.lastTick===s.tick)return;f.lastTick=s.tick;
 const relay=(kind,msg,data)=>emit(s,env,kind,msg,data),navEnv={...env,emit:relay};
 env.entities?.tick(s,navEnv);env.emergencyOps?.tick(s,navEnv);env.navigation.step(s,navEnv);env.logistics.refine(s,env.economy);environment(s,env);
 if(f.active){activeTick(s,env);return;}
 if(s.navigation.phase==='drift'&&!s.navigation.hold&&s.navigation.target&&(s.equipment.C08?.condition||0)>=45&&s.power>=40){env.navigation.plan(s,s.navigation.target,navEnv);return;}
 if(!f.enabled||s.navigation.phase!=='orbit'||s.navigation.hold||!s.crew.length)return;
 if(Object.values(s.remoteCore.missions).some(Boolean))return;
 if(s.navigation.current==='HOME'&&(!env.homeComplete||!env.homeComplete()))return;
 if(s.tick-f.lastPlan<60)return;f.lastPlan=s.tick;if(env.operations?.criticalShip(s)){s.navigation.lastDecision={at:s.tick,reason:'Hold: measured critical ship fault; available engineers retained aboard'};return;}
 if(s.equipment.B01?.condition>=40&&s.power>=40){const d=env.universe.find(s,s.navigation.current);env.universe.scan(s,d.x,d.y);}
 const options=opportunities(s,env);if(options.length&&begin(s,options[0],env))return;
 if(options.some(o=>o.resource))return; // a real reserve deficit takes precedence over more science travel
 if(options.length&&s.tick-(s.navigation.leg?.start||0)<2880)return; // allow actual staffing recovery, not an eternal blockade
 if(s.economy.mode==='survival'){s.navigation.lastDecision={at:s.tick,reason:'Hold: ship survival priorities'};return;}
 const target=env.navigation.choose(s,env);if(target)env.navigation.plan(s,target.id,navEnv);
}
function command(s,action,id,env){init(s,env);if(action==='hold'){s.navigation.hold=true;emit(s,env,'captain_hold','Captain ordered hold at the current or next arrival orbit.');return {ok:true};}
 if(action==='resume'){s.navigation.hold=false;s.frontier.enabled=true;return {ok:true};}
 if(action==='course')return env.navigation.plan(s,id,{...env,emit:(k,m,d)=>emit(s,env,k,m,d)},true);
 if(action==='recall'){const m=s.remoteCore.missions.frontier;if(m){if(m.stranded)return {ok:false,reason:'Stranded transport requires feasible rescue or repair'};m.failed=true;if(m.phase==='boarding'){m.stagingCancelled=true;finish(s,s.frontier.jobs.find(j=>j.id===s.frontier.active),m,env);}else{m.phase='returning';m.progress=0;}return {ok:true};}return {ok:false,reason:'No frontier expedition'};}
 return {ok:false,reason:'Unknown navigation command'};
}
function audit(s,env){const f=init(s,env),errors=[...(env.repair?.audit(s)||[]),...(env.anthology?.audit(s)||[]),...env.universe.audit(s),...env.navigation.audit(s,env.universe),...env.logistics.audit(s,env.universe)];
 errors.push(...(env.entities?.audit(s)||[]),...(env.experiences?.audit(s)||[]),...(env.emergencyOps?.audit(s)||[]),...(env.chronicles?.audit(s)||[]));
 if(f.active&&!f.jobs.some(j=>j.id===f.active))errors.push('Lost frontier mission');if(f.jobs.some(j=>j.status==='active'&&s.tick-j.started>(s.remoteCore.missions.frontier?.incidentId?3600:1800)))errors.push('Stuck frontier operation');return errors;
}
const api={init,tick,opportunities,begin,command,audit};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSFrontier=api;
})(typeof globalThis!=='undefined'?globalThis:this);
