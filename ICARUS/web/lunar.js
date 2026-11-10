/* Offline geocentric phase calculation; no simulation effects or network requests. */
(function(root){'use strict';
const A=typeof module==='object'&&module.exports?require('./vendor/astronomy'):root.Astronomy,cache=new Map(),DAY=86400000;
function supported(ms){return Number.isFinite(ms)&&ms>=Date.UTC(2000,0,1)&&ms<Date.UTC(2101,0,1);}
function moons(ms){if(!supported(ms))return [];const d=new Date(ms),key=d.getUTCFullYear()+'-'+d.getUTCMonth();if(cache.has(key))return [...cache.get(key)];const start=Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),1)-2*DAY,end=Date.UTC(d.getUTCFullYear(),d.getUTCMonth()+1,1)+2*DAY,result=[];let at=start;
 while(at<end){const f=A.SearchMoonPhase(180,new Date(at),40);if(!f||f.date.getTime()>=end)break;const t=f.date.getTime();result.push(t);at=t+1000;}
 if(cache.size>=24)cache.delete(cache.keys().next().value);cache.set(key,result);return [...result];
}
function view(ms,dateKey){if(!supported(ms))return {fullMoon:false,lunarPhase:null,fullMoonAt:null,lunarSupported:false,lunarModel:'Unsupported date; supported UTC years 2000–2100'};const full=moons(ms).find(t=>dateKey(t)===dateKey(ms));return {fullMoon:full!==undefined,lunarPhase:A.MoonPhase(new Date(ms))/360,fullMoonAt:full??null,lunarSupported:true,lunarModel:'Astronomy Engine 2.1.19 geocentric longitude phase; full-moon local calendar date (UTC years 2000–2100)'};}
const api={view,moons,supported};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSLunar=api;
})(globalThis);
