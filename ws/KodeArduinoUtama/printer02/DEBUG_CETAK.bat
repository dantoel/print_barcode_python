@echo off
REM ========================================================================
REM DEBUG VERSION - Cetak barcode dari database dengan detail logging
REM ========================================================================

chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "C:\ws\KodeArduinoUtama\printer02"

echo.
echo ========================================================================
echo  CETAK BARCODE DARI DATABASE - DEBUG MODE
echo ========================================================================
echo.
echo Mode: DEBUG (verbose output)
echo.

python cetak_dari_database.py --debug

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✓ Debug selesai
) else (
    echo.
    echo ✗ Debug selesai dengan error
)

echo.
echo Log file tersimpan di: C:\ws\KodeArduinoUtama\printer02\cetak_log.txt
echo.
pause
