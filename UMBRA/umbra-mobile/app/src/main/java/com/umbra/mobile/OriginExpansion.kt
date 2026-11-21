package com.umbra.mobile

import androidx.activity.compose.BackHandler
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.TransformOrigin
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.positionInWindow
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.semantics.paneTitle
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.zIndex
import kotlin.math.roundToInt

class ExpansionState {
    var selected by mutableStateOf<String?>(null)
    var opening by mutableStateOf(false)
    var origin by mutableStateOf(Rect.Zero)
    var category by mutableStateOf(TransitionCategory.Folder)
    fun open(id: String,bounds: Rect,kind: TransitionCategory) { origin=bounds;category=kind;selected=id;opening=true }
    fun close(){opening=false}
    fun dismissImmediately(){opening=false;selected=null}
}
@Composable fun OriginExpansionHost(state: ExpansionState,c: Config,motion: MotionPolicy,title: String,content: @Composable ()->Unit) {
    val selected=state.selected ?: return
    val plan=transitionPlan(c,motion,state.category)
    val progress=remember(selected){Animatable(0f)}
    LaunchedEffect(selected,state.opening,plan.enabled) {
        if(plan.enabled)progress.animateTo(if(state.opening)1f else 0f,tween(plan.duration)) else progress.snapTo(if(state.opening)1f else 0f)
        if(!state.opening)state.selected=null
    }
    BackHandler {state.close()}
    var hostPosition by remember { mutableStateOf(androidx.compose.ui.geometry.Offset.Zero) }
    BoxWithConstraints(Modifier.fillMaxSize().zIndex(10f).onGloballyPositioned {hostPosition=it.positionInWindow()}) {
        val density=LocalDensity.current
        val targetWidth=minOf(maxWidth-24.dp,480.dp).coerceAtLeast(100.dp)
        val targetHeight=minOf(maxHeight-24.dp,560.dp).coerceAtLeast(100.dp)
        val widthPx=with(density){targetWidth.toPx()};val heightPx=with(density){targetHeight.toPx()}
        val targetX=(constraints.maxWidth-widthPx)/2;val targetY=(constraints.maxHeight-heightPx)/2
        val origin=state.origin.translate(-hostPosition.x,-hostPosition.y)
        val p=if(plan.enabled)progress.value else if(state.opening)1f else 0f
        Box(Modifier.fillMaxSize().background(Color.Black.copy(alpha=.28f*p)).clickable {state.close()})
        val expands=plan.originExpansion && origin.width>0f && origin.height>0f
        val x=if(expands)origin.left+(targetX-origin.left)*p else targetX
        val y=if(expands)origin.top+(targetY-origin.top)*p else targetY
        Surface(shape=Chamfer,color=Panel,border=androidx.compose.foundation.BorderStroke(1.dp,MaterialTheme.colorScheme.primary),
            modifier=Modifier.absoluteOffset{IntOffset(x.roundToInt(),y.roundToInt())}.size(targetWidth,targetHeight).graphicsLayer {
                transformOrigin=TransformOrigin(0f,0f)
                scaleX=if(expands)(origin.width/widthPx).coerceIn(.02f,1f)+(1-(origin.width/widthPx).coerceIn(.02f,1f))*p else 1f
                scaleY=if(expands)(origin.height/heightPx).coerceIn(.02f,1f)+(1-(origin.height/heightPx).coerceIn(.02f,1f))*p else 1f
                alpha=if(plan.enabled)p else 1f;clip=true
            }.semantics {paneTitle=title}.pointerInput(Unit){detectTapGestures { /* Consume only blank panel taps; children keep their gestures. */ }}) {
            Column(Modifier.padding(16.dp)) {
                Row(Modifier.fillMaxWidth(),horizontalArrangement=Arrangement.SpaceBetween) { Text(title,modifier=Modifier.weight(1f),style=MaterialTheme.typography.titleMedium);TextButton(onClick={state.close()}){Text("Close")} }
                Box(Modifier.weight(1f).graphicsLayer {alpha=if(plan.enabled)((p-.25f)/.75f).coerceIn(0f,1f) else 1f}){content()}
            }
        }
    }
}
