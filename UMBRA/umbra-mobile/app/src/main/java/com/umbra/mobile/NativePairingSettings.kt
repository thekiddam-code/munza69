package com.umbra.mobile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.lifecycle.compose.LifecycleStartEffect
import kotlinx.coroutines.*

@Composable fun NativePairingSettings(c: Config,model: LauncherModel) {
    val base=serverBase(c);val scope=rememberCoroutineScope()
    var pin by remember(base){mutableStateOf("")};var message by remember(base){mutableStateOf("")};var job by remember {mutableStateOf<Job?>(null)};var busy by remember {mutableStateOf(false)}
    LifecycleStartEffect(base){onStopOrDispose {job?.cancel();pin="";busy=false}}
    Text("Pair this phone",style=MaterialTheme.typography.titleMedium)
    Text("Save the companion address above, then enter the PIN shown on your PC.",style=MaterialTheme.typography.bodySmall)
    OutlinedTextField(pin,{pin=it.take(64)},label={Text("Server PIN")},singleLine=true,visualTransformation=PasswordVisualTransformation(),keyboardOptions=KeyboardOptions(keyboardType=KeyboardType.Password),modifier=Modifier.fillMaxWidth())
    Button(onClick={if(!busy){busy=true;val entered=pin.trim();pin="";job=scope.launch {
        try {val token=model.remote.pair(base,entered,c.timeout);if(serverBase(model.config.value)!=base)throw RemoteFailure(message="Server changed; pair again.");model.vault.remember(base,token);message="Phone paired securely.";model.instant.reconnectNow()}
        catch(e: CancellationException){throw e}catch(e: Exception){message=(e as? java.io.IOException)?.message ?: "Pairing unavailable."}
        finally {busy=false}
    }}},enabled=base.isNotEmpty() && pin.isNotBlank() && !busy,shape=Chamfer){Text("Pair with PC")}
    if(message.isNotBlank())Text(message)
}
