# GitHub 上傳指南

## 📋 準備清單

在上傳到 GitHub 之前，請確認以下文件已準備好：

### ✅ 必要文件
- [x] `README.md` - 英文說明文件
- [x] `README_ZH.md` - 繁體中文說明文件
- [x] `LICENSE` - 授權條款 (CC BY-NC 4.0)
- [x] `.gitignore` - Git 忽略文件
- [x] `requirements.txt` - Python 依賴
- [x] `icon.png` - 應用程式圖標
- [x] 源代碼文件（`main.py`, `core/`, `ui/` 等）

### ✅ 發布文件
- [x] `releases/CameraFileClassifier_Portable_v1.0.0.zip` (13 MB)
- [x] `releases/CameraFileClassifier_Setup_v1.0.0.exe` (9.7 MB)
- [x] `RELEASE_NOTES.md` - 發布說明

## 🚀 上傳步驟

### 步驟 1：初始化 Git 倉庫

```bash
cd D:\code\claude_test\camera_raw
git init
git add .
git commit -m "Initial commit: Camera File Classifier v1.0.0"
```

### 步驟 2：在 GitHub 創建新倉庫

1. 登入 GitHub
2. 點擊右上角的 `+` → `New repository`
3. 填寫以下資訊：
   - **Repository name**: `camera-file-classifier`
   - **Description**: `相機檔案分類工具 - 自動將 RAW、JPG、HEIC、影片檔案分類到不同資料夾`
   - **Visibility**: `Public`（公開）或 `Private`（私密）
   - ❌ **不要**勾選 "Initialize this repository with a README"
4. 點擊 `Create repository`

### 步驟 3：連接遠程倉庫

```bash
git remote add origin https://github.com/YOUR_USERNAME/camera-file-classifier.git
git branch -M main
git push -u origin main
```

**注意**：將 `YOUR_USERNAME` 替換為你的 GitHub 用戶名

### 步驟 4：創建 Release（發布版本）

#### 方法一：使用 GitHub 網頁界面（推薦）

1. 前往你的倉庫頁面
2. 點擊右側的 `Releases` → `Create a new release`
3. 填寫以下資訊：
   - **Tag**: `v1.0.0`
   - **Release title**: `Camera File Classifier v1.0.0`
   - **Description**: 複製 `RELEASE_NOTES.md` 的內容
4. **上傳文件**（Attach binaries）：
   - 拖放或選擇 `releases/CameraFileClassifier_Setup_v1.0.0.exe`
   - 拖放或選擇 `releases/CameraFileClassifier_Portable_v1.0.0.zip`
5. 勾選 `Set as the latest release`
6. 點擊 `Publish release`

#### 方法二：使用 GitHub CLI（進階）

```bash
# 安裝 GitHub CLI: https://cli.github.com/

# 登入
gh auth login

# 創建 Release
gh release create v1.0.0 \
  releases/CameraFileClassifier_Setup_v1.0.0.exe \
  releases/CameraFileClassifier_Portable_v1.0.0.zip \
  --title "Camera File Classifier v1.0.0" \
  --notes-file RELEASE_NOTES.md
```

## 📝 更新 README 中的鏈接

發布後，請更新以下文件中的佔位符：

### 在 `README.md` 和 `README_ZH.md` 中：

將所有 `YOUR_USERNAME` 替換為你的 GitHub 用戶名：

```markdown
<!-- 之前 -->
https://github.com/YOUR_USERNAME/camera-file-classifier/releases/latest

<!-- 之後 -->
https://github.com/your-actual-username/camera-file-classifier/releases/latest
```

然後提交更新：

```bash
git add README.md README_ZH.md
git commit -m "Update GitHub links with actual username"
git push
```

## 🏷️ 添加 Topics（標籤）

在 GitHub 倉庫頁面：

1. 點擊右側的 ⚙️ (Settings) 旁邊的 `About` 區域
2. 點擊 ⚙️ 圖標
3. 在 `Topics` 欄位添加以下標籤：
   - `camera`
   - `file-organizer`
   - `raw-photos`
   - `photo-management`
   - `tkinter`
   - `python`
   - `windows`
   - `chinese`
4. 點擊 `Save changes`

## 📊 添加 Badges（徽章）

可以在 README.md 頂部添加以下徽章：

```markdown
![GitHub release](https://img.shields.io/github/v/release/YOUR_USERNAME/camera-file-classifier)
![GitHub downloads](https://img.shields.io/github/downloads/YOUR_USERNAME/camera-file-classifier/total)
![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
```

## 🔄 未來更新流程

當需要發布新版本時：

1. **更新版本號**：
   - 在 `installer.iss` 中更新 `MyAppVersion`
   - 在 `prepare_release.bat` 中更新版本號

2. **重新打包**：
   ```bash
   prepare_release.bat
   ```

3. **提交更改**：
   ```bash
   git add .
   git commit -m "Release v1.1.0: [更新說明]"
   git push
   ```

4. **創建新 Release**：
   - 使用新的標籤（如 `v1.1.0`）
   - 上傳新的安裝文件
   - 更新發布說明

## ✅ 完成檢查清單

上傳完成後，請確認：

- [ ] 倉庫可以正常訪問
- [ ] README 顯示正確
- [ ] 圖標圖片正常顯示
- [ ] Release 頁面有兩個下載文件
- [ ] 下載鏈接可以正常工作
- [ ] LICENSE 文件存在
- [ ] Topics 標籤已添加

## 🎉 完成！

恭喜！你的專案已經成功上傳到 GitHub。

現在可以：
- 分享倉庫鏈接給其他人
- 在社群媒體宣傳
- 收集用戶反饋
- 持續改進專案

## 🐛 常見問題

### Q: 文件太大無法上傳？
A: GitHub Release 單檔最大 2GB，你的文件都在限制內。

### Q: 如何刪除錯誤的 Release？
A: 在 Release 頁面，點擊 Release 右上角的 🗑️ 圖標。

### Q: 如何修改 Release 說明？
A: 在 Release 頁面，點擊 `Edit release` 按鈕。

## 📧 需要幫助？

如果遇到問題：
- 查看 [GitHub 官方文檔](https://docs.github.com/)
- 搜尋 [GitHub Community](https://github.community/)
- 或在專案中創建 Issue 詢問

---

**祝你的專案成功！** 🚀
