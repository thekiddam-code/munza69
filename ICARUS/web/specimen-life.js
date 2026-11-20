/* Biological life extends unifiedWorld.organisms and existing custody/crew work.
   All mutation is called by the authoritative minute tick or validated commands. */
(function(root){'use strict';
const species=Object.freeze({
 grazer:{label:'Small mineral grazer',color:'#9cce91',mobile:true,defensive:false,minPressure:10},
 colony:{label:'Light-responsive colony',color:'#82d9d0',mobile:false,defensive:false,minPressure:15},
 defender:{label:'Defensive segmented crawler',color:'#d6a47b',mobile:true,defensive:true,minPressure:10}
});
const clamp=(v,a=0,b=100)=>Math.max(a,Math.min(b,v)),copy=v=>JSON.parse(JSON.stringify(v));
const data=s=>s.unifiedWorld?.biologicalLife49;
const organisms=s=>Object.values(s.unifiedWorld?.organisms||{}).filter(o=>o.life49);
const item=(s,o)=>(s.specimenCustody?.items||[]).find(i=>i.id===o.life49.custodyId);
const position=(env,p)=>env.position(p),same=(a,b)=>!!a&&!!b&&a.domain===b.domain&&a.node===b.node;
const at=(env,p,q)=>!p.route?.length&&!p.liftRide&&same(position(env,p),q);
function draw(s,key){let h=(s.entropy?.seed??s.universe?.seed??1)>>>0;for(const c of 'bio49:'+key)h=Math.imul(h^c.charCodeAt(0),16777619)>>>0;h^=h>>>16;return (h>>>0)/4294967296;}
function init(s){if(!s.unifiedWorld)return null;if(!data(s))s.unifiedWorld.biologicalLife49={version:1,installedAt:s.tick,lastTick:-1,habitats:{},enclosures:Object.fromEntries([1,2,3,4].map(n=>['BIO-'+n,{id:'BIO-'+n,room:'B03',integrity:100,latched:true,occupant:null,inspectedAt:null,lastAttempt:-1000,source:'Existing B03 storage fixture registered for biological containment; no historical occupants asserted'}])),history:[],nextEvent:1,requests:{},stats:{observed:0,collected:0,escapes:0,care:0,repairs:0,recaptured:0,injuries:0,deaths:0}};
 const b=data(s);for(const r of s.asteroidExploration?.rooms||[]){if(b.habitats[r.id]||!r.field||r.id===0||r.id>=21)continue;
  const viable=r.field.pressure>=10&&r.field.temperature>-20&&r.field.temperature<50&&draw(s,r.id+':present')<.68;
  const family=['grazer','colony','defender'][Math.floor(draw(s,r.id+':family')*3)],id='BIO49-'+r.id;
  b.habitats[r.id]={cell:r.id,examined:false,work:0,organismId:viable?id:null,substrate:viable?2:0,source:'Finite local habitat; no crew knowledge until physical inspection'};
  if(viable&&!s.unifiedWorld.organisms[id])s.unifiedWorld.organisms[id]={id,stage:'adult',sealed:false,dormant:false,location:'asteroid:'+r.id,origin:'8847-A microhabitat '+r.id,life49:{family,custodyId:null,enclosure:null,carrier:null,stress:family==='defender'?45:10,pose:'sheltering',x:draw(s,id+':x'),observed:false,seen:{},lastReport:null,lastService:-1000},behavior:{version:1,state:'sheltering',energy:100,stamina:100,health:100,lastTick:-1,lastAttack:-100,steps:0,meals:0,trace:[]}};
 }return b;}
function note(s,o,pose){if(o.behavior.state!==pose){o.behavior.trace.push({at:s.tick,from:o.behavior.state,to:pose,location:o.location});o.behavior.trace=o.behavior.trace.slice(-64);}o.behavior.state=o.life49.pose=pose;}
function event(s,o,kind,text,people,env,extra={}){const b=data(s),q=env.parse(o.location),r=env.record(kind,text,people,{organismId:o.id,biology49:true,location:o.location,...extra});
 const e={id:'BIO-EVENT-'+b.nextEvent++,at:s.tick,kind,text,organismId:o.id,sourceId:r?.id||null,location:o.location};
 // Operational history contains only received evidence, never hidden field state.
 if(people.length||env.visible?.(q)){o.life49.lastReport={at:s.tick,location:o.location,sourceId:r?.id||null};}
 if(r?.id)b.history.push(e);b.history=b.history.slice(-64);return r;}
function observe(s,o,people,env,source='local witness'){if(!people.length)return null;const key=people.slice().sort().join('|');if(o.life49.seen[key]!==undefined&&s.tick-o.life49.seen[key]<360)return null;o.life49.seen[key]=s.tick;o.life49.observed=true;data(s).stats.observed++;return event(s,o,'observation','Observed '+species[o.life49.family].label.toLowerCase()+'; identification remains provisional.',people,env,{sourceMethod:source,uncertain:true});}
function field(s,m,env){const b=init(s),a=m.ops44;if(!b||!a||a.stage!=='field'||a.edge||a.returning||m.phase!=='onsite')return false;
 const h=b.habitats[a.node];if(!h||h.examined)return false;const ps=s.crew.filter(p=>m.members.includes(p.name)&&same(position(env,p),{domain:'asteroid',node:a.node}));
 if(!ps.length||!ps.some(p=>p.job==='Scientist')||!env.fieldLit(m))return false;
 if(h.lastWorkTick===s.tick)return true;h.lastWorkTick=s.tick;for(const p of ps)p.task='Inspecting a local biological microhabitat';h.work++;if(h.work<4)return true;h.examined=true;h.examinedAt=s.tick;
 const o=s.unifiedWorld.organisms[h.organismId];if(!o||o.behavior.health<=0){env.fieldEvent?.(m,'habitat:'+a.node,'Physical habitat inspection found no recoverable living organism.');return true;}
 const leader=ps.find(p=>p.job==='Scientist');observe(s,o,ps.map(p=>p.name),env);const safe=!species[o.life49.family].defensive||((m.cargo.tools||0)>=.1&&leader.energy>=45&&leader.stress<65);
 if(organisms(s).filter(x=>x.life49.custodyId&&item(s,x)?.status!=='archived deceased').length>=4||!safe||!env.capacity(m,1)||!env.cargoPay(m,{lab:.25,tools:.02})){h.outcome='Observed; collection declined or supplies unavailable';return true;}
 const finding={id:'BIO-OBS-'+o.id,room:s.asteroidExploration.rooms[a.node].name,item:'Living biological specimen / '+o.id,biological:true,integrity:100,contamination:0,properties:{composition:'organic polymer',activity:4,viability:'physically observed living organism'},source:{location:'asteroid',cell:a.node,missionId:m.id,at:s.tick}};
 const physical=env.acquire(finding,leader);if(!physical)return true;physical.organismId49=o.id;physical.carrier=leader.name;physical.location='asteroid';physical.status='field secured';
 Object.assign(o.life49,{custodyId:physical.id,carrier:leader.name,enclosure:null,transportIntegrity:100});o.sealed=true;note(s,o,'secured in portable containment');b.stats.collected++;h.outcome='Collected '+o.id;
 env.fieldEvent?.(m,'biological-collection:'+o.id,'Collected the physically observed '+o.id+' into a paid sealed transport container.');event(s,o,'research',leader.name+' secured '+o.id+' in portable containment.',ps.map(p=>p.name),env,{specimenId:physical.id,missionId:m.id});return true;}
function observeDrone(s,node,name,env){const b=data(s),h=b?.habitats[node],o=s.unifiedWorld?.organisms[h?.organismId];if(!o||o.life49.carrier||o.behavior.health<=0||o.location!=='asteroid:'+node)return null;
 // A drone observes only at its physically reached node; it does not collect.
 return {organismId:o.id,classification:'unidentified local biological motion',familyAppearance:o.life49.family,camera:name,confirmedSpecies:null};}
function syncCarrier(s,o,env){const l=o.life49,p=s.crew.find(p=>p.name===l.carrier),i=item(s,o);if(!l.carrier)return;
 if(!p||(p.vitals?.health??100)<=0){const d=s.living?.deceased?.find(d=>d.name===l.carrier);if(d&&env.bodyPosition){const q=env.bodyPosition(d);if(q)o.location=env.format(q);}if(i){i.status='lost';i.location=o.location;}l.formerCarrier=l.carrier;l.carrier=null;note(s,o,'sealed container awaiting recovery');return;}
 const q=position(env,p);if(q)o.location=env.format(q);if(i){i.location=o.location;i.carrier=p.name;if(!p.expeditionAway)i.status='aboard sealed';}
}
function damage(s,o,amount,env,reason){if(o.behavior.health<=0)return;o.behavior.health=clamp(o.behavior.health-amount);if(o.behavior.health===0){note(s,o,'dead');data(s).stats.deaths++;event(s,o,'observation',o.id+' ceased biological activity: '+reason,env.witnesses(env.parse(o.location)),env,{cause:reason});}}
function tick(s,env){const b=init(s);if(!b||b.lastTick===s.tick)return;b.lastTick=s.tick;
 for(const o of organisms(s)){const l=o.life49;syncCarrier(s,o,env);if(o.behavior.health<=0)continue;
 const q=env.parse(o.location),c=b.enclosures[l.enclosure];if(c){o.location='ship:R:'+c.room;c.integrity=clamp(c.integrity-.00015);const powered=env.power(c.room)>=.2,air=env.air({domain:'ship',node:'R:'+c.room});
  const unsuitable=!powered||air&&(air.pressure<species[l.family].minPressure||air.temperature<0||air.temperature>40||air.fire);l.stress=clamp(l.stress+(unsuitable?.12:-.04));if(unsuitable)damage(s,o,.015,env,'unsuitable containment environment');
  if(species[l.family].defensive&&l.stress>60&&s.tick%5===0)c.integrity=clamp(c.integrity-.08);
  if(species[l.family].mobile&&(!c.latched||c.integrity<=15)&&s.tick%5===0&&draw(s,o.id+':escape:'+s.tick)<.15){c.occupant=null;l.enclosure=null;o.sealed=false;b.stats.escapes++;const i=item(s,o);if(i){i.status='escaped';i.location=c.room;i.carrier=null;}note(s,o,'hiding');event(s,o,'encounter','Containment loss at '+c.id+': '+o.id+' left a physically compromised enclosure.',env.witnesses(q),env,{enclosure:c.id,integrity:c.integrity,latched:c.latched});}
 }
 if(o.life49.custodyId){o.behavior.energy=clamp(o.behavior.energy-.006);if(o.behavior.energy<10)damage(s,o,.01,env,'exhausted biological care reserve');}
 const i=item(s,o);if(i&&i.status==='lost'&&l.carrier){l.carrier=null;o.sealed=true;}
 }
 // Existing field conditions deteriorate only with real occupancy/use, not a disaster timer.
 const m=s.remoteCore?.missions?.asteroid;if(m?.ops44?.stage==='field'&&!m.ops44.edge&&!m.ops44.returning){const r=s.asteroidExploration.rooms[m.ops44.node];if(r.field.stability<.55&&m.ops44.elapsed%15===0&&!m.ops44.actions['secured:'+r.id]){const ps=s.crew.filter(p=>m.members.includes(p.name));if((m.cargo.tools||0)>=.1&&env.cargoPay(m,{tools:.1})){m.ops44.actions['secured:'+r.id]=true;env.fieldEvent?.(m,'terrain-secured:'+r.id,'Crew secured the observed unstable footing with carried material.');}else if(draw(s,m.id+':footing:'+s.tick)<.2){const p=ps[0];if(p)env.hurt(p,3,'Unsecured unstable asteroid footing');env.fieldEvent?.(m,'terrain-slip:'+r.id,'A crew member slipped on the actual unsecured unstable footing.');m.ops44.returning=true;}}}
}
function behave(s,o,env){const b=o.behavior,l=o.life49;if(b.lastTick===s.tick||s.tick%5)return;b.lastTick=s.tick;if(b.health<=0)return;const sp=species[l.family];
 if(o.sealed){note(s,o,b.energy<40?'awaiting care':l.stress>45?'agitated':Math.floor(s.tick/30)%3===0?'resting':sp.mobile?'foraging in enclosure':'responding to light');l.x=clamp(l.x+(draw(s,o.id+':pace:'+s.tick)-.5)*.3,0,1);return;}
 if(o.dormant)return;const q=env.parse(o.location);if(!q)return;
 if(l.transit){const e=l.transit;if(!env.neighbors(e.from).some(n=>same(n,e.to))){l.transit=null;note(s,o,'sheltering behind obstruction');return;}if(++e.elapsed>=e.duration){o.location=env.format(e.to);b.steps++;l.transit=null;}return;}
 const air=env.air(q);if(air&&(air.pressure<sp.minPressure||air.fire||air.temperature>55))damage(s,o,1,env,'local environmental exposure');if(b.health<=0)return;
 const local=s.crew.filter(p=>(p.vitals?.health??100)>0&&at(env,p,q));if(local.length)observe(s,o,local.map(p=>p.name),env);
 const habitat=data(s).habitats[q.domain==='asteroid'?q.node:-1];if(habitat?.substrate>0&&b.energy<85){const n=Math.min(.01,habitat.substrate);habitat.substrate-=n;b.energy=clamp(b.energy+n*10);note(s,o,'feeding on finite substrate');}
 else b.energy=clamp(b.energy-(b.energy<15&&!local.length?.0003:.015));
 if(b.energy===0)damage(s,o,.05,env,'exhausted finite habitat substrate');
 if(sp.defensive&&local.length&&l.stress>45&&s.tick-b.lastAttack>=60&&draw(s,o.id+':defend:'+s.tick)<.12){const p=local[0];b.lastAttack=s.tick;const r=event(s,o,'encounter',o.id+' reacted defensively during a co-located encounter with '+p.name,[p.name],env,{lethal:false});env.hurt(p,4+Math.floor(draw(s,o.id+':injury:'+s.tick)*5),'Documented defensive contact '+o.id+' source '+r?.id);data(s).stats.injuries++;}
 l.stress=clamp(l.stress+(local.length?1:-1));note(s,o,local.length?'sheltering':'foraging');l.x=draw(s,o.id+':x:'+s.tick);
 if(sp.mobile&&(!habitat||local.length)&&draw(s,o.id+':move:'+s.tick)<.14){const ns=env.neighbors(q).filter(n=>n.domain===q.domain);if(ns.length){const to=ns[Math.floor(draw(s,o.id+':edge:'+s.tick)*ns.length)];l.transit={from:q,to,elapsed:0,duration:Math.max(2,env.duration?.(q,to)||4)};note(s,o,'moving through connected passage');}}
 if(q.domain==='ship'&&env.visible(q)&&l.pose!=='sheltering'){l.lastReport={at:s.tick,location:o.location,sourceId:l.lastReport?.sourceId||null};}
}
function busy(p){return p.expeditionAway||p.expeditionId||p.emergencyId||p.survivalDestination||p.survivalIncapacitated||p.researchAssignment||p.systemAssignment||p.maintenanceRoom||p.droneAssignment||p.forwardAssignment||p.privateEventId||p.responseAssignment||p.rescuePatient;}
function job(s,p,env){const b=data(s);if(!b||p.bioAssignment||busy(p)||!env.ready(p)||p.energy<35)return null;
 let o=organisms(s).find(o=>o.life49.carrier===p.name&&!p.expeditionAway),kind=o?(o.behavior.health<=0?'archive-store':'deliver'):null,dest=kind==='archive-store'?'B10':'B03',c=null;
 if(!o)for(const x of organisms(s)){const l=x.life49,e=b.enclosures[l.enclosure];if(s.tick-(l.lastService??-1000)<60)continue;
  if(e&&x.behavior.health<=0&&p.job==='Scientist'){o=x;c=e;kind='archive';break;}
  if(e&&e.integrity<90&&p.job==='Engineer'){o=x;c=e;kind='repair';break;}
  if(e&&p.job==='Scientist'&&(x.behavior.energy<65||b.requests[e.id]||s.tick-(e.inspectedAt??-1000)>720)){o=x;c=e;kind=x.behavior.energy<65?'care':'inspect';break;}
  const q=env.parse(l.lastReport?.location);if(!x.sealed&&x.life49.custodyId&&['Scientist','Security'].includes(p.job)&&q?.domain==='ship'&&String(q.node).startsWith('R:')&&s.tick-l.lastReport.at<120){o=x;kind='recover';dest=q.node.slice(2);break;}
 }
 if(!o||s.crew.some(q=>q.bioAssignment?.organismId===o.id))return null;
 if(!env.access(p,dest))return null;const needs=['care','repair','recover'].includes(kind);p.bioAssignment={organismId:o.id,kind,dest,phase:needs?'collect':'work',progress:0,paid:false};o.life49.lastService=s.tick;
 return {task:needs?'Collecting biological service supplies':'Transporting / inspecting living specimen',goal:'Biological '+kind,dest:needs?'C04':dest,duration:120};}
function release(s,p,env,reason){if(p.bioAssignment?.paid)env.record('maintenance','Prepared biological service materials were expended during interrupted work: '+reason,[p.name],{biology49:true});delete p.bioAssignment;p.taskMinutes=0;p.carrying=null;p.interaction=null;}
function work(s,p,env){const a=p.bioAssignment;if(!a)return false;const o=s.unifiedWorld.organisms[a.organismId],b=data(s);if(!o||busy(p)||!env.ready(p)||p.energy<28){release(s,p,env,'crew unavailable / higher-priority duty');return false;}
 const dest=a.phase==='collect'?'C04':a.dest;if(!at(env,p,{domain:'ship',node:'R:'+dest}))return true;
 p.interaction='working';p.task=a.phase==='collect'?'Preparing biological service supplies':a.kind==='deliver'?'Placing sealed specimen in containment':a.kind==='care'?'Tending a living specimen':a.kind==='repair'?'Repairing containment enclosure':a.kind==='recover'?'Searching for / securing reported specimen':'Inspecting living containment';p.energy=clamp(p.energy-.04);const factor=env.workFactor?.(p)??1;if(factor<=0){a.blocker='Awaiting a secure low-gravity work position';return true;}a.progress+=factor;
 if(a.phase==='collect'){if(a.progress<2)return true;const cost=a.kind==='repair'?{spares:.15,tools:.02}:a.kind==='care'?{food:.03,water:.05,lab:.03}:{lab:.15,tools:.02};if(!env.pay(cost,'Prepared biological '+a.kind+' kit')){release(s,p,env,'supplies unavailable');return true;}a.paid=true;a.phase='work';a.progress=0;p.carrying=a.kind==='repair'?'tools':'sealed service kit';env.travel(p,a.dest,p.task);return true;}
 const oAt=env.parse(o.location);if(a.kind!=='inspect'&&a.kind!=='care'&&a.kind!=='repair'&&!same(oAt,{domain:'ship',node:'R:'+a.dest})){release(s,p,env,'specimen no longer at observed location');return true;}
 if(env.power(a.dest)<.2&&a.kind!=='recover'){a.blocker='Local power unavailable';if(a.progress>30)release(s,p,env,a.blocker);return true;}
 if(a.progress< (a.kind==='repair'?12:a.kind==='recover'?8:5))return true;
 let c=b.enclosures[o.life49.enclosure];if(a.kind==='archive'){if(!c||o.behavior.health>0){release(s,p,env,'archive requires a documented deceased specimen');return true;}c.occupant=null;o.life49.enclosure=null;o.life49.carrier=p.name;a.kind='archive-store';a.dest='B10';a.progress=0;p.carrying='sealed deceased specimen';env.travel(p,'B10','Archiving deceased biological specimen');return true;}
 if(a.kind==='archive-store'){if(o.behavior.health>0){release(s,p,env,'living specimen cannot be archived as deceased');return true;}o.life49.carrier=null;o.location='ship:R:B10';const i=item(s,o);if(i){i.status='archived deceased';i.location='B10';i.carrier=null;}event(s,o,'research',p.name+' physically archived the deceased specimen; identity and research custody retained.',[p.name],env);release(s,p,{...env,record:()=>null},'complete');return true;}
 if(a.kind==='deliver'||a.kind==='recover'){
  if(a.kind==='recover'){if(o.sealed||o.life49.transit){release(s,p,env,'organism not accessible for capture');return true;}const chance=species[o.life49.family].defensive?.65:.9;if(draw(s,o.id+':capture:'+s.tick)>chance){o.life49.stress=clamp(o.life49.stress+20);event(s,o,'encounter',p.name+' attempted recovery; the observed specimen evaded capture.',[p.name],env);release(s,p,env,'capture failed');return true;}o.sealed=true;o.life49.carrier=p.name;const i=item(s,o);if(i){i.status='aboard sealed';i.carrier=p.name;}b.stats.recaptured++;a.kind='deliver';a.dest='B03';a.progress=0;env.travel(p,'B03','Carrying recaptured specimen');return true;}
  c=Object.values(b.enclosures).find(e=>!e.occupant&&e.latched&&e.integrity>=70);if(!c){a.blocker='No intact empty enclosure; specimen remains with physical carrier';release(s,p,env,a.blocker);return true;}c.occupant=o.id;c.inspectedAt=s.tick;o.life49.enclosure=c.id;o.life49.carrier=null;o.location='ship:R:B03';o.sealed=true;const i=item(s,o);if(i){i.status='quarantined';i.location='B03';i.carrier=null;}event(s,o,'research',p.name+' placed '+o.id+' into '+c.id+' after physical transfer.',[p.name],env,{enclosure:c.id,specimenId:o.life49.custodyId});env.intake?.(o);
 }else if(!c||c.occupant!==o.id){release(s,p,env,'enclosure occupancy changed');return true;}
 else if(a.kind==='inspect'&&o.life49.stress>40){o.life49.stress=clamp(o.life49.stress-5);}
 else if(a.kind==='care'){o.behavior.energy=clamp(o.behavior.energy+40);o.life49.stress=clamp(o.life49.stress-15);b.stats.care++;}
 else if(a.kind==='repair'){const amount=(p.energy/100)*30;if(amount<12){release(s,p,env,'worker could not complete repair');return true;}c.integrity=clamp(c.integrity+amount);c.latched=true;b.stats.repairs++;}
 if(c){c.inspectedAt=s.tick;delete b.requests[c.id];}event(s,o,'maintenance',p.name+' completed biological '+a.kind+' work.',[p.name],env,{activity:'biological-'+a.kind,enclosure:c?.id||null});release(s,p,{...env,record:()=>null},'complete');return true;}
function roomView(s,location,available=true){if(!available)return {specimens:[],enclosures:[]};const b=data(s);if(!b)return {specimens:[],enclosures:[]};return {enclosures:location==='ship:R:B03'?Object.values(b.enclosures).map(c=>({id:c.id,integrity:c.integrity,latched:c.latched,occupant:c.occupant})):[],specimens:organisms(s).filter(o=>o.location===location&&!o.life49.transit&&(!o.life49.carrier||!o.sealed)&&(o.sealed||o.life49.pose!=='sheltering')).slice(0,16).map(o=>({id:o.id,family:o.life49.family,pose:o.life49.pose,health:o.behavior.health,energy:o.behavior.energy,stress:o.life49.stress,x:o.life49.x,enclosure:o.life49.enclosure,sealed:o.sealed}))};}
function project(s,env){const b=data(s);if(!b)return null;const live=env.visible({domain:'ship',node:'R:B03'}),view=roomView(s,'ship:R:B03',live);return {version:1,tick:s.tick,live,source:live?'B03 installed camera / observed state':'Containment camera unavailable; occupancy unconfirmed',...view,requests:copy(b.requests),crew:s.crew.filter(p=>p.bioAssignment&&env.visible(position(env,p))).map(p=>({name:p.name,kind:p.bioAssignment.kind,phase:p.bioAssignment.phase,room:p.room,blocker:p.bioAssignment.blocker||null})),history:b.history.filter(e=>env.knownSource(e.sourceId)).slice(-8)};}
function command(s,c,env){const b=data(s),parts=String(c).split(':');if(!b||parts.length!==3||parts[0]!=='biology'||parts[1]!=='inspect'||!b.enclosures[parts[2]])return {ok:false,reason:'Unknown containment command'};if(!b.enclosures[parts[2]].occupant)return {ok:false,reason:'Empty enclosure has no biological inspection target'};if(!env.visible({domain:'ship',node:'R:B03'}))return {ok:false,reason:'No current containment camera/inspection source; unavailable remotely'};b.requests[parts[2]]=s.tick;return {ok:true,reason:'Inspection requested; qualified available crew and physical access required'};}
function audit(s){const b=data(s);if(!b)return [];const e=[],ids=new Set();if(b.version!==1||Object.keys(b.habitats).length>20||Object.keys(b.enclosures).length!==4||b.history.length>64)e.push('Invalid bounded biological state');for(const c of Object.values(b.enclosures)){if(!Number.isFinite(c.integrity)||c.integrity<0||c.integrity>100)e.push('Invalid enclosure integrity');if(c.occupant){if(ids.has(c.occupant))e.push('Duplicate enclosure occupant');ids.add(c.occupant);const o=s.unifiedWorld.organisms[c.occupant];if(!o||o.life49.enclosure!==c.id||!o.sealed||o.location!=='ship:R:'+c.room)e.push('Enclosure custody mismatch');}}
 for(const o of organisms(s)){const l=o.life49;if(!species[l.family]||!Number.isFinite(l.stress)||l.stress<0||l.stress>100||!Number.isFinite(l.x)||l.x<0||l.x>1)e.push('Invalid living specimen');if(l.custodyId&&!item(s,o))e.push('Missing biological custody');if(l.transit&&(!Number.isFinite(l.transit.elapsed)||l.transit.elapsed<0||l.transit.elapsed>l.transit.duration))e.push('Invalid biological transit');}return e;}
const api={species,init,draw,field,observeDrone,tick,behave,job,work,roomView,project,command,audit};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSSpecimenLife=api;
})(globalThis);
