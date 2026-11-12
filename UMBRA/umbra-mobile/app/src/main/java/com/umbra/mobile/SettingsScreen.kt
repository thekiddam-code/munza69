package com.umbra.mobile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable fun Configuration(c: Config,model: LauncherModel,accent: Color,homeSettings: ()->Unit) {
    var url by rememberSaveable(c.url) { mutableStateOf(c.url) }
    var timeout by rememberSaveable(c.timeout) { mutableStateOf(c.timeout.toString()) }
    var saved by remember { mutableStateOf(false) }
    val urlValid = url.isEmpty() || validDeckUrl(url)
    val seconds = timeout.toIntOrNull()
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(12.dp)) {
        Text("TERMINAL CONFIGURATION",fontFamily=FontFamily.Monospace,fontSize=18.sp,color=accent)
        Text("Performance profile",style=MaterialTheme.typography.titleMedium)
        Profile.entries.forEach { profile ->
            Row(verticalAlignment=Alignment.CenterVertically) {
                RadioButton(selected=c.profile==profile,onClick={model.profile(profile)})
                TextButton(onClick={model.profile(profile)}) { Text(profile.name) }
            }
        }
        Text(when(c.profile) {
            Profile.Adaptive -> "Subtle idle effects pause during interaction. Low battery, Android power saving, and reduced motion disable optional animation."
            Profile.Cinematic -> "Longer transitions and faster ambient movement. Android power and motion restrictions still apply."
            Profile.Minimal -> "Instant transitions. No decorative animation or continuous effects."
        },style=MaterialTheme.typography.bodySmall)
        Toggle("Master animations",c.master){model.flag("master",it)}
        Text("Individual selections are saved independently and restored when the master switch is enabled.",style=MaterialTheme.typography.bodySmall)
        Toggle("Ambient lighting",c.ambient){model.flag("ambient",it)}
        Toggle("Terminal startup and transitions",c.transitions){model.flag("transitions",it)}
        Toggle("Environmental effects",c.environment){model.flag("environment",it)}
        Toggle("ICARUS status alert animations",c.alerts){model.flag("alerts",it)}
        Toggle("Animated terminal background",c.wallpaper){model.flag("wallpaper",it)}
        HorizontalDivider()
        Text("Appearance",style=MaterialTheme.typography.titleMedium)
        Toggle("Muted green accent (amber when off)",c.greenAccent){model.flag("greenAccent",it)}
        Toggle("Device status panel",c.statusPanel){model.flag("statusPanel",it)}
        Text("Home shortcuts follow your drawer favorites in alphabetical order. Tap a star to add or remove a shortcut.",style=MaterialTheme.typography.bodySmall)
        HorizontalDivider()
        Text("ICARUS Remote Deck",style=MaterialTheme.typography.titleMedium)
        OutlinedTextField(url,{url=it;saved=false},label={Text("Remote Deck URL")},supportingText={Text(if(urlValid) "HTTP(S) address without credentials, query, or fragment." else "Enter a valid HTTP(S) URL, or leave empty.")},isError=!urlValid,singleLine=true,keyboardOptions=KeyboardOptions(keyboardType=KeyboardType.Uri),modifier=Modifier.fillMaxWidth())
        OutlinedTextField(timeout,{timeout=it;saved=false},label={Text("Connection timeout (1–30 seconds)")},isError=seconds !in 1..30,singleLine=true,keyboardOptions=KeyboardOptions(keyboardType=KeyboardType.Number),modifier=Modifier.fillMaxWidth())
        Button(onClick={model.deck(url,seconds!!);saved=true},enabled=urlValid && seconds in 1..30,modifier=Modifier.fillMaxWidth()) { Text(if(saved && c.url==url && c.timeout==seconds) "Saved" else "Save connection") }
        Text("Checks send an HTTP HEAD request only when UMBRA becomes visible, the connection changes, or you tap Check. HTTP responses show reachability; authentication and server health are not verified. Keep Tailscale connected. HTTP is allowed for private tailnet services; prefer HTTPS. Authentication stays in your browser.",style=MaterialTheme.typography.bodySmall)
        HorizontalDivider()
        Button(onClick=homeSettings,modifier=Modifier.fillMaxWidth()) { Text("Choose default Home application") }
        Text("To restore Samsung: Android Settings → Apps → Choose default apps → Home app → One UI Home. Notification shade, lock screen, phone, biometrics, and Android gestures remain managed by Samsung.",style=MaterialTheme.typography.bodySmall)
        Text("UMBRA MOBILE / PHASE 1 / LOCAL SETTINGS",fontFamily=FontFamily.Monospace,fontSize=11.sp,color=accent,modifier=Modifier.padding(vertical=16.dp))
    }
}
@Composable private fun Toggle(label: String,value: Boolean,change: (Boolean)->Unit) {
    Row(Modifier.fillMaxWidth().heightIn(min=56.dp),verticalAlignment=Alignment.CenterVertically) {
        Text(label,modifier=Modifier.weight(1f))
        Switch(checked=value,onCheckedChange=change,modifier=Modifier.padding(start=12.dp).semantics { contentDescription = label })
    }
}
