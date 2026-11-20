"""Mono K-weighted, gated integrated loudness and bounded lookahead peak protection.
No device capture here; operates only on caller-supplied PCM. No loudness claim from peaks alone.
"""
import array,collections,io,math,sys,wave
RATE=24000

def pcm(raw):
 with wave.open(io.BytesIO(raw),'rb') as f:
  if (f.getnchannels(),f.getsampwidth(),f.getframerate(),f.getcomptype())!=(1,2,RATE,'NONE'):raise ValueError('Expected 24 kHz mono PCM16')
  a=array.array('h',f.readframes(f.getnframes()))
 if sys.byteorder!='little':a.byteswap()
 return [v/32768 for v in a]

def biquad(values,kind):
 f0,q,gain=(1681.9744509555339,.7071752369554196,3.999843853973347) if kind=='shelf' else (38.13547087602444,.5003270373238773,0)
 k=math.tan(math.pi*f0/RATE)
 if kind=='shelf':
  vh=10**(gain/20);vb=vh**.4996667741545416;den=1+k/q+k*k;b0=(vh+vb*k/q+k*k)/den;b1=2*(k*k-vh)/den;b2=(vh-vb*k/q+k*k)/den
 else:
  den=1+k/q+k*k;b0=1;b1=-2;b2=1
 a1=2*(k*k-1)/den;a2=(1-k/q+k*k)/den;x1=x2=y1=y2=0.;out=[]
 for x in values:
  y=b0*x+b1*x1+b2*x2-a1*y1-a2*y2;out.append(y);x2=x1;x1=x;y2=y1;y1=y
 return out

def measure(raw):
 values=pcm(raw)
 if not values:raise ValueError('No PCM samples')
 filtered=biquad(biquad(values,'shelf'),'highpass');window=min(len(values),int(.4*RATE));hop=int(.1*RATE);prefix=[0.]
 for x in filtered:prefix.append(prefix[-1]+x*x)
 energies=[max(0,(prefix[i+window]-prefix[i])/window) for i in range(0,len(values)-window+1,hop)]
 def lufs(e):return -.691+10*math.log10(e) if e>0 else None
 absolute=[e for e in energies if e>0 and lufs(e)>=-70]
 gated=[]
 if absolute:
  relative=lufs(sum(absolute)/len(absolute))-10;gated=[e for e in absolute if lufs(e)>=relative]
 integrated=lufs(sum(gated)/len(gated)) if gated else None
 peak=max(abs(x) for x in values);rms=math.sqrt(sum(x*x for x in values)/len(values))
 return {'integrated_lufs':integrated,'sample_peak_dbfs':20*math.log10(peak) if peak else None,'rms_dbfs':20*math.log10(rms) if rms else None,'duration_seconds':len(values)/RATE,'gated_blocks':len(gated),'short_clip':len(values)<int(.4*RATE),'clipped_samples':sum(abs(x)>=.999 for x in values),'method':'ITU-R BS.1770 mono K-weighting; 400ms / 100ms gated blocks (-70 LUFS absolute, -10 LU relative). Short clips use one available-length block; sample peak, not true peak.'}

def normalize(raw,speech_lufs,offset=-3,volume=.35,ceiling=-1,max_boost=6):
 if not all(isinstance(v,(float,int)) and math.isfinite(v) for v in [speech_lufs,offset,volume,ceiling,max_boost]):raise ValueError('Finite profile required')
 if not -60<=speech_lufs<=0 or not -12<=offset<=0 or not 0<=volume<=1 or not -12<=ceiling<=-1 or not 0<=max_boost<=6:raise ValueError('Unsafe normalization settings')
 info=measure(raw);level=info['integrated_lufs'];target=speech_lufs+offset
 gain_db=min(max_boost,target-level+20*math.log10(volume/.35)) if level is not None and volume>0 else -120
 gain_db=max(-120,gain_db);amp=10**(gain_db/20);cap=10**(ceiling/20);values=pcm(raw);n=len(values);look=int(.01*RATE);maxima=collections.deque();next_index=0;envelope=amp;output=array.array('h');attack=math.exp(-1/(.002*RATE));release=math.exp(-1/(.08*RATE));limited=0
 for i,x in enumerate(values):
  while next_index<min(n,i+look+1):
   magnitude=abs(values[next_index])
   while maxima and maxima[-1][1]<=magnitude:maxima.pop()
   maxima.append((next_index,magnitude));next_index+=1
  while maxima and maxima[0][0]<i:maxima.popleft()
  peak=maxima[0][1] if maxima else 0;tgt=min(amp,cap/peak) if peak else amp;factor=attack if tgt<envelope else release;envelope=factor*envelope+(1-factor)*tgt
  y=x*envelope*min(1,i/look,(n-1-i)/look)
  if abs(y)>cap:limited+=1;y=max(-cap,min(cap,y))
  output.append(max(-32768,min(32767,round(y*32767))))
 if sys.byteorder!='little':output.byteswap()
 b=io.BytesIO()
 with wave.open(b,'wb') as f:f.setparams((1,2,RATE,0,'NONE','not compressed'));f.writeframes(output.tobytes())
 return b.getvalue(),{'input':info,'target_lufs':target,'applied_gain_db':gain_db,'max_boost_db':max_boost,'sample_peak_ceiling_dbfs':ceiling,'guard_samples':limited,'nominal_volume':.35,'note':'35% retained library volume is nominal; manual per-sound gain is relative to it. Quiet/short clips and limiting may fall below target. No true-peak/inter-sample guarantee.'}
