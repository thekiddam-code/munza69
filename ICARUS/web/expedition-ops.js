/* Extend existing manifests/mission registry, not a second mission scheduler or clock. */
(function(root){'use strict';
const W=()=>root.ICARUSExpeditionWorld,F=()=>root.ICARUSFieldEvidence;
const kinds=['survey','inspection','repair','salvage','reconnaissance','sampling','anomaly','retrieval'];
function init(s){W().init(s);F().init(s);return s.expeditionOperations||(s.expeditionOperations={version:1,history:[],requests:[],lastTick:-1});}
function attach(s,m,job){init(s);m.ops44={version:1,stage:'collect',stageAt:s.tick,elapsed:0,node:null,edge:null,devices:[],visited:[],observed:{},actions:{},returning:false,signal:'UNAVAILABLE',lastTick:-1,objective:job.objective,category:job.fieldCategory||({research:'sampling',resource:'salvage'}[job.type]||'survey'),target:job.fieldTarget??null,airlock:{pressure:100,inner:'open',outer:'closed'},suits:{},log:[]};return m;}
function members(s,m){return s.crew.filter(p=>m.members.includes(p.name));}
function move(s,m,room,env){for(const p of members(s,m))env.move(p,room);}
function at(s,m,room){const ps=members(s,m);return ps.length>0&&ps.every(p=>p.room===room&&!p.route.length&&!p.liftRide&&!p.nav?.steps?.[p.nav.index]);}
function event(s,m,env,key,message,significance=2,kind='observation'){const o=m.ops44;o.log.push({at:s.tick,key,message,node:o.node});o.log=o.log.slice(-24);F().capture(s,m,{key,significance,message,kind},env);}
function observe(s,m,env){const o=m.ops44,w=W().init(s),r=w.rooms[o.node],routes=W().passages(s,o.node),signature=JSON.stringify([routes,r.hazard,r.field.utility?.condition]);if(o.observed[o.node]===signature)return;o.observed[o.node]=signature;
 const first=!env.knownMap(m.crew,o.node)?.visited;r.known=r.visited=true;w.position=o.node;env.observe(m,r,{location:'asteroid',cell:r.id,name:r.name,visited:true,blocked:!!r.blocked,hazard:r.hazard||null,routes,fieldKind:r.field.kind,observedAt:s.tick});if(!o.visited.includes(r.id))o.visited.push(r.id);
 F().sample(s,m);if(first){event(s,m,env,'discovery:'+r.id,'The expedition physically surveyed '+r.name+' and its visible passages.',3);if((m.cargo.lab||0)>=.1){env.economy.cargoUse(s,m,'lab',.1);env.survey(m,r);}}if(r.hazard)event(s,m,env,'hazard:'+r.id+':'+r.hazard,'Local observation reported '+r.hazard+' at '+r.name+'.',3);
 F().recover(s,m,env);
}
function returning(s,m,env,reason){const o=m.ops44;if(!o.returning){o.returning=true;o.returnReason=reason;const job=env.job(m);job.completionReason=reason;event(s,m,env,'return:'+reason,'Expedition elected a physical return: '+reason+'.',2,'mission');}m.phase='onsite';}
function advanceEdge(s,m,env){const o=m.ops44,e=o.edge;if(!e)return false;if(!e.retreat&&W().blocked(s,e.from,e.to)){e.retreat=true;event(s,m,env,'route-interrupted:'+e.from+':'+e.to+':'+s.tick,'A local passage became inaccessible; reversing the traversed segment.',3);}e.elapsed+=e.retreat?-1:1;
 for(const p of members(s,m)){p.fieldMotion={from:e.from,to:e.to,elapsed:e.elapsed,duration:e.duration,retreat:!!e.retreat};p.task=e.retreat?'Retracing obstructed field passage':'Traversing '+W().edge(s,e.from,e.to).kind;}
 if(e.retreat&&e.elapsed<=0){o.edge=null;for(const p of members(s,m))delete p.fieldMotion;observe(s,m,env);}else if(e.elapsed>=e.duration){const link=W().edge(s,e.from,e.to);if(link.kind==='lift'){const u=s.asteroidExploration.rooms[5].field.utility;u.battery=Math.max(0,u.battery-.05);}o.node=e.to;o.edge=null;for(const p of members(s,m)){p.fieldPosition=o.node;delete p.fieldMotion;}observe(s,m,env);}return true;}
function beginEdge(s,m,to,env){const o=m.ops44;if(W().blocked(s,o.node,to)){observe(s,m,env);return false;}o.edge={from:o.node,to,elapsed:0,duration:W().duration(s,o.node,to,members(s,m))};return true;}
function action(s,m,env){const o=m.ops44,r=s.asteroidExploration.rooms[o.node],key=o.category+':'+o.node;
 if(o.actions[key]||o.target!==null&&o.target!==o.node)return false;
 if(o.category==='repair'&&r.field.utility){o.action='repair';const u=r.field.utility;if(!members(s,m).some(p=>p.job==='Engineer'))return false;const n=Math.min(.8,(m.cargo.tools||0)/.003,(m.cargo.spares||0)/.005,(m.cargo.energy||0)/.008,86-u.condition);if(n<=0){returning(s,m,env,'repair_consumables');return false;}env.economy.cargoUse(s,m,'tools',n*.003);env.economy.cargoUse(s,m,'spares',n*.005);env.economy.cargoUse(s,m,'energy',n*.008);u.condition+=n;for(const p of members(s,m))p.task='Repairing observed industrial equipment';if(u.condition>=86){const charge=Math.min(1,m.cargo.energy||0);env.economy.cargoUse(s,m,'energy',charge);u.battery+=charge;o.actions[key]=true;event(s,m,env,'repair:'+r.id,'Paid field repair and power transfer restored observed industrial machinery at '+r.name+'.',3,'maintenance');returning(s,m,env,'objective_met');}return true;}
 if(['salvage','sampling','anomaly','inspection','retrieval'].includes(o.category)){o.action=o.category==='sampling'?'sample':'inspect';o.work=(o.work||0)+1;for(const p of members(s,m))p.task=o.action==='sample'?'Collecting an observed field sample':'Inspecting observed field conditions';if(o.work<4)return true;o.work=0;
  if(r.object&&['unseen','detected'].includes(r.objectStatus)&&['salvage','sampling'].includes(o.category)&&![17,22,23,24].includes(r.id)&&(m.cargo.lab||0)>=.25){env.economy.cargoUse(s,m,'lab',.25);env.collect(m,r);r.objectStatus='secured';event(s,m,env,'recovered-object:'+r.id,'Recovered the observed '+r.object+' in a paid sample container.',3,'research');}
  o.actions[key]=true;event(s,m,env,'inspection:'+key,'Completed physical '+o.category+' of '+r.name+'; observations remain distinct from interpretation.',2);returning(s,m,env,'objective_met');return true;
 }return false;}
function tick(s,m,env){init(s);const o=m.ops44;if(!o||o.lastTick===s.tick)return;o.lastTick=s.tick;const ps=members(s,m);if(!ps.length){F().lost(s,m);return;}o.elapsed++;
 if(['collect','stage','airlock'].includes(o.stage)){
  if(ps.some(p=>!env.ready(p))||s.tick-m.launched>480){env.abortStaging(m,'Required crew/readiness or physical staging access unavailable');return;}
  const dest=o.stage==='collect'?'C04':o.stage==='stage'?'C01':'C02';if(!at(s,m,dest))return;
  o.dwell=(o.dwell||0)+1;if(o.dwell<3)return;o.dwell=0;
  if(o.stage==='collect'){if(!F().prepare(s,m,env)){env.abortStaging(m,'Physical camera/light assembly requires actual carried parts/tools/energy or available storage');return;}for(const p of ps){p.carrying='expedition loadout';o.suits[p.name]={condition:100,checked:false,source:'Reserved existing environmental suit token; legacy condition registered at inspection'};}o.stage='stage';move(s,m,'C01',env);}
  else if(o.stage==='stage'){if(m.suits<ps.length||(m.cargo.oxygen||0)<ps.length*.5){env.abortStaging(m,'Suit protection/oxygen check failed');return;}for(const q of Object.values(o.suits))q.checked=true;o.stage='airlock';move(s,m,'C02',env);}
  else {if(!env.airlock()){env.abortStaging(m,'C02 power/hatch/atmosphere safety prevents departure');return;}o.stage='depressurizing';o.airlock.inner='closed';for(const p of ps){p.expeditionAway='asteroid';p.fieldPosition=null;p.task='Sealed EVA vestibule pressure cycle';}m.phase='transit';}
  return;
 }
 if(o.stage==='depressurizing'){if(!env.airlock()){o.stage='repressurizing';o.cancelled=true;return;}if((m.cargo.energy||0)<.02){o.stage='repressurizing';o.cancelled=true;return;}env.economy.cargoUse(s,m,'energy',.02);o.airlock.pressure=Math.max(0,o.airlock.pressure-25);if(o.airlock.pressure===0){o.airlock.outer='open';o.stage='outbound';o.flight=0;}return;}
 if(o.stage==='outbound'||o.stage==='homebound'){
  env.teamField(m);if(!s.remoteCore.missions.asteroid)return;o.flight=(o.flight||0)+1;for(const p of members(s,m))p.task=o.stage==='outbound'?'Expedition shuttle outbound transit':'Expedition shuttle return transit';m.progress=Math.min(100,o.flight*2);
  if(o.stage==='outbound'&&m.phase==='returning'){o.stage='homebound';o.flight=50-o.flight;return;}
  if(o.flight<50)return;
  if(o.stage==='outbound'){o.node=0;o.stage='field';m.phase='onsite';m.progress=0;for(const p of members(s,m))p.fieldPosition=0;observe(s,m,env);event(s,m,env,'landing','Completed physical preparation, pressure cycle and shuttle travel to Landing Shelf.',2,'mission');}
  else{o.node=null;o.stage='repressurizing';o.airlock.outer='closed';o.airlock.pressure=0;}
  return;
 }
 if(o.stage==='repressurizing'){const need=.1;if((m.cargo.oxygen||0)>=need){env.economy.cargoUse(s,m,'oxygen',need);o.airlock.pressure=Math.min(100,o.airlock.pressure+25);}else{o.blocker='Vestibule repressurization awaits actual ship oxygen';if(env.economy.available(s).oxygen>=need)env.economy.moveToCargo(s,m.cargo,'oxygen',need);}if(o.airlock.pressure<100)return;o.airlock.inner='open';o.stage='complete';F().flush(s,m,env,true);env.finish(m);return;}
 if(o.stage!=='field'&&o.stage!=='stranded')return;
 if(m.phase==='returning')returning(s,m,env,'authorized_recall');m.phase='onsite';o.signal=env.signal();env.teamField(m);if(!s.remoteCore.missions.asteroid)return;
 if(m.phase==='returning')returning(s,m,env,'team_safety');m.phase='onsite';
 const power=.006*ps.length,got=env.economy.cargoUse(s,m,'energy',power);if(got<power)returning(s,m,env,'battery_reserve');if((m.cargo.oxygen||0)<=0)for(const p of [...members(s,m)])env.hurt(p,.5,'Exhausted carried suit oxygen');
 const known=id=>env.knownMap(m.crew,id),back=W().route(s,o.node,0,known),reserve=(back?.length??20)*10+60;
 if((m.cargo.oxygen||0)<reserve*.001*ps.length*1.3||(m.cargo.energy||0)<reserve*power+.2||ps.some(p=>p.energy<35||p.vitals.health<60)||o.elapsed>650)returning(s,m,env,'measured_return_reserve');
 F().sample(s,m);F().flush(s,m,env);if(advanceEdge(s,m,env))return;
 const r=s.asteroidExploration.rooms[o.node];if(r.field.radiation>0){o.dose=(o.dose||0)+r.field.radiation*.002;if(o.dose>.25)returning(s,m,env,'measured_radiation_exposure');}
 if(r.field.stability<.4&&!o.actions['secured:'+o.node]){if((m.cargo.tools||0)>=.1){env.economy.cargoUse(s,m,'tools',.1);o.actions['secured:'+o.node]=true;event(s,m,env,'secured:'+o.node,'Used carried safety-line material to secure an observed unstable passage.',3);}else returning(s,m,env,'unstable_terrain_without_line');}
 if(o.returning){if(o.node===0){o.stage='homebound';o.flight=0;m.phase='returning';return;}if(!back?.length){o.stage='stranded';o.blocker='No known accessible return route; no teleport';return;}o.stage='field';o.blocker=null;beginEdge(s,m,back[0],env);return;}
 if(action(s,m,env))return;
 if(o.visited.filter(id=>id!==0).length>=6){returning(s,m,env,'objective_met');return;}
 const path=o.target!==null?W().route(s,o.node,o.target,known):W().next(s,o.node,known);if(!path?.length){returning(s,m,env,'observed_frontier_exhausted');return;}o.action=null;beginEdge(s,m,path[0],env);
}
function complete(s,m){const o=m.ops44,ops=init(s);ops.history.push({id:m.id,at:s.tick,category:o.category,objective:o.objective,visited:[...o.visited],reason:o.returnReason||'completed',devices:[...o.devices],decisions:[...o.log],airlockCycles:true});ops.history=ops.history.slice(-40);for(const p of members(s,m)){delete p.fieldPosition;delete p.fieldMotion;p.carrying=null;}}
function project(s,env){if(!s.expeditionOperations)return null;const m=s.remoteCore.missions.asteroid,o=m?.ops44,live=o&&env.live(m),known=id=>env.map(id);const maps=s.asteroidExploration.rooms.map(r=>({id:r.id,cell:known(r.id)})).filter(r=>r.cell).map(r=>({id:r.id,name:r.cell.name,visited:!!r.cell.visited,hazard:r.cell.hazard||null,routes:r.cell.routes||[],observedAt:r.cell.observedAt??null}));return {version:1,tick:s.tick,active:o?{id:m.id,objective:o.objective,category:o.category,members:m.members,stage:live||!Number.isInteger(o.node)?o.stage:'FIELD / last report only',node:live?o.node:null,signal:live?o.signal:'UNAVAILABLE',cargo:live||!Number.isInteger(o.node)?{...m.cargo}:null,blocker:live?o.blocker:null,returnReason:live?o.returnReason:null}:null,maps,history:s.expeditionOperations.history.slice(-8),records:s.fieldEvidence.archive.slice(-4).map(c=>({id:c.id,camera:c.camera,missionId:c.missionId,at:c.at,location:c.location,reason:c.reason,sourceId:c.sourceId,label:c.recordingAvailability,frames:c.frames.slice(-3),frameCount:c.frames.length,signalGaps:c.signalGaps})),threshold:s.fieldEvidence.threshold,limits:'Bounded camera-state event records; no video encoder'};}
function audit(s){const e=[...W().audit(s),...F().audit(s)],m=s.remoteCore?.missions?.asteroid,o=m?.ops44;if(o?.edge&&!W().edge(s,o.edge.from,o.edge.to))e.push('Disconnected expedition segment');if(o&&o.node!==null&&!s.asteroidExploration.rooms[o.node])e.push('Missing expedition location');return e;}
const api={init,attach,members,tick,complete,project,audit,kinds};if(typeof module==='object'&&module.exports){root.ICARUSExpeditionWorld=require('./expedition-world');root.ICARUSFieldEvidence=require('./field-evidence');module.exports=api;}else root.ICARUSExpeditionOps=api;
})(globalThis);
