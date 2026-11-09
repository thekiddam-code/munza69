/* Extraction moves finite destination material into a held cargo lot before credit. */
(function(root){'use strict';
function init(s){if(!s.logistics)s.logistics={capacity:2600,receipts:[],credited:{},lost:{},extracted:{},nextReceipt:1};return s.logistics;}
function cargoMass(s){const l=init(s),feed=s.economy.feedstock;return ['ore','fuel','nutrients','waterIce'].reduce((n,k)=>n+(feed[k]||0),0)+Object.values(s.remoteCore.missions||{}).reduce((n,m)=>n+Object.values(m?.extracted||{}).reduce((a,b)=>a+b,0),0);}
function needs(s){const e=s.economy,water=e.stock.water;return {fuel:Math.max(0,65-e.feedstock.fuel),ore:Math.max(0,300-e.feedstock.ore),waterIce:water<100?Math.max(0,80-e.feedstock.waterIce):0,nutrients:Math.max(0,100-e.feedstock.nutrients)};}
function extract(s,d,m,key,amount){const l=init(s),available=d.deposits[key]||0,room=Math.max(0,l.capacity-cargoMass(s)),n=Math.max(0,Math.min(amount,available,room));if(!n)return 0;
 d.deposits[key]-=n;d.extracted[key]=(d.extracted[key]||0)+n;m.extracted=m.extracted||{};m.extracted[key]=(m.extracted[key]||0)+n;l.extracted[key]=(l.extracted[key]||0)+n;return n;}
function recover(s,d,m,amount){const l=init(s);m.extracted=m.extracted||{};let room=Math.min(amount,Math.max(0,l.capacity-cargoMass(s))),got=0;
 for(const [key,n] of Object.entries(d.cache||{})){const take=Math.min(room,n);d.cache[key]-=take;m.extracted[key]=(m.extracted[key]||0)+take;room-=take;got+=take;if(room<=0)break;}return got;}
function deposit(s,d,m,economy,success){if(m.rawFinalized)return;m.rawFinalized=true;const l=init(s);
 for(const [key,amount] of Object.entries(m.extracted||{})){
  if(success){economy.creditFeed(s,key,amount,'destination '+d.id+' / mission '+m.id);l.credited[key]=(l.credited[key]||0)+amount;l.receipts.push({id:'RAW-'+l.nextReceipt++,at:s.tick,destination:d.id,mission:m.id,key,amount});}
  else{d.cache=d.cache||{};d.cache[key]=(d.cache[key]||0)+amount;}
  m.extracted[key]=0;
 }l.receipts=l.receipts.slice(-300);
}
function lose(s,m){const l=init(s);if(m.rawFinalized)return;m.rawFinalized=true;for(const [k,n] of Object.entries(m.extracted||{})){l.lost[k]=(l.lost[k]||0)+n;m.extracted[k]=0;}}
function refine(s,economy){init(s);const e=s.economy;if(e.stock.water>=150||e.feedstock.waterIce<=0||e.stock.energy<1||(s.equipment.C06?.condition||0)<40)return 0;
 const n=Math.min(.04,150-e.stock.water,e.feedstock.waterIce);economy.burnFeed(s,'waterIce',n,'ice refining');economy.consume(s,'energy',n*.2,'ice refining');return economy.produce(s,'water',n,'melted recovered/carried water ice');}
function audit(s,universe){const l=init(s),errors=[];for(const key of ['ore','fuel','nutrients','waterIce']){
  const held=Object.values(s.remoteCore.missions||{}).reduce((n,m)=>n+(m?.extracted?.[key]||0),0),cached=universe.bodies(s).reduce((n,d)=>n+(d.cache?.[key]||0),0);
  const difference=(l.extracted[key]||0)-(l.credited[key]||0)-(l.lost[key]||0)-held-cached;if(Math.abs(difference)>1e-6)errors.push('Unreconciled extracted cargo '+key);
 }if(cargoMass(s)>l.capacity+1e-6)errors.push('Dry cargo capacity exceeded');return errors;}
const api={init,cargoMass,needs,extract,recover,deposit,lose,refine,audit};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSLogistics=api;
})(typeof globalThis!=='undefined'?globalThis:this);
