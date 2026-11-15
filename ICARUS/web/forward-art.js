/* Cargo establishing view: one vehicle at a declared 20px/metre projection, no tent interiors. */
(function(root){'use strict';
function draw(c,r){const v=r.forward?.vehicle;if(!v)return;const R=(x,y,w,h,color)=>{c.fillStyle=color;c.fillRect(x,y,w,h);};R(0,0,384,216,'#162a32');R(0,0,384,15,'#071b27');c.fillStyle='#b2c7bd';c.font='7px monospace';c.fillText('ICARUS / C03 / CARGO ESTABLISHING CAMERA',5,10);for(let x=20;x<380;x+=60){R(x,20,4,145,'#52616a');R(x+7,28,43,2,'#72817e');}R(0,165,384,48,'#29383b');for(let x=88;x<280;x+=20)R(x,186,12,2,'#c6ac63');R(87,103,2,84,'#c6ac63');R(258,103,2,84,'#c6ac63');R(20,107,38,53,'#59695e');R(24,112,30,16,'#283b3e');R(303,115,52,48,'#5b594a');R(307,119,44,2,'#ae9a70');c.font='7px monospace';c.fillStyle='#a9c4b5';c.fillText('C03 / FOC-01 PARKING · 8m × 4m',80,28);c.fillText('SERVICE / LOADING · KEEP CLEAR',86,201);
 if(!['parked','loading','securing'].includes(v.stage)){c.fillText('PARKING EMPTY / SEE RECEIVED FREIGHT REPORT',69,98);return;}rover(c,108+Math.round((v.loadingProgress||0)*140),108,124,62,r.lighting,v.condition);c.fillStyle='#d8d0ae';c.font='7px monospace';c.fillText('6.2m / 3.1m · '+(v.restrained?'RESTRAINED':'CARGO TRANSFER'),91,91);}
function rover(c,x,y,w=124,h=62,light=1,condition=100){c.save();c.translate(x,y);c.scale(w/124,h/62);const R=(x,y,w,h,col)=>{c.fillStyle=col;c.fillRect(x,y,w,h);},P=(pts,col)=>{c.fillStyle=col;c.beginPath();pts.forEach(([x,y],i)=>i?c.lineTo(x,y):c.moveTo(x,y));c.closePath();c.fill();};
 // One angular pressure hull, an integrated forward cockpit and three suspended axles.
 P([[4,43],[8,20],[24,11],[77,11],[98,22],[119,37],[123,48],[6,48]],'#273f45');
 P([[8,35],[13,22],[28,15],[75,15],[94,25],[112,37],[111,43],[8,43]],'#747c72');
 P([[78,17],[96,26],[108,36],[82,34]],'#142e3c');R(83,23,9,2,'#6c9b9a');R(89,31,13,1,'#587f82');
 for(let i=0;i<3;i++){const xx=18+i*36;R(xx-2,42,22,5,'#8b998e');R(xx+7,39,3,12,'#536c72');R(xx,45,18,17,'#08131b');R(xx+3,48,12,11,'#293e49');R(xx+7,50,4,7,'#a2b2a2');for(let dy=1;dy<15;dy+=4)R(xx-1,46+dy,3,2,'#64746c');}
 R(15,26,23,13,'#506967');R(42,24,26,17,'#929184');R(46,27,18,2,'#c2b699');R(72,36,29,5,'#435a61');
 for(let i=0;i<4;i++){R(17+i*11,17,7,3,'#3c535c');R(17+i*11,20,7,1,'#abbaa2');}R(25,9,45,3,'#536a6c');R(32,4,28,5,'#8e8b70');R(69,0,2,13,'#99aaa2');R(61,2,12,2,'#a6b5aa');R(10,32,2,9,'#b39b64');R(115,36,5,3,light>.15?'#c7e5d9':'#364850');R(9,39,5,2,light>.15?'#b18054':'#364850');
 R(9,44,110,3,'#182d38');R(16,43,9,2,'#baa260');R(45,35,6,3,'#776750');R(65,26,2,11,'#334d57');if(condition<70){R(39,22,10,2,'#253d43');R(34,30,6,2,'#293940');}c.fillStyle='#d4d0b6';c.font='6px monospace';c.fillText('FOC-01',17,35);c.restore();}

function field(c,r){const f=r.forward;if(!f)return;const R=(x,y,w,h,color)=>{c.fillStyle=color;c.fillRect(x,y,w,h);};rover(c,14,132,82,41,r.lighting,f.vehicle.condition);if(!f.camp)return;
 for(const [i,q] of f.camp.objects.filter(q=>['medicalTent','sleepingTents'].includes(q.kind)).entries()){const x=126+i*69;c.fillStyle=q.kind==='medicalTent'?'#7d8982':'#707769';c.beginPath();c.moveTo(x,175);c.lineTo(x+27,137);c.lineTo(x+55,175);c.closePath();c.fill();R(x+22,153,13,22,'#293a3d');if(q.kind==='medicalTent'){R(x+5,163,9,3,'#b4c5b5');R(x+8,160,3,9,'#b4c5b5');}}
 if(f.powered){R(104,123,2,57,'#8b9891');R(96,122,17,4,'#d7d1a0');}c.fillStyle='#b8c9ae';c.fillText(f.camp.stage==='deployed'?'CAMP / EXTERIOR ONLY':f.camp.stage.toUpperCase(),10,112);}
root.ICARUSForwardArt={draw,field,rover};
})(globalThis);
