package com.umbra.mobile

import org.junit.Assert.*
import org.junit.Test

class Phase23GridTest {
    @Test fun mixedSpansSnapWithoutOverlapAcrossDensities() {
        val items=(0..39).map {GridItem("item-$it","Item",if(it%5==0)2 else 1,if(it%7==0)2 else 1)}
        var layout: GridLayout?=null
        for(columns in listOf(2,3,4,8,2)) {
            layout=resolveGrid(items,layout,columns)
            layout.cells.forEach {a->assertTrue(a.x>=0 && a.x+a.w<=columns);assertTrue(layout!!.cells.none {b->a.id!=b.id && intersects(a,b)})}
            layout=relocateGrid(layout,"item-39",0,0)
            assertEquals(0,layout.cells.first {it.id=="item-39"}.y)
            layout.cells.forEach {a->assertFalse(layout!!.cells.any {b->a.id!=b.id && intersects(a,b)})}
        }
    }
    @Test fun collapsedModulesKeepExpandedSizesAndStableOrder() {
        val items=listOf(GridItem("a","A",2,7,true),GridItem("b","B",2,5,true))
        val saved=GridLayout(columns=2,cells=listOf(GridCell("a",w=2,h=7,collapsed=true),GridCell("b",y=1,w=2,h=5,collapsed=true)))
        val actual=resolveGrid(items,saved,2,compact=true)
        assertEquals(listOf(1,1),actual.cells.map {it.h})
        val moved=relocateGrid(actual,"b",0,0)
        assertEquals("b",moved.cells.minBy {it.y}.id)
        assertTrue(moved.cells.all {it.collapsed})
        val expanded=saved.copy(cells=saved.cells.map {if(it.id=="a")it.copy(collapsed=false) else it})
        assertEquals(7,resolveGrid(items,expanded,2,true).cells.first {it.id=="a"}.h)
    }
    @Test fun hiddenCellsDoNotOccupySlotsAndBadImportsFail() {
        val layout=resolveGrid(listOf(GridItem("a","A"),GridItem("b","B")),GridLayout(columns=2,cells=listOf(GridCell("a",hidden=true))),2)
        assertEquals(0,layout.cells.first {it.id=="b"}.y)
        assertTrue(runCatching {importConfig(exportConfig(Config(gridLayouts=mapOf("deck" to layout))).replace("\"x\":0","\"x\":\"0\""))}.isFailure)
        assertTrue(runCatching {validateGrid(layout.copy(cells=layout.cells+layout.cells.first()))}.isFailure)
    }
    @Test fun modeVisibilityAndMotionRemainIndependent() {
        val c=Config(master=false,visualDetail=VisualDetail.Cinematic,commandExpanded=false,statusTabs=DEFAULT_STATUS_TABS+("Applications" to true))
        val restored=importConfig(exportConfig(c))
        assertFalse(restored.master);assertFalse(restored.commandExpanded);assertEquals(VisualDetail.Cinematic,restored.visualDetail)
        assertTrue(showStatusPanel(restored,"Applications"));assertFalse(showStatusPanel(restored,"Settings"))
        assertFalse(showStatusPanel(restored.copy(statusPanel=false),"Applications"))
        assertTrue(restored.immersive)
    }
}
