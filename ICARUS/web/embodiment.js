/* Read-only visible activity: existing physical/task/custody state is authoritative. */
(function(root){'use strict';
function pose(p,spatial,alarm=false,now=Infinity){const moving=['corridor','vertical'].includes(spatial.kind)||!!p.route?.length,t=String(p.task||'').toLowerCase();let kind='idle',prop='',label='ON DUTY';
 if((p.vitals?.health??100)<=0){label='NO LIVING ACTIVITY';}
 else if(p.survivalIncapacitated){kind='treatment';label='AWAITING ASSISTANCE';}
 else if(moving){kind='walk';label=spatial.kind==='vertical'?'DECK TRANSFER':'IN TRANSIT';}
 else if(p.conversation?.until>now){kind='talk';label='CONVERSATION';}
 else if(p.rescuePatient){kind='treatment';label='ASSISTING PATIENT';prop='+';}
 else if(p.vitals?.treatmentPaid&&p.room==='A08'){kind='treatment';label='MEDICAL RECOVERY';prop='+';}
 else if(/waiting|blocked/i.test(p.interaction||'')||/waiting for/.test(t)){label='WAITING';}
 else if(/rest|sleep|recover|quiet break/.test(t)){kind='rest';label='RESTING';}
 else if(p.interaction==='working'||!p.interaction){
  if(/repair|servic|maintain|fabricat|distribution circuit|reactor control/.test(t)){kind='repair';label='EQUIPMENT WORK';prop='⚒';}
  else if(/experiment|analyz|sample|research/.test(t)){kind='research';label='RESEARCH';prop='⚗';}
  else if(/social|conversation|meeting|talk|mediat|disput/.test(t)){kind='talk';label='CONVERSATION';}
  else if(/meal|eat|ration|coffee/.test(t)){kind='eat';label='MEAL / BREAK';prop='◡';}
  else if(/monitor|review|record|report|transmission|manifest/.test(t)){kind='console';label='AT CONSOLE';prop='▤';}
  else if(/inspect|patrol|check/.test(t)){kind='inspect';label='INSPECTING';prop='⌕';}
 }
 if(p.carrying&&(p.vitals?.health??100)>0&&!p.survivalIncapacitated){prop='▣';label=(moving?'CARRYING ':'USING ')+String(p.carrying);}
 if(alarm&&p.emergencyId)label=moving?'RESPONDING TO ALARM':label;
 return {kind,prop,label,locomotion:p.body?.locomotion||'walk',build:p.body?.build||'medium',carrying:p.carrying||null};
}
function station(p,stationFor){const q=root.ICARUSSpatial.position(p),value=n=>{const x=String(n||'').split(':');return x[0]==='R'?stationFor(x[1]):/^[HVL]$/.test(x[0])?Number(x[2]):stationFor(p.room);};return {deck:root.ICARUSSpatial.deck(q),station:value(q.node)+(value(q.next||q.node)-value(q.node))*(q.fraction||0),kind:q.kind,node:q.node,next:q.next};}
const api={pose,station};if(typeof module==='object'&&module.exports){root.ICARUSSpatial=require('./spatial');module.exports=api;}else root.ICARUSEmbodiment=api;
})(globalThis);
