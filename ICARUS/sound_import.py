"""User-initiated public Myinstants import; strict HTTPS allowlist, no bypass/automation."""
import base64,html,ipaddress,re,socket,urllib.parse,urllib.request
from html.parser import HTMLParser
from sound_library import SoundError
HOSTS={'myinstants.com','www.myinstants.com'}
def allowed(url,audio=False):
 try:
  p=urllib.parse.urlsplit(url)
  if p.scheme!='https' or p.hostname not in HOSTS or p.username or p.password or p.port not in (None,443) or p.query or p.fragment:raise ValueError()
  pattern=r'/media/sounds/[A-Za-z0-9_%.-]+\.(mp3|wav|ogg|m4a)' if audio else r'/[a-z]{2}/instant/[a-zA-Z0-9_-]+/?'
  if not re.fullmatch(pattern,p.path) or '..' in urllib.parse.unquote(p.path) or any(c in urllib.parse.unquote(p.path) for c in ('\\','\x00')):raise ValueError()
  return p.geturl()
 except (ValueError,TypeError):raise SoundError('Paste a supported public HTTPS Myinstants sound page; otherwise upload a local audio file')
class Redirect(urllib.request.HTTPRedirectHandler):
 def __init__(self,audio):self.audio=audio
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  allowed(newurl,self.audio);public_host(newurl);return super().redirect_request(req,fp,code,msg,headers,newurl)
def public_host(url):
 try:
  results=socket.getaddrinfo(urllib.parse.urlsplit(url).hostname,443,type=socket.SOCK_STREAM)
  if not results or any(not ipaddress.ip_address(r[4][0]).is_global for r in results):raise ValueError()
 except (OSError,ValueError):raise SoundError('Import host is unavailable or resolves to a non-public address')
def fetch(url,audio=False):
 allowed(url,audio);public_host(url);limit=3*1024*1024 if audio else 512*1024
 request=urllib.request.Request(url,headers={'User-Agent':'UMBRA/4.8 user-initiated sound import','Accept':'audio/*' if audio else 'text/html'})
 try:
  with urllib.request.build_opener(Redirect(audio)).open(request,timeout=8) as r:
   allowed(r.url,audio);raw=r.read(limit+1);mime=r.headers.get_content_type()
   if len(raw)>limit:raise SoundError('Import exceeds size limit; upload a shorter local clip',413)
   if not audio and mime!='text/html':raise SoundError('Myinstants did not provide a sound page')
   if audio and mime not in ('audio/mpeg','audio/wav','audio/x-wav','audio/ogg','audio/mp4','application/octet-stream'):raise SoundError('Unsupported audio response; use local upload')
   return raw,mime
 except SoundError:raise
 except Exception as e:raise SoundError('Myinstants import unavailable (no access restriction bypass): '+str(e)[:100]+'. Use local upload.',502)
class Page(HTMLParser):
 def __init__(self):super().__init__();self.audio=[];self.primary=[];self.title=[];self.in_title=False;self.in_audio=False
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='title':self.in_title=True
  if tag=='meta' and d.get('property')=='og:audio' and d.get('content'):self.primary.append(d['content'])
  if tag=='audio':self.in_audio=True
  if (tag=='audio' or tag=='source' and self.in_audio) and d.get('src'):self.audio.append(d['src'])
  if d.get('id')=='instant-page-button-element' or 'large-button' in d.get('class','').split():
   if d.get('data-url'):self.primary.append(d['data-url'])
   if d.get('onclick'):self.primary.extend(re.findall(r"(?:play|playSound)\(['\"](/media/sounds/[^'\"]+)['\"]",d['onclick']))
 def handle_endtag(self,tag):
  if tag=='title':self.in_title=False
  if tag=='audio':self.in_audio=False
 def handle_data(self,data):
  if self.in_title:self.title.append(data)
def import_page(url,permission):
 if permission is not True:raise SoundError('Confirm audio usage permission before importing')
 url=allowed(url);raw,_=fetch(url);page=Page();page.feed(raw.decode('utf8',errors='replace'));target=None
 for candidate in page.primary+page.audio:
  try:target=allowed(urllib.parse.urljoin(url,html.unescape(candidate)),True);break
  except SoundError:continue
 if not target:raise SoundError('No supported public audio source found. Download with permission and upload the file instead.',422)
 raw,mime=fetch(target,True);title=html.unescape(''.join(page.title)).strip().split(' - Myinstants')[0][:48] or 'Imported sound'
 return {'name':title,'source':url,'mime':mime,'audio':base64.b64encode(raw).decode('ascii')}
