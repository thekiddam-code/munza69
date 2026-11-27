package com.umbra.mobile

import kotlinx.coroutines.*
import kotlinx.serialization.json.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Test
import java.util.concurrent.TimeUnit

fun monitorFixture(age: Int=1)=Json.parseToJsonElement("""{"sample":{"supported":true,"cpu_percent":23,"cpu_temperature_c":61,"memory":{"percent":42,"used":8589934592,"total":17179869184},"gpus":[{"model":"Fixture GPU","utilization_percent":40,"temperature_c":55,"vram_used_bytes":1073741824,"vram_total_bytes":8589934592}],"battery":null,"power_scheme":"Balanced","interfaces":[{"name":"Ethernet","link_up":true}]},"age_seconds":$age,"sampled_at":1,"interval_seconds":3}""").jsonObject
fun windowsCatalogFixture()="""{"supported":true,"hotkeys":[{"id":"settings","name":"Settings","category":"System"}],"apps":[]}"""
class Phase3PcTest {
    @Test fun televisionMappingsArePreservedButInvisibleAndInert() {
        val tv=CustomButton(id="oldtv",label="Old remote",kind=OutputKind.TvKey)
        val pc=CustomButton(id="pc",label="PC macro",kind=OutputKind.Macro,name="Copy")
        val c=Config(customButtons=listOf(tv,pc),instantSelection=setOf("local:oldtv","local:pc"),loungeUrl="http://localhost/old")
        val imported=importConfig(exportConfig(c))
        assertEquals(c.customButtons,imported.customButtons);assertEquals(c.loungeUrl,imported.loungeUrl)
        assertEquals(listOf("local:pc"),buttonCatalog(imported,null).map {it.id})
        assertTrue(runCatching {buttonAction(tv)}.isFailure)
        assertEquals("api/action",buttonAction(pc).path)
    }
    @Test fun presetsPreserveIndependentWidgetsGridBindingsAndMappings() {
        val widget=DesktopItem("cpu","widget",widget=DesktopWidget(kind="engineering_cpu",collapsed=true,showDetails=false,accent="#FFB547"))
        val native=DesktopItem("native","widget",widget=DesktopWidget(kind="android",appWidgetId=42,provider="org.example/.Widget"))
        val original=Config(desktop=DesktopLayout(pages=listOf(DesktopPage("main","Original",items=listOf(widget,native)))),gridLayouts=mapOf("home:main" to GridLayout(cells=listOf(GridCell("cpu",x=1,y=3,w=2,h=4,collapsed=true)))),customButtons=listOf(CustomButton(id="keep")))
        assertFalse(gridForStorage(original,"home:main",original.gridLayouts.getValue("home:main")).cells.first().collapsed)
        val second=addHomePreset(original,"Gaming");assertEquals(2,homePresetNames(second).size)
        assertTrue(resolvedDesktop(second).pages.single().items.isEmpty());assertEquals(setOf(42),allNativeWidgetIds(second))
        val edited=second.copy(desktop=resolvedDesktop(second).let {it.updatePage(it.homePageId){p->p.copy(items=listOf(widget.copy(id="independent",widget=widget.widget!!.copy(collapsed=false,span=1))))}})
        val returned=switchHomePreset(edited,"default")
        assertEquals(original.desktop,returned.desktop);assertEquals(original.gridLayouts,returned.gridLayouts);assertEquals(original.customButtons,returned.customButtons)
        val again=switchHomePreset(returned,second.activeHomePreset);assertFalse(again.desktop!!.pages.single().items.single().widget!!.collapsed)
        assertEquals(setOf(42),allNativeWidgetIds(again))
        val exported=importConfig(exportConfig(again));assertTrue(allNativeWidgetIds(exported).isEmpty());assertEquals(again.activeHomePreset,exported.activeHomePreset)
        for(version in listOf(2,3,4))assertFalse(importConfig(exportConfig(Config(master=false)).replace("\"schemaVersion\":7","\"schemaVersion\":$version")).master)
    }
    @Test fun actualAuthenticatedStatusAndMonitorAreSharedWithoutDuplicateCollectors()=runBlocking {
        val server=MockWebServer();server.start();val remote=IcarusClient();val ctl=InstantController(remote){"fixture-token"};val c=Config(serverUrl=server.url("/").toString())
        try {
            server.enqueue(MockResponse().setBody("""{"hostname":"TEST-PC","cpu":21,"ram":43,"macros":["Copy"]}"""))
            server.enqueue(MockResponse().setBody(monitorFixture().toString()));server.enqueue(MockResponse().setBody(windowsCatalogFixture()))
            ctl.refresh(c,engineering=true)
            assertEquals(PcPhase.Connected,ctl.pcConnection.value.phase);assertEquals("TEST-PC",ctl.pcConnection.value.name);assertNotNull(ctl.pcConnection.value.latencyMs)
            assertEquals(23.0,engineeringSample(ctl.pcConnection.value)!!.number("cpu_percent")!!,0.0)
            val calls=(0..2).map {server.takeRequest()};assertEquals(listOf("/api/status","/api/windows/monitor","/api/windows/catalog"),calls.map {it.path});assertTrue(calls.all {it.getHeader("Authorization")=="Bearer fixture-token"})
            server.enqueue(MockResponse().setBody(monitorFixture().toString()));ctl.refresh(c,engineering=true)
            assertEquals("/api/windows/monitor",server.takeRequest().path);assertEquals(4,server.requestCount)
            server.enqueue(MockResponse().setBody("""{"message":"Settings sent"}"""));ctl.executeWindows(c,"settings")
            val action=server.takeRequest();assertEquals("/api/windows/command",action.path)
            val body=Json.parseToJsonElement(action.body.readUtf8()).jsonObject
            assertEquals(setOf("kind","id","requestId"),body.keys);assertEquals("hotkey",body.literal("kind"));assertEquals("settings",body.literal("id"))
            ctl.executeWindows(c,"arbitrary-program");assertEquals(5,server.requestCount)
            server.enqueue(MockResponse().setResponseCode(503));ctl.refresh(c,force=true)
            assertEquals(PcPhase.Offline,ctl.pcConnection.value.phase);assertNull(ctl.pcConnection.value.latencyMs);assertNull(engineeringSample(ctl.pcConnection.value))
        }finally {remote.close();server.shutdown()}
    }
    @Test fun oldCompanionSupportsHonestCpuRamFallbackWithoutInventedSensors()=runBlocking {
        val server=MockWebServer();server.start();val remote=IcarusClient();val ctl=InstantController(remote){"token"};val c=Config(serverUrl=server.url("/").toString())
        try {
            server.enqueue(MockResponse().setBody("""{"cpu":17,"ram":39}"""));server.enqueue(MockResponse().setResponseCode(404));server.enqueue(MockResponse().setResponseCode(404))
            ctl.refresh(c,engineering=true);assertEquals(PcPhase.Connected,ctl.pcConnection.value.phase);assertTrue(ctl.pcConnection.value.monitorUnsupported)
            assertNull(engineeringSample(ctl.pcConnection.value));assertEquals(17.0,ctl.state.value.pc!!.cpu!!,0.0);assertNull(ctl.pcConnection.value.name)
            server.enqueue(MockResponse().setBody("""{"cpu":18,"ram":40}"""));ctl.refresh(c,engineering=true);assertEquals(4,server.requestCount)
        }finally {remote.close();server.shutdown()}
    }
    @Test fun interruptedRequestsReleaseTheSingleGateAndDoNotRemainGreen()=runBlocking {
        val server=MockWebServer();server.start();val remote=IcarusClient();val ctl=InstantController(remote){"token"};val c=Config(serverUrl=server.url("/").toString(),timeout=10)
        try {
            server.enqueue(MockResponse().setSocketPolicy(SocketPolicy.NO_RESPONSE))
            val job=launch(Dispatchers.Default){ctl.refresh(c,true,true)}
            assertNotNull(server.takeRequest(3,TimeUnit.SECONDS));assertEquals(PcPhase.Connecting,ctl.pcConnection.value.phase)
            ctl.refresh(c,true,true);assertEquals(1,server.requestCount)
            job.cancelAndJoin();assertFalse(ctl.state.value.busy);assertEquals(PcPhase.Offline,ctl.pcConnection.value.phase)
            server.enqueue(MockResponse().setBody("{}"));ctl.refresh(c,true);assertEquals(PcPhase.Connected,ctl.pcConnection.value.phase)
            ctl.markInactive();assertEquals(PcPhase.Offline,ctl.pcConnection.value.phase)
        }finally {remote.close();server.shutdown()}
    }
    @Test fun sensorAgesAndNetworkMethodsAreConservative() {
        val state=PcConnectionState(phase=PcPhase.Connected,checkedAt=System.currentTimeMillis(),monitorAt=System.currentTimeMillis(),monitor=monitorFixture(30))
        assertNull(engineeringSample(state));assertNull(engineeringSample(state.copy(monitor=monitorFixture(),monitorAt=System.currentTimeMillis()-30000)));assertNotNull(engineeringSample(state.copy(monitor=monitorFixture())))
        assertTrue(connectionMethod("http://100.100.1.2/").startsWith("Tailscale"));assertTrue(connectionMethod("https://pc.tail.ts.net/").startsWith("Tailscale"))
        assertTrue(connectionMethod("http://192.168.1.2/").startsWith("Local"));assertTrue(connectionMethod("https://example.com/").startsWith("Unknown"))
        assertTrue(connectionMethod("https://something.100.100.1.2/").startsWith("Unknown"))
        assertEquals(3000L,engineeringInterval(true,false,false));assertEquals(30000L,engineeringInterval(false,false,false));assertEquals(60000L,engineeringInterval(true,true,false))
    }
}
