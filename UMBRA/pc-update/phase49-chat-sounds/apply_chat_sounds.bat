@echo off
setlocal
set /p "ICARUS_TARGET=Original ICARUS folder containing server.py: "
py -3 "%~dp0apply_chat_sounds.py" "%ICARUS_TARGET%"
if errorlevel 1 goto failed
echo Restart the same companion normally.
pause
exit /b 0
:failed
echo Update stopped. Read the error above; do not replace your installation.
pause
exit /b 1
