@echo off
REM ========================================================================
REM View log file
REM ========================================================================

chcp 65001 >nul

echo.
echo ========================================================================
echo  LOG FILE VIEWER
echo ========================================================================
echo.

set LOG_FILE=C:\ws\KodeArduinoUtama\printer02\cetak_log.txt

if exist "%LOG_FILE%" (
    echo Log file: %LOG_FILE%
    echo.
    type "%LOG_FILE%"
    echo.
) else (
    echo Log file tidak ditemukan: %LOG_FILE%
    echo.
)

pause
