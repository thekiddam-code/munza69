/* Optional private preferences editor. Never appears in Bridge telemetry or invents a voyage event. */
(function(root){'use strict';
function preferences(host,s,p,save){if(!root.ICARUSBridgeMode?.creator)return;const box=document.createElement('details'),summary=document.createElement('summary');summary.textContent='PRIVATE RELATIONSHIP PREFERENCES / CREATOR';box.append(summary);
 const note=document.createElement('p');note.textContent='Optional character configuration. No orientation or adulthood is inferred. Mutual preferences, gradual trust and an actual meeting are required; this does not create consent or a relationship.';box.append(note);
 const label=document.createElement('label'),adult=document.createElement('input');adult.type='checkbox';adult.checked=p.adult===true;label.append(adult,document.createTextNode(' Explicitly adult character'));box.append(label);
 const peers=document.createElement('select');peers.multiple=true;peers.setAttribute('aria-label','Willing to consider a personal relationship with');for(const q of s.crew){if(q.name===p.name)continue;const o=document.createElement('option');o.value=q.name;o.textContent=q.name;o.selected=!!p.romanticInterest?.includes(q.name);peers.append(o);}box.append(peers);
 const button=document.createElement('button');button.textContent='Save private preferences';button.onclick=()=>{if(!root.ICARUSBridgeMode?.creator)return;p.adult=adult.checked;p.romanticInterest=[...peers.selectedOptions].map(o=>o.value);const m=s.crewSocial?.people[p.name];if(m)for(const [peer,consent] of Object.entries(m.consents))if(!p.adult||!p.romanticInterest.includes(peer)){consent.accepted=false;consent.withdrawnAt=s.tick;consent.withdrawal='Private preference configuration changed';}save();note.textContent='Private preferences saved. No conversation or consent event was manufactured.';};box.append(button);host.append(box);
}
root.ICARUSCrewLifeUI={preferences};
})(globalThis);
