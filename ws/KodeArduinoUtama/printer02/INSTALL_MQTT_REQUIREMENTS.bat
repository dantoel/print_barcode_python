@echo off
chcp 65001 >nul
title Install MQTT Printer Requirements
color 0E

echo ========================================================================
echo INSTALL MQTT PRINTER REQUIREMENTS
echo ========================================================================
echo.
echo This will install required Python packages:
echo   - paho-mqtt (MQTT client library)
echo.
echo ========================================================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Python not found!
    echo Please install Python 3.7 or higher from python.org
    echo.
    pause
    exit /b 1
)

echo.
echo Installing paho-mqtt...
echo.
python -m pip install --upgrade pip
python -m pip install paho-mqtt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================================
    echo SUCCESS: All requirements installed!
    echo ========================================================================
    echo.
    echo You can now run: RUN_MQTT_CLOUD_PRINTER.bat
    echo.
) else (
    echo.
    echo ========================================================================
    echo ERROR: Installation failed!
    echo ========================================================================
    echo.
    echo Try running this command manually:
    echo   pip install paho-mqtt
    echo.
)

pause
