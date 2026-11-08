/* Seeded field sampling and provenance: one survey opportunity per physical cell. */
(function(root){'use strict';
function survey(s,loc,room,mission,random){
 if(room.scientificSurvey)return null;
 const prior=(s.specimenCustody?.items||[]).filter(x=>x.origin===loc).length;
 const probability=Math.max(.12,Math.min(.7,(loc==='derelict'?.30:.24)+room.id*.008+Math.min(2,mission.kit||0)*.04-prior*.008));
 const roll=random();room.scientificSurvey={at:s.tick,probability,roll,outcome:'no specimen'};
 if(roll>=probability)return null;
 const r=random(),biological=loc==='derelict'?r<.45:r<.15;
 const kind=biological?'biological specimen':r>.8?'data artifact':'geological material';
 const source=loc+':'+room.id;
 const composition=biological?'organic polymer':kind==='data artifact'?'manufactured alloy':random()<.55?'silicate':'carbonate';
 const properties={composition,activity:biological&&random()<.45?1+random()*4:0};
 const finding={id:'OBS-'+loc+'-'+room.id,room:room.name,item:kind+' / '+room.name,status:'secured by expedition',source:{location:loc,cell:room.id,depth:Math.floor(room.id/5),missionId:mission.id,at:s.tick},properties,biological,integrity:65+Math.floor(random()*35),contamination:biological?Math.floor(random()*18):0,bulk:kind==='geological material'?{ore:4,waterIce:2}:null};
 room.scientificSurvey.outcome=finding.id;return finding;
}
function nextStep(world,neighbors){
 const queue=[[world.position]],seen=new Set([world.position]);
 for(let i=0;i<queue.length;i++){const path=queue[i],at=path.at(-1);
  if(at!==world.position&&!world.rooms[at].visited)return path[1];
  for(const n of neighbors(at)){if(seen.has(n)||world.rooms[n].blocked)continue;seen.add(n);queue.push([...path,n]);}
 }return null;
}
function conclusions(sc,now){
 sc.conclusions=sc.conclusions||[];
 const groups=new Map(),byCase=new Map();
 for(const e of sc.experiments||[])if(e.status==='complete'&&e.observations?.composition){const arr=byCase.get(e.caseId)||[];arr.push(e);byCase.set(e.caseId,arr);}
 for(const [id,es] of byCase){
  const c=sc.cases.find(c=>c.id===id);if(!c||c.status!=='complete'||new Set(es.map(e=>e.observations.composition)).size>1)continue;
  if(sc.programs?.some(p=>p.hypotheses?.some(h=>h.caseId===id&&h.status==='unsupported')))continue;
  for(const e of es){const key=e.observations.composition,arr=groups.get(key)||[];arr.push(e);groups.set(key,arr);}
 }
 for(const c of sc.conclusions){const es=groups.get(c.composition)||[],sources=[...new Set(es.map(e=>e.observations.sourceKey).filter(Boolean))];if(sources.length<2&&c.status!=='contested'){c.status='contested';c.revisedAt=now;c.reason='Independent support lost or replication/custody conflict';}}
 for(const [composition,es] of groups){
  const independent=[...new Set(es.map(e=>e.observations.sourceKey).filter(Boolean))];if(independent.length<2)continue;
  let c=sc.conclusions.find(c=>c.composition===composition);
  if(!c){c={id:'CON-'+sc.conclusions.length,kind:'replicated composition family',composition,confirmedAt:now,scope:'Matching measured spectra; origin, function and viability remain unverified'};sc.conclusions.push(c);}
  Object.assign(c,{status:'confirmed',caseIds:[...new Set(es.map(e=>e.caseId))],experimentIds:es.map(e=>e.id),independentSources:independent});
 }
}

const api={survey,nextStep,conclusions};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSDiscovery=api;
})(typeof globalThis!=='undefined'?globalThis:this);
