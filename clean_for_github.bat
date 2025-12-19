@echo off
echo ========================================
echo Cleaning temporary files for GitHub
echo ========================================
echo.

echo Removing temporary folders...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist output rmdir /s /q output
if exist test_dist rmdir /s /q test_dist
if exist installer_output rmdir /s /q installer_output
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo Removing temporary files...
if exist config.json del /q config.json
if exist icon.jpg del /q icon.jpg
if exist TestApp.spec del /q TestApp.spec
if exist build_exe.py del /q build_exe.py
if exist PLAN.md del /q PLAN.md

echo.
echo Removing Python cache files...
for /r %%i in (__pycache__) do @if exist "%%i" rmdir /s /q "%%i"
for /r %%i in (*.pyc) do @if exist "%%i" del /q "%%i"
for /r %%i in (*.pyo) do @if exist "%%i" del /q "%%i"

echo.
echo ========================================
echo Cleanup completed!
echo ========================================
echo.
echo The following folders and files will be uploaded to GitHub:
echo - Source code (main.py, core/, ui/)
echo - Documentation (README.md, LICENSE, etc.)
echo - Build scripts (CameraFileClassifier.spec, installer.iss)
echo - Icon files (icon.png, icon.ico)
echo - Requirements (requirements.txt)
echo.
echo The releases/ folder contains your distributable files.
echo These should be uploaded separately in GitHub Releases.
echo.
pause
