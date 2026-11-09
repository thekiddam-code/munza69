/* Event-card reconstruction, with source IDs; never invented camera footage. */
(function(root){'use strict';
function init(s){return s.chronicles||(s.chronicles={version:1,weeks:{},seen:{}});}
function record(s,r){if(!r)return;const c=init(s);if(c.seen[r.id])return;c.seen[r.id]=true;const w=c.weeks[r.episode]||(c.weeks[r.episode]={episode:r.episode,sourceIds:[],segments:[],kinds:{},unresolved:[]});w.sourceIds.push(r.id);w.kinds[r.kind]=(w.kinds[r.kind]||0)+1;
 if(['research','mission','rescue','encounter','medical','injury','recovery','death','relationship','social','emergency'].includes(r.kind)){w.segments.push({sourceId:r.id,minute:r.minute,kind:r.kind,people:r.people,message:r.message,label:'Reconstruction from recorded simulation event'});if(w.segments.length>30)w.segments.splice(1,1);}
}
function close(s){const c=init(s),w=c.weeks[s.episode];if(w)w.unresolved=(s.emergencyOps?.incidents||[]).filter(i=>i.status==='open').map(i=>({id:i.id,cause:i.cause,source:'recorded unresolved incident'}));}
function eligible(record,incidentIds){const d=record.data||{};return d.lethal&&d.encounter&&d.extraordinary&&incidentIds.has(d.recordingId)&&Array.isArray(d.causalEventIds)&&d.causalEventIds.length>0&&d.danger>=.8&&d.disadvantage>=.6&&d.ingenuity>=.6&&d.rarity<=.02;}
function audit(s){const c=init(s),errors=[];for(const w of Object.values(c.weeks))for(const r of w.segments)if(!w.sourceIds.includes(r.sourceId))errors.push('Untraceable chronicle '+r.sourceId);return errors;}
const api={init,record,close,eligible,audit};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSChronicles=api;
})(globalThis);
