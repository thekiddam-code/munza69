package com.umbra.mobile
import kotlinx.coroutines.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Test
import java.util.concurrent.TimeUnit
class DeckTest {
    @Test fun actualHeadResponsesDistinguishReachabilityAuthAndRedirects() = runBlocking {
        val server=MockWebServer()
        server.start()
        try {
            server.enqueue(MockResponse().setResponseCode(200))
            assertEquals("REACHABLE · HTTP 200",checkDeck(server.url("/deck").toString(),2))
            assertEquals("HEAD",server.takeRequest().method)
            server.enqueue(MockResponse().setResponseCode(401))
            assertEquals("AUTH REQUIRED · HTTP 401",checkDeck(server.url("/deck").toString(),2))
            server.takeRequest()
            server.enqueue(MockResponse().setResponseCode(302).addHeader("Location","http://example.test/"))
            assertEquals("REDIRECT · HTTP 302",checkDeck(server.url("/deck").toString(),2))
            assertEquals(3,server.requestCount)
        } finally { server.shutdown() }
    }
    @Test fun requestTimeoutAndCancellationAreBounded() = runBlocking {
        val server=MockWebServer()
        server.start()
        try {
            server.enqueue(MockResponse().setHeadersDelay(5,TimeUnit.SECONDS))
            val start=System.nanoTime()
            assertEquals("OFFLINE / UNREACHABLE",checkDeck(server.url("/").toString(),1))
            assertTrue(TimeUnit.NANOSECONDS.toMillis(System.nanoTime()-start)<3500)
            server.enqueue(MockResponse().setHeadersDelay(5,TimeUnit.SECONDS))
            val job=launch { checkDeck(server.url("/").toString(),10) }
            delay(100)
            withTimeout(1000) { job.cancelAndJoin() }
            assertTrue(job.isCancelled)
        } finally { server.shutdown() }
    }
}
