; Custom Crosshair - установщик (Inno Setup)
; Сборка: "C:\Program Files\Inno Setup 7\ISCC.exe" installer.iss

#define MyAppName "Custom Crosshair"
#define MyAppVersion "1.0.0"
#define MyAppExeName "CustomCrosshair.exe"
#define MyAppPublisher "Custom Crosshair"
#define MyAppId "7C0B1E52-4B1F-4C6F-9A1E-3F2D5E6A7B8C"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\CustomCrosshair
DefaultGroupName=Custom Crosshair
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=installer-output
OutputBaseFilename=SetupCustomCrosshair
SetupIconFile=app.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName=Custom Crosshair
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "app.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Custom Crosshair"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app.ico"
Name: "{group}\Uninstall Custom Crosshair"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Custom Crosshair"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,Custom Crosshair}"; Flags: nowait postinstall skipifsilent
