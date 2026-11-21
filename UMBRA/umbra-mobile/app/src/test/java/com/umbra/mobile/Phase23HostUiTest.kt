package com.umbra.mobile

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.semantics.SemanticsActions
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
class Phase23HostUiTest {
    private val rule=createAndroidComposeRule<MainActivity>()
    @get:Rule val rules=org.junit.rules.RuleChain.outerRule(object: org.junit.rules.ExternalResource() {
        override fun before() {
            androidx.test.espresso.IdlingPolicies.setMasterPolicyTimeout(20,java.util.concurrent.TimeUnit.SECONDS)
            val app=org.robolectric.RuntimeEnvironment.getApplication()
            org.robolectric.Shadows.shadowOf(app).grantPermissions("com.umbra.mobile.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION")
            val cells=MODULES.mapIndexed {i,name->GridCell(name,y=i,w=2,h=7,collapsed=true)}
            val buttons=(0..13).map {CustomButton(id="b$it",label="Button $it")}
            runBlocking {ConfigStore(app).replace(Config(master=false,immersive=false,statusPanel=false,customButtons=buttons,gridLayouts=mapOf("command" to GridLayout(columns=2,cells=cells))))}
        }
        override fun after(){androidx.test.espresso.IdlingPolicies.setMasterPolicyTimeout(60,java.util.concurrent.TimeUnit.SECONDS)}
    }).around(rule)
    private fun config()=runBlocking {ConfigStore(rule.activity).config.first()}
    private fun waitFor(condition: (Config)->Boolean) {rule.waitUntil(5000){org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();condition(config())}}
    private fun hold(node: SemanticsNodeInteraction) {
        node.performTouchInput {down(center)}
        rule.mainClock.advanceTimeBy(700)
        rule.runOnUiThread {org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idleFor(java.time.Duration.ofMillis(700))}
    }
    @Test fun collapsedHeadersDragWithMotionOff()=dragCollapsed(false)
    @Test fun collapsedHeadersDragWithMotionOn()=dragCollapsed(true)
    private fun dragCollapsed(motion: Boolean) {
        rule.onNodeWithTag("nav-COMMAND").performClick()
        runBlocking {ConfigStore(rule.activity).update {it.copy(master=motion)}};waitFor {it.master==motion}
        rule.onNodeWithTag("arrangement-toolbar").assertDoesNotExist()
        rule.onNodeWithTag("placement-highlights-command").assertDoesNotExist()
        val source=rule.onNodeWithTag("module-header-command-Device")
        val target=rule.onNodeWithTag("module-header-command-System")
        source.assertIsDisplayed();target.assertIsDisplayed()
        val point=target.fetchSemanticsNode().boundsInRoot.center-source.fetchSemanticsNode().boundsInRoot.topLeft
        hold(source)
        rule.onNodeWithTag("placement-highlights-command").assertExists()
        source.performTouchInput {moveTo(point,delayMillis=180);up()}
        waitFor {c->val cells=c.gridLayouts.getValue("command").cells;cells.first {it.id=="Device"}.y>cells.first {it.id=="System"}.y}
        assertTrue(config().gridLayouts.getValue("command").cells.all {it.collapsed})
        rule.onNodeWithTag("placement-highlights-command").assertDoesNotExist()
        rule.onNodeWithText("Undo").performClick()
        waitFor {it.gridLayouts.getValue("command").cells.first {it.id=="Device"}.y==0}
        rule.onNodeWithText("Done").performClick()
        rule.onNodeWithTag("arrangement-toolbar").assertDoesNotExist()
        // Each expansion is independent, even when earlier content pushes another header off-screen.
        rule.onNodeWithTag("module-header-command-System").performClick()
        rule.onNodeWithTag("module-header-command-Device").performClick()
        waitFor {c->c.gridLayouts.getValue("command").cells.filter {it.id in listOf("Device","System")}.all {!it.collapsed}}
        rule.onNodeWithTag("command-compact").performClick();waitFor {!it.commandExpanded}
        rule.activityRule.scenario.recreate()
        assertFalse(config().commandExpanded)
        rule.onNodeWithTag("nav-COMMAND").performClick()
        rule.onNodeWithTag("command-compact").assertIsSelected()
        assertEquals(motion,config().master)
        capture("command-${if(motion)"motion" else "static"}")
    }
    @Test fun perTabStatusAndCompactSettingsHeaderPersist() {
        runBlocking {ConfigStore(rule.activity).update {it.copy(statusPanel=true)}}
        rule.onNodeWithTag("umbra-status-panel").assertIsDisplayed()
        rule.onNodeWithTag("nav-APPS").performClick();rule.onNodeWithTag("umbra-status-panel").assertDoesNotExist()
        runBlocking {ConfigStore(rule.activity).update {it.copy(statusTabs=it.statusTabs+("Applications" to true))}}
        rule.onNodeWithTag("umbra-status-panel").assertIsDisplayed()
        rule.onNodeWithTag("nav-CONFIG").performClick()
        rule.onNodeWithText("Settings").assertIsDisplayed();rule.onNodeWithText("UMBRA").assertDoesNotExist()
        rule.onNodeWithTag("umbra-status-panel").assertDoesNotExist()
        rule.onNodeWithText("◆ UMBRA",substring=true).performScrollTo().assertIsDisplayed()
        assertFalse(config().immersive)
        capture("settings")
    }
    @Test fun instantPageSelectsAllFourteenAndLongPressDoesNotExecute() {
        rule.onNodeWithTag("nav-ICARUS").performClick()
        rule.onNodeWithText("Instant Buttons").performScrollTo().performClick()
        val model=androidx.lifecycle.ViewModelProvider(rule.activity)[LauncherModel::class.java]
        rule.onNodeWithTag("instant-editor-header").performScrollTo().performSemanticsAction(SemanticsActions.OnLongClick){it()}
        rule.onNodeWithText("Select buttons / widgets").performClick()
        rule.onNodeWithText("14 selected",substring=true).performScrollTo().assertIsDisplayed()
        rule.onNodeWithText("Deselect all").performScrollTo().performClick();waitFor {it.instantSelection?.isEmpty()==true}
        rule.onNodeWithText("Select all").performScrollTo().performClick();waitFor {it.instantSelection?.size==14}
        rule.onNodeWithText("Done").performClick()
        val before=model.instant.state.value.status
        val button=rule.onNodeWithTag("instant-action-local:b0").performScrollTo()
        hold(button)
        rule.onNodeWithTag("placement-highlights-instant-page").assertExists()
        button.performTouchInput {up()}
        rule.onNodeWithText("Configure").assertIsDisplayed()
        rule.onNodeWithTag("placement-highlights-instant-page").assertDoesNotExist()
        assertEquals(before,model.instant.state.value.status)
        assertEquals(14,config().instantSelection!!.size)
    }
    @Test fun nativeButtonEditorSavesTimedOutputWithoutExecuting() {
        rule.onNodeWithTag("nav-ICARUS").performClick()
        rule.onNodeWithText("Instant Buttons").performScrollTo().performClick()
        rule.onNodeWithTag("instant-editor-header").performScrollTo().performSemanticsAction(SemanticsActions.OnLongClick){it()}
        rule.onNodeWithText("Create button").performClick()
        rule.onNodeWithText("Button name").performTextClearance()
        rule.onNodeWithText("Button name").performTextInput("Timed mining")
        rule.onNodeWithText("ForwardMine").performScrollTo().performClick()
        rule.onNodeWithText("Hold duration · 0.2–10 seconds").performScrollTo().performTextClearance()
        rule.onNodeWithText("Save button").assertIsNotEnabled()
        rule.onNodeWithText("Hold duration · 0.2–10 seconds").performTextInput("4.5")
        rule.onNodeWithText("Test command").performScrollTo().assertIsNotEnabled()
        rule.onNodeWithText("Save button").performClick()
        waitFor {it.customButtons.any {b->b.label=="Timed mining"}}
        val b=config().customButtons.single {it.label=="Timed mining"}
        assertEquals(OutputKind.ForwardMine,b.kind);assertEquals(4.5,b.seconds,0.0)
        val model=androidx.lifecycle.ViewModelProvider(rule.activity)[LauncherModel::class.java]
        assertFalse(model.instant.state.value.busy)
        assertEquals(15,config().customButtons.size)
    }
    private fun capture(name: String) {
        val folder=System.getProperty("umbra.captureDir") ?: return
        rule.runOnUiThread {val view=rule.activity.window.decorView;val bitmap=android.graphics.Bitmap.createBitmap(view.width,view.height,android.graphics.Bitmap.Config.ARGB_8888)
            try {view.draw(android.graphics.Canvas(bitmap));java.io.File(folder,"phase23-$name-sdk${android.os.Build.VERSION.SDK_INT}.png").apply {parentFile?.mkdirs()}.outputStream().use {bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it)}}finally {bitmap.recycle()}}
    }
}
