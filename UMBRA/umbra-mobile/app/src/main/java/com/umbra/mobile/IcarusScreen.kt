package com.umbra.mobile

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LifecycleStartEffect
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.lifecycle.repeatOnLifecycle
import kotlinx.coroutines.*
import kotlinx.serialization.json.*

@OptIn(ExperimentalLayoutApi::class)
@Composable fun IcarusScreen(c: Config,model: LauncherModel,accent: Color,initialModule: String,open: (Intent)->Unit,configure: ()->Unit,powerSave: Boolean,networkVersion: Long) {
    val lifecycle=LocalLifecycleOwner.current.lifecycle
    val scope=rememberCoroutineScope()
    val base=serverBase(c)
    var module by rememberSaveable(initialModule) { mutableStateOf(if(initialModule in listOf("Engineering","Lounge","Simulator")) initialModule else "Engineering") }
    var pin by remember { mutableStateOf("") }
    var paired by remember(base) { mutableStateOf(false) }
    var pc by remember(base) { mutableStateOf<PcStatus?>(null) }
    var ship by remember(base) { mutableStateOf<ShipStatus?>(null) }
    var status by remember(base) { mutableStateOf("Not checked") }
    var refreshed by remember(base) { mutableStateOf<String?>(null) }
    var refresh by remember { mutableIntStateOf(0) }
    val refreshGate=remember(base) { RefreshGate() }
    var actionJob by remember { mutableStateOf<Job?>(null) }
    var busy by remember { mutableStateOf(false) }
    var visible by remember { mutableStateOf(false) }
    LifecycleStartEffect(Unit) {
        visible=true
        onStopOrDispose { visible=false;actionJob?.cancel();busy=false;pin="" }
    }
    val networkKey=if(c.refreshOnNetwork) networkVersion else 0L
    LaunchedEffect(lifecycle,base,c.timeout,refresh,networkKey,c.foregroundRefreshSeconds,c.refreshOnResume,powerSave) {
        lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED) {
            paired=model.vault.read(base)!=null
            if(base.isEmpty()) { status="Configure the server address or Remote Deck URL.";return@repeatOnLifecycle }
            if(!paired) { status="Pair this native client using the server PIN. Browser authentication is separate.";return@repeatOnLifecycle }
            val triggered=refreshGate.shouldRefresh(c.refreshOnResume,c.refreshOnNetwork,refresh,networkVersion,base+"|"+c.timeout)
            if(!triggered) {
                if(c.foregroundRefreshSeconds==0 || powerSave) return@repeatOnLifecycle
                delay(c.foregroundRefreshSeconds*1000L)
            }
            do {
                val token=model.vault.read(base) ?: break
                status="Checking configured server…"
                try {
                    pc=model.remote.status(base,token,c.timeout)
                    ship=try { model.remote.ship(base,token,c.timeout) } catch(e: RemoteFailure) { if(e.status==404) null else throw e }
                    model.instant.publish(base,pc!!)
                    refreshed=java.time.LocalTime.now().withNano(0).toString()
                    status="Authenticated server response · HTTP 200"
                } catch(e: RemoteFailure) {
                    pc=null;ship=null;status=e.message ?: "Unreachable"
                    if(e.status==401) { model.vault.clear();paired=false }
                }
                if(c.foregroundRefreshSeconds==0 || powerSave) break
                delay(c.foregroundRefreshSeconds*1000L)
            } while(isActive)
        }
    }
    fun runAction(block: suspend ()->Unit) {
        if(busy || !visible) return
        busy=true
        actionJob=scope.launch {
            try { block() } catch(e: CancellationException) { throw e }
            catch(e: Exception) { status=if(e is RemoteFailure || e is java.io.IOException) e.message ?: "Request failed" else "Unsupported server response." }
            finally { busy=false }
        }
    }
    fun requestCommand(label: String,path: String,body: JsonObject) {
        runAction {
            val token=model.vault.read(base) ?: throw RemoteFailure(401,"Pair this client first.")
            val response=model.remote.request(base,path,c.timeout,token,body)
            status=response.number("queued")?.let { "Queued #${it.toInt()} · waiting for PC execution" } ?: "$label · server acknowledged request."
        }
    }
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(12.dp)) {
        Readout("ICARUS / NATIVE REMOTE SYSTEMS",accent)
        Row(Modifier.fillMaxWidth()) { TextButton(onClick=configure){Text("Connection settings")};TextButton(onClick={refresh++},enabled=!busy){Text("Refresh status")} }
        Text(status,modifier=Modifier.fillMaxWidth().semantics { liveRegion=LiveRegionMode.Polite },color=if(pc!=null) Green else Muted)
        Text(if(refreshed==null) "No authenticated snapshot yet." else "Snapshot at $refreshed · refresh to verify current state.",style=MaterialTheme.typography.bodySmall)
        val destination=remoteDestination(c,module)
        Button(onClick={if(validDeckUrl(destination))open(Intent(Intent.ACTION_VIEW,Uri.parse(destination).normalizeScheme())) else configure()},shape=Chamfer,modifier=Modifier.fillMaxWidth()){Text("Open $module Remote Deck")}
        if(!paired) Frame(accent.copy(alpha=.5f)) {
            Text("Pair native controls",style=MaterialTheme.typography.titleMedium)
            Text("Use the PIN shown by your existing Remote Deck server. The token stays encrypted on this phone and is excluded from settings exports.",style=MaterialTheme.typography.bodySmall)
            OutlinedTextField(pin,{pin=it.take(64)},label={Text("Server pairing PIN")},singleLine=true,visualTransformation=PasswordVisualTransformation(),keyboardOptions=KeyboardOptions(keyboardType=KeyboardType.NumberPassword),modifier=Modifier.fillMaxWidth())
            Button(onClick={runAction {
                val entered=pin.trim();pin=""
                val token=model.remote.pair(base,entered,c.timeout)
                if(serverBase(model.config.value)!=base) throw RemoteFailure(message="Server changed. Pair again with the current server.")
                model.vault.remember(base,token);paired=true;refresh++;status="Pairing saved securely."
            }},enabled=base.isNotEmpty() && pin.isNotBlank() && !busy,shape=Chamfer){Text("Pair phone")}
        } else TextButton(onClick={runAction {
            val token=model.vault.read(base)
            try { if(token!=null)model.remote.request(base,"api/unpair",c.timeout,token,buildJsonObject{}) }
            finally { model.vault.clear();paired=false;pc=null;ship=null;status="Local pairing removed. Re-pair if needed." }
        }},enabled=!busy){Text("Forget native pairing")}
        FlowRow(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(6.dp)) {
            listOf("Engineering","Lounge","Simulator").forEach { tab -> FilterChip(selected=module==tab,onClick={module=tab},label={Text(tab,style=MaterialTheme.typography.labelSmall)}) }
        }
        when(module) {
            "Engineering" -> Frame(accent) {
                Readout("PC / SERVER SNAPSHOT",accent)
                Text("PC CPU: ${pc?.cpu?.let { "$it%" } ?: "Unavailable"}")
                Text("PC RAM: ${pc?.ram?.let { "$it%" } ?: "Unavailable"}")
                Text(when { ship==null->"Simulation telemetry endpoint unavailable or not checked.";ship?.online==true->"Simulation online at last refresh";else->"Simulation offline at last refresh" })
                if(ship?.online==true) {
                    val data=ship?.data
                    Text("Episode: ${(data?.get("episode") as? JsonPrimitive)?.contentOrNull?.take(40) ?: "Unavailable"}")
                    Text("Simulation time: ${data?.literal("time") ?: "Unavailable"}")
                    Text("Speed: ${data?.number("speed") ?: "Unavailable"} · Crew: ${data?.number("crewTotal")?.toInt() ?: "Unavailable"}")
                    listOf("Pause" to "pause","Resume" to "resume","1× speed" to "speed1","5× speed" to "speed5","20× speed" to "speed20","Save simulation" to "save").forEach { (label,value) ->
                        OutlinedButton(onClick={requestCommand(label,"api/icarus/command",buildJsonObject { put("command",value) })},enabled=!busy,shape=Chamfer,modifier=Modifier.fillMaxWidth()){Text(label)}
                    }
                }
                Text("Diagnostics use actual HTTP responses. No host key or privileged telemetry publisher endpoint is used.",style=MaterialTheme.typography.bodySmall)
            }
            "Lounge" -> Frame(accent) {
                Readout("SAMSUNG TV / EXISTING SERVER",accent)
                Text(if(pc?.tvConfigured==true) "TV configured on the server. Key delivery is acknowledged by the server." else "TV configuration is unavailable. Configure and pair the TV in Remote Deck first.")
                if(pc?.tvConfigured==true) {
                    val keys=listOf("Home" to "home","Back" to "back","Up" to "up","Left" to "left","OK" to "ok","Right" to "right","Down" to "down","Volume +" to "vol_up","Volume −" to "vol_down","Mute" to "mute","Play / pause" to "play_pause","Source" to "source","Power off" to "power_off")
                    keys.chunked(2).forEach { row -> Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(6.dp)) { row.forEach { (label,key) -> OutlinedButton(onClick={requestCommand(label,"api/tv/key",buildJsonObject { put("key",key) })},enabled=!busy,shape=Chamfer,modifier=Modifier.weight(1f)){Text(label)} } } }
                }
                Text("Direct TV app launching is not exposed by the inspected server. No fake Stremio or TV Plus launch controls are shown.",style=MaterialTheme.typography.bodySmall)
            }
            else -> Column {
                // Parent status refresh publishes the shared catalog; avoid a duplicate GET.
                InstantControls(c,model,false,compact=false)
                Frame(accent) {
                Readout("SIMULATOR / CONFIGURED ACTIONS",accent)
                if(pc==null) Text("Refresh an authenticated server snapshot to discover configured game controls.")
                else {
                    Text("Configured PC macros")
                    pc!!.macros.forEach { label -> OutlinedButton(onClick={requestCommand(label,"api/action",buildJsonObject { put("action","macro");put("name",label) })},enabled=!busy,shape=Chamfer,modifier=Modifier.fillMaxWidth()){Text(label)} }
                    Text("Rocket League quick chat")
                    pc!!.quick.forEach { label -> OutlinedButton(onClick={requestCommand(label,"api/action",buildJsonObject { put("action","quick");put("name",label) })},enabled=!busy,shape=Chamfer,modifier=Modifier.fillMaxWidth()){Text(label)} }
                    Text("Configured Fortnite emotes")
                    pc!!.emotes.forEach { emote -> OutlinedButton(onClick={requestCommand(emote.label,"api/action",buildJsonObject { put("action","fortnite_emote");put("index",emote.index) })},enabled=!busy,shape=Chamfer,modifier=Modifier.fillMaxWidth()){Text(emote.label)} }
                    OutlinedButton(onClick={requestCommand("Stop held game inputs","api/action",buildJsonObject { put("action","stop") })},enabled=!busy,shape=Chamfer){Text("Stop held inputs")}
                    Text("These actions require the intended game/application to be focused on the PC. Only server-configured shortcuts are offered.",style=MaterialTheme.typography.bodySmall)
                }
            }
        }
        }
        Spacer(Modifier.height(16.dp))
    }
}
