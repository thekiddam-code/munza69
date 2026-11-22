package com.umbra.mobile

import androidx.activity.compose.BackHandler
import androidx.compose.foundation.*
import androidx.compose.foundation.gestures.*
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment
import androidx.compose.ui.geometry.*
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.*
import androidx.compose.ui.layout.*
import androidx.compose.ui.platform.*
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.*
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.zIndex
import kotlin.math.roundToInt

class GridEditSession {
    var surface by mutableStateOf<String?>(null)
    var selected by mutableStateOf<String?>(null)
    var dragOwner by mutableStateOf<String?>(null)
    var options: (()->Unit)?=null
    fun finish(){surface=null;selected=null;dragOwner=null;options=null}
}
val LocalGridEditing=staticCompositionLocalOf {GridEditSession()}
class GridItemScope(val headerModifier: Modifier)

@Composable fun GridBoard(surface: String,items: List<GridItem>,c: Config,model: LauncherModel,columns: Int=c.deckColumns,
    cellHeight: Dp=72.dp,compact: Boolean=false,forcedCollapsed: Set<String> = emptySet(),
    onConfigure: ((String)->Unit)?=null,onRemove: ((String)->Unit)?=null,onDuplicate: ((String)->Unit)?=null,
    onDrop: ((String,String?)->Boolean)?=null,onEdge: ((Int)->Unit)?=null,onResize: ((String,Int,Int)->Unit)?=null,onResizeRequest: ((String)->Boolean)?=null,onMovePage: ((String)->Unit)?=null,onCollapse: ((String)->Unit)?=null,canDuplicate: (String)->Boolean={true},canCollapse: (String)->Boolean={true},
    content: @Composable GridItemScope.(GridItem,GridCell)->Unit) {
    val session=LocalGridEditing.current
    val haptic=LocalHapticFeedback.current
    val scope=rememberCoroutineScope()
    val rects=remember {mutableStateMapOf<String,Rect>()}
    var origin by remember {mutableStateOf(Offset.Zero)}
    var dragging by remember {mutableStateOf<String?>(null)}
    var pointer by remember {mutableStateOf(Offset.Zero)}
    var distance by remember {mutableFloatStateOf(0f)}
    var menu by remember {mutableStateOf<String?>(null)}
    var resize by remember {mutableStateOf<String?>(null)}
    var viewport by remember {mutableStateOf(Rect.Zero)}
    val latestItems by rememberUpdatedState(items)
    val latestDrop by rememberUpdatedState(onDrop)
    val latestEdge by rememberUpdatedState(onEdge)
    val hapticsEnabled by rememberUpdatedState(c.editHaptics)
    val editing=session.surface==surface
    SideEffect {if(editing)session.options={menu=session.selected}}
    DisposableEffect(surface){onDispose {if(session.surface==surface)session.finish()}}
    LaunchedEffect(session.surface){if(session.surface!=surface){dragging=null;resize=null;menu=null}}
    BackHandler(editing){session.finish();menu=null;resize=null;dragging=null}
    LaunchedEffect(items.map {it.id}) {rects.keys.toList().filterNot {id->items.any {it.id==id}}.forEach {rects.remove(it)}}
    val edge=if(dragging==null || onEdge==null)0 else if(pointer.x<viewport.left+24)-1 else if(pointer.x>viewport.right-24)1 else 0
    LaunchedEffect(edge,dragging) {if(edge!=0){kotlinx.coroutines.delay(450);latestEdge?.invoke(edge)}}
    fun edit(id: String) {session.surface=surface;session.selected=id;menu=id}
    val editNow by rememberUpdatedState<(String)->Unit>({edit(it)})
    Column(Modifier.fillMaxWidth().testTag("grid-$surface")) {
        BoxWithConstraints(Modifier.fillMaxWidth().onGloballyPositioned {viewport=it.boundsInWindow()}) {
            val density=LocalDensity.current
            val desiredColumns=if(maxWidth>600.dp)(columns*2).coerceAtMost(8) else columns
            val actualColumns=desiredColumns.coerceAtMost((maxWidth.value/54f).toInt().coerceAtLeast(1))
            val layout=remember(items,c.gridLayouts[surface],actualColumns,compact,forcedCollapsed){resolveGrid(items,c.gridLayouts[surface],actualColumns,compact,forcedCollapsed)}
            val currentLayout by rememberUpdatedState(layout)
            val cellWidth=maxWidth/actualColumns
            val screenHeight=with(density){LocalConfiguration.current.screenHeightDp.dp.toPx()}
            val cw=with(density){cellWidth.toPx()};val ch=with(density){cellHeight.toPx()}
            val currentWidth by rememberUpdatedState(cw);val currentHeight by rememberUpdatedState(ch)
            fun save(layout: GridLayout) {
                val old=c.gridLayouts[surface]
                val cells=layout.cells.map {cell->
                    val previous=old?.cells?.firstOrNull {it.id==cell.id}
                    if((cell.collapsed || cell.id in forcedCollapsed) && cell.id!=resize)cell.copy(h=previous?.h ?: items.first {it.id==cell.id}.height) else cell
                }
                model.saveGrid(surface,layout.copy(cells=cells))
            }
            val saveNow by rememberUpdatedState<(GridLayout)->Unit>({save(it)})
            val dragInput=Modifier.pointerInput(surface) {
                awaitEachGesture {
                    val down=awaitFirstDown(requireUnconsumed=false)
                    val at=origin+down.position
                    val hit=rects.entries.firstOrNull {e->latestItems.any {it.id==e.key} && currentLayout.cells.any {it.id==e.key && !it.hidden} && e.value.contains(at)} ?: run {
                        if(session.surface==surface)session.finish()
                        return@awaitEachGesture
                    }
                    val held=awaitLongPressOrCancellation(down.id) ?: return@awaitEachGesture
                    if(session.dragOwner!=null && session.dragOwner!=surface)return@awaitEachGesture
                    session.dragOwner=surface;session.surface=surface;session.selected=hit.key
                    dragging=hit.key;pointer=origin+held.position;distance=0f
                    if(hapticsEnabled)haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.LongPress)
                    var released=false
                    try {
                        while(true) {
                            val event=awaitPointerEvent(PointerEventPass.Initial)
                            val change=event.changes.firstOrNull {it.id==held.id} ?: break
                            pointer=origin+change.position
                            if(!change.pressed){change.consume();released=true;break}
                            distance+=(change.position-change.previousPosition).getDistance();change.consume()
                        }
                        if(released && session.surface==surface && session.dragOwner==surface) {
                            if(distance<viewConfiguration.touchSlop)editNow(hit.key)
                            else {
                                val target=rects.entries.firstOrNull {it.key!=hit.key && latestItems.any {item->item.id==it.key} && it.value.contains(pointer)}?.key
                                val handled=latestDrop?.invoke(hit.key,target)==true
                                if(handled && target!=null)session.selected=target
                                if(!handled) {
                                    val current=currentLayout
                                    val selected=current.cells.first {it.id==hit.key}
                                    val x=((pointer.x-origin.x)/currentWidth-selected.w/2f).roundToInt().coerceIn(0,current.columns-selected.w)
                                    val y=((pointer.y-origin.y)/currentHeight-.5f).roundToInt().coerceAtLeast(0)
                                    saveNow(relocateGrid(current,hit.key,x,y))
                                }
                            }
                        }
                    } finally {dragging=null;session.dragOwner=null}
                }
            }
            val rows=(layout.cells.filterNot {it.hidden}.maxOfOrNull {it.y+it.h} ?: 1)+if(dragging!=null || resize!=null)2 else 0
            Box(Modifier.fillMaxWidth().height(cellHeight*rows).then(dragInput).onGloballyPositioned {origin=it.positionInWindow()}) {
                if(editing && (dragging!=null || resize!=null))Canvas(Modifier.matchParentSize().testTag("placement-highlights-$surface")) {
                    for(row in ((-origin.y/ch).toInt()-2).coerceAtLeast(0)..((screenHeight-origin.y)/ch+2).toInt().coerceAtMost(rows-1)) {repeat(actualColumns) {col->
                        val candidate=GridCell("preview",col,row)
                        val free=layout.cells.none {it.id!=dragging && !it.hidden && intersects(candidate,it)}
                        if(free) {
                            drawRect(Amber.copy(alpha=.10f),Offset(col*cw+3,row*ch+3),Size(cw-6,ch-6))
                            drawRect(Amber.copy(alpha=.4f),Offset(col*cw+3,row*ch+3),Size(cw-6,ch-6),style=Stroke(1.dp.toPx()))
                        }
                    }}
                }
                layout.cells.filter { !it.hidden && (it.id==dragging || (origin.y+(it.y+it.h)*ch> -ch*2 && origin.y+it.y*ch<screenHeight+ch*2)) }.forEach {cell->
                    key(cell.id) {
                    DisposableEffect(cell.id){onDispose {rects.remove(cell.id)}}
                    val item=items.first {it.id==cell.id}
                    val registration=Modifier.onGloballyPositioned {rects[item.id]=it.boundsInWindow()}.semantics {
                        onLongClick("Edit ${item.title}"){edit(item.id);true}
                        customActions=listOf(
                            CustomAccessibilityAction("Move earlier"){saveNow(relocateGrid(currentLayout,item.id,cell.x,(cell.y-1).coerceAtLeast(0)));true},
                            CustomAccessibilityAction("Move later"){saveNow(relocateGrid(currentLayout,item.id,cell.x,cell.y+1));true})
                    }
                    Box(Modifier.absoluteOffset(x=cellWidth*cell.x,y=cellHeight*cell.y).size(cellWidth*cell.w,cellHeight*cell.h)
                        .padding(3.dp).clipToBounds().then(if(item.headerOnly)Modifier else registration).testTag("grid-item-$surface-${item.id}")
                        .then(if(dragging==cell.id)Modifier.border(1.dp,Amber) else Modifier)) {
                        GridItemScope(if(item.headerOnly)registration else Modifier).content(item,cell)
                    }
                    }
                }
                if(dragging!=null)Text(items.firstOrNull {it.id==dragging}?.title ?: "Move",color=Amber,modifier=Modifier.zIndex(10f).absoluteOffset {IntOffset((pointer.x-origin.x).roundToInt(),(pointer.y-origin.y).roundToInt())}.background(Panel).padding(6.dp))
            }
            if(menu!=null) {
                val id=menu!!;val cell=layout.cells.firstOrNull {it.id==id}
                if(cell!=null)DesktopEditorDialog(items.firstOrNull {it.id==id}?.title ?: "Arrange",{menu=null},confirm={TextButton(onClick={menu=null;session.finish()}){Text("Done")}}) {
                    onConfigure?.let {TextButton(onClick={menu=null;it(id)}){Text("Configure")}}
                    TextButton(onClick={menu=null;if(onResizeRequest?.invoke(id)!=true)resize=id}){Text("Resize")}
                    onMovePage?.let {TextButton(onClick={menu=null;it(id)}){Text("Move to another page")}}
                    onCollapse?.takeIf {canCollapse(id)}?.let {TextButton(onClick={menu=null;it(id)}){Text(if(cell.collapsed || id in forcedCollapsed)"Expand module" else "Collapse module")}}
                    onDuplicate?.takeIf {canDuplicate(id)}?.let {TextButton(onClick={menu=null;it(id)}){Text("Duplicate")}}
                    onRemove?.let {TextButton(onClick={menu=null;it(id)}){Text("Remove")}}
                    if(onRemove==null)TextButton(onClick={saveNow(layout.copy(cells=layout.cells.map {if(it.id==id)it.copy(hidden=true) else it}));menu=null;session.finish()}){Text("Hide")}
                    TextButton(onClick={saveNow(relocateGrid(layout,id,0,0));menu=null}){Text("Move to first position")}
                }
            }
            if(resize!=null) {
                val id=resize!!;val cell=layout.cells.firstOrNull {it.id==id}
                if(cell!=null) {
                    var w by remember(id){mutableIntStateOf(cell.w)};var h by remember(id){mutableIntStateOf(if(cell.collapsed || id in forcedCollapsed)c.gridLayouts[surface]?.cells?.firstOrNull {it.id==id}?.h ?: items.first {it.id==id}.height else cell.h)}
                    DesktopEditorDialog("Resize · grid handles",{resize=null},confirm={TextButton(onClick={
                        val changed=layout.copy(cells=layout.cells.map {if(it.id==id)it.copy(w=w,h=h) else it})
                        saveNow(relocateGrid(changed,id,cell.x,cell.y));onResize?.invoke(id,w,h);resize=null
                    }){Text("Save size")}}) {
                        Text("Width $w · Height $h",modifier=Modifier.testTag("resize-handles-$surface"))
                        Row {TextButton(onClick={w=(w-1).coerceAtLeast(1)}){Text("◀")};TextButton(onClick={w=(w+1).coerceAtMost(actualColumns)}){Text("▶")};TextButton(onClick={h=(h-1).coerceAtLeast(1)}){Text("▲")};TextButton(onClick={h=(h+1).coerceAtMost(24)}){Text("▼")}}
                    }
                }
            }
        }
    }
}
fun relocateGrid(layout: GridLayout,id: String,x: Int,y: Int): GridLayout {
    val moving=layout.cells.firstOrNull {it.id==id} ?: return layout
    val selected=moving.copy(x=x.coerceIn(0,layout.columns-moving.w),y=y.coerceIn(0,2047-moving.h))
    val placed=mutableListOf(selected)
    layout.cells.filterNot {it.id==id}.sortedWith(compareBy<GridCell>{it.y}.thenBy{it.x}).forEach {other->placed+=if(other.hidden)other else nearestGridCell(other,placed,layout.columns,other.x,other.y)}
    return layout.copy(cells=placed)
}

@Composable fun GridEditingToolbar(session: GridEditSession,model: LauncherModel) {
    if(session.surface!=null)Row(Modifier.fillMaxWidth().heightIn(min=48.dp).testTag("arrangement-toolbar"),verticalAlignment=Alignment.CenterVertically) {
        Text("Arrange",style=MaterialTheme.typography.labelLarge,modifier=Modifier.weight(1f))
        val undo by model.hasLayoutUndo.collectAsState()
        TextButton(onClick={model.undoArrangement()},enabled=undo){Text("Undo")}
        TextButton(onClick={session.options?.invoke()}){Text("Options")}
        TextButton(onClick={session.finish()}){Text("Done")}
    }
}
