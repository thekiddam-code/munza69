/* Stable disclosure/scroll identity across legacy live redraws; no world state. */
(function(root){'use strict';
function key(el){if(el.id)return '#'+el.id;const parent=el.parentElement;if(!parent||parent===document.body)return null;const pk=key(parent);if(!pk)return null;return pk+'/'+el.tagName+':'+Array.from(parent.children).filter(x=>x.tagName===el.tagName).indexOf(el);}
function capture(host,ignoreProfiles=false){const states=new Map();for(const el of host.querySelectorAll('details,[id],.psych-roster,.history,.ng-scroll-content')){if(ignoreProfiles&&el.closest('#detail,#horrormonitor'))continue;const k=key(el);if(k&&(el.scrollTop||el.scrollLeft||el.tagName==='DETAILS'))states.set(k,{top:el.scrollTop,left:el.scrollLeft,open:el.tagName==='DETAILS'?el.open:undefined});}const y=scrollY;return ()=>{for(const el of host.querySelectorAll('details,[id],.psych-roster,.history,.ng-scroll-content')){const v=states.get(key(el));if(!v)continue;if(v.open!==undefined)el.open=v.open;el.scrollTop=v.top;el.scrollLeft=v.left;}if(Math.abs(scrollY-y)>1)scrollTo(scrollX,y);};}
root.ICARUSUIContinuity={capture};
})(globalThis);
