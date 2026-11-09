/* Stateless seeded sector descriptors; only sensor-discovered sectors are persisted. */
(function(root){'use strict';
function hash(seed,key){let h=(seed>>>0)^2166136261;for(const c of key){h^=c.charCodeAt(0);h=Math.imul(h,16777619);}h^=h>>>16;h=Math.imul(h,2246822507);return (h^(h>>>13))>>>0;}
function draw(seed,key){return hash(seed,key)/4294967296;}
function sector(seed,x,y){
 const id='SYS:'+x+':'+y,r=n=>draw(seed,id+':'+n);
 if((x||y)&&r('presence')<.24)return {id,x,y,empty:true,bodies:[]};
 const count=r('barren')<.12?0:2+Math.floor(r('count')*5),bodies=[];
 for(let i=0;i<count;i++){
  const bid=id+'/'+i,b=n=>draw(seed,bid+':'+n),t=b('type');
  const type=t<.28?'planet':t<.47?'moon':t<.72?'asteroid field':t<.87?'derelict':t<.97?'anomaly':'rare installation';
  const hazard=b('hazard')*.85,temperature=Math.round(b('temp')*250-170),angle=b('angle')*Math.PI*2,radius=.12+b('radius')*.55;
  const deposits={ore:0,waterIce:0,fuel:0,nutrients:0};
  if(type==='asteroid field'){deposits.ore=40+Math.floor(b('ore')*90);deposits.waterIce=b('ice')>.4?30+Math.floor(b('water')*60):0;deposits.fuel=b('fuel')<.25?25:0;}
  if(type==='planet'||type==='moon'){deposits.waterIce=temperature<0?20+Math.floor(b('water')*90):0;deposits.ore=b('ore')<.4?30:0;deposits.nutrients=b('bio')<.15?30:0;}
  if(type==='derelict'||type==='rare installation'){deposits.ore=20+Math.floor(b('ore')*70);deposits.fuel=12+Math.floor(b('fuel')*45);deposits.nutrients=b('cargo')<.4?20:0;}
  bodies.push({id:bid,systemId:id,name:type+' '+(i+1)+' / '+x+','+y,type,x:x+Math.cos(angle)*radius,y:y+Math.sin(angle)*radius,temperature,hazard,interest:b('interest'),distress:b('distress')<.045,biological:b('bio')<.2,composition:b('spectrum')<.5?'silicate':'carbonate',deposits,initialDeposits:{...deposits},extracted:{},surveyed:false,visited:false,sampled:false,signalResolved:false,conditionsRevision:0});
 }
 return {id,x,y,empty:false,name:'Contact '+x+','+y,bodies};
}
function init(s){if(s.universe)return s.universe;
 const seed=hash(s.entropy?.seed||1,'icarus-universe');
 s.universe={version:1,seed,systems:{},scanned:{},lastScan:-1,events:[],visitedCount:1};
 const home=sector(seed,0,0);home.name='ICARUS origin';home.bodies.unshift({id:'HOME',systemId:'SYS:0:0',name:'Legacy derelict / asteroid staging',type:'home orbit',x:0,y:0,hazard:0,interest:0,deposits:{},initialDeposits:{},extracted:{},visited:true,surveyed:true,sampled:true,signalResolved:true});s.universe.systems[home.id]=home;return s.universe;
}
function bodies(s){return Object.values(init(s).systems).flatMap(x=>x.bodies);}
function find(s,id){return bodies(s).find(x=>x.id===id);}
function scan(s,x,y){const u=init(s),cx=Math.round(x),cy=Math.round(y),found=[];
 for(let dx=-1;dx<=1;dx++)for(let dy=-1;dy<=1;dy++){
  const sx=cx+dx,sy=cy+dy,key=sx+','+sy;if(u.scanned[key])continue;u.scanned[key]=true;
  const system=sector(u.seed,sx,sy);if(u.systems[system.id])continue;u.systems[system.id]=system;found.push(system.id);
 }u.lastScan=s.tick;return found;
}
function environment(s,d){const u=init(s),day=Math.floor(s.tick/1440),key=d.id+':weather:'+day;
 const factor=(draw(u.seed,key)-.5)*.18;return Math.max(0,Math.min(.95,d.hazard+factor));}
function audit(s){const u=init(s),errors=[];for(const [id,sys] of Object.entries(u.systems)){if(id!==sys.id)errors.push('System identity mismatch');for(const d of sys.bodies)for(const [key,initial] of Object.entries(d.initialDeposits||{})){const remaining=d.deposits[key]||0,extracted=d.extracted[key]||0;if(remaining<0||Math.abs(initial-remaining-extracted)>1e-7)errors.push('Deposit conservation '+d.id+' '+key);}}return errors;}
const api={hash,draw,sector,init,bodies,find,scan,environment,audit};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSUniverse=api;
})(typeof globalThis!=='undefined'?globalThis:this);
