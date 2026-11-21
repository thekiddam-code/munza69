package com.umbra.mobile

import androidx.datastore.preferences.core.*
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.first
import org.junit.Assert.*
import org.junit.Test
import java.nio.file.Files

class Phase23PersistenceTest {
    @Test fun schemaThreeMigrationPreservesHostIdsAndPersistsAllModuleFlags() = runBlocking {
        val dir=Files.createTempDirectory("umbra-23").toFile();val file=dir.resolve("settings.preferences_pb")
        val desktop=DesktopLayout(pages=listOf(DesktopPage("main",items=listOf(DesktopItem("native","widget",widget=DesktopWidget(kind="android",appWidgetId=0,provider="example/Widget")),DesktopItem("folder","folder",folder=DesktopFolder("Saved",listOf("example/App")))))))
        val initial=Config(desktop=desktop,master=false,environment=true,favorites=setOf("example/App"),url="https://deck.example/",instantFavorites=setOf("quick:Saved"))
        val old=exportConfig(initial).replace("\"schemaVersion\":4","\"schemaVersion\":3").replace("\"appWidgetId\":0","\"appWidgetId\":42")
        suspend fun useStore(block: suspend (androidx.datastore.core.DataStore<androidx.datastore.preferences.core.Preferences>,ConfigStore)->Unit) {
            val scope=CoroutineScope(SupervisorJob()+Dispatchers.IO);val data=PreferenceDataStoreFactory.create(scope=scope,produceFile={file})
            try {block(data,ConfigStore(data))} finally {scope.coroutineContext[Job]!!.cancelAndJoin()}
        }
        try {
            useStore {data,store->
                data.edit {it[stringPreferencesKey("config_v2")]=old}
                val migrated=store.config.first();assertEquals(42,migrated.desktop!!.item("native")!!.widget!!.appWidgetId)
                assertEquals(initial.url,migrated.url);assertFalse(migrated.master);assertTrue(migrated.environment);assertEquals(initial.instantFavorites,migrated.instantFavorites)
                store.update {it.copy(commandExpanded=false,gridLayouts=mapOf("command" to GridLayout(columns=2,cells=listOf(GridCell("Device",x=1,y=3,w=1,h=8,hidden=true,collapsed=true)))),statusTabs=it.statusTabs+("Applications" to true))}
            }
            useStore {_,store->val saved=store.config.first();assertFalse(saved.commandExpanded);assertFalse(saved.master);assertTrue(saved.statusTabs.getValue("Applications"))
                val cell=saved.gridLayouts.getValue("command").cells.single();assertEquals(3,cell.y);assertEquals(8,cell.h);assertTrue(cell.hidden);assertTrue(cell.collapsed)
                assertEquals(42,saved.desktop!!.item("native")!!.widget!!.appWidgetId);assertEquals(0,importConfig(exportConfig(saved)).desktop!!.item("native")!!.widget!!.appWidgetId)
                assertEquals(listOf("example/App"),saved.desktop.item("folder")!!.folder!!.apps)
            }
        } finally {dir.deleteRecursively()}
    }
}
