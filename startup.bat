@echo off

where pwsh >nul 2>nul
if %ERRORLEVEL%==0 (
    start "" pwsh -NoExit
) else (
    start "" powershell -NoExit
)