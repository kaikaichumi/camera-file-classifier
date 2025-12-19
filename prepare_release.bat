@echo off
echo ========================================
echo Camera File Classifier - Prepare Release
echo ========================================
echo.

REM 清理旧的发布文件
echo Cleaning old releases...
if exist releases rmdir /s /q releases
mkdir releases
echo.

REM 1. 打包便携版
echo Step 1: Building portable version...
python -m PyInstaller --clean CameraFileClassifier.spec
if errorlevel 1 (
    echo Error: Failed to build portable version!
    pause
    exit /b 1
)
echo.

REM 2. 压缩便携版
echo Step 2: Compressing portable version...
cd dist
powershell Compress-Archive -Path CameraFileClassifier -DestinationPath ..\releases\CameraFileClassifier_Portable_v1.0.0.zip -Force
cd ..
echo Portable version created: releases\CameraFileClassifier_Portable_v1.0.0.zip
echo.

REM 3. 生成安装程序
echo Step 3: Building installer...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
if errorlevel 1 (
    echo Error: Failed to build installer!
    pause
    exit /b 1
)
echo.

REM 4. 复制安装程序到releases文件夹
echo Step 4: Copying installer to releases...
copy installer_output\CameraFileClassifier_Setup_v1.0.0.exe releases\
echo.

echo ========================================
echo Release preparation completed!
echo ========================================
echo.
echo Created files:
echo 1. releases\CameraFileClassifier_Portable_v1.0.0.zip (Portable version)
echo 2. releases\CameraFileClassifier_Setup_v1.0.0.exe (Installer)
echo.
echo You can now upload these files to GitHub Releases.
echo.
pause
