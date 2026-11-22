package com.umbra.mobile

import android.app.Activity
import android.appwidget.AppWidgetHost
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProviderInfo
import android.content.ComponentName
import android.content.Context
import android.content.ContextWrapper
import android.content.Intent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.lifecycle.compose.LifecycleStartEffect
import kotlinx.coroutines.flow.MutableStateFlow

data class PendingWidget(val id: Int,val provider: String,val page: String,val replaceItem: String?)
class WidgetHostController(context: Context) {
    val manager=AppWidgetManager.getInstance(context)
    val host=AppWidgetHost(context,0x554d42)
    private val prefs=context.getSharedPreferences("umbra_widget_binding",Context.MODE_PRIVATE)
    val pending=MutableStateFlow(readPending())
    private fun readPending(): PendingWidget? {
        val id=prefs.getInt("id",0);val provider=prefs.getString("provider",null) ?: return null
        return if(id>0)PendingWidget(id,provider,prefs.getString("page","main")!!,prefs.getString("replace",null)) else null
    }
    fun allocate(provider: ComponentName,page: String,replace: String?=null): PendingWidget {
        cancel()
        val p=PendingWidget(host.allocateAppWidgetId(),provider.flattenToString(),page,replace)
        prefs.edit().putInt("id",p.id).putString("provider",p.provider).putString("page",p.page).putString("replace",p.replaceItem).commit()
        pending.value=p;return p
    }
    fun bindIntent(p: PendingWidget)=Intent(AppWidgetManager.ACTION_APPWIDGET_BIND).putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID,p.id).putExtra(AppWidgetManager.EXTRA_APPWIDGET_PROVIDER,ComponentName.unflattenFromString(p.provider))
    fun tryBind(p: PendingWidget)=runCatching {manager.bindAppWidgetIdIfAllowed(p.id,ComponentName.unflattenFromString(p.provider))}.getOrDefault(false)
    fun validBinding(id: Int,provider: String)=runCatching {id in host.appWidgetIds && manager.getAppWidgetInfo(id)?.provider?.flattenToString()==provider}.getOrDefault(false)
    private var listeners=0
    fun acquire(){if(listeners++==0)runCatching {host.startListening()}}
    fun release(){if(listeners>0 && --listeners==0)runCatching {host.stopListening()}}
    fun finish(){prefs.edit().clear().commit();pending.value=null}
    fun cancel(){pending.value?.let {runCatching {host.deleteAppWidgetId(it.id)}};finish()}
    fun releaseUnused(keep: Set<Int>){runCatching {host.appWidgetIds.filter {it !in keep && it!=pending.value?.id}.forEach(host::deleteAppWidgetId)}}
    companion object {const val CONFIGURE_REQUEST=0x5542}
}
fun Context.umbraActivity(): MainActivity? {var current: Context=this;while(current is ContextWrapper){if(current is MainActivity)return current;current=current.baseContext};return current as? MainActivity}
@Composable fun HostedAndroidWidget(item: DesktopItem,model: LauncherModel,visible: Boolean) {
    val context=LocalContext.current;val spec=item.widget!!;val host=model.widgetHost
    var valid by remember(spec.appWidgetId,spec.provider){mutableStateOf(host.validBinding(spec.appWidgetId,spec.provider))}
    val density=LocalDensity.current
    LifecycleStartEffect(visible,host) {
        valid=host.validBinding(spec.appWidgetId,spec.provider)
        if(visible)host.acquire()
        onStopOrDispose {if(visible)host.release()}
    }
    if(!valid)Column(Modifier.fillMaxWidth().height((spec.rows*64).dp).padding(12.dp)) {
        Text("Android widget requires binding",style=MaterialTheme.typography.titleMedium)
        Text(spec.provider.substringBefore('/'),style=MaterialTheme.typography.bodySmall)
        Button(onClick={context.umbraActivity()?.beginWidgetBinding(ComponentName.unflattenFromString(spec.provider)!!,resolvedDesktop(model.config.value).pages.firstOrNull {p->p.items.any {it.id==item.id}}?.id ?: "main",item.id)},shape=Chamfer){Text("Bind widget")}
    } else {
        // No clickable, pointer interception, or custom RemoteViews click handler around this view.
        AndroidView(factory={ctx->host.host.createView(ctx,spec.appWidgetId,host.manager.getAppWidgetInfo(spec.appWidgetId))},
            modifier=Modifier.fillMaxWidth().height(maxOf(spec.rows*64f,with(density){(host.manager.getAppWidgetInfo(spec.appWidgetId)?.minResizeHeight?.takeIf {it>0} ?: 0).toDp().value}).dp),update={view->
                view.post {val width=with(density){view.width.toDp().value.toInt()}.coerceAtLeast(1);val height=with(density){view.height.toDp().value.toInt()}.coerceAtLeast(1)
                    view.updateAppWidgetSize(null,width,height,width,height)}
            })
    }
}
@Composable fun WidgetPicker(c: Config,model: LauncherModel,page: String,close: ()->Unit) {
    val context=LocalContext.current
    var androidPicker by remember {mutableStateOf(false)}
    val providers=remember {runCatching {model.widgetHost.manager.installedProviders.sortedBy {it.loadLabel(context.packageManager).toString()}}.getOrDefault(emptyList())}
    DesktopEditorDialog(if(androidPicker)"Android widget providers" else "Add widget",close,confirm={}) {
        if(androidPicker) {
            if(providers.isEmpty())Text("No widget providers are available in this profile.")
            providers.forEach {provider->TextButton(onClick={context.umbraActivity()?.beginWidgetBinding(provider.provider,page);close()}){Text(provider.loadLabel(context.packageManager).toString())}}
        } else {
            CLOCK_STYLES.forEach {style->TextButton(onClick={model.editDesktop {layout->layout.updatePage(page){it.copy(items=it.items+DesktopItem(desktopId(),"widget",widget=DesktopWidget(style=style,span=it.columns,rows=if(style=="Analog")3 else 2)))}};close()}){Text("Clock · $style")}}
            listOf("weather","battery","calendar","system","icarus","soundboard").forEach {kind->TextButton(onClick={model.editDesktop {layout->layout.updatePage(page){it.copy(items=it.items+DesktopItem(desktopId(),"widget",widget=DesktopWidget(kind=kind,span=it.columns,rows=if(kind in listOf("icarus","soundboard","calendar"))3 else 2)))}};close()}){Text(if(kind=="icarus")"Button widget · choose game or hotkeys" else if(kind=="soundboard")"Soundboard buttons" else kind.replaceFirstChar(Char::uppercase))}}
            ENGINEERING_KINDS.forEach {kind->TextButton(onClick={model.editDesktop {layout->layout.updatePage(page){it.copy(items=it.items+DesktopItem(desktopId(),"widget",widget=DesktopWidget(kind=kind,span=it.columns,rows=3)))}};close()}){Text("Engineering · "+kind.removePrefix("engineering_").uppercase())}}
            TextButton(onClick={androidPicker=true}){Text("Third-party Android widget…")}
        }
    }
}
