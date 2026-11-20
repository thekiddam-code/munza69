@echo off
cd /d "%~dp0"
echo Stop UMBRA before backing up. No original sound files will be removed.
py sound_backup.py --root "%~dp0soundboard_data" --require-existing
if errorlevel 1 (echo Backup or library audit needs attention. Do not replace the existing installation.) else (echo Backup verification completed. Keep soundboard_data and the backup ZIP.)
pause
