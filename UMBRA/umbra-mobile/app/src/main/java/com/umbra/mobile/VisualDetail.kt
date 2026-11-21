package com.umbra.mobile

import androidx.compose.foundation.layout.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawWithCache
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp
import kotlinx.serialization.Serializable

@Serializable enum class VisualDetail { Minimal, Enhanced, Cinematic }
val LocalVisualDetail=staticCompositionLocalOf { VisualDetail.Enhanced }
@Composable fun StaticTerminalBackground(detail: VisualDetail,accent: Color) {
    // No clock, animation state, or running coroutine. Geometry is cached until size/style changes.
    val layer=remember(detail,accent) { Modifier.drawWithCache {
        val grid=Path()
        val step=if(detail==VisualDetail.Cinematic)36.dp.toPx() else 52.dp.toPx()
        var x=0f;while(x<size.width){grid.moveTo(x,0f);grid.lineTo(x,size.height);x+=step}
        var y=0f;while(y<size.height){grid.moveTo(0f,y);grid.lineTo(size.width,y);y+=step}
        val hull=Path().apply {
            moveTo(size.width*.08f,size.height*.18f);lineTo(size.width*.24f,size.height*.06f);lineTo(size.width*.76f,size.height*.06f)
            lineTo(size.width*.92f,size.height*.18f);lineTo(size.width*.92f,size.height*.88f);lineTo(size.width*.76f,size.height*.96f)
            lineTo(size.width*.24f,size.height*.96f);lineTo(size.width*.08f,size.height*.88f);close()
        }
        val gradient=Brush.radialGradient(listOf(accent.copy(alpha=if(detail==VisualDetail.Cinematic).07f else .035f),Color.Transparent),center=Offset(size.width*.85f,size.height*.15f),radius=size.height*.65f)
        onDrawBehind {
            if(detail!=VisualDetail.Minimal) {
                drawRect(gradient)
                drawPath(grid,Color(0xFF7998B0).copy(alpha=.045f),style=Stroke(1f))
                drawPath(hull,accent.copy(alpha=.065f),style=Stroke(1.5f))
                repeat(if(detail==VisualDetail.Cinematic)8 else 4) { i ->
                    val yy=size.height*(.16f+i*.1f)
                    drawLine(accent.copy(alpha=.07f),Offset(size.width*.08f,yy),Offset(size.width*.18f,yy),2f)
                    drawLine(accent.copy(alpha=.07f),Offset(size.width*.82f,yy),Offset(size.width*.92f,yy),2f)
                }
                if(detail==VisualDetail.Cinematic) {
                    repeat(5) { n ->val inset=n*18.dp.toPx();drawRect(accent.copy(alpha=.025f),Offset(inset,inset),Size((size.width-2*inset).coerceAtLeast(1f),(size.height-2*inset).coerceAtLeast(1f)),style=Stroke(1f))}
                }
            }
        }
    } }
    Box(Modifier.fillMaxSize().then(layer))
}
fun Modifier.panelDetail(detail: VisualDetail,accent: Color): Modifier = drawWithCache {
    onDrawBehind {
        if(detail!=VisualDetail.Minimal) {
            val length=24.dp.toPx()
            drawLine(accent.copy(alpha=.45f),Offset(14.dp.toPx(),3.dp.toPx()),Offset(14.dp.toPx()+length,3.dp.toPx()),1.5f)
            drawLine(accent.copy(alpha=.25f),Offset(size.width-length-14.dp.toPx(),size.height-3.dp.toPx()),Offset(size.width-14.dp.toPx(),size.height-3.dp.toPx()),1.5f)
            if(detail==VisualDetail.Cinematic)repeat(3){i->drawLine(accent.copy(alpha=.2f),Offset(size.width-8.dp.toPx(),(16+i*5).dp.toPx()),Offset(size.width-4.dp.toPx(),(16+i*5).dp.toPx()),1f)}
        }
    }
}
