@echo off
setlocal
cd /d "%~dp0"
if defined JAVA_HOME goto check_java_home
where java >nul 2>nul
if errorlevel 1 (
  echo ERROR: Install JDK 17 or 21 and set JAVA_HOME or add Java to PATH.
  exit /b 1
)
goto build
:check_java_home
if not exist "%JAVA_HOME%\bin\java.exe" (
  echo ERROR: JAVA_HOME must point to a valid JDK 17 or 21 installation.
  exit /b 1
)
:build
call gradlew.bat --no-daemon :app:testDebugUnitTest :app:lintDebug :app:assembleDebug
if errorlevel 1 (
  echo BUILD FAILED. Check Android SDK setup and the Gradle error above.
  exit /b 1
)
echo APK: %CD%\app\build\outputs\apk\debug\app-debug.apk
endlocal
