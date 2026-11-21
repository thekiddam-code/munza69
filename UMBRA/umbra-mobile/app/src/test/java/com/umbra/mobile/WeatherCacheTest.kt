package com.umbra.mobile

import kotlinx.coroutines.runBlocking
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config as RoboConfig

@RunWith(RobolectricTestRunner::class)
@RoboConfig(sdk=[34])
class WeatherCacheTest {
    @Test fun cacheSurvivesRecreationDeduplicatesAndExpiresOfflineData() = runBlocking {
        val app=RuntimeEnvironment.getApplication()
        java.io.File(app.cacheDir,"umbra-weather-v1.json").delete()
        val server=MockWebServer();server.start();val client=WeatherClient(server.url("/").toString())
        val c=Config(weatherLatitude=1.0,weatherLongitude=2.0)
        var elapsed=0L
        try {
            server.enqueue(MockResponse().setBody("""{"timezone":"UTC","current":{"time":1800000000,"temperature_2m":18,"weather_code":0}}"""))
            val first=WeatherRepository(app,client){System.currentTimeMillis()+elapsed};first.refresh(c)
            assertNotNull(first.state.value.snapshot)
            first.refresh(c);assertEquals(1,server.requestCount)
            val recreated=WeatherRepository(app,client){System.currentTimeMillis()+elapsed};recreated.refresh(c)
            assertEquals(1,server.requestCount);assertNotNull(recreated.state.value.snapshot)
            elapsed+=31*60000L;server.enqueue(MockResponse().setResponseCode(503));recreated.refresh(c)
            assertNotNull(recreated.state.value.snapshot);assertTrue(recreated.state.value.message.contains("cached"))
            elapsed+=8*86400000L;server.enqueue(MockResponse().setResponseCode(503));recreated.refresh(c)
            assertNull(recreated.state.value.snapshot)
            assertEquals(3,server.requestCount)
            recreated.refresh(Config());assertNull(recreated.state.value.snapshot);assertEquals(3,server.requestCount)
        } finally {client.close();server.shutdown()}
    }
}
