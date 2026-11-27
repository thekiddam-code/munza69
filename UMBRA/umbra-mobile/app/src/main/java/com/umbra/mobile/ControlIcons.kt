package com.umbra.mobile

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.graphics.vector.PathParser
import androidx.compose.ui.unit.dp

/** Original monochrome line artwork: no emoji glyphs, fonts, downloaded logos or animation. */
private fun lineIcon(name: String,path: String)=ImageVector.Builder(name,24.dp,24.dp,24f,24f).addPath(
    pathData=PathParser().parsePathString(path).toNodes(),fill=null,stroke=SolidColor(Color.White),strokeLineWidth=1.6f,
    strokeLineCap=StrokeCap.Round,strokeLineJoin=StrokeJoin.Round).build()
object ControlIcons {
    val Car=lineIcon("Car","M4 16 V11 L7 6 H17 L20 11 V17 H4 V16 M4 11 H20 M7 17 V19 M17 17 V19 M7 14 H9 M15 14 H17")
    val Dance=lineIcon("Dancer","M12 6 A2 2 0 1 0 12 2 A2 2 0 1 0 12 6 M12 7 L11 13 L6 18 L3 18 M11 13 L16 16 L18 21 M11 9 L6 10 L3 7 M12 9 L17 8 L20 4")
    val Pickaxe=lineIcon("Pickaxe","M5 4 Q13 2 20 10 L17 12 Q12 6 5 7 Z M13 8 L4 20 L6 22 L15 10")
    val Keyboard=lineIcon("Keyboard","M3 6 H21 V18 H3 Z M6 9 H7 M10 9 H11 M14 9 H15 M18 9 H19 M6 12 H7 M10 12 H11 M14 12 H15 M18 12 H19 M8 15 H16")
    val Speaker=lineIcon("Speaker","M3 10 H7 L12 6 V18 L7 14 H3 Z M16 9 Q20 12 16 15 M18 6 Q25 12 18 18")
    val Ship=lineIcon("Ship","M12 3 L21 20 L12 16 L3 20 Z M12 3 V16")
    val Headphones=lineIcon("Headphones","M4 14 V11 A8 8 0 0 1 20 11 V17 H16 V11 H20 M4 11 H8 V18 H4 Z")
    val Clip=lineIcon("Save clip","M3 4 H21 V17 H3 Z M7 4 V17 M17 4 V17 M3 8 H7 M3 13 H7 M17 8 H21 M17 13 H21 M10 8 L14 10 L10 12 Z M12 18 V22 M9 20 L12 23 L15 20")
    fun category(family: ButtonFamily,actionId: String?=null): ImageVector=when(family) {
        ButtonFamily.RocketLeague->Car
        ButtonFamily.Fortnite->Dance
        ButtonFamily.Minecraft->Pickaxe
        ButtonFamily.PcHotkey->Keyboard
        ButtonFamily.Soundboard->Speaker
        ButtonFamily.Simulation->Ship
        ButtonFamily.HostAction->if(actionId=="host:arctis")Headphones else Clip
    }
}
