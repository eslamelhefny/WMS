@echo off
setlocal
set "ANDALUSIA_SHORTCUT=%USERPROFILE%\Desktop\Andalusia Task Planner.lnk"

if exist "%ANDALUSIA_SHORTCUT%" (
  del "%ANDALUSIA_SHORTCUT%"
  echo Desktop shortcut removed.
) else (
  echo No Andalusia Task Planner shortcut was found on the Desktop.
)

echo.
pause
endlocal
