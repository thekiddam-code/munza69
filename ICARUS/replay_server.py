"""Serve an unchanged old build with passive diagnostics added to its HTML response only."""
import functools,http.server,io,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def handler(web_root):
    class Instrumented(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*a):pass
        def send_head(self):
            path=self.path.split('?',1)[0]
            if path not in ('/icarus.html','/stability-diagnostics.js'):return super().send_head()
            if path=='/stability-diagnostics.js':data=(ROOT/'web/stability-diagnostics.js').read_bytes();mime='text/javascript'
            else:
                s=(Path(web_root)/'icarus.html').read_text()
                if 'stability:()=>JSON.parse(JSON.stringify(ICARUSStabilityDiagnostics.read(state)))' not in s:
                    assert '  time:()=>state.tick,' in s,'Unsupported diagnostic entry point'
                    s=s.replace('<script src="diagnostics.js">','<script src="stability-diagnostics.js"></script><script src="diagnostics.js">',1).replace('  time:()=>state.tick,','  stability:()=>JSON.parse(JSON.stringify(ICARUSStabilityDiagnostics.read(state))),\n  time:()=>state.tick,',1)
                data=s.encode();mime='text/html; charset=utf-8'
            self.send_response(200);self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(data)));self.end_headers();return io.BytesIO(data)
    return functools.partial(Instrumented,directory=str(web_root))
