/* Core and Extended Universe never share a writable save namespace. */
(function(root){'use strict';
const extended=!!root.__icarusExtendedTest&&new URLSearchParams(location.search).has('icarus_soak');
const aliases={'icarus-v02':'icarus-anthology-v14','icarus-core-recovery-v0941':'icarus-anthology-recovery-v14','icarus-recovery-v039':'icarus-anthology-checkpoints-v14','icarus-durable-cache':'icarus-anthology-cache-v14'};
if(!extended){const get=Storage.prototype.getItem,set=Storage.prototype.setItem,remove=Storage.prototype.removeItem;Storage.prototype.getItem=function(k){return get.call(this,this===localStorage?(aliases[k]||k):k);};Storage.prototype.setItem=function(k,v){return set.call(this,this===localStorage?(aliases[k]||k):k,v);};Storage.prototype.removeItem=function(k){return remove.call(this,this===localStorage?(aliases[k]||k):k);};}
root.ICARUSEdition={core:!extended,database:extended?'icarus-voyage':'icarus-anthology-v14'};
})(globalThis);
