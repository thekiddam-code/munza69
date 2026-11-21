package com.umbra.mobile

import kotlinx.coroutines.*
import kotlinx.serialization.json.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Test
import java.util.concurrent.TimeUnit

class InstantControllerTest {
    @Test fun syncedQuickCommandUsesAuthenticatedServerContractAndRejectsAnotherBase() = runBlocking {
        val server=MockWebServer();server.start();val remote=IcarusClient()
        val controller=InstantController(remote){"test-token"};val c=Config(serverUrl=server.url("/").toString())
        try {
            server.enqueue(MockResponse().setBody("""{"quick":["Latest mapping"],"custom_messages":[]}"""))
            controller.refresh(c,true)
            assertEquals("/api/status",server.takeRequest().path);assertTrue(controller.state.value.synchronizedAt>0)
            controller.refresh(c);assertEquals(1,server.requestCount)
            server.enqueue(MockResponse().setBody("""{"message":"Quick chat sent"}"""))
            controller.execute(c,"quick:Latest mapping")
            val action=server.takeRequest();assertEquals("/api/action",action.path);assertEquals("Bearer test-token",action.getHeader("Authorization"))
            val payload=Json.parseToJsonElement(action.body.readUtf8()).jsonObject
            assertEquals("Latest mapping",payload.literal("name"));assertFalse(payload.containsKey("keys"))
            assertEquals("Quick chat sent",controller.state.value.status)
            controller.execute(c.copy(serverUrl=server.url("/other/").toString()),"quick:Latest mapping")
            assertEquals(2,server.requestCount);assertTrue(controller.state.value.status.contains("Refresh"))
        } finally {remote.close();server.shutdown()}
    }
    @Test fun repeatedTapsCannotQueueDuplicateCommandsAndCancellationReleasesGate() = runBlocking {
        val server=MockWebServer();server.start();val remote=IcarusClient();val controller=InstantController(remote){"test-token"}
        val c=Config(serverUrl=server.url("/").toString())
        controller.publish(serverBase(c),parsePcStatus(Json.parseToJsonElement("""{"quick":["Latest mapping"]}""").jsonObject))
        try {
            server.enqueue(MockResponse().setSocketPolicy(SocketPolicy.NO_RESPONSE))
            val first=launch(Dispatchers.Default){controller.execute(c,"quick:Latest mapping")}
            assertNotNull(server.takeRequest(3,TimeUnit.SECONDS))
            controller.execute(c,"quick:Latest mapping");assertEquals(1,server.requestCount)
            first.cancelAndJoin();assertFalse(controller.state.value.busy)
            server.enqueue(MockResponse().setBody("""{"message":"Stopped"}"""))
            controller.execute(c,"action:stop");assertEquals(2,server.requestCount);assertEquals("Stopped",controller.state.value.status)
        } finally {remote.close();server.shutdown()}
    }
}
