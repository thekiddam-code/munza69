package com.umbra.mobile
import org.junit.Assert.*
import org.junit.Test
class AnimationEngineTest {
    @Test fun commandAndTerminalTransitionSwitchesAreIndependentInBothDirections() {
        val c=Config(transitions=false,commandAnimations=true)
        assertTrue(pageAnimationAllowed("HOME","COMMAND",c))
        assertTrue(pageAnimationAllowed("COMMAND","HOME",c))
        assertFalse(pageAnimationAllowed("HOME","APPS",c))
        val inverse=c.copy(transitions=true,commandAnimations=false)
        assertFalse(pageAnimationAllowed("HOME","COMMAND",inverse))
        assertFalse(pageAnimationAllowed("COMMAND","HOME",inverse))
        assertTrue(pageAnimationAllowed("HOME","APPS",inverse))
    }
    @Test fun allNineSelectionsSurviveMasterOverrideAndZeroIntensity() {
        val c=Config(ambient=false,wallpaper=true,transitions=false,startup=true,parallax=false,statusEffects=true,environment=true,alerts=false,commandAnimations=true)
        val disabled=importConfig(exportConfig(c.copy(master=false)))
        assertEquals(c,disabled.copy(master=true))
        assertFalse(motionPolicy(disabled,false,false,true,false).enabled)
        assertFalse(motionPolicy(c.copy(intensity=0),false,false,true,false).enabled)
    }
}
