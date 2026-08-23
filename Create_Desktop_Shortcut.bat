@echo off
setlocal
cd /d "%~dp0"

set "ANDALUSIA_APP_DIR=%~dp0"
set "ANDALUSIA_SHORTCUT=%USERPROFILE%\Desktop\Andalusia Work Management.lnk"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$shell = New-Object -ComObject WScript.Shell;" ^
  "$shortcut = $shell.CreateShortcut($env:ANDALUSIA_SHORTCUT);" ^
  "$shortcut.TargetPath = Join-Path $env:ANDALUSIA_APP_DIR 'run.bat';" ^
  "$shortcut.WorkingDirectory = $env:ANDALUSIA_APP_DIR;" ^
  "$shortcut.IconLocation = (Join-Path $env:ANDALUSIA_APP_DIR 'Andalusia_Work_Management.ico') + ',0';" ^
  "$shortcut.Description = 'Andalusia Academy Work Management System';" ^
  "$shortcut.Save();"

if exist "%ANDALUSIA_SHORTCUT%" (
  echo.
  echo Desktop shortcut created successfully:
  echo %ANDALUSIA_SHORTCUT%
) else (
  echo.
  echo The shortcut could not be created.
)

echo.
pause
endlocal
