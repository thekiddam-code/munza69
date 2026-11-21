package com.umbra.mobile

import android.app.ActivityOptions
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.View
import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.geometry.Rect
import kotlinx.serialization.Serializable
import kotlin.math.roundToInt

@Serializable enum class TransitionStyle { SamsungInspired, UmbraCinematic, Minimal, NativeAndroid }
enum class TransitionCategory { App, Folder, Widget, CommandCenter, Panel }
data class TransitionPlan(val enabled: Boolean,val duration: Int,val originExpansion: Boolean)
fun transitionPlan(c: Config,motion: MotionPolicy,category: TransitionCategory): TransitionPlan {
    val selected=when(category){TransitionCategory.App->c.appLaunchTransitions;TransitionCategory.Folder->c.folderTransitions;TransitionCategory.Widget->c.widgetTransitions;TransitionCategory.CommandCenter->c.commandAnimations;TransitionCategory.Panel->c.transitions}
    val enabled=motion.enabled && selected && c.transitionStyle!=TransitionStyle.Minimal
    val baseDuration=if(c.transitionStyle==TransitionStyle.UmbraCinematic) minOf(320,motion.duration+60) else minOf(200,motion.duration)
    val duration=if(!enabled)0 else (baseDuration*(.35f+.65f*c.intensity/100f)).roundToInt().coerceAtLeast(1)
    return TransitionPlan(enabled,duration,enabled && c.transitionStyle!=TransitionStyle.NativeAndroid)
}
fun panelTransition(from: String,to: String,c: Config,motion: MotionPolicy): ContentTransform {
    val command=from=="COMMAND" || to=="COMMAND"
    val plan=transitionPlan(c,motion,if(command)TransitionCategory.CommandCenter else TransitionCategory.Panel)
    if(!plan.enabled)return EnterTransition.None togetherWith ExitTransition.None
    val reveal=if(command) {
        if(to=="COMMAND") slideInVertically(tween(plan.duration)){ -it/12 } else slideInVertically(tween(plan.duration)){ it/24 }
    } else slideInVertically(tween(plan.duration)){it/80}
    val exit=if(command && from=="COMMAND") slideOutVertically(tween(plan.duration)){-it/12} else ExitTransition.None
    return (fadeIn(tween(plan.duration))+reveal) togetherWith (fadeOut(tween(plan.duration))+exit)
}
val LocalIconLaunch=staticCompositionLocalOf<((LaunchApp,Rect?)->Unit)?> { null }
val LocalLauncherConfig=staticCompositionLocalOf { Config() }
fun appLaunchOptions(context: Context,anchor: View,bounds: Rect?,c: Config,motion: MotionPolicy): Bundle? {
    val plan=transitionPlan(c,motion,TransitionCategory.App)
    if(!plan.enabled)return ActivityOptions.makeCustomAnimation(context,0,0).toBundle()
    if(c.transitionStyle==TransitionStyle.NativeAndroid)return null
    return runCatching {
        if(bounds==null || bounds.width<1f || bounds.height<1f) error("No measured launch icon")
        val position=IntArray(2);anchor.getLocationInWindow(position)
        val x=(bounds.left-position[0]).roundToInt();val y=(bounds.top-position[1]).roundToInt()
        val width=bounds.width.roundToInt().coerceAtLeast(1);val height=bounds.height.roundToInt().coerceAtLeast(1)
        if(c.transitionStyle==TransitionStyle.UmbraCinematic) ActivityOptions.makeClipRevealAnimation(anchor,x,y,width,height).toBundle()
        else ActivityOptions.makeScaleUpAnimation(anchor,x,y,width,height).toBundle()
    }.getOrElse { ActivityOptions.makeCustomAnimation(context,R.anim.umbra_app_fade_in,R.anim.umbra_app_fade_out).toBundle() }
}
fun startLauncherApp(context: Context,app: LaunchApp,anchor: View,bounds: Rect?,c: Config,motion: MotionPolicy) {
    val component=android.content.ComponentName.unflattenFromString(app.id) ?: throw IllegalArgumentException("Invalid activity")
    val intent=Intent.makeMainActivity(component)
    val options=appLaunchOptions(context,anchor,bounds,c,motion)
    try { context.startActivity(intent,options) }
    catch(_: IllegalArgumentException) {
        val enabled=transitionPlan(c,motion,TransitionCategory.App).enabled
        context.startActivity(intent,ActivityOptions.makeCustomAnimation(context,if(enabled)R.anim.umbra_app_fade_in else 0,if(enabled)R.anim.umbra_app_fade_out else 0).toBundle())
    }
}
