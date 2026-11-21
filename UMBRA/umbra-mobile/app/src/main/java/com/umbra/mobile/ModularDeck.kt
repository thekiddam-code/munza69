package com.umbra.mobile

import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalFoundationApi::class)
@Composable fun ModularDeck(surface: String,names: List<String>,c: Config,model: LauncherModel,compactMode: Boolean=false,initialOpen: String?=null,
    onFocus: (String)->Unit={},status: (String)->String={""},body: @Composable (String)->Unit) {
    var restore by remember {mutableStateOf(false)}
    val session=LocalGridEditing.current
    val items=names.map {GridItem(it,it,c.deckColumns,when(it){"Device","Engineering"->7;"System","Lounge"->7;"Instant Controls","Rocket League"->6;else->5},true,initialOpen!=null && it!=initialOpen)}
    val legacyHidden=if(surface=="command")c.hiddenModules else emptySet()
    val available=items.filterNot {it.id in legacyHidden}
    val forced=if(compactMode)available.filterNot {it.id=="System"}.map {it.id}.toSet() else emptySet()
    Column {
        if(available.isEmpty())Text("Long-press this space to restore modules.",modifier=Modifier.fillMaxWidth().heightIn(min=64.dp).combinedClickable(onClick={},onLongClick={restore=true}))
        GridBoard(surface,available,c,model,compact=true,forcedCollapsed=forced,onConfigure={restore=true},onCollapse={id->model.arrange {old->
            val grid=old.gridLayouts[surface] ?: resolveGrid(items,null,old.deckColumns,true)
            old.copy(gridLayouts=old.gridLayouts+(surface to grid.copy(cells=grid.cells.map {if(it.id==id)it.copy(collapsed=!it.collapsed,h=old.gridLayouts[surface]?.cells?.firstOrNull {it.id==id}?.h ?: items.first {i->i.id==id}.height) else it})))
        }}) {item,cell->
            val expanded=!cell.collapsed && item.id !in forced
            Surface(color=Panel,shape=Chamfer,border=BorderStroke(1.dp,MaterialTheme.colorScheme.primary.copy(alpha=.45f)),modifier=Modifier.fillMaxSize()) {
                Column(Modifier.fillMaxSize().panelDetail(c.visualDetail,MaterialTheme.colorScheme.primary).padding(horizontal=10.dp)) {
                    Row(headerModifier.fillMaxWidth().height(58.dp).testTag("module-header-$surface-${item.id}").clickable {
                        if(session.surface==surface)return@clickable
                        onFocus(item.id)
                        model.arrange {old->
                            val grid=resolveGrid(items,old.gridLayouts[surface],old.deckColumns,true)
                            val stored=old.gridLayouts[surface]
                            old.copy(commandExpanded=if(surface=="command" && compactMode)true else old.commandExpanded,
                                gridLayouts=old.gridLayouts+(surface to grid.copy(cells=grid.cells.map {g->if(g.id==item.id)g.copy(collapsed=expanded,h=stored?.cells?.firstOrNull {it.id==g.id}?.h ?: item.height) else g.copy(h=stored?.cells?.firstOrNull {it.id==g.id}?.h ?: items.first {i->i.id==g.id}.height)})))
                        }
                    },verticalAlignment=Alignment.CenterVertically) {
                        Text("▣",color=MaterialTheme.colorScheme.primary)
                        Column(Modifier.weight(1f).padding(horizontal=8.dp)) {
                            Text(item.title,style=MaterialTheme.typography.labelLarge,maxLines=2)
                            val value=status(item.id);if(value.isNotEmpty())Text(value,style=MaterialTheme.typography.bodySmall,maxLines=1,color=Muted)
                        }
                        Text(if(expanded)"−" else "+",color=MaterialTheme.colorScheme.primary)
                    }
                    val policy=LocalMotionPolicy.current
                    val plan=transitionPlan(c,policy,TransitionCategory.Panel)
                    val animate=plan.enabled
                    AnimatedVisibility(expanded,enter=if(animate)fadeIn(tween(plan.duration))+expandVertically(tween(plan.duration)) else EnterTransition.None,exit=if(animate)fadeOut(tween(plan.duration))+shrinkVertically(tween(plan.duration)) else ExitTransition.None,modifier=Modifier.weight(1f)) {
                        Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(bottom=10.dp),verticalArrangement=Arrangement.spacedBy(10.dp)) {body(item.id)}
                    }
                }
            }
        }
        if(session.surface==surface)TextButton(onClick={restore=true}){Text("Restore / configure modules")}
    }
    if(restore)DesktopEditorDialog("Deck modules",{restore=false},confirm={TextButton(onClick={restore=false;session.finish()}){Text("Done")}}) {
        Choice("Grid density",listOf("2","3","4"),c.deckColumns.toString()){value->model.arrange {it.copy(deckColumns=value.toInt())}}
        names.forEach {name->val hidden=name in legacyHidden || c.gridLayouts[surface]?.cells?.firstOrNull {it.id==name}?.hidden==true
            Toggle("Show $name",!hidden){show->model.arrange {old->val grid=resolveGrid(items,old.gridLayouts[surface],old.deckColumns,true);old.copy(hiddenModules=if(surface=="command")old.hiddenModules-name else old.hiddenModules,gridLayouts=old.gridLayouts+(surface to grid.copy(cells=grid.cells.map {if(it.id==name)it.copy(hidden=!show) else it})))}}
        }
        TextButton(onClick={model.undoArrangement()}){Text("Undo arrangement")}
    }
}
