package com.umbra.mobile

import android.Manifest
import android.content.pm.PackageManager
import android.location.LocationManager
import android.os.CancellationSignal
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.compose.*
import androidx.lifecycle.repeatOnLifecycle
import kotlinx.coroutines.*
import kotlin.coroutines.resume
import kotlin.math.round
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter

val LocalWeatherSettings=staticCompositionLocalOf<()->Unit>{{}}
private fun weatherTime(time: Long,zone: String,pattern: String)=runCatching {Instant.ofEpochSecond(time).atZone(ZoneId.of(zone)).format(DateTimeFormatter.ofPattern(pattern))}.getOrDefault("Unavailable")
@Composable private fun observeWeather(c: Config,model: LauncherModel,visible: Boolean): WeatherState {
    val lifecycle=LocalLifecycleOwner.current.lifecycle
    val state by model.weather.state.collectAsStateWithLifecycle()
    LaunchedEffect(lifecycle,visible,c.weatherLatitude,c.weatherLongitude,c.weatherFahrenheit) {if(visible)lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED){model.weather.refresh(c)}}
    return if(state.snapshot?.key==weatherKey(c) || state.snapshot==null)state else WeatherState(message="Updating selected location…")
}
@Composable fun WeatherWidgetCompact(c: Config,model: LauncherModel,visible: Boolean) {
    val state=observeWeather(c,model,visible);val weather=state.snapshot
    Readout(c.weatherPlace.ifEmpty {"WEATHER"},MaterialTheme.colorScheme.primary)
    if(weather!=null){Text(weather.temperature?.let {"${round(it).toInt()}°${if(c.weatherFahrenheit)"F" else "C"}"} ?: "Unavailable",style=MaterialTheme.typography.headlineLarge);Text(weatherCondition(weather.code));Text("Open-Meteo · ${weatherTime(weather.fetchedAt/1000,weather.timezone,"MMM d HH:mm")}",style=MaterialTheme.typography.bodySmall)}
    else {Text(state.message,style=MaterialTheme.typography.bodySmall);TextButton(onClick=LocalWeatherSettings.current){Text("Choose location")}}
}
@Composable fun WeatherDetails(c: Config,model: LauncherModel) {
    val state=observeWeather(c,model,true);val scope=rememberCoroutineScope();val weather=state.snapshot
    var refreshJob by remember {mutableStateOf<Job?>(null)}
    LifecycleStartEffect(Unit){onStopOrDispose {refreshJob?.cancel()}}
    Column(verticalArrangement=Arrangement.spacedBy(10.dp)) {
        Text(c.weatherPlace.ifEmpty {"Select a weather location"},style=MaterialTheme.typography.titleLarge)
        Text(state.message)
        Row {TextButton(onClick=LocalWeatherSettings.current){Text("Location / units")};TextButton(onClick={if(refreshJob?.isActive!=true)refreshJob=scope.launch {model.weather.refresh(c,true)}},enabled=!state.refreshing && c.weatherLatitude!=null){Text("Refresh weather")}}
        if(weather!=null) {
            Text("${weather.temperature?.toString() ?: "Unavailable"}°${if(c.weatherFahrenheit)"F" else "C"} · ${weatherCondition(weather.code)}")
            weather.days.firstOrNull()?.let {Text("High ${it.high ?: "Unavailable"}° · Low ${it.low ?: "Unavailable"}°")}
            Text("Last updated ${weatherTime(weather.fetchedAt/1000,weather.timezone,"MMM d, HH:mm")}",style=MaterialTheme.typography.bodySmall)
            Readout("HOURLY FORECAST",MaterialTheme.colorScheme.primary)
            weather.hours.forEach {Text("${weatherTime(it.time,weather.timezone,"EEE HH:mm")} · ${it.temperature ?: "Unavailable"}° · ${weatherCondition(it.code)}",style=MaterialTheme.typography.bodySmall)}
            Readout("MULTI-DAY FORECAST",MaterialTheme.colorScheme.primary)
            weather.days.forEach {Text("${weatherTime(it.time,weather.timezone,"EEE, MMM d")} · ${it.low ?: "Unavailable"}° / ${it.high ?: "Unavailable"}° · ${weatherCondition(it.code)}",style=MaterialTheme.typography.bodySmall)}
        }
        Text("Weather data by Open-Meteo (CC BY 4.0). Cache lifetime 30 minutes; offline data is dated and retained up to 7 days. No background weather polling.",style=MaterialTheme.typography.bodySmall)
    }
}
@Composable fun WeatherSettings(c: Config,model: LauncherModel) {
    val context=LocalContext.current;val scope=rememberCoroutineScope()
    var query by remember {mutableStateOf("")};var results by remember {mutableStateOf<List<WeatherPlace>>(emptyList())};var message by remember {mutableStateOf("")};var work by remember {mutableStateOf<Job?>(null)}
    LifecycleStartEffect(Unit){onStopOrDispose {work?.cancel()}}
    fun approximate() {
        work?.cancel();work=scope.launch {
            val location=withTimeoutOrNull(12000){suspendCancellableCoroutine<android.location.Location?> {continuation->
                val manager=context.getSystemService(LocationManager::class.java)
                if(LocationManager.NETWORK_PROVIDER !in manager.getProviders(true)){continuation.resume(null);return@suspendCancellableCoroutine}
                if(android.os.Build.VERSION.SDK_INT>=30) {
                    val signal=CancellationSignal();continuation.invokeOnCancellation{signal.cancel()}
                    try {manager.getCurrentLocation(LocationManager.NETWORK_PROVIDER,signal,context.mainExecutor){if(continuation.isActive)continuation.resume(it)}}catch(_:RuntimeException){if(continuation.isActive)continuation.resume(null)}
                } else {
                    val listener=object: android.location.LocationListener {
                        override fun onLocationChanged(location: android.location.Location){manager.removeUpdates(this);if(continuation.isActive)continuation.resume(location)}
                        override fun onProviderDisabled(provider: String){};override fun onProviderEnabled(provider: String){};@Deprecated("Legacy Android callback")override fun onStatusChanged(provider: String?,status: Int,extras: android.os.Bundle?){}
                    }
                    continuation.invokeOnCancellation{manager.removeUpdates(listener)}
                    @Suppress("DEPRECATION")
                    try {manager.requestSingleUpdate(LocationManager.NETWORK_PROVIDER,listener,android.os.Looper.getMainLooper())}catch(_:RuntimeException){if(continuation.isActive)continuation.resume(null)}
                }
            }}
            if(location==null)message="Approximate location unavailable. Enable Android location or search for a city."
            else {val lat=round(location.latitude*100)/100;val lon=round(location.longitude*100)/100;model.change {it.copy(weatherPlace="Approximate location",weatherLatitude=lat,weatherLongitude=lon)};message="Approximate location selected; coordinates are sent only to the weather provider."}
        }
    }
    val permission=rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()){granted->if(granted)approximate() else message="Location permission not granted. Manual city selection remains available."}
    Text("Provider: Open-Meteo",style=MaterialTheme.typography.titleMedium)
    Text("Chosen location: ${c.weatherPlace.ifEmpty {"None"}}")
    Text("City search and forecast requests go to Open-Meteo. Optional Android approximate location is requested only when you choose it. No background location access.",style=MaterialTheme.typography.bodySmall)
    OutlinedTextField(query,{query=it.take(100)},label={Text("Search city")},singleLine=true,modifier=Modifier.fillMaxWidth())
    Button(onClick={work?.cancel();work=scope.launch {message="Searching…";try{results=model.weather.client.search(query);message=if(results.isEmpty())"No matching locations." else "Choose a location."}catch(e:CancellationException){throw e}catch(_:Exception){message="City search unavailable. Try again later."}}},enabled=query.trim().length>=2,shape=Chamfer){Text("Search locations")}
    results.forEach {place->TextButton(onClick={model.change {it.copy(weatherPlace=place.name,weatherLatitude=place.latitude,weatherLongitude=place.longitude)};results=emptyList();message="Location saved."}){Text(place.name)}}
    TextButton(onClick={if(ContextCompat.checkSelfPermission(context,Manifest.permission.ACCESS_COARSE_LOCATION)==PackageManager.PERMISSION_GRANTED)approximate() else permission.launch(Manifest.permission.ACCESS_COARSE_LOCATION)}){Text("Use approximate Android location")}
    Toggle("Fahrenheit (Celsius when off)",c.weatherFahrenheit){v->model.change {it.copy(weatherFahrenheit=v)}}
    TextButton(onClick={model.change {it.copy(weatherPlace="",weatherLatitude=null,weatherLongitude=null)};message="Weather location cleared."}){Text("Clear weather location")}
    if(message.isNotEmpty())Text(message,style=MaterialTheme.typography.bodySmall)
}
