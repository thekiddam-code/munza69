package com.umbra.mobile

import kotlinx.coroutines.*
import kotlinx.serialization.json.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Test
import java.util.concurrent.TimeUnit

class IcarusClientTest {
    @Test fun pairingStatusAndCommandsUseExistingContract() = runBlocking {
        val server=MockWebServer();server.start();val client=IcarusClient()
        try {
            server.enqueue(MockResponse().setBody("{\"token\":\"native_pairing_token_123456789\"}"))
            val token=client.pair(server.url("/").toString(),"Az_9-x2",2)
            val pair=server.takeRequest();assertEquals("/api/pair",pair.path);assertEquals("POST",pair.method)
            assertEquals("Az_9-x2",Json.parseToJsonElement(pair.body.readUtf8()).jsonObject.literal("pin"));assertNull(pair.getHeader("Authorization"))
            server.enqueue(MockResponse().setBody("{\"cpu\":12.5,\"ram\":42,\"tv_configured\":true,\"macros\":[\"Copy\"],\"quick\":[\"Nice shot!\"],\"fortnite_emotes\":[{\"label\":\"Dance\"}]}"))
            val status=client.status(server.url("/").toString(),token,2)
            assertEquals(12.5,status.cpu!!,0.0);assertTrue(status.tvConfigured);assertEquals(listOf("Copy"),status.macros)
            assertEquals("Bearer $token",server.takeRequest().getHeader("Authorization"))
            server.enqueue(MockResponse().setBody("{\"queued\":7}"))
            val result=client.request(server.url("/").toString(),"api/icarus/command",2,token,buildJsonObject { put("command","pause") })
            assertEquals(7.0,result.number("queued")!!,0.0)
            val command=server.takeRequest();assertEquals("/api/icarus/command",command.path)
            assertEquals("pause",Json.parseToJsonElement(command.body.readUtf8()).jsonObject.literal("command"))
        } finally { client.close();server.shutdown() }
    }
    @Test fun redirectsAndUnauthorizedResponsesNeverLeakTokensOrFakeConnection() = runBlocking {
        val server=MockWebServer();val other=MockWebServer();server.start();other.start();val client=IcarusClient()
        try {
            server.enqueue(MockResponse().setResponseCode(302).addHeader("Location",other.url("/stolen")))
            val redirect=runCatching { client.status(server.url("/").toString(),"secret",2) }.exceptionOrNull()
            assertTrue(redirect is RemoteFailure);assertEquals(0,other.requestCount)
            server.enqueue(MockResponse().setResponseCode(401))
            val unauthorized=runCatching { client.status(server.url("/").toString(),"secret",2) }.exceptionOrNull()
            assertEquals(401,(unauthorized as RemoteFailure).status)
            assertFalse(unauthorized.message!!.contains("secret"))
        } finally { client.close();server.shutdown();other.shutdown() }
    }
    @Test fun missingReadingsAndOfflineShipRemainUnavailable() {
        val pc=parsePcStatus(buildJsonObject { put("cpu",JsonNull);put("ram",999);put("tv_configured",false) })
        assertNull(pc.cpu);assertNull(pc.ram);assertFalse(pc.tvConfigured);assertTrue(pc.macros.isEmpty())
    }
    @Test fun apiCancellationAndSizeBoundsWork() = runBlocking {
        val server=MockWebServer();server.start();val client=IcarusClient()
        try {
            server.enqueue(MockResponse().setBody("{\"oversized\":\"${"x".repeat(132000)}\"}"))
            assertTrue(runCatching { client.status(server.url("/").toString(),"token",2) }.exceptionOrNull() is RemoteFailure)
            server.enqueue(MockResponse().setHeadersDelay(5,TimeUnit.SECONDS).setBody("{}"))
            val job=launch { client.status(server.url("/").toString(),"token",10) }
            delay(100);withTimeout(1000){job.cancelAndJoin()};assertTrue(job.isCancelled)
        } finally { client.close();server.shutdown() }
    }
}
