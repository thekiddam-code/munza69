package com.umbra.mobile

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.lifecycle.ViewModelProvider
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.first
import kotlinx.serialization.json.*
import okhttp3.mockwebserver.*
import org.junit.Assert.*
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config as RoboConfig
import org.robolectric.annotation.GraphicsMode
import org.robolectric.annotation.LooperMode

@RunWith(RobolectricTestRunner::class)
@RoboConfig(sdk=[30,34],qualifiers="w432dp-h936dp-port-xhdpi")
@LooperMode(LooperMode.Mode.PAUSED)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class Host33HostUiTest {
    private val rule=createAndroidComposeRule<MainActivity>()
    @get:Rule val rules=org.junit.rules.RuleChain.outerRule(object: org.junit.rules.ExternalResource() {
        override fun before() {
            val app=org.robolectric.RuntimeEnvironment.getApplication()
            org.robolectric.Shadows.shadowOf(app).grantPermissions("com.umbra.mobile.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION")
            runBlocking {ConfigStore(app).replace(Config(master=false,immersive=true,statusPanel=false,pcIndicator=false))}
        }
    }).around(rule)
    private fun config()=runBlocking {ConfigStore(rule.activity).config.first()}
    private fun waitFor(condition: ()->Boolean){rule.waitUntil(7000){org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();condition()}}
    private fun enabled(tag: String)=waitFor {rule.onAllNodesWithTag(tag).fetchSemanticsNodes().any {!it.config.contains(androidx.compose.ui.semantics.SemanticsProperties.Disabled)}}
    @Test fun exitingFullscreenHasOneRecoveryButtonAndRetainsSelectedPresetPageAndNavigation() {
        val model=ViewModelProvider(rule.activity)[LauncherModel::class.java]
        val layout=DesktopLayout(pages=listOf(DesktopPage("main","First page"),DesktopPage("second","Second page",items=listOf(DesktopItem("clock","widget",widget=DesktopWidget(rows=2))))))
        val c=config().copy(activeHomePreset="ops",homePresets=listOf(HomePreset("ops","Operations",layout)),desktop=layout)
        runBlocking {model.store.replace(c)};waitFor {config().activeHomePreset=="ops"}
        rule.onNodeWithTag("page-second").performClick();rule.onNodeWithText("Second page").assertIsDisplayed()
        rule.runOnUiThread {rule.activity.setAndroidBarsVisible(true)};waitFor {!config().immersive}
        rule.onNodeWithTag("return-fullscreen").assertIsDisplayed();rule.onNodeWithTag("nav-APPS").assertDoesNotExist();rule.onNodeWithTag("home-edit-header").assertDoesNotExist();rule.onNodeWithText("UMBRA").assertDoesNotExist()
        assertEquals("ops",config().activeHomePreset);assertEquals(layout,config().desktop)
        capture("windowed")
        rule.onNodeWithTag("return-fullscreen").performClick();waitFor {config().immersive}
        rule.onNodeWithText("Second page").assertIsDisplayed();rule.onNodeWithTag("nav-APPS").assertIsDisplayed();assertEquals("ops",config().activeHomePreset)
        rule.onNodeWithTag("nav-APPS").performClick();rule.onNodeWithText("Search applications").performTextInput("kept-query")
        rule.runOnUiThread {rule.activity.setAndroidBarsVisible(true)};waitFor {!config().immersive}
        rule.onNodeWithTag("return-fullscreen").performClick();waitFor {config().immersive}
        rule.onNodeWithText("kept-query").assertIsDisplayed();rule.onNodeWithText("APPLICATION INDEX").assertIsDisplayed()
    }
    @Test fun optionalSilverTilesRestartSelectionAndArctisPickerUseOneExistingWidget() {
        val server=MockWebServer();val calls=java.util.concurrent.CopyOnWriteArrayList<RecordedRequest>();var remembered=false
        server.dispatcher=object: Dispatcher(){override fun dispatch(r: RecordedRequest): MockResponse {
            calls+=r
            val data=when(r.path) {
                "/api/status"->buildJsonObject {put("cpu",10);put("ram",20);put("quick",buildJsonArray {add("Nice shot!")});put("macros",buildJsonArray {add("Save Clip")})}
                "/api/windows/monitor"->monitorFixture()
                "/api/windows/catalog"->Json.parseToJsonElement(windowsCatalogFixture()).jsonObject
                "/api/sounds/library"->soundFixture(2)
                "/api/sonar/arctis"->{val body=Json.parseToJsonElement(r.body.clone().readUtf8()).jsonObject;if(body.literal("output_id")=="b")remembered=true
                    if(!remembered)Json.parseToJsonElement("""{"state":"selection_required","outputs":[{"id":"a","name":"Arctis A"},{"id":"b","name":"Arctis B"}],"message":"Choose output"}""").jsonObject
                    else Json.parseToJsonElement("""{"state":"verified","verified":true,"microphone_preserved":true,"output":{"id":"b","name":"Arctis B"},"routes":{"game":"b","chat":"b","media":"b","aux":"b"},"message":"All four outputs verified"}""").jsonObject}
                "/api/moments/save-clip"->{val id=Json.parseToJsonElement(r.body.clone().readUtf8()).jsonObject.literal("requestId")!!;buildJsonObject {put("request_id",id);put("state","pending");put("message","Waiting for clip file")}}
                "/api/moments/clip-status"->{val id=Json.parseToJsonElement(r.body.clone().readUtf8()).jsonObject.literal("requestId")!!;buildJsonObject {put("request_id",id);put("state","unverified");put("clip_file_verified",false);put("message","No new clip observed")}}
                else->return MockResponse().setResponseCode(404)
            };return MockResponse().setBody(data.toString())
        }};server.start()
        val model=ViewModelProvider(rule.activity)[LauncherModel::class.java]
        try {
            rule.runOnUiThread {model.instant=InstantController(model.remote){"fixture-token"};model.soundboard=SoundboardController {c,path,body->model.remote.request(serverBase(c),path,c.timeout,"fixture-token",body)}}
            val desktop=DesktopLayout(pages=listOf(DesktopPage("main","Mixed",items=listOf(DesktopItem("mixed","widget",widget=DesktopWidget(kind="icarus",title="My controls",buttonSet="mixed",fillPage=true))))))
            runBlocking {model.store.replace(config().copy(serverUrl=server.url("/").toString(),desktop=desktop))}
            waitFor {model.instant.state.value.pc!=null && !model.instant.state.value.busy}
            rule.onNodeWithTag("instant-action-host:arctis").assertDoesNotExist();rule.onNodeWithTag("instant-action-host:save-clip").assertDoesNotExist()
            rule.onNodeWithTag("instant-editor-header").performSemanticsAction(androidx.compose.ui.semantics.SemanticsActions.OnLongClick){it()};rule.onNodeWithText("Configure").performClick()
            // Search exposes the existing mixed picker; host actions are optional until explicitly selected.
            rule.onNodeWithText("Deselect all").performScrollTo().performClick()
            rule.onNodeWithText("Search available buttons").performScrollTo().performTextInput("Switch to Arctis")
            rule.onNodeWithTag("available-button-list").performScrollTo()
            rule.onNodeWithTag("select-host:arctis").performScrollTo().performClick().assertIsOn()
            rule.onNodeWithText("Search available buttons").performTextClearance();rule.onNodeWithText("Search available buttons").performTextInput("Save Clip")
            // The macro itself and the silver action can both match; select the explicit built-in by its row tag.
            rule.onNodeWithTag("available-button-list").performScrollTo()
            rule.onNodeWithTag("select-host:save-clip").performScrollTo().performClick().assertIsOn()
            rule.onNodeWithText("Save widget").performClick();try {waitFor {config().widgetButtonSelections["mixed"]?.containsAll(listOf("host:arctis","host:save-clip"))==true}} catch(e: Exception){throw AssertionError("Saved selections="+config().widgetButtonSelections+" settingsError="+model.settingsError.value,e)}
            rule.onNodeWithText("Done").performClick()
            waitFor {!model.instant.state.value.busy && model.instant.pcConnection.value.catalog!=null}
            enabled("instant-action-host:arctis")
            rule.onNodeWithTag("instant-action-host:arctis").assertIsDisplayed().assertIsEnabled().performClick()
            waitFor {model.instant.state.value.hostResult?.literal("state")=="selection_required" && !model.instant.state.value.busy}
            rule.onNodeWithText("Choose Arctis output").assertIsDisplayed();rule.onNodeWithText("Arctis B").performClick()
            waitFor {model.instant.state.value.status=="All four outputs verified"}
            waitFor {!model.instant.state.value.busy}
            enabled("instant-action-host:save-clip")
            rule.onNodeWithTag("instant-action-host:save-clip").assertIsEnabled().performClick();waitFor {model.instant.state.value.hostResult?.literal("state") in setOf("pending","unverified")}
            rule.mainClock.advanceTimeBy(1500);waitFor {model.instant.state.value.hostResult?.literal("state")=="unverified"}
            assertTrue(model.instant.state.value.status.contains("unconfirmed"));assertEquals(1,calls.count {it.path=="/api/moments/save-clip"})
            val before=config();rule.activityRule.scenario.recreate()
            rule.onNodeWithTag("instant-action-host:arctis").assertIsDisplayed();rule.onNodeWithTag("instant-action-host:save-clip").assertIsDisplayed()
            assertEquals(before.widgetButtonSelections,config().widgetButtonSelections);assertEquals(before.gridLayouts,config().gridLayouts)
            assertTrue(calls.filter {it.path in setOf("/api/sonar/arctis","/api/moments/save-clip")}.all {it.getHeader("Authorization")=="Bearer fixture-token"})
            capture("silver-actions")
        }finally {server.shutdown()}
    }
    private fun capture(name: String) {
        val folder=System.getProperty("umbra.captureDir") ?: return
        rule.runOnUiThread {val view=rule.activity.window.decorView;val bitmap=android.graphics.Bitmap.createBitmap(view.width,view.height,android.graphics.Bitmap.Config.ARGB_8888)
            try {view.draw(android.graphics.Canvas(bitmap));java.io.File(folder,"host33-$name-sdk${android.os.Build.VERSION.SDK_INT}.png").apply {parentFile?.mkdirs()}.outputStream().use {bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it)}}finally {bitmap.recycle()}}
    }
}
