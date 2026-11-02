[Setup]
AppName=Proposta Solar
AppVersion=1.0
DefaultDirName={autopf}\PropostaSolar
DefaultGroupName=Proposta Solar
OutputBaseFilename=PropostaSolar_Setup
OutputDir=..
Compression=lzma
SolidCompression=yes
[Files]
Source: "..\dist\PropostaSolar\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs
[Icons]
Name: "{autodesktop}\Proposta Solar"; Filename: "{app}\PropostaSolar.exe"
Name: "{group}\Proposta Solar"; Filename: "{app}\PropostaSolar.exe"
[Run]
Filename: "{app}\PropostaSolar.exe"; Description: "Abrir Proposta Solar"; Flags: nowait postinstall skipifsilent
