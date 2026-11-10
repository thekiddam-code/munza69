/* Read-only procedural motion. Assigned work is not proof of a performed gesture. */
(function(root){'use strict';
function project(p,options={}){
 const at=root.ICARUSSpatial.position(p),pose=p.recordedPose||root.ICARUSEmbodiment.pose(p,at,!!p.emergencyId,options.tick??Infinity);
 const dead=(p.vitals?.health??100)<=0,disabled=dead||p.survivalIncapacitated,walking=!disabled&&!p.expeditionAway&&['corridor','vertical'].includes(at.kind);
 let motion='still',cue=pose.label;
 if(walking){motion=pose.locomotion==='wheelchair'?'roll':at.kind==='vertical'?([at.node,at.next].some(n=>n?.startsWith('V:'))?'climb':'lift'):'stride';}
 else if(!disabled&&at.kind==='room'){
  if(p.conversation?.until>(options.tick??Infinity))motion='gesture';
  else if(p.rescuePatient||p.vitals?.treatmentPaid)motion='care';
  else if(p.interaction==='working')motion=({repair:'tool',research:'sample',console:'console',inspect:'inspect',eat:'meal',talk:'gesture',rest:'rest'})[pose.kind]||'still';
  else if(pose.kind==='rest')motion='rest';
 }
 if(p.carrying&&walking){motion=pose.locomotion==='wheelchair'?'roll-carry':'carry';cue='CARRYING '+p.carrying;}
 if(dead)cue='NO LIVING ACTIVITY';else if(p.survivalIncapacitated)cue='IMMOBILE / AWAITING ASSISTANCE';
 return {...pose,motion,active:!options.paused&&!options.reduced&&!p.recordedPose&&!disabled&&motion!=='still',cue,node:at.node,next:at.next||null};
}
const api={project};if(typeof module==='object'&&module.exports){root.ICARUSSpatial=require('./spatial');root.ICARUSEmbodiment=require('./embodiment');module.exports=api;}else root.ICARUSAnimation=api;
})(globalThis);
