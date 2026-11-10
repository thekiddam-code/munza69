/* Wall time drives pacing; only existing simulation steps mutate physical history. */
(function(root){'use strict';
const MINUTE=60000,DAY=86400000,formatters=new Map();
function zone(z){try{new Intl.DateTimeFormat('en',{timeZone:z}).format(0);return z;}catch{throw new Error('Invalid IANA timezone');}}
function parts(ms,z){let f=formatters.get(z);if(!f){f=new Intl.DateTimeFormat('en-CA',{timeZone:zone(z),year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'});formatters.set(z,f);}const a=Object.fromEntries(f.formatToParts(ms).filter(x=>x.type!=='literal').map(x=>[x.type,Number(x.value)]));return {y:a.year,m:a.month,d:a.day,h:a.hour,min:a.minute,sec:a.second};}
function key(p){return [p.y,String(p.m).padStart(2,'0'),String(p.d).padStart(2,'0')].join('-');}
function weekday(p){return new Date(Date.UTC(p.y,p.m-1,p.d)).getUTCDay();}
function week(p){const d=new Date(Date.UTC(p.y,p.m-1,p.d));d.setUTCDate(d.getUTCDate()-(d.getUTCDay()+6)%7);return d.toISOString().slice(0,10);}
function easter(y){const a=y%19,b=Math.floor(y/100),c=y%100,d=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),g=Math.floor((b-f+1)/3),h=(19*a+b-d-g+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-h-k)%7,m=Math.floor((a+11*h+22*l)/451),n=h+l-7*m+114;return {y,m:Math.floor(n/31),d:n%31+1};}
function holiday(p){const w=weekday(p),nth=Math.floor((p.d-1)/7)+1,last=p.d+7>new Date(Date.UTC(p.y,p.m,0)).getUTCDate();
 const sync=(p.m===1&&p.d===1)?'New Year’s Day':p.m===5&&w===1&&last?'Memorial Day':p.m===7&&p.d===4?'Independence Day':p.m===9&&w===1&&nth===1?'Labor Day':p.m===10&&p.d===31?'Halloween':p.m===11&&p.d===11?'Veterans Day':p.m===11&&w===4&&nth===4?'Thanksgiving':p.m===12&&p.d===24?'Christmas Eve':p.m===12&&p.d===25?'Christmas Day':null;
 const e=easter(p.y),recognized=p.m===1&&w===1&&nth===3?'Martin Luther King Jr. Day':p.m===2&&p.d===14?'Valentine’s Day':p.m===2&&w===1&&nth===3?'Presidents’ Day':p.m===3&&p.d===17?'St. Patrick’s Day':p.m===e.m&&p.d===e.d?'Easter':p.m===6&&p.d===19?'Juneteenth':p.m===10&&w===1&&nth===2?'Columbus Day / Indigenous Peoples’ Day':p.m===12&&p.d===31?'New Year’s Eve':null;
 return {name:sync||recognized,synchronized:!!sync,rate:sync?1:4,id:(sync||recognized)?key(p)+':'+(sync||recognized):null};
}
function atmosphere(ms,z){const p=parts(ms,z),monday=new Date(week(p)+'T00:00:00Z');monday.setUTCDate(monday.getUTCDate()+4);const lunarDays=(ms-Date.UTC(2000,0,6,18,14))/DAY,phase=((lunarDays/29.530588853)%1+1)%1,full=Math.abs(phase-.5)<.035;return {october:p.m===10,friday13Week:monday.getUTCDate()===13,fullMoon:full,lunarPhase:phase,lunarModel:'Approximate mean synodic Earth cycle; not an astronomical ephemeris',presentationOnly:true};}
function nextMidnight(ms,z){const date=key(parts(ms,z));let lo=ms,hi=ms+27*3600000;while(hi-lo>1){const mid=Math.floor((lo+hi)/2);if(key(parts(mid,z))===date)lo=mid;else hi=mid;}return hi;}
function init(s,now,z){if(s.calendar)return s.calendar;if(!Number.isFinite(now))throw new Error('Finite real timestamp required');z=zone(z||Intl.DateTimeFormat().resolvedOptions().timeZone||'UTC');const p=parts(now,z);return s.calendar={version:1,timeZone:z,wallCursor:now,displayMs:now,carry:0,lastSeen:now,episodeKey:week(p),visitedWeeks:{[week(p)]:true},occurrences:{},pending:[],corrections:[],recovery:{discardedMs:0,rollbackCount:0},mode:'wall',maxCatchupMs:6*3600000};}
function sync(s,c,at,env){const p=parts(at,c.timeZone),h=holiday(p),wk=week(p);
 if(wk!==c.episodeKey&&!c.visitedWeeks[wk]){env.boundary?.(s,c.episodeKey,wk);c.visitedWeeks[wk]=true;c.episodeKey=wk;}
 if(h.id&&!c.occurrences[h.id]){c.occurrences[h.id]={id:h.id,name:h.name,date:key(p),synchronized:h.synchronized,at,simTick:s.tick,status:'observed'};c.pending.push(h.id);if(h.synchronized){c.corrections.push({at,before:c.displayMs,after:at,id:h.id,simTick:s.tick});c.corrections=c.corrections.slice(-64);c.displayMs=at;}env.observance?.(c.occurrences[h.id]);}
 return h;
}
function advance(s,now,env={},options={}){const c=init(s,now,options.timeZone);if(!Number.isFinite(now))throw new Error('Finite real timestamp required');const max=options.maxTicks??120;if(!Number.isInteger(max)||max<0)throw new Error('Invalid work budget');
 if(now<c.lastSeen){c.recovery.rollbackCount++;return {ticks:0,rollback:true,backlogMs:Math.max(0,c.lastSeen-c.wallCursor)};}c.lastSeen=now;
 if(now-c.wallCursor>c.maxCatchupMs){const skipped=now-c.wallCursor-c.maxCatchupMs;c.wallCursor=now-c.maxCatchupMs;c.recovery.discardedMs+=skipped;env.gap?.(skipped);}
 let ticks=0;sync(s,c,c.wallCursor,env);
 if(options.paused){c.wallCursor=now;sync(s,c,now,env);return {ticks:0,paused:true,backlogMs:0};}
 while(c.wallCursor<now&&ticks<max){const h=holiday(parts(c.wallCursor,c.timeZone)),end=Math.min(now,nextMidnight(c.wallCursor,c.timeZone)),needed=(MINUTE-c.carry)/h.rate,dt=Math.min(end-c.wallCursor,needed);
  c.displayMs+=dt*h.rate;c.carry+=dt*h.rate;c.wallCursor+=dt;sync(s,c,c.wallCursor,env);
  if(c.carry>=MINUTE-1e-5){c.carry=Math.max(0,c.carry-MINUTE);env.step?.();ticks++;}
 }
 return {ticks,backlogMs:Math.max(0,now-c.wallCursor),rate:holiday(parts(c.wallCursor,c.timeZone)).rate};
}
function configure(s,z,now,env={}){zone(z);const c=init(s,now,z);if(c.wallCursor<now)throw new Error('Drain pending wall time before changing timezone');c.timeZone=z;sync(s,c,now,env);return c;}
function view(s,now){const c=s.calendar;if(!c)return null;const h=holiday(parts(now,c.timeZone));return {date:key(parts(c.displayMs,c.timeZone)),time:parts(c.displayMs,c.timeZone),timeZone:c.timeZone,rate:h.rate,holiday:h.name,week:week(parts(now,c.timeZone)),archiveWeek:c.episodeKey,atmosphere:atmosphere(now,c.timeZone),recovery:c.recovery};}
const api={parts,key,week,holiday,easter,atmosphere,nextMidnight,init,advance,configure,view};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSCalendar=api;
})(globalThis);
