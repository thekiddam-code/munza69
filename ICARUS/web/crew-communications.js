/* Hearsay is a sourced communication claim, never a replacement for physical evidence. */
(function(root){'use strict';
function share(s,p,q,f,env){const K=root.ICARUSKnowledge;if(!f||['private','classified'].includes(f.disclosure)||f.kind==='reported-claim'||!K.known(s,p.name,f.id)||!K.can(s,p.name,q.name,'conversation',env.channel))return false;
 const claims=Object.values(s.knowledge.facts).filter(x=>x.kind==='reported-claim'&&x.data.premise===f.id&&K.known(s,q.name,x.id));
 // A later encounter can supply the original report and correct the listener's earlier interpretation.
 if(claims.length){const sent=K.speak(s,p.name,q.name,f.id,env.channel);if(sent)for(const claim of claims){const e=K.entry(s,q.name,claim.id);e.review={at:s.tick,sourceFactId:f.id,status:'withdrawn interpretation; original report received'};}return sent;}
 const uncertain=f.confidence<.7&&(p.stress||0)>60,draw=root.ICARUSUniverse.draw(s.universe?.seed??1,'interpretation:'+p.name+':'+q.name+':'+f.id);
 if(!uncertain||draw>=.2)return K.speak(s,p.name,q.name,f.id,env.channel);
 const text=p.name+' gave '+q.name+' a tentative, potentially exaggerated interpretation of an uncertain report: '+f.text.slice(0,160)+'. This is hearsay, not a confirmed change in conditions.';
 const r=env.record('social',text,[p.name,q.name],{activity:'conversation',topic:'interpretation',premise:f.id,epistemicStatus:'reported-claim'},{kind:'reported-claim',confidence:Math.min(.4,f.confidence),disclosure:'shareable'});
 const id=s.knowledge.byKey[r?.id];return id&&K.known(s,q.name,id)?{record:r}:false;
}
function review(s,name,received){const K=root.ICARUSKnowledge;if(!received||!K.known(s,name,received.id))return 0;const facts=received.kind==='reported-claim'?[received]:Object.keys(s.knowledge.actors[name].entries).map(id=>s.knowledge.facts[id]).filter(f=>f?.kind==='reported-claim'&&f.data.premise===received.id);let n=0;for(const claim of facts){if(!K.known(s,name,claim.data.premise))continue;const e=K.entry(s,name,claim.id);if(e.review)continue;e.review={at:s.tick,sourceFactId:claim.data.premise,status:'withdrawn interpretation; original report received'};n++;}return n;}
function classification(f){return f.kind==='reported-claim'?'reported claim':f.kind==='inference'?'inference':f.acquisition?.method==='direct-observation'?'direct observation':f.acquisition?.method==='recorded-evidence'?'documented record':'received report';}
const api={share,review,classification};if(typeof module==='object'&&module.exports){root.ICARUSKnowledge=require('./knowledge');root.ICARUSUniverse=require('./universe');module.exports=api;}else root.ICARUSCrewCommunications=api;
})(globalThis);
