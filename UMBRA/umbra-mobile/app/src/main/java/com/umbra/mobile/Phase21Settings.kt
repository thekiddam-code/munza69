package com.umbra.mobile

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable fun TransitionSettings(c: Config,model: LauncherModel) {
    Text("Transitions",style=MaterialTheme.typography.titleLarge)
    val choices=linkedMapOf(TransitionStyle.SamsungInspired to "Samsung-inspired",TransitionStyle.UmbraCinematic to "UMBRA Cinematic",TransitionStyle.Minimal to "Minimal",TransitionStyle.NativeAndroid to "Native Android")
    Choice("Unified transition style",choices.values.toList(),choices[c.transitionStyle]!!){label->model.change {it.copy(transitionStyle=choices.entries.first {entry->entry.value==label}.key)}}
    Toggle("App launch transitions",c.appLaunchTransitions){v->model.change {it.copy(appLaunchTransitions=v)}}
    Toggle("Folder expansion transitions",c.folderTransitions){v->model.change {it.copy(folderTransitions=v)}}
    Toggle("Widget expansion transitions",c.widgetTransitions){v->model.change {it.copy(widgetTransitions=v)}}
    Toggle("Command Center transitions",c.commandAnimations){v->model.change {it.copy(commandAnimations=v)}}
    Toggle("Terminal panel transitions",c.transitions){v->model.change {it.copy(transitions=v)}}
    Text("Master, intensity, power, and system reduced motion still apply. Native Android delegates external launches to the OS; launcher-owned panels use restrained fades. Samsung may replace third-party launcher activity animations. Visual Detail is independent.",style=MaterialTheme.typography.bodySmall)
    TextButton(onClick={model.change {it.copy(transitionStyle=TransitionStyle.SamsungInspired,appLaunchTransitions=true,folderTransitions=true,widgetTransitions=true,commandAnimations=true,transitions=true)}}){Text("Reset transitions (preserve detail and master)")}
}
@Composable fun OrganizationSettings(c: Config,model: LauncherModel,apps: List<LaunchApp>) {
    Text("Home organization",style=MaterialTheme.typography.titleMedium)
    Text("Home → Pages adds, renames, reorders, removes, or changes the grid of a page. Folder creates a named group. Hold and drag an item: drop in the middle of an app to group, or near its edge to reorder. Hold at a page side to move across pages. Hold and release for an item menu. Android widget management handles stay outside their native view.",style=MaterialTheme.typography.bodySmall)
    Text("Hidden applications",style=MaterialTheme.typography.titleMedium)
    if(c.hiddenApps.isEmpty())Text("No hidden applications.")
    c.hiddenApps.forEach {id->Row {Text(apps.firstOrNull {it.id==id}?.label ?: id.substringBefore('/'),modifier=Modifier.weight(1f));TextButton(onClick={model.change {it.copy(hiddenApps=it.hiddenApps-id)}}){Text("Unhide")}}}
    Text("Drawer order",style=MaterialTheme.typography.titleMedium)
    val ordered=apps.sortedBy {c.drawerOrder.indexOf(it.id).takeIf {n->n>=0} ?: Int.MAX_VALUE}
    ordered.forEachIndexed {i,app->Row(Modifier.fillMaxWidth()) {
        Text(app.label,modifier=Modifier.weight(1f))
        TextButton(onClick={model.change {it.copy(drawerOrder=moveItem(ordered.map {a->a.id},app.id,-1))}},enabled=i>0){Text("↑")}
        TextButton(onClick={model.change {it.copy(drawerOrder=moveItem(ordered.map {a->a.id},app.id,1))}},enabled=i<ordered.lastIndex){Text("↓")}
    } }
    TextButton(onClick={model.change {it.copy(drawerOrder=emptyList())}}){Text("Restore alphabetical drawer order")}
}
