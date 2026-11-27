package com.umbra.mobile

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.*
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.*
import androidx.lifecycle.repeatOnLifecycle
import kotlinx.coroutines.*
import java.io.ByteArrayOutputStream

@OptIn(ExperimentalFoundationApi::class)
@Composable fun InstantControls(c: Config,model: LauncherModel,visible: Boolean,compact: Boolean,surface: String="instant-controls",widgetId: String?=null,filter: String="",headingModifier: Modifier=Modifier,soundState: SoundboardState?=null,runSound: (((suspend ()->Unit))->Unit)?=null) {
    val snapshot by model.instant.state.collectAsStateWithLifecycle()
    val lifecycle=LocalLifecycleOwner.current.lifecycle;val scope=rememberCoroutineScope();val context=LocalContext.current
    val editing=LocalGridEditing.current
    var soundEdit by remember {mutableStateOf<String?>(null)}
    var work by remember {mutableStateOf<Job?>(null)};var manager by remember {mutableStateOf(false)}
    var edited by remember {mutableStateOf<CustomButton?>(null)};var editedSource by remember {mutableStateOf<String?>(null)};var picker by remember {mutableStateOf(false)}
    var imported by remember {mutableStateOf<List<CustomButton>?>(null)};var fileMessage by remember {mutableStateOf("")}
    val current=snapshot.takeIf {it.base==serverBase(c)} ?: InstantSnapshot(status="Sync controls or pair this phone in ICARUS.")
    val connection by model.instant.pcConnection.collectAsStateWithLifecycle()
    val spec=widgetId?.let {widgetSpec(c,it)}
    val actualFilter=spec?.buttonSet ?: filter
    val mixed=actualFilter=="mixed"
    val soundCatalog=soundState?.catalog.takeIf {mixed}
    val catalog=(widgetCatalog(c,current.pc,widgetId,connection.catalog.takeIf {connection.base==serverBase(c)})+soundButtonActions(soundCatalog)).sortedBy {c.instantOrder.indexOf(it.id).takeIf {i->i>=0} ?: Int.MAX_VALUE}
    val selected=widgetId?.let {c.widgetButtonSelections[it]?.toSet() ?: catalog.map {a->a.id}.toSet()} ?: catalog.map {it.id}.toSet()
    val missing=selected.count {id->catalog.none {it.id==id}}
    val actions=catalog.filter {action->action.id in selected && simulatorAllows(actualFilter,action,c)}
    LifecycleStartEffect(Unit){onStopOrDispose {work?.cancel()}}
    LaunchedEffect(lifecycle,visible,serverBase(c),c.refreshOnResume){if(visible && c.refreshOnResume)lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED){model.instant.refresh(c,engineering=widgetId!=null)}}
    val export=rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument("application/json")){uri->if(uri!=null)scope.launch {
        try {withContext(Dispatchers.IO){context.contentResolver.openOutputStream(uri,"wt")?.use {it.write(exportButtons(c.customButtons).toByteArray())} ?: error("No output")};fileMessage="Buttons saved; credentials excluded."}catch(e:CancellationException){throw e}catch(_:Exception){fileMessage="Could not export buttons."}
    }}
    val load=rememberLauncherForActivityResult(ActivityResultContracts.OpenDocument()){uri->if(uri!=null)scope.launch {
        try {imported=withContext(Dispatchers.IO){context.contentResolver.openInputStream(uri)?.use {input->val out=ByteArrayOutputStream();val buffer=ByteArray(4096);while(true){val n=input.read(buffer);if(n<0)break;require(out.size()+n<=MAX_CONFIG_BYTES);out.write(buffer,0,n)};importButtons(out.toByteArray().decodeToString(throwOnInvalidSequence=true))} ?: error("No input")}}catch(e:CancellationException){throw e}catch(_:Exception){fileMessage="Invalid button file; current buttons preserved."}
    }}
    Column(if(compact)Modifier.fillMaxSize() else Modifier.fillMaxWidth(),verticalArrangement=Arrangement.spacedBy(4.dp)) {
        Row(Modifier.fillMaxWidth(),verticalAlignment=androidx.compose.ui.Alignment.CenterVertically) {
            Column(Modifier.weight(1f).heightIn(min=48.dp).then(headingModifier).testTag("instant-editor-header")) {
                Text(spec?.title?.takeIf {it.isNotBlank()} ?: if(widgetId!=null)"Button widget" else "Game controls",style=MaterialTheme.typography.titleMedium)
                if(current.synchronizedAt>0)Text("Sync ${java.text.DateFormat.getTimeInstance().format(java.util.Date(current.synchronizedAt))}",style=MaterialTheme.typography.bodySmall)
            }
            TextButton(onClick={if(work?.isActive!=true)work=scope.launch {model.instant.refresh(c,true,engineering=widgetId!=null)};if(mixed)runSound?.invoke {model.soundboard.sync(c)}},enabled=!current.busy && soundState?.busy!=true){Text("Sync")}
            if(mixed)TextButton(onClick={runSound?.invoke {model.soundboard.stop(c)}},enabled=soundCatalog!=null && soundState?.busy!=true){Text("Stop")}
        }
        Text(current.status+(if(missing>0)" · $missing selected buttons unavailable; selections retained." else ""),style=MaterialTheme.typography.bodySmall,maxLines=if(compact)2 else 4,modifier=Modifier.semantics {liveRegion=LiveRegionMode.Polite})
        if(mixed)Text("Sounds: ${soundCatalog?.sounds?.size ?: 0} loaded · "+(if(soundState?.playbackKnown==true)soundCatalog?.player?.literal("state") ?: "unknown" else "status unknown"),style=MaterialTheme.typography.labelSmall)
        if(mixed)soundState?.error?.let {Text(it,color=MaterialTheme.colorScheme.error,style=MaterialTheme.typography.labelSmall,modifier=Modifier.semantics {liveRegion=LiveRegionMode.Polite})}
        if(actions.isEmpty())Text("Configure a widget to choose or add buttons. Pair in ICARUS configuration to discover server controls.",style=MaterialTheme.typography.bodySmall)
        val boardModifier=if(compact)Modifier.weight(1f) else Modifier.heightIn(max=560.dp)
        Column(boardModifier.fillMaxWidth().verticalScroll(rememberScrollState())) {
            GridBoard(surface,actions.map {GridItem(it.id,if(widgetId!=null)it.label else c.instantLabels[it.id] ?: it.label)},c,model,columns=spec?.buttonColumns ?: 2,cellHeight=(spec?.buttonHeight ?: 64).dp,rowMajor=true,maxColumns=12,
                onConfigure=if(widgetId==null)null else {id->editing.finish();if(id.startsWith("sound:"))soundEdit=id.removePrefix("sound:") else {editedSource=id;edited=spec?.buttonOverrides?.get(id) ?: actionCopy(catalog.first {it.id==id})}},
                onRemove=if(widgetId==null)null else {id->model.change {old->old.copy(widgetButtonSelections=old.widgetButtonSelections+(widgetId to (selected-id).toList()))}}) {item,_->
                val action=actions.first {it.id==item.id}
                val local=spec?.buttonOverrides?.get(item.id) ?: c.customButtons.firstOrNull {"local:${it.id}"==item.id}
                val isSound=action.path=="api/sounds/play"
                CategoryControlButton((local?.icon?.plus(" ") ?: "")+(if(widgetId!=null)action.label else c.instantLabels[item.id] ?: action.label),buttonFamily(action),
                    if(isSound)soundState?.busy==false else !current.busy,Modifier.fillMaxSize().testTag("instant-action-${item.id}")) {
                    if(isSound)runSound?.invoke {model.soundboard.play(c,action.id.removePrefix("sound:"))}
                    else if(work?.isActive!=true)work=scope.launch {model.instant.execute(c,action.id,widgetId)}
                }
            }
        }
        if(fileMessage.isNotEmpty())Text(fileMessage,style=MaterialTheme.typography.bodySmall)
    }
    soundEdit?.let {id->soundCatalog?.sounds?.firstOrNull {it.id==id}?.let {sound->
        AlertDialog(onDismissRequest={soundEdit=null},title={Text(sound.name)},text={Text("Favorite flags are shared with ICARUS; this widget's grid and selection are independent.")},
            confirmButton={TextButton(onClick={soundEdit=null;runSound?.invoke {model.soundboard.favorite(c,id)}},enabled=soundState?.busy!=true){Text(if(sound.favorite)"Remove favorite" else "Favorite")}},
            dismissButton={TextButton(onClick={soundEdit=null}){Text("Close")}})
    }}
    if(manager)DesktopEditorDialog("Button widget",{manager=false},confirm={TextButton(onClick={manager=false}){Text("Done")}}) {
        TextButton(onClick={editedSource=null;edited=CustomButton();manager=false}){Text("Create button")}
        TextButton(onClick={picker=true;manager=false}){Text("Select buttons")}
        TextButton(onClick={export.launch("umbra-buttons.json")}){Text("Save button configurations")}
        TextButton(onClick={load.launch(arrayOf("application/json","text/plain"))}){Text("Load button configurations")}
        TextButton(onClick={model.restoreGridItems(surface);manager=false}){Text("Restore hidden buttons")}
        Text("Local customizations use the existing authenticated ICARUS command APIs. Long-press any button to configure, resize, duplicate, remove, or drag it.")
    }
    if(picker)DesktopEditorDialog("Select buttons",{picker=false},confirm={TextButton(onClick={picker=false}){Text("Done")}}){ButtonSelection(c,model,widgetId,actualFilter)}
    edited?.let {button->ButtonEditor(button,c,current.pc,model,{edited=null;editedSource=null},editedSource,widgetId)}
    imported?.let {buttons->DesktopEditorDialog("Import ${buttons.size} buttons?",{imported=null},confirm={TextButton(onClick={model.change {old->old.copy(customButtons=old.customButtons.filterNot {saved->buttons.any {it.id==saved.id}}+buttons)};imported=null}){Text("Merge buttons")}}) {
        Text("This merges by stable button ID and does not execute commands or modify the server. Export current buttons before replacing an existing ID.")
        TextButton(onClick={export.launch("umbra-buttons-backup.json")}){Text("Back up current buttons")}
    }}
}
@Composable fun ButtonSelection(c: Config,model: LauncherModel,widgetId: String?=null,filter: String="all",draft: Set<String>?=null,onDraft: ((Set<String>)->Unit)?=null,specOverride: DesktopWidget?=null) {
    val snapshot by model.instant.state.collectAsStateWithLifecycle()
    val connection by model.instant.pcConnection.collectAsStateWithLifecycle()
    val sounds by model.soundboard.state.collectAsStateWithLifecycle()
    val catalog=widgetCatalog(c,snapshot.pc.takeIf {snapshot.base==serverBase(c)},widgetId,connection.catalog.takeIf {connection.base==serverBase(c)},specOverride).filter {simulatorAllows(filter,it,c)}+
        (if(filter=="mixed")soundButtonActions(sounds.catalog.takeIf {sounds.base==serverBase(c)}) else emptyList())
    val scope=rememberCoroutineScope();var sync by remember {mutableStateOf<Job?>(null)}
    LifecycleStartEffect(widgetId,filter){onStopOrDispose {sync?.cancel()}}
    if(filter=="mixed")TextButton(onClick={if(sync?.isActive!=true)sync=scope.launch {model.instant.refresh(c,true,true);model.soundboard.sync(c)}}){Text("Sync commands and sounds")}
    if(filter=="mixed")sounds.error?.takeIf {sounds.base==serverBase(c)}?.let {Text(it,color=MaterialTheme.colorScheme.error)}
    var query by remember {mutableStateOf("")}
    val selected=if(onDraft!=null)draft ?: catalog.map {it.id}.toSet() else widgetId?.let {c.widgetButtonSelections[it]?.toSet() ?: catalog.map {a->a.id}.toSet()} ?: chosenButtonIds(c,catalog)
    fun set(ids: Set<String>) {if(onDraft!=null)onDraft(ids) else model.change {old->if(widgetId==null)old.copy(instantSelection=ids) else old.copy(widgetButtonSelections=old.widgetButtonSelections+(widgetId to ids.toList()))}}
    OutlinedTextField(query,{query=it},label={Text("Search available buttons")},singleLine=true,modifier=Modifier.fillMaxWidth())
    Row {TextButton(onClick={set(catalog.map {it.id}.toSet())}){Text("Select all")};TextButton(onClick={set(emptySet())}){Text("Deselect all")}}
    Text("${selected.intersect(catalog.map {it.id}.toSet()).size} selected · ${catalog.size} available",style=MaterialTheme.typography.bodySmall)
    LazyColumn(Modifier.fillMaxWidth().heightIn(max=320.dp)) {items(catalog.filter {it.label.contains(query,true)},key={it.id}) {action->Row(verticalAlignment=androidx.compose.ui.Alignment.CenterVertically) {
        Checkbox(action.id in selected,{checked->set(if(checked)selected+action.id else selected-action.id)});Column {Text(action.label);Text(buttonFamily(action).label,color=buttonFamily(action).color,style=MaterialTheme.typography.labelSmall)}
    }}}
}
fun actionCopy(action: InstantAction): CustomButton {
    val body=action.body
    require(action.path in listOf("api/action","api/tv/key","api/icarus/command","api/windows/command")){"Unsupported server output"}
    val kind=when(action.path){"api/windows/command"->OutputKind.WindowsHotkey;"api/tv/key"->OutputKind.TvKey;"api/icarus/command"->OutputKind.Simulation;else->when(body.literal("action")){"quick"->OutputKind.QuickChat;"macro"->OutputKind.Macro;"text"->OutputKind.Text;"fortnite_emote"->OutputKind.FortniteEmote;"mine_toggle"->OutputKind.MineToggle;"forward_mine"->OutputKind.ForwardMine;"stop"->OutputKind.Stop;else->error("Unsupported server output")}}
    return CustomButton(label=action.label.take(48),kind=kind,name=body.literal("name") ?: body.literal("id") ?: "",text=body.literal("text") ?: "",channel=body.literal("channel") ?: "match",speed=body.literal("speed") ?: "balanced",index=body.number("index")?.toInt() ?: 0,seconds=body.number("seconds") ?: 3.0,key=body.literal("key") ?: "home",command=body.literal("command") ?: "pause")
}
@Composable fun ButtonEditor(original: CustomButton,c: Config,pc: PcStatus?,model: LauncherModel,close: ()->Unit,replaceSource: String?=null,widgetId: String?=null,saveDraft: ((CustomButton)->Unit)?=null) {
    var b by remember(original.id){mutableStateOf(original)}
    var seconds by remember {mutableStateOf(b.seconds.toString())}
    val scope=rememberCoroutineScope();var job by remember {mutableStateOf<Job?>(null)}
    LifecycleStartEffect(Unit){onStopOrDispose {job?.cancel()}}
    val valid=runCatching {validateButton(b)}.isSuccess && (b.kind!=OutputKind.ForwardMine || seconds.toDoubleOrNull()?.let {it in .2..10.0}==true)
    DesktopEditorDialog("Configure button",close,confirm={TextButton(onClick={val saved=b;if(saveDraft!=null)saveDraft(saved) else model.change {old->if(widgetId!=null && replaceSource!=null)overrideWidgetButton(old.copy(desktop=resolvedDesktop(old,model.apps.value)),widgetId,replaceSource,saved) else upsertButton(old,saved,pc,replaceSource)};close()},enabled=valid){Text(if(replaceSource==null)"Save button" else "Save UMBRA override")}}) {
        if(replaceSource!=null)Text("This edits the UMBRA copy and preserves its placement. The PC mapping is unchanged.")
        OutlinedTextField(b.label,{b=b.copy(label=it.take(48))},label={Text("Button name")},singleLine=true)
        Choice("Icon",BUTTON_ICONS,b.icon){b=b.copy(icon=it)}
        Choice("Output",OutputKind.entries.filter {it!=OutputKind.TvKey}.map {it.name},b.kind.name){b=b.copy(kind=OutputKind.valueOf(it))}
        when(b.kind) {
            OutputKind.QuickChat,OutputKind.Macro->{
                val names=if(b.kind==OutputKind.QuickChat)pc?.quick ?: emptyList() else pc?.macros ?: emptyList()
                OutlinedTextField(b.name,{b=b.copy(name=it.take(120))},label={Text("Exact configured server name")},singleLine=true)
                if(names.isNotEmpty())Choice("Current server choices",names,b.name){b=b.copy(name=it)}
            }
            OutputKind.Text->{OutlinedTextField(b.text,{b=b.copy(text=it.take(120))},label={Text("Message (1–120 characters)")});Choice("Channel",listOf("match","team"),b.channel){b=b.copy(channel=it)};Choice("Timing",listOf("fast","balanced","safe"),b.speed){b=b.copy(speed=it)}}
            OutputKind.FortniteEmote->Choice("Configured emote slot",(0..8).map {it.toString()},b.index.toString()){b=b.copy(index=it.toInt())}
            OutputKind.ForwardMine->{OutlinedTextField(seconds,{seconds=it;it.toDoubleOrNull()?.let {value->b=b.copy(seconds=value)}},label={Text("Hold duration · 0.2–10 seconds")},singleLine=true,isError=seconds.toDoubleOrNull()?.let {it !in .2..10.0} ?: true);Text("Server holds forward + mining, then releases on its existing timer.")}
            OutputKind.MineToggle->Text("Toggle server-held mining input; server applies its 60-second safety release.")
            OutputKind.Stop->Text("Release inputs currently held by the server.")
            OutputKind.TvKey->Text("Retired output is unavailable.")
            OutputKind.WindowsHotkey->OutlinedTextField(b.name,{b=b.copy(name=it.take(64))},label={Text("Advertised Windows hotkey ID")},singleLine=true)
            OutputKind.Simulation->Choice("Supported simulation command",SHIP_COMMANDS,b.command){b=b.copy(command=it)}
        }
        val unsupported=buttonSupport(b,pc);if(unsupported!=null)Text(unsupported)
        Text("Arbitrary key-down/key-up, arbitrary scripts, and generic hold protocols are not exposed by this server and are unsupported. Existing timed mining and Stop are supported.",style=MaterialTheme.typography.bodySmall)
        TextButton(onClick={if(job?.isActive!=true)job=scope.launch {
            val temp=c.copy(customButtons=c.customButtons.filterNot {it.id==b.id}+b)
            model.instant.execute(temp,"local:${b.id}")
        }},enabled=valid && unsupported==null){Text("Test command")}
        val response by model.instant.state.collectAsStateWithLifecycle();Text(response.status,modifier=Modifier.semantics {liveRegion=LiveRegionMode.Polite})
        if(c.customButtons.any {it.id==b.id})TextButton(onClick={val id=b.id;model.change {deleteButton(it,"local:$id")};close()}){Text("Delete button")}
    }
}

fun simulatorAllows(filter: String,action: InstantAction,c: Config): Boolean {
    val type=action.body.literal("action")
    return when(filter) {
        "pc"->action.path=="api/windows/command" || type in listOf("macro","stop")
        "rocket"->type in listOf("quick","text")
        "fortnite"->type=="fortnite_emote"
        "minecraft"->type in listOf("mine_toggle","forward_mine","stop")
        "simulation"->action.path=="api/icarus/command"
        else->true
    }
}
