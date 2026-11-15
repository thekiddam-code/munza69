/* Lossless cache encoding on a local worker. Save text is data, never evaluated. */
'use strict';
importScripts('vendor/lz-string.min.js');
function encode(raw){const compressed=raw.length<4096?raw:'ICARUS-LZ1:'+LZString.compressToUTF16(raw);return compressed.length<raw.length?compressed:raw;}
onmessage=e=>{const {id,raw,previousRaw}=e.data;if(!Number.isInteger(id)||typeof raw!=='string')throw Error('Invalid cache encoding request');const start=performance.now(),encoded=encode(raw),previousEncoded=typeof previousRaw==='string'?encode(previousRaw):undefined;postMessage({id,encoded,previousEncoded,elapsedMs:performance.now()-start});};
