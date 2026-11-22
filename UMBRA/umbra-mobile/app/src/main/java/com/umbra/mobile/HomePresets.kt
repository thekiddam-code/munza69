package com.umbra.mobile

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*

@Serializable data class HomePreset(val id: String,val name: String,val desktop: DesktopLayout,val grids: Map<String,GridLayout> = emptyMap())
fun homePresetNames(c: Config): List<Pair<String,String>> = if(c.homePresets.isEmpty())listOf("default" to "Default") else c.homePresets.map {it.id to it.name}
private fun snapshotPreset(c: Config): List<HomePreset> {
    val current=HomePreset(c.activeHomePreset,homePresetNames(c).first {it.first==c.activeHomePreset}.second,resolvedDesktop(c),c.gridLayouts.filterKeys {it.startsWith("home:")})
    return if(c.homePresets.any {it.id==c.activeHomePreset})c.homePresets.map {if(it.id==c.activeHomePreset)current else it} else c.homePresets+current
}
fun switchHomePreset(c: Config,id: String): Config {
    if(id==c.activeHomePreset)return c
    val saved=snapshotPreset(c);val target=saved.first {it.id==id}
    return c.copy(activeHomePreset=id,homePresets=saved,desktop=target.desktop,gridLayouts=c.gridLayouts.filterKeys {!it.startsWith("home:")}+target.grids)
}
fun addHomePreset(c: Config,name: String): Config {
    require(homePresetNames(c).size<8 && name.isNotBlank() && name.length<=48 && name.none(Char::isISOControl))
    val id=desktopId();val page=desktopId()
    val preset=HomePreset(id,name.trim(),DesktopLayout(homePageId=page,pages=listOf(DesktopPage(page,name.trim()))))
    return switchHomePreset(c.copy(homePresets=snapshotPreset(c)+preset),id)
}
fun allNativeWidgetIds(c: Config): Set<Int> = (listOfNotNull(c.desktop)+c.homePresets.filterNot {it.id==c.activeHomePreset}.map {it.desktop}).flatMap {it.pages}.flatMap {it.items}.mapNotNull {it.widget?.appWidgetId?.takeIf {id->id>0}}.toSet()
fun validatePresets(c: Config) {
    require(c.homePresets.size<=8 && c.homePresets.map {it.id}.distinct().size==c.homePresets.size)
    require(if(c.homePresets.isEmpty())c.activeHomePreset=="default" else c.homePresets.any {it.id==c.activeHomePreset})
    c.homePresets.forEach {
        require(Regex("[A-Za-z0-9_-]{1,64}").matches(it.id) && it.name.isNotBlank() && it.name.length<=48 && it.name.none(Char::isISOControl))
        validateDesktop(it.desktop);require(it.grids.size<=12 && it.grids.keys.all {key->key.startsWith("home:") && key.length<=120});it.grids.values.forEach(::validateGrid)
    }
    val bindings=(listOfNotNull(c.desktop)+c.homePresets.filterNot {it.id==c.activeHomePreset}.map {it.desktop}).flatMap {it.pages}.flatMap {it.items}.mapNotNull {it.widget?.appWidgetId?.takeIf {id->id>0}}
    require(bindings.distinct().size==bindings.size)
}
fun validatePresetsJson(value: JsonElement) {
    val rows=value as? JsonArray ?: error("Expected presets");require(rows.size<=8)
    rows.forEach {row->val o=strictFields(row,strings=setOf("id","name"),nested=setOf("desktop","grids"));o["desktop"]?.let(::validateDesktopJson);o["grids"]?.let(::validateGridsJson)}
}
@Composable fun HomePresetBar(c: Config,model: LauncherModel) {
    val editing=LocalGridEditing.current
    var manager by remember {mutableStateOf(false)};var name by remember {mutableStateOf("")}
    Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState())) {
        homePresetNames(c).forEach {(id,label)->FilterChip(selected=id==c.activeHomePreset,onClick={editing.finish();model.switchPreset(id)},label={Text(label)})}
        TextButton(onClick={manager=true}){Text("Presets")}
    }
    if(manager)DesktopEditorDialog("HOME presets",{manager=false},confirm={TextButton(onClick={manager=false}){Text("Done")}}) {
        Text("Each preset keeps its own pages, widget appearance and grid layout.")
        OutlinedTextField(name,{name=it.take(48)},label={Text("New preset name")},singleLine=true)
        Button(onClick={model.addPreset(name);manager=false},enabled=name.isNotBlank() && name.none(Char::isISOControl) && homePresetNames(c).size<8,shape=Chamfer){Text("Create blank preset")}
    }
}

// Engineering collapse lives on the instance, so a resize cannot leave a second
// collapsed flag in the grid that prevents a later expansion.
fun gridForStorage(c: Config,surface: String,grid: GridLayout): GridLayout {
    if(!surface.startsWith("home:"))return grid
    val ids=resolvedDesktop(c).pages.flatMap {it.items}.filter {it.widget?.kind in ENGINEERING_KINDS}.map {it.id}.toSet()
    return grid.copy(cells=grid.cells.map {if(it.id in ids)it.copy(collapsed=false) else it})
}
