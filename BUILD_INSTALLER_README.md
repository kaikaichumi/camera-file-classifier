# 如何建立安裝程式

## 準備工作

### 1. 安裝 Inno Setup

1. 下載 Inno Setup 6：https://jrsoftware.org/isdl.php
2. 選擇 "Download Inno Setup 6.x.x" (最新版本)
3. 執行安裝程式，按照默認設定安裝

### 2. 確認 Python 環境

確保你已經安裝了以下 Python 套件：
```bash
pip install pyinstaller pillow
```

## 建立安裝程式

### 方法一：使用自動化腳本（推薦）

1. 雙擊運行 `build_installer.bat`
2. 等待腳本完成
3. 安裝程式會生成在 `installer_output` 資料夾中

### 方法二：手動建立

1. 先打包程式：
   ```bash
   python -m PyInstaller --clean CameraFileClassifier.spec
   ```

2. 使用 Inno Setup 編譯安裝腳本：
   - 打開 Inno Setup Compiler
   - 開啟 `installer.iss` 文件
   - 點擊 Build -> Compile（或按 Ctrl+F9）
   - 等待編譯完成

3. 安裝程式會生成在 `installer_output` 資料夾中

## 安裝程式功能

生成的安裝程式包含以下功能：

- ✅ 自動安裝到 Program Files
- ✅ 在開始菜單創建快捷方式
- ✅ 可選擇在桌面創建快捷方式
- ✅ 完整的卸載功能
- ✅ 支持繁體中文和英文界面
- ✅ 現代化的安裝向導界面
- ✅ 安裝完成後可選擇立即運行程式

## 自定義安裝程式

如果需要修改安裝程式的設定，請編輯 `installer.iss` 文件：

- **應用程式版本**：修改 `MyAppVersion`
- **發布者名稱**：修改 `MyAppPublisher`
- **安裝圖標**：修改 `SetupIconFile`
- **默認安裝路徑**：修改 `DefaultDirName`

## 分發安裝程式

將生成的 `CameraFileClassifier_Setup_v1.0.0.exe` 分發給用戶即可。

用戶只需：
1. 下載安裝程式
2. 雙擊執行
3. 按照安裝向導完成安裝
4. 從開始菜單或桌面快捷方式啟動程式

## 注意事項

- 首次運行時可能會被 Windows Defender SmartScreen 攔截，這是正常現象
- 如果需要代碼簽名以避免警告，需要購買代碼簽名證書
- 確保 `dist\CameraFileClassifier\` 資料夾包含完整的程式文件
