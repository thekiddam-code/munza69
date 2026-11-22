@echo off
setlocal
set "umbra_install=%~1"
if not defined umbra_install set /p "umbra_install=Original ICARUS folder containing server.py: "
if not defined umbra_install exit /b 1
echo Stop the companion normally and close its authoritative browser tab after saving.
echo This installer verifies Phase 4.9 files and backs up the existing sound library before changing code.
where py >nul 2>nul
if errorlevel 1 (
  python "%~dp0apply_bulk_update.py" "%umbra_install%"
) else (
  py -3 "%~dp0apply_bulk_update.py" "%umbra_install%"
)
set "umbra_result=%errorlevel%"
pause
exit /b %umbra_result%
