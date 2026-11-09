/* Finite stores, explicit conversion inputs, bounded ledgers and conservation audit. */
(function(root){'use strict';
const keys=['food','water','oxygen','energy','medical','spares','tools','lab'];
// Persist compensated sums: small per-minute flows must remain auditable after millions of transactions.
function add(e,domain,key,n){e[domain]=e[domain]||{};e.compensation=e.compensation||{};const c=e.compensation[domain]||(e.compensation[domain]={}),old=e[domain][key]||0,y=n-(c[key]||0),next=old+y;c[key]=(next-old)-y;e[domain][key]=next;}
function totals(s){const e=s.economy||{},t={};for(const k of keys)t[k]=(e.stock?.[k]||0)+(s.operations?.reserve?.[k]||0)+(s.interactions?.supplies?.[k]||0)+(k==='medical'?(s.tissueRepair?.cartridges||0):0);
 for(const m of Object.values(s.remoteCore?.missions||{}))if(m)for(const k of keys)t[k]+=m.cargo?.[k]||0;
 return t;}
function init(s){if(s.economy)return s.economy;
 s.operations=s.operations||{reserve:{food:120,lab:60,tools:60,spares:40},transfers:[]};s.interactions=s.interactions||{supplies:{food:30,lab:24,tools:20,spares:16}};s.tissueRepair=s.tissueRepair||{cartridges:12,condition:96,cycles:0,activePatient:null};
 const e=s.economy={version:1,stock:{water:150,oxygen:120,energy:120},feedstock:{fuel:150,ore:1200,nutrients:600,wasteWater:0,co2:0,organicWaste:0,waterIce:200},capacity:{water:200,oxygen:180,energy:180,food:160,medical:20,spares:70,tools:70,lab:80},produced:{},consumed:{},disposed:{},imports:{},history:[],decisions:[],lastTick:-1,mode:'normal',initial:null};
 e.initial=totals(s);e.feedstockInitial={...e.feedstock};e.feedstockUsed={};e.feedstockImported={};return e;}
function note(s,kind,key,amount,source){const e=init(s);if(amount<=0)return;e.ledger=e.ledger||{};const id=JSON.stringify([kind,key,source]);const row=e.ledger[id]||(e.ledger[id]={kind,key,source,amount:0,count:0,first:s.tick,last:s.tick});const y=amount-(row.compensation||0),next=row.amount+y;row.compensation=(next-row.amount)-y;row.amount=next;row.count++;row.last=s.tick;e.history.push({at:s.tick,kind,key,amount,source});e.history=e.history.slice(-200);}
function remove(s,key,amount){let left=amount,e=init(s);for(const obj of [e.stock,s.operations?.reserve,s.interactions?.supplies]){if(!obj)continue;const n=Math.min(left,obj[key]||0);if(n>0){obj[key]-=n;left-=n;}if(left<1e-12)break;}
 if(key==='medical'&&left>0){const n=Math.min(left,s.tissueRepair.cartridges);s.tissueRepair.cartridges-=n;left-=n;}return amount-left;}
function consume(s,key,amount,source){const e=init(s),got=remove(s,key,amount);add(e,'consumed',key,got);note(s,'consume',key,got,source);return got;}
function externalConsumption(s,key,amount,source){const e=init(s);add(e,'consumed',key,amount);note(s,'consume',key,amount,source);if(key==='food')creditFeed(s,'organicWaste',amount,'recovered meal residue');if(key==='medical'){creditFeed(s,'wasteWater',amount,'recovered clinical rinse');creditFeed(s,'organicWaste',amount,'spent culture medium');}if(['tools','lab','spares'].includes(key))creditFeed(s,'ore',amount*.98,'recovered process scrap');}
function feed(s,key,amount,source="production conversion"){const e=init(s),n=Math.min(amount,e.feedstock[key]||0);e.feedstock[key]-=n;add(e,'feedstockUsed',key,n);note(s,'feedstock_use',key,n,source);return n;}
function produce(s,key,amount,source){const e=init(s),room=Math.max(0,e.capacity[key]-totals(s)[key]),n=Math.min(amount,room);if(n<=0)return 0;
 if(key==='medical')s.tissueRepair.cartridges+=n;else if(['food','lab','tools','spares'].includes(key))s.operations.reserve[key]=(s.operations.reserve[key]||0)+n;else e.stock[key]=(e.stock[key]||0)+n;
 e.productionSources=e.productionSources||{};add(e,'productionSources',source,n);add(e,'produced',key,n);note(s,'produce',key,n,source);return n;}
function moveToCargo(s,cargo,key,amount){const e=init(s);if(totals(s)[key]+1e-9<amount)return false;const n=remove(s,key,amount);cargo[key]=(cargo[key]||0)+n;note(s,'transfer',key,n,'ship to expedition cargo');return Math.abs(n-amount)<1e-9;}
function cargoUse(s,m,key,amount){const e=init(s),got=Math.min(m.cargo?.[key]||0,amount);m.cargo[key]-=got;add(e,'consumed',key,got);note(s,'consume',key,got,'field metabolism '+m.id);return got;}
function returnCargo(s,m){const e=init(s);for(const [k,n] of Object.entries(m.cargo||{})){if(['food','lab','tools','spares'].includes(k))s.operations.reserve[k]=(s.operations.reserve[k]||0)+n;else e.stock[k]=(e.stock[k]||0)+n;note(s,'transfer',k,n,'returned expedition '+m.id);m.cargo[k]=0;}}
function loseCargo(s,m){const e=init(s);for(const [k,n] of Object.entries(m.cargo||{})){add(e,'disposed',k,n);note(s,'loss',k,n,'lost expedition '+m.id);m.cargo[k]=0;}}
function audit(s){const e=init(s),actual=totals(s),errors=[];for(const k of keys){const expected=(e.initial[k]||0)+(e.produced[k]||0)+(e.imports[k]||0)-(e.consumed[k]||0)-(e.disposed[k]||0);if(!Number.isFinite(actual[k])||actual[k]<-1e-7||Math.abs(expected-actual[k])>1e-6)errors.push({key:k,expected,actual:actual[k],difference:actual[k]-expected});}
 for(const pool of [e.stock,s.operations?.reserve,s.interactions?.supplies,{medical:s.tissueRepair?.cartridges},...Object.values(s.remoteCore?.missions||{}).map(m=>m?.cargo)])for(const [key,value] of Object.entries(pool||{}))if(!Number.isFinite(value)||value<-1e-7)errors.push({pool:'physical inventory',key,actual:value});
 for(const k of Object.keys(e.feedstock)){const expected=(e.feedstockInitial[k]||0)+(e.feedstockImported[k]||0)-(e.feedstockUsed[k]||0);if(e.feedstock[k]<-1e-7||Math.abs(expected-e.feedstock[k])>1e-6)errors.push({feedstock:k,expected,actual:e.feedstock[k]});}if(s.teamLog){const suits=s.teamLog.suits+s.teamLog.lostSuits+Object.values(s.remoteCore?.missions||{}).reduce((n,m)=>n+(m?.suits||0),0);if(suits!==6||s.teamLog.suits<0||s.teamLog.lostSuits<0)errors.push({key:'expedition suits',expected:6,actual:suits});}return errors;}
function creditFeed(s,key,amount,source){const e=init(s);e.feedstock[key]=(e.feedstock[key]||0)+amount;add(e,'feedstockImported',key,amount);note(s,'recover',key,amount,source);}
function tick(s,env){const e=init(s);if(e.lastTick===s.tick)return;e.lastTick=s.tick;
 const eq=id=>Math.max(0,Math.min(1,(s.equipment?.[id]?.condition??0)/100));
 // Reactor converts carried fuel; solar input is an explicit external energy source.
 const wanted=Math.max(0,e.capacity.energy-e.stock.energy);
 const solar=Math.min(wanted,.20*eq('C07'));produce(s,'energy',solar,'incident starlight / installed collector');
 const fuel=Math.min(Math.max(0,(e.capacity.energy-e.stock.energy)/120),.002*eq('C08')*eq('C07'));
 produce(s,'energy',feed(s,'fuel',fuel)*120,'reactor fuel conversion');
 const alive=s.crew.filter(p=>!p.expeditionAway).length,energyNeed=.065+alive*.002;
 const powered=consume(s,'energy',energyNeed,'ship hotel load')>=energyNeed-1e-9;
 const pump=eq('C09'),fabricator=eq('C06'),galley=eq('A04'),lab=eq('B01');
 if(powered){
  const water=Math.min(.06*pump,e.capacity.water-totals(s).water,e.feedstock.wasteWater);if(water>0)produce(s,'water',feed(s,'wasteWater',water),'wastewater reclamation');
  const oxygen=Math.min(.05*pump,e.capacity.oxygen-totals(s).oxygen,e.feedstock.co2);if(oxygen>0)produce(s,'oxygen',feed(s,'co2',oxygen),'closed-cycle CO2 regeneration');
  // Normalized mass units: 1 water -> .88 oxygen, .12 hydrogen vented.
  // Replenish expedition/leak losses only with actual water and electrical work.
  if(e.stock.oxygen<90&&e.stock.water>25&&pump>.4&&fabricator>.4){
   const input=Math.min(.03*pump,e.stock.water-25,(90-e.stock.oxygen)/.88,e.stock.energy/.8);
   if(input>0){const used=consume(s,'water',input,'oxygen electrolysis');consume(s,'energy',used*.8,'oxygen electrolysis');produce(s,'oxygen',used*.88,'water electrolysis; hydrogen vented');note(s,'byproduct_loss','hydrogen',used*.12,'water electrolysis');}
  }
  for(const [key,rate,source,factor] of [['food',.5,'organicWaste',galley],['spares',.012,'ore',fabricator],['tools',.20,'ore',fabricator],['lab',.20,'ore',lab]]){
   const deficit=Math.max(0,e.capacity[key]-totals(s)[key]),want=Math.min(deficit,rate*factor,e.stock.energy/.06);let n=feed(s,source,want);
   if(key==='food'&&n<want)n+=feed(s,'nutrients',want-n);
   if(n){consume(s,'energy',n*.06,'production '+key);produce(s,key,n,'conversion from '+source+(key==='food'?' / nutrients':''));}
  }
  if(s.tissueRepair.cartridges<e.capacity.medical&&s.tick%240===0&&lab>.4&&fabricator>.4&&e.feedstock.nutrients>=1&&e.stock.water>=1&&e.stock.energy>=1){feed(s,'nutrients',1);consume(s,'water',1,'sterile cartridge culture');consume(s,'energy',1,'sterilization');produce(s,'medical',1,'sterile cartridge culture from nutrients and water');}
 }
 e.rationFactor=totals(s).food<10?.75:1;
 let deprived=false;
 for(const [key,perPerson] of [['food',.0007],['water',.0014],['oxygen',.001]]){
  const want=alive*perPerson*(key==='food'?e.rationFactor:1),got=consume(s,key,want,'crew metabolism');if(got<want-1e-9)deprived=true;
  const waste=key==='food'?'organicWaste':key==='water'?'wasteWater':'co2';creditFeed(s,waste,got,'recovered metabolic output');
 }
 // Physical hull breaches vent stored oxygen; the loss remains in the ledger.
 if(Object.values(s.physicalWorld?.rooms||{}).some(r=>r.atmosphere?.breach))consume(s,'oxygen',.03,'hull leak');
 const t=totals(s),mode=deprived||t.energy<10||t.water<5||t.oxygen<5?'survival':t.food<10||t.lab<3||t.spares<3?'rationing':'normal';
 if(mode!==e.mode){e.mode=mode;e.decisions.push({at:s.tick,mode,reason:'Measured stores and life-support demand',totals:t});e.decisions=e.decisions.slice(-100);if(env.emit)env.emit('SOL resource priority: '+mode+'.','system');}
 e.shortage=deprived;e.allowResearch=mode!=='survival'&&t.energy>=10&&t.lab>=1;e.allowLaunch=mode==='normal'&&t.energy>=15;
 if(deprived&&s.tick%30===0&&env.hurt)for(const p of s.crew.filter(p=>!p.expeditionAway))env.hurt(p,.7,'life-support resource shortage');
 if(!powered)s.power=0;
}
const api={keys,burnFeed:(s,k,n,source)=>feed(s,k,n,source),init,totals,consume,externalConsumption,produce,moveToCargo,cargoUse,returnCargo,loseCargo,audit,creditFeed,tick};if(typeof module==='object'&&module.exports)module.exports=api;else root.ICARUSEconomy=api;
})(typeof globalThis!=='undefined'?globalThis:this);
