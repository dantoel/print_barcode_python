@echo off
REM ========================================================================
REM Troubleshoot Database Connection
REM ========================================================================

chcp 65001 >nul
cd /d "C:\ws\KodeArduinoUtama\printer02"

echo.
echo ========================================================================
echo  DATABASE CONNECTION TROUBLESHOOTING
echo ========================================================================
echo.
echo Script ini akan test:
echo   [1] Ping ke server
echo   [2] Port 3306 (MySQL)
echo   [3] Koneksi MySQL
echo   [4] Table production_schedule
echo.
echo ========================================================================
echo.

python troubleshoot_connection.py

echo.
pause
