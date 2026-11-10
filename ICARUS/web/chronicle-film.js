/* Pure event selection; archive writes occur only at real episode boundaries. */
(function(root){'use strict';
const copy=x=>JSON.parse(JSON.stringify(x));
function legendary(s,r){const d=r.data||{},records=s.chronicle?.records||[],publicIds=new Set(records.filter(r=>!r.data?.privateKnowledge&&!r.data?.creatorAuthored).map(r=>r.id));const clip=s.cinema?.recordings.find(v=>v.id===d.recordingId&&v.sourceIds.includes(r.id)&&v.actors.length);return !!clip&&root.ICARUSChronicles.eligible(r,new Set([clip.id]),publicIds)&&records.some(x=>x.kind==='death'&&x.data?.encounterSourceId===r.id&&publicIds.has(x.id));}
function compile(s,episode){const w=s.chronicles?.weeks[episode],records=s.chronicle?.records||[],byId=new Map(records.map(r=>[r.id,r])),segments=[],people=new Set(),counts={};
 const add=(kind,text,sourceIds=[],extra={})=>segments.push({kind,text,sourceIds,duration:kind==='highlight'?14:10,label:'RECONSTRUCTION — recorded event summary',...extra});
 add('opening','ICARUS · Episode '+episode+(w?.realWeek?' · '+w.realWeek:'')+'. A chronicle of the saved voyage.');
 for(const row of w?.segments||[]){const r=byId.get(row.sourceId);if(r?.data?.privateKnowledge||r?.data?.creatorAuthored)continue;if((counts[row.kind]||0)>=3||segments.filter(x=>x.kind==='highlight').length>=12)continue;counts[row.kind]=(counts[row.kind]||0)+1;(row.people||[]).forEach(n=>people.add(n));const id=r?.data?.observedSourceId||row.sourceId,at=r?.data?.observedAt??row.minute-480,frame=s.cinema?.recordings.find(v=>v.sourceIds.includes(id)&&v.at===at);add('highlight',row.message,[row.sourceId],frame?{label:frame.label,frame:copy(frame)}:{});
 if(r&&legendary(s,r))add('legendary','Legendary Kill Cam · documented extraordinary lethal encounter',[r.id,...r.data.causalEventIds],{label:frame?.label||'RECONSTRUCTION — missing matched snapshot',frame:frame?copy(frame):null});}
 if(people.size)add('crew','Recorded participants: '+[...people].join(', '),segments.flatMap(x=>x.sourceIds));
 for(const x of [...(w?.unresolved||[]),...(w?.openStories||[])].slice(0,3))add('unresolved','Unresolved at archive: '+(x.cause||x.stage||x.id)+' ['+x.id+']',[]);
 const voice=s.solVoice?.entries.filter(e=>e.episode===Number(episode)&&w?.sourceIds.includes(e.sourceId)).at(-1);if(voice)add('SOL',voice.text,[voice.sourceId]);
 add('credits',people.size?'Archive credits · '+[...people].join(', ')+'. Sources are shown on each card.':'Quiet archive. No eligible shared event highlights retained.');
 return {version:1,episode:Number(episode),realWeek:w?.realWeek||null,segments,duration:segments.reduce((n,x)=>n+x.duration,0),label:'In-app state-snapshot / reconstruction timeline; not recorded video'};
}
function archive(s){const c=root.ICARUSCinema.init(s);if(!c.films[s.episode])c.films[s.episode]=compile(s,s.episode);const keys=Object.keys(c.films).sort((a,b)=>Number(a)-Number(b));while(keys.length>12)delete c.films[keys.shift()];return c.films[s.episode];}
function audit(s){const errors=[];for(const f of Object.values(s.cinema?.films||{}))for(const x of f.segments){if(x.frame&&(!x.frame.sourceIds.length||!x.frame.actors.length||!x.label.includes('not video')))errors.push('Unverified cinematic frame');if(x.kind==='highlight'&&!x.sourceIds.length)errors.push('Unsourced highlight');}return errors;}
const api={compile,archive,legendary,audit};if(typeof module==='object'&&module.exports){root.ICARUSCinema=require('./cinema');root.ICARUSChronicles=require('./chronicles');module.exports=api;}else root.ICARUSChronicleFilm=api;
})(globalThis);
