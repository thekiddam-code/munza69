/* Presentation boundary, not a security sandbox. Actual remote permissions live on server. */
(function(root){'use strict';let creator=false,render=null;
const selectors='#speed,#pause,#test-pause,#command-test,#command-release,#area-settings-testing,#area-settings-advanced,#director-entry,#director-modal,#reset,#calendar-zone,#knowledge-actor,#knowledge-read,.audit,#detail,#horrormonitor,#crew,#roomdetail,#observer,#world,#log,#medical-overview,.crew-impact,.disputes,#crewimpact,#conflicts,#decisions,#focusbar,#viewport,#living-frontier-controls [data-autonomy],#frontier-controls [data-frontier=toggle],#soldirectives,#emergencies,#liveincident,#living-frontier-controls';
function tag(){for(const el of document.querySelectorAll(selectors))el.dataset.creatorOnly='true';for(const el of document.querySelectorAll('#page-settings [data-subtab=testing],#page-settings [data-subtab=advanced],[data-remote-action*=autonomy]'))el.dataset.creatorOnly='true';}
function apply(){document.body.dataset.bridgeMode=creator?'creator':'bridge';const b=document.getElementById('bridge-mode-status');if(b)b.textContent=creator?'CREATOR MODE · Ctrl + Shift + F12 to return':'BRIDGE MODE';tag();document.dispatchEvent(new CustomEvent('icarus-mode',{detail:{creator}}));render?.();}
function install(callback){render=callback;const b=document.createElement('aside');b.id='bridge-mode-status';b.setAttribute('role','status');document.querySelector('header').after(b);creator=false;apply();let queued=false;new MutationObserver(()=>{if(queued)return;queued=true;requestAnimationFrame(()=>{queued=false;tag();});}).observe(document.getElementById('icarus-pages')||document.body,{childList:true,subtree:true});
 document.addEventListener('keydown',e=>{if(e.ctrlKey&&e.shiftKey&&e.key==='F12'){e.preventDefault();creator=!creator;apply();}},true);
 for(const type of ['click','change','input'])document.addEventListener(type,e=>{if(!creator&&e.target.closest('[data-creator-only=true]')){e.preventDefault();e.stopImmediatePropagation();}},true);
}
root.ICARUSBridgeMode={install,get creator(){return creator;}};
})(globalThis);
