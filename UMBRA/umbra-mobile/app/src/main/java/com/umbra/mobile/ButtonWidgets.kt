package com.umbra.mobile

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.*
import androidx.compose.ui.unit.dp
import kotlinx.serialization.json.*

val BUTTON_SETS=listOf("all","mixed","pc","rocket","fortnite","minecraft","simulation","favorites")
fun widgetSpec(c: Config,id: String): DesktopWidget?=resolvedDesktop(c).item(id)?.widget
fun windowsButtonActions(catalog: JsonObject?): List<InstantAction> {
    if(catalog?.truth("supported")!=true)return emptyList()
    return (catalog["hotkeys"] as? JsonArray)?.mapNotNull {it as? JsonObject}?.mapNotNull {spec->
        val id=spec.literal("id")?.takeIf {it.matches(Regex("[a-z0-9_]{1,64}"))} ?: return@mapNotNull null
        InstantAction("windows:$id",spec.literal("name") ?: id,"api/windows/command",buildJsonObject {put("kind","hotkey");put("id",id);put("requestId",java.util.UUID.randomUUID().toString())})
    } ?: emptyList()
}
fun widgetCatalog(c: Config,pc: PcStatus?,widgetId: String?,windows: JsonObject?=null,specOverride: DesktopWidget?=null): List<InstantAction> {
    val mixed=(specOverride ?: widgetId?.let {widgetSpec(c,it)})?.buttonSet=="mixed"
    val base=buttonCatalog(c,pc)+windowsButtonActions(windows)+(if(mixed)hostButtonActions() else emptyList())
    val overrides=specOverride?.buttonOverrides ?: widgetId?.let {widgetSpec(c,it)?.buttonOverrides} ?: emptyMap()
    return base.map {action->overrides[action.id]?.let {buttonAction(it).copy(id=action.id)} ?: if(widgetId!=null)action.copy(label=c.instantLabels[action.id] ?: action.label) else action}+overrides.filterKeys {base.none {a->a.id==it}}.map {(id,b)->buttonAction(b).copy(id=id)}
}
fun overrideWidgetButton(c: Config,id: String,source: String,button: CustomButton): Config {
    validateButton(button);require(button.kind!=OutputKind.TvKey)
    return c.copy(desktop=resolvedDesktop(c).updateItem(id){item->val w=requireNotNull(item.widget);item.copy(widget=w.copy(buttonOverrides=w.buttonOverrides+(source to button)))})
}
@Composable fun ButtonWidget(item: DesktopItem,c: Config,model: LauncherModel,visible: Boolean,accent: Color,header: Modifier) {
    val w=item.widget!!;var bounds by remember(item.id){mutableStateOf(Rect.Zero)}
    val color=if(w.accent.isBlank())accent else Color(android.graphics.Color.parseColor(w.accent))
    Surface(color=if(w.transparent)Color.Transparent else Panel,shape=androidx.compose.foundation.shape.CutCornerShape(topStart=8.dp,bottomEnd=8.dp),modifier=Modifier.fillMaxSize().onGloballyPositioned {bounds=it.boundsInWindow()}) {
        androidx.compose.material3.MaterialTheme(colorScheme=androidx.compose.material3.MaterialTheme.colorScheme.copy(primary=color)) {
            Column(Modifier.fillMaxSize().padding(6.dp)) {
                val active=visible && bounds.width>1 && bounds.height>1
                if(w.kind=="soundboard")SoundboardScreen(c,model,widgetId=item.id,compact=true,visible=active,headingModifier=header)
                else if(w.buttonSet=="mixed")SoundboardSession(c,model,true,active) {state,run->
                    InstantControls(c,model,active,true,surface="instant-widget:${item.id}",widgetId=item.id,headingModifier=header,soundState=state,runSound=run)
                } else InstantControls(c,model,active,true,surface="instant-widget:${item.id}",widgetId=item.id,headingModifier=header)
            }
        }
    }
}

/** Presentation references only: playback stays on the shared original soundboard controller. */
fun soundButtonActions(catalog: SoundCatalog?): List<InstantAction> = catalog?.sounds?.map {sound->
    InstantAction("sound:${sound.id}",sound.name,"api/sounds/play",buildJsonObject {put("id",sound.id)})
} ?: emptyList()

/** Optional stable references, never another macro binding or audio setting store. */
fun hostButtonActions()=listOf(
    InstantAction("host:arctis","Switch to Arctis","api/sonar/arctis",buildJsonObject {}),
    InstantAction("host:save-clip","Save Clip","api/moments/save-clip",buildJsonObject {})
)
fun defaultWidgetButtonIds(catalog: List<InstantAction>)=catalog.filterNot {it.id.startsWith("host:")}.map {it.id}.toSet()
