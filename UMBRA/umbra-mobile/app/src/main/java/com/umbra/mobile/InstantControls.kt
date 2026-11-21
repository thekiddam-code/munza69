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
data class InstantSnapshot(val base: String="",val pc: PcStatus?=null,val synchronizedAt: Long=0,val status: String="Native pairing required.",val busy: Boolean=false)
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
    suspend fun refresh(c: Config,force: Boolean=false) {
        if(!mutex.tryLock())return
        val base=serverBase(c)
        try {
            if(base.isEmpty()){state.value=InstantSnapshot(status="Configure ICARUS first.");return}
            val token=tokenFor(base)
            if(token==null){state.value=InstantSnapshot(base,status="Pair this phone in the ICARUS screen.");return}
            if(!force && state.value.base==base && state.value.pc!=null && System.currentTimeMillis()-state.value.synchronizedAt<30000)return
            state.value=state.value.takeIf {it.base==base}?.copy(busy=true,status="Synchronizing server controls…") ?: InstantSnapshot(base,busy=true)
            val pc=remote.status(base,token,c.timeout)
            state.value=InstantSnapshot(base,pc,System.currentTimeMillis(),"Synchronized with the existing server.")
        }catch(e:CancellationException){throw e}catch(e:Exception){state.value=state.value.copy(status=(e as? RemoteFailure)?.message ?: "Synchronization unavailable.")}
        finally {state.value=state.value.copy(busy=false);mutex.unlock()}
    }
    fun publish(base: String,pc: PcStatus) {state.value=InstantSnapshot(base,pc,System.currentTimeMillis(),"Synchronized with the existing server.")}
    suspend fun execute(c: Config,id: String) {
        if(!mutex.tryLock())return
        try {
            val base=serverBase(c)
            val snapshot=state.value
            if(snapshot.base!=base || snapshot.pc==null)throw RemoteFailure(message="Refresh the current server controls first.")
            val local=c.customButtons.firstOrNull {"local:${it.id}"==id}
            if(local!=null)buttonSupport(local,snapshot.pc)?.let {throw RemoteFailure(message=it)}
            val action=buttonCatalog(c,snapshot.pc).firstOrNull {it.id==id} ?: throw RemoteFailure(message="This command is no longer available. Refresh controls.")
            val token=tokenFor(base) ?: throw RemoteFailure(401,"Pair this phone in the ICARUS screen.")
            state.value=snapshot.copy(busy=true,status="Sending ${action.label}…")
            val response=remote.request(base,action.path,c.timeout,token,action.body)
            state.value=state.value.copy(status=response.number("queued")?.let {"Queued #${it.toInt()} · PC execution pending."} ?: response.literal("message") ?: "Server acknowledged ${action.label}.")
        }catch(e:CancellationException){throw e}catch(e:Exception){state.value=state.value.copy(status=(e as? RemoteFailure)?.message ?: "Command failed.")}
        finally{state.value=state.value.copy(busy=false);mutex.unlock()}
    }
}
