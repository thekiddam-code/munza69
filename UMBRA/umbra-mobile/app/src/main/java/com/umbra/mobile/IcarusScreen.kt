package com.umbra.mobile

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.*
import kotlinx.coroutines.*
import kotlinx.serialization.json.buildJsonObject

/** Dedicated PC companion/remote access. Engineering and games live in their own destinations. */
@Composable fun IcarusScreen(c: Config,model: LauncherModel,accent: Color,initialModule: String,open: (Intent)->Unit,configure: ()->Unit,powerSave: Boolean,networkVersion: Long,onModuleChange: (String)->Unit={}) {
    val base=serverBase(c);val saved by model.instant.pcConnection.collectAsStateWithLifecycle()
    val connection=saved.takeIf {it.base==base} ?: PcConnectionState()
    val scope=rememberCoroutineScope();var paired by remember(base){mutableStateOf(false)}
    var pin by remember {mutableStateOf("")};var error by remember {mutableStateOf<String?>(null)};var work by remember {mutableStateOf<Job?>(null)}
    LaunchedEffect(base,connection.checkedAt,connection.error){paired=model.vault.read(base)!=null}
    LifecycleStartEffect(base){onStopOrDispose {work?.cancel();pin=""}}
    LaunchedEffect(Unit){onModuleChange("PC Remote")}
    fun run(action: suspend ()->Unit) {if(work?.isActive!=true)work=scope.launch {try {error=null;action()}catch(e: CancellationException){throw e}catch(e: Exception){error=(e as? java.io.IOException)?.message ?: "Companion request unavailable."}}}
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(12.dp)) {
        Readout("ICARUS / PC REMOTE",accent)
        PcConnectionReadout(connection)
        TextButton(onClick={model.instant.reconnectNow()}){Text("Reconnect PC")}
        TextButton(onClick=configure){Text("Connection settings")}
        error?.let {Text(it,color=MaterialTheme.colorScheme.error)}
        if(!paired)Frame(accent) {
            Text("Pair native controls")
            OutlinedTextField(pin,{pin=it.take(64)},label={Text("Server pairing PIN")},singleLine=true,visualTransformation=PasswordVisualTransformation(),keyboardOptions=KeyboardOptions(keyboardType=KeyboardType.Password),modifier=Modifier.fillMaxWidth())
            Button(onClick={run {
                val entered=pin.trim();pin="";val token=model.remote.pair(base,entered,c.timeout)
                if(serverBase(model.config.value)!=base)throw RemoteFailure(message="Server changed. Pair again.")
                model.vault.remember(base,token);paired=true;model.instant.reconnectNow()
            }},enabled=base.isNotEmpty() && pin.isNotBlank() && work?.isActive!=true,shape=Chamfer){Text("Pair phone")}
            Text("Use the existing Windows companion PIN. Browser authentication remains separate.",style=MaterialTheme.typography.bodySmall)
        } else TextButton(onClick={run {
            val token=model.vault.read(base)
            try {if(token!=null)model.remote.request(base,"api/unpair",c.timeout,token,buildJsonObject {})}
            finally {model.vault.clear();paired=false;model.instant.markInactive();model.instant.reconnectNow()}
        }}){Text("Forget native pairing")}
        Button(onClick={if(validDeckUrl(c.url))open(Intent(Intent.ACTION_VIEW,Uri.parse(c.url).normalizeScheme())) else configure()},shape=Chamfer,modifier=Modifier.fillMaxWidth()){Text("Open PC Remote Deck")}
        Text("Opens your existing PC remote interface. Native desktop video/input streaming is not exposed by this companion API.",style=MaterialTheme.typography.bodySmall)
    }
}
