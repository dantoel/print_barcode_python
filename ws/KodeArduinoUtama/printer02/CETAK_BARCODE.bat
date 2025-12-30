@echo off
REM =====================================================
REM Script untuk cetak barcode manual
REM =====================================================
REM Double-click file ini untuk mulai cetak barcode
REM =====================================================

setlocal enabledelayedexpansion

title CETAK BARCODE MANUAL

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

REM Run the Python script
echo.
echo ===================================================
echo Starting Barcode Printing Script...
echo ===================================================
echo.

python cetak_manual.py

exit /b 0
