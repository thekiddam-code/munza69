package com.umbra.mobile

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawWithCache
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Category identity is static and independent of optional motion and Visual Detail.
enum class ButtonFamily(val label: String,val color: Color,val glow: Boolean=false) {
    RocketLeague("Rocket League",Color(0xFF80BEFF)),
    Fortnite("Fortnite",Color(0xFF83D4FF)),
    Minecraft("Minecraft",Color(0xFF92DD71)),
    PcHotkey("PC hotkey",Color(0xFF70F0B2),true),
    Soundboard("Soundboard",Color(0xFFE3EEFF)),
    Simulation("Simulation",Amber)
}
fun buttonFamily(action: InstantAction): ButtonFamily = when {
    action.path=="api/sounds/play"->ButtonFamily.Soundboard
    action.path=="api/icarus/command"->ButtonFamily.Simulation
    action.body.literal("action") in listOf("quick","text")->ButtonFamily.RocketLeague
    action.body.literal("action")=="fortnite_emote"->ButtonFamily.Fortnite
    action.body.literal("action") in listOf("mine_toggle","forward_mine")->ButtonFamily.Minecraft
    else->ButtonFamily.PcHotkey
}
@Composable fun CategoryControlButton(label: String,family: ButtonFamily,enabled: Boolean,modifier: Modifier=Modifier,onClick: ()->Unit) {
    val color=family.color
    val glow=if(family.glow && enabled)Modifier.drawWithCache {
        val cut=6.dp.toPx();val path=Path().apply {moveTo(cut,0f);lineTo(size.width,0f);lineTo(size.width,size.height-cut);lineTo(size.width-cut,size.height);lineTo(0f,size.height);lineTo(0f,cut);close()}
        onDrawBehind {drawPath(path,color.copy(alpha=.10f),style=Stroke(7.dp.toPx()));drawPath(path,color.copy(alpha=.17f),style=Stroke(3.dp.toPx()))}
    } else Modifier
    OutlinedButton(onClick=onClick,enabled=enabled,shape=Chamfer,border=BorderStroke(1.dp,color.copy(alpha=if(enabled).8f else .3f)),
        colors=ButtonDefaults.outlinedButtonColors(containerColor=color.copy(alpha=.09f),contentColor=color,disabledContainerColor=color.copy(alpha=.03f),disabledContentColor=color.copy(alpha=.4f)),
        contentPadding=PaddingValues(horizontal=4.dp,vertical=3.dp),modifier=modifier.then(glow).semantics {stateDescription="${family.label} control"}) {
        Column(verticalArrangement=Arrangement.Center) {
            Text(label,maxLines=3,overflow=TextOverflow.Ellipsis,style=MaterialTheme.typography.labelLarge)
            Text(family.label,fontSize=9.sp,lineHeight=11.sp,maxLines=1,overflow=TextOverflow.Ellipsis,color=color.copy(alpha=if(enabled).8f else .4f))
        }
    }
}
