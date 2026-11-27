package com.umbra.mobile

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*
import kotlin.math.abs

@Serializable data class GridCell(val id: String,val x: Int=0,val y: Int=0,val w: Int=1,val h: Int=1,val hidden: Boolean=false,val collapsed: Boolean=false)
@Serializable data class GridLayout(val version: Int=1,val columns: Int=3,val cells: List<GridCell> = emptyList())
const val MAX_GRID_COLUMNS=12
data class GridItem(val id: String,val title: String,val width: Int=1,val height: Int=1,val headerOnly: Boolean=false,val initialCollapsed: Boolean=false,val adaptiveSize: Boolean=false)
fun intersects(a: GridCell,b: GridCell)=a.x<b.x+b.w && a.x+a.w>b.x && a.y<b.y+b.h && a.y+a.h>b.y
fun nearestGridCell(item: GridCell,others: List<GridCell>,columns: Int,x: Int,y: Int): GridCell {
    val w=item.w.coerceIn(1,columns);val h=item.h.coerceIn(1,24)
    val desiredX=x.coerceIn(0,columns-w);val desiredY=y.coerceIn(0,2047-h)
    val occupied=HashSet<Int>()
    others.filterNot {it.hidden}.forEach {other->repeat(other.h){dy->repeat(other.w){dx->occupied.add((other.y+dy)*MAX_GRID_COLUMNS+other.x+dx)}}}
    for(distance in 0..4096) {
        val candidates=mutableListOf<Pair<Int,Int>>()
        for(col in 0..columns-w) {
            val vertical=distance-abs(col-desiredX)
            if(vertical>=0)for(row in listOf(desiredY-vertical,desiredY+vertical).distinct())if(row in 0..2047-h)candidates+=col to row
        }
        for((col,row) in candidates.sortedWith(compareBy<Pair<Int,Int>>{it.second}.thenBy{it.first})) {
            val free=(0 until h).all {dy->(0 until w).all {dx->(row+dy)*MAX_GRID_COLUMNS+col+dx !in occupied}}
            if(free)return item.copy(x=col,y=row,w=w,h=h)
        }
    }
    error("Grid capacity exceeded")
}
fun resolveGrid(items: List<GridItem>,stored: GridLayout?,columns: Int,compact: Boolean=false,forcedCollapsed: Set<String> = emptySet(),rowMajor: Boolean=false): GridLayout {
    val saved=stored?.cells?.associateBy {it.id} ?: emptyMap()
    val ordered=if(compact)items.sortedWith(compareBy<GridItem> {saved[it.id]?.y ?: Int.MAX_VALUE}.thenBy {saved[it.id]?.x ?: 0}) else items
    val placed=mutableListOf<GridCell>()
    ordered.forEachIndexed {index,item->
        val old=saved[item.id]
        val width=if(item.adaptiveSize)columns else old?.w?.let {if(stored!!.columns==columns)it else (it.toFloat()*columns/stored.columns).toInt().coerceAtLeast(1)} ?: item.width
        val cell=GridCell(item.id,old?.x?.let {if(stored!!.columns==columns)it else it*columns/stored.columns} ?: if(rowMajor)index%columns else 0,old?.y ?: if(rowMajor)index/columns else 0,width.coerceIn(1,columns),if((old?.collapsed ?: item.initialCollapsed) || item.id in forcedCollapsed)1 else if(item.adaptiveSize)item.height else old?.h ?: item.height,old?.hidden ?: false,old?.collapsed ?: item.initialCollapsed)
        if(cell.hidden)placed+=cell else placed+=nearestGridCell(cell,placed,columns,cell.x,if(compact)0 else old?.y ?: if(rowMajor)index/columns else 0)
    }
    return GridLayout(columns=columns,cells=placed)
}
fun GridLayout.move(id: String,x: Int,y: Int): GridLayout {
    val cell=cells.firstOrNull {it.id==id} ?: return this
    val next=nearestGridCell(cell,cells.filterNot {it.id==id},columns,x,y)
    return copy(cells=cells.map {if(it.id==id)next else it})
}
fun validateGrid(layout: GridLayout): GridLayout {
    require(layout.version==1 && layout.columns in 1..MAX_GRID_COLUMNS && layout.cells.size<=2048)
    require(layout.cells.map {it.id}.distinct().size==layout.cells.size)
    layout.cells.forEach {require(it.id.length in 1..180 && it.id.none(Char::isISOControl) && it.x in 0 until MAX_GRID_COLUMNS && it.y in 0..2047 && it.w in 1..MAX_GRID_COLUMNS && it.h in 1..24 && it.x+it.w<=layout.columns)}
    return layout
}
fun strictFields(value: JsonElement,strings: Set<String> = emptySet(),ints: Set<String> = emptySet(),bools: Set<String> = emptySet(),numbers: Set<String> = emptySet(),nested: Set<String> = emptySet()): JsonObject {
    val obj=value as? JsonObject ?: error("Expected object")
    require(obj.keys.all {it in strings+ints+bools+numbers+nested})
    obj.forEach {(key,v)->when(key) {
        in strings->require(v is JsonPrimitive && v.isString)
        in ints->require(v is JsonPrimitive && !v.isString && v.intOrNull!=null)
        in bools->require(v is JsonPrimitive && !v.isString && v.booleanOrNull!=null)
        in numbers->require(v is JsonPrimitive && !v.isString && v.doubleOrNull?.isFinite()==true)
    }}
    return obj
}
fun validateGridsJson(value: JsonElement) {
    val map=value as? JsonObject ?: error("Expected layouts");require(map.size<=128)
    map.values.forEach {v->val grid=strictFields(v,ints=setOf("version","columns"),nested=setOf("cells"));(grid["cells"] as? JsonArray ?: error("Missing cells")).forEach {strictFields(it,strings=setOf("id"),ints=setOf("x","y","w","h"),bools=setOf("hidden","collapsed"))}}
}
val STATUS_TABS=listOf("Main Home","Applications","Information Deck","ICARUS","Engineering","Lounge","Simulator","Instant Buttons","Settings","Command Center")
val DEFAULT_STATUS_TABS=STATUS_TABS.filterNot {it in listOf("Lounge","Instant Buttons")}.associateWith {it !in listOf("Applications","Settings")}
fun showStatusPanel(c: Config,tab: String)=c.statusPanel && (c.statusTabs[tab] ?: DEFAULT_STATUS_TABS[tab] ?: true)
