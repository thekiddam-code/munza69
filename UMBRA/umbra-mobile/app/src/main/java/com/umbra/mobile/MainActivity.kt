package com.umbra.mobile

import android.animation.ValueAnimator
import android.content.*
import android.database.ContentObserver
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.*
import android.provider.Settings
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.*
import androidx.compose.foundation.shape.GenericShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LifecycleStartEffect
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.repeatOnLifecycle
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

private val Amber = Color(0xFFFFB547)
private val Green = Color(0xFF94B59A)
private val Ink = Color(0xFF090B0C)
private val Panel = Color(0xFF171B1E)
private val White = Color(0xFFECE9E1)
private val Muted = Color(0xFFADB2B3)
private val Chamfer = GenericShape { size, _ ->
    val cut = (size.width * .035f).coerceAtMost(size.height / 3)
    moveTo(cut,0f); lineTo(size.width,0f); lineTo(size.width,size.height-cut)
    lineTo(size.width-cut,size.height); lineTo(0f,size.height); lineTo(0f,cut); close()
}
class MainActivity : ComponentActivity() {
    private val model: LauncherModel by viewModels()
    private val homeEvents = mutableIntStateOf(0)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent { Umbra(model,homeEvents.intValue) }
    }
    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        if (intent.hasCategory(Intent.CATEGORY_HOME)) homeEvents.intValue++
    }
}
private data class Device(val battery: Int = -1, val charging: Boolean = false, val network: String = "OFFLINE", val powerSave: Boolean = false, val motion: Boolean = true)
@Composable private fun rememberDevice(): State<Device> {
    val context = LocalContext.current
    val state = remember { mutableStateOf(Device()) }
    LifecycleStartEffect(context) {
        val cm = context.getSystemService(ConnectivityManager::class.java)
        val pm = context.getSystemService(PowerManager::class.java)
        fun update() {
            val b = context.registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
            val level = b?.getIntExtra(BatteryManager.EXTRA_LEVEL,-1) ?: -1
            val scale = b?.getIntExtra(BatteryManager.EXTRA_SCALE,100) ?: 100
            val status = b?.getIntExtra(BatteryManager.EXTRA_STATUS,-1)
            val capabilities = cm.getNetworkCapabilities(cm.activeNetwork)
            val network = when {
                capabilities == null -> "OFFLINE"
                capabilities.hasTransport(NetworkCapabilities.TRANSPORT_VPN) -> "VPN NETWORK"
                capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> "WI-FI"
                capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> "CELLULAR"
                else -> "CONNECTED"
            }
            state.value = Device(if (level >= 0 && scale > 0) level*100/scale else -1,
                status == BatteryManager.BATTERY_STATUS_CHARGING || status == BatteryManager.BATTERY_STATUS_FULL,
                network, pm.isPowerSaveMode, ValueAnimator.areAnimatorsEnabled() &&
                    Settings.Global.getFloat(context.contentResolver,Settings.Global.TRANSITION_ANIMATION_SCALE,1f) > 0f &&
                    Settings.Global.getFloat(context.contentResolver,Settings.Global.WINDOW_ANIMATION_SCALE,1f) > 0f)
        }
        val handler = Handler(Looper.getMainLooper())
        val receiver = object : BroadcastReceiver() { override fun onReceive(c: Context?, i: Intent?) { update() } }
        val observer = object : ContentObserver(handler) { override fun onChange(selfChange: Boolean) { update() } }
        val network = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(n: android.net.Network) { handler.post { update() } }
            override fun onLost(n: android.net.Network) { handler.post { update() } }
            override fun onCapabilitiesChanged(n: android.net.Network, c: NetworkCapabilities) { handler.post { update() } }
        }
        ContextCompat.registerReceiver(context,receiver,IntentFilter().apply {
            addAction(Intent.ACTION_BATTERY_CHANGED); addAction(PowerManager.ACTION_POWER_SAVE_MODE_CHANGED)
        },ContextCompat.RECEIVER_NOT_EXPORTED)
        listOf(Settings.Global.ANIMATOR_DURATION_SCALE,Settings.Global.TRANSITION_ANIMATION_SCALE,Settings.Global.WINDOW_ANIMATION_SCALE).forEach {
            context.contentResolver.registerContentObserver(Settings.Global.getUriFor(it),false,observer)
        }
        cm.registerDefaultNetworkCallback(network)
        update()
        onStopOrDispose {
            context.unregisterReceiver(receiver); context.contentResolver.unregisterContentObserver(observer)
            cm.unregisterNetworkCallback(network); handler.removeCallbacksAndMessages(null)
        }
    }
    return state
}

@Composable private fun Umbra(model: LauncherModel, homeEvent: Int) {
    val context = LocalContext.current
    val lifecycle = androidx.lifecycle.compose.LocalLifecycleOwner.current.lifecycle
    val c by model.config.collectAsStateWithLifecycle()
    val apps by model.apps.collectAsStateWithLifecycle()
    val appError by model.appError.collectAsStateWithLifecycle()
    val settingsError by model.settingsError.collectAsStateWithLifecycle()
    val device by rememberDevice()
    var screen by rememberSaveable { mutableStateOf("HOME") }
    var query by rememberSaveable { mutableStateOf("") }
    var favoritesOnly by rememberSaveable { mutableStateOf(false) }
    var now by remember { mutableStateOf(LocalDateTime.now()) }
    var deckStatus by remember { mutableStateOf("NOT CHECKED") }
    var checkId by remember { mutableIntStateOf(0) }
    var active by remember { mutableStateOf(false) }
    var lastInteraction by remember { mutableLongStateOf(0L) }
    var interacting by remember { mutableStateOf(false) }
    val accent = if (c.greenAccent) Green else Amber
    val policy = motionPolicy(c,device.powerSave,device.battery in 0..20,device.motion,interacting || screen != "HOME")
    fun open(intent: Intent) {
        try { context.startActivity(intent) } catch (_: ActivityNotFoundException) {
            Toast.makeText(context,"No application can open this destination.",Toast.LENGTH_SHORT).show()
            model.refreshApps()
        } catch (_: SecurityException) { Toast.makeText(context,"Android restricted this action.",Toast.LENGTH_SHORT).show() }
    }
    fun launch(app: LaunchApp) = open(Intent.makeMainActivity(ComponentName.unflattenFromString(app.id)))
    LaunchedEffect(homeEvent) { screen = "HOME"; query = "" }
    BackHandler(screen != "HOME") { screen = "HOME"; query = "" }
    LifecycleStartEffect(Unit) {
        active = true; model.refreshApps()
        val receiver = object : BroadcastReceiver() { override fun onReceive(c: Context?, i: Intent?) { model.refreshApps() } }
        ContextCompat.registerReceiver(context,receiver,IntentFilter().apply {
            addAction(Intent.ACTION_PACKAGE_ADDED); addAction(Intent.ACTION_PACKAGE_REMOVED); addAction(Intent.ACTION_PACKAGE_CHANGED); addDataScheme("package")
        },ContextCompat.RECEIVER_NOT_EXPORTED)
        onStopOrDispose { active = false; context.unregisterReceiver(receiver) }
    }
    LaunchedEffect(lifecycle) {
        lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED) {
            while (true) { now = LocalDateTime.now(); delay(60_000L - System.currentTimeMillis()%60_000L) }
        }
    }
    LaunchedEffect(lastInteraction) {
        interacting = true; delay(2500); interacting = false
    }
    LaunchedEffect(lifecycle,c.url,c.timeout,checkId,device.network) {
        lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED) {
            deckStatus = if (c.url.isEmpty()) "NOT CONFIGURED" else "CHECKING…"
            deckStatus = checkDeck(c.url,c.timeout)
        }
    }
    val startup = remember { Animatable(1f) }
    LaunchedEffect(active,policy.enabled,c.transitions) {
        if(active && policy.enabled && c.transitions) { startup.snapTo(.8f); startup.animateTo(1f,tween(policy.duration)) } else startup.snapTo(1f)
    }
    val colors = darkColorScheme(primary=accent,background=Ink,surface=Panel,onSurface=White,onBackground=White,secondary=Green)
    MaterialTheme(colorScheme=colors) {
        Surface(color=Ink,modifier=Modifier.fillMaxSize()) {
            Box(Modifier.fillMaxSize().pointerInput(Unit) {
                awaitPointerEventScope { while(true) { val event = awaitPointerEvent(); if (event.changes.any { it.pressed }) lastInteraction = SystemClock.elapsedRealtime() } }
            }) {
                if (active && policy.continuous && (c.ambient || c.environment || c.wallpaper)) Atmosphere(c,accent)
                Column(Modifier.fillMaxSize().alpha(if(policy.enabled && c.transitions) startup.value else 1f).safeDrawingPadding().imePadding().padding(horizontal=20.dp,vertical=10.dp)) {
                    Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceBetween,verticalAlignment=Alignment.CenterVertically) {
                        Column { Text("UMBRA",color=accent,fontSize=27.sp,fontWeight=FontWeight.Black,letterSpacing=5.sp); Readout("MOBILE OS / TERMINAL 01",Muted) }
                        Text("◆",color=Green,fontSize=24.sp,modifier=Modifier.semantics { contentDescription = "Terminal active" })
                    }
                    HorizontalDivider(Modifier.padding(vertical=12.dp),color=accent.copy(alpha=.45f))
                    if(settingsError) Text("Settings could not be saved. Check device storage and try again.",color=Color(0xFFEF8B82),modifier=Modifier.semantics { liveRegion=LiveRegionMode.Polite })
                    AnimatedContent(targetState=screen,modifier=Modifier.weight(1f),transitionSpec={
                        if (active && policy.enabled && c.transitions) (fadeIn(tween(policy.duration)) + slideInHorizontally { it/12 }) togetherWith fadeOut(tween(policy.duration))
                        else EnterTransition.None togetherWith ExitTransition.None
                    },label="terminal navigation") { page ->
                        when(page) {
                            "APPS" -> Column(Modifier.fillMaxSize()) {
                                Text("APPLICATION INDEX",color=accent,fontFamily=FontFamily.Monospace,fontSize=18.sp)
                                OutlinedTextField(query,{query=it},label={Text("Search applications")},singleLine=true,modifier=Modifier.fillMaxWidth().padding(top=10.dp))
                                Row(verticalAlignment=Alignment.CenterVertically) { Checkbox(favoritesOnly,{favoritesOnly=it}); Text("Favorites only"); Spacer(Modifier.weight(1f)); TextButton(onClick=model::refreshApps){Text("Refresh")} }
                                val filtered = apps.filter { it.label.contains(query,true) && (!favoritesOnly || it.id in c.favorites) }
                                if(appError) Text("Unable to read applications. Tap Refresh.",color=Color(0xFFEF8B82))
                                if(filtered.isEmpty()) Text("No applications match.",color=Muted,modifier=Modifier.padding(16.dp))
                                LazyVerticalGrid(columns=GridCells.Adaptive(98.dp),contentPadding=PaddingValues(bottom=16.dp),horizontalArrangement=Arrangement.spacedBy(8.dp),verticalArrangement=Arrangement.spacedBy(8.dp)) {
                                    items(filtered,key={it.id}) { app -> AppTile(app,model,app.id in c.favorites,{launch(app)},{model.favorite(app.id)},accent) }
                                }
                            }
                            "CONFIG" -> Configuration(c,model,accent,{open(Intent(Settings.ACTION_HOME_SETTINGS))})
                            else -> Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(14.dp)) {
                                Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceBetween) { Readout(device.network,Green); Readout(if(device.battery<0) "BAT --" else "BAT ${device.battery}%${if(device.charging) " +" else ""}",accent) }
                                Spacer(Modifier.height(12.dp))
                                BoxWithConstraints(Modifier.fillMaxWidth()) {
                                    val clockSize = minOf(64f,maxWidth.value/(3.2f*LocalDensity.current.fontScale))
                                    Text(now.format(DateTimeFormatter.ofPattern("HH:mm")),fontFamily=FontFamily.Monospace,fontSize=clockSize.sp,fontWeight=FontWeight.Light,color=White)
                                }
                                Readout(now.format(DateTimeFormatter.ofPattern("EEE / dd MMM yyyy")).uppercase(),Muted)
                                Readout("01 / COMMAND DECK",accent)
                                Frame(accent) {
                                    Text("ICARUS",fontSize=24.sp,fontWeight=FontWeight.Bold,color=accent,letterSpacing=3.sp)
                                    AlertReadout(deckStatus,active && policy.enabled && c.alerts,accent)
                                    Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(8.dp)) {
                                        Button(onClick={ if(validDeckUrl(c.url)) open(Intent(Intent.ACTION_VIEW,android.net.Uri.parse(c.url).normalizeScheme())) else screen="CONFIG" },modifier=Modifier.weight(1f),shape=Chamfer) { Text(if(c.url.isEmpty()) "Configure deck" else "Open deck") }
                                        OutlinedButton(onClick={checkId++},enabled=!deckStatus.startsWith("CHECKING"),shape=Chamfer) { Text("Check") }
                                    }
                                }
                                Readout("02 / QUICK ACCESS",accent)
                                val favorites = apps.filter { it.id in c.favorites }
                                if(favorites.isEmpty()) Text("Star applications in the drawer to pin shortcuts here.",color=Muted)
                                favorites.chunked(3).forEach { row ->
                                    Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(8.dp)) {
                                        row.forEach { app -> Box(Modifier.weight(1f)) { AppTile(app,model,true,{launch(app)},{model.favorite(app.id)},accent) } }
                                        repeat(3-row.size) { Spacer(Modifier.weight(1f)) }
                                    }
                                }
                                if(c.statusPanel) Frame(accent.copy(alpha=.4f)) {
                                    Readout("DEVICE TELEMETRY",accent)
                                    Text("${device.network} · ${if(device.charging) "Charging" else "On battery"}",color=White)
                                    Text("${c.profile} · ${if(policy.enabled) "Motion available" else "Motion reduced"}",color=Muted)
                                    if(device.powerSave) Text("Android power saving is active",color=Green)
                                }
                                OutlinedButton(onClick={open(Intent(Settings.ACTION_SETTINGS))},modifier=Modifier.fillMaxWidth(),shape=Chamfer) { Text("Android system settings") }
                                Spacer(Modifier.height(4.dp))
                            }
                        }
                    }
                    HorizontalDivider(Modifier.padding(top=8.dp),color=accent.copy(alpha=.3f))
                    Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceEvenly) {
                        listOf("HOME" to "Home","APPS" to "Apps","CONFIG" to "Config").forEach { (id,label) ->
                            TextButton(onClick={screen=id},modifier=Modifier.heightIn(min=56.dp)) { Text(label.uppercase(),color=if(screen==id) accent else Muted,fontFamily=FontFamily.Monospace) }
                        }
                    }
                }
            }
        }
    }
}

@Composable private fun Readout(value: String,color: Color) { Text(value,color=color,fontFamily=FontFamily.Monospace,fontSize=12.sp,letterSpacing=1.sp) }
@Composable private fun Frame(accent: Color, content: @Composable ColumnScope.()->Unit) {
    Surface(shape=Chamfer,color=Panel,border=BorderStroke(1.dp,accent),modifier=Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(10.dp),content=content)
    }
}
@Composable private fun AppTile(app: LaunchApp,model: LauncherModel,favorite: Boolean,launch: ()->Unit,toggle: ()->Unit,accent: Color) {
    var bitmap by remember(app.id) { mutableStateOf<android.graphics.Bitmap?>(null) }
    LaunchedEffect(app.id) { bitmap = model.icon(app.id) }
    Surface(shape=Chamfer,color=Panel,border=BorderStroke(1.dp,accent.copy(alpha=.25f))) {
        Column(horizontalAlignment=Alignment.CenterHorizontally,modifier=Modifier.fillMaxWidth()) {
            Column(Modifier.fillMaxWidth().clickable(onClick=launch).padding(top=12.dp,start=6.dp,end=6.dp),horizontalAlignment=Alignment.CenterHorizontally) {
                if(bitmap!=null) Image(bitmap!!.asImageBitmap(),contentDescription=null,modifier=Modifier.size(40.dp)) else Text("◇",fontSize=32.sp,color=accent,modifier=Modifier.size(40.dp))
                Text(app.label,color=White,fontSize=13.sp,maxLines=2,overflow=TextOverflow.Ellipsis,modifier=Modifier.heightIn(min=40.dp).padding(top=6.dp),textAlign=androidx.compose.ui.text.style.TextAlign.Center)
            }
            TextButton(onClick=toggle,modifier=Modifier.heightIn(min=48.dp).semantics { contentDescription = if(favorite) "Remove ${app.label} from favorites" else "Add ${app.label} to favorites" }) { Text(if(favorite) "★" else "☆",color=accent,fontSize=20.sp) }
        }
    }
}
@Composable private fun AlertReadout(status: String,animate: Boolean,accent: Color) {
    val alpha = remember { Animatable(1f) }
    LaunchedEffect(status,animate) {
        alpha.snapTo(1f)
        if(animate && !status.startsWith("REACHABLE") && !status.startsWith("CHECKING")) {
            alpha.animateTo(.5f,tween(250)); alpha.animateTo(1f,tween(400))
        }
    }
    Text(status,color=if(status.startsWith("OFFLINE")) Color(0xFFEF8B82) else accent,fontFamily=FontFamily.Monospace,fontSize=12.sp,modifier=Modifier.alpha(if(animate) alpha.value else 1f).semantics { liveRegion=LiveRegionMode.Polite })
}
@Composable private fun Atmosphere(c: Config,accent: Color) {
    // Decorative effects update at 8 Hz (Adaptive) or 12 Hz (Cinematic), not display refresh rate.
    var phase by remember { mutableFloatStateOf(0f) }
    LaunchedEffect(c.profile) {
        val period = if(c.profile==Profile.Cinematic) 18000L else 32000L
        while(true) {
            val progress=(SystemClock.uptimeMillis()%period).toFloat()/period
            phase=if(progress<.5f) progress*2f else (1f-progress)*2f
            delay(if(c.profile==Profile.Cinematic) 83L else 125L)
        }
    }
    Canvas(Modifier.fillMaxSize()) {
        if(c.ambient) drawRect(accent.copy(alpha=.012f+phase*.018f))
        if(c.wallpaper) {
            val y=size.height*(.2f+phase*.5f)
            drawLine(accent.copy(alpha=.10f),androidx.compose.ui.geometry.Offset(0f,y),androidx.compose.ui.geometry.Offset(size.width,y-size.width*.3f),2f)
        }
        if(c.environment) repeat(12) { i ->
            val x=size.width*(i+1)/13
            val y=size.height*((i*.13f+phase*.15f)%1f)
            drawCircle(accent.copy(alpha=.15f),1.5f,androidx.compose.ui.geometry.Offset(x,y))
        }
    }
}
