@echo off
setlocal
set "umbra_install=%~1"
if not defined umbra_install set /p "umbra_install=Original ICARUS folder containing server.py: "
if not defined umbra_install exit /b 1
py -3 "%~dp0apply_host_actions.py" "%umbra_install%"
set "umbra_result=%errorlevel%"
if not "%umbra_result%"=="0" goto finish
py -3 "%~dp0configure_host_actions.py" "%umbra_install%"
set "umbra_result=%errorlevel%"
:finish
pause
exit /b %umbra_result%
