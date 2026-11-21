package com.umbra.mobile

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

@OptIn(ExperimentalLayoutApi::class)
@Composable fun StatusPanel(c: Config, d: Device, time: LocalDateTime, deck: String, accent: Color, notificationCount: Int? = null) {
    FlowRow(Modifier.testTag("umbra-status-panel").fillMaxWidth().padding(bottom=10.dp),horizontalArrangement=Arrangement.spacedBy(12.dp),verticalArrangement=Arrangement.spacedBy(4.dp)) {
        if("Time" in c.indicators) Readout(time.format(DateTimeFormatter.ofPattern("HH:mm")),accent)
        if("Date" in c.indicators) Readout(time.format(DateTimeFormatter.ofPattern("dd MMM")),Muted)
        if("Battery" in c.indicators) Readout("BAT ${if(d.battery<0) "--" else "${d.battery}%"} · ${if(d.charging==true) "CHARGING" else if(d.charging==false) "NOT CHARGING" else "STATE UNKNOWN"}",accent)
        if("Network" in c.indicators) Readout(d.network,Green)
        if("ICARUS" in c.indicators) Readout("ICARUS · $deck",accent)
        if("Notifications" in c.indicators) Readout("NOTIFICATIONS · ${notificationCount?.toString() ?: "UNAVAILABLE"}",Muted)
    }
    if(c.immersive && ((c.hideTopBar && WindowInsets.areStatusBarsVisible) || (c.hideBottomBar && WindowInsets.areNavigationBarsVisible))) {
        Text("Android bars visible · transient gesture or system restriction",color=Muted,style=androidx.compose.material3.MaterialTheme.typography.bodySmall)
    }
}
