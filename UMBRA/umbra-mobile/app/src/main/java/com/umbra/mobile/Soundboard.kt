package com.umbra.mobile

import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.sync.Mutex
import kotlinx.serialization.json.*
import java.time.Instant
import java.util.UUID

data class SoundEntry(val id: String,val name: String,val fields: JsonObject) {
    val favorite get()=fields.truth("favorite")
}
data class SoundCatalog(val revision: Int,val sounds: List<SoundEntry>,val devices: List<JsonObject>,val output: JsonObject?,val player: JsonObject,val deviceError: Boolean,val profile: JsonObject?)
/** Parse the whole real library or fail; an absent/malformed catalog is never an empty success. */
fun parseSoundCatalog(j: JsonObject): SoundCatalog {
    fun check(value: Boolean) {if(!value)throw RemoteFailure(message="Invalid soundboard catalog. Previous snapshot retained; refresh after checking ICARUS.")}
    check(j.number("version")==1.0)
    val revision=j.number("revision");check(revision!=null && revision>=0 && revision<=Int.MAX_VALUE && revision%1==0.0)
    val rows=j["sounds"] as? JsonArray;check(rows!=null)
    val sounds=rows!!.map {value->
        val row=value as? JsonObject ?: throw RemoteFailure(message="Invalid soundboard entry.")
        val id=row.literal("id");val name=row.literal("name")
        check(id!=null && Regex("[a-f0-9]{32}").matches(id));check(!name.isNullOrBlank() && name.length<=48 && name.none(Char::isISOControl))
        check(!row.literal("category").isNullOrBlank() && row.literal("icon")!=null)
        check(row.number("volume")?.let {it in 0.0..1.0}==true && (row["favorite"] as? JsonPrimitive)?.booleanOrNull!=null && (row["favorite"] as? JsonPrimitive)?.isString==false)
        SoundEntry(id!!,name!!,buildJsonObject {listOf("name","category","icon","volume","favorite").forEach {put(it,row.getValue(it))}})
    }
    check(sounds.map {it.id}.distinct().size==sounds.size)
    val devices=j["devices"] as? JsonArray;check(devices!=null)
    fun device(value: JsonElement): JsonObject {
        val d=value as? JsonObject ?: throw RemoteFailure(message="Invalid output device.")
        check(d.number("id")?.let {it>=0 && it<=Int.MAX_VALUE && it%1==0.0}==true && !d.literal("name").isNullOrBlank())
        return buildJsonObject {put("id",d.getValue("id"));put("name",d.getValue("name"))}
    }
    val output=when(val v=j["output"]) {JsonNull->null;null->throw RemoteFailure(message="Missing saved output.");else->device(v)}
    val player=j["player"] as? JsonObject;check(player!=null && player.literal("state") in setOf("idle","starting","playing","error"))
    return SoundCatalog(revision!!.toInt(),sounds,devices!!.map(::device),output,player!!,!j["deviceError"].let {it==null || it==JsonNull},j["audio_profile"] as? JsonObject)
}
data class SoundboardState(val base: String="",val catalog: SoundCatalog?=null,val syncedAt: Instant?=null,val error: String?=null,val busy: Boolean=false,val playbackKnown: Boolean=false)
/** An authenticated adapter to ICARUS, never an audio engine or an independent audio-settings store. */
class SoundboardController(private val request: suspend (Config,String,JsonObject?)->JsonObject) {
    private val mutable=MutableStateFlow(SoundboardState())
    val state=mutable.asStateFlow()
    private val gate=Mutex()
    private suspend fun operation(c: Config,block: suspend ()->Unit) {
        if(!gate.tryLock())return
        val base=serverBase(c)
        if(mutable.value.base!=base)mutable.value=SoundboardState(base)
        mutable.value=mutable.value.copy(busy=true,error=null)
        try {block()}
        catch(e: CancellationException){mutable.value=mutable.value.copy(playbackKnown=false);throw e}
        catch(e: Exception){mutable.value=mutable.value.copy(error=if(e is RemoteFailure)e.message else "Soundboard request failed. Refresh before retrying.",playbackKnown=false)}
        finally {mutable.value=mutable.value.copy(busy=false);gate.unlock()}
    }
    private suspend fun load(c: Config) {
        val catalog=parseSoundCatalog(request(c,"api/sounds/library",null))
        mutable.value=mutable.value.copy(catalog=catalog,syncedAt=Instant.now(),error=null,playbackKnown=true)
    }
    suspend fun sync(c: Config)=operation(c){load(c)}
    suspend fun play(c: Config,id: String)=operation(c){
        require(mutable.value.catalog?.sounds?.any {it.id==id}==true)
        val player=request(c,"api/sounds/play",buildJsonObject {put("id",id);put("requestId",UUID.randomUUID().toString())})
        require(player.literal("state") in setOf("idle","starting","playing","error"))
        mutable.value=mutable.value.copy(catalog=mutable.value.catalog?.copy(player=player),playbackKnown=true)
    }
    suspend fun stop(c: Config)=operation(c){
        request(c,"api/sounds/stop",buildJsonObject {});load(c)
    }
    suspend fun output(c: Config,device: JsonObject)=operation(c){
        val catalog=mutable.value.catalog ?: throw RemoteFailure(message="Sync the catalog first.")
        require(device in catalog.devices)
        request(c,"api/sounds/output",buildJsonObject {put("device",device);put("revision",catalog.revision)})
        load(c) // Read the authoritative saved selection; never save a phone-only output preference.
    }
    suspend fun favorite(c: Config,id: String)=operation(c){
        val catalog=mutable.value.catalog ?: throw RemoteFailure(message="Sync first.")
        val sound=catalog.sounds.first {it.id==id}
        request(c,"api/sounds/edit",buildJsonObject {
            put("id",id);put("revision",catalog.revision)
            put("fields",JsonObject(sound.fields+("favorite" to JsonPrimitive(!sound.favorite))))
        });load(c)
    }
    suspend fun profile(c: Config,fields: JsonObject)=operation(c){
        request(c,"api/audio/profile",fields);load(c)
    }
}
