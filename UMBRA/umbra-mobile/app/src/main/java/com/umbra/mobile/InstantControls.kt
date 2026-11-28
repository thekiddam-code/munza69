package com.umbra.mobile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.*
import androidx.lifecycle.repeatOnLifecycle
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.sync.Mutex
import kotlinx.serialization.json.*
import java.security.MessageDigest
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter

data class SavedMessage(val label: String,val text: String,val channel: String)
data class InstantAction(val id: String,val label: String,val path: String,val body: JsonObject)
data class InstantSnapshot(val base: String="",val pc: PcStatus?=null,val synchronizedAt: Long=0,val status: String="Native pairing required.",val busy: Boolean=false,val hostResult: JsonObject?=null,val hostWidgetId: String?=null)
fun instantActions(pc: PcStatus): List<InstantAction> {
    val actions=mutableListOf<InstantAction>()
    pc.quick.forEach {name->actions+=InstantAction("quick:$name",name,"api/action",buildJsonObject {put("action","quick");put("name",name)})}
    pc.messages.forEach {message->
        val digest=MessageDigest.getInstance("SHA-256").digest((message.label+"|"+message.channel+"|"+message.text).toByteArray()).take(10).joinToString(""){"%02x".format(it)}
        actions+=InstantAction("message:$digest",message.label,"api/action",buildJsonObject {put("action","text");put("text",message.text);put("channel",message.channel);put("speed","balanced")})
    }
    pc.macros.forEach {name->actions+=InstantAction("macro:$name",name,"api/action",buildJsonObject {put("action","macro");put("name",name)})}
    pc.emotes.forEach {emote->actions+=InstantAction("emote:${emote.index}:${emote.label}",emote.label,"api/action",buildJsonObject {put("action","fortnite_emote");put("index",emote.index)})}
    actions+=InstantAction("action:stop","Stop held inputs","api/action",buildJsonObject {put("action","stop")})
    return actions.distinctBy {it.id}
}
class InstantController(private val remote: IcarusClient,private val tokenFor: suspend (String)->String?) {
    constructor(remote: IcarusClient,vault: CredentialVault):this(remote,{base->vault.read(base)})
    val state=MutableStateFlow(InstantSnapshot())
    private val mutex=Mutex()
    val pcConnection=MutableStateFlow(PcConnectionState())
    val engineeringConsumers=MutableStateFlow<Set<String>>(emptySet())
    val reconnect=MutableStateFlow(0)
    private var monitorAttempt=0L
    private var catalogAttempt=0L
    fun reconnectNow(){reconnect.value++}
    fun markInactive(){pcConnection.value=pcConnection.value.copy(phase=PcPhase.Offline,latencyMs=null,error="Connection will be checked when visible.")}
    suspend fun refresh(c: Config,force: Boolean=false,engineering: Boolean=false) {
        if(!mutex.tryLock())return
        val base=serverBase(c)
        try {
            if(pcConnection.value.base!=base){pcConnection.value=PcConnectionState(base);monitorAttempt=0;catalogAttempt=0}
            if(base.isEmpty()){state.value=InstantSnapshot(status="Configure ICARUS first.");pcConnection.value=PcConnectionState(base,error="Configure the companion address.");return}
            val token=tokenFor(base)
            if(token==null){state.value=InstantSnapshot(base,status="Pair this phone in the ICARUS screen.");pcConnection.value=PcConnectionState(base,error="Native pairing required.");return}
            val now=System.currentTimeMillis()
            val cached=state.value.base==base && state.value.pc!=null && now-state.value.synchronizedAt<30000
            if(!force && cached && !engineering && pcConnection.value.phase==PcPhase.Connected)return
            val needsStatus=force || !cached || pcConnection.value.phase!=PcPhase.Connected || engineering && pcConnection.value.monitorUnsupported
            if(pcConnection.value.phase!=PcPhase.Connected)pcConnection.value=pcConnection.value.copy(phase=PcPhase.Connecting,error=null)
            state.value=state.value.takeIf {it.base==base}?.copy(busy=true) ?: InstantSnapshot(base,busy=true)
            suspend fun read(path: String): JsonObject {
                val started=System.nanoTime();val response=remote.request(base,path,c.timeout,token)
                pcConnection.value=pcConnection.value.copy(phase=PcPhase.Connected,checkedAt=System.currentTimeMillis(),latencyMs=((System.nanoTime()-started)/1000000).coerceAtLeast(0),error=null)
                return response
            }
            if(needsStatus) {
                val response=read("api/status")
                state.value=state.value.copy(base=base,pc=parsePcStatus(response),synchronizedAt=System.currentTimeMillis(),status=if(state.value.hostResult?.literal("state")=="pending")state.value.status else "Synchronized with the existing server.",busy=true)
                pcConnection.value=pcConnection.value.copy(name=response.literal("hostname") ?: response.literal("computer_name") ?: pcConnection.value.name)
            }
            if(engineering) {
                if(!pcConnection.value.monitorUnsupported || force || now-monitorAttempt>=60000) {
                    monitorAttempt=now
                    try {
                        val response=read("api/windows/monitor")
                        require(response.keys.containsAll(listOf("sample","age_seconds"))) {"Invalid monitor response"}
                        val sample=response["sample"]
                        require(sample==JsonNull || sample is JsonObject)
                        pcConnection.value=pcConnection.value.copy(monitor=response,monitorAt=System.currentTimeMillis(),monitorUnsupported=false,name=(sample as? JsonObject)?.literal("hostname") ?: pcConnection.value.name)
                    } catch(e: RemoteFailure) {if(e.status==404)pcConnection.value=pcConnection.value.copy(monitorUnsupported=true,monitor=null) else throw e}
                }
                if(force || now-catalogAttempt>=60000) {
                    catalogAttempt=now
                    try {
                        val response=read("api/windows/catalog")
                        require(response["hotkeys"] is JsonArray && response["supported"] is JsonPrimitive)
                        pcConnection.value=pcConnection.value.copy(catalog=response)
                    }catch(e: RemoteFailure){if(e.status!=404)throw e else pcConnection.value=pcConnection.value.copy(catalog=null)}
                }
            }
        }catch(e: CancellationException){pcConnection.value=pcConnection.value.copy(phase=PcPhase.Offline,latencyMs=null);throw e}
        catch(e: Exception){val message=(e as? RemoteFailure)?.message ?: "Companion response unavailable.";state.value=state.value.copy(status=message);pcConnection.value=pcConnection.value.copy(phase=PcPhase.Offline,latencyMs=null,error=message)}
        finally {state.value=state.value.copy(busy=false);mutex.unlock()}
    }
    suspend fun executeWindows(c: Config,id: String) {
        if(!mutex.tryLock())return
        try {
            val connection=pcConnection.value
            require(connection.base==serverBase(c) && connection.phase==PcPhase.Connected && connection.catalog?.truth("supported")==true)
            val spec=(connection.catalog["hotkeys"] as? JsonArray)?.mapNotNull {it as? JsonObject}?.firstOrNull {it.literal("id")==id} ?: error("Unavailable action")
            require(Regex("[a-z0-9_]{1,64}").matches(id))
            val token=tokenFor(connection.base) ?: throw RemoteFailure(401,"Pair native controls first.")
            state.value=state.value.copy(busy=true)
            val result=remote.request(connection.base,"api/windows/command",c.timeout,token,buildJsonObject {put("kind","hotkey");put("id",id);put("requestId",java.util.UUID.randomUUID().toString())})
            state.value=state.value.copy(status=result.literal("message") ?: (spec.literal("name") ?: "Action")+" · server acknowledged.")
        }catch(e: CancellationException){throw e}catch(e: Exception){state.value=state.value.copy(status=(e as? RemoteFailure)?.message ?: "PC action unavailable. Refresh Engineering first.")}
        finally {state.value=state.value.copy(busy=false);mutex.unlock()}
    }
    fun publish(base: String,pc: PcStatus) {state.value=InstantSnapshot(base,pc,System.currentTimeMillis(),"Synchronized with the existing server.")}
    suspend fun execute(c: Config,id: String,widgetId: String?=null) {
        if(id.startsWith("host:")){executeHost(c,id,widgetId);return}
        if(!mutex.tryLock())return
        try {
            val base=serverBase(c)
            val snapshot=state.value
            if(snapshot.base!=base || snapshot.pc==null)throw RemoteFailure(message="Refresh the current server controls first.")
            val local=widgetId?.let {widgetSpec(c,it)?.buttonOverrides?.get(id)} ?: c.customButtons.firstOrNull {"local:${it.id}"==id}
            if(local!=null)buttonSupport(local,snapshot.pc)?.let {throw RemoteFailure(message=it)}
            val action=widgetCatalog(c,snapshot.pc,widgetId,pcConnection.value.catalog).firstOrNull {it.id==id} ?: throw RemoteFailure(message="This command is no longer available. Refresh controls.")
            if(action.path=="api/windows/command") {
                val advertised=windowsButtonActions(pcConnection.value.catalog).map {it.body.literal("id")}
                require(action.body.literal("id") in advertised && pcConnection.value.base==base && pcConnection.value.phase==PcPhase.Connected)
            }
            val token=tokenFor(base) ?: throw RemoteFailure(401,"Pair this phone in the ICARUS screen.")
            state.value=snapshot.copy(busy=true,status="Sending ${action.label}…")
            val response=remote.request(base,action.path,c.timeout,token,action.body)
            state.value=state.value.copy(status=response.number("queued")?.let {"Queued #${it.toInt()} · PC execution pending."} ?: response.literal("message") ?: "Server acknowledged ${action.label}.")
        }catch(e:CancellationException){throw e}catch(e:Exception){state.value=state.value.copy(status=((e as? RemoteFailure)?.message ?: "Command failed.")+" Delivery may be unconfirmed; no automatic retry.")}
        finally{state.value=state.value.copy(busy=false);mutex.unlock()}
    }
    fun dismissHostResult(widgetId: String?) {if(state.value.hostWidgetId==widgetId)state.value=state.value.copy(hostResult=null,hostWidgetId=null)}
    suspend fun executeHost(c: Config,id: String,widgetId: String?,outputId: String?=null) {
        if(!mutex.tryLock())return
        try {
            val base=serverBase(c);val snapshot=state.value
            if(snapshot.base!=base || snapshot.pc==null)throw RemoteFailure(message="Synchronize the paired host first.")
            require(id in setOf("host:arctis","host:save-clip"))
            require(widgetId!=null && widgetSpec(c,widgetId)?.buttonSet=="mixed")
            val token=tokenFor(base) ?: throw RemoteFailure(401,"Pair this phone in ICARUS configuration.")
            state.value=snapshot.copy(busy=true,hostResult=null,hostWidgetId=widgetId,status="Sending host action…")
            val path=if(id=="host:arctis")"api/sonar/arctis" else "api/moments/save-clip"
            val body=buildJsonObject {put("requestId",java.util.UUID.randomUUID().toString());if(outputId!=null)put("output_id",outputId)}
            val response=remote.request(base,path,c.timeout,token,body)
            publishHost(response,widgetId,id,body.literal("requestId"))
        }catch(e: CancellationException){state.value=state.value.copy(hostResult=null,status="Host request interrupted; outcome unconfirmed. No action was replayed.");throw e}
        catch(e: Exception){state.value=state.value.copy(hostResult=null,status=(e as? RemoteFailure)?.message ?: "Host action unavailable.")}
        finally {state.value=state.value.copy(busy=false);mutex.unlock()}
    }
    private fun publishHost(response: JsonObject,widgetId: String?,id: String,requestId: String?=null) {
        val message=response.literal("message") ?: response.literal("error") ?: "Host outcome unavailable."
        val status=if(id=="host:arctis" && response.literal("state")=="verified") {
            val output=(response["output"] as? JsonObject)?.literal("id")
            val routes=response["routes"] as? JsonObject
            if(!response.truth("verified") || !response.truth("microphone_preserved") || output.isNullOrBlank() || listOf("game","chat","media","aux").any {routes?.literal(it)!=output})throw RemoteFailure(message="Host did not verify all four routes and microphone preservation.")
            message
        } else if(id=="host:save-clip") {
            val stage=response.literal("state")
            if(stage in setOf("pending","clip_detected")) {
                if(response.literal("request_id")!=requestId || requestId==null)throw RemoteFailure(message="Clip response did not identify this request; creation is unconfirmed.")
            }
            when(stage) {
                "clip_detected"->{val clip=response["clip"] as? JsonObject;if(!response.truth("clip_file_verified") || clip?.literal("name").isNullOrBlank() || (clip?.number("bytes") ?: 0.0)<=0)throw RemoteFailure(message="Host did not verify a new clip file.");"New clip file observed. Confirm in Moments. "+message}
                "pending"->"Clip creation pending. "+message
                else->"Clip creation unconfirmed. "+message
            }
        } else message
        state.value=state.value.copy(status=status,hostResult=response,hostWidgetId=widgetId)
    }
    suspend fun pollClip(c: Config,requestId: String,widgetId: String?) {
        if(!mutex.tryLock())return
        try {
            val base=serverBase(c);val current=state.value
            if(current.base!=base || current.hostWidgetId!=widgetId || current.hostResult?.literal("request_id")!=requestId || current.hostResult?.literal("state")!="pending")return
            require(runCatching {java.util.UUID.fromString(requestId)}.isSuccess)
            val token=tokenFor(base) ?: throw RemoteFailure(401,"Pairing expired during clip verification.")
            val response=remote.request(base,"api/moments/clip-status",c.timeout,token,buildJsonObject {put("requestId",requestId)})
            publishHost(response,widgetId,"host:save-clip",requestId)
        }catch(e: CancellationException){throw e}
        catch(e: Exception){state.value=state.value.copy(status=((e as? RemoteFailure)?.message ?: "Clip verification unavailable.")+" Clip creation is unconfirmed; the shortcut was not replayed.",hostResult=null)}
        finally {mutex.unlock()}
    }

}
