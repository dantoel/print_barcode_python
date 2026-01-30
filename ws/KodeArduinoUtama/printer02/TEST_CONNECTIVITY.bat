@echo off
REM =====================================================
REM Test MQTT Broker Connectivity
REM =====================================================

setlocal enabledelayedexpansion

title MQTT Connectivity Test

cd /d "%~dp0"

cls

echo.
echo =====================================================
echo MQTT CONNECTIVITY DIAGNOSTIC
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

echo Running connectivity tests...
echo.

REM Run test script
python test_connectivity.py

echo.
echo Press any key to continue...
pause >nul

exit /b 0
