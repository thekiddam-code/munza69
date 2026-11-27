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
class Widget31HostUiTest {
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
    @Test fun rocketAndSoundboardSharePageWhileFortniteHasIndependentPage() {
        val server=MockWebServer();val requests=java.util.concurrent.CopyOnWriteArrayList<String>()
        server.dispatcher=object: Dispatcher(){override fun dispatch(r: RecordedRequest): MockResponse {requests+=r.path ?: "";return when(r.path){
            "/api/status"->MockResponse().setBody("""{"cpu":10,"ram":20,"quick":["Nice shot!"],"macros":["Copy"],"fortnite_emotes":[{"label":"Dance"}]}""")
            "/api/windows/monitor"->MockResponse().setBody(monitorFixture().toString())
            "/api/windows/catalog"->MockResponse().setBody(windowsCatalogFixture())
            "/api/action"->MockResponse().setBody("{\"message\":\"Game command acknowledged\"}")
            else->MockResponse().setResponseCode(404)
        }}};server.start()
        val model=ViewModelProvider(rule.activity)[LauncherModel::class.java]
        val soundCalls=java.util.concurrent.CopyOnWriteArrayList<String>()
        try {
            rule.runOnUiThread {model.instant=InstantController(model.remote){"fixture-token"};model.soundboard=SoundboardController {_,path,_->soundCalls+=path;if(path.endsWith("play"))buildJsonObject {put("state","idle")} else soundFixture()}}
            val soundId=13.toString(16).padStart(32,'0')
            val main=DesktopPage("main","Mixed controls",columns=4,items=listOf(
                DesktopItem("rocket","widget",widget=DesktopWidget(kind="icarus",title="Rocket deck",buttonSet="rocket",span=4,rows=4,buttonColumns=3)),
                DesktopItem("sounds","widget",widget=DesktopWidget(kind="soundboard",title="Sound deck",span=4,rows=4,buttonColumns=3))))
            val other=DesktopPage("fortnite","Fortnite",columns=4,items=listOf(DesktopItem("emotes","widget",widget=DesktopWidget(kind="icarus",title="Emote deck",buttonSet="fortnite",span=4,rows=4))))
            runBlocking {model.store.replace(Config(master=false,immersive=true,statusPanel=false,pcIndicator=false,serverUrl=server.url("/").toString(),instantSelection=emptySet(),desktop=DesktopLayout(pages=listOf(main,other)),widgetButtonSelections=mapOf("sounds" to listOf("sound:$soundId"))))}
            waitFor {model.instant.state.value.pc!=null && !model.instant.state.value.busy && model.instant.pcConnection.value.catalog!=null && model.soundboard.state.value.catalog!=null}
            rule.onNodeWithText("Rocket deck").assertIsDisplayed();rule.onNodeWithText("Sound deck").assertIsDisplayed()
            rule.onNodeWithTag("instant-action-quick:Nice shot!").assertIsDisplayed().assertIsEnabled().performClick()
            waitFor {"/api/action" in requests}
            rule.onNodeWithTag("sound-$soundId").assertIsDisplayed().performClick();waitFor {"api/sounds/play" in soundCalls}
            assertEquals(1,requests.count {it=="/api/action"});assertFalse(soundCalls.any {it=="api/sounds/output"})
            capture("mixed-widgets")
            rule.onNodeWithTag("page-fortnite").performClick()
            rule.onNodeWithTag("instant-action-emote:0:Dance").assertIsDisplayed()
            waitFor {!model.instant.state.value.busy}
            rule.onNodeWithTag("instant-action-emote:0:Dance").assertIsEnabled().performClick()
            waitFor {requests.count {it=="/api/action"}==2}
            assertEquals(listOf("sound:$soundId"),config().widgetButtonSelections["sounds"])
            assertEquals("rocket",config().desktop!!.item("rocket")!!.widget!!.buttonSet)
            rule.onNodeWithTag("nav-COMMAND").performClick()
            rule.onNodeWithText("Command library").assertDoesNotExist();rule.onNodeWithText("Instant Buttons").assertDoesNotExist();rule.onNodeWithTag("deck-section-Soundboard").assertDoesNotExist()
            rule.onNodeWithTag("nav-SIMULATOR").performClick();rule.onNodeWithText("Soundboard").assertIsDisplayed()
        }finally {server.shutdown()}
    }
    @Test fun configurationPinAndRecentsOptInAreAvailableWithoutScreenReading() {
        rule.onNodeWithContentDescription("Recent apps").assertIsDisplayed().performClick()
        rule.onNodeWithText("Recent apps shortcut").assertIsDisplayed()
        rule.onNodeWithText("Use native bar").performClick()
        waitFor {!config().immersive}
        rule.onNodeWithTag("return-fullscreen").assertIsDisplayed().performClick()
        waitFor {config().immersive}
        val xml=rule.activity.resources.getXml(com.umbra.mobile.R.xml.recents_accessibility)
        while(xml.eventType!=org.xmlpull.v1.XmlPullParser.START_TAG)xml.next()
        val ns="http://schemas.android.com/apk/res/android"
        assertFalse(xml.getAttributeBooleanValue(ns,"canRetrieveWindowContent",true));assertFalse(xml.getAttributeBooleanValue(ns,"canPerformGestures",true));assertEquals("com.umbra.mobile",xml.getAttributeValue(ns,"packageNames"));xml.close()
        rule.onNodeWithTag("nav-CONFIG").performClick();rule.onNodeWithTag("settings-category-ICARUS").performScrollTo().performClick()
        rule.onNodeWithText("Server PIN").performScrollTo().performTextInput("Ab_9-x2")
        rule.onNodeWithText("Pair with PC").assertIsNotEnabled() // saved address is required
        assertFalse(exportConfig(config()).contains("Ab_9-x2"))
        capture("config-pairing")
    }
    private fun capture(name: String) {
        val folder=System.getProperty("umbra.captureDir") ?: return
        rule.runOnUiThread {val view=rule.activity.window.decorView;val bitmap=android.graphics.Bitmap.createBitmap(view.width,view.height,android.graphics.Bitmap.Config.ARGB_8888)
            try {view.draw(android.graphics.Canvas(bitmap));java.io.File(folder,"widget31-$name-sdk${android.os.Build.VERSION.SDK_INT}.png").apply {parentFile?.mkdirs()}.outputStream().use {bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it)}}finally {bitmap.recycle()}}
    }
}
