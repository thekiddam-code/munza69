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
class Home32HostUiTest {
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
    @Test fun collapseRecoveryExpandsViewportPersistsAndNeverTrapsNavigation() {
        val model=ViewModelProvider(rule.activity)[LauncherModel::class.java]
        val desktop=DesktopLayout(pages=listOf(DesktopPage("main","Persistent page",items=listOf(DesktopItem("clock","widget",widget=DesktopWidget(rows=2))))))
        runBlocking {model.store.replace(config().copy(desktop=desktop))}
        val initial=rule.onNodeWithTag("home-pages").fetchSemanticsNode().boundsInRoot.height
        rule.onNodeWithText("Full screen").performScrollTo().performClick()
        waitFor {config().homeHeaderCollapsed && config().homeFooterCollapsed}
        rule.onNodeWithTag("home-edit-header").assertDoesNotExist();rule.onNodeWithTag("nav-APPS").assertDoesNotExist()
        rule.onNodeWithTag("restore-home-header").assertIsDisplayed();rule.onNodeWithTag("restore-home-footer").assertIsDisplayed()
        val expanded=rule.onNodeWithTag("home-pages").fetchSemanticsNode().boundsInRoot.height
        assertTrue("Collapse must reclaim real layout space",expanded>initial+100)
        assertEquals(desktop,config().desktop)
        capture("focus")
        rule.activityRule.scenario.recreate()
        rule.onNodeWithTag("restore-home-header").assertIsDisplayed()
        assertTrue(config().homeHeaderCollapsed);assertTrue(config().homeFooterCollapsed)
        rule.onNodeWithTag("restore-home-footer").performClick();waitFor {!config().homeFooterCollapsed}
        assertTrue(config().homeHeaderCollapsed)
        rule.onNodeWithTag("nav-APPS").assertIsDisplayed().performClick()
        rule.onNodeWithText("APPLICATION INDEX").assertIsDisplayed();rule.onNodeWithTag("nav-HOME").performClick()
        rule.onNodeWithTag("restore-home-header").performClick();waitFor {!config().homeHeaderCollapsed}
        rule.onNodeWithTag("home-edit-header").assertIsDisplayed();assertEquals(desktop,config().desktop)
    }
    @Test fun onePageSizedWidgetMixesColorFamiliesAndUsesOriginalSeparateEndpoints()=mixedWidget(3)
    @Test @RoboConfig(sdk=[34],qualifiers="w1000dp-h720dp-land-xhdpi")
    fun tabletUsesTwelveColumnsAcrossOneWidget()=mixedWidget(12)
    private fun mixedWidget(columns: Int) {
        val server=MockWebServer();val calls=java.util.concurrent.CopyOnWriteArrayList<RecordedRequest>()
        val quick=listOf("Nice shot!","Great pass!","Thanks!","What a save!","No problem.","GG")
        server.dispatcher=object: Dispatcher(){override fun dispatch(r: RecordedRequest): MockResponse {
            calls+=r
            val data=when(r.path) {
                "/api/status"->buildJsonObject {put("cpu",10);put("ram",20);put("quick",JsonArray(quick.map(::JsonPrimitive)));put("macros",buildJsonArray {add("Copy")});put("fortnite_emotes",buildJsonArray {add(buildJsonObject {put("label","Dance")})})}
                "/api/windows/monitor"->monitorFixture()
                "/api/windows/catalog"->Json.parseToJsonElement(windowsCatalogFixture()).jsonObject
                "/api/sounds/library"->soundFixture(4)
                "/api/sounds/play"->buildJsonObject {put("state","idle")}
                "/api/action"->buildJsonObject {put("message","Quick chat acknowledged")}
                else->return MockResponse().setResponseCode(404)
            }
            return MockResponse().setBody(data.toString())
        }};server.start()
        val model=ViewModelProvider(rule.activity)[LauncherModel::class.java]
        try {
            rule.runOnUiThread {model.instant=InstantController(model.remote){"fixture-token"};model.soundboard=SoundboardController {c,path,body->model.remote.request(serverBase(c),path,c.timeout,"fixture-token",body)}}
            val sounds=(0..3).map {"sound:"+it.toString(16).padStart(32,'0')}
            val selection=quick.map {"quick:$it"}+sounds+listOf("emote:0:Dance","windows:settings","local:mining")
            val desktop=DesktopLayout(pages=listOf(DesktopPage("main","Combined preset",columns=4,items=listOf(DesktopItem("mixed","widget",widget=DesktopWidget(kind="icarus",title="Combined controls",buttonSet="mixed",fillPage=true,span=4,rows=8,buttonColumns=columns))))))
            runBlocking {model.store.replace(config().copy(homeHeaderCollapsed=true,homeFooterCollapsed=true,serverUrl=server.url("/").toString(),customButtons=listOf(CustomButton(id="mining",label="Mine",kind=OutputKind.MineToggle)),desktop=desktop,widgetButtonSelections=mapOf("mixed" to selection)))}
            waitFor {model.instant.state.value.pc!=null && !model.instant.state.value.busy && model.instant.pcConnection.value.catalog!=null && model.soundboard.state.value.catalog!=null && !model.soundboard.state.value.busy}
            for(id in selection)rule.onNodeWithTag("instant-action-$id").assertIsDisplayed()
            rule.onNodeWithTag("instant-action-quick:Nice shot!").performClick();waitFor {calls.any {it.path=="/api/action"}}
            rule.onNodeWithTag("instant-action-${sounds.last()}").performClick();waitFor {calls.any {it.path=="/api/sounds/play"}}
            val play=calls.first {it.path=="/api/sounds/play"};assertEquals("Bearer fixture-token",play.getHeader("Authorization"))
            val body=Json.parseToJsonElement(play.body.readUtf8()).jsonObject;assertEquals(sounds.last().removePrefix("sound:"),body.literal("id"));assertNotNull(body.literal("requestId"))
            assertEquals(1,calls.count {it.path=="/api/action"});assertEquals(1,calls.count {it.path=="/api/sounds/play"});assertFalse(calls.any {it.path=="/api/sounds/output"})
            assertEquals(selection,config().widgetButtonSelections["mixed"])
            val page=rule.onNodeWithTag("home-pages").fetchSemanticsNode().boundsInRoot
            val widget=rule.onNodeWithTag("grid-item-home:main-mixed").fetchSemanticsNode().boundsInRoot
            assertTrue(widget.height>page.height*.85f);assertTrue(widget.bottom<=page.bottom+1)
            if(columns==12) {
                val buttons=selection.map {rule.onNodeWithTag("instant-action-$it").fetchSemanticsNode().boundsInRoot}.sortedWith(compareBy<androidx.compose.ui.geometry.Rect> {it.top}.thenBy {it.left}).take(12)
                assertTrue(buttons.all {kotlin.math.abs(it.top-buttons.first().top)<1f})
                assertTrue(buttons.zipWithNext().all {(a,b)->b.left>a.left && a.right<=b.left})
                assertEquals(12,config().desktop!!.item("mixed")!!.widget!!.buttonColumns)
            }
            capture(if(columns==12)"tablet-twelve-columns" else "mixed-full-page")
            // Stopped launcher cancels widget sessions; no idle sound polling is started.
            val count=calls.size
            rule.activityRule.scenario.moveToState(androidx.lifecycle.Lifecycle.State.CREATED)
            rule.mainClock.advanceTimeBy(5000);org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle()
            assertEquals(count,calls.size)
        }finally {server.shutdown()}
    }
    private fun capture(name: String) {
        val folder=System.getProperty("umbra.captureDir") ?: return
        rule.runOnUiThread {val view=rule.activity.window.decorView;val bitmap=android.graphics.Bitmap.createBitmap(view.width,view.height,android.graphics.Bitmap.Config.ARGB_8888)
            try {view.draw(android.graphics.Canvas(bitmap));java.io.File(folder,"home32-$name-sdk${android.os.Build.VERSION.SDK_INT}.png").apply {parentFile?.mkdirs()}.outputStream().use {bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it)}}finally {bitmap.recycle()}}
    }
}
