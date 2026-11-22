package com.umbra.mobile

import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.*
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.compose.LifecycleStartEffect
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import kotlinx.serialization.json.*
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter

fun JsonObject.reading(key: String,min: Double=0.0,max: Double=Double.MAX_VALUE): Double?=number(key)?.takeIf {it in min..max}
fun engineeringSample(connection: PcConnectionState): JsonObject? {
    if(connection.phase!=PcPhase.Connected)return null
    val monitor=connection.monitor ?: return null
    if(connection.monitorAt<=0)return null
    val age=monitor.reading("age_seconds",0.0,15.0) ?: return null
    if(age+(System.currentTimeMillis()-connection.monitorAt).coerceAtLeast(0)/1000.0>20)return null
    return (monitor["sample"] as? JsonObject)?.takeIf {it.truth("supported")}
}
private fun metric(value: Double?,unit: String) = value?.let {"%.1f%s".format(it,unit)} ?: "Unavailable"
@Composable fun PcConnectionIndicator(c: Config,model: LauncherModel) {
    val saved by model.instant.pcConnection.collectAsStateWithLifecycle()
    val state=saved.takeIf {it.base==serverBase(c)} ?: PcConnectionState()
    var panel by remember {mutableStateOf(false)}
    if(!c.pcIndicator)return
    val color=when(state.phase){PcPhase.Connected->Green;PcPhase.Connecting->Amber;PcPhase.Offline->MaterialTheme.colorScheme.error}
    TextButton(onClick={panel=true},contentPadding=PaddingValues(4.dp),modifier=Modifier.sizeIn(minWidth=48.dp,minHeight=48.dp).testTag("pc-connection-indicator").semantics {contentDescription="PC connection: ${state.phase.name}"}) {Text("● PC",color=color,style=MaterialTheme.typography.labelSmall)}
    if(panel)AlertDialog(onDismissRequest={panel=false},title={Text("PC connection")},text={Column(verticalArrangement=Arrangement.spacedBy(8.dp)) {
        PcConnectionReadout(state)
    }},confirmButton={TextButton(onClick={model.instant.reconnectNow()}){Text("Reconnect")}},dismissButton={TextButton(onClick={panel=false}){Text("Close")}})
}
@Composable fun PcConnectionReadout(state: PcConnectionState) {
    Text("PC name: ${state.name ?: "Not reported by companion"}")
    Text("Status: ${state.phase.name}",modifier=Modifier.semantics {liveRegion=LiveRegionMode.Polite})
    Text("Connection: ${connectionMethod(state.base)}")
    Text("Latency: ${state.latencyMs?.let {"$it ms · HTTP round trip"} ?: "Unavailable"}")
    if(state.checkedAt>0)Text("Last authenticated response: "+Instant.ofEpochMilli(state.checkedAt).atZone(ZoneId.systemDefault()).format(DateTimeFormatter.ofPattern("HH:mm:ss")),style=MaterialTheme.typography.bodySmall)
    state.error?.let {Text(it,color=MaterialTheme.colorScheme.error)}
}
@Composable fun EngineeringWidget(item: DesktopItem,c: Config,model: LauncherModel,visible: Boolean,accent: Color,expand: (Rect)->Unit) {
    val w=item.widget!!;var bounds by remember(item.id){mutableStateOf(Rect.Zero)}
    val color=if(w.accent.isEmpty())accent else Color(android.graphics.Color.parseColor(w.accent))
    EngineeringDemand(model,"widget:${item.id}",visible && !w.collapsed && bounds.width>1 && bounds.height>1)
    Surface(color=if(w.transparent)Color.Transparent else Panel,shape=Chamfer,modifier=Modifier.fillMaxSize().onGloballyPositioned {bounds=it.boundsInWindow()}.testTag("engineering-widget-${item.id}").clickable {expand(bounds)}) {
        Column(Modifier.padding(8.dp).verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(4.dp)) {
            Text("PC / "+w.kind.removePrefix("engineering_").uppercase(),color=color,style=MaterialTheme.typography.labelLarge)
            if(!w.collapsed)EngineeringReadings(w.kind.removePrefix("engineering_"),c,model,w.showDetails)
        }
    }
}
@Composable fun EngineeringModule(module: String,c: Config,model: LauncherModel,visible: Boolean=true,details: Boolean=true) {
    val owner=remember {desktopId()}
    EngineeringDemand(model,owner,visible)
    Column(Modifier.fillMaxWidth().testTag("engineering-module-$module"),verticalArrangement=Arrangement.spacedBy(8.dp)) {EngineeringReadings(module,c,model,details)}
}
@Composable private fun EngineeringReadings(module: String,c: Config,model: LauncherModel,details: Boolean) {
    val current by model.instant.pcConnection.collectAsStateWithLifecycle()
    val buttons by model.instant.state.collectAsStateWithLifecycle()
    val connection=current.takeIf {it.base==serverBase(c)} ?: PcConnectionState()
    val pc=buttons.pc.takeIf {buttons.base==connection.base && connection.phase==PcPhase.Connected}
    val sample=engineeringSample(connection)
    when(module) {
        "cpu"->{Text("CPU: "+metric(sample?.reading("cpu_percent",0.0,100.0) ?: if(connection.monitorUnsupported)pc?.cpu else null,"%"));if(details){Text("Temperature: "+metric(sample?.reading("cpu_temperature_c",-100.0,200.0),"°C"));sample?.literal("cpu_model")?.let {Text(it,style=MaterialTheme.typography.bodySmall)}}}
        "gpu"->{val gpus=(sample?.get("gpus") as? JsonArray)?.mapNotNull {it as? JsonObject} ?: emptyList()
            if(gpus.isEmpty())Text("GPU sensors: Unavailable")
            gpus.forEach {gpu->Text(gpu.literal("model") ?: "GPU");Text("Usage: "+metric(gpu.reading("utilization_percent",0.0,100.0),"%"));if(details){Text("Temperature: "+metric(gpu.reading("temperature_c",-100.0,200.0),"°C"));Text("VRAM: "+metric(gpu.reading("vram_used_bytes")?.div(1073741824)," GiB")+" / "+metric(gpu.reading("vram_total_bytes")?.div(1073741824)," GiB"))}}}
        "ram"->{val memory=sample?.get("memory") as? JsonObject;Text("RAM: "+metric(memory?.reading("percent",0.0,100.0) ?: if(connection.monitorUnsupported)pc?.ram else null,"%"));if(details)Text("Used: "+metric(memory?.reading("used")?.div(1073741824)," GiB")+" / "+metric(memory?.reading("total")?.div(1073741824)," GiB"))}
        "power"->{val battery=sample?.get("battery") as? JsonObject;Text("Power mode: ${sample?.literal("power_scheme") ?: "Unavailable"}");Text("PC battery: "+metric(battery?.reading("percent",0.0,100.0),"%"));if(details)Text(if(battery==null)"Charging: Unavailable" else if(battery.truth("charging"))"External power connected" else "On battery")}
        "network"->{Text("Companion: ${connection.phase.name}");Text("Latency: ${connection.latencyMs?.let {"$it ms"} ?: "Unavailable"}");if(details){Text(connectionMethod(connection.base));val interfaces=sample?.get("interfaces") as? JsonArray
            if(interfaces.isNullOrEmpty())Text("PC network interfaces: Unavailable")
            interfaces?.mapNotNull {it as? JsonObject}?.forEach {n->Text((n.literal("name") ?: "Interface")+if(n.truth("link_up"))" · link up" else " · state unavailable");Text("↓ "+metric(n.reading("download_bytes_sec")?.div(1024)," KiB/s")+"  ↑ "+metric(n.reading("upload_bytes_sec")?.div(1024)," KiB/s"))}}}
        "actions"->WindowsActions(c,model,connection)
    }
    if(connection.phase!=PcPhase.Connected)Text("Offline · readings unavailable",color=MaterialTheme.colorScheme.error,style=MaterialTheme.typography.bodySmall)
    else if(sample==null && module !in listOf("network","actions"))Text(if(connection.monitorUnsupported)"Basic companion readings only; extended sensors unavailable." else "Waiting for a fresh supported Windows sample.",style=MaterialTheme.typography.bodySmall)
}
@Composable private fun WindowsActions(c: Config,model: LauncherModel,connection: PcConnectionState) {
    val snapshot by model.instant.state.collectAsStateWithLifecycle();val scope=rememberCoroutineScope();var work by remember {mutableStateOf<Job?>(null)};var confirm by remember {mutableStateOf<String?>(null)}
    LifecycleStartEffect(Unit){onStopOrDispose {work?.cancel()}}
    val hotkeys=(connection.catalog?.get("hotkeys") as? JsonArray)?.mapNotNull {it as? JsonObject}?.filter {it.literal("id")?.matches(Regex("[a-z0-9_]{1,64}"))==true} ?: emptyList()
    if(connection.catalog?.truth("supported")!=true || hotkeys.isEmpty())Text("PC system actions: Unavailable on this companion.")
    else hotkeys.forEach {spec->val id=spec.literal("id")!!
        TextButton(onClick={if(id=="lock")confirm=id else if(work?.isActive!=true)work=scope.launch {model.instant.executeWindows(c,id)}},enabled=connection.phase==PcPhase.Connected && !snapshot.busy){Text(spec.literal("name") ?: id)}
    }
    Text(snapshot.status,style=MaterialTheme.typography.bodySmall)
    if(confirm!=null)AlertDialog(onDismissRequest={confirm=null},title={Text("Lock PC?")},text={Text("Unlock using the PC's normal authentication.")},confirmButton={TextButton(onClick={val id=confirm!!;confirm=null;if(work?.isActive!=true)work=scope.launch {model.instant.executeWindows(c,id)}}){Text("Lock PC")}},dismissButton={TextButton(onClick={confirm=null}){Text("Cancel")}})
}
