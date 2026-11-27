package com.umbra.mobile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable fun FolderEditor(item: DesktopItem?,apps: List<LaunchApp>,c: Config,save: (String,List<String>)->Unit,close: ()->Unit) {
    var name by remember(item?.id){mutableStateOf(item?.folder?.name ?: "Folder")}
    var selected by remember(item?.id){mutableStateOf(item?.folder?.apps ?: emptyList())}
    var search by remember {mutableStateOf("")}
    DesktopEditorDialog(if(item==null)"Create folder" else "Manage folder",close,confirm={TextButton(onClick={save(name.trim(),selected)},enabled=name.isNotBlank() && name.none(Char::isISOControl)){Text("Save folder")}}) {
        OutlinedTextField(name,{name=it.take(48)},label={Text("Folder name")},singleLine=true)
        selected.forEachIndexed {i,id->Row(verticalAlignment=Alignment.CenterVertically) {
            Text(apps.firstOrNull {it.id==id}?.label ?: "Unavailable app",modifier=Modifier.weight(1f))
            TextButton(onClick={selected=moveItem(selected,id,-1)},enabled=i>0){Text("↑")}
            TextButton(onClick={selected=moveItem(selected,id,1)},enabled=i<selected.lastIndex){Text("↓")}
        } }
        OutlinedTextField(search,{search=it},label={Text("Find apps")},singleLine=true)
        apps.filter {it.id !in c.hiddenApps && it.label.contains(search,true)}.forEach {app->
            Row(verticalAlignment=Alignment.CenterVertically){Checkbox(app.id in selected,{checked->selected=if(checked)(selected+app.id).distinct().take(64) else selected-app.id});Text(app.label)}
        }
    }
}
@Composable fun PageManager(layout: DesktopLayout,update: ((DesktopLayout)->DesktopLayout)->Unit,close: ()->Unit) {
    var newName by remember {mutableStateOf("New deck")}
    var editing by remember {mutableStateOf<DesktopPage?>(null)}
    var title by remember {mutableStateOf("")}
    if(editing!=null)AlertDialog(onDismissRequest={editing=null},title={Text("Page name")},text={OutlinedTextField(title,{title=it.take(48)},singleLine=true)},confirmButton={TextButton(onClick={val id=editing!!.id;update{it.updatePage(id){p->p.copy(name=title.trim())}};editing=null},enabled=title.isNotBlank() && title.none(Char::isISOControl)){Text("Rename")}})
    DesktopEditorDialog("Home pages",close,confirm={TextButton(onClick=close){Text("Done")}}) {
        layout.pages.forEachIndexed {i,p->
            Text(p.name+if(layout.homePageId==p.id)" · Home" else "",style=MaterialTheme.typography.titleMedium)
            Row {
                TextButton(onClick={update{it.reorderPage(p.id,-1)}},enabled=i>0){Text("←")}
                TextButton(onClick={update{it.reorderPage(p.id,1)}},enabled=i<layout.pages.lastIndex){Text("→")}
                TextButton(onClick={editing=p;title=p.name}){Text("Rename")}
                TextButton(onClick={update{it.copy(homePageId=p.id)}}){Text("Home")}
            }
            Choice("Columns",(2..8).map(Int::toString),p.columns.toString()){v->update{it.updatePage(p.id){page->page.copy(columns=v.toInt())}}}
            Text("More columns fit on wider pages; buttons retain a usable touch size.",style=MaterialTheme.typography.bodySmall)
            Choice("Page header",listOf("terminal","information","icarus","blank"),p.kind){kind->update{it.updatePage(p.id){page->page.copy(kind=kind)}}}
            TextButton(onClick={update{it.removePage(p.id)}},enabled=layout.pages.size>1){Text("Remove page · move its items to first remaining page")}
            HorizontalDivider()
        }
        OutlinedTextField(newName,{newName=it.take(48)},label={Text("New page name")},singleLine=true)
        Button(onClick={update{it.copy(pages=it.pages+DesktopPage(desktopId(),newName.trim()))}},enabled=layout.pages.size<12 && newName.isNotBlank() && newName.none(Char::isISOControl),shape=Chamfer){Text("Add page")}
    }
}
@Composable fun WidgetEditor(item: DesktopItem,save: (DesktopWidget,Set<String>?)->Unit,remove: ()->Unit,close: ()->Unit,columns: Int=3) {
    var newButton by remember {mutableStateOf<CustomButton?>(null)}
    var widget by remember(item.id){mutableStateOf(item.widget!!.let {if(it.kind in listOf("icarus","soundboard"))it.copy(rows=it.rows.coerceAtLeast(3)) else it})}
    val config=LocalLauncherConfig.current
    val model: LauncherModel=androidx.lifecycle.viewmodel.compose.viewModel()
    var selected by remember(item.id){mutableStateOf(config.widgetButtonSelections[item.id]?.toSet())}
    val context=androidx.compose.ui.platform.LocalContext.current
    val density=androidx.compose.ui.platform.LocalDensity.current
    val provider=remember(item.widget?.appWidgetId){runCatching {android.appwidget.AppWidgetManager.getInstance(context).getAppWidgetInfo(item.widget!!.appWidgetId)}.getOrNull()}
    val minimumRows=provider?.let {info->kotlin.math.ceil(with(density){(info.minResizeHeight.takeIf {it>0} ?: info.minHeight).toDp().value}/64f).toInt().coerceIn(1,12)} ?: if(widget.kind in listOf("icarus","soundboard"))3 else 1
    val canResizeWidth=provider==null || provider.resizeMode and android.appwidget.AppWidgetProviderInfo.RESIZE_HORIZONTAL!=0
    val canResizeHeight=provider==null || provider.resizeMode and android.appwidget.AppWidgetProviderInfo.RESIZE_VERTICAL!=0
    val available=androidx.compose.ui.platform.LocalConfiguration.current.screenWidthDp-40f
    val minimumColumns=provider?.let {info->kotlin.math.ceil(with(density){(info.minResizeWidth.takeIf {it>0} ?: info.minWidth).toDp().value}/(available/columns)).toInt().coerceIn(1,columns)} ?: 1
    DesktopEditorDialog("Widget configuration",close,confirm={TextButton(onClick={save(widget,selected)},enabled=validAccent(widget.accent)){Text("Save widget")}}) {
        if(widget.kind in (ENGINEERING_KINDS+listOf("icarus","soundboard")))Toggle("Collapsed",widget.collapsed){widget=widget.copy(collapsed=it)}
        if(widget.kind in ENGINEERING_KINDS) {
            Toggle("Show sensor details",widget.showDetails){widget=widget.copy(showDetails=it)}
        }
        if(widget.kind in listOf("icarus","soundboard")) {
            Toggle("Fill available page",widget.fillPage){widget=widget.copy(fillPage=it)}
            OutlinedTextField(widget.title,{widget=widget.copy(title=it.take(48))},label={Text("Widget title")},singleLine=true)
            Choice("Button columns",(1..12).map(Int::toString),widget.buttonColumns.toString()){widget=widget.copy(buttonColumns=it.toInt())}
            Text("Up to 12 columns on a wide tablet. Narrow views show fewer columns to keep usable touch targets.",style=MaterialTheme.typography.bodySmall)
            Choice("Button height",listOf("56","64","72","80","96"),widget.buttonHeight.toString()){widget=widget.copy(buttonHeight=it.toInt())}
            if(widget.kind=="icarus") {
                Choice("Button set",BUTTON_SETS.filterNot {it=="favorites"},widget.buttonSet){widget=widget.copy(buttonSet=it);selected=null}
                ButtonSelection(config,model,item.id,widget.buttonSet,selected,{selected=it},widget)
                Text("Choose mixed to put sounds and game/hotkey controls in one grid. Fill available page adapts to the screen without removing other widgets.",style=MaterialTheme.typography.bodySmall)
                TextButton(onClick={newButton=CustomButton(label="New widget button")}){Text("Add custom button")}
            } else {Toggle("Favorites only",widget.buttonSet=="favorites"){widget=widget.copy(buttonSet=if(it)"favorites" else "all")};SoundSelection(config,model,item.id,selected,{selected=it})}
        }
        if(widget.kind=="clock") {
            Choice("Clock style",CLOCK_STYLES,widget.style){widget=widget.copy(style=it)}
            Toggle("24-hour clock",widget.clock24){widget=widget.copy(clock24=it)}
            Toggle("Show seconds",widget.seconds){widget=widget.copy(seconds=it)}
        }
        Choice("Width in columns",(if(canResizeWidth)(minimumColumns..columns).toList() else listOf(widget.span)).map(Int::toString),widget.span.toString()){widget=widget.copy(span=it.toInt())}
        Choice("Height in rows",(if(canResizeHeight)(minimumRows..12).toList() else listOf(widget.rows)).map(Int::toString),widget.rows.toString()){widget=widget.copy(rows=it.toInt())}
        if(widget.kind!="android") {
            Toggle("Transparent background",widget.transparent){widget=widget.copy(transparent=it)}
            OutlinedTextField(widget.accent,{widget=widget.copy(accent=it.take(7))},label={Text("Accent #RRGGBB (empty uses theme)")},singleLine=true,isError=!validAccent(widget.accent))
        } else Text("Provider minimum size and resize support still apply. Native widget clicks are never intercepted for UMBRA expansion.",style=MaterialTheme.typography.bodySmall)
        TextButton(onClick=remove){Text("Remove widget")}
    }
    newButton?.let {button->
        val snapshot by model.instant.state.collectAsState()
        val connection by model.instant.pcConnection.collectAsState()
        ButtonEditor(button,config,snapshot.pc,model,{newButton=null},saveDraft={saved->
            val id="widget:${saved.id}"
            selected=(selected ?: widgetCatalog(config,snapshot.pc,item.id,connection.catalog,widget).map {it.id}.toSet())+id
            widget=widget.copy(buttonOverrides=widget.buttonOverrides+(id to saved));newButton=null
        })
    }
}

// Explicit bounded content avoids intrinsic width/height negotiation between a
// scrollable editor, FlowRow choices, and the platform dialog window.
@Composable fun DesktopEditorDialog(title: String,close: ()->Unit,confirm: @Composable ()->Unit,content: @Composable ColumnScope.()->Unit) {
    val maxHeight=(androidx.compose.ui.platform.LocalConfiguration.current.screenHeightDp*.8f).dp
    androidx.compose.ui.window.Dialog(onDismissRequest=close,properties=androidx.compose.ui.window.DialogProperties(usePlatformDefaultWidth=false)) {
        Surface(modifier=Modifier.widthIn(max=480.dp).fillMaxWidth(.92f).heightIn(max=maxHeight),shape=Chamfer,color=Panel,border=androidx.compose.foundation.BorderStroke(1.dp,MaterialTheme.colorScheme.primary)) {
            Column(Modifier.padding(20.dp),verticalArrangement=Arrangement.spacedBy(12.dp)) {
                Text(title,style=MaterialTheme.typography.titleLarge)
                Column(Modifier.weight(1f,fill=false).fillMaxWidth().verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(8.dp),content=content)
                Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.End) {TextButton(onClick=close){Text("Cancel")};confirm()}
            }
        }
    }
}
