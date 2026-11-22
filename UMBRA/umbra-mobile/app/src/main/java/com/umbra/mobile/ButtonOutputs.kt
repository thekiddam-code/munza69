package com.umbra.mobile

import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.*

@Serializable enum class OutputKind { QuickChat, Macro, Text, FortniteEmote, MineToggle, ForwardMine, Stop, TvKey, Simulation }
@Serializable data class CustomButton(val id: String=desktopId(),val label: String="New button",val icon: String="◆",val kind: OutputKind=OutputKind.Stop,
    val name: String="",val text: String="",val channel: String="match",val speed: String="balanced",val seconds: Double=3.0,val index: Int=0,val key: String="home",val command: String="pause")
val BUTTON_ICONS=listOf("◆","⚡","⌘","●","▣","▶","■","✦")
val TV_KEYS=listOf("home","back","up","left","ok","right","down","vol_up","vol_down","mute","play_pause","source","power_off","ch_up","ch_down","play","pause","stop","rewind","forward","menu","info","exit")
val SHIP_COMMANDS=listOf("pause","resume","speed1","speed5","speed20","save")
fun validateButton(button: CustomButton): CustomButton {
    require(Regex("[A-Za-z0-9_-]{1,64}").matches(button.id))
    require(button.label.length in 1..48 && button.label.isNotBlank() && button.label.none(Char::isISOControl) && button.icon in BUTTON_ICONS)
    require(button.name.length<=120 && button.name.none(Char::isISOControl) && button.text.length<=120 && button.text.none(Char::isISOControl))
    require(button.channel in listOf("team","match") && button.speed in listOf("fast","balanced","safe"))
    require(button.seconds.isFinite() && button.seconds in .2..10.0 && button.index in 0..8 && button.key in TV_KEYS && button.command in SHIP_COMMANDS)
    if(button.kind in listOf(OutputKind.QuickChat,OutputKind.Macro))require(button.name.isNotBlank())
    if(button.kind==OutputKind.Text)require(button.text.isNotBlank())
    return button
}
fun buttonAction(b: CustomButton): InstantAction {
    validateButton(b)
    require(b.kind!=OutputKind.TvKey){"Retired output is retained for migration only."}
    val path=when(b.kind){OutputKind.TvKey->"api/tv/key";OutputKind.Simulation->"api/icarus/command";else->"api/action"}
    val body=buildJsonObject {when(b.kind) {
        OutputKind.TvKey->put("key",b.key)
        OutputKind.Simulation->put("command",b.command)
        else->{put("action",when(b.kind){OutputKind.QuickChat->"quick";OutputKind.Macro->"macro";OutputKind.Text->"text";OutputKind.FortniteEmote->"fortnite_emote";OutputKind.MineToggle->"mine_toggle";OutputKind.ForwardMine->"forward_mine";else->"stop"})
            when(b.kind){OutputKind.QuickChat,OutputKind.Macro->put("name",b.name);OutputKind.Text->{put("text",b.text);put("channel",b.channel);put("speed",b.speed)};OutputKind.FortniteEmote->put("index",b.index);OutputKind.ForwardMine->put("seconds",b.seconds);else->Unit}
        }
    }}
    return InstantAction("local:${b.id}",b.label,path,body)
}
fun buttonSupport(b: CustomButton,pc: PcStatus?): String?=when {
    pc==null->"Synchronize an authenticated server snapshot first."
    b.kind==OutputKind.QuickChat && b.name !in pc.quick->"Quick-chat name is absent from the current server."
    b.kind==OutputKind.Macro && b.name !in pc.macros->"Macro name is absent from the current server."
    b.kind==OutputKind.FortniteEmote && pc.emotes.none {it.index==b.index}->"Emote slot is unavailable."
    b.kind==OutputKind.TvKey->"Retired output is unavailable."
    else->null
}
fun buttonCatalog(c: Config,pc: PcStatus?): List<InstantAction> =(pc?.let(::instantActions) ?: emptyList())+c.customButtons.filter {it.kind!=OutputKind.TvKey}.map(::buttonAction)
fun chosenButtonIds(c: Config,catalog: List<InstantAction>): Set<String> = c.instantSelection ?: c.instantFavorites.takeIf {it.isNotEmpty()} ?: catalog.map {it.id}.toSet()
@Serializable private data class ButtonFile(val version: Int=1,val buttons: List<CustomButton>)
private val buttonJson=Json {encodeDefaults=true;ignoreUnknownKeys=false}
fun exportButtons(buttons: List<CustomButton>): String=buttonJson.encodeToString(ButtonFile(buttons=buttons.onEach(::validateButton)))
fun validateButtonsJson(value: JsonElement) {
    val list=value as? JsonArray ?: error("Expected buttons");require(list.size<=512)
    list.forEach {strictFields(it,strings=setOf("id","label","icon","kind","name","text","channel","speed","key","command"),ints=setOf("index"),numbers=setOf("seconds"))}
}
fun importButtons(text: String): List<CustomButton> {
    require(text.toByteArray().size<=MAX_CONFIG_BYTES)
    val obj=strictFields(buttonJson.parseToJsonElement(text),ints=setOf("version"),nested=setOf("buttons"))
    require(obj["version"]?.jsonPrimitive?.intOrNull==1);validateButtonsJson(obj["buttons"] ?: error("Missing buttons"))
    val file=buttonJson.decodeFromString<ButtonFile>(text);require(file.buttons.map {it.id}.distinct().size==file.buttons.size)
    return file.buttons.onEach(::validateButton)
}

fun upsertButton(c: Config,b: CustomButton,pc: PcStatus?,replaceSource: String?=null): Config {
    validateButton(b)
    val id="local:${b.id}"
    val chosen=chosenButtonIds(c,buttonCatalog(c,pc))
    val selection=if(replaceSource!=null)chosen-replaceSource+id else if(c.instantSelection!=null || c.instantFavorites.isNotEmpty())chosen+id else null
    return c.copy(customButtons=c.customButtons.filterNot {it.id==b.id}+b,instantSelection=selection,
        widgetButtonSelections=if(replaceSource==null)c.widgetButtonSelections else c.widgetButtonSelections.mapValues {(_,ids)->ids.map {if(it==replaceSource)id else it}.distinct()},
        gridLayouts=if(replaceSource==null)c.gridLayouts else c.gridLayouts.mapValues {(_,grid)->grid.copy(cells=grid.cells.map {if(it.id==replaceSource)it.copy(id=id) else it})})
}
fun deleteButton(c: Config,id: String): Config = c.copy(customButtons=c.customButtons.filterNot {"local:${it.id}"==id},instantSelection=c.instantSelection?.minus(id),
    widgetButtonSelections=c.widgetButtonSelections.mapValues {(_,ids)->ids-id},instantOrder=c.instantOrder-id,instantLabels=c.instantLabels-id,
    gridLayouts=c.gridLayouts.mapValues {(_,grid)->grid.copy(cells=grid.cells.filterNot {it.id==id})})
