package com.umbra.mobile

import android.content.Context
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.*
import okhttp3.*
import okhttp3.HttpUrl.Companion.toHttpUrl
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.IOException
import java.util.concurrent.TimeUnit
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException

@Serializable data class WeatherHour(val time: Long,val temperature: Double?,val code: Int?)
@Serializable data class WeatherDay(val time: Long,val high: Double?,val low: Double?,val code: Int?)
@Serializable data class WeatherSnapshot(val key: String,val fetchedAt: Long,val timezone: String,val currentTime: Long,val temperature: Double?,val code: Int?,val hours: List<WeatherHour>,val days: List<WeatherDay>)
data class WeatherPlace(val name: String,val latitude: Double,val longitude: Double)
data class WeatherState(val snapshot: WeatherSnapshot?=null,val refreshing: Boolean=false,val message: String="Choose a weather location.")
fun weatherKey(c: Config)="${c.weatherLatitude}|${c.weatherLongitude}|${c.weatherFahrenheit}"
fun weatherCondition(code: Int?): String=when(code){0->"Clear";1->"Mainly clear";2->"Partly cloudy";3->"Overcast";45,48->"Fog";51,53,55->"Drizzle";56,57->"Freezing drizzle";61,63,65->"Rain";66,67->"Freezing rain";71,73,75,77->"Snow";80,81,82->"Rain showers";85,86->"Snow showers";95,96,99->"Thunderstorm";null->"Conditions unavailable";else->"Weather code $code"}
private fun JsonObject.numbers(name: String)=((get(name) as? JsonArray) ?: JsonArray(emptyList())).map {(it as? JsonPrimitive)?.takeUnless {p->p.isString}?.doubleOrNull?.takeIf(Double::isFinite)}
fun parseWeather(j: JsonObject,key: String,now: Long): WeatherSnapshot {
    val current=j["current"] as? JsonObject ?: throw IOException("Weather response lacks current conditions.")
    val currentTime=current.number("time")?.toLong() ?: throw IOException("Weather time unavailable.")
    val daily=j["daily"] as? JsonObject ?: JsonObject(emptyMap());val hourly=j["hourly"] as? JsonObject ?: JsonObject(emptyMap())
    val times=hourly.numbers("time");val temperatures=hourly.numbers("temperature_2m");val codes=hourly.numbers("weather_code")
    val days=daily.numbers("time");val highs=daily.numbers("temperature_2m_max");val lows=daily.numbers("temperature_2m_min");val dailyCodes=daily.numbers("weather_code")
    return WeatherSnapshot(key,now,j.literal("timezone") ?: "UTC",currentTime,current.number("temperature_2m"),current.number("weather_code")?.toInt(),
        times.mapIndexedNotNull {i,t->t?.toLong()?.takeIf {it>=currentTime-3600}?.let {WeatherHour(it,temperatures.getOrNull(i),codes.getOrNull(i)?.toInt())}}.take(24),
        days.take(5).mapIndexedNotNull {i,t->t?.toLong()?.let {WeatherDay(it,highs.getOrNull(i),lows.getOrNull(i),dailyCodes.getOrNull(i)?.toInt())}})
}
class WeatherClient(private val forecastBase: String="https://api.open-meteo.com/v1/forecast",private val geocodeBase: String="https://geocoding-api.open-meteo.com/v1/search") {
    private val client=OkHttpClient.Builder().callTimeout(10,TimeUnit.SECONDS).connectTimeout(8,TimeUnit.SECONDS).followRedirects(false).followSslRedirects(false).build()
    private suspend fun get(url: HttpUrl): JsonObject=suspendCancellableCoroutine { continuation->
        val call=client.newCall(Request.Builder().url(url).header("Accept","application/json").build())
        continuation.invokeOnCancellation {call.cancel()}
        call.enqueue(object: Callback {
            override fun onFailure(call: Call,e: IOException){if(continuation.isActive)continuation.resumeWithException(IOException("Weather provider unreachable."))}
            override fun onResponse(call: Call,response: Response){
                try {
                    val result=response.use {r->
                        if(!r.isSuccessful)throw IOException("Weather provider returned HTTP ${r.code}.")
                        val out=ByteArrayOutputStream()
                        r.body?.byteStream()?.use {input->val buffer=ByteArray(4096);while(true){val n=input.read(buffer);if(n<0)break;if(out.size()+n>262144)throw IOException("Weather response too large.");out.write(buffer,0,n)}} ?: throw IOException("Empty weather response.")
                        Json.parseToJsonElement(out.toByteArray().decodeToString(throwOnInvalidSequence=true)) as? JsonObject ?: throw IOException("Unsupported weather response.")
                    }
                    if(continuation.isActive)continuation.resume(result)
                }catch(e: Exception){if(continuation.isActive)continuation.resumeWithException(if(e is IOException)e else IOException("Unsupported weather response."))}
            }
        })
    }
    suspend fun forecast(c: Config): WeatherSnapshot {
        require(c.weatherLatitude!=null && c.weatherLongitude!=null)
        val url=forecastBase.toHttpUrl().newBuilder().addQueryParameter("latitude",c.weatherLatitude.toString()).addQueryParameter("longitude",c.weatherLongitude.toString())
            .addQueryParameter("current","temperature_2m,weather_code").addQueryParameter("hourly","temperature_2m,weather_code").addQueryParameter("daily","weather_code,temperature_2m_max,temperature_2m_min")
            .addQueryParameter("temperature_unit",if(c.weatherFahrenheit)"fahrenheit" else "celsius").addQueryParameter("timezone","auto").addQueryParameter("timeformat","unixtime").addQueryParameter("forecast_days","5").build()
        return parseWeather(get(url),weatherKey(c),System.currentTimeMillis())
    }
    suspend fun search(query: String): List<WeatherPlace> {
        require(query.trim().length in 2..100)
        val j=get(geocodeBase.toHttpUrl().newBuilder().addQueryParameter("name",query.trim()).addQueryParameter("count","8").addQueryParameter("language","en").addQueryParameter("format","json").build())
        return (j["results"] as? JsonArray)?.take(8)?.mapNotNull {value->val p=value as? JsonObject ?: return@mapNotNull null
            val lat=p.number("latitude")?.takeIf {it in -90.0..90.0} ?: return@mapNotNull null;val lon=p.number("longitude")?.takeIf {it in -180.0..180.0} ?: return@mapNotNull null
            val name=p.literal("name") ?: return@mapNotNull null;WeatherPlace(listOfNotNull(name,p.literal("admin1"),p.literal("country")).joinToString(", ").take(120),lat,lon)
        } ?: emptyList()
    }
    fun close(){client.dispatcher.cancelAll();client.connectionPool.evictAll();client.dispatcher.executorService.shutdown()}
}
class WeatherRepository(context: Context,val client: WeatherClient=WeatherClient(),private val now: ()->Long=System::currentTimeMillis) {
    val state=MutableStateFlow(WeatherState())
    private val mutex=Mutex()
    private val file=File(context.cacheDir,"umbra-weather-v1.json")
    suspend fun refresh(c: Config,force: Boolean=false)=mutex.withLock {
        if(c.weatherLatitude==null){state.value=WeatherState();return@withLock}
        val key=weatherKey(c)
        val cached=state.value.snapshot?.takeIf {it.key==key && it.fetchedAt<=now() && now()-it.fetchedAt<7*86400000L} ?: withContext(Dispatchers.IO) {runCatching {
            require(file.length() in 1..262144);Json.decodeFromString<WeatherSnapshot>(file.readText()).takeIf {it.key==key && it.fetchedAt<=now() && now()-it.fetchedAt<7*86400000L}
        }.getOrNull()}
        if(!force && cached!=null && now()-cached.fetchedAt<30*60000L){state.value=WeatherState(cached,message="Cached provider response");return@withLock}
        state.value=WeatherState(cached,true,"Updating weather…")
        try {
            val snapshot=client.forecast(c)
            withContext(Dispatchers.IO){runCatching {val temp=File(file.parentFile,"umbra-weather-v1.tmp");temp.writeText(Json.encodeToString(snapshot));if(!temp.renameTo(file))temp.delete()}}
            state.value=WeatherState(snapshot,message="Provider response received")
        }catch(e: CancellationException){state.value=WeatherState(cached,message=if(cached==null)"Weather update cancelled." else "Cached weather");throw e}
        catch(e: IOException){state.value=WeatherState(cached,message=if(cached!=null)"Offline / provider unavailable · cached forecast" else e.message ?: "Weather unavailable")}
    }
}
