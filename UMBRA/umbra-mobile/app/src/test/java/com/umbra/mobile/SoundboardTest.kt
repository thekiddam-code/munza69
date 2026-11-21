package com.umbra.mobile

import kotlinx.coroutines.*
import kotlinx.serialization.json.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Test
import java.util.concurrent.TimeUnit

fun soundFixture(count: Int=14,revision: Int=7,output: JsonElement=JsonNull): JsonObject=buildJsonObject {
    put("version",1);put("revision",revision);put("output",output)
    put("sounds",buildJsonArray {repeat(count){i->add(buildJsonObject {
        put("id",i.toString(16).padStart(32,'0'));put("name","Existing sound $i");put("category","Original");put("icon","play");put("volume",0.35);put("favorite",false)
    })}})
    put("devices",buildJsonArray {add(buildJsonObject {put("id",2);put("name","Existing render output")})})
    put("deviceError",JsonNull);put("player",buildJsonObject {put("state","idle");put("error",JsonNull)})
}
class SoundboardTest {
    private val c=Config(serverUrl="http://localhost:9000/")
    @Test fun parsesEveryExistingSoundAndRejectsPartialOrDuplicateCatalogs() {
        assertEquals(64,parseSoundCatalog(soundFixture(64)).sounds.size)
        for(bad in listOf(JsonObject(emptyMap()),JsonObject(soundFixture()-"sounds"),JsonObject(soundFixture()+("sounds" to buildJsonArray {add(soundFixture()["sounds"]!!.jsonArray[0]);add(soundFixture()["sounds"]!!.jsonArray[0])})))) {
            assertTrue(runCatching {parseSoundCatalog(bad)}.exceptionOrNull() is RemoteFailure)
        }
    }
    @Test fun failedSyncNeverUpdatesSuccessTimestampOrErasesPriorCatalog()=runBlocking {
        var response=soundFixture()
        val ctl=SoundboardController {_,_,_->response}
        ctl.sync(c);val first=ctl.state.value
        response=buildJsonObject {};ctl.sync(c)
        assertEquals(first.syncedAt,ctl.state.value.syncedAt);assertEquals(14,ctl.state.value.catalog!!.sounds.size)
        assertNotNull(ctl.state.value.error);assertFalse(ctl.state.value.playbackKnown)
        ctl.sync(c.copy(serverUrl="http://localhost:9001/"));assertNull(ctl.state.value.syncedAt);assertNull(ctl.state.value.catalog)
    }
    @Test fun nativePlaybackUsesOriginalAuthenticatedSoundRouteAndUniqueRequestId()=runBlocking {
        val server=MockWebServer();server.start();val remote=IcarusClient()
        val config=c.copy(serverUrl=server.url("/").toString())
        val ctl=SoundboardController {cfg,path,body->remote.request(serverBase(cfg),path,cfg.timeout,"test-token",body)}
        try {
            server.enqueue(MockResponse().setBody(soundFixture().toString()));ctl.sync(config)
            val get=server.takeRequest();assertEquals("/api/sounds/library",get.path);assertEquals("Bearer test-token",get.getHeader("Authorization"))
            val id=ctl.state.value.catalog!!.sounds[12].id
            server.enqueue(MockResponse().setBody("""{"state":"playing","id":"$id"}"""));ctl.play(config,id)
            val play=server.takeRequest();assertEquals("/api/sounds/play",play.path);assertEquals("Bearer test-token",play.getHeader("Authorization"))
            val body=Json.parseToJsonElement(play.body.readUtf8()).jsonObject
            assertEquals(setOf("id","requestId"),body.keys);assertEquals(id,body.literal("id"));assertTrue(body.literal("requestId")!!.length>=8)
            assertEquals("playing",ctl.state.value.catalog!!.player.literal("state"))
            server.enqueue(MockResponse().setResponseCode(409));ctl.play(config,id)
            assertFalse(ctl.state.value.playbackKnown);assertNotNull(ctl.state.value.error)
            assertEquals(3,server.requestCount) // no automatic replay or quick-chat request
        } finally {remote.close();server.shutdown()}
    }
    @Test fun outputAndFavoritesAreRevisionCheckedAndReadBackFromServer()=runBlocking {
        var authoritative=soundFixture();val requests=mutableListOf<Pair<String,JsonObject?>>()
        val transport: suspend (Config,String,JsonObject?)->JsonObject={_,path,body->
            requests+=path to body
            when(path) {
                "api/sounds/output"->{assertEquals(7,body!!["revision"]!!.jsonPrimitive.int);authoritative=soundFixture(revision=8,output=body.getValue("device"));authoritative}
                "api/sounds/edit"->{assertEquals(8,body!!["revision"]!!.jsonPrimitive.int);val fields=body["fields"]!!.jsonObject;assertTrue(fields.truth("favorite"));assertEquals("Original",fields.literal("category"));assertEquals(0.35,fields.number("volume")!!,0.0)
                    authoritative=JsonObject(authoritative+("revision" to JsonPrimitive(9))+("sounds" to JsonArray(authoritative["sounds"]!!.jsonArray.map {row->if(row.jsonObject.literal("id")==body.literal("id"))JsonObject(row.jsonObject+fields) else row})));authoritative}
                else->authoritative
            }
        }
        val ctl=SoundboardController(transport);ctl.sync(c);val device=ctl.state.value.catalog!!.devices.first()
        ctl.output(c,device);assertEquals(device,ctl.state.value.catalog!!.output)
        ctl.favorite(c,ctl.state.value.catalog!!.sounds.first().id);assertTrue(ctl.state.value.catalog!!.sounds.first().favorite)
        val restarted=SoundboardController(transport);restarted.sync(c);assertEquals(device,restarted.state.value.catalog!!.output);assertTrue(restarted.state.value.catalog!!.sounds.first().favorite)
        assertEquals(listOf("api/sounds/library","api/sounds/output","api/sounds/library","api/sounds/edit","api/sounds/library","api/sounds/library"),requests.map {it.first})
    }
    @Test fun rapidTapsDoNotQueueAndCancellationReleasesGate()=runBlocking {
        var plays=0;val started=CompletableDeferred<Unit>()
        val ctl=SoundboardController {_,path,_->if(path=="api/sounds/play"){plays++;started.complete(Unit);awaitCancellation()} else soundFixture()}
        ctl.sync(c);val id=ctl.state.value.catalog!!.sounds.first().id
        val job=launch {ctl.play(c,id)};started.await();ctl.play(c,id);assertEquals(1,plays)
        job.cancelAndJoin();assertFalse(ctl.state.value.busy);assertFalse(ctl.state.value.playbackKnown)
        ctl.sync(c);assertTrue(ctl.state.value.playbackKnown)
    }
    @Test fun stopUsesExistingEmptyBodyAndReportsFreshPlayerState()=runBlocking {
        val calls=mutableListOf<String>()
        val ctl=SoundboardController {_,path,body->calls+=path;if(path.endsWith("stop")){assertEquals(buildJsonObject {},body);buildJsonObject {put("state","idle")}} else soundFixture()}
        ctl.sync(c);ctl.stop(c);assertEquals(listOf("api/sounds/library","api/sounds/stop","api/sounds/library"),calls);assertEquals("idle",ctl.state.value.catalog!!.player.literal("state"))
    }
    @Test fun optionalNormalizationUsesOnlyAdvertisedServerProfileAndExistingFields()=runBlocking {
        assertNull(parseSoundCatalog(soundFixture()).profile)
        var profile=buildJsonObject {put("enabled",false);put("offset_db",-3);put("ceiling_dbfs",-1);put("max_boost_db",6);put("speech",buildJsonObject {put("integrated_lufs",-20)})}
        var updates=0
        val ctl=SoundboardController {_,path,body->
            if(path=="api/audio/profile") {
                updates++;assertEquals(setOf("enabled","offset_db","ceiling_dbfs","max_boost_db"),body!!.keys)
                profile=JsonObject(profile+body);profile
            } else JsonObject(soundFixture()+("audio_profile" to profile))
        }
        ctl.sync(c)
        ctl.profile(c,buildJsonObject {put("enabled",true);put("offset_db",-6);put("ceiling_dbfs",-2);put("max_boost_db",3)})
        assertEquals(1,updates);assertTrue(ctl.state.value.catalog!!.profile!!.truth("enabled"));assertEquals(-6.0,ctl.state.value.catalog!!.profile!!.number("offset_db")!!,0.0)
    }

}
