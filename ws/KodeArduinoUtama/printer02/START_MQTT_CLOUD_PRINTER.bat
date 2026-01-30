@echo off
chcp 65001 >nul
title MQTT Cloud Printer - AUTO START
color 0B

echo ========================================================================
echo MQTT CLOUD PRINTER - AUTO RESTART SERVICE
echo ========================================================================
echo.
echo This script will automatically restart the service if it crashes
echo Press Ctrl+C to stop completely
echo.
echo ========================================================================
echo.

cd /d "%~dp0"

:restart
echo [%date% %time%] Starting MQTT Cloud Printer Service...
echo.

python mqtt_cloud_printer.py

echo.
echo [%date% %time%] Service stopped. Exit code: %ERRORLEVEL%
echo.

if %ERRORLEVEL% EQU 0 (
    echo Service stopped normally. Exiting...
    timeout /t 3 >nul
    exit /b 0
) else (
    echo Service crashed! Restarting in 5 seconds...
    echo Press Ctrl+C to cancel...
    timeout /t 5
    echo.
    echo ========================================================================
    echo.
    goto restart
)
