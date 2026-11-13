/* Observer controls affect only presentation; no simulation mutation or remote commands. */
(function(root){'use strict';let auto=false;
function install(anchor,getState,onShot,isPaused){const box=document.createElement('div');box.className='controls spectator-controls';box.innerHTML='<button id="bridge-spectator" aria-pressed="false">Bridge spectator: MANUAL</button><button id="spectator-next">Choose actual activity</button><span id="spectator-status" role="status">LIVE STATE PROJECTION / manual observer</span>';anchor.insertAdjacentElement('beforebegin',box);let last=0,lastSubject=null;
 function manual(){auto=false;const b=box.querySelector('#bridge-spectator');b.setAttribute('aria-pressed','false');b.textContent='Bridge spectator: MANUAL';}
 document.addEventListener('click',e=>{if(e.target.closest('#camfollow,#camroom,#camcycle,#camreview,[data-person]'))manual();});
 document.addEventListener('icarus-observation-manual',manual);
 function pick(){const shot=root.ICARUSCinema.select(getState(),{lastSubject});lastSubject=shot.subject;onShot(shot);box.querySelector('#spectator-status').textContent=(shot.mode==='live-state'?'LIVE STATE PROJECTION':'TELEMETRY / NO CAMERA')+' · '+(shot.subject||'')+' · '+shot.reason;last=Date.now();}
 box.querySelector('#bridge-spectator').onclick=e=>{auto=!auto;e.currentTarget.setAttribute('aria-pressed',String(auto));e.currentTarget.textContent='Bridge spectator: '+(auto?'AUTO':'MANUAL');if(auto)pick();};box.querySelector('#spectator-next').onclick=()=>{manual();pick();};
 setInterval(()=>{if(auto&&!isPaused()&&Date.now()-last>=15000)pick();},1000);
 return {active:()=>auto};
}
root.ICARUSCinemaUI={install};
})(globalThis);
