@echo off
REM ========================================================================
REM PRINTER DIAGNOSTIC BATCH FILE
REM Jalankan ini untuk test printer
REM ========================================================================

setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo                    PRINTER DIAGNOSTIC TOOL
echo ========================================================================
echo.
echo Diagnostic ini akan test:
echo   1. DLL availability
echo   2. DLL loading
echo   3. Printer connection
echo   4. Print test
echo   5. MQTT connection
echo   6. USB devices
echo   7. File permissions
echo.
echo Starting diagnostic...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python tidak ter-install atau tidak di-PATH
    echo Silakan install Python dari https://www.python.org/
    pause
    exit /b 1
)

REM Run diagnostic
python DIAGNOSTIC_PRINTER.py

REM Show result
if %errorlevel% equ 0 (
    echo.
    echo ========================================================================
    echo Diagnostic selesai. Lihat hasil di atas.
    echo ========================================================================
) else (
    echo.
    echo ERROR: Diagnostic failed with error code %errorlevel%
    echo ========================================================================
)

pause
