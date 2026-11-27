package com.umbra.mobile

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.semantics.SemanticsActions
import androidx.lifecycle.ViewModelProvider
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.first
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
class Phase3HostUiTest {
    private val rule=createAndroidComposeRule<MainActivity>()
    @get:Rule val rules=org.junit.rules.RuleChain.outerRule(object: org.junit.rules.ExternalResource() {
        override fun before() {
            val app=org.robolectric.RuntimeEnvironment.getApplication()
            org.robolectric.Shadows.shadowOf(app).grantPermissions("com.umbra.mobile.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION")
            runBlocking {ConfigStore(app).replace(Config(master=false,immersive=true,statusPanel=false))}
        }
    }).around(rule)
    private fun config()=runBlocking {ConfigStore(rule.activity).config.first()}
    private fun waitFor(condition: ()->Boolean) {rule.waitUntil(7000){org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();condition()}}
    @Test fun allSixDestinationsKeepCompactIndicatorAndHidePreferencePersists() {
        for(id in listOf("HOME","APPS","COMMAND","SIMULATOR","ICARUS","CONFIG")) {
            rule.onNodeWithTag("nav-$id").performClick()
            rule.onNodeWithTag("pc-connection-indicator").assertIsDisplayed()
            rule.onNodeWithText("Lounge").assertDoesNotExist();rule.onNodeWithText("Supported TV key").assertDoesNotExist()
        }
        rule.onNodeWithTag("settings-category-ICARUS").performScrollTo().performClick()
        rule.onNodeWithContentDescription("Show PC connection indicator").performScrollTo().performClick()
        waitFor {!config().pcIndicator}
        rule.onNodeWithTag("pc-connection-indicator").assertDoesNotExist()
        val old=config().desktop
        rule.activityRule.scenario.recreate();assertFalse(config().pcIndicator);assertEquals(old,config().desktop)
        rule.onNodeWithTag("nav-HOME").performClick();rule.onNodeWithTag("pc-connection-indicator").assertDoesNotExist()
        capture("six-tabs")
    }
    @Test fun twoEngineeringWidgetsShareTelemetryAndPersistIndependentResizeCollapse() {
        val server=MockWebServer();server.dispatcher=object: Dispatcher() {
            override fun dispatch(request: RecordedRequest): MockResponse=when(request.path) {
                "/api/status"->MockResponse().setBody("""{"hostname":"TEST-PC","cpu":21,"ram":43,"macros":["Copy"]}""")
                "/api/windows/monitor"->MockResponse().setBody(monitorFixture().toString())
                "/api/windows/catalog"->MockResponse().setBody(windowsCatalogFixture())
                else->MockResponse().setResponseCode(404)
            }
        };server.start()
        val model=ViewModelProvider(rule.activity)[LauncherModel::class.java]
        val controller=InstantController(model.remote){"fixture-token"}
        try {
            rule.runOnUiThread {model.instant=controller}
            val items=listOf("cpu","gpu").map {kind->DesktopItem(kind,"widget",widget=DesktopWidget(kind="engineering_$kind",span=3,rows=3))}
            runBlocking {model.store.replace(Config(master=false,immersive=true,statusPanel=false,serverUrl=server.url("/").toString(),desktop=DesktopLayout(pages=listOf(DesktopPage("main","Engineering preset",items=items)))))}
            waitFor {controller.pcConnection.value.monitor!=null && controller.pcConnection.value.catalog!=null && controller.engineeringConsumers.value.size==2}
            rule.onNodeWithText("CPU: 23.0%").assertIsDisplayed();rule.onNodeWithText("Fixture GPU").assertIsDisplayed()
            assertEquals(3,server.requestCount)
            model.editDesktop {layout->layout.updatePage("main"){it.copy(items=it.items+DesktopItem("ram","widget",widget=DesktopWidget(kind="engineering_ram",span=3,rows=2)))}}
            waitFor {controller.engineeringConsumers.value.size==3}
            assertEquals(3,server.requestCount) // another visible consumer must not restart the shared polling loop
            model.removeDesktopItem("ram");waitFor {controller.engineeringConsumers.value.size==2}
            rule.onNodeWithTag("pc-connection-indicator").performClick()
            rule.onNodeWithText("PC name: TEST-PC").assertIsDisplayed();rule.onNodeWithText("Status: Connected").assertIsDisplayed()
            rule.onNodeWithText("HTTP round trip",substring=true).assertIsDisplayed()
            rule.onNodeWithText("Close").performClick()
            capture("engineering-home")
            rule.onNodeWithTag("grid-item-home:main-cpu").performSemanticsAction(SemanticsActions.OnLongClick){it()}
            rule.onNodeWithText("Resize").performClick();rule.onNodeWithText("◀").performClick();rule.onNodeWithText("▼").performClick();rule.onNodeWithText("Save size").performClick()
            waitFor {config().desktop!!.item("cpu")!!.widget!!.let {it.span==2 && it.rows==4}}
            rule.onNodeWithText("Options").performClick();rule.onNodeWithText("Collapse module").performClick();rule.onNodeWithText("Done").performClick()
            waitFor {config().desktop!!.item("cpu")!!.widget!!.collapsed}
            // Resize while collapsed preserves the expanded height and remains expandable.
            rule.onNodeWithTag("grid-item-home:main-cpu").performSemanticsAction(SemanticsActions.OnLongClick){it()}
            rule.onNodeWithText("Resize").performClick();rule.onNodeWithText("◀").performClick();rule.onNodeWithText("Save size").performClick()
            waitFor {config().desktop!!.item("cpu")!!.widget!!.span==1}
            assertEquals(4,config().desktop!!.item("cpu")!!.widget!!.rows)
            assertFalse(config().gridLayouts.getValue("home:main").cells.first {it.id=="cpu"}.collapsed)
            rule.onNodeWithText("Options").performClick();rule.onNodeWithText("Expand module").performClick();rule.onNodeWithText("Done").performClick()
            waitFor {!config().desktop!!.item("cpu")!!.widget!!.collapsed}
            rule.onNodeWithTag("grid-item-home:main-cpu").performSemanticsAction(SemanticsActions.OnLongClick){it()}
            rule.onNodeWithText("Collapse module").performClick();rule.onNodeWithText("Done").performClick()
            waitFor {config().desktop!!.item("cpu")!!.widget!!.collapsed}
            assertEquals(3,config().desktop!!.item("gpu")!!.widget!!.span)
            model.addPreset("Blank");waitFor {config().activeHomePreset!="default" && controller.engineeringConsumers.value.isEmpty()}
            val blank=config().activeHomePreset
            model.switchPreset("default");waitFor {config().activeHomePreset=="default" && controller.engineeringConsumers.value.size==1}
            assertTrue(config().desktop!!.item("cpu")!!.widget!!.collapsed)
            assertEquals(1,config().desktop!!.item("cpu")!!.widget!!.span)
            model.switchPreset(blank);waitFor {controller.engineeringConsumers.value.isEmpty()}
            rule.activityRule.scenario.moveToState(androidx.lifecycle.Lifecycle.State.CREATED)
            val count=server.requestCount
            Thread.sleep(200);org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idleFor(java.time.Duration.ofSeconds(5))
            assertEquals(count,server.requestCount);assertEquals(PcPhase.Offline,controller.pcConnection.value.phase)
        } finally {server.shutdown()}
    }
    private fun capture(name: String) {
        val folder=System.getProperty("umbra.captureDir") ?: return
        rule.runOnUiThread {val view=rule.activity.window.decorView;val bitmap=android.graphics.Bitmap.createBitmap(view.width,view.height,android.graphics.Bitmap.Config.ARGB_8888)
            try {view.draw(android.graphics.Canvas(bitmap));java.io.File(folder,"phase3-$name-sdk${android.os.Build.VERSION.SDK_INT}.png").apply {parentFile?.mkdirs()}.outputStream().use {bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it)}}finally {bitmap.recycle()}}
    }
}
