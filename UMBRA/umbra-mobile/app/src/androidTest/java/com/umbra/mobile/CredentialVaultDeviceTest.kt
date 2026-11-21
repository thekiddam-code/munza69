package com.umbra.mobile

import android.content.ContextWrapper
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import kotlinx.coroutines.runBlocking
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.util.UUID

@RunWith(AndroidJUnit4::class)
class CredentialVaultDeviceTest {
    @Test fun pairingIsEncryptedBoundToServerAndClearable() = runBlocking {
        val target=InstrumentationRegistry.getInstrumentation().targetContext
        val dir=File(target.cacheDir,"umbra-vault-test-${UUID.randomUUID()}").apply { mkdirs() }
        val isolated=object: ContextWrapper(target) { override fun getNoBackupFilesDir()=dir }
        val vault=CredentialVault(isolated)
        val token="test_pairing_token_123456789"
        try {
            vault.remember("https://deck.example/",token)
            assertEquals(token,vault.read("https://deck.example/"))
            assertNull(vault.read("https://other.example/"))
            assertNull(vault.read("http://deck.example/"))
            assertNull(vault.read("https://deck.example/another-base/"))
            assertFalse(File(dir,"icarus_pairing.enc").readBytes().decodeToString().contains(token))
            assertFalse(exportConfig(Config()).contains(token))
            vault.clear();assertNull(vault.read("https://deck.example/"))
        } finally { dir.deleteRecursively() }
    }
}
