[Setup]
AppName=Proposta Solar
AppVersion=1.0
DefaultDirName={autopf}\PropostaSolar
DefaultGroupName=Proposta Solar
OutputBaseFilename=PropostaSolar_Setup
OutputDir=..
SetupIconFile=icone.ico
UninstallDisplayIcon={app}\PropostaSolar.exe
Compression=lzma
SolidCompression=yes
[Files]
Source: "..\dist\PropostaSolar\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs
[Icons]
Name: "{autodesktop}\Proposta Solar"; Filename: "{app}\PropostaSolar.exe"
Name: "{group}\Proposta Solar"; Filename: "{app}\PropostaSolar.exe"
[Run]
Filename: "{app}\PropostaSolar.exe"; Description: "Abrir Proposta Solar"; Flags: nowait postinstall skipifsilent

[Code]
procedure MataPrograma();
var R: Integer;
begin
  Exec('taskkill.exe', '/F /T /IM PropostaSolar.exe', '', SW_HIDE, ewWaitUntilTerminated, R);
  Sleep(1500);
end;

function InitializeSetup(): Boolean;
begin
  MataPrograma();
  Result := True;
end;

function InitializeUninstall(): Boolean;
begin
  MataPrograma();
  Result := True;
end;
