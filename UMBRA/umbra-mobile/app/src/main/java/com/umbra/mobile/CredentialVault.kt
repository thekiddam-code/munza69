package com.umbra.mobile

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.AtomicFile
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.*
import okhttp3.HttpUrl.Companion.toHttpUrl
import java.io.File
import java.io.IOException
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

// One phone pairing, encrypted with Android Keystore; never in DataStore or exports.
class CredentialVault(context: Context) {
    private val file=AtomicFile(File(context.noBackupFilesDir,"icarus_pairing.enc"))
    private val alias="umbra_icarus_pairing_v1"
    private fun key(): SecretKey {
        val store=KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
        (store.getKey(alias,null) as? SecretKey)?.let { return it }
        return KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES,"AndroidKeyStore").apply {
            init(KeyGenParameterSpec.Builder(alias,KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM).setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE).build())
        }.generateKey()
    }
    private fun binding(base: String)=base.toHttpUrl().toString().trimEnd('/')
    suspend fun read(base: String): String? = withContext(Dispatchers.IO) {
        if(base.isEmpty()) return@withContext null
        runCatching {
            require(file.baseFile.length()<=32768)
            val bytes=file.readFully();require(bytes.size in 30..32768 && bytes[0]==1.toByte())
            val cipher=Cipher.getInstance("AES/GCM/NoPadding")
            cipher.init(Cipher.DECRYPT_MODE,key(),GCMParameterSpec(128,bytes.copyOfRange(1,13)))
            val data=Json.parseToJsonElement(cipher.doFinal(bytes.copyOfRange(13,bytes.size)).decodeToString()).jsonObject
            if(data["server"]?.jsonPrimitive?.content==binding(base)) data["token"]?.jsonPrimitive?.content else null
        }.getOrNull()
    }
    suspend fun remember(base: String,token: String) = withContext(Dispatchers.IO) {
        try {
            val data=buildJsonObject { put("server",binding(base));put("token",token) }.toString().toByteArray()
            val cipher=Cipher.getInstance("AES/GCM/NoPadding").apply { init(Cipher.ENCRYPT_MODE,key()) }
            val encrypted=byteArrayOf(1)+cipher.iv+cipher.doFinal(data)
            val stream=file.startWrite()
            try { stream.write(encrypted);file.finishWrite(stream) } catch(e: Exception) { file.failWrite(stream);throw e }
        } catch(_: Exception) { throw IOException("Pairing could not be stored securely.") }
    }
    suspend fun clear() = withContext(Dispatchers.IO) { file.delete() }
}
