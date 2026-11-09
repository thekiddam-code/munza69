(function(root){'use strict';
function init(s){if(!s.navigation)s.navigation={version:1,current:'HOME',position:{x:0,y:0},phase:'orbit',target:null,leg:null,nextLeg:1,hold:false,arrivals:0,fuelUsed:0,history:[],lastDecision:null};return s.navigation;}
function distance(a,b){return Math.hypot(a.x-b.x,a.y-b.y);}
function plan(s,id,env,override=false){
 const n=init(s),reject=reason=>{n.lastDecision={at:s.tick,reason,requested:id};return {ok:false,reason};},d=env.universe.find(s,id);if(!d)return reject('Destination is not a sensor contact');
 if(Object.values(s.remoteCore?.missions||{}).some(Boolean))return reject('Expeditions must return before departure');
 if(n.current===id&&n.phase==='orbit')return reject('Already in orbit');
 const dist=distance(n.position,d),cost=Math.max(.15,dist*5),fuel=s.economy.feedstock.fuel;
 if(fuel+1e-9<cost+(override?0:8))return reject('Insufficient fuel plus safety reserve');
 if(s.power<40||(s.equipment?.C08?.condition||0)<35)return reject('Drive or ship power unavailable');
 const leg={id:'NAV-'+n.nextLeg++,from:{...n.position},to:{x:d.x,y:d.y},target:id,start:s.tick,duration:Math.max(90,Math.ceil(dist*800)),cost,elapsed:0,burned:0};
 n.leg=leg;n.target=id;n.current=null;n.phase='transit';n.hold=false;
 n.lastDecision={at:s.tick,reason:override?'Captain course override':'Selected observed contact by scientific value, fuel need and risk',target:id,cost,duration:leg.duration};
 if(env.emit)env.emit('departure','ICARUS departed toward '+d.name+'; '+leg.duration+' minutes and '+cost.toFixed(2)+' fuel budget.',{legId:leg.id,destination:id});return {ok:true,leg};
}
function step(s,env){const n=init(s);if(n.phase!=='transit'||n.lastTick===s.tick)return;n.lastTick=s.tick;
 if(s.power<20||(s.equipment.C08?.condition||0)<25){n.phase='drift';n.lastDecision={at:s.tick,reason:'Propulsion hardware unsafe; stopped at actual coordinate'};if(env.emit)env.emit('drive_failure','Propulsion interrupted by measured ship damage.',{});return;}
 const l=n.leg;if(!l||!env.universe.find(s,l.target)){n.phase='drift';n.lastDecision={at:s.tick,reason:'Invalid navigation solution; engines stopped'};return;}
 const needed=Math.min(l.cost-l.burned,l.cost/l.duration),burned=env.economy.burnFeed(s,'fuel',needed,'navigation '+l.id);
 if(burned<needed-1e-10){n.phase='drift';n.lastDecision={at:s.tick,reason:'Fuel exhausted; no arrival asserted'};if(env.emit)env.emit('fuel_shortage','Ship propulsion halted: insufficient fuel.',{legId:l.id});return;}
 l.burned+=burned;n.fuelUsed+=burned;l.elapsed++;
 const f=Math.min(1,l.elapsed/l.duration);n.position={x:l.from.x+(l.to.x-l.from.x)*f,y:l.from.y+(l.to.y-l.from.y)*f};
 if(l.elapsed>=l.duration&&n.arrivedLeg!==l.id){
  n.arrivedLeg=l.id;n.current=l.target;n.target=null;n.phase='orbit';const d=env.universe.find(s,n.current);if(!d.visited)s.universe.visitedCount++;d.visited=true;d.lastArrival=s.tick;n.arrivals++;
  n.history.push({id:l.id,destination:d.id,at:s.tick,fuel:l.burned});n.history=n.history.slice(-100);
  if(env.emit)env.emit('arrival','ICARUS established orbit at '+d.name+'.',{legId:l.id,destination:d.id});
 }
}
function choose(s,env){const n=init(s),fuel=s.economy.feedstock.fuel,needFuel=fuel<70,needKey=needFuel?'fuel':s.economy.feedstock.nutrients<100?'nutrients':s.economy.feedstock.ore<300?'ore':s.economy.stock.water<100&&s.economy.feedstock.waterIce<80?'waterIce':null;
 const options=env.universe.bodies(s).filter(d=>d.id!=='HOME'&&d.id!==n.current&&(!d.visited||(needKey&&d.surveyed&&(d.deposits[needKey]||0)>0))).map(d=>{
  const dist=distance(n.position,d),cost=Math.max(.15,dist*5),fuelHint=needKey&&(d.visited?(d.deposits[needKey]||0)>0:d.resourceHints?.[needKey]);
  const score=(d.visited?0:12+d.interest*8)+(needKey&&fuelHint?30:0)+(d.distress&&!d.signalResolved?8:0)-d.hazard*15-dist*5;
  return {d,score,cost,resourceMatch:fuelHint};
 }).filter(x=>(!needKey||x.resourceMatch)&&x.cost+8<=fuel&&x.d.hazard<.86).sort((a,b)=>b.score-a.score||a.d.id.localeCompare(b.d.id));
 return options[0]?.d||null;
}
function audit(s,universe){const n=init(s),errors=[];if(!Number.isFinite(n.position.x)||!Number.isFinite(n.position.y))errors.push('Invalid ship coordinates');if(n.phase==='transit'&&(!n.leg||!universe.find(s,n.leg.target)))errors.push('Lost travel target');if(n.phase==='orbit'){const d=universe.find(s,n.current);if(!d||distance(n.position,d)>1e-8)errors.push('Orbit position differs from destination');}return errors;}
const api={init,distance,plan,step,choose,audit};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSNavigation=api;
})(typeof globalThis!=='undefined'?globalThis:this);
