package com.umbra.mobile

import android.app.Application
import android.content.ComponentName
import android.content.Intent
import android.graphics.Bitmap
import android.util.LruCache
import androidx.core.graphics.drawable.toBitmap
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import okhttp3.*
import java.io.IOException
import java.text.Collator
import java.util.concurrent.TimeUnit
import kotlin.coroutines.resume

data class LaunchApp(val id: String, val label: String)
class LauncherModel(app: Application) : AndroidViewModel(app) {
    val store = ConfigStore(app)
    val config = store.config.stateIn(viewModelScope, SharingStarted.Eagerly, Config())
    val apps = MutableStateFlow<List<LaunchApp>>(emptyList())
    val appError = MutableStateFlow(false)
    val settingsError = MutableStateFlow(false)
    private val icons = LruCache<String, Bitmap>(128)
    private var loading: Job? = null
    fun refreshApps() {
        loading?.cancel()
        loading = viewModelScope.launch(Dispatchers.IO) {
            runCatching {
                val pm = getApplication<Application>().packageManager
                val intent = Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER)
                val collator = Collator.getInstance()
                pm.queryIntentActivities(intent, 0).filter { it.activityInfo.packageName != "com.umbra.mobile" }
                    .map { LaunchApp(ComponentName(it.activityInfo.packageName, it.activityInfo.name).flattenToString(), it.loadLabel(pm).toString()) }
                    .distinctBy { it.id }.sortedWith { a,b -> collator.compare(a.label,b.label) }
            }.onSuccess { icons.evictAll(); apps.value = it; appError.value = false }.onFailure { appError.value = true }
        }
    }
    suspend fun icon(id: String): Bitmap? = withContext(Dispatchers.IO) {
        icons.get(id) ?: runCatching {
            getApplication<Application>().packageManager.getActivityIcon(ComponentName.unflattenFromString(id)!!).toBitmap(96,96).also { icons.put(id,it) }
        }.getOrNull()
    }
    private fun save(action: suspend () -> Unit) = viewModelScope.launch {
        try { action(); settingsError.value = false } catch (_: IOException) { settingsError.value = true }
    }
    fun flag(key: String, value: Boolean) = save { store.flag(key,value) }
    fun profile(value: Profile) = save { store.profile(value) }
    fun favorite(id: String) = save { store.favorite(id) }
    fun deck(url: String, timeout: Int) = save { store.deck(url,timeout) }
}
// An HTTP response proves reachability, not ICARUS identity or authenticated health.
// No redirects, credentials, cookies, analytics, or response body downloads.
suspend fun checkDeck(url: String, seconds: Int): String {
    if (url.isEmpty()) return "NOT CONFIGURED"
    if (!validDeckUrl(url)) return "INVALID URL"
    val client = OkHttpClient.Builder().callTimeout(seconds.toLong(), TimeUnit.SECONDS)
        .connectTimeout(seconds.toLong(), TimeUnit.SECONDS).readTimeout(seconds.toLong(), TimeUnit.SECONDS)
        .followRedirects(false).followSslRedirects(false).build()
    return try {
        suspendCancellableCoroutine { continuation ->
            val call = client.newCall(Request.Builder().url(url).head().build())
            continuation.invokeOnCancellation { call.cancel() }
            call.enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) { if (continuation.isActive) continuation.resume("OFFLINE / UNREACHABLE") }
                override fun onResponse(call: Call, response: Response) {
                    val code = response.use { it.code }
                    if (continuation.isActive) continuation.resume(when(code) {
                        in 200..299 -> "REACHABLE · HTTP $code"
                        in 300..399 -> "REDIRECT · HTTP $code"
                        401,403 -> "AUTH REQUIRED · HTTP $code"
                        else -> "RESPONDED · HTTP $code"
                    })
                }
            })
        }
    } finally { client.connectionPool.evictAll(); client.dispatcher.executorService.shutdown() }
}
