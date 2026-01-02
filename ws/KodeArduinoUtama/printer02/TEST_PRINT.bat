@echo off
REM ========================================================================
REM Cetak barcode terbatas (test print 1-5 item)
REM ========================================================================

chcp 65001 >nul
setlocal enabledelayedexpansion

cd /d "C:\ws\KodeArduinoUtama\printer02"

echo.
echo ========================================================================
echo  TEST PRINT - Cetak Limited Items
echo ========================================================================
echo.
echo Pilih jumlah item yang ingin dicetak:
echo   1. Test (1 item)
echo   2. Small batch (5 item)
echo   3. Full batch (semua item)
echo.
set /p choice="Pilih (1-3): "

if "%choice%"=="1" (
    echo Mencetak 1 item...
    python cetak_dari_database.py --limit 1
) else if "%choice%"=="2" (
    echo Mencetak 5 item...
    python cetak_dari_database.py --limit 5
) else if "%choice%"=="3" (
    echo Mencetak semua item...
    python cetak_dari_database.py
) else (
    echo Pilihan tidak valid
)

echo.
pause
