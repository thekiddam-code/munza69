package com.umbra.mobile

import android.content.Intent
import android.net.Uri
import android.provider.Settings
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.layout.boundsInWindow
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.semantics.*
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@OptIn(ExperimentalFoundationApi::class)
@Composable fun AppTile(app: LaunchApp,model: LauncherModel,favorite: Boolean,launch: ()->Unit,toggle: ()->Unit,accent: Color,
    desktopGesture: Boolean=false,onLongPress: (()->Unit)?=null) {
    val c=LocalLauncherConfig.current
    val density=LocalDensity.current
    val pixels=with(density){c.iconSize.dp.roundToPx()}.coerceIn(64,224)
    var bitmap by remember(app.id,pixels){mutableStateOf<android.graphics.Bitmap?>(null)}
    var iconBounds by remember {mutableStateOf<Rect?>(null)}
    var menu by remember {mutableStateOf(false)}
    val nativeLaunch=LocalIconLaunch.current
    val context=LocalContext.current
    LaunchedEffect(app.id,pixels){bitmap=model.icon(app.id,pixels)}
    fun open(){if(nativeLaunch!=null)nativeLaunch(app,iconBounds) else launch()}
    Box {
        val interaction=if(desktopGesture)Modifier.clickable(onClick={open()}) else Modifier.combinedClickable(onClick={open()},onLongClick={if(onLongPress!=null)onLongPress() else menu=true})
        Column(Modifier.fillMaxWidth().then(interaction).padding(vertical=8.dp,horizontal=4.dp).semantics {
            contentDescription=app.label
            customActions=listOf(CustomAccessibilityAction(if(favorite)"Remove favorite" else "Add favorite"){toggle();true})
        },horizontalAlignment=Alignment.CenterHorizontally) {
            val iconModifier=Modifier.size(c.iconSize.dp).onGloballyPositioned {iconBounds=it.boundsInWindow()}
            if(bitmap!=null)Image(bitmap!!.asImageBitmap(),contentDescription=null,modifier=iconModifier)
            else Text("◇",fontSize=c.iconSize.sp,color=accent,modifier=iconModifier)
            if(c.showAppLabels)Text(app.label,color=White,fontSize=13.sp,maxLines=2,overflow=TextOverflow.Ellipsis,
                modifier=Modifier.heightIn(min=36.dp).padding(top=6.dp),textAlign=androidx.compose.ui.text.style.TextAlign.Center)
        }
        DropdownMenu(expanded=menu,onDismissRequest={menu=false}) {
            DropdownMenuItem(text={Text("Open ${app.label}")},onClick={menu=false;open()})
            DropdownMenuItem(text={Text(if(favorite)"Remove favorite" else "Add favorite")},onClick={menu=false;toggle()})
            DropdownMenuItem(text={Text("Add to Home")},onClick={menu=false;model.placeShortcut(app.id)})
            DropdownMenuItem(text={Text("Hide from launcher")},onClick={menu=false;model.change {it.copy(hiddenApps=it.hiddenApps+app.id)}})
            DropdownMenuItem(text={Text("Android app info")},onClick={menu=false;runCatching {context.startActivity(Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS,Uri.parse("package:"+app.id.substringBefore('/'))))}})
        }
    }
}
