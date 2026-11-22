package com.umbra.mobile

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.core.handlers.ReplaceFileCorruptionHandler
import androidx.datastore.preferences.core.*
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.*
import okhttp3.HttpUrl.Companion.toHttpUrlOrNull
import java.io.IOException
import java.net.URI
import kotlin.math.pow

val Context.umbraStore by preferencesDataStore("umbra_settings", corruptionHandler = ReplaceFileCorruptionHandler { emptyPreferences() })
@Serializable enum class Profile { Adaptive, Cinematic, Minimal }
val MODULES = listOf("Device", "System", "ICARUS", "Notifications", "Applications")
val INDICATORS = setOf("Time", "Date", "Battery", "Network", "ICARUS", "Notifications")
const val MAX_CONFIG_BYTES = 1048576
@Serializable data class Config(
    val pcIndicator: Boolean=true, val activeHomePreset: String="default", val homePresets: List<HomePreset> = emptyList(),
    val profile: Profile = Profile.Adaptive, val master: Boolean = true,
    val ambient: Boolean = true, val transitions: Boolean = true,
    val environment: Boolean = false, val alerts: Boolean = true,
    val wallpaper: Boolean = false, val statusPanel: Boolean = true,
    val greenAccent: Boolean = false, val url: String = "", val timeout: Int = 5,
    val favorites: Set<String> = emptySet(),
    val startup: Boolean = true, val parallax: Boolean = true,
    val statusEffects: Boolean = true, val commandAnimations: Boolean = true,
    val intensity: Int = 65,
    val immersive: Boolean = true, val hideTopBar: Boolean = true, val hideBottomBar: Boolean = true,
    val indicators: Set<String> = INDICATORS - "Notifications",
    val accent: String = "", val background: String = "Void", val typography: String = "Technical",
    val density: Int = 2, val gridColumns: Int = 3, val tileSize: Int = 2,
    val moduleOrder: List<String> = MODULES, val hiddenModules: Set<String> = emptySet(),
    val quickOrder: List<String> = emptyList(), val quickLabels: Map<String, String> = emptyMap(),
    val swipeDown: Boolean = true, val secondSwipe: Boolean = true,
    val windowBrightness: Float = -1f,
    val serverUrl: String = "", val engineeringUrl: String = "", val loungeUrl: String = "", val simulatorUrl: String = "",
    val refreshOnResume: Boolean = true, val refreshOnNetwork: Boolean = true, val foregroundRefreshSeconds: Int = 0,
    val notificationsEnabled: Boolean = false,
    val visualDetail: VisualDetail = VisualDetail.Enhanced,
    val transitionStyle: TransitionStyle = TransitionStyle.SamsungInspired,
    val appLaunchTransitions: Boolean = true, val folderTransitions: Boolean = true, val widgetTransitions: Boolean = true,
    val showAppLabels: Boolean = true, val iconSize: Int = 48,
    val hiddenApps: Set<String> = emptySet(), val drawerOrder: List<String> = emptyList(),
    val desktop: DesktopLayout? = null,
    val weatherPlace: String = "", val weatherLatitude: Double? = null, val weatherLongitude: Double? = null,
    val weatherFahrenheit: Boolean = false,
    val instantOrder: List<String> = emptyList(), val instantLabels: Map<String,String> = emptyMap(), val instantFavorites: Set<String> = emptySet(),
    val gridLayouts: Map<String,GridLayout> = emptyMap(), val editHaptics: Boolean=false, val deckColumns: Int=2,
    val commandExpanded: Boolean=true, val statusTabs: Map<String,Boolean> = DEFAULT_STATUS_TABS,
    val instantSelection: Set<String>?=null, val widgetButtonSelections: Map<String,List<String>> = emptyMap(), val customButtons: List<CustomButton> = emptyList()
)
@Serializable private data class ConfigEnvelope(val schemaVersion: Int = 5, val settings: Config)
private val configJson = Json { encodeDefaults = true; ignoreUnknownKeys = false }
private val componentPattern = Regex("[A-Za-z0-9_.$]+/[A-Za-z0-9_.$]+")
fun validComponent(value: String) = value.length in 3..512 && componentPattern.matches(value)
fun validDeckUrl(value: String): Boolean = runCatching {
    val uri = URI(value)
    value.toHttpUrlOrNull() != null && value.length <= 2048 && value.none { it.isWhitespace() || it.isISOControl() } &&
        uri.scheme?.lowercase() in setOf("http", "https") && !uri.host.isNullOrBlank() &&
        uri.rawUserInfo == null && uri.rawFragment == null && uri.rawQuery == null &&
        (uri.port == -1 || uri.port in 1..65535)
}.getOrDefault(false)
fun validAccent(value: String): Boolean {
    if (value.isEmpty()) return true
    if (!Regex("#[0-9a-fA-F]{6}").matches(value)) return false
    val n = value.drop(1).toInt(16)
    fun channel(shift: Int): Double { val c = ((n shr shift) and 255)/255.0; return if(c <= .04045) c/12.92 else ((c+.055)/1.055).pow(2.4) }
    // Keep custom text/icons readable against every offered dark background.
    return .2126*channel(16)+.7152*channel(8)+.0722*channel(0) >= .25
}
fun validateConfig(c: Config): Config {
    validatePresets(c)
    require(c.gridLayouts.size<=128 && c.gridLayouts.keys.all {it.length in 1..120 && it.none(Char::isISOControl)})
    c.gridLayouts.values.forEach(::validateGrid)
    require(c.deckColumns in 2..4 && c.statusTabs.keys.all {it in STATUS_TABS})
    require(c.instantSelection==null || (c.instantSelection.size<=2048 && c.instantSelection.all {it.length in 1..180 && it.none(Char::isISOControl)}))
    require(c.widgetButtonSelections.size<=256 && c.widgetButtonSelections.values.all {v->v.size<=2048 && v.distinct().size==v.size && v.all {it.length in 1..180 && it.none(Char::isISOControl)}})
    require(c.customButtons.size<=512 && c.customButtons.map {it.id}.distinct().size==c.customButtons.size)
    c.customButtons.forEach(::validateButton)
    require(c.intensity in 0..100 && c.timeout in 1..30)
    require(c.iconSize in 32..72 && c.hiddenApps.size<=256 && c.hiddenApps.all(::validComponent))
    require(c.drawerOrder.size<=512 && c.drawerOrder.distinct().size==c.drawerOrder.size && c.drawerOrder.all(::validComponent))
    c.desktop?.let(::validateDesktop)
    require(c.weatherPlace.length<=120 && c.weatherPlace.none(Char::isISOControl))
    require((c.weatherLatitude==null)==(c.weatherLongitude==null))
    c.weatherLatitude?.let { require(it.isFinite() && it in -90.0..90.0) }
    c.weatherLongitude?.let { require(it.isFinite() && it in -180.0..180.0) }
    require(c.instantOrder.size<=2048 && c.instantOrder.distinct().size==c.instantOrder.size && c.instantOrder.all { it.length in 1..160 && it.none(Char::isISOControl) })
    require(c.instantFavorites.size<=2048 && c.instantFavorites.all { it.length in 1..160 && it.none(Char::isISOControl) })
    require(c.instantLabels.size<=2048 && c.instantLabels.all { (key,value)->key.length in 1..160 && key.none(Char::isISOControl) && value.length in 1..48 && value.none(Char::isISOControl) })
    require(c.density in 1..3 && c.gridColumns in 3..5 && c.tileSize in 1..3)
    require(c.background in listOf("Void", "Graphite", "Blueprint"))
    require(c.typography in listOf("Technical", "Mono", "System"))
    require(validAccent(c.accent))
    require(c.indicators.all { it in INDICATORS })
    require(c.moduleOrder.size == MODULES.size && c.moduleOrder.toSet() == MODULES.toSet())
    require(c.hiddenModules.all { it in MODULES })
    require(c.favorites.size <= 256 && c.favorites.all(::validComponent))
    require(c.quickOrder.size <= 256 && c.quickOrder.distinct().size == c.quickOrder.size && c.quickOrder.all(::validComponent))
    require(c.quickLabels.size <= 256 && c.quickLabels.all { (key, value) -> validComponent(key) && value.length in 1..48 && value.none { it.isISOControl() } })
    require(c.windowBrightness.isFinite() && (c.windowBrightness == -1f || c.windowBrightness in .1f..1f))
    require(c.foregroundRefreshSeconds == 0 || c.foregroundRefreshSeconds in 30..300)
    require(listOf(c.url,c.serverUrl,c.engineeringUrl,c.loungeUrl,c.simulatorUrl).all { it.isEmpty() || validDeckUrl(it) })
    return c
}
private fun encodeConfig(c: Config): String {
    val text = configJson.encodeToString(ConfigEnvelope(settings = validateConfig(c)))
    require(text.toByteArray(Charsets.UTF_8).size <= MAX_CONFIG_BYTES)
    return text
}
fun exportConfig(c: Config): String = encodeConfig(c.copy(desktop=c.desktop?.let(::portableDesktop),homePresets=c.homePresets.map {it.copy(desktop=portableDesktop(it.desktop))}))
private fun decodeConfig(text: String,portable: Boolean): Config {
    require(text.toByteArray(Charsets.UTF_8).size <= MAX_CONFIG_BYTES) { "Configuration exceeds 1 MiB" }
    val root = configJson.parseToJsonElement(text) as? JsonObject ?: error("Expected configuration object")
    require(root.keys == setOf("schemaVersion", "settings"))
    val version = root["schemaVersion"] as? JsonPrimitive ?: error("Missing version")
    require(!version.isString && version.intOrNull in setOf(2,3,4,5))
    val fields = root["settings"] as? JsonObject ?: error("Missing settings")
    val defaults = configJson.encodeToJsonElement(Config()).jsonObject
    fields.forEach { (key, value) ->
        val sample = defaults[key] ?: error("Unknown setting")
        if(key=="homePresets"){validatePresetsJson(value);return@forEach}
        if(key=="widgetButtonSelections"){require(value is JsonObject && value.values.all {it is JsonArray && it.all {v->v is JsonPrimitive && v.isString}});return@forEach}
        if(key=="gridLayouts"){validateGridsJson(value);return@forEach}
        if(key=="customButtons"){validateButtonsJson(value);return@forEach}
        if(key=="statusTabs"){require(value is JsonObject && value.values.all {it is JsonPrimitive && !it.isString && it.booleanOrNull!=null});return@forEach}
        if(key=="instantSelection"){require(value is JsonNull || (value is JsonArray && value.all {it is JsonPrimitive && it.isString}));return@forEach}
        if(key=="desktop") { if(value !is JsonNull)validateDesktopJson(value);return@forEach }
        if(key=="weatherLatitude" || key=="weatherLongitude") { require(value is JsonNull || (value is JsonPrimitive && !value.isString && value.doubleOrNull?.isFinite()==true));return@forEach }
        when(sample) {
            is JsonPrimitive -> {
                require(value is JsonPrimitive && value !is JsonNull)
                if(sample.isString) require(value.isString)
                else if(sample.booleanOrNull != null) require(!value.isString && value.booleanOrNull != null)
                else if(key == "windowBrightness") require(!value.isString && value.floatOrNull?.isFinite() == true)
                else require(!value.isString && value.intOrNull != null)
            }
            is JsonArray -> require(value is JsonArray && value.all { it is JsonPrimitive && it.isString })
            is JsonObject -> require(value is JsonObject && value.values.all { it is JsonPrimitive && it.isString })
        }
    }
    val envelope = configJson.decodeFromString<ConfigEnvelope>(text)
    require(envelope.schemaVersion in setOf(2,3,4,5)) { "Unsupported configuration version" }
    val valid=validateConfig(envelope.settings)
    return if(portable)valid.copy(desktop=valid.desktop?.let(::portableDesktop),homePresets=valid.homePresets.map {it.copy(desktop=portableDesktop(it.desktop))}) else valid
}
fun importConfig(text: String): Config = decodeConfig(text,true)
fun serverBase(c: Config): String {
    if(c.serverUrl.isNotEmpty()) return c.serverUrl.trimEnd('/') + "/"
    return c.url.toHttpUrlOrNull()?.newBuilder()?.encodedPath("/")?.query(null)?.fragment(null)?.build()?.toString() ?: ""
}
fun remoteDestination(c: Config, module: String): String = when(module) {
    "Engineering" -> c.engineeringUrl; "Simulator" -> c.simulatorUrl; else -> c.url
}.ifEmpty { c.url }
fun orderedFavorites(c: Config, apps: List<LaunchApp>): List<LaunchApp> {
    val pinned = apps.filter { it.id in c.favorites && it.id !in c.hiddenApps }
    val byId = pinned.associateBy { it.id }
    return c.quickOrder.mapNotNull { byId[it] } + pinned.filter { it.id !in c.quickOrder }
}
fun moveItem(items: List<String>, value: String, delta: Int): List<String> {
    val index = items.indexOf(value)
    if(index < 0) return items
    val target = (index + delta).coerceIn(0,items.lastIndex)
    return items.toMutableList().apply { removeAt(index); add(target,value) }
}
fun resetCategory(c: Config, category: String): Config {
    val d = Config()
    return when(category) {
        "Appearance" -> c.copy(visualDetail=d.visualDetail,showAppLabels=d.showAppLabels,iconSize=d.iconSize,accent=d.accent,greenAccent=d.greenAccent,background=d.background,typography=d.typography,density=d.density,gridColumns=d.gridColumns)
        "Animation" -> c.copy(profile=d.profile,master=d.master,ambient=d.ambient,transitions=d.transitions,environment=d.environment,alerts=d.alerts,wallpaper=d.wallpaper,startup=d.startup,parallax=d.parallax,statusEffects=d.statusEffects,commandAnimations=d.commandAnimations,intensity=d.intensity)
        "Display" -> c.copy(immersive=d.immersive,hideTopBar=d.hideTopBar,hideBottomBar=d.hideBottomBar,statusPanel=d.statusPanel,indicators=d.indicators,windowBrightness=d.windowBrightness)
        "Command Center" -> c.copy(moduleOrder=d.moduleOrder,hiddenModules=d.hiddenModules,tileSize=d.tileSize,quickOrder=d.quickOrder,quickLabels=d.quickLabels,swipeDown=d.swipeDown,secondSwipe=d.secondSwipe)
        "ICARUS" -> c.copy(url=d.url,serverUrl=d.serverUrl,timeout=d.timeout,engineeringUrl=d.engineeringUrl,loungeUrl=d.loungeUrl,simulatorUrl=d.simulatorUrl,refreshOnResume=d.refreshOnResume,refreshOnNetwork=d.refreshOnNetwork,foregroundRefreshSeconds=d.foregroundRefreshSeconds)
        else -> c
    }
}
data class MotionPolicy(val enabled: Boolean, val continuous: Boolean, val duration: Int)
fun motionPolicy(c: Config, powerSave: Boolean, lowBattery: Boolean, systemMotion: Boolean, interacting: Boolean, thermal: Int = 0, screenOn: Boolean = true): MotionPolicy {
    val enabled = c.master && c.intensity > 0 && c.profile != Profile.Minimal && !powerSave && !lowBattery && systemMotion && thermal < 3 && screenOn
    return MotionPolicy(enabled, enabled && !interacting && thermal < 2,
        if (!enabled) 0 else if(interacting && c.profile == Profile.Adaptive) 100 else if(c.profile == Profile.Cinematic) 550 else 200)
}
class ConfigStore(private val store: DataStore<Preferences>) {
    constructor(context: Context) : this(context.applicationContext.umbraStore)
    private val key = stringPreferencesKey("config_v2")
    private fun read(p: Preferences): Config {
        p[key]?.let { return runCatching { decodeConfig(it,false) }.getOrDefault(Config()) }
        // Phase 1 migration. Preserve the former combined startup/transition preference.
        fun flag(name: String, default: Boolean) = p[booleanPreferencesKey(name)] ?: default
        return Config(
            profile=runCatching { Profile.valueOf(p[stringPreferencesKey("profile")] ?: "Adaptive") }.getOrDefault(Profile.Adaptive),
            master=flag("master",true),ambient=flag("ambient",true),transitions=flag("transitions",true),startup=flag("transitions",true),
            environment=flag("environment",false),alerts=flag("alerts",true),wallpaper=flag("wallpaper",false),
            statusPanel=flag("statusPanel",true),greenAccent=flag("greenAccent",false),
            url=p[stringPreferencesKey("url")]?.takeIf(::validDeckUrl) ?: "",timeout=(p[intPreferencesKey("timeout")] ?: 5).coerceIn(1,30),
            favorites=(p[stringSetPreferencesKey("favorites")] ?: emptySet()).filter(::validComponent).take(256).toSet()
        )
    }
    val config = store.data.catch { if(it is IOException) emit(emptyPreferences()) else throw it }.map(::read)
    suspend fun update(transform: (Config) -> Config) { store.edit { p -> p[key] = encodeConfig(transform(read(p))) } }
    suspend fun replace(c: Config) { val encoded = encodeConfig(c); store.edit { it[key] = encoded } }
    suspend fun flag(key: String, value: Boolean) = update { c -> when(key) {
        "master" -> c.copy(master=value); "ambient" -> c.copy(ambient=value); "transitions" -> c.copy(transitions=value)
        "environment" -> c.copy(environment=value); "alerts" -> c.copy(alerts=value); "wallpaper" -> c.copy(wallpaper=value)
        "statusPanel" -> c.copy(statusPanel=value); "greenAccent" -> c.copy(greenAccent=value)
        else -> c
    } }
    suspend fun profile(value: Profile) = update { it.copy(profile=value) }
    suspend fun deck(url: String, timeout: Int) { require(url.isEmpty() || validDeckUrl(url)); update { it.copy(url=url,timeout=timeout.coerceIn(1,30)) } }
    suspend fun favorite(id: String) = update { c ->
        require(validComponent(id))
        if(id in c.favorites) c.copy(favorites=c.favorites-id,quickOrder=c.quickOrder-id,quickLabels=c.quickLabels-id,
            desktop=c.desktop?.copy(pages=c.desktop.pages.map { p->p.copy(items=p.items.filterNot { it.kind=="app" && it.component==id }) }))
        else c.copy(favorites=c.favorites+id,quickOrder=(c.quickOrder+id).distinct(),desktop=c.desktop?.let { layout ->
            if(layout.pages.any { p->p.items.any { it.kind=="app" && it.component==id } })layout
            else layout.updatePage(layout.homePageId) { it.copy(items=it.items+DesktopItem(desktopId(),component=id)) }
        })
    }
}
