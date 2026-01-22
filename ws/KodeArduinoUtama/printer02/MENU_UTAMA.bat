@echo off
REM ========================================================================
REM LAUNCHER GUI STYLE - Click-friendly version
REM ========================================================================

setlocal enabledelayedexpansion

:menu
cls
echo.
echo ========================================================================
echo           CETAK QR CODE DARI DATABASE PRODUCTION_SCHEDULE
echo ========================================================================
echo.
echo Database: 192.168.12.250 (admin-reka)
echo Status: WHERE production_proggress = 'Ready'
echo.
echo ========================================================================
echo.
echo Pilih opsi:
echo.
echo   [1] PRINT SEMUA DATA READY
echo       - Cetak semua produk dengan status Ready
echo.
echo   [2] TEST PRINT (Limit)
echo       - Test dengan 1, 5, atau semua item
echo.
echo   [3] DEBUG MODE
echo       - Tampilkan detail step-by-step
echo.
echo   [4] TEST DATABASE
echo       - Cek koneksi database
echo.
echo   [5] LIHAT LOG
echo       - Lihat history print
echo.
echo   [6] EXIT
echo       - Keluar
echo.
echo ========================================================================
echo.
set /p choice="Masukkan pilihan (1-6): "

if "%choice%"=="1" goto print_all
if "%choice%"=="2" goto test_print
if "%choice%"=="3" goto debug_mode
if "%choice%"=="4" goto test_db
if "%choice%"=="5" goto view_log
if "%choice%"=="6" goto exit_menu
if "%choice%"=="0" goto exit_menu

echo.
echo [X] Pilihan tidak valid
echo.
pause
goto menu

:print_all
cls
echo.
echo ========================================================================
echo  PRINT SEMUA DATA READY
echo ========================================================================
echo.
cd /d "C:\ws\KodeArduinoUtama\printer02"
python cetak_dari_database.py
pause
goto menu

:test_print
cls
echo.
echo ========================================================================
echo  TEST PRINT
echo ========================================================================
echo.
echo [1] Test 1 item
echo [2] Test 5 item
echo [3] Print semua
echo.
set /p test_choice="Pilih (1-3): "

if "%test_choice%"=="1" (
    cd /d "C:\ws\KodeArduinoUtama\printer02"
    python cetak_dari_database.py --limit 1
) else if "%test_choice%"=="2" (
    cd /d "C:\ws\KodeArduinoUtama\printer02"
    python cetak_dari_database.py --limit 5
) else if "%test_choice%"=="3" (
    cd /d "C:\ws\KodeArduinoUtama\printer02"
    python cetak_dari_database.py
) else (
    echo Pilihan tidak valid
)

pause
goto menu

:debug_mode
cls
echo.
echo ========================================================================
echo  DEBUG MODE - Verbose Output
echo ========================================================================
echo.
cd /d "C:\ws\KodeArduinoUtama\printer02"
python cetak_dari_database.py --debug
pause
goto menu

:test_db
cls
echo.
echo ========================================================================
echo  TEST DATABASE CONNECTION
echo ========================================================================
echo.
cd /d "C:\ws\KodeArduinoUtama\printer02"
python test_database_connection.py
pause
goto menu

:view_log
cls
echo.
echo ========================================================================
echo  LOG FILE - CETAK_LOG.TXT
echo ========================================================================
echo.
set LOG_FILE=C:\ws\KodeArduinoUtama\printer02\cetak_log.txt
if exist "%LOG_FILE%" (
    type "%LOG_FILE%"
) else (
    echo Log file tidak ditemukan: %LOG_FILE%
)
echo.
echo ========================================================================
echo.
pause
goto menu

:exit_menu
cls
echo.
echo Terima kasih telah menggunakan CETAK QR CODE
echo.
exit /b 0
