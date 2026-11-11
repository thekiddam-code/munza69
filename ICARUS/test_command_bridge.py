"""Phase 4.1 host/terminal integration over real HTTP; no physical host or TV input."""
import json,unittest,urllib.request,urllib.error
from test_umbra_browser import UmbraBrowser
class CommandBridge(UmbraBrowser):
 def req(self,path,payload=None,headers=None):
  req=urllib.request.Request(self.url+path,json.dumps(payload).encode() if payload is not None else None,headers={'Content-Type':'application/json',**(headers or {})})
  try:
   with urllib.request.urlopen(req) as r:return r.status,json.load(r)
  except urllib.error.HTTPError as e:return e.code,json.load(e)
 def test_auto_local_bootstrap_and_single_server_authority_without_manual_key(self):
  p=self.page(pc=True);p.wait_for_function('document.querySelector("#rd-bridge-status").textContent.includes("LINKED")');self.assertTrue(p.evaluate('ICARUSHost.canWrite()'));c=self.browser.new_context();self.contexts.append(c);q=c.new_page();q.goto(self.url+'/icarus.html?icarus_soak=1');q.wait_for_function('!!window.__icarusSoak');self.assertFalse(q.evaluate('ICARUSHost.canWrite()'));before=q.evaluate('__icarusSoak.time()');q.evaluate('__icarusSoak.advance(5)');self.assertEqual(q.evaluate('__icarusSoak.time()'),before)
 def test_local_bootstrap_rejects_lan_host_header_and_remote_document_redirects(self):
  # A local peer with non-loopback Host is not the approved host launch URL.
  code,d=self.req('/api/icarus/bootstrap',headers={'Host':'192.168.1.123'});self.assertEqual(code,403)
  r=urllib.request.Request(self.url+'/icarus.html',headers={'Host':'192.168.1.123'})
  with urllib.request.urlopen(r) as response:self.assertIn('terminal=icarus',response.url);self.assertNotIn('world-schema.js',response.read().decode())
 def test_dispatch_ack_dedup_and_world_is_authoritative(self):
  p=self.page(pc=True);p.wait_for_function('document.querySelector("#rd-bridge-status").textContent.includes("LINKED")');auth={'Authorization':'Bearer test-client'}
  a=self.req('/api/icarus/dispatch',{'command':'nav:hold','requestId':'test-idempotent'},auth);b=self.req('/api/icarus/dispatch',{'command':'nav:hold','requestId':'test-idempotent'},auth);self.assertEqual(a[1]['queued'],b[1]['queued']);p.wait_for_function('__icarusSoak.snapshot().navigation.hold');p.wait_for_timeout(1800);self.assertEqual(self.m.BRIDGE_SERVICE.queue,[])
  code,_=self.req('/api/icarus/dispatch',{'command':'speed20','requestId':'creator-denied'},auth);self.assertEqual(code,403)
 def test_stale_remote_state_never_becomes_a_save_upload(self):
  self.assertEqual(self.req('/api/icarus/host/publish',{'telemetry':{'tick':99999}}, {'Authorization':'Bearer test-client'})[0],403)
  p=self.page(pc=True);p.wait_for_function('document.querySelector("#rd-bridge-status").textContent.includes("LINKED")');code,d=self.req('/api/icarus/live',headers={'Authorization':'Bearer test-client'});self.assertEqual(code,200);self.assertEqual(d['telemetry']['tick'],p.evaluate('__icarusSoak.time()'));self.assertEqual(d['state'],'SIMULATION PAUSED')
if __name__=='__main__':unittest.main()
