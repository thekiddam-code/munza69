package com.umbra.mobile
import org.junit.Assert.*
import org.junit.Test
class RefreshGateTest {
    @Test fun manualRequestDoesNotEnableFutureResumeChecks() {
        val gate=RefreshGate()
        assertFalse(gate.shouldRefresh(false,false,0,1,"server"))
        assertTrue(gate.shouldRefresh(false,false,1,1,"server"))
        assertFalse(gate.shouldRefresh(false,false,1,1,"server"))
        assertFalse(gate.shouldRefresh(false,false,1,2,"server"))
        assertTrue(gate.shouldRefresh(false,false,1,2,"changed server"))
    }
    @Test fun enabledResumeAndNetworkTriggersWorkIndependently() {
        val gate=RefreshGate()
        assertTrue(gate.shouldRefresh(true,false,0,0,"server"))
        assertFalse(gate.shouldRefresh(false,true,0,0,"server"))
        assertTrue(gate.shouldRefresh(false,true,0,1,"server"))
        assertFalse(gate.shouldRefresh(false,true,0,1,"server"))
    }
}
