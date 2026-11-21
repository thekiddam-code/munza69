package com.umbra.mobile

import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.boundsInWindow
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.lifecycle.repeatOnLifecycle
import kotlinx.coroutines.delay
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

@Composable fun rememberWidgetTime(visible: Boolean,seconds: Boolean): LocalDateTime {
    val lifecycle=LocalLifecycleOwner.current.lifecycle
    var now by remember {mutableStateOf(LocalDateTime.now())}
    LaunchedEffect(lifecycle,visible,seconds) {
        if(visible)lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED) {
            while(true){now=LocalDateTime.now();val tick=if(seconds)1000L else 60000L;delay(tick-System.currentTimeMillis()%tick)}
        }
    }
    return now
}
@Composable fun BuiltinWidget(item: DesktopItem,c: Config,model: LauncherModel,device: Device,unusedTime: LocalDateTime,accent: Color,visible: Boolean,expand: (Rect)->Unit) {
    val w=item.widget!!
    if(w.kind=="android") { HostedAndroidWidget(item,model,visible);return }
    var bounds by remember(item.id){mutableStateOf(Rect.Zero)}
    val color=if(w.accent.isEmpty())accent else Color(android.graphics.Color.parseColor(w.accent))
    Surface(color=if(w.transparent)Color.Transparent else Panel,shape=Chamfer,modifier=Modifier.fillMaxWidth().height((w.rows*64).coerceAtLeast(96).dp).onGloballyPositioned {bounds=it.boundsInWindow()}.testTag("widget-${item.id}").clickable {expand(bounds)}) {
        Column(Modifier.padding(10.dp),verticalArrangement=Arrangement.Center,horizontalAlignment=Alignment.CenterHorizontally) {
            when(w.kind) {
                "clock" -> ClockFace(w,rememberWidgetTime(visible,w.seconds),color)
                "weather" -> WeatherWidgetCompact(c,model,visible)
                "battery" -> {Readout("BATTERY",color);Text(device.battery.takeIf {it>=0}?.let {"$it%"} ?: "Unavailable",fontSize=32.sp,color=color);Text(if(device.charging==true)"Charging" else if(device.charging==false)"Not charging" else "State unavailable")}
                "calendar" -> {Readout("CALENDAR",color);Text(unusedTime.format(DateTimeFormatter.ofPattern("EEE, d MMM yyyy")),fontSize=20.sp);Text("Tap for month view",style=MaterialTheme.typography.bodySmall)}
                "system" -> {Readout("DEVICE STATUS",color);Text(device.network);Text(if(device.powerSave)"Battery saver on" else "Battery saver off")}
                "icarus" -> InstantControls(c,model,visible,compact=true,surface="instant-widget:${item.id}",widgetId=item.id)
            }
        }
    }
}
@Composable fun ClockFace(w: DesktopWidget,time: LocalDateTime,accent: Color) {
    val pattern=if(w.clock24)if(w.seconds)"HH:mm:ss" else "HH:mm" else if(w.seconds)"hh:mm:ss a" else "hh:mm a"
    if(w.style=="Analog") {
        Canvas(Modifier.fillMaxHeight().aspectRatio(1f,false)) {
            val radius=minOf(size.width,size.height)*.43f;val center=Offset(size.width/2,size.height/2)
            drawCircle(accent.copy(alpha=.35f),radius,center,style=androidx.compose.ui.graphics.drawscope.Stroke(2.dp.toPx()))
            repeat(12){i->val angle=i*PI/6-PI/2;drawLine(accent.copy(alpha=.6f),center+Offset((cos(angle)*radius*.88).toFloat(),(sin(angle)*radius*.88).toFloat()),center+Offset((cos(angle)*radius).toFloat(),(sin(angle)*radius).toFloat()),2.dp.toPx())}
            fun hand(value: Double,length: Float,width: Float,color: Color){val angle=value*2*PI-PI/2;drawLine(color,center,center+Offset((cos(angle)*radius*length).toFloat(),(sin(angle)*radius*length).toFloat()),width)}
            hand((time.hour%12+time.minute/60.0)/12,.55f,4.dp.toPx(),accent);hand(time.minute/60.0,.8f,2.dp.toPx(),accent)
            if(w.seconds)hand(time.second/60.0,.9f,1.dp.toPx(),Green)
        }
    } else if(w.style=="Segmented") {
        val text=time.format(DateTimeFormatter.ofPattern(if(w.clock24)if(w.seconds)"HH:mm:ss" else "HH:mm" else if(w.seconds)"hh:mm:ss" else "hh:mm"))
        SegmentedClock(text,accent)
        if(!w.clock24)Text(time.format(DateTimeFormatter.ofPattern("a")),color=accent,style=MaterialTheme.typography.bodySmall)
    } else {
        Text(time.format(DateTimeFormatter.ofPattern(pattern)),fontFamily=FontFamily.Monospace,fontSize=when(w.style){"Terminal"->36.sp;"Date and time"->24.sp;else->28.sp},color=accent,maxLines=1)
        if(w.style in listOf("Terminal","Date and time"))Text(time.format(DateTimeFormatter.ofPattern("EEE / dd MMM yyyy")),color=Muted,style=MaterialTheme.typography.bodySmall)
    }
}
@Composable private fun SegmentedClock(text: String,accent: Color) {
    val masks=intArrayOf(0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f)
    Canvas(Modifier.fillMaxWidth().heightIn(min=32.dp,max=100.dp).weightlessHeight()) {
        val cell=size.width/text.length;val h=minOf(size.height,cell*1.8f);val t=(cell*.09f).coerceAtLeast(1f)
        text.forEachIndexed {index,ch->val x=index*cell+cell*.1f;val width=cell*.72f
            if(ch==':'){drawCircle(accent,t,Offset(x+width/2,h*.35f));drawCircle(accent,t,Offset(x+width/2,h*.7f))}
            else if(ch.isDigit()) {
                val segments=listOf(Rect(x+t,0f,x+width-t,t),Rect(x+width-t,t,x+width,h/2-t),Rect(x+width-t,h/2+t,x+width,h-t),Rect(x+t,h-t,x+width-t,h),Rect(x,h/2+t,x+t,h-t),Rect(x,t,x+t,h/2-t),Rect(x+t,h/2-t/2,x+width-t,h/2+t/2))
                segments.forEachIndexed {bit,r->drawRect(if(masks[ch.digitToInt()] and (1 shl bit)!=0)accent else accent.copy(alpha=.08f),r.topLeft,r.size)}
            }
        }
    }
}
private fun Modifier.weightlessHeight()=height(72.dp)
@OptIn(ExperimentalFoundationApi::class)
@Composable fun WidgetDetails(item: DesktopItem,c: Config,model: LauncherModel,device: Device,time: LocalDateTime,accent: Color,configure: ()->Unit) {
    Column(Modifier.fillMaxSize().combinedClickable(onClick={},onLongClick=configure).verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(12.dp)) {
        when(item.widget!!.kind) {
            "weather" -> WeatherDetails(c,model)
            "system","battery" -> TelemetryReadouts(device)
            "calendar" -> {
                val month=time.toLocalDate().withDayOfMonth(1)
                Text(month.format(DateTimeFormatter.ofPattern("MMMM yyyy")),style=MaterialTheme.typography.titleLarge)
                Row(Modifier.fillMaxWidth()) {listOf("M","T","W","T","F","S","S").forEach {Text(it,modifier=Modifier.weight(1f),color=Muted)}}
                (List(month.dayOfWeek.value-1){0}+(1..month.lengthOfMonth()).toList()).chunked(7).forEach {row->Row(Modifier.fillMaxWidth()) {
                    (row+List(7-row.size){0}).forEach {day->Text(if(day==0)"" else day.toString(),modifier=Modifier.weight(1f),color=if(day==time.dayOfMonth)accent else White)}
                }}
                val context=LocalContext.current
                TextButton(onClick={runCatching{context.startActivity(android.content.Intent(android.content.Intent.ACTION_MAIN).addCategory(android.content.Intent.CATEGORY_APP_CALENDAR))}}){Text("Open Android calendar")}
            }
            "icarus" -> InstantControls(c,model,true,compact=false)
            else -> Column(Modifier.fillMaxWidth().height(240.dp),horizontalAlignment=Alignment.CenterHorizontally){ClockFace(item.widget,rememberWidgetTime(device.screenOn,item.widget.seconds),accent)}
        }
    }
}
