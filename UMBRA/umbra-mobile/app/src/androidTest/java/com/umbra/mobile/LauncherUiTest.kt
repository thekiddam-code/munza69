package com.umbra.mobile

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class LauncherUiTest {
    @get:Rule val rule = createAndroidComposeRule<MainActivity>()
    @Test fun drawerSearchAndBackReturnToTerminal() {
        rule.onNodeWithText("APPS").performClick()
        rule.onNodeWithText("Search applications").performTextInput("umbra_no_such_app_123456")
        rule.onNodeWithText("No applications match.").assertIsDisplayed()
        rule.runOnUiThread { rule.activity.onBackPressedDispatcher.onBackPressed() }
        rule.onNodeWithText("01 / COMMAND DECK").assertIsDisplayed()
    }
    @Test fun masterSwitchSurvivesActivityRecreation() {
        rule.onNodeWithText("CONFIG").performClick()
        val toggle = rule.onNodeWithContentDescription("Master animations")
        toggle.performScrollTo()
        val before = toggle.fetchSemanticsNode().config[androidx.compose.ui.semantics.SemanticsProperties.ToggleableState]
        toggle.performClick()
        rule.waitUntil(5000) { toggle.fetchSemanticsNode().config[androidx.compose.ui.semantics.SemanticsProperties.ToggleableState] != before }
        // Wait for DataStore and its lifecycle-aware UI collector before recreation.
        rule.waitForIdle()
        val wasOn = toggle.fetchSemanticsNode().config[androidx.compose.ui.semantics.SemanticsProperties.ToggleableState] == androidx.compose.ui.state.ToggleableState.On
        rule.activityRule.scenario.recreate()
        rule.waitForIdle()
        rule.onNodeWithText("CONFIG").performClick()
        rule.onNodeWithContentDescription("Master animations").performScrollTo()
        rule.waitUntil(5000) {
            val on = rule.onNodeWithContentDescription("Master animations").fetchSemanticsNode().config[androidx.compose.ui.semantics.SemanticsProperties.ToggleableState] == androidx.compose.ui.state.ToggleableState.On
            on == wasOn
        }
    }
}
