package com.umbra.mobile

import org.junit.Assert.*
import org.junit.Test

class Phase21PolicyTest {
    @Test fun detailAndTransitionsAreIndependentOfMotion() {
        assertEquals(VisualDetail.Enhanced,Config().visualDetail)
        val c=Config(visualDetail=VisualDetail.Cinematic,master=false,transitionStyle=TransitionStyle.SamsungInspired)
        val decoded=importConfig(exportConfig(c))
        assertEquals(VisualDetail.Cinematic,decoded.visualDetail)
        TransitionCategory.entries.forEach {category->assertFalse(transitionPlan(decoded,motionPolicy(decoded,false,false,true,false),category).enabled)}
        assertFalse(c.copy(visualDetail=VisualDetail.Minimal).master)
        assertEquals(VisualDetail.Cinematic,resetCategory(c,"Animation").visualDetail)
    }
    @Test fun allTransitionCategoriesDisableSeparately() {
        val base=Config()
        val motion=motionPolicy(base,false,false,true,false)
        assertTrue(transitionPlan(base,motion,TransitionCategory.App).originExpansion)
        assertFalse(transitionPlan(base.copy(appLaunchTransitions=false),motion,TransitionCategory.App).enabled)
        assertTrue(transitionPlan(base.copy(appLaunchTransitions=false),motion,TransitionCategory.Folder).enabled)
        assertFalse(transitionPlan(base.copy(folderTransitions=false),motion,TransitionCategory.Folder).enabled)
        assertFalse(transitionPlan(base.copy(widgetTransitions=false),motion,TransitionCategory.Widget).enabled)
        assertFalse(transitionPlan(base.copy(commandAnimations=false),motion,TransitionCategory.CommandCenter).enabled)
        assertFalse(transitionPlan(base.copy(transitions=false),motion,TransitionCategory.Panel).enabled)
        TransitionCategory.entries.forEach {assertFalse(transitionPlan(base.copy(transitionStyle=TransitionStyle.Minimal),motion,it).enabled)}
    }
    @Test fun legacySchemaImportsUpgradeToEnhancedWithoutResettingSelections() {
        val old=exportConfig(Config(master=false,environment=true)).replace("\"schemaVersion\":5","\"schemaVersion\":2")
        val c=importConfig(old)
        assertFalse(c.master);assertTrue(c.environment);assertEquals(VisualDetail.Enhanced,c.visualDetail)
    }
    @Test fun pagesFoldersMovesAndDeletionKeepStableReferences() {
        val a=DesktopItem("a",component="example/First")
        val b=DesktopItem("b",component="example/Second")
        var layout=DesktopLayout(pages=listOf(DesktopPage("main",items=listOf(a,b)),DesktopPage("next")))
        layout=validateDesktop(layout.groupApps("a","b"))
        assertEquals(listOf("example/Second","example/First"),layout.item("b")!!.folder!!.apps)
        layout=validateDesktop(layout.moveItem("b","next"))
        assertTrue(layout.page("main").items.isEmpty());assertEquals("b",layout.page("next").items.single().id)
        layout=validateDesktop(layout.reorderPage("next",-1).removePage("next"))
        assertEquals("b",layout.page("main").items.single().id)
        assertTrue(layout.removeItem("b").pages.single().items.isEmpty())
        assertEquals(layout,layout.moveItem("b","removed-page"))
        assertEquals(layout,layout.removePage("removed-page"))
    }
    @Test fun portableWidgetsRequireRebindingAndMalformedNestedTypesFail() {
        val widget=DesktopItem("widget","widget",widget=DesktopWidget(kind="android",appWidgetId=11,provider="example/Widget"))
        val c=Config(desktop=DesktopLayout(pages=listOf(DesktopPage("main",items=listOf(widget)))))
        val imported=importConfig(exportConfig(c))
        assertEquals(0,imported.desktop!!.item("widget")!!.widget!!.appWidgetId)
        val malformed=exportConfig(c).replace("\"rows\":2","\"rows\":\"2\"")
        assertTrue(runCatching {importConfig(malformed)}.isFailure)
        assertTrue(runCatching {validateDesktop(c.desktop!!.copy(pages=c.desktop.pages+c.desktop.pages))}.isFailure)
    }
    @Test fun folderWidgetAndPagePreferencesPersistThroughCodec() {
        val layout=DesktopLayout(homePageId="info",pages=listOf(DesktopPage("main",items=listOf(DesktopItem("folder","folder",folder=DesktopFolder("Daily",listOf("example/App"))))),DesktopPage("info",columns=4,items=listOf(DesktopItem("clock","widget",widget=DesktopWidget(style="Analog",clock24=false,seconds=true,span=4))))))
        val c=Config(desktop=layout,visualDetail=VisualDetail.Cinematic,transitionStyle=TransitionStyle.UmbraCinematic,weatherPlace="Chosen city",weatherLatitude=41.1,weatherLongitude=-87.1)
        assertEquals(c,importConfig(exportConfig(c)))
    }
}
