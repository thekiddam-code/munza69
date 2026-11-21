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
    val vault = CredentialVault(app)
    val remote = IcarusClient()
    val instant = InstantController(remote,vault)
    val weather = WeatherRepository(app)
    val widgetHost = WidgetHostController(app)
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
            }.onSuccess { currentCoroutineContext().ensureActive(); icons.evictAll(); apps.value = it; appError.value = false }.onFailure { appError.value = true }
        }
    }
    suspend fun icon(id: String,size: Int=128): Bitmap? = withContext(Dispatchers.IO) {
        icons.get("$id|$size") ?: runCatching {
            getApplication<Application>().packageManager.getActivityIcon(ComponentName.unflattenFromString(id)!!).toBitmap(size,size).also { icons.put("$id|$size",it) }
        }.getOrNull()
    }
    private fun save(action: suspend () -> Unit) = viewModelScope.launch {
        try { action(); settingsError.value = false } catch (_: IOException) { settingsError.value = true } catch (_: IllegalArgumentException) { settingsError.value = true }
    }
    private var arrangementBackup: Config?=null
    val hasLayoutUndo=MutableStateFlow(false)
    fun arrange(transform: (Config)->Config)=save {
        store.update {old->val next=transform(old);arrangementBackup=old;hasLayoutUndo.value=true;next}
    }
    fun undoArrangement()=save {
        val old=arrangementBackup ?: return@save
        store.update {it.copy(gridLayouts=old.gridLayouts,desktop=old.desktop,moduleOrder=old.moduleOrder,hiddenModules=old.hiddenModules,instantOrder=old.instantOrder)}
        arrangementBackup=null;hasLayoutUndo.value=false
    }
    fun saveGrid(surface: String,grid: GridLayout)=arrange {c->
        val ids=grid.cells.map {it.id}.toSet()
        val unknown=c.gridLayouts[surface]?.cells?.filterNot {it.id in ids} ?: emptyList()
        c.copy(gridLayouts=c.gridLayouts+(surface to validateGrid(grid.copy(cells=grid.cells+unknown))))
    }
    fun restoreGridItems(surface: String)=arrange {c->c.copy(gridLayouts=c.gridLayouts+(surface to (c.gridLayouts[surface] ?: GridLayout()).let {it.copy(cells=it.cells.map {cell->cell.copy(hidden=false)})}))}
    fun change(transform: (Config) -> Config) = save { store.update(transform) }
    fun removeDesktopItem(id: String) = save {
        store.update { c->c.copy(desktop=validateDesktop(resolvedDesktop(c,apps.value).removeItem(id))) }
        val latest=store.config.first();widgetHost.releaseUnused(latest.desktop?.pages?.flatMap {it.items}?.mapNotNull {it.widget?.appWidgetId?.takeIf {n->n>0}}?.toSet() ?: emptySet())
    }
    fun completePendingWidget() = save {
        val pending=widgetHost.pending.value ?: return@save
        try {
        require(widgetHost.validBinding(pending.id,pending.provider))
        store.update {c->val layout=resolvedDesktop(c,apps.value);val page=pending.page.takeIf {id->layout.pages.any {it.id==id}} ?: layout.homePageId
            val existing=pending.replaceItem?.let {layout.item(it)}
            val spec=(existing?.widget ?: DesktopWidget(kind="android",span=layout.page(page).columns,rows=kotlin.math.ceil((widgetHost.manager.getAppWidgetInfo(pending.id)?.minHeight ?: 0).toFloat()/getApplication<Application>().resources.displayMetrics.density/64f).toInt().coerceIn(2,6),provider=pending.provider)).copy(appWidgetId=pending.id,provider=pending.provider)
            c.copy(desktop=validateDesktop(if(existing!=null)layout.updateItem(existing.id){it.copy(widget=spec)} else layout.updatePage(page){it.copy(items=it.items+DesktopItem(desktopId(),"widget",widget=spec))}))
        }
        widgetHost.finish()
        widgetHost.releaseUnused(store.config.first().desktop?.pages?.flatMap {it.items}?.mapNotNull {it.widget?.appWidgetId?.takeIf {id->id>0}}?.toSet() ?: emptySet())
        } catch(e: Exception) {widgetHost.cancel();throw e}
    }
    fun editDesktop(change: (DesktopLayout)->DesktopLayout) = save { store.update { c->c.copy(desktop=validateDesktop(change(resolvedDesktop(c,apps.value)))) } }
    fun placeShortcut(component: String,pageId: String?=null) = save {
        store.update { c->
            require(validComponent(component))
            val layout=resolvedDesktop(c,apps.value);val destination=pageId?.takeIf { id->layout.pages.any { it.id==id } } ?: layout.homePageId
            val next=if(layout.page(destination).items.any { it.kind=="app" && it.component==component })layout else layout.updatePage(destination){it.copy(items=it.items+DesktopItem(desktopId(),component=component))}
            c.copy(desktop=validateDesktop(next),favorites=c.favorites+component)
        }
    }
    fun replace(c: Config) = save { store.replace(c);widgetHost.cancel();widgetHost.releaseUnused(c.desktop?.pages?.flatMap {it.items}?.mapNotNull {it.widget?.appWidgetId?.takeIf {id->id>0}}?.toSet() ?: emptySet()) }
    fun reset() = save { vault.clear();store.replace(Config());widgetHost.cancel();widgetHost.releaseUnused(emptySet()) }
    fun flag(key: String, value: Boolean) = save { store.flag(key,value) }
    fun profile(value: Profile) = save { store.profile(value) }
    fun favorite(id: String) = save { store.favorite(id) }
    fun deck(url: String, timeout: Int) = save { store.deck(url,timeout) }
    override fun onCleared() { remote.close();weather.client.close();widgetHost.host.stopListening();super.onCleared() }
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
