@echo off
echo ========================================
echo Camera File Classifier - Build Installer
echo ========================================
echo.

echo Step 1: Building executable with PyInstaller...
python -m PyInstaller --clean CameraFileClassifier.spec
if errorlevel 1 (
    echo Error: PyInstaller build failed!
    pause
    exit /b 1
)
echo Executable built successfully!
echo.

echo Step 2: Checking for Inno Setup...
set INNO_SETUP="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %INNO_SETUP% (
    echo.
    echo WARNING: Inno Setup not found!
    echo Please install Inno Setup 6 from: https://jrsoftware.org/isdl.php
    echo.
    echo After installation, run this script again to create the installer.
    pause
    exit /b 1
)
echo Inno Setup found!
echo.

echo Step 3: Building installer with Inno Setup...
%INNO_SETUP% installer.iss
if errorlevel 1 (
    echo Error: Inno Setup build failed!
    pause
    exit /b 1
)
echo.

echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo The installer is located at:
echo installer_output\CameraFileClassifier_Setup_v1.0.0.exe
echo.
pause
