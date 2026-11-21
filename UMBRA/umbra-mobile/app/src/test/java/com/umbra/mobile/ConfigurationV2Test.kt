package com.umbra.mobile

import androidx.datastore.preferences.core.*
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.first
import org.junit.Assert.*
import org.junit.Test
import java.nio.file.Files

class ConfigurationV2Test {
    @Test fun roundTripAllCategoriesAndIndependentEffects() {
        val c=Config(startup=false,transitions=true,parallax=false,intensity=42,immersive=false,accent="#94B59A",
            favorites=setOf("example/App"),quickOrder=listOf("example/App"),quickLabels=mapOf("example/App" to "Phone"),
            moduleOrder=MODULES.reversed(),hiddenModules=setOf("Notifications"),indicators=setOf("Battery"),foregroundRefreshSeconds=60)
        assertEquals(c,importConfig(exportConfig(c)))
        assertFalse(importConfig(exportConfig(c.copy(master=false))).startup)
        assertEquals(c,importConfig(exportConfig(c.copy(master=false))).copy(master=true))
    }
    @Test fun malformedUnknownAndOversizedImportsFail() {
        val examples=listOf("{}", "[]", "{broken",exportConfig(Config()).replace("\"schemaVersion\":4","\"schemaVersion\":99"),
            exportConfig(Config()).replace("\"intensity\":65","\"intensity\":101"),exportConfig(Config()).replace("\"master\":true","\"master\":\"true\""),
            exportConfig(Config()).replace("\"Void\"","\"unsupported\"")," ".repeat(MAX_CONFIG_BYTES+1))
        examples.forEach { assertTrue(it.take(120),runCatching { importConfig(it) }.isFailure) }
        assertTrue(runCatching { importConfig(exportConfig(Config()).replace("\"settings\":{","\"settings\":{\"token\":\"secret\",")) }.isFailure)
    }
    @Test fun importsRejectUnsafeLayoutsUrlsAndColors() {
        listOf(Config(moduleOrder=listOf("Device")),Config(quickOrder=listOf("bad")),Config(accent="#000000"),
            Config(serverUrl="https://user:secret@host/"),Config(windowBrightness=Float.NaN),Config(quickLabels=mapOf("example/App" to "bad\nlabel")))
            .forEach { assertTrue(runCatching { validateConfig(it) }.isFailure) }
    }
    @Test fun zeroIntensityThermalAndScreenOffStopEffects() {
        assertFalse(motionPolicy(Config(intensity=0),false,false,true,false).enabled)
        assertFalse(motionPolicy(Config(),false,false,true,false,thermal=3).enabled)
        assertFalse(motionPolicy(Config(),false,false,true,false,screenOn=false).enabled)
        assertFalse(motionPolicy(Config(),false,false,true,false,thermal=2).continuous)
    }
    @Test fun categoryResetPreservesOtherSettingsAndOrderMovement() {
        val c=Config(intensity=12,immersive=false,url="https://deck.example/",moduleOrder=MODULES.reversed())
        val reset=resetCategory(c,"Animation")
        assertEquals(Config().intensity,reset.intensity);assertFalse(reset.immersive);assertEquals(c.url,reset.url)
        assertEquals(listOf("b","a","c"),moveItem(listOf("a","b","c"),"b",-1))
        assertEquals(listOf("a","b"),moveItem(listOf("a","b"),"a",-1))
    }
    @Test fun phaseOnePreferencesMigrateWithoutLosingSelections() = runBlocking {
        val dir=Files.createTempDirectory("umbra-migration").toFile()
        val scope=CoroutineScope(SupervisorJob()+Dispatchers.IO)
        val data=PreferenceDataStoreFactory.create(scope=scope,produceFile={dir.resolve("migration.preferences_pb")})
        try {
            data.edit { p -> p[booleanPreferencesKey("transitions")]=false; p[booleanPreferencesKey("master")]=false
                p[booleanPreferencesKey("environment")]=true; p[stringSetPreferencesKey("favorites")]=setOf("example/App") }
            val store=ConfigStore(data)
            val c=store.config.first()
            assertFalse(c.startup);assertFalse(c.transitions);assertFalse(c.master);assertTrue(c.environment)
            assertEquals(setOf("example/App"),c.favorites)
            store.update { it.copy(intensity=32) }
            assertEquals(32,store.config.first().intensity);assertFalse(store.config.first().startup)
        } finally { scope.coroutineContext[Job]!!.cancelAndJoin();dir.deleteRecursively() }
    }
}
