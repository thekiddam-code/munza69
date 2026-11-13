/* Actual local search decisions; display frames never call this controller. */
(function(root){'use strict';
function tick(s,env){if(s.observationTick===s.tick)return;s.observationTick=s.tick;for(const p of s.crew){let a=p.socialSearch;if(!root.ICARUSCrewLife.available(p)||root.ICARUSSpatial.position(p).kind!=='room'){if(a&&!['finished','interrupted'].includes(a.phase)){a.phase='interrupted';a.at=s.tick;a.endedAt=s.tick;}continue;}
 if(!/seeking.*(conversation|company)|searching.*conversation/i.test(p.goal||p.task||'')){if(a&&a.phase!=='interrupted'){a.phase='finished';a.at=s.tick;}continue;}
 if(!a||['finished','interrupted'].includes(a.phase)||a.activity!==p.goal)a=p.socialSearch={activity:p.goal,startedAt:s.tick,phaseAt:s.tick,phase:'looking',at:s.tick};a.at=s.tick;
 if(p.conversation?.until>s.tick){a.phase='talking';a.sourceId=p.conversation.sourceId;continue;}
 if(a.phase==='talking'){a.phase='finished';continue;}
 const present=s.crew.filter(q=>q!==p&&root.ICARUSCrewLife.available(q)&&env.coLocated(p,q));const q=present.find(q=>q.name===a.target)||present.sort((x,y)=>(p.relationships?.[y.name]||0)-(p.relationships?.[x.name]||0)||x.name.localeCompare(y.name))[0];
 if(s.tick-a.startedAt>=14){a.phase='giving-up';a.target=null;a.targetPoint=null;if(s.tick-a.startedAt>=16)p.taskMinutes=0;continue;}
 if(s.tick-a.startedAt<2)continue;
 if(!q){a.phase='waiting';a.target=null;a.targetPoint=null;continue;}
 if(a.target!==q.name){a.target=q.name;a.phase='approaching';a.phaseAt=s.tick;const i=s.crew.filter(x=>root.ICARUSSpatial.position(x).room===p.room).indexOf(q),at=root.ICARUSObservation.anchor(root.ICARUSEmbodiment.pose(q,root.ICARUSSpatial.position(q),false,s.tick).kind,Math.max(0,i));a.targetPoint={x:Math.max(48,at.x-37),y:at.y};}
 if(s.tick-a.phaseAt<3)continue;const r=env.talk(p,q);if(r?.id){a.phase='talking';a.sourceId=r.id;p.conversation.speaker=true;q.conversation.speaker=false;}else a.phase='waiting';
 }}
const api={tick};if(typeof module==='object'&&module.exports){root.ICARUSCrewLife=require('./crew-life');root.ICARUSSpatial=require('./spatial');root.ICARUSObservation=require('./observation-model');module.exports=api;}else root.ICARUSCrewObservation=api;
})(globalThis);
