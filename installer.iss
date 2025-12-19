; Inno Setup Script for Camera File Classifier
; 相機檔案分類工具安裝程式

#define MyAppName "Camera File Classifier"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Your Company"
#define MyAppExeName "CameraFileClassifier.exe"
#define MyAppAssocName MyAppName
#define MyAppAssocExt ""
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
; 應用程式基本資訊
AppId={{8B5F2D3A-9C4E-4F1B-8D6A-2E7F9B1C3A5D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
; 安裝程式圖標
SetupIconFile=icon.ico
; 輸出設定
OutputDir=installer_output
OutputBaseFilename=CameraFileClassifier_Setup_v{#MyAppVersion}
; 壓縮設定
Compression=lzma2/max
SolidCompression=yes
; Windows 版本要求
MinVersion=6.1sp1
; 架構
ArchitecturesInstallIn64BitMode=x64compatible
; 許可協議（如果有的話）
; LicenseFile=LICENSE.txt
; 安裝資訊
InfoBeforeFile=
InfoAfterFile=
; 安裝程式外觀
WizardStyle=modern
DisableWelcomePage=no
; 卸載圖標
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; 主程式和所有依賴文件
Source: "dist\CameraFileClassifier\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\CameraFileClassifier\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs
; 注意：如果有其他資源文件，在這裡添加

[Icons]
; 開始菜單快捷方式
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
; 桌面快捷方式
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
; 快速啟動欄快捷方式
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; 安裝完成後詢問是否立即運行
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; 卸載時刪除的額外文件或文件夾
Type: filesandordirs; Name: "{app}"

[Code]
// 可以在這裡添加自定義的 Pascal Script 代碼
// 例如檢查系統需求、卸載舊版本等
