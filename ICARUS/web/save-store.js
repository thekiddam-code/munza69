/* Lossless on-disk encoding only for ICARUS core/recovery/checkpoint keys.
   Application callers and portable backups continue to read/write ordinary JSON. */
(function(root,factory){if(typeof module==='object'&&module.exports)module.exports=factory(require('./vendor/lz-string.min.js'));else {root.ICARUSSaveStore=factory(typeof LZString==='undefined'?root.LZString:LZString);root.ICARUSSaveStore.install();}})(typeof globalThis!=='undefined'?globalThis:this,function(codec){'use strict';
 const prefix='ICARUS-LZ1:',keys=new Set(['icarus-v02','icarus-core-recovery-v0941','icarus-recovery-v039']);let originalGet,originalSet;
 function encode(value){value=String(value);if(value.length<4096)return value;const compressed=prefix+codec.compressToUTF16(value);return compressed.length<value.length?compressed:value;}
 function decode(value){if(value===null||!value.startsWith(prefix))return value;return codec.decompressFromUTF16(value.slice(prefix.length));}
 function install(){if(typeof Storage==='undefined')return false;if(Storage.prototype.__icarusLosslessCodec){originalGet=Storage.prototype.__icarusOriginalGet;originalSet=Storage.prototype.__icarusOriginalSet;return true;}
  originalGet=Storage.prototype.getItem;originalSet=Storage.prototype.setItem;
  Object.defineProperty(Storage.prototype,'__icarusLosslessCodec',{value:true});Object.defineProperty(Storage.prototype,'__icarusOriginalGet',{value:originalGet});Object.defineProperty(Storage.prototype,'__icarusOriginalSet',{value:originalSet});
  Storage.prototype.getItem=function(key){const value=originalGet.call(this,key);return keys.has(String(key))?decode(value):value;};
  Storage.prototype.setItem=function(key,value){return originalSet.call(this,key,keys.has(String(key))?encode(value):value);};return true;
 }
 function stats(){if(!originalGet)return null;try{const values=[...keys].map(k=>originalGet.call(localStorage,k)||'');return {physical_bytes:values.reduce((n,v)=>n+v.length*2,0),primary_bytes:values[0].length*2,compressed:values[0].startsWith(prefix)};}catch{return null;}}
 return {encode,decode,install,stats};
});
