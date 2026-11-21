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
            val action=instantActions(snapshot.pc).firstOrNull {it.id==id} ?: throw RemoteFailure(message="This command is no longer available. Refresh controls.")
            val token=tokenFor(base) ?: throw RemoteFailure(401,"Pair this phone in the ICARUS screen.")
            state.value=snapshot.copy(busy=true,status="Sending ${action.label}…")
            val response=remote.request(base,action.path,c.timeout,token,action.body)
            state.value=state.value.copy(status=response.literal("message") ?: "Server acknowledged ${action.label}.")
        }catch(e:CancellationException){throw e}catch(e:Exception){state.value=state.value.copy(status=(e as? RemoteFailure)?.message ?: "Command failed.")}
        finally{state.value=state.value.copy(busy=false);mutex.unlock()}
    }
}
@Composable fun InstantControls(c: Config,model: LauncherModel,visible: Boolean,compact: Boolean) {
    val snapshot by model.instant.state.collectAsStateWithLifecycle()
    val lifecycle=LocalLifecycleOwner.current.lifecycle
    val scope=rememberCoroutineScope();var work by remember {mutableStateOf<Job?>(null)};var editing by remember {mutableStateOf(false)}
    LifecycleStartEffect(Unit){onStopOrDispose {work?.cancel()}}
    LaunchedEffect(lifecycle,visible,serverBase(c),c.refreshOnResume){if(visible && c.refreshOnResume)lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED){model.instant.refresh(c)}}
    val current=snapshot.takeIf {it.base==serverBase(c)} ?: InstantSnapshot(status="Refresh controls for the configured server.")
    val catalog=current.pc?.let(::instantActions) ?: emptyList()
    val ordered=catalog.sortedBy {c.instantOrder.indexOf(it.id).takeIf {n->n>=0} ?: Int.MAX_VALUE}
    val selected=if(c.instantFavorites.isEmpty())ordered else ordered.filter {it.id in c.instantFavorites}
    Column(verticalArrangement=Arrangement.spacedBy(6.dp)) {
        Readout("ICARUS / INSTANT ACTIONS",MaterialTheme.colorScheme.primary)
        Text(current.status,style=MaterialTheme.typography.bodySmall,modifier=Modifier.semantics {liveRegion=androidx.compose.ui.semantics.LiveRegionMode.Polite})
        if(current.synchronizedAt>0)Text("Last sync ${Instant.ofEpochMilli(current.synchronizedAt).atZone(ZoneId.systemDefault()).format(DateTimeFormatter.ofPattern("MMM d HH:mm:ss"))}",style=MaterialTheme.typography.bodySmall)
        Row {TextButton(onClick={if(work?.isActive!=true)work=scope.launch {model.instant.refresh(c,true)}},enabled=!current.busy){Text("Sync controls")};TextButton(onClick={editing=true},enabled=catalog.isNotEmpty()){Text("Arrange")}}
        if(current.pc==null)Text("Native pairing is separate from your browser. Open ICARUS to pair.",style=MaterialTheme.typography.bodySmall)
        (if(compact)selected.take(6) else selected).chunked(2).forEach {row->Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(6.dp)) {
            row.forEach {action->OutlinedButton(onClick={if(work?.isActive!=true)work=scope.launch {model.instant.execute(c,action.id)}},enabled=!current.busy,shape=Chamfer,modifier=Modifier.weight(1f)){Text(c.instantLabels[action.id] ?: action.label)}}
        } }
        if(c.instantFavorites.any {id->catalog.none {it.id==id}})Text("Some favorite actions are absent from the current server snapshot.",style=MaterialTheme.typography.bodySmall)
        if(!compact)Text("Quick-chat names are synchronized; key mappings remain on the server and are resolved there for each command. The status API does not expose key arrays. Saved messages come from the latest sync. Keep the intended game focused.",style=MaterialTheme.typography.bodySmall)
    }
    if(editing)InstantEditor(c,model,ordered){editing=false}
}
@Composable private fun InstantEditor(c: Config,model: LauncherModel,actions: List<InstantAction>,close: ()->Unit) {
    var labelAction by remember {mutableStateOf<InstantAction?>(null)};var label by remember {mutableStateOf("")}
    if(labelAction!=null)AlertDialog(onDismissRequest={labelAction=null},title={Text("Local button label")},text={OutlinedTextField(label,{label=it.take(48)},singleLine=true)},confirmButton={TextButton(onClick={val id=labelAction!!.id;model.change {it.copy(instantLabels=it.instantLabels+(id to label.trim()))};labelAction=null},enabled=label.isNotBlank() && label.none(Char::isISOControl)){Text("Save")}})
    DesktopEditorDialog("Instant buttons / current server",close,confirm={TextButton(onClick=close){Text("Done")}}) {
        Text("No server mappings are overwritten. Select favorites, move buttons, or edit local labels.",style=MaterialTheme.typography.bodySmall)
        actions.forEachIndexed {index,action->
            Row {Checkbox(action.id in c.instantFavorites,{selected->model.change {it.copy(instantFavorites=if(selected)it.instantFavorites+action.id else it.instantFavorites-action.id)}});Text(c.instantLabels[action.id] ?: action.label,modifier=Modifier.weight(1f))}
            Row {
                TextButton(onClick={model.change {it.copy(instantOrder=moveItem(actions.map {a->a.id},action.id,-1))}},enabled=index>0){Text("↑")}
                TextButton(onClick={model.change {it.copy(instantOrder=moveItem(actions.map {a->a.id},action.id,1))}},enabled=index<actions.lastIndex){Text("↓")}
                TextButton(onClick={labelAction=action;label=c.instantLabels[action.id] ?: action.label}){Text("Label")}
            }
        }
    }
}
