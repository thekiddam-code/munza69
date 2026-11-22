package com.umbra.mobile

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*
import java.util.UUID

fun desktopId()=UUID.randomUUID().toString()
@Serializable data class DesktopFolder(val name: String="Folder",val apps: List<String> = emptyList())
@Serializable data class DesktopWidget(
    val collapsed: Boolean=false,val showDetails: Boolean=true,
    val title: String="",val buttonSet: String="all",val buttonColumns: Int=2,val buttonHeight: Int=64,
    val buttonOverrides: Map<String,CustomButton> = emptyMap(),
    val kind: String="clock",val style: String="Digital",val span: Int=3,val rows: Int=2,
    val clock24: Boolean=true,val seconds: Boolean=false,val transparent: Boolean=true,val accent: String="",
    val appWidgetId: Int=0,val provider: String=""
)
@Serializable data class DesktopItem(val id: String="",val kind: String="app",val component: String="",val folder: DesktopFolder?=null,val widget: DesktopWidget?=null)
@Serializable data class DesktopPage(val id: String="",val name: String="Deck",val kind: String="blank",val columns: Int=3,val items: List<DesktopItem> = emptyList())
@Serializable data class DesktopLayout(val schemaVersion: Int=1,val homePageId: String="main",val pages: List<DesktopPage> = emptyList())
val CLOCK_STYLES=listOf("Digital","Terminal","Analog","Segmented","Date and time")
val WIDGET_KINDS=listOf("clock","weather","battery","calendar","system","icarus","soundboard","android")+ENGINEERING_KINDS
private fun validDesktopId(value: String)=Regex("[A-Za-z0-9_-]{1,64}").matches(value)
private fun validDesktopName(value: String)=value.length in 1..48 && value.none(Char::isISOControl)
fun validateDesktop(layout: DesktopLayout): DesktopLayout {
    require(layout.schemaVersion==1 && layout.pages.size in 1..12)
    require(layout.pages.map { it.id }.distinct().size==layout.pages.size && layout.pages.any { it.id==layout.homePageId })
    val items=layout.pages.flatMap { it.items }
    require(items.size<=256 && items.map { it.id }.distinct().size==items.size)
    layout.pages.forEach { p ->
        require(validDesktopId(p.id) && validDesktopName(p.name) && p.kind in listOf("terminal","information","icarus","blank") && p.columns in 2..8 && p.items.size<=256)
        p.items.forEach { item ->
            require(validDesktopId(item.id))
            when(item.kind) {
                "app" -> require(validComponent(item.component) && item.folder==null && item.widget==null)
                "folder" -> {
                    val f=requireNotNull(item.folder)
                    require(item.component.isEmpty() && item.widget==null && validDesktopName(f.name) && f.apps.size<=64 && f.apps.distinct().size==f.apps.size && f.apps.all(::validComponent))
                }
                "widget" -> {
                    val w=requireNotNull(item.widget)
                    require(item.component.isEmpty() && item.folder==null && w.kind in WIDGET_KINDS && w.style in CLOCK_STYLES && w.span in 1..8 && w.rows in 1..12 && validAccent(w.accent))
                    require(w.title.length<=48 && w.title.none(Char::isISOControl) && w.buttonSet in BUTTON_SETS && w.buttonColumns in 1..6 && w.buttonHeight in 56..96)
                    require(w.buttonOverrides.size<=512 && w.buttonOverrides.keys.all {it.length in 1..180 && it.none(Char::isISOControl)})
                    w.buttonOverrides.values.forEach {require(it.kind!=OutputKind.TvKey);validateButton(it)}
                    require(w.appWidgetId>=0 && (w.kind!="android" || validComponent(w.provider)))
                    if(w.kind!="android")require(w.appWidgetId==0 && w.provider.isEmpty())
                }
                else -> error("Unknown desktop item")
            }
        }
    }
    require(items.mapNotNull { it.widget?.appWidgetId?.takeIf { id->id>0 } }.let { it.distinct().size==it.size })
    return layout
}
fun resolvedDesktop(c: Config,apps: List<LaunchApp> = emptyList()): DesktopLayout {
    c.desktop?.let { return it }
    val pinned=orderedFavorites(c,apps).map { it.id }
    val order=(pinned+c.quickOrder.filter { it in c.favorites }+c.favorites.sorted()).distinct()
    fun widget(id: String,kind: String,style: String="Digital",rows: Int=2)=DesktopItem(id,"widget",widget=DesktopWidget(kind=kind,style=style,rows=rows))
    return DesktopLayout(pages=listOf(
        DesktopPage("main","Main Terminal","terminal",c.gridColumns,order.map { DesktopItem(UUID.nameUUIDFromBytes(it.toByteArray()).toString(),component=it) }),
        DesktopPage("information","Information Deck","information",3,listOf(widget("info-clock","clock","Date and time"),widget("info-weather","weather"),widget("info-battery","battery"),widget("info-calendar","calendar",rows=3))),
        DesktopPage("icarus","ICARUS Command Deck","icarus",3,listOf(widget("icarus-instant","icarus",rows=4)))
    ))
}
fun DesktopLayout.page(id: String)=pages.first { it.id==id }
fun DesktopLayout.item(id: String)=pages.flatMap { it.items }.firstOrNull { it.id==id }
fun DesktopLayout.updatePage(id: String,change: (DesktopPage)->DesktopPage)=copy(pages=pages.map { if(it.id==id)change(it) else it })
fun DesktopLayout.updateItem(id: String,change: (DesktopItem)->DesktopItem)=copy(pages=pages.map { p->p.copy(items=p.items.map { if(it.id==id)change(it) else it }) })
fun DesktopLayout.removeItem(id: String)=copy(pages=pages.map { p->p.copy(items=p.items.filterNot { it.id==id }) })
fun DesktopLayout.moveItem(id: String,pageId: String,before: String?=null): DesktopLayout {
    val moving=item(id) ?: return this
    if(id==before || pages.none {it.id==pageId})return this
    val removed=removeItem(id)
    return removed.updatePage(pageId) { p->val items=p.items.toMutableList();val index=items.indexOfFirst { it.id==before };items.add(if(index<0)items.size else index,moving);p.copy(items=items) }
}
fun DesktopLayout.groupApps(source: String,target: String): DesktopLayout {
    val from=item(source) ?: return this;val to=item(target) ?: return this
    if(source==target || from.kind!="app")return this
    val removed=removeItem(source)
    return when(to.kind) {
        "app" -> removed.updateItem(target) { DesktopItem(it.id,"folder",folder=DesktopFolder("Folder",listOf(to.component,from.component).distinct())) }
        "folder" -> removed.updateItem(target) { it.copy(folder=it.folder!!.copy(apps=(it.folder.apps+from.component).distinct())) }
        else -> this
    }
}
fun DesktopLayout.removePage(id: String): DesktopLayout {
    if(pages.size==1 || pages.none {it.id==id})return this
    val removed=page(id);val remaining=pages.filterNot { it.id==id };val destination=remaining.first()
    return copy(homePageId=if(homePageId==id)destination.id else homePageId,pages=remaining.map { if(it.id==destination.id)it.copy(items=it.items+removed.items) else it })
}
fun DesktopLayout.reorderPage(id: String,delta: Int): DesktopLayout {
    val pages=pages.toMutableList();val from=pages.indexOfFirst { it.id==id };if(from<0)return this
    val to=(from+delta).coerceIn(0,pages.lastIndex);val moved=pages.removeAt(from);pages.add(to,moved);return copy(pages=pages)
}
fun portableDesktop(layout: DesktopLayout)=layout.copy(pages=layout.pages.map { p->p.copy(items=p.items.map { item->if(item.widget?.kind=="android")item.copy(widget=item.widget.copy(appWidgetId=0)) else item }) })

// Explicit shape checks prevent kotlinx.serialization's primitive coercions in imported nested data.
fun validateDesktopJson(value: JsonElement) {
    fun typed(value: JsonElement,strings: Set<String>,ints: Set<String>,bools: Set<String>,objects: Set<String> = emptySet(),arrays: Set<String> = emptySet()): JsonObject {
        val o=value as? JsonObject ?: error("Expected layout object")
        require(o.keys.all { it in strings+ints+bools+objects+arrays })
        o.forEach { (k,v) -> when(k) {
            in strings -> require(v is JsonPrimitive && v.isString)
            in ints -> require(v is JsonPrimitive && !v.isString && v.intOrNull!=null)
            in bools -> require(v is JsonPrimitive && !v.isString && v.booleanOrNull!=null)
            in objects -> require(v is JsonObject || v is JsonNull)
            in arrays -> require(v is JsonArray)
        } }
        return o
    }
    val root=typed(value,setOf("homePageId"),setOf("schemaVersion"),emptySet(),arrays=setOf("pages"))
    require(root["schemaVersion"]?.jsonPrimitive?.intOrNull==1)
    val pages=root["pages"] as? JsonArray ?: error("Missing pages");require(pages.size in 1..12)
    pages.forEach { p ->
        val page=typed(p,setOf("id","name","kind"),setOf("columns"),emptySet(),arrays=setOf("items"))
        val items=page["items"] as? JsonArray ?: JsonArray(emptyList());require(items.size<=256)
        items.forEach { entry ->
            val item=typed(entry,setOf("id","kind","component"),emptySet(),emptySet(),objects=setOf("folder","widget"))
            item["folder"]?.takeUnless { it is JsonNull }?.let { folder ->
                val f=typed(folder,setOf("name"),emptySet(),emptySet(),arrays=setOf("apps"))
                val apps=f["apps"] as? JsonArray ?: JsonArray(emptyList());require(apps.size<=64 && apps.all { it is JsonPrimitive && it.isString })
            }
            item["widget"]?.takeUnless { it is JsonNull }?.let { widget -> val obj=typed(widget,setOf("kind","style","accent","provider","title","buttonSet"),setOf("span","rows","appWidgetId","buttonColumns","buttonHeight"),setOf("clock24","seconds","transparent","collapsed","showDetails"),objects=setOf("buttonOverrides"))
                (obj["buttonOverrides"] as? JsonObject)?.let {validateButtonsJson(JsonArray(it.values.toList()))} }
        }
    }
}
