package com.umbra.mobile

import androidx.datastore.preferences.core.PreferenceDataStoreFactory
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.first
import org.junit.Assert.*
import org.junit.Test
import java.nio.file.Files

class PersistenceTest {
    @Test fun settingsSurviveStoreRecreationAndMasterPreservesFlags() = runBlocking {
        val dir = Files.createTempDirectory("umbra-test").toFile()
        val file = dir.resolve("test.preferences_pb")
        suspend fun createAndUse(block: suspend (ConfigStore) -> Unit) {
            val scope = CoroutineScope(SupervisorJob()+Dispatchers.IO)
            val data = PreferenceDataStoreFactory.create(scope=scope,produceFile={file})
            try { block(ConfigStore(data)) } finally { scope.coroutineContext[Job]!!.cancelAndJoin() }
        }
        try {
            createAndUse { store ->
                store.flag("environment",true); store.flag("wallpaper",false)
                store.flag("master",false); store.profile(Profile.Cinematic)
                store.deck("http://icarus.tailnet.ts.net:8080/",12)
                store.favorite("example/App")
                store.update { it.copy(intensity=37,startup=false,commandAnimations=false,moduleOrder=MODULES.reversed(),accent="#94B59A",hideTopBar=false) }
            }
            createAndUse { store ->
                val c=store.config.first()
                assertFalse(c.master); assertTrue(c.environment); assertFalse(c.wallpaper)
                assertEquals(37,c.intensity);assertFalse(c.startup);assertFalse(c.commandAnimations)
                assertEquals(MODULES.reversed(),c.moduleOrder);assertEquals("#94B59A",c.accent);assertFalse(c.hideTopBar)
                assertEquals(Profile.Cinematic,c.profile); assertEquals(12,c.timeout)
                assertEquals("http://icarus.tailnet.ts.net:8080/",c.url)
                assertTrue("example/App" in c.favorites)
                store.flag("master",true)
                assertTrue(store.config.first().environment)
                store.favorite("example/App")
                assertTrue(store.config.first().favorites.isEmpty())
            }
        } finally { dir.deleteRecursively() }
    }
    @Test fun nativeWidgetIdsAndWorkspaceSurviveDataStoreRecreation() = runBlocking {
        val dir=Files.createTempDirectory("umbra-layout").toFile();val file=dir.resolve("settings.preferences_pb")
        val layout=DesktopLayout(pages=listOf(DesktopPage("main",items=listOf(
            DesktopItem("daily","folder",folder=DesktopFolder("Daily",listOf("example/App"))),
            DesktopItem("native","widget",widget=DesktopWidget(kind="android",appWidgetId=42,provider="example/Provider"))))))
        suspend fun useStore(block: suspend (ConfigStore)->Unit) {
            val scope=CoroutineScope(SupervisorJob()+Dispatchers.IO)
            val data=PreferenceDataStoreFactory.create(scope=scope,produceFile={file})
            try {block(ConfigStore(data))} finally {scope.coroutineContext[Job]!!.cancelAndJoin()}
        }
        try {
            useStore {it.replace(Config(desktop=layout,transitionStyle=TransitionStyle.UmbraCinematic,folderTransitions=false,visualDetail=VisualDetail.Cinematic))}
            useStore {store->val c=store.config.first()
                assertEquals(layout,c.desktop);assertEquals(42,c.desktop!!.item("native")!!.widget!!.appWidgetId)
                assertEquals(0,importConfig(exportConfig(c)).desktop!!.item("native")!!.widget!!.appWidgetId)
                assertFalse(c.folderTransitions);assertEquals(TransitionStyle.UmbraCinematic,c.transitionStyle)
                store.update {it.copy(master=false)}
            }
            useStore {store->val c=store.config.first();assertFalse(c.master);assertFalse(c.folderTransitions);assertEquals(VisualDetail.Cinematic,c.visualDetail);assertEquals(layout,c.desktop)}
        } finally {dir.deleteRecursively()}
    }
}
