package com.umbra.mobile

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.first
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
class LauncherHostUiTest {
    private val rule=createAndroidComposeRule<MainActivity>()
    // Android grants this app-owned signature permission at installation; Robolectric
    // requires the install grant to be modeled explicitly before the activity starts.
    @get:Rule val rules=org.junit.rules.RuleChain.outerRule(object: org.junit.rules.ExternalResource() {
        override fun before() {
            val app=org.robolectric.RuntimeEnvironment.getApplication()
            org.robolectric.Shadows.shadowOf(app).grantPermissions("com.umbra.mobile.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION")
            runBlocking { ConfigStore(app).replace(Config(master=false,immersive=false)) }
        }
    }).around(rule)
    @Test fun homeDrawerGestureCommandCenterAndPersistenceRegression() {
        runBlocking { ConfigStore(rule.activity).replace(Config(master=false,immersive=false)) }
        rule.onNodeWithText("APPS").performClick()
        rule.onNodeWithText("Search applications").performTextInput("umbra_no_such_app_123456")
        rule.onNodeWithText("No applications match.").assertIsDisplayed()
        rule.runOnUiThread { rule.activity.onBackPressedDispatcher.onBackPressed() }
        rule.onNodeWithText("01 / COMMAND DECK").performScrollTo().assertIsDisplayed()
        capture("home")
        runBlocking { ConfigStore(rule.activity).update { it.copy(immersive=true,hideTopBar=true,hideBottomBar=true) } }
        rule.onNodeWithTag("home-swipe-handle").performScrollTo().performTouchInput { swipeDown() }
        rule.onNodeWithText("UMBRA / COMMAND CENTER").assertIsDisplayed()
        capture("command-center")
        rule.onNodeWithTag("command-swipe-handle").performTouchInput { swipeDown() }
        rule.onNodeWithText("Native Android notifications").assertIsDisplayed()
        rule.onNodeWithText("Restore Android bars").performClick()
        rule.waitUntil(5000) { runBlocking { !ConfigStore(rule.activity).config.first().immersive } }
        val restored=runBlocking { ConfigStore(rule.activity).config.first() }
        assertFalse(restored.hideTopBar);assertFalse(restored.hideBottomBar)
        rule.onNodeWithTag("command-swipe-handle").performTouchInput { swipeUp() }
        rule.onNodeWithText("01 / COMMAND DECK").performScrollTo().assertIsDisplayed()
        rule.onNodeWithText("CONFIG").performClick()
        rule.onNodeWithContentDescription("Master animations").performScrollTo().assertIsOff()
        rule.onNodeWithContentDescription("Master animations").performClick()
        rule.waitUntil(5000) { rule.onAllNodesWithContentDescription("Master animations").fetchSemanticsNodes().any { it.config[androidx.compose.ui.semantics.SemanticsProperties.ToggleableState]==androidx.compose.ui.state.ToggleableState.On } }
        rule.onNodeWithContentDescription("Master animations").performClick()
        rule.waitUntil(5000) { rule.onAllNodesWithContentDescription("Master animations").fetchSemanticsNodes().any { it.config[androidx.compose.ui.semantics.SemanticsProperties.ToggleableState]==androidx.compose.ui.state.ToggleableState.Off } }
        rule.onNodeWithText("Minimal").performScrollTo().performClick()
        rule.activityRule.scenario.recreate()
        rule.onNodeWithText("CONFIG").performClick()
        rule.waitUntil(5000) { rule.onNodeWithContentDescription("Master animations").fetchSemanticsNode().config[androidx.compose.ui.semantics.SemanticsProperties.ToggleableState] == androidx.compose.ui.state.ToggleableState.Off }
        rule.onNodeWithText("Minimal").assertIsSelected()
        capture("studio")
        rule.onNodeWithTag("nav-ICARUS").performClick()
        rule.onNodeWithText("Pair native controls").performScrollTo().assertIsDisplayed()
        capture("icarus")
        val server=okhttp3.mockwebserver.MockWebServer()
        server.start()
        try {
            val model=androidx.lifecycle.ViewModelProvider(rule.activity)[LauncherModel::class.java]
            rule.runOnUiThread {model.instant=InstantController(model.remote){"test-token"}}
            server.enqueue(okhttp3.mockwebserver.MockResponse().setSocketPolicy(okhttp3.mockwebserver.SocketPolicy.NO_RESPONSE))
            runBlocking { ConfigStore(rule.activity).update { it.copy(url=server.url("/").toString(),refreshOnNetwork=false,refreshOnResume=true,timeout=10) } }
            rule.waitUntil(5000) { org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();server.requestCount>=1 }
            assertEquals(1,server.requestCount)
            rule.activityRule.scenario.moveToState(androidx.lifecycle.Lifecycle.State.CREATED)
            org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idleFor(java.time.Duration.ofMillis(150))
            Thread.sleep(150)
            assertEquals(1,server.requestCount)
            server.enqueue(okhttp3.mockwebserver.MockResponse().setResponseCode(200))
            rule.activityRule.scenario.moveToState(androidx.lifecycle.Lifecycle.State.RESUMED)
            rule.waitUntil(5000) { org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();server.requestCount>=2 }
            assertEquals(2,server.requestCount)
            rule.activityRule.scenario.moveToState(androidx.lifecycle.Lifecycle.State.CREATED)
            assertEquals(2,server.requestCount)
        } finally { server.shutdown() }
        val wallpaper=java.io.ByteArrayOutputStream()
        exportWallpaper(Config(),wallpaper)
        val bytes=wallpaper.toByteArray()
        val decoded=android.graphics.BitmapFactory.decodeByteArray(bytes,0,bytes.size)
        assertNotNull(decoded);assertEquals(1440,decoded.width);assertEquals(3120,decoded.height)
        System.getProperty("umbra.captureDir")?.let { path -> java.io.File(path,"umbra-lock-screen.png").apply { parentFile?.mkdirs();writeBytes(bytes) } }
        decoded.recycle()
    }
    private fun capture(name: String) {
        val folder=System.getProperty("umbra.captureDir") ?: return
        rule.runOnUiThread {
            val view=rule.activity.window.decorView
            val bitmap=android.graphics.Bitmap.createBitmap(view.width,view.height,android.graphics.Bitmap.Config.ARGB_8888)
            try {
                view.draw(android.graphics.Canvas(bitmap))
                val file=java.io.File(folder,"$name-sdk${android.os.Build.VERSION.SDK_INT}.png")
                file.parentFile?.mkdirs()
                file.outputStream().use { assertTrue(bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it)) }
            } finally { bitmap.recycle() }
        }
    }

}
