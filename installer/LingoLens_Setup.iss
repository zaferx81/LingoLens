#define MyAppName "LingoLens"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Zafer Software"
#define MyAppExeName "LingoLens.exe"
#define MyAppURL "https://lingolens.app"

[Setup]
AppId={{A9F0E2B8-8D6B-4A9D-9F9A-100010001000}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=C:\LingoLens\release
OutputBaseFilename=LingoLens_Setup_v1.0.0
SetupIconFile=C:\LingoLens\assets\logo\LingoLens.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "Masaüstü kısayolu oluştur"; GroupDescription: "Kısayollar:"; Flags: checkedonce

[Files]
Source: "C:\LingoLens\dist\LingoLens.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\LingoLens\assets\logo\LingoLens.ico"; DestDir: "{app}\assets\logo"; Flags: ignoreversion
Source: "C:\LingoLens\assets\logo\LingoLens_Logo.png"; DestDir: "{app}\assets\logo"; Flags: ignoreversion
Source: "C:\LingoLens\version.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\LingoLens\settings.json"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

[Icons]
Name: "{group}\LingoLens"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\assets\logo\LingoLens.ico"
Name: "{autodesktop}\LingoLens"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\assets\logo\LingoLens.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "LingoLens'i başlat"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\settings.json"