/* One existing shaft; authoritative cabin/threshold state. No renderer advances this model. */
(function(root){'use strict';
const decks=['A','B','C'];
function init(s){return s.transit||(s.transit={version:1,lastTick:-1,doors:{},lift:{id:'LIFT-01',deck:'A',phase:'idle',from:'A',to:'A',remaining:0,passengers:[],queue:[],capacity:4,completed:0}});}
function tick(s){const t=init(s);if(t.lastTick===s.tick)return;t.lastTick=s.tick;const l=t.lift;
 const alive=n=>(s.crew||[]).some(p=>p.name===n&&!p.expeditionAway&&(p.vitals?.health??100)>0);
 l.queue=l.queue.filter(r=>alive(r.name)&&s.crew.find(p=>p.name===r.name)?.route?.length);l.passengers=l.passengers.filter(alive);
 for(const [id,d] of Object.entries(t.doors)){const room=s.physicalWorld?.rooms?.[id];if(!room)continue;if(['sealed','jammed','locked','blocked','unpowered'].includes(room.door)){d.phase=room.door;continue;}if(d.phase==='opening'&&s.tick-d.at>=1){room.door='open';d.phase='open';d.until=s.tick+3;}else if(d.phase==='open'&&s.tick>d.until){d.phase='closing';d.at=s.tick;}else if(d.phase==='closing'&&s.tick-d.at>=1){room.door='closed';d.phase='closed';}}
 const online=s.navSystem?.elevator!=='offline'&&(s.power??100)>=15;l.fault=online?null:'Lift power/service unavailable';if(!online){if(l.phase!=='idle')l.stalled=true;return;}l.stalled=false;
 if(l.remaining>0){l.remaining--;if(l.remaining>0)return;}
 if(l.phase==='positioning'){l.deck=l.from;l.phase='boarding';l.remaining=1;}
 else if(l.phase==='boarding'){l.phase=l.passengers.length?'travel':'idle';l.remaining=l.passengers.length?5:0;}
 else if(l.phase==='travel'){l.deck=l.to;l.phase='arrival';l.remaining=1;}
 else if(l.phase==='arrival'){for(const name of l.passengers){const p=s.crew.find(p=>p.name===name);if(p?.liftRide){p.liftRide.arrived=true;p.liftRide.phase='exiting';}}l.phase='unloading';}
 else if(l.phase==='unloading'&&!l.passengers.length){l.completed++;l.phase='idle';}
 if(l.phase==='idle'&&l.queue.length){const r=l.queue[0];l.from=r.from;l.to=r.to;l.phase=l.deck===r.from?'boarding':'positioning';l.remaining=l.phase==='boarding'?2:Math.max(1,Math.abs(decks.indexOf(l.deck)-decks.indexOf(l.from))*2);}

}
function gate(s,p,from,to){const id=from.startsWith('R:')?from.slice(2):to.startsWith('R:')?to.slice(2):null;if(!id)return true;const t=init(s),r=s.physicalWorld?.rooms?.[id];if(!r)return true;
 if(['sealed','jammed','locked','blocked','unpowered'].includes(r.door))return false;
 let d=t.doors[id];if(r.door==='closed'||d?.phase==='opening'){if((s.power??100)<15)return false;if(d?.phase!=='opening')t.doors[id]={phase:'opening',at:s.tick,until:s.tick+3};return false;}
 t.doors[id]={phase:'open',at:d?.at??s.tick,until:s.tick+3};return true;}
function request(s,p,from,to){const l=init(s).lift;let ride=p.liftRide;
 if(ride?.arrived){l.passengers=l.passengers.filter(n=>n!==p.name);delete p.liftRide;return 'arrived';}
 if(ride)return 'aboard';
 l.queue=l.queue.filter(r=>r.name!==p.name||r.from===from&&r.to===to);if(!l.queue.some(r=>r.name===p.name))l.queue.push({name:p.name,from,to,at:s.tick});
 if(l.fault||l.phase!=='boarding'||l.from!==from||l.to!==to||l.passengers.length>=l.capacity)return 'waiting';
 l.queue=l.queue.filter(r=>r.name!==p.name);l.passengers.push(p.name);p.liftRide={id:l.id,from,to,boardedAt:s.tick,phase:'aboard',arrived:false};return 'aboard';}
function locate(p){const at=root.ICARUSSpatial.position(p);if(p.liftRide)return 'LIFT-01';if(at.kind==='room')return at.room;if(at.kind==='field')return null;const node=(at.node||'').split(':'),next=(at.next||'').split(':'),deck=node[1]?.[0];if(at.kind==='vertical'&&!p.liftRide&&node[0]==='V')return 'LADDER-'+deck+'-'+node[2];if(node[0]==='R')return 'COR-'+deck+'-'+(api.station?.(node[1])??0);return 'COR-'+deck+'-'+(node[2]||next[2]||0);}
function audit(s){const t=s.transit;if(!t)return [];const l=t.lift,e=[];if(new Set(l.passengers).size!==l.passengers.length||l.passengers.length>l.capacity)e.push('Invalid lift occupancy');for(const p of s.crew||[])if(p.liftRide&&!l.passengers.includes(p.name))e.push('Missing cabin passenger '+p.name);for(const name of l.passengers)if(!s.crew.some(p=>p.name===name&&p.liftRide))e.push('Ghost lift passenger '+name);return e;}
const api={init,tick,gate,request,locate,audit,station:null,layout:{}};if(typeof module==='object'&&module.exports){root.ICARUSSpatial=require('./spatial');module.exports=api;}else root.ICARUSTransit=api;
})(globalThis);
