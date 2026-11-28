package com.umbra.mobile
import androidx.compose.material3.MaterialTheme
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.ViewModelStore
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.flow.first
import org.junit.Assert.*
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config as RoboConfig
import org.robolectric.annotation.LooperMode
import org.robolectric.annotation.GraphicsMode
@RunWith(RobolectricTestRunner::class)
@RoboConfig(sdk=[30,34],qualifiers="w432dp-h936dp-port-xhdpi")
@LooperMode(LooperMode.Mode.PAUSED)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class ChatSound34UiTest {
 @get:Rule val rule=createComposeRule()
 @Test fun editorSelectsExistingSoundAndSavedChoicePersistsInDataStore() {
  val app=RuntimeEnvironment.getApplication();val store=ViewModelStore()
  val model=ViewModelProvider(store,ViewModelProvider.AndroidViewModelFactory(app))[LauncherModel::class.java]
  val c=Config(serverUrl="http://localhost:8765/");model.soundboard=SoundboardController {_,_,_->soundFixture(14)}
  runBlocking {model.soundboard.sync(c);model.store.replace(c)};var saved: CustomButton?=null
  rule.setContent {MaterialTheme {ButtonEditor(CustomButton(id="chat",kind=OutputKind.Text,text="Nice shot!"),c,null,model,{},saveDraft={saved=it})}}
  try {
   rule.onNodeWithTag("choose-after-chat-sound").performScrollTo().performClick()
   rule.waitUntil(5000) {org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();rule.onAllNodesWithTag("after-sound-list").fetchSemanticsNodes().isNotEmpty()}
   rule.onNodeWithTag("after-sound-list").performScrollToNode(hasTestTag("after-sound-${13.toString(16).padStart(32,'0')}"))
   rule.onNodeWithTag("after-sound-${13.toString(16).padStart(32,'0')}").performClick()
   rule.onNodeWithText("Save button").performClick();rule.runOnIdle {assertNotNull(saved)}
   runBlocking {model.store.replace(c.copy(customButtons=listOf(saved!!)))}
   val reloaded=runBlocking {ConfigStore(app).config.first()};assertEquals(13.toString(16).padStart(32,'0'),reloaded.customButtons.single().afterSoundId)
   rule.onNodeWithTag("choose-after-chat-sound").performScrollTo().performClick();rule.onNodeWithTag("after-sound-none").performClick();rule.onNodeWithText("Save button").performClick()
   rule.runOnIdle {assertEquals("",saved!!.afterSoundId)}
  }finally {rule.runOnUiThread {store.clear()}}
 }
}
