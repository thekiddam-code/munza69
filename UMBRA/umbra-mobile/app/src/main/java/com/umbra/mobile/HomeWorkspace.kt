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
    onPageContext: (String)->Unit={},terminal: @Composable ()->Unit,footer: @Composable ()->Unit) {
    val layout=resolvedDesktop(c,apps)
    val editSession=LocalGridEditing.current
    var selectedPage by rememberSaveable {mutableStateOf(layout.homePageId)}
    val pager=rememberPagerState(initialPage=layout.pages.indexOfFirst {it.id==selectedPage}.coerceAtLeast(0),pageCount={layout.pages.size})
    val scope=rememberCoroutineScope();val expansion=remember {ExpansionState()}
    var homeMenu by remember {mutableStateOf(false)};var pagesEditor by remember {mutableStateOf(false)}
    var folderEditor by remember {mutableStateOf<DesktopItem?>(null)};var newFolder by remember {mutableStateOf(false)}
    var widgetPage by remember {mutableStateOf<String?>(null)};var widgetEditor by remember {mutableStateOf<DesktopItem?>(null)}
    var appEditor by remember {mutableStateOf<DesktopItem?>(null)};var moveTarget by remember {mutableStateOf<DesktopItem?>(null)}
    var handledEvent by rememberSaveable {mutableIntStateOf(homeEvent)}
    val pageId=layout.pages.getOrNull(pager.currentPage)?.id ?: layout.homePageId
    val latestPages by rememberUpdatedState(layout.pages)
    LaunchedEffect(pager){snapshotFlow {pager.settledPage}.collectLatest {latestPages.getOrNull(it)?.let {p->selectedPage=p.id;onPageContext(when(p.kind){"terminal"->"Main Home";"icarus"->"ICARUS";else->"Information Deck"})}}}
    LaunchedEffect(layout.pages.map {it.id},homeEvent) {
        val target=if(homeEvent!=handledEvent)layout.homePageId else selectedPage.takeIf {id->layout.pages.any {it.id==id}} ?: layout.homePageId
        pager.scrollToPage(layout.pages.indexOfFirst {it.id==target}.coerceAtLeast(0));handledEvent=homeEvent;selectedPage=target;expansion.dismissImmediately()
    }
    fun configure(item: DesktopItem) {when(item.kind){"folder"->folderEditor=item;"widget"->widgetEditor=item;else->appEditor=item}}
    Box(Modifier.fillMaxSize().semantics {onLongClick("Edit Home"){homeMenu=true;true}}) {
        Column(Modifier.fillMaxSize()) {
            Text(layout.page(pageId).name,style=MaterialTheme.typography.labelLarge,modifier=Modifier.fillMaxWidth().heightIn(min=48.dp).combinedClickable(onClick={},onLongClick={homeMenu=true}).testTag("home-edit-header"))
            HorizontalPager(state=pager,key={layout.pages[it].id},modifier=Modifier.weight(1f).fillMaxWidth().testTag("home-pages"),beyondViewportPageCount=1) {index->
                val page=layout.pages[index]
                Column(Modifier.fillMaxSize().then(if(page.kind=="terminal")Modifier.nestedScroll(homePull) else Modifier).verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(10.dp)) {
                    if(page.kind=="terminal")terminal()
                    val visible=page.items.filterNot {it.kind=="app" && it.component in c.hiddenApps}
                    if(visible.isEmpty())Text("Long-press the page title to add widgets, folders, or pages. Long-press apps in Apps to pin them.",color=Muted)
                    GridBoard("home:${page.id}",visible.map {GridItem(it.id,it.folder?.name ?: apps.firstOrNull {a->a.id==it.component}?.label ?: it.widget?.kind ?: "Application",it.widget?.span ?: 1,it.widget?.rows ?: 2)},c,model,page.columns,64.dp,
                        onConfigure={id->layout.item(id)?.let(::configure)},onMovePage={id->moveTarget=layout.item(id)},onResizeRequest={id->val native=layout.item(id)?.takeIf {it.widget?.kind=="android"};if(native!=null){widgetEditor=native;true} else false},onRemove={model.removeDesktopItem(it)},
                        canDuplicate={layout.item(it)?.widget?.kind!="android"},onDuplicate={id->model.arrange {old->val l=resolvedDesktop(old,apps);val item=l.item(id)!!;require(item.widget?.kind!="android");val copyId=desktopId();old.copy(desktop=l.updatePage(page.id){it.copy(items=it.items+item.copy(id=copyId))},widgetButtonSelections=old.widgetButtonSelections[item.id]?.let {ids->old.widgetButtonSelections+(copyId to ids)} ?: old.widgetButtonSelections)}},
                        onDrop={id,target->
                            val moving=layout.item(id);val targetItem=target?.let {layout.item(it)}
                            if(page.id!=pageId){model.arrange {it.copy(desktop=resolvedDesktop(it,apps).moveItem(id,pageId))};editSession.surface="home:$pageId";true}
                            else if(moving?.kind=="app" && targetItem?.kind in listOf("app","folder")){model.arrange {it.copy(desktop=resolvedDesktop(it,apps).groupApps(id,targetItem!!.id))};true}
                            else false
                        },onEdge={edge->scope.launch {pager.scrollToPage((pager.currentPage+edge).coerceIn(0,layout.pages.lastIndex))}},
                        onResize={id,w,h->model.editDesktop {it.updateItem(id){item->if(item.widget!=null)item.copy(widget=item.widget.copy(span=w.coerceAtMost(5),rows=h.coerceAtMost(6))) else item}}}) {entry,_->
                        val item=visible.first {it.id==entry.id}
                        when(item.kind) {
                            "app"->{val app=apps.firstOrNull {it.id==item.component};if(app!=null)AppTile(app.copy(label=c.quickLabels[app.id] ?: app.label),model,app.id in c.favorites,{}, {model.favorite(app.id)},accent,desktopGesture=true) else TextButton(onClick={configure(item)}){Text("Unavailable app")}}
                            "folder"->FolderTile(item,apps,model,accent,{rect->expansion.open(item.id,rect,TransitionCategory.Folder)})
                            else->BuiltinWidget(item,c,model,device,now,accent,active && device.screenOn && index==pager.currentPage && expansion.selected==null && LocalGridEditing.current.surface==null && widgetEditor==null && folderEditor==null && !pagesEditor && !homeMenu,{rect->expansion.open(item.id,rect,TransitionCategory.Widget)})
                        }
                    }
                    if(page.kind=="terminal")footer()
                }
            }
            Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()),horizontalArrangement=Arrangement.Center) {
                layout.pages.forEachIndexed {i,p->TextButton(onClick={selectedPage=p.id;pager.requestScrollToPage(i)},modifier=Modifier.testTag("page-${p.id}").semantics {contentDescription="${p.name}, page ${i+1}"}){Text(if(i==pager.currentPage)"●" else "○",color=if(i==pager.currentPage)accent else Muted)}}
            }
        }
        val item=expansion.selected?.let {layout.item(it)}
        if(item!=null)OriginExpansionHost(expansion,c,motion,item.folder?.name ?: "Widget details") {
            if(item.folder!=null)FolderContents(item,apps,model,c,accent,{folderEditor=item}) else WidgetDetails(item,c,model,device,now,accent,{widgetEditor=item})
        }
    }
    if(homeMenu)DesktopEditorDialog("Edit Home",{homeMenu=false},confirm={TextButton(onClick={homeMenu=false}){Text("Done")}}) {
        TextButton(onClick={homeMenu=false;newFolder=true}){Text("Add folder")}
        TextButton(onClick={homeMenu=false;widgetPage=pageId}){Text("Add widget")}
        TextButton(onClick={homeMenu=false;pagesEditor=true}){Text("Home pages")}
        TextButton(onClick={model.restoreGridItems("home:$pageId");homeMenu=false}){Text("Restore hidden items")}
        TextButton(onClick={model.undoArrangement();homeMenu=false}){Text("Undo arrangement")}
    }
    if(pagesEditor)PageManager(layout,{model.arrange {old->old.copy(desktop=it(resolvedDesktop(old,apps)))}},{pagesEditor=false})
    if(newFolder || folderEditor!=null)FolderEditor(folderEditor,apps,c,{name,ids->val edited=folderEditor
        model.arrange {old->
            val l=resolvedDesktop(old,apps)
            val next=if(edited!=null)l.updateItem(edited.id){it.copy(folder=DesktopFolder(name,ids))}
                else l.updatePage(pageId){page->page.copy(items=page.items.filterNot {item->item.kind=="app" && item.component in ids}+DesktopItem(desktopId(),"folder",folder=DesktopFolder(name,ids)))}
            old.copy(desktop=next)
        }
        folderEditor=null;newFolder=false
    },{folderEditor=null;newFolder=false})
    widgetPage?.let {destination->WidgetPicker(c,model,destination,{widgetPage=null})}
    widgetEditor?.let {edited->WidgetEditor(edited,{spec->model.editDesktop {it.updateItem(edited.id){old->old.copy(widget=spec)}};widgetEditor=null},{model.removeDesktopItem(edited.id);widgetEditor=null},{widgetEditor=null},layout.page(pageId).columns)}
    appEditor?.let {item->DesktopEditorDialog("Application",{appEditor=null},confirm={TextButton(onClick={appEditor=null}){Text("Done")}}) {
        TextButton(onClick={model.favorite(item.component)}){Text("Toggle favorite")}
        TextButton(onClick={moveTarget=item;appEditor=null}){Text("Move to another page")}
        TextButton(onClick={model.change {it.copy(hiddenApps=it.hiddenApps+item.component)};appEditor=null}){Text("Hide")}
        TextButton(onClick={model.removeDesktopItem(item.id);appEditor=null}){Text("Remove shortcut")}
    }}
    moveTarget?.let {item->DesktopEditorDialog("Move to page",{moveTarget=null},confirm={}){layout.pages.forEach {p->TextButton(onClick={model.arrange {it.copy(desktop=resolvedDesktop(it,apps).moveItem(item.id,p.id))};moveTarget=null}){Text(p.name)}}}}
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
@OptIn(ExperimentalFoundationApi::class)
@Composable private fun FolderContents(item: DesktopItem,apps: List<LaunchApp>,model: LauncherModel,c: Config,accent: Color,manage: ()->Unit) {
    Column(Modifier.fillMaxSize().combinedClickable(onClick={},onLongClick=manage).semantics {onLongClick("Configure folder"){manage();true}}.verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(8.dp)) {
        if(item.folder!!.apps.isEmpty())Text("Folder is empty. Long-press its icon or this panel to configure.",color=Muted)
        item.folder.apps.filterNot {it in c.hiddenApps}.chunked(3).forEach {row->Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.spacedBy(4.dp)) {
            row.forEach {id->Box(Modifier.weight(1f)){apps.firstOrNull {it.id==id}?.let {app->AppTile(app,model,id in c.favorites,{}, {model.favorite(id)},accent)}}};repeat(3-row.size){Spacer(Modifier.weight(1f))}
        } }
    }
}
