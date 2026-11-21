package com.umbra.mobile

import kotlinx.coroutines.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Test

class WeatherClientTest {
    @Test fun weatherUsesRealProviderContractUnitsAndNoAuthorization() = runBlocking {
        val server=MockWebServer();server.start();val client=WeatherClient(server.url("/forecast").toString(),server.url("/search").toString())
        try {
            server.enqueue(MockResponse().setBody("""{"timezone":"America/Chicago","current":{"time":1800000000,"temperature_2m":18.5,"weather_code":3},"hourly":{"time":[1800000000],"temperature_2m":[19],"weather_code":[2]},"daily":{"time":[1800000000],"temperature_2m_max":[21],"temperature_2m_min":[12],"weather_code":[3]}}"""))
            val c=Config(weatherPlace="Test fixture",weatherLatitude=41.0,weatherLongitude=-87.0,weatherFahrenheit=true)
            val forecast=client.forecast(c)
            assertEquals(18.5,forecast.temperature!!,0.0);assertEquals(21.0,forecast.days.single().high!!,0.0);assertEquals(1,forecast.hours.size)
            val request=server.takeRequest();assertTrue(request.path!!.contains("temperature_unit=fahrenheit"));assertNull(request.getHeader("Authorization"))
            server.enqueue(MockResponse().setBody("""{"results":[{"name":"Chosen city","country":"US","latitude":41.0,"longitude":-87.0}]}"""))
            assertEquals("Chosen city, US",client.search("Chosen").single().name)
            assertTrue(server.takeRequest().path!!.contains("name=Chosen"))
        } finally{client.close();server.shutdown()}
    }
    @Test fun providerErrorsAreNotDemonstrationData() = runBlocking {
        val server=MockWebServer();server.start();val client=WeatherClient(server.url("/").toString())
        try {server.enqueue(MockResponse().setResponseCode(503));assertTrue(runCatching {client.forecast(Config(weatherLatitude=1.0,weatherLongitude=2.0))}.isFailure)}finally{client.close();server.shutdown()}
    }
}
