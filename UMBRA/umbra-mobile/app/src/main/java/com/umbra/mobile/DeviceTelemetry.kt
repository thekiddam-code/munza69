package com.umbra.mobile
import android.animation.ValueAnimator
import android.content.*
import android.database.ContentObserver
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.*
import android.provider.Settings
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.core.content.ContextCompat
import androidx.lifecycle.compose.LifecycleStartEffect

data class Device(val battery: Int = -1, val charging: Boolean? = null, val network: String = "OFFLINE", val powerSave: Boolean = false, val motion: Boolean = true, val thermal: Int = -1, val screenOn: Boolean = true, val storageAvailable: Long? = null, val storageTotal: Long? = null, val memoryAvailable: Long? = null, val memoryTotal: Long? = null, val uptime: Long = 0, val networkGeneration: Long = 0)
@Composable fun rememberDevice(refresh: Int = 0): State<Device> {
    val context = LocalContext.current
    val state = remember { mutableStateOf(Device()) }
    LifecycleStartEffect(context, refresh) {
        val cm = context.getSystemService(ConnectivityManager::class.java)
        val pm = context.getSystemService(PowerManager::class.java)
        fun update() {
            val b = context.registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
            val level = b?.getIntExtra(BatteryManager.EXTRA_LEVEL,-1) ?: -1
            val scale = b?.getIntExtra(BatteryManager.EXTRA_SCALE,100) ?: 100
            val status = b?.getIntExtra(BatteryManager.EXTRA_STATUS,-1)
            val capabilities = cm.getNetworkCapabilities(cm.activeNetwork)
            val network = when {
                capabilities == null -> "OFFLINE"
                capabilities.hasTransport(NetworkCapabilities.TRANSPORT_VPN) -> "VPN NETWORK"
                capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> "WI-FI"
                capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> "CELLULAR"
                else -> "CONNECTED"
            }
            state.value = Device(if (level >= 0 && scale > 0) level*100/scale else -1,
                if(status == null || status < 0 || status == BatteryManager.BATTERY_STATUS_UNKNOWN) null else status == BatteryManager.BATTERY_STATUS_CHARGING,
                network, pm.isPowerSaveMode, ValueAnimator.areAnimatorsEnabled() &&
                    Settings.Global.getFloat(context.contentResolver,Settings.Global.TRANSITION_ANIMATION_SCALE,1f) > 0f &&
                    Settings.Global.getFloat(context.contentResolver,Settings.Global.WINDOW_ANIMATION_SCALE,1f) > 0f,
                runCatching { pm.currentThermalStatus }.getOrDefault(-1), pm.isInteractive, state.value.storageAvailable, state.value.storageTotal,
                state.value.memoryAvailable, state.value.memoryTotal, state.value.uptime, state.value.networkGeneration)
        }
        val handler = Handler(Looper.getMainLooper())
        val receiver = object : BroadcastReceiver() { override fun onReceive(c: Context?, i: Intent?) { update() } }
        val observer = object : ContentObserver(handler) { override fun onChange(selfChange: Boolean) { update() } }
        val network = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(n: android.net.Network) { handler.post { update();state.value=state.value.copy(networkGeneration=state.value.networkGeneration+1) } }
            override fun onLost(n: android.net.Network) { handler.post { update();state.value=state.value.copy(networkGeneration=state.value.networkGeneration+1) } }
            override fun onCapabilitiesChanged(n: android.net.Network, c: NetworkCapabilities) { handler.post { update();state.value=state.value.copy(networkGeneration=state.value.networkGeneration+1) } }
        }
        ContextCompat.registerReceiver(context,receiver,IntentFilter().apply {
            addAction(Intent.ACTION_BATTERY_CHANGED); addAction(PowerManager.ACTION_POWER_SAVE_MODE_CHANGED); addAction(Intent.ACTION_SCREEN_ON); addAction(Intent.ACTION_SCREEN_OFF)
        },ContextCompat.RECEIVER_NOT_EXPORTED)
        listOf(Settings.Global.ANIMATOR_DURATION_SCALE,Settings.Global.TRANSITION_ANIMATION_SCALE,Settings.Global.WINDOW_ANIMATION_SCALE).forEach {
            context.contentResolver.registerContentObserver(Settings.Global.getUriFor(it),false,observer)
        }
        cm.registerDefaultNetworkCallback(network)
        val thermal = PowerManager.OnThermalStatusChangedListener { update() }
        val thermalRegistered=runCatching { pm.addThermalStatusListener(context.mainExecutor, thermal) }.isSuccess
        update()
        // Expensive readings refresh only on visibility entry or explicit user refresh.
        val storage = runCatching { StatFs(context.filesDir.path) }.getOrNull()
        val memory = android.app.ActivityManager.MemoryInfo()
        val memoryOk = runCatching { context.getSystemService(android.app.ActivityManager::class.java).getMemoryInfo(memory) }.isSuccess
        state.value = state.value.copy(storageAvailable=storage?.availableBytes?.takeIf { (storage?.totalBytes ?: 0)>0 },storageTotal=storage?.totalBytes?.takeIf { it>0 },
            memoryAvailable=memory.availMem.takeIf { memoryOk && memory.totalMem>0 },memoryTotal=memory.totalMem.takeIf { memoryOk && it>0 },uptime=SystemClock.elapsedRealtime())
        onStopOrDispose {
            if(thermalRegistered) runCatching { pm.removeThermalStatusListener(thermal) }
            context.unregisterReceiver(receiver); context.contentResolver.unregisterContentObserver(observer)
            cm.unregisterNetworkCallback(network); handler.removeCallbacksAndMessages(null)
        }
    }
    return state
}
