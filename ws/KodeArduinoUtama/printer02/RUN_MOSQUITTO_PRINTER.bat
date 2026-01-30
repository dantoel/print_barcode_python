@echo off
REM =====================================================
REM MQTT Mosquitto Barcode Printer Service
REM =====================================================

setlocal enabledelayedexpansion

title MQTT Mosquitto Barcode Printer Service

cd /d "%~dp0"

cls

echo.
echo =====================================================
echo MQTT MOSQUITTO BARCODE PRINTER SERVICE
echo =====================================================
echo Using Mosquitto Broker (Lokal)
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
if not exist "mosquitto_config.ini" (
    echo ERROR: mosquitto_config.ini not found!
    pause
    exit /b 1
)

echo [*] Configuration:
echo     Config File: mosquitto_config.ini
echo.

REM Check if Mosquitto service is running
echo [*] Checking Mosquitto service...
sc query mosquitto >nul 2>&1
if errorlevel 1 (
    echo WARNING: Mosquitto service not found!
    echo.
    echo Please install Mosquitto first:
    echo 1. Download from https://mosquitto.org/download/
    echo 2. Install as Windows Service
    echo.
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

echo.
echo =====================================================
echo Starting Service...
echo =====================================================
echo.

REM Change config file reference for mosquitto version
REM We need to update the script to use mosquitto_config.ini instead of mqtt_config.ini

REM Run service with custom config
python -c "import configparser; c=configparser.ConfigParser(); c.read('mosquitto_config.ini'); import sys; sys.path.insert(0, '.'); exec(open('mqtt_cloud_printer.py').read().replace('mqtt_config.ini', 'mosquitto_config.ini'))"

if %errorlevel% neq 0 (
    REM If above fails, just run with default (will use mqtt_config.ini)
    python mqtt_cloud_printer.py
)

echo.
pause

exit /b 0
