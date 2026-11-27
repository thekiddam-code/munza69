package com.umbra.mobile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlinx.serialization.json.*

@Composable fun HostActionDialogs(c: Config,model: LauncherModel,widgetId: String?,current: InstantSnapshot,info: String?,closeInfo: ()->Unit) {
    val scope=rememberCoroutineScope()
    if(info!=null)AlertDialog(onDismissRequest=closeInfo,title={Text(if(info=="host:arctis")"Switch to Arctis" else "Save Clip")},text={Text(if(info=="host:arctis")"Changes only Game, Chat, Media and Aux on the paired PC. The host remembers the chosen Arctis output after readback. Microphone and VoiceMeeter controls are excluded." else "Uses the PC's current Save Clip macro through the host-actions API. Clip creation is unconfirmed until a new stable video file is observed. Confirm capture is active in Moments.")},confirmButton={TextButton(onClick=closeInfo){Text("Close")}})
    val result=current.hostResult.takeIf {current.hostWidgetId==widgetId}
    if(result?.literal("state")=="selection_required") {
        val choices=(result["outputs"] as? JsonArray)?.mapNotNull {it as? JsonObject}?.take(32)?.filter {it.literal("id")?.isNotBlank()==true && it.literal("name")?.isNotBlank()==true} ?: emptyList()
        AlertDialog(onDismissRequest={model.instant.dismissHostResult(widgetId)},title={Text("Choose Arctis output")},text={Column(Modifier.fillMaxWidth().heightIn(max=360.dp).verticalScroll(rememberScrollState())) {
            Text(result.literal("message") ?: result.literal("error") ?: "No output has been changed.")
            choices.forEach {choice->TextButton(onClick={val id=choice.literal("id")!!;model.instant.dismissHostResult(widgetId);scope.launch {model.instant.executeHost(c,"host:arctis",widgetId,id)}},enabled=!current.busy,modifier=Modifier.fillMaxWidth().heightIn(min=48.dp)){Text(choice.literal("name")!!)}}
        }},confirmButton={TextButton(onClick={model.instant.dismissHostResult(widgetId)}){Text("Cancel")}})
    }
}
