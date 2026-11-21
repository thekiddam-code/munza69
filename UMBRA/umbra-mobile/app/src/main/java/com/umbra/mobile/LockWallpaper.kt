package com.umbra.mobile

import android.app.WallpaperManager
import android.content.Context
import android.graphics.*
import java.io.OutputStream

fun umbraWallpaper(c: Config): Bitmap {
    val width=1440;val height=3120
    val bitmap=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888)
    val canvas=Canvas(bitmap)
    canvas.drawColor(Color.rgb(9,11,12))
    val accent=Color.parseColor(c.accent.ifEmpty { if(c.greenAccent) "#94B59A" else "#FFB547" })
    val paint=Paint(Paint.ANTI_ALIAS_FLAG).apply { color=accent;strokeWidth=4f;style=Paint.Style.STROKE }
    val path=Path().apply { moveTo(112f,240f);lineTo(1328f,240f);lineTo(1328f,2840f);lineTo(1232f,2936f);lineTo(112f,2936f);close() }
    paint.alpha=90;canvas.drawPath(path,paint)
    paint.alpha=22;paint.strokeWidth=2f
    for(x in 160..1280 step 80)canvas.drawLine(x.toFloat(),420f,x.toFloat()-160f,2720f,paint)
    paint.alpha=50;canvas.drawLine(112f,1030f,1328f,1030f,paint);canvas.drawLine(112f,2640f,1328f,2640f,paint)
    paint.style=Paint.Style.FILL;paint.alpha=230;paint.textSize=144f;paint.typeface=Typeface.create("sans-serif-condensed",Typeface.BOLD)
    canvas.drawText("UMBRA",192f,1450f,paint)
    paint.textSize=30f;paint.alpha=130;paint.typeface=Typeface.MONOSPACE
    canvas.drawText("M O B I L E   S Y S T E M S",200f,1528f,paint)
    paint.alpha=100
    repeat(8){i->canvas.drawRect(192f+i*20f,2578f,204f+i*20f,2600f,paint)}
    return bitmap
}
fun exportWallpaper(c: Config,output: OutputStream) {
    val bitmap=umbraWallpaper(c)
    try { check(bitmap.compress(Bitmap.CompressFormat.PNG,100,output)) } finally { bitmap.recycle() }
}
fun applyLockWallpaper(context: Context,c: Config) {
    val manager=WallpaperManager.getInstance(context)
    check(manager.isWallpaperSupported && manager.isSetWallpaperAllowed) { "Wallpaper changes are restricted on this device." }
    val bitmap=umbraWallpaper(c)
    try { manager.setBitmap(bitmap,null,false,WallpaperManager.FLAG_LOCK) } finally { bitmap.recycle() }
}
