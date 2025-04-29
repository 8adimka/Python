@echo off
setlocal enabledelayedexpansion

set "TARGET_DIR=%APPDATA%\SystemLogs"
set "EXE_PATH=%TARGET_DIR%\winupdater.exe"
set "PROC_NAME=winupdater.exe"

echo [+] Завершение процесса %PROC_NAME%...
taskkill /F /IM %PROC_NAME% >nul 2>&1

echo [+] Удаление из автозагрузки...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SystemLogs" /f >nul 2>&1

echo [+] Удаление файлов...
del /F /Q "%EXE_PATH%" >nul 2>&1
del /F /Q "%TARGET_DIR%\app.log" >nul 2>&1
del /F /Q "%TARGET_DIR%\keys.log" >nul 2>&1

echo [+] Удаление директории...
rmdir "%TARGET_DIR%" >nul 2>&1

echo [✓] Удаление завершено.
pause
exit /b
