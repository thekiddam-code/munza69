package com.umbra.mobile

import android.content.Intent
import android.provider.Settings
import androidx.compose.foundation.gestures.detectVerticalDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.input.nestedscroll.*
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.unit.Velocity
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp

fun Modifier.terminalSwipe(enabled: Boolean, down: () -> Unit, up: () -> Unit): Modifier = pointerInput(enabled,down,up) {
    if(enabled) {
        var distance=0f
        detectVerticalDragGestures(onDragStart={distance=0f},onDragCancel={distance=0f},onDragEnd={
            if(distance>24.dp.toPx()) down() else if(distance< -24.dp.toPx()) up()
        }) { change, amount -> change.consume();distance+=amount }
    }
}
@Composable fun rememberPullNavigation(enabled: Boolean,down: ()->Unit,up: ()->Unit): NestedScrollConnection {
    val currentDown by rememberUpdatedState(down)
    val currentUp by rememberUpdatedState(up)
    val threshold=with(LocalDensity.current){48.dp.toPx()}
    return remember(enabled,threshold) { object: NestedScrollConnection {
        var pulled=0f
        var fired=false
        override fun onPostScroll(consumed: Offset,available: Offset,source: NestedScrollSource): Offset {
            if(!enabled || fired || source!=NestedScrollSource.UserInput)return Offset.Zero
            if(consumed.y!=0f || (pulled>0f && available.y<0f) || (pulled<0f && available.y>0f))pulled=0f
            pulled+=available.y
            if(pulled>threshold){fired=true;currentDown()} else if(pulled< -threshold){fired=true;currentUp()}
            return Offset.Zero
        }
        override suspend fun onPostFling(consumed: Velocity,available: Velocity): Velocity { pulled=0f;fired=false;return Velocity.Zero }
    } }
}
@Composable fun TelemetryReadouts(d: Device) {
    val context=LocalContext.current
    fun bytes(value: Long?) = value?.let { android.text.format.Formatter.formatShortFileSize(context,it) } ?: "Unavailable"
    Text("Battery: ${d.battery.takeIf { it>=0 }?.let { "$it%" } ?: "Unavailable"} · ${if(d.charging==true) "Charging" else if(d.charging==false) "Not charging" else "Charging state unavailable"}")
    Text("Network: ${d.network}")
    Text("Power saving: ${if(d.powerSave) "On" else "Off"}")
    Text("Available storage: ${bytes(d.storageAvailable)} / ${bytes(d.storageTotal)}")
    Text("Available system memory: ${bytes(d.memoryAvailable)} / ${bytes(d.memoryTotal)}")
    Text("Uptime at refresh: ${d.uptime/3600000}h ${(d.uptime/60000)%60}m")
    Text("Android thermal status: ${when(d.thermal) { 0->"None";1->"Light";2->"Moderate";3->"Severe";4->"Critical";5->"Emergency";6->"Shutdown";else->"Unavailable" }}",style=MaterialTheme.typography.bodySmall)
}
@Composable fun CommandCenter(c: Config,d: Device,model: LauncherModel,apps: List<LaunchApp>,deck: String,accent: Color,
    open: (Intent)->Unit, launch: (LaunchApp)->Unit, close: ()->Unit, nativeNotifications: ()->Unit,
    icarus: (String)->Unit, dashboard: ()->Unit, refreshDevice: ()->Unit, notificationCount: Int?) {
    val granted=rememberNotificationAccess()
    val editSession=LocalGridEditing.current
    var restore by remember {mutableStateOf(false)}
    val pull=rememberPullNavigation(true,{if(c.secondSwipe)nativeNotifications()},close)
    Column(Modifier.fillMaxSize()) {
        Row(Modifier.fillMaxWidth().heightIn(min=64.dp).testTag("command-swipe-handle").terminalSwipe(true,
            { if(c.secondSwipe) nativeNotifications() },close),verticalAlignment=Alignment.CenterVertically) {
            Column(Modifier.weight(1f)) { Readout("UMBRA / COMMAND CENTER",accent);Text("Swipe up here to close",style=MaterialTheme.typography.bodySmall,color=Muted) }
            TextButton(onClick=close) { Text("Close") }
        }
        Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.End) {
            FilterChip(selected=!c.commandExpanded,onClick={model.change {it.copy(commandExpanded=false)}},label={Text("Compact")},modifier=Modifier.testTag("command-compact"))
            Spacer(Modifier.width(8.dp))
            FilterChip(selected=c.commandExpanded,onClick={model.change {it.copy(commandExpanded=true)}},label={Text("Expanded")},modifier=Modifier.testTag("command-expanded"))
        }
        Column(Modifier.fillMaxWidth().weight(1f).nestedScroll(pull).verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy((6+c.density*3).dp)) {
            ModularDeck("command",c.moduleOrder,c,model,compactMode=!c.commandExpanded,status={if(it=="Device")d.network else if(it=="ICARUS")deck else ""}) {module->
                    when(module) {
                        "Device" -> {
                            TelemetryReadouts(d)
                            Row { TextButton(onClick=refreshDevice){Text("Refresh device")};TextButton(onClick=dashboard){Text("Dashboard")} }
                        }
                        "System" -> {
                            Text("UMBRA window brightness",style=MaterialTheme.typography.bodyMedium)
                            val brightness=if(c.windowBrightness<0) .5f else c.windowBrightness
                            var draft by remember(c.windowBrightness) { mutableFloatStateOf(brightness) }
                            Slider(draft,{draft=it},onValueChangeFinished={model.change { it.copy(windowBrightness=draft) }},valueRange=.1f..1f)
                            Text("${if(c.windowBrightness<0) "System brightness" else "${(c.windowBrightness*100).toInt()}% for UMBRA only"}",style=MaterialTheme.typography.bodySmall)
                            TextButton(onClick={model.change { it.copy(windowBrightness=-1f) }}){Text("Use system brightness")}
                            SystemControlGrid(c,model,listOf("Sound" to Settings.ACTION_SOUND_SETTINGS,"Wi-Fi" to Settings.Panel.ACTION_WIFI,"Bluetooth" to Settings.ACTION_BLUETOOTH_SETTINGS,"Display" to Settings.ACTION_DISPLAY_SETTINGS,"Battery" to Settings.ACTION_BATTERY_SAVER_SETTINGS,"Media app" to "__MEDIA__")) { if(it=="__MEDIA__")open(Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_APP_MUSIC)) else open(Intent(it)) }
                            OutlinedButton(onClick=nativeNotifications,modifier=Modifier.fillMaxWidth(),shape=Chamfer){Text("Android notifications")}
                        }
                        "ICARUS" -> {
                            Text(deck)
                            NamedControlGrid("icarus-shortcuts",c,model,listOf("Engineering" to "Engineering","Lounge" to "Lounge","Simulator" to "Simulator","Open Remote Deck" to "Deck"),icarus)
                        }
                        "Notifications" -> {
                            Text(when { !c.notificationsEnabled->"Notification summary is off."; !granted->"Android notification access is required.";notificationCount==null->"Waiting for the Android notification listener.";else->"$notificationCount active notifications (group summaries excluded)." })
                            Text("Counts only. Notification content is never displayed, saved, or transmitted.",style=MaterialTheme.typography.bodySmall)
                            if(!c.notificationsEnabled || !granted) Button(onClick={model.change { it.copy(notificationsEnabled=true) };open(Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS))},shape=Chamfer){Text("Authorize notification count")}
                            else TextButton(onClick={model.change { it.copy(notificationsEnabled=false) }}){Text("Disable count")}
                            TextButton(onClick={open(Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS))}){Text("Android access settings")}
                        }
                        "Applications" -> {
                            val favorites=orderedFavorites(c,apps)
                            if(favorites.isEmpty()) Text("Long-press applications in Apps to choose favorites.",color=Muted)
                            val columns=when(c.tileSize){1->4;3->2;else->3}
                            GridBoard("command-apps",favorites.map {GridItem(it.id,c.quickLabels[it.id] ?: it.label,height=2)},c,model,columns=columns,onRemove={model.favorite(it)}) {item,_->
                                val app=favorites.first {it.id==item.id}
                                AppTile(app.copy(label=c.quickLabels[app.id] ?: app.label),model,true,{launch(app)},{model.favorite(app.id)},accent,desktopGesture=true)
                            }
                        }
                    }
            }
            TextButton(onClick=nativeNotifications,modifier=Modifier.fillMaxWidth()){Text("Native shade: swipe from the screen's top edge")}
            Spacer(Modifier.height(12.dp))
        }
    }
}
@Composable fun ActionGrid(actions: List<Pair<String,String>>,size: Int, action: (String)->Unit) {
    val columns=if(size==3) 1 else 2
    actions.chunked(columns).forEach { row ->
        Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(8.dp)) {
            row.forEach { (label,value) -> OutlinedButton(onClick={action(value)},shape=Chamfer,modifier=Modifier.weight(1f).heightIn(min=if(size==1) 48.dp else 56.dp)){Text(label)} }
            repeat(columns-row.size){Spacer(Modifier.weight(1f))}
        }
    }
}

@Composable fun SystemControlGrid(c: Config,model: LauncherModel,actions: List<Pair<String,String>>,action: (String)->Unit) {
    GridBoard("system-controls",actions.map {GridItem(it.second,it.first)},c,model,cellHeight=64.dp) {item,_->
        OutlinedButton(onClick={action(item.id)},modifier=Modifier.fillMaxSize(),shape=Chamfer){Text(item.title)}
    }
}

@Composable fun NamedControlGrid(surface: String,c: Config,model: LauncherModel,actions: List<Pair<String,String>>,action: (String)->Unit) {
    GridBoard(surface,actions.map {GridItem(it.second,it.first)},c,model,cellHeight=64.dp) {item,_->OutlinedButton(onClick={action(item.id)},modifier=Modifier.fillMaxSize(),shape=Chamfer){Text(item.title)}}
}
