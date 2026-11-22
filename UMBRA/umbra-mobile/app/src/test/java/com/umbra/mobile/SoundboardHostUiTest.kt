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
class SoundboardHostUiTest {
    private val rule=createAndroidComposeRule<MainActivity>()
    @get:Rule val rules=org.junit.rules.RuleChain.outerRule(object: org.junit.rules.ExternalResource() {
        override fun before() {
            val app=org.robolectric.RuntimeEnvironment.getApplication()
            org.robolectric.Shadows.shadowOf(app).grantPermissions("com.umbra.mobile.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION")
            runBlocking {ConfigStore(app).replace(Config(master=false,immersive=false,statusPanel=false,serverUrl="http://localhost:9000/"))}
        }
    }).around(rule)
    private fun config()=runBlocking {ConfigStore(rule.activity).config.first()}
    private fun waitFor(condition: ()->Boolean) {rule.waitUntil(5000){org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();condition()}}
    @Test fun catalogScrollsAndHoldDragDoesNotPlayWithMasterOff() {
        val calls=mutableListOf<String>()
        val ctl=SoundboardController {_,path,_->calls+=path;if(path.endsWith("play"))kotlinx.serialization.json.buildJsonObject {put("state",kotlinx.serialization.json.JsonPrimitive("playing"))} else soundFixture()}
        val model=androidx.lifecycle.ViewModelProvider(rule.activity)[LauncherModel::class.java]
        rule.runOnUiThread {model.soundboard=ctl}
        rule.onNodeWithTag("nav-COMMAND").performClick()
        rule.onNodeWithTag("deck-section-Soundboard").performClick()
        waitFor {ctl.state.value.catalog?.sounds?.size==14}
        val id="0".repeat(32)
        rule.onNodeWithText("Tap to play on the saved ICARUS output.",substring=true).performScrollTo()
        rule.onNodeWithTag("grid-soundboard").performScrollTo()
        val source=rule.onNodeWithTag("sound-$id").performScrollTo()
        capture("before-hold")
        source.assertIsDisplayed().assertIsEnabled()
        source.performTouchInput {down(center)}
        rule.mainClock.advanceTimeBy(700)
        rule.runOnUiThread {org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idleFor(java.time.Duration.ofMillis(700))}
        rule.onNodeWithTag("placement-highlights-soundboard").assertExists()
        source.performTouchInput {moveBy(androidx.compose.ui.geometry.Offset(0f,170f),delayMillis=180);up()}
        waitFor {config().gridLayouts["soundboard"]!=null}
        rule.onNodeWithTag("placement-highlights-soundboard").assertDoesNotExist()
        assertFalse(calls.any {it.endsWith("play")})
        rule.onNodeWithText("Done").performClick()
        // A later sound remains available beyond the first six. A regular tap uses playback.
        rule.onNodeWithText("Tap to play on the saved ICARUS output.",substring=true).performScrollTo()
        rule.onNodeWithTag("grid-soundboard").performScrollTo()
        rule.onNodeWithTag("sound-${13.toString(16).padStart(32,'0')}").performScrollTo().assertIsDisplayed().performClick()
        waitFor {calls.any {it=="api/sounds/play"}}
        assertFalse(calls.any {it=="api/action"})
        rule.onNodeWithText("Playback device",substring=true).assertDoesNotExist()
        capture("soundboard")
    }
    @Test fun audioOutputLivesInSettingsAndReadsServerChoice() {
        var fixture=soundFixture()
        val ctl=SoundboardController {_,path,body->if(path.endsWith("output"))fixture=soundFixture(revision=8,output=body!!.getValue("device"));fixture}
        val model=androidx.lifecycle.ViewModelProvider(rule.activity)[LauncherModel::class.java]
        rule.runOnUiThread {model.soundboard=ctl}
        rule.onNodeWithTag("nav-CONFIG").performClick()
        rule.onNodeWithTag("settings-category-ICARUS").performScrollTo().performClick()
        rule.onNodeWithText("Soundboard → Audio Output").performScrollTo().performClick()
        waitFor {ctl.state.value.catalog!=null}
        rule.onNodeWithText("Use: Existing render output [2]").performScrollTo().performClick()
        waitFor {ctl.state.value.catalog?.output!=null}
        rule.onNodeWithText("Saved playback device: Existing render output").performScrollTo().assertIsDisplayed()
        assertFalse(exportConfig(config()).contains("Existing render output"))
        capture("audio-output")
    }
    private fun capture(name: String) {
        val folder=System.getProperty("umbra.captureDir") ?: return
        rule.runOnUiThread {val view=rule.activity.window.decorView;val bitmap=android.graphics.Bitmap.createBitmap(view.width,view.height,android.graphics.Bitmap.Config.ARGB_8888)
            try {view.draw(android.graphics.Canvas(bitmap));java.io.File(folder,"soundboard-$name-sdk${android.os.Build.VERSION.SDK_INT}.png").apply {parentFile?.mkdirs()}.outputStream().use {bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it)}}finally {bitmap.recycle()}}
    }
}
