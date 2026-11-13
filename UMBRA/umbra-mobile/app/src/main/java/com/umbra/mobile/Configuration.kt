package com.umbra.mobile

import android.content.Context
import androidx.datastore.preferences.core.*
import androidx.datastore.core.DataStore
import androidx.datastore.core.handlers.ReplaceFileCorruptionHandler
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.map
import java.io.IOException
import java.net.URI
import okhttp3.HttpUrl.Companion.toHttpUrlOrNull

val Context.umbraStore by preferencesDataStore("umbra_settings", corruptionHandler = ReplaceFileCorruptionHandler { emptyPreferences() })
enum class Profile { Adaptive, Cinematic, Minimal }
data class Config(
    val profile: Profile = Profile.Adaptive, val master: Boolean = true,
    val ambient: Boolean = true, val transitions: Boolean = true,
    val environment: Boolean = false, val alerts: Boolean = true,
    val wallpaper: Boolean = false, val statusPanel: Boolean = true,
    val greenAccent: Boolean = false, val url: String = "", val timeout: Int = 5,
    val favorites: Set<String> = emptySet()
)
data class MotionPolicy(val enabled: Boolean, val continuous: Boolean, val duration: Int)
fun motionPolicy(c: Config, powerSave: Boolean, lowBattery: Boolean, systemMotion: Boolean, interacting: Boolean): MotionPolicy {
    val enabled = c.master && c.profile != Profile.Minimal && !powerSave && !lowBattery && systemMotion
    return MotionPolicy(enabled, enabled && !interacting, if (!enabled) 0 else if (c.profile == Profile.Cinematic) 550 else 200)
}
fun validDeckUrl(value: String): Boolean = runCatching {
    val uri = URI(value)
    value.toHttpUrlOrNull() != null && value.length <= 2048 && value.none { it.isWhitespace() || it.isISOControl() } &&
        uri.scheme?.lowercase() in setOf("http", "https") && !uri.host.isNullOrBlank() &&
        uri.rawUserInfo == null && uri.rawFragment == null && uri.rawQuery == null &&
        (uri.port == -1 || uri.port in 1..65535)
}.getOrDefault(false)
class ConfigStore(private val store: DataStore<Preferences>) {
    constructor(context: Context) : this(context.applicationContext.umbraStore)
    val config = store.data.catch { if (it is IOException) emit(emptyPreferences()) else throw it }.map { p ->
        Config(
            profile = runCatching { Profile.valueOf(p[stringPreferencesKey("profile")] ?: "Adaptive") }.getOrDefault(Profile.Adaptive),
            master = p[booleanPreferencesKey("master")] ?: true,
            ambient = p[booleanPreferencesKey("ambient")] ?: true,
            transitions = p[booleanPreferencesKey("transitions")] ?: true,
            environment = p[booleanPreferencesKey("environment")] ?: false,
            alerts = p[booleanPreferencesKey("alerts")] ?: true,
            wallpaper = p[booleanPreferencesKey("wallpaper")] ?: false,
            statusPanel = p[booleanPreferencesKey("statusPanel")] ?: true,
            greenAccent = p[booleanPreferencesKey("greenAccent")] ?: false,
            url = p[stringPreferencesKey("url")]?.takeIf { it.isEmpty() || validDeckUrl(it) } ?: "",
            timeout = (p[intPreferencesKey("timeout")] ?: 5).coerceIn(1,30),
            favorites = p[stringSetPreferencesKey("favorites")] ?: emptySet()
        )
    }
    suspend fun flag(key: String, value: Boolean) { store.edit { it[booleanPreferencesKey(key)] = value } }
    suspend fun profile(value: Profile) { store.edit { it[stringPreferencesKey("profile")] = value.name } }
    suspend fun deck(url: String, timeout: Int) {
        require(url.isEmpty() || validDeckUrl(url))
        store.edit { it[stringPreferencesKey("url")] = url; it[intPreferencesKey("timeout")] = timeout.coerceIn(1,30) }
    }
    suspend fun favorite(id: String) { store.edit { p ->
        val key = stringSetPreferencesKey("favorites")
        val current = p[key] ?: emptySet()
        p[key] = if (id in current) current - id else current + id
    } }
}
