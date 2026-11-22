package com.umbra.mobile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.*
import androidx.lifecycle.repeatOnLifecycle
import kotlinx.coroutines.*
import kotlinx.serialization.json.*
import java.time.ZoneId
import java.time.format.DateTimeFormatter

@Composable private fun SoundboardSession(c: Config,model: LauncherModel,pollPlayback: Boolean,visible: Boolean=true,content: @Composable (SoundboardState,(suspend ()->Unit)->Unit)->Unit) {
    val saved by model.soundboard.state.collectAsStateWithLifecycle()
    val state=saved.takeIf {it.base==serverBase(c)} ?: SoundboardState()
    val lifecycle=LocalLifecycleOwner.current.lifecycle
    val scope=rememberCoroutineScope()
    var work by remember {mutableStateOf<Job?>(null)}
    LifecycleStartEffect(serverBase(c),visible) {onStopOrDispose {work?.cancel()}}
    LaunchedEffect(lifecycle,serverBase(c),c.timeout,visible) {
        if(visible)lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED){model.soundboard.sync(c)}
    }
    val playing=state.playbackKnown && state.catalog?.player?.literal("state") in setOf("starting","playing")
    LaunchedEffect(lifecycle,serverBase(c),c.timeout,pollPlayback,playing,visible) {
        if(visible && pollPlayback && playing)lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED) {
            while(isActive){delay(1000);model.soundboard.sync(c)}
        }
    }
    content(state) {action->
        if(visible && work?.isActive!=true && lifecycle.currentState.isAtLeast(Lifecycle.State.STARTED))work=scope.launch {action()}
    }
}
@Composable private fun SoundboardSyncStatus(state: SoundboardState) {
    val stamp=state.syncedAt?.atZone(ZoneId.systemDefault())?.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))
    Text(if(stamp==null)"Soundboard: no successful catalog synchronization." else "Soundboard: ${state.catalog?.sounds?.size ?: 0} entries loaded · Last successful sync $stamp",style=MaterialTheme.typography.bodySmall)
    state.error?.let {Text(it,color=androidx.compose.ui.graphics.Color(0xFFD27970),modifier=Modifier.semantics {liveRegion=LiveRegionMode.Polite})}
    if(state.busy)Text("Synchronizing / sending request…",style=MaterialTheme.typography.bodySmall)
}
@OptIn(ExperimentalFoundationApi::class)
@Composable fun SoundboardScreen(c: Config,model: LauncherModel,widgetId: String?=null,compact: Boolean=false,visible: Boolean=true,headingModifier: Modifier=Modifier) {
    var manage by remember {mutableStateOf(false)};var favoritesOnly by rememberSaveable {mutableStateOf(false)};var configured by remember {mutableStateOf<String?>(null)}
    val spec=widgetId?.let {widgetSpec(c,it)};val surface=widgetId?.let {"sound-widget:$it"} ?: "soundboard"
    SoundboardSession(c,model,true,visible) {state,run->
        val catalog=state.catalog
        Column(if(compact)Modifier.fillMaxSize() else Modifier.fillMaxWidth(),verticalArrangement=Arrangement.spacedBy(4.dp)) {
            Row(Modifier.fillMaxWidth()) {
                Box(Modifier.weight(1f).heightIn(min=48.dp).then(headingModifier).then(if(widgetId==null)Modifier.combinedClickable(onClick={},onLongClick={manage=true}) else Modifier).testTag("soundboard-header")) {
                    Text(spec?.title?.takeIf {it.isNotBlank()} ?: "Soundboard",color=MaterialTheme.colorScheme.primary,style=MaterialTheme.typography.titleMedium)
                }
                TextButton(onClick={run {model.soundboard.sync(c)}},enabled=!state.busy){Text("Sync")}
                TextButton(onClick={run {model.soundboard.stop(c)}},enabled=catalog!=null && !state.busy){Text("Stop")}
            }
            if(!compact)SoundboardSyncStatus(state) else {
                Text("${catalog?.sounds?.size ?: 0} sounds · "+(if(state.playbackKnown)catalog?.player?.literal("state") ?: "unknown" else "status unknown"),style=MaterialTheme.typography.labelSmall)
                state.error?.let {Text(it,color=MaterialTheme.colorScheme.error,style=MaterialTheme.typography.labelSmall,modifier=Modifier.semantics {liveRegion=LiveRegionMode.Polite})}
            }
            if(!compact) {
                Text(if(!state.playbackKnown)"Playback status unknown; refresh to verify." else "Server playback: ${catalog?.player?.literal("state") ?: "unknown"}",modifier=Modifier.semantics {liveRegion=LiveRegionMode.Polite})
                FilterChip(selected=favoritesOnly,onClick={favoritesOnly=!favoritesOnly},label={Text("Favorites only")})
            }
            if(catalog?.player?.literal("state")=="error")Text("Server playback failed. Check Audio Output.",color=MaterialTheme.colorScheme.error)
            val selected=widgetId?.let {c.widgetButtonSelections[it]?.toSet()}
            val sounds=catalog?.sounds?.filter {(selected==null || "sound:${it.id}" in selected) && (!(favoritesOnly || spec?.buttonSet=="favorites") || it.favorite)} ?: emptyList()
            if(catalog!=null && sounds.isEmpty())Text("No selected sounds. Configure this widget or add sounds on the PC.",style=MaterialTheme.typography.bodySmall)
            Column((if(compact)Modifier.weight(1f) else Modifier.heightIn(max=560.dp)).fillMaxWidth().verticalScroll(rememberScrollState())) {
                GridBoard(surface,sounds.map {GridItem(it.id,it.name)},c,model,columns=spec?.buttonColumns ?: 2,cellHeight=(spec?.buttonHeight ?: 76).dp,onConfigure={configured=it}) {item,_->
                    val sound=sounds.first {it.id==item.id}
                    OutlinedButton(onClick={run {model.soundboard.play(c,sound.id)}},enabled=!state.busy,shape=Chamfer,contentPadding=PaddingValues(horizontal=4.dp,vertical=4.dp),modifier=Modifier.fillMaxSize().testTag("sound-${sound.id}")) {Text((if(sound.favorite)"★ " else "")+sound.name,maxLines=3)}
                }
            }
            if(!compact)Text("Tap to play on the saved ICARUS output. Long-press to move, resize, or favorite. Audio Output is in Settings → ICARUS → Soundboard.",style=MaterialTheme.typography.bodySmall)
        }
        if(manage)AlertDialog(onDismissRequest={manage=false},title={Text("Soundboard layout")},text={Text("Restore hidden buttons without changing ICARUS output or sound mappings.")},confirmButton={TextButton(onClick={model.restoreGridItems(surface);manage=false}){Text("Restore hidden sounds")}},dismissButton={TextButton(onClick={manage=false}){Text("Close")}})
        configured?.let {id->catalog?.sounds?.firstOrNull {it.id==id}?.let {sound->AlertDialog(onDismissRequest={configured=null},title={Text(sound.name)},text={Text("Favorites are shared with ICARUS. This widget's selection and grid are independent.")},confirmButton={TextButton(onClick={configured=null;run {model.soundboard.favorite(c,id)}},enabled=!state.busy){Text(if(sound.favorite)"Remove favorite" else "Favorite")}},dismissButton={TextButton(onClick={configured=null}){Text("Close")}})}}
    }
}
@Composable fun SoundSelection(c: Config,model: LauncherModel,widgetId: String,draft: Set<String>?,set: (Set<String>)->Unit) {
    val saved by model.soundboard.state.collectAsStateWithLifecycle();val scope=rememberCoroutineScope()
    val state=saved.takeIf {it.base==serverBase(c)}
    val sounds=state?.catalog?.sounds ?: emptyList();val selected=draft ?: sounds.map {"sound:${it.id}"}.toSet()
    var query by remember {mutableStateOf("")};var job by remember {mutableStateOf<Job?>(null)}
    LifecycleStartEffect(widgetId){onStopOrDispose {job?.cancel()}}
    TextButton(onClick={if(job?.isActive!=true)job=scope.launch {model.soundboard.sync(c)}}){Text("Sync available sounds")}
    state?.error?.let {Text(it,color=MaterialTheme.colorScheme.error)}
    OutlinedTextField(query,{query=it},label={Text("Search sounds")},singleLine=true)
    Row {TextButton(onClick={set(sounds.map {"sound:${it.id}"}.toSet())}){Text("Select all")};TextButton(onClick={set(emptySet())}){Text("Deselect all")}}
    androidx.compose.foundation.lazy.LazyColumn(Modifier.fillMaxWidth().heightIn(max=320.dp)) {
        items(sounds.size,key={sounds[it].id}) {i->val sound=sounds[i];if(sound.name.contains(query,true))Row {Checkbox("sound:${sound.id}" in selected,{checked->set(if(checked)selected+"sound:${sound.id}" else selected-"sound:${sound.id}")});Text(sound.name)}}
    }
}
@Composable fun SoundboardOutputSettings(c: Config,model: LauncherModel) {
    SoundboardSession(c,model,false) {state,run->
        Text("ICARUS → Soundboard → Audio Output",style=MaterialTheme.typography.titleMedium)
        SoundboardSyncStatus(state)
        TextButton(onClick={run {model.soundboard.sync(c)}},enabled=!state.busy){Text("Refresh server audio settings")}
        state.catalog?.let {catalog->
            Text("Saved playback device: ${catalog.output?.literal("name") ?: "Not configured"}")
            if(catalog.deviceError)Text("ICARUS could not enumerate playback devices. Retry on the server.",color=androidx.compose.ui.graphics.Color(0xFFD27970))
            if(catalog.output!=null && catalog.output !in catalog.devices)Text("The saved output is unavailable. Select its current identity below. No fallback output is selected automatically.",color=androidx.compose.ui.graphics.Color(0xFFD27970))
            catalog.devices.forEach {device->
                TextButton(onClick={run {model.soundboard.output(c,device)}},enabled=!state.busy && device!=catalog.output,modifier=Modifier.fillMaxWidth()) {
                    Text((if(device==catalog.output)"Selected: " else "Use: ")+device.literal("name")+" [${device.number("id")?.toInt()}]")
                }
            }
            if(catalog.devices.isEmpty())Text("No render devices reported by ICARUS.")
            Text("Saved on ICARUS and shared with Remote Deck. The selection persists across phone restarts. Selecting an output stops current server playback.",style=MaterialTheme.typography.bodySmall)
            // 4.8C advertises its real normalization profile; 4.8B has no such controls.
            val profile=catalog.profile
            if(profile!=null && !profile.truth("invalid") && listOf("offset_db","ceiling_dbfs","max_boost_db").all {profile.number(it)!=null}) {
                ServerNormalization(profile,state.busy) {fields->run {model.soundboard.profile(c,fields)}}
            }
        }
    }
}
@Composable private fun ServerNormalization(profile: JsonObject,busy: Boolean,save: (JsonObject)->Unit) {
    var enabled by remember(profile){mutableStateOf(profile.truth("enabled"))}
    var offset by remember(profile){mutableFloatStateOf(profile.number("offset_db")!!.toFloat())}
    var ceiling by remember(profile){mutableFloatStateOf(profile.number("ceiling_dbfs")!!.toFloat())}
    var boost by remember(profile){mutableFloatStateOf(profile.number("max_boost_db")!!.toFloat())}
    val calibrated=profile["speech"] is JsonObject
    Text("Server clip normalization",style=MaterialTheme.typography.titleMedium)
    Row {Checkbox(checked=enabled,onCheckedChange={enabled=it},enabled=!busy && calibrated);Text("Use existing server speech calibration")}
    if(!calibrated)Text("Calibrate on the existing Remote Deck before enabling normalization.",style=MaterialTheme.typography.bodySmall)
    Text("Speech offset: ${offset.toInt()} dB");Slider(offset,{offset=it},valueRange=-12f..0f,steps=11,enabled=!busy)
    Text("Peak ceiling: ${ceiling.toInt()} dBFS");Slider(ceiling,{ceiling=it},valueRange=-12f..-1f,steps=10,enabled=!busy)
    Text("Maximum boost: ${boost.toInt()} dB");Slider(boost,{boost=it},valueRange=0f..6f,steps=5,enabled=!busy)
    TextButton(onClick={save(buildJsonObject {put("enabled",enabled);put("offset_db",offset.toInt());put("ceiling_dbfs",ceiling.toInt());put("max_boost_db",boost.toInt())})},enabled=!busy){Text("Save server normalization")}
}
