; Inno Setup Script for TextMergeApp
; Build exe first using build_exe.ps1

#define MyAppName "Text Merge Application"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Text Merge Team"
#define MyAppExeName "TextMergeApp.exe"
#define MyAppSourceDir "dist\\TextMergeApp"

[Setup]
AppId={{8C0D2528-2D66-4D39-BD95-E566A2F1AA91}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\TextMergeApp
DefaultGroupName=Text Merge Application
OutputDir=dist
OutputBaseFilename=TextMergeInstaller
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Files]
Source: "{#MyAppSourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
