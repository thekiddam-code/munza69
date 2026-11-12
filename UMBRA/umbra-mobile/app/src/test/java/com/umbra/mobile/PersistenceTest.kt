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
            }
            createAndUse { store ->
                val c=store.config.first()
                assertFalse(c.master); assertTrue(c.environment); assertFalse(c.wallpaper)
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
}
