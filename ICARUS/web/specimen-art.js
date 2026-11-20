/* Original small pixel organisms. Presentation is read-only; positions come from the world. */
(function(root){'use strict';
const colors={grazer:'#a6c89a',colony:'#88d5c6',defender:'#ce9a7b'};
function organism(c,o,x,y,time){const living=o.health>0,active=living&&!/rest|dead|awaiting/.test(o.pose),step=active?Math.floor(time/220)%2:0;const color=colors[o.family]||'#9ba5ac';
 c.save();c.translate(Math.round(x),Math.round(y));c.fillStyle='#06181b';c.fillRect(-10,0,22,3);c.fillStyle=living?color:'#687578';
 if(o.family==='colony'){for(let i=0;i<5;i++){const h=5+(i*7)%12;c.fillRect(i*4-9,-h,3,h);c.fillStyle=living?(i%2?'#a6e2cf':'#7bafc2'):'#687578';c.fillRect(i*4-10,-h-2,5,3);}if(living&&active){c.globalAlpha=.18+step*.1;c.fillStyle='#8ee9cc';c.fillRect(-12,-17,25,20);}}
 else {c.fillRect(-9,-7,17,6);for(let i=0;i<4;i++){c.fillRect(i*4-8,-9,3,3);c.fillRect(i*5-9,step?-1:-2,2,3);}c.fillStyle=o.family==='defender'?'#875b62':'#668479';c.fillRect(-7,-6,12,2);c.fillStyle=living?'#e6e6a7':'#273b40';c.fillRect(7,-6,2,2);if(o.family==='defender'){c.fillStyle='#c7b29a';c.fillRect(-5,-12,2,4);c.fillRect(1,-12,2,4);}}
 if(!living){c.strokeStyle='#cfb38a';c.beginPath();c.moveTo(-4,-14);c.lineTo(3,-7);c.moveTo(3,-14);c.lineTo(-4,-7);c.stroke();}c.restore();}
function draw(c,room,options={}){const enclosures=room.enclosures||[],specimens=room.specimens||[],time=options.time||0;
 for(let i=0;i<enclosures.length;i++){const e=enclosures[i],x=39+i*80,y=57;c.fillStyle='#13292f';c.fillRect(x-3,y-3,70,101);c.fillStyle=e.integrity<40?'#c28570':'#668c8a';c.fillRect(x-3,y-3,70,3);c.fillRect(x-3,y,3,98);c.fillRect(x+64,y,3,98);c.fillStyle='#10242d';c.fillRect(x,y,64,90);c.fillStyle='#355557';c.fillRect(x,y+81,64,9);c.fillStyle=e.latched?'#8fbaa0':'#d5a66e';c.fillRect(x+54,y+85,6,3);const o=specimens.find(o=>o.id===e.occupant);if(o)organism(c,o,x+13+o.x*37,y+78,time);c.fillStyle='#a5c4b2';c.font='7px monospace';c.fillText(e.id,x+4,y+12);c.fillStyle='#73a4a0';c.fillRect(x+7,y+20,1,50);c.fillStyle=e.integrity<40?'#d79f7c':'#85b1a7';c.fillRect(x,y+94,64*e.integrity/100,2);if(e.integrity<30){c.strokeStyle='#d7b3a1';c.beginPath();c.moveTo(x+40,y+25);c.lineTo(x+28,y+43);c.lineTo(x+39,y+54);c.stroke();}}
 for(const o of specimens.filter(o=>!o.enclosure))organism(c,o,35+o.x*305,190,time);
}
root.ICARUSSpecimenArt={draw};
})(globalThis);
