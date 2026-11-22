package com.umbra.mobile

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.LifecycleStartEffect
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.repeatOnLifecycle
import kotlinx.coroutines.*
import kotlinx.serialization.json.*

/** Existing ship controls stay in SIMULATOR; PC Engineering never sends game commands. */
@Composable fun SimulationControls(c: Config,model: LauncherModel) {
    val lifecycle=LocalLifecycleOwner.current.lifecycle
    val scope=rememberCoroutineScope();var ship by remember(serverBase(c)){mutableStateOf<ShipStatus?>(null)}
    var work by remember {mutableStateOf<Job?>(null)};var message by remember {mutableStateOf("Not synchronized")};var refresh by remember {mutableIntStateOf(0)}
    LifecycleStartEffect(serverBase(c)){onStopOrDispose {work?.cancel()}}
    LaunchedEffect(lifecycle,serverBase(c),c.timeout,refresh) {
        lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED) {
        try {val token=model.vault.read(serverBase(c)) ?: throw RemoteFailure(401,"Pair native controls in ICARUS.");ship=model.remote.ship(serverBase(c),token,c.timeout);message=if(ship?.online==true)"Simulation online at last refresh" else "Simulation offline"}
        catch(e: CancellationException){throw e}catch(e: Exception){ship=null;message=(e as? RemoteFailure)?.message ?: "Simulation telemetry unavailable"}
        }
    }
    Column(Modifier.fillMaxWidth(),verticalArrangement=Arrangement.spacedBy(8.dp)) {
        Text(message);TextButton(onClick={refresh++}){Text("Refresh simulation")}
        SHIP_COMMANDS.forEach {command->TextButton(onClick={if(work?.isActive!=true)work=scope.launch {
            try {
                val token=model.vault.read(serverBase(c)) ?: throw RemoteFailure(401,"Pair native controls first.")
                val result=model.remote.request(serverBase(c),"api/icarus/command",c.timeout,token,buildJsonObject {put("command",command)})
                message=result.number("queued")?.let {"Queued #${it.toInt()} · PC execution pending"} ?: "Server acknowledged simulation command."
            }catch(e: CancellationException){throw e}catch(e: Exception){message=(e as? RemoteFailure)?.message ?: "Command unavailable"}
        }},enabled=ship?.online==true && work?.isActive!=true){Text(command)}}
    }
}
