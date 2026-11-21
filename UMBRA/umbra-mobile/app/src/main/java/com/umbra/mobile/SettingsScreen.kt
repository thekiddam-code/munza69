package com.umbra.mobile

import android.content.Intent
import android.provider.Settings
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.*
import java.io.ByteArrayOutputStream
import java.io.IOException

@OptIn(ExperimentalLayoutApi::class)
@Composable fun Configuration(c: Config,model: LauncherModel,accent: Color,homeSettings: ()->Unit,apps: List<LaunchApp> = emptyList(),open: (Intent)->Unit = {},initialCategory: String = "Animation") {
    val context=LocalContext.current
    val scope=rememberCoroutineScope()
    val installedVersion=remember {runCatching {context.packageManager.getPackageInfo(context.packageName,0).let {"${it.versionName} (${it.longVersionCode})"}}.getOrDefault("Version unavailable")}
    val buildLabel=if(context.applicationInfo.flags and android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE!=0)"debug" else "release"
    var category by rememberSaveable(initialCategory) { mutableStateOf(initialCategory) }
    var notice by remember { mutableStateOf("") }
    var pendingImport by remember { mutableStateOf<Config?>(null) }
    var resetAll by remember { mutableStateOf(false) }
    var exported by remember { mutableStateOf(c) }
    var labelApp by remember { mutableStateOf<LaunchApp?>(null) }
    var label by remember { mutableStateOf("") }
    val export=rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument("application/json")) { uri ->
        if(uri!=null) scope.launch {
            try { withContext(Dispatchers.IO) { context.contentResolver.openOutputStream(uri,"wt")?.use { it.write(exportConfig(exported).toByteArray()) } ?: throw IOException() };notice="Configuration exported. Pairing credentials are excluded." }
            catch(e: CancellationException){throw e} catch(_:Exception){notice="Could not export configuration."}
        }
    }
    val importLauncher=rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()) { uri ->
        if(uri!=null) scope.launch {
            try {
                pendingImport=withContext(Dispatchers.IO) {
                    val bytes=context.contentResolver.openInputStream(uri)?.use { input ->
                        val out=ByteArrayOutputStream();val buffer=ByteArray(4096)
                        while(true){val n=input.read(buffer);if(n<0)break;require(out.size()+n<=MAX_CONFIG_BYTES);out.write(buffer,0,n)}
                        out.toByteArray()
                    } ?: throw IOException()
                    importConfig(bytes.decodeToString(throwOnInvalidSequence=true))
                }
            } catch(e: CancellationException){throw e} catch(_:Exception){notice="Import rejected. Use a valid schema 2, 3, or 4 UMBRA configuration under 1 MiB. Existing settings were preserved."}
        }
    }
    val wallpaperExport=rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument("image/png")) { uri ->
        if(uri!=null) scope.launch {
            try { withContext(Dispatchers.IO){context.contentResolver.openOutputStream(uri,"wt")?.use { exportWallpaper(exported,it) } ?: throw IOException()};notice="Wallpaper exported. Apply it through Samsung Wallpaper and style." }
            catch(e: CancellationException){throw e} catch(_:Exception){notice="Could not export the wallpaper."}
        }
    }
    if(pendingImport!=null) AlertDialog(onDismissRequest={pendingImport=null},title={Text("Import validated settings?")},text={Text("This replaces appearance, animation, display, layout, connection preferences, and favorites. Native pairing credentials are never imported. Android widgets require rebinding after import. Weather location in the file is used with Open-Meteo when its widget is visible.\n${pendingImport!!.favorites.size} favorites · ${pendingImport!!.profile} · ${pendingImport!!.intensity}% intensity")},
        confirmButton={TextButton(onClick={model.replace(pendingImport!!);pendingImport=null;notice="Import submitted. Check any save error above."}){Text("Apply settings")}},dismissButton={TextButton(onClick={pendingImport=null}){Text("Cancel")}})
    if(resetAll) AlertDialog(onDismissRequest={resetAll=false},title={Text("Restore all UMBRA defaults?")},text={Text("This clears favorites and local native pairing, and restores UMBRA settings. It does not modify Android or the ICARUS server.")},
        confirmButton={TextButton(onClick={model.reset();resetAll=false;notice="Defaults submitted. Android notification access can be revoked separately in system settings."}){Text("Restore defaults")}},dismissButton={TextButton(onClick={resetAll=false}){Text("Cancel")}})
    if(labelApp!=null) AlertDialog(onDismissRequest={labelApp=null},title={Text("Quick tile label")},text={OutlinedTextField(label,{label=it.take(48)},singleLine=true,label={Text("Label (1–48 characters)")})},
        confirmButton={TextButton(onClick={val id=labelApp!!.id;model.change { it.copy(quickLabels=it.quickLabels+(id to label.trim())) };labelApp=null},enabled=label.isNotBlank() && label.none { it.isISOControl() }){Text("Save label")}},dismissButton={TextButton(onClick={labelApp=null}){Text("Cancel")}})
    Column(Modifier.fillMaxSize()) {
        // Compact Settings title is provided by the activity header.
        Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState())) {
            listOf("Appearance","Animation","Display","Command Center","ICARUS","Organization","Weather","Configuration","Lock screen").forEach { item -> TextButton(onClick={category=item}){Text(item,color=if(category==item)accent else Muted)} }
        }
        if(notice.isNotEmpty()) Text(notice,color=accent,style=MaterialTheme.typography.bodySmall,modifier=Modifier.semantics { liveRegion=LiveRegionMode.Polite })
        Column(Modifier.weight(1f).fillMaxWidth().verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(12.dp)) {
            Text(category,style=MaterialTheme.typography.titleLarge)
            when(category) {
                "Appearance" -> {
                    Choice("Visual Detail",VisualDetail.entries.map {it.name},c.visualDetail.name){detail->model.change {it.copy(visualDetail=VisualDetail.valueOf(detail))}}
                    Text("Enhanced is the default. Visual Detail controls cached static structure and panel detail; changing it never enables animations. Master off and Minimal motion do not reduce visual detail.",style=MaterialTheme.typography.bodySmall)
                    Toggle("Show app labels",c.showAppLabels){v->model.change {it.copy(showAppLabels=v)}}
                    Choice("Application icon size",listOf("32","40","48","56","64","72"),c.iconSize.toString()){v->model.change {it.copy(iconSize=v.toInt())}}
                    TransitionSettings(c,model)
                    var hex by remember(c.accent) { mutableStateOf(c.accent) }
                    OutlinedTextField(hex,{hex=it.take(7)},label={Text("Custom accent #RRGGBB")},singleLine=true,isError=!validAccent(hex),supportingText={Text("Bright, high-contrast colors only. Empty uses the selected preset.")},modifier=Modifier.fillMaxWidth())
                    Button(onClick={model.change { it.copy(accent=hex) }},enabled=validAccent(hex),shape=Chamfer){Text("Save accent")}
                    Row { TextButton(onClick={model.change { it.copy(accent="",greenAccent=false) }}){Text("Amber preset")};TextButton(onClick={model.change { it.copy(accent="",greenAccent=true) }}){Text("Muted green preset")} }
                    Choice("Background",listOf("Void","Graphite","Blueprint"),c.background){v->model.change { it.copy(background=v) }}
                    Choice("Typography",listOf("Technical","Mono","System"),c.typography){v->model.change { it.copy(typography=v) }}
                    Choice("Panel density",listOf("Compact","Balanced","Spacious"),listOf("Compact","Balanced","Spacious")[c.density-1]){v->model.change { it.copy(density=listOf("Compact","Balanced","Spacious").indexOf(v)+1) }}
                    Choice("Application columns",listOf("3","4","5"),c.gridColumns.toString()){v->model.change { it.copy(gridColumns=v.toInt()) }}
                }
                "Animation" -> {
                    Choice("Performance profile",Profile.entries.map { it.name },c.profile.name){model.profile(Profile.valueOf(it))}
                    Text("Adaptive reduces effects during interaction. All profiles respect Android reduced motion, battery saver, low battery, thermal restrictions, and screen power.",style=MaterialTheme.typography.bodySmall)
                    Toggle("Master animations",c.master){model.change { old->old.copy(master=it) }}
                    Text("Individual selections remain saved while master is off. Zero intensity disables all optional motion.",style=MaterialTheme.typography.bodySmall)
                    Intensity(c.intensity){v->model.change { it.copy(intensity=v) }}
                    Toggle("Ambient lighting",c.ambient){model.flag("ambient",it)}
                    Toggle("Animated backgrounds",c.wallpaper){model.flag("wallpaper",it)}
                    Toggle("Terminal transitions",c.transitions){model.flag("transitions",it)}
                    Toggle("Startup animation",c.startup){v->model.change { it.copy(startup=v) }}
                    Toggle("Parallax",c.parallax){v->model.change { it.copy(parallax=v) }}
                    Toggle("Status indicator effects",c.statusEffects){v->model.change { it.copy(statusEffects=v) }}
                    Toggle("Environmental effects",c.environment){model.flag("environment",it)}
                    Toggle("ICARUS alert animations",c.alerts){model.flag("alerts",it)}
                    Toggle("Command Center animations",c.commandAnimations){v->model.change { it.copy(commandAnimations=v) }}
                }
                "Display" -> {
                    Toggle("Enable Immersive Fullscreen",c.immersive){v->model.change { it.copy(immersive=v) }}
                    Toggle("Hide Top Status Bar",c.hideTopBar){v->model.change { it.copy(hideTopBar=v) }}
                    Toggle("Hide Bottom Navigation Bar",c.hideBottomBar){v->model.change { it.copy(hideBottomBar=v) }}
                    Toggle("Show UMBRA Status Panel",c.statusPanel){model.flag("statusPanel",it)}
                    Text("Status Panel · per tab",style=MaterialTheme.typography.titleMedium)
                    STATUS_TABS.forEach {tab->Toggle("Status Panel on $tab",c.statusTabs[tab] ?: DEFAULT_STATUS_TABS.getValue(tab)){value->model.change {it.copy(statusTabs=it.statusTabs+(tab to value))}}}
                    Button(onClick={model.change { it.copy(immersive=false,hideTopBar=false,hideBottomBar=false) }},shape=Chamfer,modifier=Modifier.fillMaxWidth()){Text("Restore Standard Android Bars")}
                    Text("Android bars is always accessible in the header. System gestures can reveal transient bars. Samsung/Android may keep protected system UI visible for HOME, keyboard, calls, accessibility, or security.",style=MaterialTheme.typography.bodySmall)
                    Text("Status panel indicators",style=MaterialTheme.typography.titleMedium)
                    INDICATORS.forEach { name -> Toggle("Show $name",name in c.indicators){show->model.change { it.copy(indicators=if(show)it.indicators+name else it.indicators-name) }} }
                    Toggle("Enable notification count",c.notificationsEnabled){v->model.change { it.copy(notificationsEnabled=v) }}
                    TextButton(onClick={open(Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS))}){Text("Authorize or revoke Android notification access")}
                    Button(onClick=homeSettings,shape=Chamfer){Text("Choose default Home application")}
                }
                "Command Center" -> {
                    Toggle("Swipe down opens Command Center",c.swipeDown){v->model.change { it.copy(swipeDown=v) }}
                    Toggle("Second swipe offers native notifications",c.secondSwipe){v->model.change { it.copy(secondSwipe=v) }}
                    Toggle("Command Center animations",c.commandAnimations){v->model.change { it.copy(commandAnimations=v) }}
                    Choice("Tile size",listOf("Small","Standard","Large"),listOf("Small","Standard","Large")[c.tileSize-1]){v->model.change { it.copy(tileSize=listOf("Small","Standard","Large").indexOf(v)+1) }}
                    Toggle("Editing haptics",c.editHaptics){value->model.change {it.copy(editHaptics=value)}}
                    Choice("Deck grid density",listOf("2","3","4"),c.deckColumns.toString()){value->model.arrange {it.copy(deckColumns=value.toInt())}}
                    TextButton(onClick={model.arrange {it.copy(gridLayouts=it.gridLayouts.mapValues {(_,grid)->grid.copy(cells=grid.cells.map {cell->cell.copy(hidden=false)})},hiddenModules=emptySet())}}){Text("Restore all hidden modules and controls")}
                    Text("Module arrangement",style=MaterialTheme.typography.titleMedium)
                    Text("Long-press deck headers to move, resize, hide, or collapse them. TalkBack also exposes Move earlier / Move later without visible arrangement buttons.",style=MaterialTheme.typography.bodySmall)
                    c.moduleOrder.forEach {name->
                        val hidden=name in c.hiddenModules || c.gridLayouts["command"]?.cells?.firstOrNull {it.id==name}?.hidden==true
                        Toggle("Show $name module",!hidden){show->model.arrange {old->
                            val grid=old.gridLayouts["command"]
                            old.copy(hiddenModules=if(show)old.hiddenModules-name else old.hiddenModules+name,gridLayouts=if(grid==null)old.gridLayouts else old.gridLayouts+("command" to grid.copy(cells=grid.cells.map {if(it.id==name)it.copy(hidden=!show) else it})))
                        }}
                    }
                    Text("Quick applications",style=MaterialTheme.typography.titleMedium)
                    Text("Long-press apps in the drawer to select favorites. Drag shortcuts directly to arrange them; labels also apply on Home.",style=MaterialTheme.typography.bodySmall)
                    val favorites=orderedFavorites(c,apps)
                    favorites.forEachIndexed { i,app ->
                        Frame(accent.copy(alpha=.4f)) {
                            Text(c.quickLabels[app.id] ?: app.label)
                            Row {
                                TextButton(onClick={model.change { old->old.copy(quickOrder=moveItem(orderedFavorites(old,apps).map { it.id },app.id,-1)) }},enabled=i>0){Text("Up")}
                                TextButton(onClick={model.change { old->old.copy(quickOrder=moveItem(orderedFavorites(old,apps).map { it.id },app.id,1)) }},enabled=i<favorites.lastIndex){Text("Down")}
                                TextButton(onClick={labelApp=app;label=c.quickLabels[app.id] ?: app.label}){Text("Edit label")}
                            }
                        }
                    }
                    Button(onClick={model.change { resetCategory(it,"Command Center") }},shape=Chamfer){Text("Reset layout to defaults")}
                }
                "ICARUS" -> {
                    ConnectionFields(c,model)
                    Toggle("Check status on resume",c.refreshOnResume){v->model.change { it.copy(refreshOnResume=v) }}
                    Toggle("Check status on network change",c.refreshOnNetwork){v->model.change { it.copy(refreshOnNetwork=v) }}
                    val refreshOptions=(listOf(0,30,60,300)+c.foregroundRefreshSeconds).distinct().sorted()
                    Choice("Foreground native ICARUS refresh",refreshOptions.map { if(it==0) "Manual" else "$it seconds" },if(c.foregroundRefreshSeconds==0) "Manual" else "${c.foregroundRefreshSeconds} seconds"){v->model.change { it.copy(foregroundRefreshSeconds=v.substringBefore(' ').toIntOrNull() ?: 0) }}
                    Text("Automatic intervals apply only while the ICARUS screen is visible and battery saver is off. All requests cancel when hidden. Pairing tokens stay encrypted on this phone and are bound to the exact server base. Configure Tailscale separately.",style=MaterialTheme.typography.bodySmall)
                    TextButton(onClick={scope.launch { model.vault.clear();notice="Local native pairing removed. Browser pairing is separate." }}){Text("Clear local native pairing")}
                }
                "Organization" -> OrganizationSettings(c,model,apps)
                "Weather" -> WeatherSettings(c,model)
                "Configuration" -> {
                    Button(onClick={exported=c;export.launch("umbra-settings-v2.json")},shape=Chamfer,modifier=Modifier.fillMaxWidth()){Text("Export settings")}
                    OutlinedButton(onClick={importLauncher.launch(arrayOf("application/json","text/plain","application/octet-stream"))},shape=Chamfer,modifier=Modifier.fillMaxWidth()){Text("Import settings")}
                    Text("Schema version 3 (schema 2 accepted). Imports are validated before atomic replacement. Maximum 256 KiB. Exports contain preferences and configured URLs, but no PIN, pairing token, notification content, or device telemetry.",style=MaterialTheme.typography.bodySmall)
                    Button(onClick={resetAll=true},shape=Chamfer){Text("Restore all defaults")}
                    Text("To restore Samsung: Settings → Apps → Choose default apps → Home app → One UI Home.",style=MaterialTheme.typography.bodyMedium)
                    Button(onClick=homeSettings,shape=Chamfer){Text("Open Android Home settings")}
                }
                "Lock screen" -> {
                    Text("Coordinated static UMBRA lock wallpaper. Android's secure keyguard, fingerprint authentication, and native clock remain in control.")
                    Button(onClick={exported=c;wallpaperExport.launch("umbra-lock-screen.png")},shape=Chamfer,modifier=Modifier.fillMaxWidth()){Text("Export lock-screen wallpaper")}
                    OutlinedButton(onClick={scope.launch {
                        try { withContext(Dispatchers.IO){applyLockWallpaper(context,c)};notice="UMBRA lock-screen wallpaper applied." }
                        catch(e:CancellationException){throw e} catch(_:Exception){notice="Android restricted direct wallpaper changes. Export the image and apply it manually in Samsung Wallpaper and style."}
                    }},shape=Chamfer,modifier=Modifier.fillMaxWidth()){Text("Apply lock-screen wallpaper")}
                    Text("Samsung setup: Settings → Wallpaper and style → Lock screen. Use the exported image, then edit the native clock and choose an amber or muted-green color. Optional Good Lock LockStar / ClockFace modules offer additional layouts where available. No unlock interface or ambient service is installed.",style=MaterialTheme.typography.bodySmall)
                    TextButton(onClick={open(Intent(Intent.ACTION_SET_WALLPAPER))}){Text("Android wallpaper chooser")}
                }
            }
            if(category in listOf("Appearance","Animation","Display","Command Center","ICARUS")) TextButton(onClick={model.change { resetCategory(it,category) };notice="$category reset submitted."}){Text("Reset $category")}
            HorizontalDivider()
            Row(verticalAlignment=Alignment.CenterVertically) {
                Icon(androidx.compose.ui.res.painterResource(R.drawable.ic_umbra),contentDescription="UMBRA logo",tint=accent,modifier=Modifier.size(20.dp))
                Text("◆ UMBRA · $installedVersion · $buildLabel · native Android launcher",style=MaterialTheme.typography.bodySmall,color=Muted)
            }
        }
    }
}
@Composable private fun ConnectionFields(c: Config,model: LauncherModel) {
    var deck by rememberSaveable(c.url) { mutableStateOf(c.url) }
    var server by rememberSaveable(c.serverUrl) { mutableStateOf(c.serverUrl) }
    var engineering by rememberSaveable(c.engineeringUrl) { mutableStateOf(c.engineeringUrl) }
    var lounge by rememberSaveable(c.loungeUrl) { mutableStateOf(c.loungeUrl) }
    var simulator by rememberSaveable(c.simulatorUrl) { mutableStateOf(c.simulatorUrl) }
    var timeout by rememberSaveable(c.timeout) { mutableStateOf(c.timeout.toString()) }
    fun valid(value: String)=value.isEmpty() || validDeckUrl(value)
    val fields=listOf(Triple("Remote Deck URL",deck,{v:String->deck=v}),Triple("Server base URL (optional)",server,{v:String->server=v}),Triple("Engineering browser URL (optional)",engineering,{v:String->engineering=v}),Triple("Lounge browser URL (optional)",lounge,{v:String->lounge=v}),Triple("Simulator browser URL (optional)",simulator,{v:String->simulator=v}))
    fields.forEach { (name,value,change) -> OutlinedTextField(value,change,label={Text(name)},singleLine=true,isError=!valid(value),keyboardOptions=KeyboardOptions(keyboardType=KeyboardType.Uri),modifier=Modifier.fillMaxWidth()) }
    OutlinedTextField(timeout,{timeout=it.take(2)},label={Text("Connection timeout (1–30 seconds)")},singleLine=true,isError=timeout.toIntOrNull() !in 1..30,keyboardOptions=KeyboardOptions(keyboardType=KeyboardType.Number),modifier=Modifier.fillMaxWidth())
    Button(onClick={model.change { it.copy(url=deck,serverUrl=server,engineeringUrl=engineering,loungeUrl=lounge,simulatorUrl=simulator,timeout=timeout.toInt()) }},enabled=fields.all { valid(it.second) } && timeout.toIntOrNull() in 1..30,shape=Chamfer){Text("Save connection")}
    Text("HTTP(S) only, without embedded credentials, query, or fragment. Empty server base uses the Remote Deck origin. Optional module browser URLs fall back to Remote Deck; the inspected web UI has no supported section deep-link contract. Prefer HTTPS over Tailscale.",style=MaterialTheme.typography.bodySmall)
}
@Composable fun Toggle(label: String,value: Boolean,change: (Boolean)->Unit) {
    Row(Modifier.fillMaxWidth().heightIn(min=56.dp),verticalAlignment=Alignment.CenterVertically) {
        Text(label,modifier=Modifier.weight(1f))
        Switch(checked=value,onCheckedChange=change,modifier=Modifier.padding(start=12.dp).semantics { contentDescription=label })
    }
}
@OptIn(ExperimentalLayoutApi::class)
@Composable fun Choice(label: String,options: List<String>,selected: String,change: (String)->Unit) {
    Text(label,style=MaterialTheme.typography.titleMedium)
    FlowRow(horizontalArrangement=Arrangement.spacedBy(6.dp)) { options.forEach { option -> FilterChip(selected=option==selected,onClick={change(option)},label={Text(option)}) } }
}
@Composable private fun Intensity(value: Int,change: (Int)->Unit) {
    var draft by remember(value) { mutableFloatStateOf(value.toFloat()) }
    Text("Animation intensity: ${draft.toInt()}%")
    Slider(draft,{draft=it},onValueChangeFinished={change(draft.toInt())},valueRange=0f..100f,modifier=Modifier.semantics { contentDescription="Animation intensity" })
}
