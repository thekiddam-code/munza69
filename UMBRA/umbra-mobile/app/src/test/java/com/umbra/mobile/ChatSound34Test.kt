package com.umbra.mobile
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Test
class ChatSound34Test {
 private val sound="a".repeat(32)
 @Test fun nonePreservesOldEndpointAndOnlyChatCanAttachSound() {
  val chat=CustomButton(id="chat",label="Nice",kind=OutputKind.Text,text="Nice shot!")
  assertEquals("api/action",buttonAction(chat).path);assertFalse(buttonAction(chat).body.containsKey("sound_id"))
  val linked=buttonAction(chat.copy(afterSoundId=sound));assertEquals("api/rocket/chat-sound",linked.path);assertEquals(sound,linked.body.literal("sound_id"))
  assertNotEquals(linked.body.literal("requestId"),buttonAction(chat.copy(afterSoundId=sound)).body.literal("requestId"))
  assertEquals("api/action",buttonAction(chat.copy(kind=OutputKind.Macro,name="Copy",afterSoundId=sound)).path)
  assertTrue(runCatching {validateButton(chat.copy(afterSoundId="../clip.wav"))}.isFailure)
 }
 @Test fun perWidgetAndPresetMappingsAndExportsPreserveSoundWithoutChangingNeighbors() {
  val original=CustomButton(id="chat",kind=OutputKind.Text,text="Nice shot!")
  val page=DesktopPage("main","Deck",items=listOf("left","right").map {DesktopItem(it,"widget",widget=DesktopWidget(kind="icarus",buttonSet="rocket"))})
  var c=Config(desktop=DesktopLayout(pages=listOf(page)),customButtons=listOf(original),widgetButtonSelections=mapOf("left" to listOf("local:chat"),"right" to listOf("local:chat")))
  c=overrideWidgetButton(c,"left","local:chat",original.copy(afterSoundId=sound))
  val other=addHomePreset(c,"Other");val back=switchHomePreset(importConfig(exportConfig(other)),"default")
  assertEquals(sound,widgetSpec(back,"left")!!.buttonOverrides["local:chat"]!!.afterSoundId)
  assertTrue(widgetSpec(back,"right")!!.buttonOverrides.isEmpty());assertEquals(c.widgetButtonSelections,back.widgetButtonSelections)
  assertEquals(sound,importButtons(exportButtons(listOf(original.copy(afterSoundId=sound)))).single().afterSoundId)
  val old=exportButtons(listOf(original)).replace(",\"afterSoundId\":\"\"","");assertEquals("",importButtons(old).single().afterSoundId)
 }
 @Test fun pairedExecutionSendsChatAndSoundTogetherAndOldServerDoesNotFallbackOrReplay()=runBlocking {
  val server=MockWebServer();server.start();val remote=IcarusClient();val ctl=InstantController(remote){"paired"}
  val b=CustomButton(id="chat",kind=OutputKind.Text,text="Well played",channel="team",afterSoundId=sound)
  val c=Config(serverUrl=server.url("/").toString(),customButtons=listOf(b));ctl.publish(serverBase(c),PcStatus(null,null,false,emptyList(),emptyList(),emptyList()))
  try {
   server.enqueue(MockResponse().setBody("""{"message":"Text input finished; sound unavailable. Chat not resent.","chat_input_completed":true,"sound_started":false}"""))
   ctl.execute(c,"local:chat");val req=server.takeRequest();assertEquals("/api/rocket/chat-sound",req.path);assertEquals("Bearer paired",req.getHeader("Authorization"));val body=Json.parseToJsonElement(req.body.readUtf8()).jsonObject
   assertEquals("Well played",body.literal("text"));assertEquals("team",body.literal("channel"));assertEquals(sound,body.literal("sound_id"));assertFalse(body.containsKey("keys"));assertTrue(ctl.state.value.status.contains("not resent"))
   server.enqueue(MockResponse().setResponseCode(404).setBody("{}"));ctl.execute(c,"local:chat");assertEquals(2,server.requestCount);assertTrue(ctl.state.value.status.contains("chat-sounds update"))
  }finally {remote.close();server.shutdown()}
 }
}
