package com.umbra.mobile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalLayoutApi::class)
@Composable fun DeckScreen(c: Config,model: LauncherModel,section: String,onSection: (String)->Unit,deviceControls: @Composable ()->Unit) {
    Column(Modifier.fillMaxSize()) {
        FlowRow(horizontalArrangement=Arrangement.spacedBy(4.dp)) {
            listOf("Engineering","Device controls").forEach {name->FilterChip(selected=section==name,onClick={onSection(name)},modifier=Modifier.testTag("deck-section-$name"),label={Text(name,style=MaterialTheme.typography.labelSmall)})}
        }
        if(section=="Device controls")deviceControls()
        else Column(Modifier.weight(1f).fillMaxWidth().verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(12.dp)) {when(section) {
            "Engineering"->{
                var module by rememberSaveable {mutableStateOf("cpu")}
                Readout("ENGINEERING / WINDOWS COMPANION",MaterialTheme.colorScheme.primary)
                FlowRow {ENGINEERING_MODULES.forEach {kind->FilterChip(selected=module==kind,onClick={module=kind},label={Text(kind.uppercase())})}}
                EngineeringModule(module,c,model)
                Text("Readings come from the existing companion. Missing, stale and unsupported sensors remain unavailable.",style=MaterialTheme.typography.bodySmall)
            }
            else->Text("Select Engineering or Device controls.")
        }}
    }
}
@OptIn(ExperimentalLayoutApi::class)
@Composable fun SimulatorScreen(c: Config,model: LauncherModel,open: (android.content.Intent)->Unit) {
    var game by rememberSaveable {mutableStateOf("Rocket League")}
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()),verticalArrangement=Arrangement.spacedBy(10.dp)) {
        Readout("SIMULATOR / GAME CONTROLS",MaterialTheme.colorScheme.primary)
        FlowRow {listOf("Rocket League","Fortnite","Minecraft","Soundboard","Simulation").forEach {name->FilterChip(selected=game==name,onClick={game=name},label={Text(name)})}}
        TextButton(onClick={open(android.content.Intent(android.content.Intent.ACTION_VIEW,android.net.Uri.parse(remoteDestination(c,"Simulator"))))},enabled=validDeckUrl(remoteDestination(c,"Simulator"))){Text("Open Simulator Remote Deck")}
        if(game=="Soundboard")SoundboardScreen(c,model)
        if(game=="Simulation")SimulationControls(c,model)
        if(game!="Soundboard")InstantControls(c,model,true,false,surface="simulator-${game.lowercase().replace(' ','-')}",filter=when(game){"Rocket League"->"rocket";"Fortnite"->"fortnite";"Minecraft"->"minecraft";else->"simulation"})
    }
}
