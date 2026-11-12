/* Private, evidence-linked social state. Numeric relationships remain owned by the existing crew model. */
(function(root){'use strict';
const limit=(n,a=-100,b=100)=>Math.max(a,Math.min(b,n)),copy=x=>JSON.parse(JSON.stringify(x));
function init(s){const c=s.crewSocial||(s.crewSocial={version:1,people:{},registry:{},lastTick:-1,experienceCursor:0});
 for(const p of s.crew||[]){if(!c.people[p.name])c.people[p.name]={bonds:{},memories:[],consents:{},lastConcern:-10000};if(!c.registry[p.name])c.registry[p.name]={name:p.name,job:p.job,status:'active',sourceId:'EXISTING-CREW-MANIFEST'};else c.registry[p.name].status='active';}
 for(const p of s.living?.deceased||[]){if(!c.registry[p.name])c.registry[p.name]={name:p.name,job:p.crew?.job||p.job||'Recorded crew',sourceId:p.sourceId||'EXISTING-MEMORIAL-RECORD'};c.registry[p.name].status='deceased';}return c;}
function canonical(s,source){return (s.chronicle?.records||[]).find(r=>r.id===source?.id&&r.message===source.message&&!r.data?.creatorAuthored);}
function bond(person,peer){return person.bonds[peer]||(person.bonds[peer]={trust:0,respect:0,resentment:0,attraction:0,loyalty:0,encounters:0,lastAt:0});}
function remember(s,name,peer,sourceId,kind,location,delta={}){const c=init(s),m=c.people[name];if(!m||name===peer||!c.people[peer])return false;
 if(m.memories.some(x=>x.sourceId===sourceId&&x.peer===peer&&x.kind===kind))return false;
 const b=bond(m,peer);for(const [k,v] of Object.entries(delta))if(['trust','respect','resentment','attraction','loyalty'].includes(k))b[k]=limit(b[k]+v,k==='resentment'||k==='attraction'||k==='loyalty'?0:-100);b.encounters++;b.lastAt=s.tick;
 m.memories.push({at:s.tick,sourceId,peer,kind,location:location?copy(location):null});m.memories=m.memories.slice(-32);return true;}
function consent(s,name,peer,accepted,source){const c=init(s);if(!canonical(s,source)||!c.people[name]||!c.people[peer]||name===peer)return false;
 const K=root.ICARUSKnowledge,fid=s.knowledge?.byKey?.[source.id],p=s.crew.find(p=>p.name===name),q=s.crew.find(p=>p.name===peer);
 // Adult consent must be explicitly supplied in a legitimate private interaction, never inferred from identity.
 if(!p||!q||p.adult!==true||q.adult!==true||!K?.known(s,name,fid)||source.data?.consentActor!==name||source.data?.consentPeer!==peer||source.data?.accepted!==!!accepted)return false;
 c.people[name].consents[peer]={accepted:!!accepted,sourceId:source.id,at:s.tick};return true;}
function observe(s,source,people,data={}){if(!canonical(s,source))return false;const K=root.ICARUSKnowledge,c=init(s),fid=s.knowledge?.byKey?.[source.id],witnesses=[...new Set(people)].filter(n=>c.people[n]&&K?.known(s,n,fid));if(witnesses.length<2)return false;
 for(const name of witnesses)for(const peer of witnesses){if(name===peer)continue;let kind,delta;
  if(data.activity==='conversation'){kind=data.topic==='support'?'support':'conversation';delta={trust:.25,respect:.1,resentment:-.15};
   const p=s.crew.find(p=>p.name===name),q=s.crew.find(p=>p.name===peer),m=c.people[name],other=c.people[peer];
   if(m.consents[peer]?.accepted&&other.consents[name]?.accepted&&p?.adult===true&&q?.adult===true)delta.attraction=.2;
   if(p?.job===q?.job&&(q?.vitals?.missions||0)>(p?.vitals?.missions||0)+2){kind='mentorship';delta.respect=.4;}
  }else if(data.disputeId){kind=data.outcome==='compromise'?'reconciliation':'disagreement';delta=kind==='reconciliation'?{trust:.3,resentment:-1}:{trust:-.5,resentment:1};}
  else if(data.activity==='assistance'){kind='assistance';delta={trust:.5,respect:.5,loyalty:.3};}else continue;
  remember(s,name,peer,source.id,kind,K.position(s,name),delta);
 }return true;}
function courtship(s,p,q,env){const c=init(s),K=root.ICARUSKnowledge;
 if(p.adult!==true||q.adult!==true||!p.romanticInterest?.includes(q.name)||!q.romanticInterest?.includes(p.name)||!K.can(s,p.name,q.name,'conversation',env.channel))return false;
 const a=c.people[p.name],b=c.people[q.name];if((a.bonds[q.name]?.trust||0)<5||(b.bonds[p.name]?.trust||0)<5||a.consents[q.name]||b.consents[p.name])return false;
 // The preference enables an autonomous, mutual choice; it never grants knowledge to SOL.
 for(const [person,peer] of [[p,q],[q,p]]){const r=env.record('social',person.name+' privately agreed to explore a personal relationship with '+peer.name+'.',[person.name,peer.name],{activity:'consent',consentActor:person.name,consentPeer:peer.name,accepted:true},{disclosure:'private'});if(r)consent(s,person.name,peer.name,true,r);}return true;
}
function preference(s,p,destination){const m=s.crewSocial?.people[p.name];if(!m)return 1;let score=1;
 for(const memory of m.memories.slice(-8)){if(memory.location?.domain!=='ship'||memory.location.node!=='R:'+destination||s.tick-memory.at>3*1440)continue;const b=m.bonds[memory.peer];if(b)score+=limit((b.trust-b.resentment)/100,-.25,.25);}
 return limit(score,.4,1.8);}
function relationship(s,name,peer){const b=s.crewSocial?.people[name]?.bonds[peer];if(!b)return {labels:[],evidence:0};const labels=[];
 if(b.trust>=5)labels.push('friendship');if(b.respect>=5)labels.push('professional respect');if(b.trust<=-3)labels.push('distrust');if(b.resentment>=5&&b.trust>-3)labels.push('rivalry');if(b.resentment>=3)labels.push('grudge');if(b.loyalty>=3)labels.push('loyalty');if(b.attraction>=3&&s.crewSocial.people[name].consents[peer]?.accepted&&s.crewSocial.people[peer]?.consents[name]?.accepted)labels.push('mutually consenting attraction');return {labels,evidence:b.encounters};}
function register(s,profile,source){const c=init(s);if(!canonical(s,source)||!profile||typeof profile.name!=='string'||!profile.name.trim()||profile.name.length>80||c.registry[profile.name]||Object.keys(c.registry).length>=128||!Array.isArray(source.data?.registeredCrew)||!source.data.registeredCrew.includes(profile.name))return false;
 c.registry[profile.name]={name:profile.name,job:String(profile.job||'Unassigned').slice(0,60),status:'dormant',sourceId:source.id};return true;}
function tick(s){const c=init(s);if(c.lastTick===s.tick)return;c.lastTick=s.tick;
 // Slow forgetting of minor resentment; no relationship or personal history is reset at episode boundaries.
 if(s.tick%1440===0)for(const m of Object.values(c.people))for(const b of Object.values(m.bonds))if(s.tick-b.lastAt>=1440)b.resentment=Math.max(0,b.resentment-.1);
 const records=s.experiences?.records||[];if(c.experienceCursor>records.length)c.experienceCursor=records.length;
 for(const r of records.slice(c.experienceCursor)){if(!c.people[r.person]||!r.sourceId)continue;for(const peer of r.peers||[])remember(s,r.person,peer,r.sourceId,r.kind,null,r.kind==='rescued'?{trust:1,respect:.5,loyalty:1}:r.kind==='failure'?{respect:-.1}:{respect:.2});}c.experienceCursor=records.length;
}
function audit(s){const c=s.crewSocial;if(!c)return [];const errors=[];if(Object.keys(c.registry).length>128)errors.push('Crew registry overflow');for(const [n,m] of Object.entries(c.people)){if(m.memories.length>32)errors.push('Social memory overflow '+n);for(const r of m.memories)if(!r.sourceId)errors.push('Unsourced social memory '+n);for(const b of Object.values(m.bonds))if(['trust','respect','resentment','attraction','loyalty'].some(k=>!Number.isFinite(b[k])||Math.abs(b[k])>100))errors.push('Invalid social bond '+n);}return errors;}
const api={init,observe,consent,courtship,preference,relationship,register,tick,audit};if(typeof module==='object'&&module.exports){root.ICARUSKnowledge=require('./knowledge');module.exports=api;}else root.ICARUSCrewSocial=api;
})(globalThis);
