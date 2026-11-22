package com.umbra.mobile

import androidx.compose.runtime.*
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.*
import androidx.lifecycle.repeatOnLifecycle
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.serialization.json.*
import java.net.URI

enum class PcPhase { Connected, Connecting, Offline }
data class PcConnectionState(val base: String="",val phase: PcPhase=PcPhase.Offline,val name: String?=null,val latencyMs: Long?=null,
    val checkedAt: Long=0,val monitorAt: Long=0,val error: String?=null,val monitor: JsonObject?=null,val catalog: JsonObject?=null,val monitorUnsupported: Boolean=false)
val ENGINEERING_MODULES=listOf("cpu","gpu","ram","power","network","actions")
val ENGINEERING_KINDS=ENGINEERING_MODULES.map {"engineering_$it"}
fun connectionMethod(base: String): String {
    val host=runCatching {URI(base).host?.lowercase()?.removePrefix("[")?.removeSuffix("]")}.getOrNull() ?: return "Unknown"
    if(host.endsWith(".ts.net") || host.startsWith("fd7a:115c:a1e0:"))return "Tailscale address · route unverified"
    val octets=host.split('.').mapNotNull {it.toIntOrNull()?.takeIf {n->n in 0..255}}
    if(host.split('.').size==4 && octets.size==4) {
        if(octets[0]==100 && octets[1] in 64..127)return "Tailscale-range address · route unverified"
        if(octets[0]==10 || octets[0]==192 && octets[1]==168 || octets[0]==172 && octets[1] in 16..31 || octets[0]==127)return "Local network address · route unverified"
    }
    return "Unknown · route not reported"
}
fun engineeringInterval(consumers: Boolean,powerSave: Boolean,unsupported: Boolean)=if(powerSave)60000L else if(!consumers)30000L else if(unsupported)10000L else 3000L
/** One polling loop at the Activity root; all consumers share the existing InstantController. */
@Composable fun SharedPcConnection(c: Config,model: LauncherModel,active: Boolean,powerSave: Boolean,remoteVisible: Boolean,networkVersion: Long) {
    val lifecycle=LocalLifecycleOwner.current.lifecycle
    val handledReconnect=remember(model.instant){intArrayOf(0)}
    LaunchedEffect(model.instant,lifecycle,serverBase(c),c.timeout,c.pcIndicator,active,powerSave,remoteVisible,networkVersion) {
        try {
            if(active)lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED) {
                try {
                combine(model.instant.engineeringConsumers,model.instant.reconnect) {owners,reconnect->owners.isNotEmpty() to reconnect}.distinctUntilChanged().collectLatest {(engineering,reconnect)->
                    val manual=reconnect>handledReconnect[0]
                    handledReconnect[0]=reconnect
                    if(!c.pcIndicator && !engineering && !remoteVisible) {
                        if(manual)model.instant.refresh(c,force=true)
                        return@collectLatest
                    }
                    var first=true
                    while(isActive) {
                        model.instant.refresh(c,force=first && manual,engineering=engineering)
                        first=false
                        delay(engineeringInterval(engineering,powerSave,model.instant.pcConnection.value.monitorUnsupported))
                    }
                }
                } finally {model.instant.markInactive()}
            }
        } finally {model.instant.markInactive()}
    }
}
@Composable fun EngineeringDemand(model: LauncherModel,id: String,visible: Boolean) {
    val lifecycle=LocalLifecycleOwner.current.lifecycle
    LifecycleStartEffect(model.instant,id,visible) {
        if(visible)model.instant.engineeringConsumers.value=model.instant.engineeringConsumers.value+id
        onStopOrDispose {model.instant.engineeringConsumers.value=model.instant.engineeringConsumers.value-id}
    }
}
