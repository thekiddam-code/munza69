package com.umbra.mobile

// A manual Check must not become a permanent polling/resume latch.
class RefreshGate {
    private var manualSeen=0
    private var networkSeen: Long?=null
    private var configurationSeen: String?=null
    fun shouldRefresh(onResume: Boolean,onNetwork: Boolean,manual: Int,network: Long,configuration: String): Boolean {
        val manualChanged=manual != manualSeen
        val networkChanged=networkSeen?.let { it != network } ?: false
        val configurationChanged=configurationSeen?.let { it != configuration } ?: false
        manualSeen=manual;networkSeen=network;configurationSeen=configuration
        return onResume || manualChanged || configurationChanged || (onNetwork && networkChanged)
    }
}
