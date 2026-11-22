package com.umbra.mobile

import android.accessibilityservice.AccessibilityService
import android.content.Intent
import android.provider.Settings
import android.view.accessibility.AccessibilityEvent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp
import java.lang.ref.WeakReference

/** User-enabled only. No window contents, input gestures, key filtering or event recording. */
class UmbraRecentsService: AccessibilityService() {
    override fun onServiceConnected(){super.onServiceConnected();current=WeakReference(this)}
    override fun onAccessibilityEvent(event: AccessibilityEvent?)=Unit
    override fun onInterrupt()=Unit
    override fun onUnbind(intent: Intent?): Boolean {if(current.get()===this)current.clear();return super.onUnbind(intent)}
    override fun onDestroy(){if(current.get()===this)current.clear();super.onDestroy()}
    companion object {
        private var current=WeakReference<UmbraRecentsService>(null)
        fun openRecents(): Boolean=current.get()?.performGlobalAction(GLOBAL_ACTION_RECENTS)==true
    }
}
@Composable fun RecentsButton() {
    var setup by remember {mutableStateOf(false)};val context=LocalContext.current
    TextButton(onClick={if(!UmbraRecentsService.openRecents())setup=true},contentPadding=PaddingValues(0.dp),modifier=Modifier.size(48.dp).testTag("recents-shortcut").semantics {contentDescription="Recent apps"}){Text("|||",style=MaterialTheme.typography.titleMedium)}
    if(setup)AlertDialog(onDismissRequest={setup=false},title={Text("Recent apps shortcut")},text={Text("Android requires you to enable UMBRA Recents in Accessibility settings for this button. It only opens the native recent-apps screen when tapped; it does not read screen content, record events, or control gestures. You can keep using Samsung's native navigation bar instead.")},confirmButton={TextButton(onClick={setup=false;runCatching {context.startActivity(Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS))}}){Text("Open Accessibility settings")}},dismissButton={TextButton(onClick={setup=false;context.umbraActivity()?.setAndroidBarsVisible(true)}){Text("Use native bar")}})
}
