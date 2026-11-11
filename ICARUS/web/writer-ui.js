/* A losing tab observes only; simulation and storage also enforce this policy. */
(function(root){'use strict';
function install(){const bar=document.createElement('aside');bar.id='writer-status';bar.setAttribute('role','status');document.querySelector('header').after(bar);const read=()=>(!root.ICARUSDurable.canWrite()||!root.ICARUSHost?.canWrite()),busy=()=>root.ICARUSBackupUI?.busy();
 function show(){bar.textContent=read()?'READ-ONLY SPECTATOR — another tab owns the voyage, or storage is unavailable. Close the writer and reload here to retry.':'AUTHORITATIVE WRITER — voyage ownership protected';bar.dataset.readonly=String(read());}
 for(const type of ['click','input','change'])document.addEventListener(type,e=>{if(!read()&&!busy())return;const observer=e.target.closest('a[download][href^="blob:"],.operational-console,.command-workspace,#workspace-tools,summary,#camera-scene,#cinematic-chronicle,.spectator-controls,#obscontrols,#reduced-motion,#visualmode,#cutawaymode,#holo-panel,[data-person],[data-page],[data-location],[data-subtab],[data-go],#command-tour,#command-tour-done,#command-explain,#command-alert,#settingsopen,#settingsclose,#exportbackup,#backup-cancel');if(observer)return;e.preventDefault();e.stopImmediatePropagation();},true);
 show();setInterval(show,1000);return bar;}
root.ICARUSWriterUI={install};
})(globalThis);
