package com.umbra.mobile

import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.serialization.json.*
import okhttp3.*
import okhttp3.HttpUrl.Companion.toHttpUrl
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.ByteArrayOutputStream
import java.io.IOException
import java.util.concurrent.TimeUnit
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException

class RemoteFailure(val status: Int? = null, message: String = "Unreachable. Check Tailscale and the server.") : IOException(message)
data class GameEmote(val index: Int,val label: String)
data class PcStatus(val cpu: Double?,val ram: Double?,val tvConfigured: Boolean,val macros: List<String>,val quick: List<String>,val emotes: List<GameEmote>,val messages: List<SavedMessage> = emptyList())
data class ShipStatus(val online: Boolean,val data: JsonObject?,val age: Double?)
fun JsonObject.number(key: String): Double? = (get(key) as? JsonPrimitive)?.takeUnless { it.isString }?.doubleOrNull?.takeIf { it.isFinite() }
fun JsonObject.literal(key: String): String? = (get(key) as? JsonPrimitive)?.takeIf { it.isString }?.content?.take(120)
fun JsonObject.truth(key: String): Boolean = (get(key) as? JsonPrimitive)?.takeUnless { it.isString }?.booleanOrNull == true
private fun JsonObject.names(key: String): List<String> = (get(key) as? JsonArray)?.mapNotNull { (it as? JsonPrimitive)?.takeIf { p -> p.isString }?.content?.takeIf { name -> name.length in 1..120 && name.none(Char::isISOControl) } } ?: emptyList()
fun parsePcStatus(j: JsonObject): PcStatus = PcStatus(j.number("cpu")?.takeIf { it in 0.0..100.0 },j.number("ram")?.takeIf { it in 0.0..100.0 },j.truth("tv_configured"),j.names("macros"),j.names("quick"),
    (j["fortnite_emotes"] as? JsonArray)?.take(9)?.mapIndexedNotNull { i,value -> (value as? JsonObject)?.literal("label")?.takeIf { it.isNotBlank() }?.let { GameEmote(i,it) } } ?: emptyList(),
    (j["custom_messages"] as? JsonArray)?.take(40)?.mapNotNull {value->
        val m=value as? JsonObject ?: return@mapNotNull null
        fun exactText(key: String,max: Int)=(m[key] as? JsonPrimitive)?.takeIf {it.isString}?.content?.takeIf {it.length in 1..max && it.isNotBlank() && it.none(Char::isISOControl)}
        val label=exactText("label",32) ?: return@mapNotNull null
        val text=exactText("text",120) ?: return@mapNotNull null
        val channel=exactText("channel",5)?.takeIf {it in listOf("team","match")} ?: return@mapNotNull null
        SavedMessage(label,text,channel)
    } ?: emptyList())
class IcarusClient {
    private val shared = OkHttpClient.Builder().followRedirects(false).followSslRedirects(false).build()
    suspend fun request(base: String,path: String,timeout: Int,token: String? = null,body: JsonObject? = null): JsonObject {
        require(validDeckUrl(base) && timeout in 1..30)
        require(path in setOf("api/rocket/chat-sound","api/sonar/arctis","api/moments/save-clip","api/moments/clip-status","api/host-actions/status","api/pair","api/unpair","api/status","api/icarus/telemetry","api/icarus/command","api/action","api/sounds/library","api/sounds/play","api/sounds/stop","api/sounds/output","api/sounds/edit","api/audio/profile","api/windows/monitor","api/windows/catalog","api/windows/command"))
        val client=shared.newBuilder().callTimeout(timeout.toLong(),TimeUnit.SECONDS).connectTimeout(timeout.toLong(),TimeUnit.SECONDS).readTimeout(timeout.toLong(),TimeUnit.SECONDS).build()
        val request=Request.Builder().url(base.toHttpUrl().resolve(path)!!).header("Accept","application/json").apply {
            if(!token.isNullOrEmpty()) header("Authorization","Bearer $token")
            if(body!=null) post(body.toString().toRequestBody("application/json".toMediaType()))
        }.build()
        return suspendCancellableCoroutine { continuation ->
            val call=client.newCall(request)
            continuation.invokeOnCancellation { call.cancel() }
            call.enqueue(object:Callback {
                override fun onFailure(call: Call,e: IOException) { if(continuation.isActive)continuation.resumeWithException(RemoteFailure()) }
                override fun onResponse(call: Call,response: Response) {
                    try {
                        val parsed=response.use { r ->
                            if(!r.isSuccessful && path in setOf("api/rocket/chat-sound","api/sonar/arctis","api/moments/save-clip","api/moments/clip-status","api/host-actions/status")) {
                                val bytes=r.body?.byteStream()?.use {input->
                                    val output=ByteArrayOutputStream();val buffer=ByteArray(4096)
                                    while(output.size()<=131072){val n=input.read(buffer);if(n<0)break;output.write(buffer,0,n)}
                                    output.toByteArray()
                                }
                                val detail=if(bytes!=null && bytes.size<=131072)runCatching {(Json.parseToJsonElement(bytes.decodeToString()) as? JsonObject)?.literal("error")?.filterNot(Char::isISOControl)}.getOrNull() else null
                                throw RemoteFailure(r.code,when(r.code){401->"Pairing required or expired.";403->"Authorization rejected.";404->if(path=="api/rocket/chat-sound")"Install the chat-sounds update on the paired PC. Chat was not sent." else "Install the host-actions update on the paired PC.";else->detail ?: "Host returned HTTP ${r.code}."})
                            }
                            if(!r.isSuccessful) throw RemoteFailure(r.code,when(r.code){401->"Pairing required or expired.";403->"Pairing code or authorization rejected.";404->"This endpoint is unavailable on the configured server.";in 300..399->"Redirect refused. Configure the final server address.";409->"Configuration changed or output unavailable. Refresh and check Audio Output before retrying.";429->"Server busy. Wait before retrying.";else->"Server returned HTTP ${r.code}."})
                            val output=ByteArrayOutputStream()
                            r.body?.byteStream()?.use { input ->
                                val buffer=ByteArray(4096)
                                while(true) { val n=input.read(buffer);if(n<0)break;if(output.size()+n>(if(path=="api/sounds/library")2097152 else 131072))throw RemoteFailure(message="Server response exceeds the supported size.");output.write(buffer,0,n) }
                            } ?: throw RemoteFailure(message="Empty server response.")
                            Json.parseToJsonElement(output.toByteArray().decodeToString(throwOnInvalidSequence=true)) as? JsonObject ?: throw RemoteFailure(message="Unsupported server response.")
                        }
                        if(continuation.isActive)continuation.resume(parsed)
                    } catch(e: Exception) { if(continuation.isActive)continuation.resumeWithException(if(e is RemoteFailure)e else RemoteFailure(message="Unsupported server response.")) }
                }
            })
        }
    }
    suspend fun pair(base: String,pin: String,timeout: Int): String {
        require(pin.length in 1..64 && pin.none { it.isISOControl() })
        val response=request(base,"api/pair",timeout,body=buildJsonObject { put("pin",pin) })
        return (response["token"] as? JsonPrimitive)?.takeIf { it.isString }?.content?.takeIf { Regex("[A-Za-z0-9_-]{16,512}").matches(it) } ?: throw RemoteFailure(message="Server did not return a supported pairing token.")
    }
    suspend fun status(base: String,token: String,timeout: Int) = parsePcStatus(request(base,"api/status",timeout,token))
    suspend fun ship(base: String,token: String,timeout: Int): ShipStatus {
        val j=request(base,"api/icarus/telemetry",timeout,token)
        val online=j.truth("online")
        return ShipStatus(online,if(online)j["telemetry"] as? JsonObject else null,j.number("age"))
    }
    fun close() { shared.dispatcher.cancelAll();shared.connectionPool.evictAll();shared.dispatcher.executorService.shutdown() }
}
