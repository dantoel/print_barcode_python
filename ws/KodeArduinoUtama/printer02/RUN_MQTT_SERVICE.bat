@echo off
REM =====================================================
REM MQTT Barcode Printer Service V2 - Launcher
REM =====================================================

setlocal enabledelayedexpansion

title MQTT Barcode Printer Service V2

cd /d "%~dp0"

cls

echo.
echo =====================================================
echo MQTT BARCODE PRINTER SERVICE V2
echo =====================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    echo Install Python from: https://www.python.org
    echo Make sure to check "Add Python to PATH"
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
    echo.
    pause
    exit /b 1
)

REM Display config
echo [*] Loading configuration from mqtt_config.ini
python -c "import configparser; c=configparser.ConfigParser(); c.read('mqtt_config.ini'); print('    Broker: %s:%s' % (c.get('MQTT','BROKER_ADDRESS'), c.get('MQTT','BROKER_PORT'))); print('    Topic: %s' % c.get('MQTT','TOPIC_BARCODE_INPUT'))"

echo.
echo =====================================================
echo Starting MQTT Printer Service...
echo =====================================================
echo.

REM Run service
python mqtt_printer_service.py

echo.
pause

exit /b 0
