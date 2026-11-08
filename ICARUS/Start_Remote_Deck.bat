@echo off
setlocal
cd /d "%~dp0"
title Remote Deck Server
if not exist "server.py" (
  echo ERROR: server.py was not found.
  echo Place this launcher in the same folder as server.py.
  pause
  exit /b 1
)
echo Starting Remote Deck...
where py >nul 2>&1
if %errorlevel%==0 (
  py server.py
) else (
  python server.py
)
echo.
echo Remote Deck server has stopped.
pause
