package com.umbra.mobile

import kotlinx.coroutines.*
import kotlinx.serialization.json.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Test

class Widget31Test {
    private fun config(): Config {
        val items=listOf(DesktopItem("rocket","widget",widget=DesktopWidget(kind="icarus",buttonSet="rocket",span=4)),DesktopItem("fortnite","widget",widget=DesktopWidget(kind="icarus",buttonSet="fortnite",span=4)),DesktopItem("sounds","widget",widget=DesktopWidget(kind="soundboard",span=8,rows=10,buttonColumns=6,buttonHeight=56)))
        return Config(desktop=DesktopLayout(pages=listOf(DesktopPage("main","Mixed controls",columns=8,items=items))))
    }
    @Test fun widgetSetsSelectionsOverridesAndGeometryStayIndependent() {
        val pc=PcStatus(1.0,2.0,false,listOf("Copy"),listOf("Nice shot!"),listOf(GameEmote(0,"Dance")))
        val c=config().copy(instantSelection=emptySet())
        val rocket=widgetCatalog(c,pc,"rocket").filter {simulatorAllows("rocket",it,c)}
        val fortnite=widgetCatalog(c,pc,"fortnite").filter {simulatorAllows("fortnite",it,c)}
        assertEquals(listOf("Nice shot!"),rocket.map {it.label});assertEquals(listOf("Dance"),fortnite.map {it.label})
        val changed=overrideWidgetButton(c,"rocket",rocket.single().id,CustomButton(label="My Rocket call",kind=OutputKind.Text,text="Custom team call",channel="team"))
        assertEquals("Custom team call",widgetCatalog(changed,pc,"rocket").first {it.id==rocket.single().id}.body.literal("text"))
        assertEquals("Nice shot!",widgetCatalog(changed,pc,"fortnite").first {it.id==rocket.single().id}.label)
        assertEquals(c.customButtons,changed.customButtons);assertEquals(c.instantSelection,changed.instantSelection)
        val owned=overrideWidgetButton(changed,"rocket","widget:own",CustomButton(label="Only here",kind=OutputKind.Text,text="Own command"))
        assertTrue(widgetCatalog(owned,pc,"rocket").any {it.id=="widget:own"})
        assertFalse(widgetCatalog(owned,pc,"fortnite").any {it.id=="widget:own"})
        assertEquals(changed,importConfig(exportConfig(changed)))
        assertEquals(8,resolvedDesktop(changed).pages.first().columns);assertEquals(6,widgetSpec(changed,"sounds")!!.buttonColumns)
    }
    @Test fun olderSharedSelectionsMigrateIntoEachWidgetWithoutTouchingAudio() {
        val c=config().copy(instantSelection=setOf("quick:Nice shot!"),widgetButtonSelections=mapOf("fortnite" to listOf("emote:0:Dance")))
        val old=exportConfig(c).replace("\"schemaVersion\":7","\"schemaVersion\":5")
        val migrated=importConfig(old)
        assertEquals(listOf("quick:Nice shot!"),migrated.widgetButtonSelections["rocket"])
        assertEquals(listOf("emote:0:Dance"),migrated.widgetButtonSelections["fortnite"])
        assertNull(migrated.widgetButtonSelections["sounds"])
        assertTrue(migrated.recentsShortcut)
    }
    @Test fun windowsButtonsUseSupportedExistingBackendAndWidgetOverrideOnly()=runBlocking {
        val server=MockWebServer();server.start();val client=IcarusClient();val ctl=InstantController(client){"fixture-token"}
        val c=config().copy(serverUrl=server.url("/").toString())
        try {
            server.enqueue(MockResponse().setBody("{}"));server.enqueue(MockResponse().setBody(monitorFixture().toString()));server.enqueue(MockResponse().setBody(windowsCatalogFixture()))
            ctl.refresh(c,true,true);repeat(3){server.takeRequest()}
            server.enqueue(MockResponse().setBody("{\"message\":\"Settings sent\"}"));ctl.execute(c,"windows:settings","rocket")
            val request=server.takeRequest();assertEquals("/api/windows/command",request.path)
            val body=Json.parseToJsonElement(request.body.readUtf8()).jsonObject
            assertEquals(setOf("kind","id","requestId"),body.keys);assertEquals("settings",body.literal("id"));assertEquals("Bearer fixture-token",request.getHeader("Authorization"))
            val overridden=overrideWidgetButton(c,"rocket","windows:settings",CustomButton(label="Own macro",kind=OutputKind.Macro,name="Unavailable"))
            ctl.execute(overridden,"windows:settings","rocket");assertEquals(4,server.requestCount)
        }finally {client.close();server.shutdown()}
    }
    @Test fun largeSoundCatalogFitsBoundedNativeResponseAndAllEntriesParse()=runBlocking {
        val server=MockWebServer();server.start();val client=IcarusClient()
        val data=JsonObject(soundFixture(512)+("padding" to JsonPrimitive("x".repeat(150000))))
        try {
            server.enqueue(MockResponse().setBody(data.toString()))
            val parsed=client.request(server.url("/").toString(),"api/sounds/library",5,"fixture")
            assertEquals(512,parseSoundCatalog(parsed).sounds.size)
            server.enqueue(MockResponse().setBody(data.toString()))
            assertTrue(runCatching {client.request(server.url("/").toString(),"api/status",5,"fixture")}.exceptionOrNull() is RemoteFailure)
        }finally {client.close();server.shutdown()}
    }
}
