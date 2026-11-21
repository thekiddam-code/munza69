package com.umbra.mobile

import kotlinx.coroutines.*
import kotlinx.serialization.json.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Test

class ButtonOutputsTest {
    @Test fun allImplementedOutputsUseExistingServerPayloads() {
        val expected=mapOf(OutputKind.QuickChat to "quick",OutputKind.Macro to "macro",OutputKind.Text to "text",OutputKind.FortniteEmote to "fortnite_emote",OutputKind.MineToggle to "mine_toggle",OutputKind.ForwardMine to "forward_mine",OutputKind.Stop to "stop")
        expected.forEach {(kind,name)->val action=buttonAction(CustomButton(kind=kind,name="Current server name",text="Current message",seconds=6.5,index=4))
            assertEquals("api/action",action.path);assertEquals(name,action.body.literal("action"))
            if(kind==OutputKind.ForwardMine)assertEquals(6.5,action.body.number("seconds")!!,0.0)
            if(kind==OutputKind.Text){assertEquals("Current message",action.body.literal("text"));assertEquals("balanced",action.body.literal("speed"))}
        }
        assertEquals("api/tv/key",buttonAction(CustomButton(kind=OutputKind.TvKey,key="ch_up")).path)
        assertEquals("api/icarus/command",buttonAction(CustomButton(kind=OutputKind.Simulation,command="speed20")).path)
        assertTrue(runCatching {validateButton(CustomButton(kind=OutputKind.ForwardMine,seconds=11.0))}.isFailure)
        assertTrue(runCatching {validateButton(CustomButton(kind=OutputKind.TvKey,key="invented"))}.isFailure)
    }
    @Test fun selectionHasNoSixButtonTruncationAndExplicitEmptyPersists() {
        val buttons=(0..19).map {CustomButton(id="button-$it",label="Button $it")}
        val c=Config(customButtons=buttons)
        val catalog=buttonCatalog(c,null)
        assertEquals(20,chosenButtonIds(c,catalog).size)
        val large=parsePcStatus(buildJsonObject {put("quick",buildJsonArray {repeat(135){add("Configured $it")}})})
        assertEquals(136,instantActions(large).size)
        val selected=c.copy(instantSelection=catalog.map {it.id}.toSet())
        assertEquals(20,importConfig(exportConfig(selected)).instantSelection!!.size)
        assertTrue(chosenButtonIds(c.copy(instantSelection=emptySet()),catalog).isEmpty())
        assertEquals(setOf("quick:Existing"),chosenButtonIds(c.copy(instantFavorites=setOf("quick:Existing")),catalog))
    }
    @Test fun buttonFilesRoundTripRejectUnsupportedAndNeverContainCredentials() {
        val original=listOf(CustomButton(kind=OutputKind.Text,text="Hello",channel="team",icon="⚡"))
        val file=exportButtons(original)
        assertEquals(original,importButtons(file));assertFalse(file.contains("token"));assertFalse(file.contains("serverUrl"))
        assertTrue(runCatching {importButtons(file.replace("\"Text\"","\"ArbitraryShell\""))}.isFailure)
        assertTrue(runCatching {importButtons(file.replace("\"seconds\":3.0","\"seconds\":\"3.0\""))}.isFailure)
        assertEquals("Hello",actionCopy(buttonAction(original.single())).text)
        assertEquals(7.0,actionCopy(buttonAction(CustomButton(kind=OutputKind.ForwardMine,seconds=7.0))).seconds,0.0)
    }
    @Test fun overridingServerReferencePreservesWidgetSelectionAndPlacement() {
        val pc=parsePcStatus(buildJsonObject {put("quick",buildJsonArray {add("Current")})})
        val source="quick:Current"
        val old=Config(instantSelection=setOf(source),widgetButtonSelections=mapOf("widget" to listOf(source)),gridLayouts=mapOf("instant-page" to GridLayout(cells=listOf(GridCell(source,x=1,y=3,w=2,h=2)))))
        val b=CustomButton(id="override",label="Renamed",kind=OutputKind.Text,text="Configured output")
        val saved=upsertButton(old,b,pc,source)
        assertEquals(setOf("local:override"),saved.instantSelection)
        assertEquals(listOf("local:override"),saved.widgetButtonSelections.getValue("widget"))
        assertEquals(GridCell("local:override",x=1,y=3,w=2,h=2),saved.gridLayouts.getValue("instant-page").cells.single())
        assertEquals(listOf("Current"),pc.quick)
        assertTrue(deleteButton(saved,"local:override").customButtons.isEmpty())
    }
    @Test fun configuredButtonsReceiveRealFeedbackAndQueueAcknowledgments() = runBlocking {
        val server=MockWebServer();server.start();val remote=IcarusClient();val controller=InstantController(remote){"test-token"}
        val b=CustomButton(id="timed",kind=OutputKind.ForwardMine,seconds=4.5)
        val c=Config(serverUrl=server.url("/").toString(),customButtons=listOf(b))
        controller.publish(serverBase(c),parsePcStatus(buildJsonObject{}))
        try {
            server.enqueue(MockResponse().setBody("""{"message":"Forward mining for 4.5s"}"""))
            controller.execute(c,"local:timed")
            val request=server.takeRequest();assertEquals("/api/action",request.path);assertEquals("Bearer test-token",request.getHeader("Authorization"))
            assertEquals(4.5,Json.parseToJsonElement(request.body.readUtf8()).jsonObject.number("seconds")!!,0.0)
            assertEquals("Forward mining for 4.5s",controller.state.value.status)
            val simulation=CustomButton(id="sim",kind=OutputKind.Simulation,command="pause")
            server.enqueue(MockResponse().setBody("""{"queued":42}"""));controller.execute(c.copy(customButtons=listOf(simulation)),"local:sim")
            assertTrue(controller.state.value.status.contains("PC execution pending"))
            server.enqueue(MockResponse().setResponseCode(503));controller.execute(c,"local:timed")
            assertFalse(controller.state.value.status.contains("Forward mining"))
        } finally {remote.close();server.shutdown()}
    }
}
