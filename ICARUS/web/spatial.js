/* Read the physical navigator; presentation never invents successive occupied rooms. */
(function(root){'use strict';
function position(p){if(p.liftRide)return {kind:'vertical',environment:'icarus',node:'LIFT-01',room:null,next:'L:'+p.liftRide.to+':2',fraction:0,lift:true};if(p.expeditionAway)return {kind:'field',environment:p.expeditionAway,node:p.fieldPosition??null,room:null,next:p.fieldMotion?.to??null,fraction:p.fieldMotion?p.fieldMotion.elapsed/p.fieldMotion.duration:0};const n=p.nav;if(!n)return {kind:'room',environment:'icarus',node:'R:'+p.room,room:p.room,fraction:0};const from=n.at||'R:'+p.room,to=n.steps?.[n.index]||from,t=Math.min(1,Math.max(0,n.progress||0));
 // A threshold crossing is a transition, not occupancy of every passed compartment.
 return {kind:from===to&&from.startsWith('R:')?'room':from.startsWith('L:')||from.startsWith('V:')||to.startsWith('L:')||to.startsWith('V:')?'vertical':'corridor',environment:'icarus',node:from,next:to,room:from===to&&from.startsWith('R:')?from.slice(2):null,fraction:t};}
function deck(pos){return (pos.node||'').split(':')[1]?.[0]||null;}
function camera(p){const q=position(p);return {...q,label:q.kind==='room'?q.room:q.kind==='field'?'FIELD / '+q.environment:q.kind==='vertical'?'DECK TRANSFER / '+q.node+' → '+q.next:'CORRIDOR / '+q.node+' → '+q.next};}
function locomotion(p){const m=p.body?.locomotion||'walk';return m==='wheelchair'?.75:m==='prosthetic'?.9:m==='damaged-android'?.55:1;}
const api={position,deck,camera,locomotion};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSSpatial=api;
})(globalThis);
