@echo off
echo Clearing Windows icon cache...

taskkill /f /im explorer.exe

timeout /t 2 /nobreak >nul

cd /d %userprofile%\AppData\Local
if exist IconCache.db del /f /q IconCache.db
if exist Microsoft\Windows\Explorer\iconcache*.db del /f /q Microsoft\Windows\Explorer\iconcache*.db

echo Icon cache cleared. Restarting Explorer...
start explorer.exe

echo Done! Please check if the icon has updated.
pause
