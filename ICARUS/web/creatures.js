/* Local seeded ecology over existing organisms and physical graph. No event quota. */
(function(root){'use strict';
const clamp=(n,a=0,b=100)=>Math.max(a,Math.min(b,n));
function init(o){if(!o.behavior)o.behavior={version:1,state:o.dormant?'dormant':'sensing',energy:100,stamina:100,health:100,lastTick:-1,lastAttack:-100,steps:0,meals:0,trace:[]};return o.behavior;}
function note(s,o,state,data={}){const b=init(o);if(b.state!==state){b.trace.push({at:s.tick,from:b.state,to:state,location:o.location,...data});b.trace=b.trace.slice(-64);}b.state=state;}
function tick(s,env){const w=s.unifiedWorld;if(!w)return;for(const o of Object.values(w.organisms)){
 if(!['adult','juvenile'].includes(o.stage))continue;const b=init(o);if(b.lastTick===s.tick||s.tick%5!==0)continue;b.lastTick=s.tick;
 if(b.health<=0){note(s,o,'dead');continue;}
 if(o.sealed){note(s,o,'contained');continue;}if(o.dormant){note(s,o,'dormant');continue;}
 if(o.location?.startsWith('vehicle:')){const arrival=env.vehicle?.(o.location.slice(8));if(arrival)o.location=env.format(arrival);else{note(s,o,'contained in transport');continue;}}const here=env.parse(o.location);if(!here){note(s,o,'unknown legacy location');continue;}
 const edges=env.neighbors(here).filter(n=>n.domain===here.domain),air=env.air?.(here);
 // Species rule for this simulation: prolonged low pressure/fire harms active organisms.
 if(air&&(air.pressure<10||air.fire&&air.temperature>65)){b.health=clamp(b.health-2);b.stamina=clamp(b.stamina-4);}
 if(b.health<=0){note(s,o,'dead');env.record('observation','An organism ceased activity under the local environmental conditions.',env.witnesses(here),{organismId:o.id,location:o.location});continue;}
 const prey=s.crew.filter(p=>(p.vitals?.health??100)>0).map(p=>({p,q:env.position(p)})).filter(x=>x.q&&x.q.domain===here.domain&&x.q.node!==null);
 const local=prey.filter(x=>x.q.node===here.node),near=prey.filter(x=>edges.some(n=>n.node===x.q.node));
 const r=key=>env.draw(s.entropy?.seed||1,o.id+':'+s.tick+':'+key);
 b.energy=clamp(b.energy-.02); // Dormant/contained metabolism is not an infinite active hunting budget.
 // Feeding can occur only on a real co-located deceased body, with bounded biomass debit.
 const corpse=(s.living?.deceased||[]).find(d=>d.crew&&d.crew.body?.species!=='android'&&(d.biomassConsumed||0)<1&&env.same(env.bodyPosition(d),here));
 if(corpse&&b.energy<80){const n=Math.min(.1,1-(corpse.biomassConsumed||0));corpse.biomassConsumed=(corpse.biomassConsumed||0)+n;b.energy=clamp(b.energy+n*40);b.meals++;note(s,o,'feeding');continue;}
 if(b.energy<=0){note(s,o,'starved');continue;}
 if(b.stamina<25||b.health<30){note(s,o,'retreat');const safe=edges.filter(n=>!prey.some(x=>env.same(x.q,n)));if(safe.length&&b.stamina>=5)move(s,o,safe[Math.floor(r('retreat')*safe.length)],env);else rest(s,o);continue;}
 if(local.length){const witnesses=local.map(x=>x.p.name);const sightingKey=o.location+':'+witnesses.join(',');if(b.sightingKey!==sightingKey||s.tick-(b.sightedAt??-100)>=60){env.record('observation','A local observer sighted an active organism.',witnesses,{organismId:o.id,location:o.location,behavior:b.state});b.sightingKey=sightingKey;b.sightedAt=s.tick;}
  const eligible=s.tick-b.lastAttack>=20&&b.stamina>=15;if(eligible){b.outcomeCounts=b.outcomeCounts||{opportunities:0,lethal:0};b.outcomeCounts.opportunities++;}if(eligible&&r('attack')<.35){const victim=local[Math.floor(r('target')*local.length)].p;b.lastAttack=s.tick;b.stamina=clamp(b.stamina-15);b.energy=clamp(b.energy-1);note(s,o,'attack',{target:victim.name});const healthBefore=victim.vitals?.health??100,causal=[];const source=env.record('encounter','A documented organism attacked '+victim.name+' at its physical location.',witnesses,{organismId:o.id,location:o.location,encounter:true,lethal:false,attackers:1,defenders:local.length,healthBefore});env.life.hurt(s,victim,12+Math.floor(r('damage')*23),'documented encounter '+o.id+' source '+(source?.id||'unavailable'),(k,m,people,data)=>{const x=env.record(k,m,people,{...data,healthBefore,organismId:o.id,encounter:true,encounterSourceId:source?.id||null});if(x?.id)causal.push(x.id);return x;});if((victim.vitals?.health??0)<=0){b.outcomeCounts.lethal++;env.record('encounter','A documented attack had a lethal outcome; causal records retained.',witnesses,{organismId:o.id,lethal:true,encounter:true,encounterSourceId:source?.id||null,causalEventIds:[source?.id,...causal].filter(Boolean),outcomeCounts:{...b.outcomeCounts}});} 
  }else note(s,o,'hiding');continue;
 }
 if(near.length&&b.stamina>=5){note(s,o,'pursuit');const target=near[Math.floor(r('prey')*near.length)];move(s,o,edges.find(n=>n.node===target.q.node),env);continue;}
 if(!edges.length){note(s,o,'contained');rest(s,o);continue;}
 if(b.stamina<70){note(s,o,'resting');rest(s,o);continue;}
 // With no local stimulus a quiet hiding cycle is valid; no distant prey knowledge.
 note(s,o,'hiding');if(r('explore')<.08){note(s,o,'sensing');move(s,o,edges[Math.floor(r('edge')*edges.length)],env);}
 }}
function rest(s,o){const b=init(o),n=Math.min(4,100-b.stamina,b.energy*2);b.stamina+=n;b.energy=clamp(b.energy-n*.5);}
function move(s,o,to,env){if(!to)return;const b=init(o);o.location=env.format(to);b.steps++;b.stamina=clamp(b.stamina-5);b.energy=clamp(b.energy-.3);}
function parse(location){if(typeof location!=='string')return null;const i=location.indexOf(':');if(i<0)return /^[ABC]\d\d$/.test(location)?{domain:'ship',node:'R:'+location}:null;const domain=location.slice(0,i),node=location.slice(i+1);return ['ship','asteroid','derelict'].includes(domain)&&node!==''?{domain,node:domain==='ship'?node:Number(node)}:null;}
function format(q){return q?q.domain+':'+q.node:'legacy-unlocated:unknown';}
function same(a,b){return !!a&&!!b&&a.domain===b.domain&&a.node===b.node;}
function audit(s){const errors=[];for(const o of Object.values(s.unifiedWorld?.organisms||{})){const b=o.behavior;if(!b)continue;for(const k of ['health','energy','stamina'])if(!Number.isFinite(b[k])||b[k]<0||b[k]>100)errors.push(o.id+': invalid '+k);if(b.trace.length>64)errors.push(o.id+': unbounded trace');}for(const d of s.living?.deceased||[])if((d.biomassConsumed||0)>1+1e-9)errors.push('Body biomass duplication '+d.name);return errors;}
const api={init,tick,parse,format,same,audit};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSCreatures=api;
})(globalThis);
