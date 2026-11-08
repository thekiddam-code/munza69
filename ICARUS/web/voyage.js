/* Continuous clock and one-time legacy timer migration. No world resets. */
(function(root){'use strict';
function migrate(s){
 if(s.clock?.version===1)return s.clock;
 const minute=s.minute,oldTick=s.tick,elapsed=Math.max(0,(s.episode-1)*9600+minute-480),oldNow=s.episode*10080+minute;
 const tickDelta=elapsed-oldTick,absoluteDelta=elapsed-oldNow;
 const shift=(obj,key,delta)=>{if(obj&&Number.isFinite(obj[key])&&obj[key]>=0)obj[key]+=delta;};
 const dict=(obj,delta)=>{if(obj)for(const k of Object.keys(obj))shift(obj,k,delta);};
 // Legacy ship clocks were episode-relative; preserve the age of existing reservations.
 const walk=(o)=>{if(!o||typeof o!=='object')return;for(const [k,v] of Object.entries(o)){
  if(['tick','lastCheck','lastRestock','lastChange','lastSignalTick','lastInteractionTick','resolvedTick','createdTick'].includes(k))shift(o,k,tickDelta);
  else if(['lastByKey','lastInteraction','lastIncident','lastBySignature','lastByGroup','faultCooldowns','notices'].includes(k)&&v&&typeof v==='object')dict(v,tickDelta);
  else if(k!=='remoteCore'&&k!=='archived')walk(v);
 }};walk(s);shift(s.maintenance,'lastScan',tickDelta);
 const d=s.remoteCore?.director;
 if(d){shift(d,'lastScan',absoluteDelta);dict(d.lastLaunch,absoluteDelta);dict(d.crewReadyAt,absoluteDelta);
  for(const j of d.registry||[])for(const k of ['created','approved','launched','completed'])shift(j,k,absoluteDelta);
  for(const x of d.interventions||[])shift(x,'time',absoluteDelta);
  const sc=d.science||{};for(const k of ['lastTick','researchLastTick'])shift(sc,k,absoluteDelta);
  for(const c of sc.cases||[])for(const k of ['received','completed'])shift(c,k,absoluteDelta);
  for(const e of sc.experiments||[]){for(const k of ['started','completed','pausedSince','analystMissingSince'])shift(e,k,absoluteDelta);shift(e.observations,'recordedAt',absoluteDelta);for(const r of e.reassignments||[])shift(r,'at',absoluteDelta);}
  for(const p of sc.programs||[])for(const x of p.disagreements||[])shift(x,'at',absoluteDelta);
 }
 shift(s.living,'lastTick',absoluteDelta);
 s.tick=elapsed;s.minute=480+elapsed;
 s.clock={version:1,elapsed,nextEpisodeAt:s.minute+Math.max(1,10080-minute),migration:{legacyEpisode:s.episode,legacyMinute:minute,legacyTick:oldTick}};
 return s.clock;
}
function advance(s){migrate(s);s.clock.elapsed++;s.tick=s.clock.elapsed;s.minute=480+s.clock.elapsed;}
function rollover(s,archive,onBoundary){migrate(s);let n=0;while(s.minute>=s.clock.nextEpisodeAt){
 s.archived=s.archived||[];s.archived.push(archive(s));s.archived=s.archived.slice(-100);s.episode++;s.clock.nextEpisodeAt+=10080;n++;if(onBoundary)onBoundary(s);
 }return n;}
const api={migrate,advance,rollover};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSVoyage=api;
})(typeof globalThis!=='undefined'?globalThis:this);
