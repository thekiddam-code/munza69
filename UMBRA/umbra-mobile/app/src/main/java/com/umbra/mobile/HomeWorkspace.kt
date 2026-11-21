package com.umbra.mobile

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.*
import androidx.compose.foundation.gestures.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.pager.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.boundsInWindow
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.positionInWindow
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.zIndex
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch
import kotlin.math.roundToInt

@OptIn(ExperimentalFoundationApi::class)
@Composable fun HomeWorkspace(c: Config,model: LauncherModel,apps: List<LaunchApp>,device: Device,now: java.time.LocalDateTime,
    motion: MotionPolicy,active: Boolean,homeEvent: Int,accent: Color,homePull: androidx.compose.ui.input.nestedscroll.NestedScrollConnection,
    terminal: @Composable ()->Unit,footer: @Composable ()->Unit) {
    val layout=resolvedDesktop(c,apps)
    var selectedPage by rememberSaveable(key="desktop-selected-page") {mutableStateOf(layout.homePageId)}
    val pager=rememberPagerState(initialPage=layout.pages.indexOfFirst {it.id==selectedPage}.coerceAtLeast(0),pageCount={layout.pages.size})
    val scope=rememberCoroutineScope()
    var handledHomeEvent by rememberSaveable(key="desktop-home-event") {mutableIntStateOf(homeEvent)}
    val expansion=remember {ExpansionState()}
    var contextItem by remember {mutableStateOf<DesktopItem?>(null)}
    var managePages by remember {mutableStateOf(false)}
    var manageFolder by remember {mutableStateOf<DesktopItem?>(null)}
    var addFolder by remember {mutableStateOf(false)}
    var widgetPicker by remember {mutableStateOf(false)}
    var widgetEditor by remember {mutableStateOf<DesktopItem?>(null)}
    var moveTarget by remember {mutableStateOf<DesktopItem?>(null)}
    val bounds=remember {mutableStateMapOf<String,Pair<String,Rect>>()}
    var dragItem by remember {mutableStateOf<DesktopItem?>(null)}
    var cursor by remember {mutableStateOf(Offset.Zero)}
    var dragDistance by remember {mutableFloatStateOf(0f)}
    var hostBounds by remember {mutableStateOf(Rect.Zero)}
    val pageId=layout.pages.getOrNull(pager.currentPage)?.id ?: layout.homePageId
    LaunchedEffect(layout) {
        val live=layout.pages.flatMap {it.items}.map {it.id}.toSet()
        bounds.keys.toList().filterNot {it in live}.forEach {bounds.remove(it)}
    }
    LaunchedEffect(layout.pages.map {it.id},homeEvent) {
        val wanted=if(homeEvent!=handledHomeEvent)layout.homePageId else selectedPage.takeIf {id->layout.pages.any {it.id==id}} ?: layout.homePageId
        pager.scrollToPage(layout.pages.indexOfFirst {it.id==wanted}.coerceAtLeast(0));selectedPage=wanted;handledHomeEvent=homeEvent;expansion.dismissImmediately()
    }
    val latestPages by rememberUpdatedState(layout.pages)
    LaunchedEffect(pager){snapshotFlow {pager.settledPage}.collectLatest { index->latestPages.getOrNull(index)?.let {selectedPage=it.id} }}
    val edge=if(dragItem==null)0 else if(cursor.x<hostBounds.left+40) -1 else if(cursor.x>hostBounds.right-40)1 else 0
    LaunchedEffect(edge,dragItem?.id,pager.currentPage) {
        if(edge!=0){delay(400);val next=(pager.currentPage+edge).coerceIn(0,layout.pages.lastIndex);if(next!=pager.currentPage)pager.scrollToPage(next)}
    }
    fun show(item: DesktopItem,rect: Rect) {expansion.open(item.id,rect,if(item.kind=="folder")TransitionCategory.Folder else TransitionCategory.Widget)}
    fun finishDrop() {
        val moving=dragItem
        if(moving!=null) {
            if(dragDistance<12f)contextItem=moving
            else {
                val hit=bounds.entries.firstOrNull {it.key!=moving.id && it.value.first==pageId && layout.page(pageId).items.any {item->item.id==it.key} && it.value.second.contains(cursor)}
                val target=hit?.let {layout.item(it.key)}
                val center=hit?.value?.second?.let {r->Rect(r.left+r.width*.22f,r.top+r.height*.18f,r.right-r.width*.22f,r.bottom-r.height*.18f).contains(cursor)} ?: false
                model.editDesktop {l->if(moving.kind=="app" && target?.kind in listOf("app","folder") && center)l.groupApps(moving.id,target!!.id) else l.moveItem(moving.id,pageId,target?.id)}
            }
        }
        dragItem=null
    }
    fun dragModifier(item: DesktopItem,sourcePage: String): Modifier=Modifier.onGloballyPositioned {bounds[item.id]=sourcePage to it.boundsInWindow()}.semantics {
        onLongClick("Manage Home item"){contextItem=item;true}
    }
    val currentLayout by rememberUpdatedState(layout)
    val currentPage by rememberUpdatedState(pageId)
    val endDrag by rememberUpdatedState<()->Unit>({finishDrop()})
    val rootDrag=Modifier.pointerInput(Unit) {
        awaitEachGesture {
            val down=awaitFirstDown(requireUnconsumed=false)
            if(expansion.selected!=null)return@awaitEachGesture
            val at=hostBounds.topLeft+down.position
            val hit=bounds.entries.firstOrNull {it.value.first==currentPage && currentLayout.page(currentPage).items.any {item->item.id==it.key} && it.value.second.contains(at)} ?: return@awaitEachGesture
            val item=currentLayout.item(hit.key) ?: return@awaitEachGesture
            val held=awaitLongPressOrCancellation(down.id) ?: return@awaitEachGesture
            dragItem=item;dragDistance=0f;cursor=hostBounds.topLeft+held.position
            // Once a long press owns a desktop drag, consume movement in Initial so
            // the child pager/scroll container cannot steal it. Native widget bodies
            // are not registered in bounds and never enter this path.
            var ended=false
            while(true) {
                val event=awaitPointerEvent(androidx.compose.ui.input.pointer.PointerEventPass.Initial)
                val change=event.changes.firstOrNull {it.id==held.id} ?: break
                if(!change.pressed){change.consume();ended=true;break}
                val delta=change.position-change.previousPosition
                cursor=hostBounds.topLeft+change.position;dragDistance+=delta.getDistance();change.consume()
            }
            if(ended)endDrag() else dragItem=null
        }
    }
    Box(Modifier.fillMaxSize().then(rootDrag).onGloballyPositioned {hostBounds=it.boundsInWindow()}) {
        Column(Modifier.fillMaxSize()) {
            Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceBetween,verticalAlignment=Alignment.CenterVertically) {
                Text(layout.page(pageId).name,style=MaterialTheme.typography.labelLarge,modifier=Modifier.weight(1f))
                TextButton(onClick={addFolder=true}){Text("Folder")}
                TextButton(onClick={widgetPicker=true}){Text("Widget")}
                TextButton(onClick={managePages=true}){Text("Pages")}
            }
            HorizontalPager(state=pager,key={layout.pages[it].id},modifier=Modifier.weight(1f).fillMaxWidth().testTag("home-pages"),beyondViewportPageCount=0) { index ->
                val page=layout.pages[index]
                Column(Modifier.fillMaxSize().then(if(page.kind=="terminal")Modifier.nestedScroll(homePull) else Modifier).verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy((5+c.density*3).dp)) {
                    if(page.kind=="terminal")terminal()
                    val visible=page.items.filterNot {it.kind=="app" && it.component in c.hiddenApps}
                    if(visible.isEmpty())Text("Long-press an app in Apps to add a shortcut. Add folders or widgets above.",color=Muted)
                    desktopRows(visible,page.columns).forEach {row->
                        Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(6.dp),verticalAlignment=Alignment.Top) {
                            row.forEach { item ->
                                val span=if(item.kind=="widget")item.widget!!.span.coerceAtMost(page.columns) else 1
                                Box(Modifier.weight(span.toFloat()).then(if(item.widget?.kind=="android")Modifier else dragModifier(item,page.id))) {
                                    when(item.kind) {
                                        "app" -> {
                                            val app=apps.firstOrNull {it.id==item.component}
                                            if(app!=null)AppTile(app.copy(label=c.quickLabels[app.id] ?: app.label),model,app.id in c.favorites,{}, {model.favorite(app.id)},accent,desktopGesture=true)
                                            else TextButton(onClick={contextItem=item}){Text("Unavailable app")}
                                        }
                                        "folder" -> FolderTile(item,apps,model,accent,{rect->show(item,rect)})
                                        else -> Column {
                                            BuiltinWidget(item,c,model,device,now,accent,active && device.screenOn && index==pager.currentPage && expansion.selected==null && widgetEditor==null && contextItem==null && !managePages && !widgetPicker && !addFolder && manageFolder==null && moveTarget==null,{rect->show(item,rect)})
                                            TextButton(onClick={widgetEditor=item},modifier=if(item.widget!!.kind=="android")dragModifier(item,page.id) else Modifier){Text("Widget options")}
                                        }
                                    }
                                }
                            }
                            val used=row.sumOf {if(it.kind=="widget")it.widget!!.span.coerceAtMost(page.columns) else 1}
                            if(used<page.columns)Spacer(Modifier.weight((page.columns-used).toFloat()))
                        }
                    }
                    if(page.kind=="terminal")footer()
                    Spacer(Modifier.height(12.dp))
                }
            }
            Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()),horizontalArrangement=Arrangement.Center) {
                layout.pages.forEachIndexed { index,p-> TextButton(onClick={scope.launch {if(motion.enabled && c.transitionStyle!=TransitionStyle.Minimal)pager.animateScrollToPage(index) else pager.scrollToPage(index)}},contentPadding=PaddingValues(4.dp),modifier=Modifier.heightIn(min=48.dp).testTag("page-${p.id}").semantics {contentDescription="${p.name}, page ${index+1} of ${layout.pages.size}"}){Text(if(index==pager.currentPage)"●" else "○",color=if(index==pager.currentPage)accent else Muted)} }
            }
        }
        dragItem?.let {item->
            Text(item.folder?.name ?: apps.firstOrNull {it.id==item.component}?.label ?: "Move item",color=accent,modifier=Modifier.zIndex(8f).absoluteOffset{IntOffset((cursor.x-hostBounds.left).roundToInt(),(cursor.y-hostBounds.top).roundToInt())}.background(Panel).padding(8.dp))
        }
        val expanded=expansion.selected?.let {layout.item(it)}
        if(expanded!=null)OriginExpansionHost(expansion,c,motion,expanded.folder?.name ?: "Widget details") {
            if(expanded.folder!=null)FolderContents(expanded,apps,model,c,accent,{manageFolder=expanded})
            else WidgetDetails(expanded,c,model,device,now,accent,{widgetEditor=expanded})
        }
    }
    if(contextItem!=null) {
        val item=layout.item(contextItem!!.id)
        if(item==null)contextItem=null
        else AlertDialog(onDismissRequest={contextItem=null},title={Text(item.folder?.name ?: apps.firstOrNull {it.id==item.component}?.label ?: "Desktop item")},text={
            Column {
                if(item.kind=="app") {
                    TextButton(onClick={model.favorite(item.component);contextItem=null}){Text(if(item.component in c.favorites)"Remove favorite" else "Add favorite")}
                    TextButton(onClick={model.change {it.copy(hiddenApps=it.hiddenApps+item.component)};contextItem=null}){Text("Hide application")}
                }
                if(item.kind=="folder")TextButton(onClick={manageFolder=item;contextItem=null}){Text("Rename / manage folder")}
                if(item.kind=="widget")TextButton(onClick={widgetEditor=item;contextItem=null}){Text("Resize / configure widget")}
                TextButton(onClick={moveTarget=item;contextItem=null}){Text("Move to another page")}
                TextButton(onClick={model.editDesktop {it.moveItem(item.id,pageId,layout.page(pageId).items.firstOrNull()?.id)};contextItem=null}){Text("Move to start of this page")}
                TextButton(onClick={model.removeDesktopItem(item.id);contextItem=null}){Text(if(item.kind=="folder")"Delete folder (apps stay installed)" else "Remove from Home")}
            }
        },confirmButton={TextButton(onClick={contextItem=null}){Text("Close")}})
    }
    if(moveTarget!=null)AlertDialog(onDismissRequest={moveTarget=null},title={Text("Move to page")},text={Column {layout.pages.forEach {p->TextButton(onClick={val id=moveTarget!!.id;model.editDesktop {it.moveItem(id,p.id)};moveTarget=null}){Text(p.name)}}}},confirmButton={TextButton(onClick={moveTarget=null}){Text("Cancel")}})
    if(addFolder || manageFolder!=null)FolderEditor(manageFolder,apps,c,{name,ids->
        val existing=manageFolder
        model.editDesktop {l->if(existing!=null)l.updateItem(existing.id){it.copy(folder=DesktopFolder(name,ids))} else l.updatePage(pageId){p->p.copy(items=p.items.filterNot {it.kind=="app" && it.component in ids}+DesktopItem(desktopId(),"folder",folder=DesktopFolder(name,ids)))}}
        manageFolder=null;addFolder=false
    },{manageFolder=null;addFolder=false})
    if(managePages)PageManager(layout,{model.editDesktop(it)},{managePages=false})
    if(widgetPicker)WidgetPicker(c,model,pageId,{widgetPicker=false})
    widgetEditor?.let {edited->WidgetEditor(edited,{updated->model.editDesktop {it.updateItem(edited.id){old->old.copy(widget=updated)}};widgetEditor=null},{model.removeDesktopItem(edited.id);widgetEditor=null},{widgetEditor=null},columns=layout.pages.firstOrNull {p->p.items.any {it.id==edited.id}}?.columns ?: 3)}
}
fun desktopRows(items: List<DesktopItem>,columns: Int): List<List<DesktopItem>> {
    val rows=mutableListOf<MutableList<DesktopItem>>();var used=0
    items.forEach {item->val span=if(item.kind=="widget")item.widget!!.span.coerceAtMost(columns) else 1
        if(rows.isEmpty() || used+span>columns){rows.add(mutableListOf());used=0}
        rows.last().add(item);used+=span
    };return rows
}
@Composable private fun FolderTile(item: DesktopItem,apps: List<LaunchApp>,model: LauncherModel,accent: Color,open: (Rect)->Unit) {
    var iconBounds by remember {mutableStateOf(Rect.Zero)}
    Column(Modifier.fillMaxWidth().clickable {open(iconBounds)}.padding(8.dp).testTag("folder-${item.id}"),horizontalAlignment=Alignment.CenterHorizontally) {
        Box(Modifier.size(LocalLauncherConfig.current.iconSize.dp).onGloballyPositioned {iconBounds=it.boundsInWindow()}.background(accent.copy(alpha=.08f),androidx.compose.foundation.shape.CutCornerShape(4.dp)),contentAlignment=Alignment.Center) {
            Text("▦",color=accent,style=MaterialTheme.typography.headlineMedium)
        }
        Text(item.folder!!.name,maxLines=2,modifier=Modifier.heightIn(min=36.dp),textAlign=androidx.compose.ui.text.style.TextAlign.Center)
    }
}
@Composable private fun FolderContents(item: DesktopItem,apps: List<LaunchApp>,model: LauncherModel,c: Config,accent: Color,manage: ()->Unit) {
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(8.dp)) {
        TextButton(onClick=manage){Text("Manage folder")}
        if(item.folder!!.apps.isEmpty())Text("Folder is empty. Add apps in Manage folder.",color=Muted)
        item.folder.apps.filterNot {it in c.hiddenApps}.chunked(3).forEach {row->Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(4.dp)) {
            row.forEach {id->Box(Modifier.weight(1f)){apps.firstOrNull {it.id==id}?.let {app->AppTile(app,model,id in c.favorites,{}, {model.favorite(id)},accent)}}};repeat(3-row.size){Spacer(Modifier.weight(1f))}
        } }
    }
}
