/* Recaps select recorded events. They never manufacture footage or encounters. */
(function(root){'use strict';
function init(s){if(!s.chronicle)s.chronicle={nextId:1,records:[],options:{anthology:false,killCam:false}};return s.chronicle;}
function record(s,kind,message,people=[],data={}){const j=init(s);if(kind==='routine')return null;const e={id:'CHR-'+s.episode+'-'+j.nextId++,episode:s.episode,minute:s.minute,kind,message,people:[...new Set(people.filter(Boolean))],data};j.records.push(e);j.records=j.records.slice(-4000);return e;}
function recap(s){const j=init(s),records=j.records.filter(e=>e.episode===s.episode),people={};for(const e of records)for(const name of e.people)people[name]=(people[name]||0)+1;
 const major=records.filter(e=>['emergency','death','injury','research','mission','medical','recovery'].includes(e.kind));
 const relationships=records.filter(e=>e.kind==='relationship'||e.kind==='social');
 const footageIds=new Set((s.incidentArchive||[]).map(r=>r.id));
 const legendary=j.options.killCam?records.filter(e=>e.data?.lethal===true&&e.data?.encounter===true&&e.data?.extraordinary===true&&footageIds.has(e.data.recordingId)):[];
 const lost=records.filter(e=>e.kind==='death').length,failed=records.filter(e=>e.kind==='research'&&['failed','no_result'].includes(e.data?.status)).length;
 return {episode:s.episode,label:'Journal-based reconstruction — not recorded camera footage',sourceIds:records.map(e=>e.id),major:major.slice(-12),relationships:relationships.slice(-6),highlights:Object.entries(people).sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,4).map(([name,events])=>({name,events,sources:records.filter(e=>e.people.includes(name)).slice(-3)})),legendary,ending:j.options.anthology?('Episode closed with '+s.crew.length+' surviving crew, '+lost+' recorded deaths and '+failed+' inconclusive or failed research results. Unresolved scientific questions carry forward.'):null};
}
const api={init,record,recap};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSStory=api;
})(typeof globalThis!=='undefined'?globalThis:this);
