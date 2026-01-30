@echo off
REM =====================================================
REM Script untuk menjalankan Node-RED Printer
REM =====================================================
REM Double-click file ini untuk mulai
REM =====================================================

setlocal enabledelayedexpansion

title NODE-RED BARCODE PRINTER

REM Set working directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ===================================================
    echo ERROR: Python tidak ditemukan!
    echo ===================================================
    echo.
    echo Solusi:
    echo 1. Install Python dari https://www.python.org
    echo 2. Pastikan "Add Python to PATH" dicentang saat install
    echo 3. Restart komputer
    echo.
    echo Tekan ENTER untuk menutup...
    pause >nul
    exit /b 1
)

REM Check if paho-mqtt is installed
python -m pip show paho-mqtt >nul 2>&1
if errorlevel 1 (
    echo.
    echo ===================================================
    echo Installing required package: paho-mqtt...
    echo ===================================================
    echo.
    python -m pip install paho-mqtt
)

REM Run the Python script
echo.
echo ===================================================
echo Starting Node-RED Barcode Printer Service...
echo ===================================================
echo.
echo MQTT Broker: 192.168.1.103
echo Subscribe Topic: node-red/barcode/print
echo Status Topic: node-red/barcode/status
echo.
echo Waiting for messages from Node-RED...
echo.

python node_red_printer.py

pause

exit /b 0
