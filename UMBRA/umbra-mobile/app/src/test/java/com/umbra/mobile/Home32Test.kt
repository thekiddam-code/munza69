package com.umbra.mobile

import kotlinx.serialization.json.*
import org.junit.Assert.*
import org.junit.Test

class Home32Test {
    @Test fun chromeAndFillPreferencesRoundTripWithoutResettingOldLayouts() {
        val item=DesktopItem("mixed","widget",widget=DesktopWidget(kind="icarus",buttonSet="mixed",fillPage=true,rows=8,buttonColumns=12))
        val c=Config(master=false,visualDetail=VisualDetail.Cinematic,homeHeaderCollapsed=true,homeFooterCollapsed=true,
            desktop=DesktopLayout(pages=listOf(DesktopPage("main","Control deck",items=listOf(item)))),widgetButtonSelections=mapOf("mixed" to listOf("quick:Nice shot!","sound:"+"0".repeat(32))))
        assertEquals(c,importConfig(exportConfig(c)))
        val legacy=c.copy(homeHeaderCollapsed=false,homeFooterCollapsed=false,desktop=c.desktop!!.updateItem("mixed"){it.copy(widget=it.widget!!.copy(fillPage=false,buttonSet="all"))})
        val old=exportConfig(legacy).replace("\"schemaVersion\":7","\"schemaVersion\":6")
            .replace("\"homeHeaderCollapsed\":false,","").replace("\"homeFooterCollapsed\":false,","").replace("\"fillPage\":false,","")
        val migrated=importConfig(old)
        assertFalse(migrated.homeHeaderCollapsed);assertFalse(migrated.homeFooterCollapsed)
        assertEquals(legacy.desktop,migrated.desktop);assertEquals(c.widgetButtonSelections,migrated.widgetButtonSelections)
        assertEquals(VisualDetail.Cinematic,migrated.visualDetail);assertFalse(migrated.master)
        assertTrue(runCatching {importConfig(exportConfig(c).replace("\"fillPage\":true","\"fillPage\":\"true\""))}.isFailure)
    }
    @Test fun fillPageAdaptsAtRenderTimeWithoutMutatingSavedCells() {
        val saved=GridLayout(columns=4,cells=listOf(GridCell("mixed",w=2,h=4),GridCell("clock",y=4,w=2,h=2)))
        val original=saved.copy()
        for(height in listOf(6,12,15)) {
            val displayed=resolveGrid(listOf(GridItem("mixed","Controls",4,height,adaptiveSize=true),GridItem("clock","Clock",2,2)),saved,4)
            val mixed=displayed.cells.first {it.id=="mixed"}
            assertEquals(4,mixed.w);assertEquals(height,mixed.h)
            assertFalse(intersects(mixed,displayed.cells.first {it.id=="clock"}))
            assertEquals(original,saved)
        }
        val collapsed=resolveGrid(listOf(GridItem("mixed","Controls",4,12,adaptiveSize=true)),saved,4,forcedCollapsed=setOf("mixed"))
        assertEquals(1,collapsed.cells.first().h)
        val packed=resolveGrid((0..11).map {GridItem("b$it","Button")},null,3,rowMajor=true)
        assertEquals(4,packed.cells.maxOf {it.y+it.h});assertEquals((0..11).map {it%3 to it/3},packed.cells.map {it.x to it.y})
        val retained=resolveGrid((0..11).map {GridItem("b$it","Button")},GridLayout(columns=3,cells=listOf(GridCell("b0",x=2,y=8))),3,rowMajor=true)
        assertEquals(8,retained.cells.first {it.id=="b0"}.y);assertEquals(2,retained.cells.first {it.id=="b0"}.x)
        val tablet=resolveGrid((0..23).map {GridItem("t$it","Tablet button")},null,12,rowMajor=true)
        assertEquals(2,tablet.cells.maxOf {it.y+it.h});assertEquals(12,tablet.cells.count {it.y==0})
        validateGrid(tablet)
        val acrossBoundary=nearestGridCell(GridCell("new"),listOf(GridCell("old",x=8,y=0)),12,0,1)
        assertEquals(0,acrossBoundary.x);assertEquals(1,acrossBoundary.y)
        val fullWidth=resolveGrid(listOf(GridItem("mixed","Controls",4,12,adaptiveSize=true)),saved,8)
        assertEquals(8,fullWidth.cells.first().w)
        val restored=resolveGrid(listOf(GridItem("mixed","Controls",3,8)),saved,4)
        assertEquals(2,restored.cells.first().w);assertEquals(4,restored.cells.first().h)
    }
    @Test fun mixedReferencesKeepSoundAndGameIdentityAndStaticColorFamilies() {
        val pc=PcStatus(1.0,2.0,false,listOf("Copy"),listOf("Nice shot!"),listOf(GameEmote(0,"Dance")))
        val controls=widgetCatalog(Config(),pc,null)+soundButtonActions(parseSoundCatalog(soundFixture(30)))
        assertEquals(30,controls.count {buttonFamily(it)==ButtonFamily.Soundboard})
        assertEquals(ButtonFamily.RocketLeague,buttonFamily(controls.first {it.id.startsWith("quick:")}))
        assertEquals(ButtonFamily.Fortnite,buttonFamily(controls.first {it.id.startsWith("emote:")}))
        assertEquals(ButtonFamily.PcHotkey,buttonFamily(controls.first {it.id.startsWith("macro:")}))
        assertEquals(controls.size,controls.map {it.id}.distinct().size)
        assertEquals(ButtonFamily.Minecraft,buttonFamily(InstantAction("mine","Mine","api/action",buildJsonObject {put("action","mine_toggle")})))
        assertTrue(ButtonFamily.PcHotkey.glow);assertFalse(ButtonFamily.Soundboard.glow)
        for(family in listOf(ButtonFamily.RocketLeague,ButtonFamily.Fortnite))assertTrue(family.color.blue>family.color.red)
        assertTrue(ButtonFamily.Minecraft.color.green>ButtonFamily.Minecraft.color.blue)
        assertTrue(ButtonFamily.Soundboard.color.red>.85f)
    }
}
