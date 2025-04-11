@echo off
setlocal enabledelayedexpansion

REM Получаем имя текущего пользователя
set "USERNAME=%USERNAME%"
set "TARGET_DIR=%APPDATA%\SystemLogs"

REM Удаляем ключ автозагрузки
echo [+] Удаление ключа из реестра...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SystemLogs" /f

REM Удаляем файлы из папки SystemLogs
echo [+] Удаление файлов из директории: %TARGET_DIR%
del /F /Q "%TARGET_DIR%\winupdater.exe"
del /F /Q "%TARGET_DIR%\config.py"
del /F /Q "%TARGET_DIR%\log.txt"

REM Удаляем папку (если она пуста)
echo [+] Удаление пустой директории: %TARGET_DIR%
rmdir "%TARGET_DIR%"

echo [✓] Удаление завершено.
pause
