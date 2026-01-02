@echo off
REM ========================================================================
REM Test database connection
REM ========================================================================

chcp 65001 >nul

cd /d "C:\ws\KodeArduinoUtama\printer02"

echo.
echo ========================================================================
echo  TEST DATABASE CONNECTION
echo ========================================================================
echo.

python test_database_connection.py

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✓ Test berhasil
) else (
    echo.
    echo ✗ Test gagal - cek konfigurasi database
)

echo.
pause
