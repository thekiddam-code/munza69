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

@Composable private fun SoundboardSession(c: Config,model: LauncherModel,pollPlayback: Boolean,content: @Composable (SoundboardState,(suspend ()->Unit)->Unit)->Unit) {
    val saved by model.soundboard.state.collectAsStateWithLifecycle()
    val state=saved.takeIf {it.base==serverBase(c)} ?: SoundboardState()
    val lifecycle=LocalLifecycleOwner.current.lifecycle
    val scope=rememberCoroutineScope()
    var work by remember {mutableStateOf<Job?>(null)}
    LifecycleStartEffect(serverBase(c)) {onStopOrDispose {work?.cancel()}}
    LaunchedEffect(lifecycle,serverBase(c),c.timeout) {
        lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED){model.soundboard.sync(c)}
    }
    val playing=state.playbackKnown && state.catalog?.player?.literal("state") in setOf("starting","playing")
    LaunchedEffect(lifecycle,serverBase(c),c.timeout,pollPlayback,playing) {
        if(pollPlayback && playing)lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED) {
            while(isActive){delay(1000);model.soundboard.sync(c)}
        }
    }
    content(state) {action->
        if(work?.isActive!=true && lifecycle.currentState.isAtLeast(Lifecycle.State.STARTED))work=scope.launch {action()}
    }
}
@Composable private fun SoundboardSyncStatus(state: SoundboardState) {
    val stamp=state.syncedAt?.atZone(ZoneId.systemDefault())?.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))
    Text(if(stamp==null)"Soundboard: no successful catalog synchronization." else "Soundboard: ${state.catalog?.sounds?.size ?: 0} entries loaded · Last successful sync $stamp",style=MaterialTheme.typography.bodySmall)
    state.error?.let {Text(it,color=androidx.compose.ui.graphics.Color(0xFFD27970),modifier=Modifier.semantics {liveRegion=LiveRegionMode.Polite})}
    if(state.busy)Text("Synchronizing / sending request…",style=MaterialTheme.typography.bodySmall)
}
@OptIn(ExperimentalFoundationApi::class)
@Composable fun SoundboardScreen(c: Config,model: LauncherModel) {
    var manage by remember {mutableStateOf(false)}
    var favoritesOnly by rememberSaveable {mutableStateOf(false)}
    var configured by remember {mutableStateOf<String?>(null)}
    SoundboardSession(c,model,true) {state,run->
        val catalog=state.catalog
        Column(verticalArrangement=Arrangement.spacedBy(8.dp)) {
            Box(Modifier.fillMaxWidth().heightIn(min=48.dp).combinedClickable(onClick={},onLongClick={manage=true}).testTag("soundboard-header")) {Readout("ICARUS / SOUNDBOARD",Amber)}
            SoundboardSyncStatus(state)
            Row {
                TextButton(onClick={run {model.soundboard.sync(c)}},enabled=!state.busy){Text("Sync sounds")}
                TextButton(onClick={run {model.soundboard.stop(c)}},enabled=catalog!=null && !state.busy){Text("Stop playback")}
            }
            val player=catalog?.player
            Text(if(!state.playbackKnown)"Playback status unknown; refresh to verify." else "Server playback: ${player?.literal("state") ?: "unknown"}${player?.literal("id")?.let {id->catalog.sounds.firstOrNull {it.id==id}?.let {" · ${it.name}"}} ?: ""}",modifier=Modifier.semantics {liveRegion=LiveRegionMode.Polite})
            if(player?.literal("state")=="error")Text("Server playback failed. Check the configured output device.",color=androidx.compose.ui.graphics.Color(0xFFD27970))
            FilterChip(selected=favoritesOnly,onClick={favoritesOnly=!favoritesOnly},label={Text("Favorites only")})
            val sounds=catalog?.sounds?.filter {!favoritesOnly || it.favorite} ?: emptyList()
            if(catalog!=null && sounds.isEmpty())Text(if(favoritesOnly)"No favorite sounds. Long-press a sound to favorite it." else "The server library is empty. Add sounds in the existing ICARUS Remote Deck.")
            Column(Modifier.heightIn(max=560.dp).fillMaxWidth().verticalScroll(rememberScrollState())) {
                GridBoard("soundboard",sounds.map {GridItem(it.id,it.name)},c,model,columns=2,cellHeight=76.dp,onConfigure={configured=it}) {item,_->
                    val sound=sounds.first {it.id==item.id}
                    OutlinedButton(onClick={run {model.soundboard.play(c,sound.id)}},enabled=!state.busy,shape=Chamfer,modifier=Modifier.fillMaxSize().testTag("sound-${sound.id}")) {
                        Text((if(sound.favorite)"★ " else "")+sound.name,maxLines=3)
                    }
                }
            }
            Text("Tap to play on the saved ICARUS output. Long-press to move, resize, or favorite. Audio Output is in Settings → ICARUS → Soundboard.",style=MaterialTheme.typography.bodySmall)
        }
        if(manage)AlertDialog(onDismissRequest={manage=false},title={Text("Soundboard layout")},text={Text("Restore buttons hidden on this phone without changing ICARUS, existing positions, or sizes.")},confirmButton={TextButton(onClick={model.restoreGridItems("soundboard");manage=false}){Text("Restore hidden sounds")}},dismissButton={TextButton(onClick={manage=false}){Text("Close")}})
        configured?.let {id->catalog?.sounds?.firstOrNull {it.id==id}?.let {sound->
            AlertDialog(onDismissRequest={configured=null},title={Text(sound.name)},text={Text("Favorites are saved in ICARUS and shared with Remote Deck. Grid positions and button sizes remain local to UMBRA.")},confirmButton={TextButton(onClick={configured=null;run {model.soundboard.favorite(c,id)}},enabled=!state.busy){Text(if(sound.favorite)"Remove favorite" else "Favorite")}},dismissButton={TextButton(onClick={configured=null}){Text("Close")}})
        }}
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
