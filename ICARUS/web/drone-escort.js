/* Ship-dock escort rotation. Received team reports only; field docks require a real camp controller. */
(function(root){'use strict';
const D=()=>root.ICARUSDroneOps,W=()=>root.ICARUSExpeditionWorld;
function tick(s,env){const o=s.droneOperations;if(!o||o.escortTick===s.tick)return;o.escortTick=s.tick;const team=env.team?.();let e=o.escort;if(!team){if(e)for(const d of Object.values(o.drones))if(d.mission?.escortId===e.missionId&&['DIRECT','RELAYED'].includes(D().signal(s,d,env))){d.mission.returning=true;d.mission.reason='Received expedition completion or loss of current escort report';}return;}
 if(!o.enabled||!env.autonomy()||env.critical())return;
 if(!e||e.missionId!==team.id)e=o.escort={missionId:team.id,active:null,replacing:null,handoffs:[],gaps:[],lastGap:null};
 const active=o.drones[e.active],replacement=o.drones[e.replacing],known=d=>id=>d.map[id]?{...d.map[id],hazard:d.map[id].readings?.hazard}:null;
 const near=d=>d?.stage==='field'&&d.node===team.node&&!d.edge&&!team.edge&&!d.mission.returning&&['DIRECT','RELAYED'].includes(D().signal(s,d,env));
 const gap=reason=>{if(e.lastGap===reason)return;e.lastGap=reason;e.gaps.push({at:s.tick,reason,node:team.node});e.gaps=e.gaps.slice(-24);env.record('mission','Drone escort coverage gap: '+reason,{missionId:team.id,location:team.node});};
 for(const d of [active,replacement].filter(Boolean))if(!d.mission.returning&&['DIRECT','RELAYED'].includes(D().signal(s,d,env))&&W().route(s,d.node??0,team.node,known(d))!==null)d.mission.target=team.node;
 if(replacement&&near(replacement)){const overlap=!!near(active);if(active&&!active.mission.returning){active.mission.returning=true;active.mission.reason='Physical replacement rendezvous; escort handed over';}e.handoffs.push({at:s.tick,from:active?.id||null,to:replacement.id,node:team.node,overlap});e.handoffs=e.handoffs.slice(-24);env.record('mission','Physical drone escort rendezvous at received expedition location.',{missionId:team.id,from:active?.id||null,to:replacement.id,node:team.node,overlap});e.active=replacement.id;e.replacing=null;e.lastGap=null;return;}
 const reserve=active?.stage==='field'?D().reserve(s,active):0;
 const need=!active||['docked','lost','stranded','carried'].includes(active.stage)||active.mission.returning||active.stage==='field'&&active.battery<=reserve+35;
 if(need&&!replacement){const candidate=Object.values(o.drones).find(d=>d!==active&&d.stage==='docked'&&!d.worker&&d.battery>=90&&d.condition>=65&&o.known[team.node]&&((route)=>route!==null&&d.battery>=25+route.length*11*.85)(W().route(s,0,team.node,id=>o.known[id])));if(candidate){const r=D().start(s,candidate,team.node,env);if(r.ok){candidate.mission.escortId=team.id;candidate.mission.objective='Escort reported expedition '+team.id;candidate.map={...candidate.map};e.replacing=candidate.id;}}}
 if(!near(active)&&!near(replacement))gap(active?.mission.returning?'Outgoing drone must return before coverage can be restored':replacement?'Replacement physically en route':'No safe charged replacement or observed route');else e.lastGap=null;
}
const api={tick};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSDroneEscort=api;
})(globalThis);
