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
import androidx.compose.foundation.shape.CutCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.testTag
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
import androidx.lifecycle.lifecycleScope
import androidx.core.view.WindowCompat
import androidx.core.view.doOnAttach
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.distinctUntilChanged
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

val Amber = Color(0xFFFFB547)
val Green = Color(0xFF94B59A)
val Ink = Color(0xFF090B0C)
val Panel = Color(0xFF171B1E)
val White = Color(0xFFECE9E1)
val Muted = Color(0xFFADB2B3)
val Chamfer = GenericShape { size, _ ->
    val cut = (size.width * .035f).coerceAtMost(size.height / 3)
    moveTo(cut,0f); lineTo(size.width,0f); lineTo(size.width,size.height-cut)
    lineTo(size.width-cut,size.height); lineTo(0f,size.height); lineTo(0f,cut); close()
}
class MainActivity : ComponentActivity() {
    private val model: LauncherModel by viewModels()
    private val homeEvents = mutableIntStateOf(0)
    private var awaitingAttach = false
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        window.attributes = window.attributes.apply { layoutInDisplayCutoutMode = android.view.WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES }
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.RESUMED) { model.config.map { listOf(it.immersive,it.hideTopBar,it.hideBottomBar,it.windowBrightness) to it }.distinctUntilChanged { old,new -> old.first==new.first }.collect { applyDisplay(it.second) } }
        }
        setContent { Umbra(model,homeEvents.intValue) }
    }
    private fun applyDisplay(c: Config) {
        if(!window.decorView.isAttachedToWindow) {
            if(!awaitingAttach) { awaitingAttach=true;window.decorView.doOnAttach { awaitingAttach=false;applyDisplay(model.config.value) } }
            return
        }
        val controller = WindowCompat.getInsetsController(window,window.decorView)
        controller.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
        if(c.immersive && c.hideTopBar) controller.hide(WindowInsetsCompat.Type.statusBars()) else controller.show(WindowInsetsCompat.Type.statusBars())
        if(c.immersive && c.hideBottomBar) controller.hide(WindowInsetsCompat.Type.navigationBars()) else controller.show(WindowInsetsCompat.Type.navigationBars())
        window.attributes = window.attributes.apply { screenBrightness = c.windowBrightness }
    }
    override fun onWindowFocusChanged(hasFocus: Boolean) {
        super.onWindowFocusChanged(hasFocus)
        if(hasFocus) applyDisplay(model.config.value)
    }
    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        if (intent.hasCategory(Intent.CATEGORY_HOME)) homeEvents.intValue++
    }
}

@Composable private fun Umbra(model: LauncherModel, homeEvent: Int) {
    val context = LocalContext.current
    val lifecycle = androidx.lifecycle.compose.LocalLifecycleOwner.current.lifecycle
    val c by model.config.collectAsStateWithLifecycle()
    val apps by model.apps.collectAsStateWithLifecycle()
    val appError by model.appError.collectAsStateWithLifecycle()
    val settingsError by model.settingsError.collectAsStateWithLifecycle()
    var deviceRefresh by remember { mutableIntStateOf(0) }
    val device by rememberDevice(deviceRefresh)
    val count by UmbraNotificationListener.count.collectAsStateWithLifecycle()
    val granted = rememberNotificationAccess()
    val notificationCount = count.takeIf { c.notificationsEnabled && granted }
    var shadeDialog by remember { mutableStateOf(false) }
    var remoteModule by rememberSaveable { mutableStateOf("Engineering") }
    var settingsCategory by rememberSaveable { mutableStateOf("Animation") }
    var screen by rememberSaveable { mutableStateOf("HOME") }
    var query by rememberSaveable { mutableStateOf("") }
    var favoritesOnly by rememberSaveable { mutableStateOf(false) }
    var now by remember { mutableStateOf(LocalDateTime.now()) }
    var deckStatus by remember { mutableStateOf("NOT CHECKED") }
    var checkId by remember { mutableIntStateOf(0) }
    val headGate=remember { RefreshGate() }
    val pointer=remember { mutableStateOf(androidx.compose.ui.geometry.Offset(.5f,.5f)) }
    val parallaxAllowed by rememberUpdatedState(c.parallax && c.master && c.intensity>0)
    var active by remember { mutableStateOf(false) }
    var lastInteraction by remember { mutableLongStateOf(0L) }
    var interacting by remember { mutableStateOf(false) }
    val accent = if(c.accent.isNotEmpty()) Color(android.graphics.Color.parseColor(c.accent)) else if (c.greenAccent) Green else Amber
    val background = when(c.background) { "Graphite" -> Color(0xFF131719); "Blueprint" -> Color(0xFF0B141B); else -> Ink }
    val policy = motionPolicy(c,device.powerSave,device.battery in 0..20,device.motion,interacting || screen != "HOME",device.thermal,device.screenOn)
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
    LaunchedEffect(lifecycle,c.url,c.timeout,checkId,if(c.refreshOnNetwork) device.networkGeneration else 0L,c.refreshOnResume) {
        lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED) {
            if(!headGate.shouldRefresh(c.refreshOnResume,c.refreshOnNetwork,checkId,device.networkGeneration,c.url+"|"+c.timeout)) return@repeatOnLifecycle
            deckStatus = if (c.url.isEmpty()) "NOT CONFIGURED" else "CHECKING…"
            deckStatus = checkDeck(c.url,c.timeout)
        }
    }
    val homePull=rememberPullNavigation(c.swipeDown,{screen="COMMAND"},{})
    val startup = remember { Animatable(1f) }
    LaunchedEffect(active,policy.enabled,c.startup) {
        if(active && policy.enabled && c.startup) { startup.snapTo(1f-.06f*c.intensity/100f); startup.animateTo(1f,tween(policy.duration)) } else startup.snapTo(1f)
    }
    val colors = darkColorScheme(primary=accent,onPrimary=Ink,primaryContainer=Panel,onPrimaryContainer=White,
        background=background,surface=Panel,onSurface=White,onBackground=White,secondary=Green,onSecondary=Ink,
        secondaryContainer=Panel,onSecondaryContainer=Green,surfaceVariant=Panel,onSurfaceVariant=Muted,
        outline=Muted,outlineVariant=accent.copy(alpha=.4f),surfaceDim=Ink,surfaceBright=Panel,
        surfaceContainer=Panel,surfaceContainerHigh=Panel,surfaceContainerHighest=Color(0xFF252B2E),
        surfaceContainerLow=Color(0xFF111416),surfaceContainerLowest=Ink,error=Color(0xFFEF8B82),onError=Ink)
    val font = when(c.typography) { "Mono" -> FontFamily.Monospace; "System" -> FontFamily.Default; else -> FontFamily.SansSerif }
    val baseTypography=Typography()
    val typography=baseTypography.copy(
        bodyLarge=baseTypography.bodyLarge.copy(fontFamily=font),bodyMedium=baseTypography.bodyMedium.copy(fontFamily=font),bodySmall=baseTypography.bodySmall.copy(fontFamily=font),
        titleLarge=baseTypography.titleLarge.copy(fontFamily=font),titleMedium=baseTypography.titleMedium.copy(fontFamily=font),
        labelLarge=baseTypography.labelLarge.copy(fontFamily=if(c.typography=="Technical")FontFamily.Monospace else font),labelSmall=baseTypography.labelSmall.copy(fontFamily=font))
    MaterialTheme(colorScheme=colors,typography=typography,shapes=Shapes(extraSmall=CutCornerShape(2.dp),small=CutCornerShape(4.dp),medium=CutCornerShape(6.dp),large=CutCornerShape(8.dp),extraLarge=CutCornerShape(12.dp))) {
    if(shadeDialog) AlertDialog(onDismissRequest={shadeDialog=false},title={Text("Native Android notifications")},text={Text("Swipe from the very top edge of the display to reveal Android's notification shade. Android does not provide ordinary HOME apps a public API to expand it. UMBRA leaves this system gesture available.")},
        confirmButton={TextButton(onClick={model.change { it.copy(immersive=false,hideTopBar=false,hideBottomBar=false) };shadeDialog=false}){Text("Restore Android bars")}},
        dismissButton={TextButton(onClick={shadeDialog=false}){Text("Close")}})

        Surface(color=background,modifier=Modifier.fillMaxSize()) {
            Box(Modifier.fillMaxSize().pointerInput(Unit) {
                awaitPointerEventScope { while(true) { val event = awaitPointerEvent(); if (event.changes.any { it.pressed }) { lastInteraction = SystemClock.elapsedRealtime();if(parallaxAllowed) { val position=event.changes.first().position;pointer.value=androidx.compose.ui.geometry.Offset(position.x/size.width.coerceAtLeast(1),position.y/size.height.coerceAtLeast(1)) } } } }
            }) {
                if (active && policy.continuous && (c.ambient || c.environment || c.wallpaper || c.parallax || c.statusEffects)) Atmosphere(c,accent,pointer)
                Column(Modifier.fillMaxSize().alpha(if(policy.enabled && c.startup) startup.value else 1f).safeDrawingPadding().imePadding().padding(horizontal=20.dp,vertical=10.dp)) {
                    Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceBetween,verticalAlignment=Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) { Text("UMBRA",color=accent,fontSize=27.sp,fontWeight=FontWeight.Black,letterSpacing=5.sp,maxLines=1,overflow=TextOverflow.Ellipsis); Readout("MOBILE OS / TERMINAL 01",Muted) }
                        TextButton(onClick={model.change { it.copy(immersive=false,hideTopBar=false,hideBottomBar=false) }}) { Text("Android bars",fontSize=12.sp,color=accent) }
                    }
                    HorizontalDivider(Modifier.padding(vertical=12.dp),color=accent.copy(alpha=.45f))
                    if(settingsError) Text("Settings could not be saved. Check values and available storage, then try again.",color=Color(0xFFEF8B82),modifier=Modifier.semantics { liveRegion=LiveRegionMode.Polite })
                    if(c.statusPanel) StatusPanel(c,device,now,deckStatus,accent,notificationCount)
                    val pageContent: @Composable (String)->Unit = { page ->
                        when(page) {
                            "APPS" -> Column(Modifier.fillMaxSize()) {
                                Text("APPLICATION INDEX",color=accent,fontFamily=FontFamily.Monospace,fontSize=18.sp)
                                OutlinedTextField(query,{query=it},label={Text("Search applications")},singleLine=true,modifier=Modifier.fillMaxWidth().padding(top=10.dp))
                                Row(verticalAlignment=Alignment.CenterVertically) { Checkbox(favoritesOnly,{favoritesOnly=it}); Text("Favorites only"); Spacer(Modifier.weight(1f)); TextButton(onClick=model::refreshApps){Text("Refresh")} }
                                val filtered = apps.filter { it.label.contains(query,true) && (!favoritesOnly || it.id in c.favorites) }
                                if(appError) Text("Unable to read applications. Tap Refresh.",color=Color(0xFFEF8B82))
                                if(filtered.isEmpty()) Text("No applications match.",color=Muted,modifier=Modifier.padding(16.dp))
                                LazyVerticalGrid(columns=GridCells.Fixed(c.gridColumns),contentPadding=PaddingValues(bottom=16.dp),horizontalArrangement=Arrangement.spacedBy(8.dp),verticalArrangement=Arrangement.spacedBy(8.dp)) {
                                    items(filtered,key={it.id}) { app -> AppTile(app,model,app.id in c.favorites,{launch(app)},{model.favorite(app.id)},accent) }
                                }
                            }
                            "COMMAND" -> CommandCenter(c,device,model,apps,deckStatus,accent,::open,::launch,{screen="HOME"},{shadeDialog=true},
                                { if(it=="Deck") { if(validDeckUrl(c.url))open(Intent(Intent.ACTION_VIEW,android.net.Uri.parse(c.url))) else screen="CONFIG" } else {remoteModule=it; screen="ICARUS"} },{screen="DEVICE"},{deviceRefresh++},notificationCount)
                            "DEVICE" -> Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(16.dp)) {
                                Readout("DEVICE / SYSTEM DASHBOARD",accent)
                                TelemetryReadouts(device)
                                Button(onClick={deviceRefresh++},shape=Chamfer){Text("Refresh telemetry")}
                                Text("Readings are snapshots from Android APIs, refreshed on visibility entry and request. No invented CPU temperature or utilization.",color=Muted)
                            }
                            "ICARUS" -> IcarusScreen(c,model,accent,remoteModule,::open,{settingsCategory="ICARUS";screen="CONFIG"},device.powerSave || device.battery in 0..20 || device.thermal>=2 || !device.screenOn,device.networkGeneration)
                            "CONFIG" -> Configuration(c,model,accent,{open(Intent(Settings.ACTION_HOME_SETTINGS))},apps,::open,settingsCategory)
                            else -> Column(Modifier.fillMaxSize().nestedScroll(homePull).verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy((5+c.density*4).dp)) {
                                Row(Modifier.fillMaxWidth().heightIn(min=64.dp).testTag("home-swipe-handle").terminalSwipe(c.swipeDown,{screen="COMMAND"},{}),horizontalArrangement=Arrangement.SpaceBetween) { Readout("↓ COMMAND ACCESS",accent);Readout("SWIPE DOWN",Muted) }
                                Spacer(Modifier.height(12.dp))
                                BoxWithConstraints(Modifier.fillMaxWidth()) {
                                    val clockSize = minOf(64f,maxWidth.value/(3.2f*LocalDensity.current.fontScale))
                                    Text(now.format(DateTimeFormatter.ofPattern("HH:mm")),fontFamily=FontFamily.Monospace,fontSize=clockSize.sp,fontWeight=FontWeight.Light,color=White)
                                }
                                Readout(now.format(DateTimeFormatter.ofPattern("EEE / dd MMM yyyy")).uppercase(),Muted)
                                Readout("01 / COMMAND DECK",accent)
                                Button(onClick={screen="COMMAND"},shape=Chamfer,modifier=Modifier.fillMaxWidth()){Text("Command Center · swipe down above") }
                                Frame(accent) {
                                    Text("ICARUS",fontSize=24.sp,fontWeight=FontWeight.Bold,color=accent,letterSpacing=3.sp)
                                    AlertReadout(deckStatus,active && policy.enabled && c.alerts,accent,c.intensity)
                                    Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(8.dp)) {
                                        Button(onClick={ if(validDeckUrl(c.url)) open(Intent(Intent.ACTION_VIEW,android.net.Uri.parse(c.url).normalizeScheme())) else {settingsCategory="ICARUS";screen="CONFIG"} },modifier=Modifier.weight(1f),shape=Chamfer) { Text(if(c.url.isEmpty()) "Configure deck" else "Open deck") }
                                        OutlinedButton(onClick={checkId++},enabled=!deckStatus.startsWith("CHECKING"),shape=Chamfer) { Text("Check") }
                                    }
                                }
                                Readout("02 / QUICK ACCESS",accent)
                                val favorites = orderedFavorites(c,apps)
                                if(favorites.isEmpty()) Text("Star applications in the drawer to pin shortcuts here.",color=Muted)
                                favorites.chunked(3).forEach { row ->
                                    Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(8.dp)) {
                                        row.forEach { app -> Box(Modifier.weight(1f)) { AppTile(app.copy(label=c.quickLabels[app.id] ?: app.label),model,true,{launch(app)},{model.favorite(app.id)},accent) } }
                                        repeat(3-row.size) { Spacer(Modifier.weight(1f)) }
                                    }
                                }
                                OutlinedButton(onClick={screen="DEVICE"},modifier=Modifier.fillMaxWidth(),shape=Chamfer){Text("Device dashboard")}
                                OutlinedButton(onClick={open(Intent(Settings.ACTION_SETTINGS))},modifier=Modifier.fillMaxWidth(),shape=Chamfer) { Text("Android system settings") }
                                Spacer(Modifier.height(4.dp))
                            }
                        }
                    }
                    if(active && policy.enabled) {
                    AnimatedContent(targetState=screen,modifier=Modifier.weight(1f),transitionSpec={
                        if (active && policy.enabled && pageAnimationAllowed(initialState,targetState,c)) (fadeIn(tween(policy.duration)) + slideInHorizontally { it/12 }) togetherWith fadeOut(tween(policy.duration))
                        else EnterTransition.None togetherWith ExitTransition.None
                    },label="terminal navigation") { page -> pageContent(page) }
                    } else Box(Modifier.weight(1f)) { pageContent(screen) }
                    HorizontalDivider(Modifier.padding(top=8.dp),color=accent.copy(alpha=.3f))
                    Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceEvenly) {
                        listOf("HOME" to "Home","APPS" to "Apps","COMMAND" to "Deck","ICARUS" to "Icarus","CONFIG" to "Config").forEach { (id,label) ->
                            TextButton(onClick={screen=id},contentPadding=PaddingValues(horizontal=2.dp),modifier=Modifier.weight(1f).heightIn(min=56.dp).testTag("nav-$id")) { Text(label.uppercase(),color=if(screen==id) accent else Muted,fontFamily=FontFamily.Monospace,fontSize=12.sp) }
                        }
                    }
                }
            }
        }
    }
}

@Composable fun Readout(value: String,color: Color) { Text(value,color=color,fontFamily=FontFamily.Monospace,fontSize=12.sp,letterSpacing=1.sp) }
@Composable fun Frame(accent: Color, content: @Composable ColumnScope.()->Unit) {
    Surface(shape=Chamfer,color=Panel,border=BorderStroke(1.dp,accent),modifier=Modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp),verticalArrangement=Arrangement.spacedBy(10.dp),content=content)
    }
}
@Composable fun AppTile(app: LaunchApp,model: LauncherModel,favorite: Boolean,launch: ()->Unit,toggle: ()->Unit,accent: Color) {
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
@Composable private fun AlertReadout(status: String,animate: Boolean,accent: Color,intensity: Int) {
    val emphasis=remember { Animatable(0f) }
    LaunchedEffect(status,animate) {
        emphasis.snapTo(0f)
        if(animate && !status.startsWith("REACHABLE") && !status.startsWith("CHECKING")) {
            emphasis.animateTo(1f,tween(250));emphasis.animateTo(0f,tween(400))
        }
    }
    // Animate an underline, never the opacity or availability of functional text.
    Text(status,color=if(status.startsWith("OFFLINE")) Color(0xFFEF8B82) else accent,fontFamily=FontFamily.Monospace,fontSize=12.sp,
        modifier=Modifier.semantics { liveRegion=LiveRegionMode.Polite })
    Canvas(Modifier.fillMaxWidth().height(2.dp)) {
        if(animate)drawLine(accent.copy(alpha=.5f),androidx.compose.ui.geometry.Offset.Zero,
            androidx.compose.ui.geometry.Offset(size.width*emphasis.value*intensity/100f,0f),2f)
    }
}
@Composable private fun Atmosphere(c: Config,accent: Color,pointer: State<androidx.compose.ui.geometry.Offset>) {
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
        val intensity=c.intensity/100f
        if(c.ambient) drawRect(accent.copy(alpha=(.012f+phase*.018f)*intensity))
        if(c.wallpaper) {
            val y=size.height*(.2f+phase*.5f)
            drawLine(accent.copy(alpha=.10f*intensity),androidx.compose.ui.geometry.Offset(0f,y),androidx.compose.ui.geometry.Offset(size.width,y-size.width*.3f),2f)
        }
        if(c.parallax) {
            val shift=((phase-.5f)*16f+(pointer.value.x-.5f)*24f)*intensity
            repeat(4) { n -> drawLine(accent.copy(alpha=.045f*intensity),androidx.compose.ui.geometry.Offset(shift+n*size.width/3,0f),androidx.compose.ui.geometry.Offset(shift+n*size.width/3-size.width*.2f,size.height),1f) }
        }
        if(c.statusEffects) drawCircle(accent.copy(alpha=(.15f+.15f*phase)*intensity),3f,androidx.compose.ui.geometry.Offset(size.width-12f,40f))
        if(c.environment) repeat(12) { i ->
            val x=size.width*(i+1)/13
            val y=size.height*((i*.13f+phase*.15f)%1f)
            drawCircle(accent.copy(alpha=.15f*intensity),1.5f,androidx.compose.ui.geometry.Offset(x,y))
        }
    }
}

fun pageAnimationAllowed(from: String,to: String,c: Config) = if(from == "COMMAND" || to == "COMMAND") c.commandAnimations else c.transitions
