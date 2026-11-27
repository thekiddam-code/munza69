package com.umbra.mobile

import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Test

class Host33Test {
    private fun config(url: String="")=Config(serverUrl=url,desktop=DesktopLayout(pages=listOf(DesktopPage("main","Deck",items=listOf(DesktopItem("mixed","widget",widget=DesktopWidget(kind="icarus",buttonSet="mixed")))))))
    @Test fun silverActionsAreOptionalStableReferencesAndPlacementSurvivesPresetRoundTrip() {
        val c=config();val catalog=widgetCatalog(c,null,"mixed")
        assertEquals(listOf("host:arctis","host:save-clip"),catalog.filter {it.id.startsWith("host:")}.map {it.id})
        assertTrue(defaultWidgetButtonIds(catalog).none {it.startsWith("host:")})
        val chosen=c.copy(widgetButtonSelections=mapOf("mixed" to listOf("host:arctis","host:save-clip")),gridLayouts=mapOf("instant-widget:mixed" to GridLayout(columns=12,cells=listOf(GridCell("host:arctis",x=10,y=3),GridCell("host:save-clip",x=11,y=3)))))
        val switched=addHomePreset(chosen,"Other")
        val restored=switchHomePreset(importConfig(exportConfig(switched)),"default")
        assertEquals(chosen.widgetButtonSelections,restored.widgetButtonSelections);assertEquals(chosen.gridLayouts["instant-widget:mixed"],restored.gridLayouts["instant-widget:mixed"])
        assertEquals(ButtonFamily.HostAction,buttonFamily(catalog.first {it.id=="host:arctis"}))
        assertEquals("Headphones",ControlIcons.category(ButtonFamily.HostAction,"host:arctis").name);assertEquals("Save clip",ControlIcons.category(ButtonFamily.HostAction,"host:save-clip").name)
    }
    @Test fun sonarUsesPairedEndpointAndRejectsIncompleteVerification()=runBlocking {
        val server=MockWebServer();server.start();val client=IcarusClient();val ctl=InstantController(client){"fixture"};val c=config(server.url("/").toString())
        try {
            ctl.publish(serverBase(c),PcStatus(null,null,false,emptyList(),emptyList(),emptyList()))
            server.enqueue(MockResponse().setBody("""{"state":"selection_required","outputs":[{"id":"a","name":"Arctis A"},{"id":"b","name":"Arctis B"}],"message":"Choose output"}"""))
            ctl.execute(c,"host:arctis","mixed")
            val first=server.takeRequest();assertEquals("/api/sonar/arctis",first.path);assertEquals("Bearer fixture",first.getHeader("Authorization"));val body=Json.parseToJsonElement(first.body.readUtf8()).jsonObject;assertEquals(setOf("requestId"),body.keys)
            assertEquals("selection_required",ctl.state.value.hostResult!!.literal("state"))
            server.enqueue(MockResponse().setBody("""{"state":"verified","verified":true,"microphone_preserved":true,"output":{"id":"b","name":"Arctis B"},"routes":{"game":"b","chat":"b","media":"b","aux":"b"},"message":"All four playback routes verified"}"""))
            ctl.executeHost(c,"host:arctis","mixed","b");val second=server.takeRequest();val selected=Json.parseToJsonElement(second.body.readUtf8()).jsonObject
            assertEquals("b",selected.literal("output_id"));assertNotEquals(body.literal("requestId"),selected.literal("requestId"));assertEquals("All four playback routes verified",ctl.state.value.status)
            server.enqueue(MockResponse().setBody("""{"state":"verified","verified":true,"microphone_preserved":true,"output":{"id":"b"},"routes":{"game":"b","chat":"b","media":"b"},"message":"OK"}"""))
            ctl.execute(c,"host:arctis","mixed");assertTrue(ctl.state.value.status.contains("did not verify"));assertNull(ctl.state.value.hostResult)
        }finally {client.close();server.shutdown()}
    }
    @Test fun clipAcknowledgmentIsNotConfirmationAndNeverHardcodesKeys()=runBlocking {
        val server=MockWebServer();server.start();val client=IcarusClient();val ctl=InstantController(client){"fixture"};val c=config(server.url("/").toString())
        try {
            ctl.publish(serverBase(c),PcStatus(null,null,false,listOf("Save Clip"),emptyList(),emptyList()))
            server.enqueue(MockResponse().setBody("""{"message":"Hotkey sent"}"""));ctl.execute(c,"host:save-clip","mixed")
            val request=server.takeRequest();val body=Json.parseToJsonElement(request.body.readUtf8()).jsonObject
            assertEquals("/api/moments/save-clip",request.path);assertEquals(setOf("requestId"),body.keys);assertFalse(body.toString().contains("alt",true));assertTrue(ctl.state.value.status.contains("unconfirmed"))
            server.enqueue(MockResponse().setResponseCode(409).setBody("""{"error":"Configure the actual Moments storage directory"}"""));ctl.execute(c,"host:save-clip","mixed")
            assertTrue(ctl.state.value.status.contains("Moments storage"))
        }finally {client.close();server.shutdown()}
    }
    @Test fun customVectorFootersKeepCategoryIdentityWithoutEmojiArtwork() {
        val icons=ButtonFamily.entries.map {ControlIcons.category(it)}
        assertTrue(icons.all {it.viewportWidth==24f && it.viewportHeight==24f})
        assertEquals("Car",ControlIcons.category(ButtonFamily.RocketLeague).name)
        assertEquals("Dancer",ControlIcons.category(ButtonFamily.Fortnite).name)
        assertEquals("Pickaxe",ControlIcons.category(ButtonFamily.Minecraft).name)
        assertEquals("Keyboard",ControlIcons.category(ButtonFamily.PcHotkey).name)
        assertEquals("Speaker",ControlIcons.category(ButtonFamily.Soundboard).name)
    }
    @Test fun clipPollingChecksTheSameRequestAndRequiresActualFileEvidence()=runBlocking {
        val server=MockWebServer();var verified=false
        server.dispatcher=object: Dispatcher(){override fun dispatch(r: RecordedRequest): MockResponse {
            val id=Json.parseToJsonElement(r.body.clone().readUtf8()).jsonObject.literal("requestId")!!
            return MockResponse().setBody(buildJsonObject {put("request_id",id);put("message","Host result");if(r.path=="/api/moments/save-clip")put("state","pending") else {put("state","clip_detected");put("clip_file_verified",verified);put("clip",buildJsonObject {put("name","fixture.mp4");put("bytes",100)})}}.toString())
        }};server.start();val client=IcarusClient();val ctl=InstantController(client){"fixture"};val c=config(server.url("/").toString())
        try {
            ctl.publish(serverBase(c),PcStatus(null,null,false,listOf("Save Clip"),emptyList(),emptyList()))
            ctl.execute(c,"host:save-clip","mixed");val first=ctl.state.value.hostResult!!.literal("request_id")!!
            ctl.pollClip(c,first,"mixed");assertTrue(ctl.state.value.status.contains("did not verify"));assertNull(ctl.state.value.hostResult)
            verified=true;ctl.execute(c,"host:save-clip","mixed");val second=ctl.state.value.hostResult!!.literal("request_id")!!;assertNotEquals(first,second)
            ctl.pollClip(c,second,"mixed");assertTrue(ctl.state.value.status.startsWith("New clip file observed. Confirm in Moments."));assertEquals(4,server.requestCount)
        }finally {client.close();server.shutdown()}
    }

}
