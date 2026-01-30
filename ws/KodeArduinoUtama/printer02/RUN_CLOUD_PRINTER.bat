@echo off
REM =====================================================
REM MQTT Cloud Barcode Printer Service
REM =====================================================

setlocal enabledelayedexpansion

title MQTT Cloud Printer Service

cd /d "%~dp0"

cls

echo.
echo =====================================================
echo MQTT CLOUD BARCODE PRINTER SERVICE
echo =====================================================
echo Using HiveMQ Cloud Broker (FREE)
echo =====================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    pause
    exit /b 1
)

REM Check paho-mqtt
python -m pip show paho-mqtt >nul 2>&1
if errorlevel 1 (
    echo [*] Installing paho-mqtt...
    python -m pip install paho-mqtt
    echo.
)

REM Check config file
if not exist "mqtt_config.ini" (
    echo ERROR: mqtt_config.ini not found!
    pause
    exit /b 1
)

echo [*] Configuration:
echo     Broker: broker.hivemq.com:1883
echo     Topic: printer/barcode/print
echo.
echo =====================================================
echo Starting Service...
echo =====================================================
echo.

REM Run service
python mqtt_cloud_printer.py

echo.
pause

exit /b 0
