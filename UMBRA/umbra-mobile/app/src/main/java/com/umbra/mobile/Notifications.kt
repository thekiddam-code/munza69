package com.umbra.mobile

import android.app.Notification
import android.content.Context
import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
import androidx.core.app.NotificationManagerCompat
import androidx.lifecycle.compose.LifecycleResumeEffect
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableStateFlow

// Counts only. Never read titles, text, actions, people, or notification extras.
class UmbraNotificationListener : NotificationListenerService() {
    private val scope = CoroutineScope(SupervisorJob()+Dispatchers.Main.immediate)
    private var enabled = false
    private var connected = false
    override fun onCreate() {
        super.onCreate()
        scope.launch { ConfigStore(this@UmbraNotificationListener).config.collect { enabled=it.notificationsEnabled; refreshCount() } }
    }
    override fun onListenerConnected() { connected=true;refreshCount() }
    override fun onListenerDisconnected() { connected=false;count.value=null }
    override fun onNotificationPosted(sbn: StatusBarNotification?) = refreshCount()
    override fun onNotificationRemoved(sbn: StatusBarNotification?) = refreshCount()
    private fun refreshCount() {
        count.value = if(enabled && connected) runCatching {
            activeNotifications?.count { it.notification.flags and Notification.FLAG_GROUP_SUMMARY == 0 }
        }.getOrNull() else null
    }
    override fun onDestroy() { count.value=null;scope.cancel();super.onDestroy() }
    companion object { val count = MutableStateFlow<Int?>(null) }
}
fun notificationAccess(context: Context) = context.packageName in NotificationManagerCompat.getEnabledListenerPackages(context)
@Composable fun rememberNotificationAccess(): Boolean {
    val context=LocalContext.current
    var granted by remember { mutableStateOf(notificationAccess(context)) }
    LifecycleResumeEffect(Unit) { granted=notificationAccess(context); onPauseOrDispose { } }
    return granted
}
