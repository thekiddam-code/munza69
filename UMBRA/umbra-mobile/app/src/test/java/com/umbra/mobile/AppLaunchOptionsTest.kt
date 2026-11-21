package com.umbra.mobile

import android.content.Context
import android.content.ContextWrapper
import android.content.Intent
import android.os.Bundle
import android.view.View
import androidx.compose.ui.geometry.Rect
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config as RoboConfig

@RunWith(RobolectricTestRunner::class)
@RoboConfig(sdk=[30,34])
class AppLaunchOptionsTest {
    @Test fun activityLaunchUsesMeasuredIconBoundsImmediatelyAndNativeMainIntent() {
        val c=Config();val ctx=RecordingContext(RuntimeEnvironment.getApplication());val anchor=View(ctx)
        val motion=motionPolicy(c,false,false,true,false)
        startLauncherApp(ctx,LaunchApp("example/First","First"),anchor,Rect(17f,31f,65f,79f),c,motion)
        assertEquals(1,ctx.calls)
        assertEquals(Intent.ACTION_MAIN,ctx.intent!!.action)
        assertTrue(ctx.intent!!.hasCategory(Intent.CATEGORY_LAUNCHER))
        assertEquals("example/First",ctx.intent!!.component!!.flattenToString())
        val bundle=ctx.options!!
        assertEquals(2,bundle.getInt("android:activity.animType")) // Android ANIM_SCALE_UP
        assertEquals(17,bundle.getInt("android:activity.animStartX"));assertEquals(31,bundle.getInt("android:activity.animStartY"))
        assertEquals(48,bundle.getInt("android:activity.animWidth"));assertEquals(48,bundle.getInt("android:activity.animHeight"))
    }
    @Test fun nativeModeAndMasterOffFallbackHonorMotionGates() {
        val ctx=RecordingContext(RuntimeEnvironment.getApplication());val view=View(ctx);val c=Config(transitionStyle=TransitionStyle.NativeAndroid)
        assertNull(appLaunchOptions(ctx,view,Rect.Zero,c,motionPolicy(c,false,false,true,false)))
        ctx.rejectFirst=true
        val off=c.copy(master=false)
        startLauncherApp(ctx,LaunchApp("example/First","First"),view,null,off,motionPolicy(off,false,false,true,false))
        assertEquals(2,ctx.calls)
        assertEquals(0,ctx.options!!.getInt("android:activity.animEnterRes"))
        assertEquals(0,ctx.options!!.getInt("android:activity.animExitRes"))
    }
    private class RecordingContext(base: Context): ContextWrapper(base) {
        var calls=0;var rejectFirst=false;var intent: Intent?=null;var options: Bundle?=null
        override fun startActivity(intent: Intent,options: Bundle?) {calls++;if(rejectFirst && calls==1)throw IllegalArgumentException("Unsupported options");this.intent=intent;this.options=options}
    }
}
