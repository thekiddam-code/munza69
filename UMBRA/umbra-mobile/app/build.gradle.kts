plugins {
    id("org.jetbrains.kotlin.plugin.serialization")
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}
android {
    namespace = "com.umbra.mobile"
    compileSdk = 35
    buildToolsVersion = "35.0.0"
    defaultConfig { applicationId = "com.umbra.mobile"; minSdk = 29; targetSdk = 35; versionCode = 7; versionName = "3.1"; testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner" }
    buildFeatures { compose = true }
    testOptions { unitTests.isIncludeAndroidResources = true }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
    kotlinOptions { jvmTarget = "17" }
    buildTypes { release { isMinifyEnabled = false } }
    lint { abortOnError = true }
}
dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.12.01"))
    implementation("androidx.activity:activity-compose:1.9.3")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.7")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.7")
    implementation("androidx.datastore:datastore-preferences:1.1.1")
    implementation("androidx.core:core-ktx:1.15.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.3")
    debugImplementation("androidx.compose.ui:ui-tooling")
    androidTestImplementation(platform("androidx.compose:compose-bom:2024.12.01"))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    androidTestImplementation("androidx.test.ext:junit:1.2.1")
    androidTestImplementation("androidx.test:runner:1.6.2")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.robolectric:robolectric:4.14.1")
    testImplementation("androidx.compose.ui:ui-test-junit4")
    testImplementation("androidx.test:core-ktx:1.6.1")
    testImplementation("androidx.test.espresso:espresso-core:3.5.0")
    testImplementation("com.squareup.okhttp3:mockwebserver:4.12.0")
}

// Honor a developer's standard JVM proxy configuration for Robolectric SDK resolution.
tasks.withType<Test>().configureEach {
    listOf("http.proxyHost","http.proxyPort","https.proxyHost","https.proxyPort").forEach { key ->
        System.getProperty(key)?.let { systemProperty(key,it) }
    }
    systemProperty("robolectric.dependency.repo.url","https://repo.maven.apache.org/maven2")
    maxHeapSize = "1536m"
    systemProperty("umbra.captureDir",layout.buildDirectory.dir("reports/ui").get().asFile.absolutePath)
}
