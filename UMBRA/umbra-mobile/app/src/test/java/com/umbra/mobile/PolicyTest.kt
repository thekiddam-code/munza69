package com.umbra.mobile
import org.junit.Assert.*
import org.junit.Test
class PolicyTest {
    @Test fun acceptsPrivateAndPublicWebDestinations() {
        listOf("https://deck.example/remote", "http://100.64.0.1:8080/", "http://icarus.tailnet.ts.net", "http://[::1]:8080/").forEach { assertTrue(it, validDeckUrl(it)) }
    }
    @Test fun rejectsCredentialsTokensAndMalformedUrls() {
        listOf("", "javascript:alert(1)", "file:///etc/passwd", "https://user:secret@host/", "https://host/?token=secret", "https://host/#secret", "https://host:65536", "http://[fe80::1%25zone]/", "https://", "https://a b/", "https://host/\n").forEach { assertFalse(it,validDeckUrl(it)) }
    }
    @Test fun powerAndAccessibilityOverrideEveryProfile() {
        Profile.entries.forEach { profile ->
            val c=Config(profile=profile)
            assertFalse(motionPolicy(c,true,false,true,false).enabled)
            assertFalse(motionPolicy(c,false,true,true,false).enabled)
            assertFalse(motionPolicy(c,false,false,false,false).enabled)
        }
    }
    @Test fun masterDoesNotMutateIndividualSelections() {
        val c=Config(environment=true,wallpaper=false,ambient=true)
        assertFalse(motionPolicy(c.copy(master=false),false,false,true,false).enabled)
        assertTrue(motionPolicy(c.copy(master=false).copy(master=true),false,false,true,false).enabled)
        assertEquals(c,c.copy(master=false).copy(master=true))
    }
    @Test fun interactionStopsContinuousEffectsAndMinimalIsInstant() {
        assertFalse(motionPolicy(Config(),false,false,true,true).continuous)
        assertTrue(motionPolicy(Config(),false,false,true,false).continuous)
        assertEquals(0,motionPolicy(Config(profile=Profile.Minimal),false,false,true,false).duration)
    }
}
