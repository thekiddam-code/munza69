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
class Phase21HostUiTest {
    private val rule=createAndroidComposeRule<MainActivity>()
    @get:Rule val rules=org.junit.rules.RuleChain.outerRule(object: org.junit.rules.ExternalResource() {
        override fun before() {
            androidx.test.espresso.IdlingPolicies.setMasterPolicyTimeout(20,java.util.concurrent.TimeUnit.SECONDS)
            val app=org.robolectric.RuntimeEnvironment.getApplication()
            org.robolectric.Shadows.shadowOf(app).grantPermissions("com.umbra.mobile.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION")
            val layout=DesktopLayout(pages=listOf(
                DesktopPage("main",kind="blank",items=listOf(DesktopItem("daily","folder",folder=DesktopFolder("Daily")))),
                DesktopPage("info",kind="information",items=listOf(DesktopItem("clock","widget",widget=DesktopWidget(span=3,style="Segmented",clock24=false,seconds=true)))),
                DesktopPage("other",kind="blank")))
            runBlocking { ConfigStore(app).replace(Config(master=false,immersive=true,statusPanel=false,visualDetail=VisualDetail.Cinematic,desktop=layout)) }
        }
        override fun after() {androidx.test.espresso.IdlingPolicies.setMasterPolicyTimeout(60,java.util.concurrent.TimeUnit.SECONDS)}
    }).around(rule)
    @Test fun folderWidgetPagerMasterOffAndBarsRemainFunctional() {
        rule.onNodeWithTag("folder-daily").performClick()
        rule.onNodeWithText("Folder is empty. Long-press its icon or this panel to configure.").assertIsDisplayed()
        capture("folder")
        rule.onNodeWithText("Close").performClick()
        rule.onNodeWithText("Manage folder").assertDoesNotExist()
        rule.onNodeWithTag("home-pages").performTouchInput { swipeLeft() }
        rule.onNodeWithTag("widget-clock").assertIsDisplayed().performClick()
        rule.onNodeWithText("Widget details").assertIsDisplayed()
        capture("clock-detail")
        rule.runOnUiThread {rule.activity.onBackPressedDispatcher.onBackPressed()}
        rule.onNodeWithText("Widget details").assertDoesNotExist()
        rule.onNodeWithTag("nav-APPS").performClick()
        rule.onNodeWithTag("nav-HOME").performClick()
        rule.onNodeWithTag("widget-clock").assertIsDisplayed()
        rule.onNodeWithText("Widget options").assertDoesNotExist()
        rule.onNodeWithTag("grid-item-home:info-clock").performSemanticsAction(androidx.compose.ui.semantics.SemanticsActions.OnLongClick){it()}
        rule.onNodeWithText("Configure").performClick()
        rule.onNodeWithContentDescription("24-hour clock").assertIsOff().performClick()
        rule.onNodeWithText("Save widget").performClick()
        rule.onNodeWithText("Done").performClick()
        rule.waitUntil(5000) { runBlocking {ConfigStore(rule.activity).config.first().desktop!!.item("clock")!!.widget!!.clock24} }
        // Real WindowInsets behavior is OEM-dependent; exercise both public requests and persistence here.
        rule.runOnUiThread {rule.activity.setAndroidBarsVisible(false)}
        rule.waitUntil(5000) {org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();runBlocking {ConfigStore(rule.activity).config.first().immersive}}
        rule.runOnUiThread {rule.activity.setAndroidBarsVisible(true)}
        rule.waitUntil(5000) {org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();runBlocking {!ConfigStore(rule.activity).config.first().immersive}}
        rule.activityRule.scenario.recreate()
        rule.onNodeWithTag("widget-clock").assertIsDisplayed()
        val saved=runBlocking {ConfigStore(rule.activity).config.first()}
        assertFalse(saved.master);assertEquals(VisualDetail.Cinematic,saved.visualDetail)
        assertTrue(saved.desktop!!.item("clock")!!.widget!!.clock24)
        rule.onNodeWithTag("return-fullscreen").assertIsDisplayed().performClick()
        rule.waitUntil(5000) {org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();runBlocking {ConfigStore(rule.activity).config.first().immersive}}
        rule.onNodeWithTag("page-main").performClick()
        rule.onNodeWithTag("grid-item-home:main-daily").performSemanticsAction(androidx.compose.ui.semantics.SemanticsActions.OnLongClick){it()}
        rule.onNodeWithText("Configure").performClick()
        rule.onNodeWithText("Folder name").performTextClearance()
        rule.onNodeWithText("Folder name").performTextInput("Navigation")
        rule.onNodeWithText("Save folder").performClick()
        rule.onNodeWithText("Done").performClick()
        rule.onNodeWithText("Navigation").assertIsDisplayed()
    }
    @Test fun dragApplicationsTogetherCreatesPersistentFolder() {
        rule.onNodeWithTag("folder-daily").assertIsDisplayed()
        val first=LaunchApp("example/First","Alpha");val second=LaunchApp("example/Second","Beta")
        val store=ConfigStore(rule.activity)
        runBlocking {store.update {c->c.copy(desktop=c.desktop!!.updatePage("main") {it.copy(items=listOf(DesktopItem("alpha",component=first.id),DesktopItem("beta",component=second.id)))})}}
        rule.runOnUiThread {androidx.lifecycle.ViewModelProvider(rule.activity)[LauncherModel::class.java].apps.value=listOf(first,second)}
        val source=rule.onNodeWithContentDescription("Alpha");val destination=rule.onNodeWithContentDescription("Beta")
        source.assertIsDisplayed();destination.assertIsDisplayed()
        val offset=destination.fetchSemanticsNode().boundsInRoot.center-source.fetchSemanticsNode().boundsInRoot.topLeft
        source.performTouchInput {down(center)}
        rule.mainClock.advanceTimeBy(700)
        rule.runOnUiThread {org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idleFor(java.time.Duration.ofMillis(700))}
        source.performTouchInput {moveTo(offset,delayMillis=150);up()}
        try {rule.waitUntil(5000) {org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();runBlocking {store.config.first().desktop!!.item("beta")?.folder!=null}}}
        finally {capture("drag-result")}
        assertEquals(listOf(second.id,first.id),runBlocking {store.config.first().desktop!!.item("beta")!!.folder!!.apps})
        rule.onNodeWithTag("folder-beta").assertIsDisplayed().performClick()
        rule.onNodeWithContentDescription("Alpha").assertIsDisplayed()
        rule.onNodeWithContentDescription("Beta").assertIsDisplayed()
    }
    @Test fun pagesAndWidgetPickerRemainUsableWithMasterOff() {
        rule.onNodeWithTag("home-edit-header").performSemanticsAction(androidx.compose.ui.semantics.SemanticsActions.OnLongClick){it()}
        rule.onNodeWithText("Home pages").performClick()
        rule.onNodeWithText("New page name").performScrollTo().performTextClearance()
        rule.onNodeWithText("New page name").performTextInput("Auxiliary")
        rule.onNodeWithText("Add page").performScrollTo().performClick()
        rule.onNodeWithText("Done").performClick()
        val store=ConfigStore(rule.activity)
        rule.waitUntil(5000) {org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();runBlocking {store.config.first().desktop!!.pages.size==4}}
        val page=runBlocking {store.config.first().desktop!!.pages.last()}
        assertEquals("Auxiliary",page.name)
        rule.onNodeWithTag("page-${page.id}").performClick()
        rule.onNodeWithTag("home-edit-header").performSemanticsAction(androidx.compose.ui.semantics.SemanticsActions.OnLongClick){it()}
        rule.onNodeWithText("Add widget").performClick()
        rule.onNodeWithText("Clock · Analog").performClick()
        rule.waitUntil(5000) {org.robolectric.Shadows.shadowOf(android.os.Looper.getMainLooper()).idle();runBlocking {store.config.first().desktop!!.page(page.id).items.size==1}}
        val widget=runBlocking {store.config.first().desktop!!.page(page.id).items.single()}
        assertEquals("Analog",widget.widget!!.style)
        rule.onNodeWithTag("widget-${widget.id}").assertIsDisplayed()
        capture("analog-page")
        rule.activityRule.scenario.recreate()
        rule.onNodeWithTag("widget-${widget.id}").assertIsDisplayed()
    }
    private fun capture(name: String) {
        val path=System.getProperty("umbra.captureDir") ?: return
        java.io.File(path).mkdirs()
        rule.runOnUiThread {
            val view=rule.activity.window.decorView
            val bitmap=android.graphics.Bitmap.createBitmap(view.width,view.height,android.graphics.Bitmap.Config.ARGB_8888)
            try {view.draw(android.graphics.Canvas(bitmap));java.io.File(path,"phase21-$name-sdk${android.os.Build.VERSION.SDK_INT}.png").outputStream().use {bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG,100,it)}} finally {bitmap.recycle()}
        }
    }
}
