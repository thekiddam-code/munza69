/* ICARUS v0.94.9. Pure local research model; no I/O or mission authorization. */
(function(root){
'use strict';
const methods=[{id:'custody_review',minutes:30,cost:1},{id:'noninvasive_screen',minutes:60,cost:2}];
function init(sc){
 if(!Array.isArray(sc.programs))sc.programs=[];
 if(!Array.isArray(sc.experiments))sc.experiments=[];
 return sc;
}
function admissible(c,item){return !!(c&&c.status==='complete'&&item&&!item.concealed&&item.status!=='field secured'&&item.status!=='concealed');}
function sync(sc,items){
 init(sc);
 for(const c of sc.cases){
  if(c.status!=='complete'&&c.status!=='held')continue;
  const item=items.find(x=>x.id===c.specimenId);
  const group=c.location+'|'+(c.classification||'unclassified');
  let p=sc.programs.find(x=>x.group===group);
  if(!p){p={id:'RES-'+sc.programs.length,group,location:c.location,subject:c.classification||'unclassified',caseIds:[],hypotheses:[],status:'queued',blocker:null};sc.programs.push(p);}
  if(!p.caseIds.includes(c.id))p.caseIds.push(c.id);
  let h=p.hypotheses.find(x=>x.caseId===c.id);
  if(!h){h={id:'HYP-'+c.id,caseId:c.id,claim:'Recovered material is consistent with '+(c.classification||'an unresolved material class'),confidence:0,status:'tentative',evidenceFor:[],evidenceAgainst:[],unknowns:['Composition','Origin','Function','Biological viability']};p.hypotheses.push(h);}
  // Current admissibility can revoke support without erasing historical experiment records.
  const valid=admissible(c,item);
  h.evidenceFor=valid?[{caseId:c.id,specimenId:item.id,kind:'metadata',observation:c.classification,verified:false}]:[];
  h.evidenceAgainst=[];
  if(!valid)h.evidenceAgainst.push({caseId:c.id,kind:'custody',observation:'Evidence unavailable or custody uncertified'});
  if(item&&item.contamination>0)h.evidenceAgainst.push({caseId:c.id,specimenId:item.id,kind:'confounder',observation:'Recorded contamination: '+item.contamination});
  const screen=sc.experiments.find(x=>x.caseId===c.id&&x.method==='noninvasive_screen'&&x.status==='complete');
  if(valid&&screen)h.evidenceFor.push({caseId:c.id,specimenId:item.id,experimentId:screen.id,kind:'screen',observation:screen.result,verified:true});
  h.confidence=valid?(screen?0.45:0.2):0;
  h.status=valid?'tentative':'unsupported';
 }
 // No revival or Lazarus program without independently recorded viability evidence.
 // Metadata and contamination screens cannot establish viability, so no automatic unlock.
 return sc;
}
function gate(c,item,env){
 if(!admissible(c,item))return 'custody';
 if((item.volatile||item.contamination>=30)&&!(item.status==='quarantined'&&env.containment>=80))return 'containment';
 if(env.lab<55)return 'lab';
 if(!env.analysts.length)return 'analyst';
 return null;
}
function tick(sc,items,env){
 sync(sc,items);
 for(const p of sc.programs){
  if(!p.disagreements)p.disagreements=[];
  const cautious=env.analysts.find(a=>(a.caution||0)>15),bold=env.analysts.find(a=>(a.caution||0)<5);
  if(cautious&&bold&&cautious!==bold&&!p.disagreements.length)p.disagreements.push({caseIds:[...p.caseIds],at:env.now,reviewers:[cautious.name,bold.name],issue:'Interpretation is provisional; reviewers disagree on whether current uncertainty warrants further handling',resolution:'Use conservative containment gates; require independent evidence'});
 }
 const bio=sc.programs.filter(p=>p.subject==='biological specimen');
 if(bio.length){
  const assays=sc.experiments.filter(e=>e.method==='viability_assay');
  sc.lazarusProgram={id:'LAZARUS-LONGITUDINAL',caseIds:[...new Set(bio.flatMap(p=>p.caseIds))],stage:assays.some(e=>e.status==='complete'&&e.observations?.recordedActivity>0)?'replication_required':'evidence_collection',unknowns:['Independent viability replication','Identity continuity','Safe reconstruction'],breakthrough:false};
 }
 if(sc.researchLastTick===env.now)return;
 sc.researchLastTick=env.now;
 const byCase=id=>sc.cases.find(c=>c.id===id);
 const byItem=c=>items.find(x=>x.id===c?.specimenId);
 let active=sc.experiments.find(x=>x.status==='running');
 if(active){
  const c=byCase(active.caseId),item=byItem(c),block=gate(c,item,env);
  const p=sc.programs.find(p=>p.id===active.programId);
  if(block){active.blocker=block;p.status='blocked';p.blocker=block;return;}
  const analyst=env.analysts.find(x=>x.name===active.analyst);
  if(!analyst){active.blocker='analyst';p.status='blocked';p.blocker='analyst';return;}
  active.blocker=null;p.blocker=null;p.status='running';active.progress++;
  if(active.progress<active.duration)return;
  active.completed=env.now;
  active.observations={caseId:c.id,specimenId:item.id,recordedAt:env.now,integrity:item.integrity,contamination:item.contamination,volatile:Boolean(item.volatile)};
  const roll=env.random?env.random():0.99;
  active.uncertaintyRoll=roll;
  // Outcomes are bounded measurements of existing state, never invented discoveries.
  if(!Number.isFinite(item.integrity)||item.integrity<40){active.status='failed';active.result='Sample integrity inadequate; no reliable interpretation';}
  else if(env.random&&roll<0.18){active.status='no_result';active.result='Instrument noise prevents a reliable result; independent replication required';}
  else if(active.method==='viability_assay'){
   const recorded=Number.isFinite(item.recordedActivity)?item.recordedActivity:null;
   active.status=recorded===null?'no_result':'complete';
   active.result=recorded===null?'No independent activity measurement exists; viability unresolved':'Recorded activity assay: '+recorded+'; identity and safe reconstruction remain unverified';
   active.observations.recordedActivity=recorded;
  }
  else if(active.method==='noninvasive_screen'&&item.contamination>0){active.status='no_result';active.result='Contamination confounds screening; composition remains unresolved';}
  else {active.status='complete';active.result=active.method==='custody_review'?'Recorded specimen identity and custody cross-checked; origin unverified':'Non-invasive screen: no recorded contamination; composition and viability unverified';}
  if(item.biological&&env.containment<90&&roll<0.08){
   active.containmentIncident=true;
   if(env.incident)env.incident(item,active);
  }
  p.status='queued';sync(sc,items);return;
 }
 for(const p of sc.programs){
  let selected=null,block=null;
  for(const id of p.caseIds){
   const c=byCase(id),item=byItem(c);
   const availableMethods=items.find(x=>x.id===c?.specimenId)?.biological?[...methods,{id:'viability_assay',minutes:180,cost:5}]:methods;
   const pending=availableMethods.find(m=>!sc.experiments.some(x=>x.caseId===id&&x.method===m.id));
   if(!pending)continue;
   const reason=gate(c,item,env);
   if(reason){block=reason;continue;}
   if(env.supplies.lab<pending.cost){block='supplies';continue;}
   selected={c,item,method:pending};break;
  }
  if(!selected){p.status=block?'blocked':'reviewed';p.blocker=block;continue;}
  const {c,method}=selected;
  env.supplies.lab-=method.cost;
  active={id:'EXP-'+sc.experiments.length,programId:p.id,caseId:c.id,specimenId:c.specimenId,method:method.id,cost:method.cost,analyst:env.analysts[0].name,started:env.now,duration:method.minutes,progress:0,status:'running',result:null};
  sc.experiments.push(active);p.status='running';p.blocker=null;return;
 }
}
const api={init,sync,tick,gate};
if(typeof module==='object'&&module.exports)module.exports=api;
else root.ICARUSResearch=api;
})(typeof globalThis!=='undefined'?globalThis:this);
