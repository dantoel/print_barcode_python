@echo off
chcp 65001 >nul
title MQTT Cloud Printer Service
color 0A

echo ========================================================================
echo MQTT BARCODE PRINTER SERVICE - CLOUD BROKER
echo ========================================================================
echo.
echo Starting service...
echo.

cd /d "%~dp0"

python mqtt_cloud_printer.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================================================
    echo ERROR: Service terminated with error code %ERRORLEVEL%
    echo ========================================================================
    echo.
    echo Possible issues:
    echo   - Python not installed
    echo   - Missing dependencies (paho-mqtt)
    echo   - Configuration file missing
    echo   - Printer DLL not found
    echo.
    echo Press any key to close...
    pause >nul
) else (
    echo.
    echo ========================================================================
    echo Service stopped normally
    echo ========================================================================
    echo.
    timeout /t 3 >nul
)
