@echo off
REM ========================================================================
REM Script untuk cetak barcode otomatis dari database MySQL
REM Database: 192.168.12.250
REM Table: production_schedule
REM Status: WHERE production_proggress = 'Ready'
REM ========================================================================

chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "C:\ws\KodeArduinoUtama\printer02"

echo.
echo ========================================================================
echo  CETAK BARCODE DARI DATABASE
echo ========================================================================
echo.
echo Konfigurasi:
echo   Host: 192.168.12.250
echo   User: admin-reka
echo   Database: reka
echo   Tabel: production_schedule
echo   Kondisi: production_proggress = 'Ready'
echo.
echo ========================================================================
echo.

python cetak_dari_database.py %*

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✓ Program selesai berhasil
) else (
    echo.
    echo ✗ Program selesai dengan error (code: %ERRORLEVEL%)
)

echo.
pause
