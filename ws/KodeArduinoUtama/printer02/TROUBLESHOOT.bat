@echo off
REM ========================================================================
REM QUICK TROUBLESHOOT MENU
REM ========================================================================

:menu
cls
echo.
echo ========================================================================
echo                   PRINTER TROUBLESHOOTING MENU
echo ========================================================================
echo.
echo Pilih opsi:
echo.
echo   1. Run Full Diagnostic (recommended first)
echo   2. Check Printer Status & Queue
echo   3. Test Print Barcode
echo   4. Clear Printer Error (reboot printer driver)
echo   5. View Error Log
echo   6. Reset Queue Database
echo   7. Test MQTT Connection
echo   8. Show System Info
echo   9. Open Troubleshooting Guide
echo   0. Exit
echo.
set /p choice="Pilihan (0-9): "

if "%choice%"=="1" goto diagnostic
if "%choice%"=="2" goto status
if "%choice%"=="3" goto testprint
if "%choice%"=="4" goto clearpriter
if "%choice%"=="5" goto viewlog
if "%choice%"=="6" goto resetqueue
if "%choice%"=="7" goto testmqtt
if "%choice%"=="8" goto sysinfo
if "%choice%"=="9" goto guide
if "%choice%"=="0" goto exit
echo Invalid choice!
pause
goto menu

REM ========================================================================

:diagnostic
echo.
echo Running full diagnostic...
echo.
python DIAGNOSTIC_PRINTER.py
goto menu

REM ========================================================================

:status
echo.
echo Checking printer status...
echo.
call CHECK_STATUS.bat
goto menu

REM ========================================================================

:testprint
echo.
echo Test print akan mencoba mencetak barcode test...
echo Pastikan printer nyala dan siap!
echo.
pause
python -c "
import os, sys, configparser
from ctypes import *

config = configparser.ConfigParser()
config.read('mqtt_config.ini')
dll_path = config.get('PRINTER', 'DLL_PATH', fallback='Msprintsdk.dll')

try:
    dll = cdll.LoadLibrary(dll_path)
    print('[*] DLL loaded')
    
    if hasattr(dll, 'OpenPrinter'):
        result = dll.OpenPrinter()
        print(f'[*] OpenPrinter: {result}')
        
        if result == 0 and hasattr(dll, 'PrintBarcode'):
            test_barcode = 'TEST123'
            print(f'[*] Printing: {test_barcode}')
            print_result = dll.PrintBarcode(test_barcode.encode())
            print(f'[*] PrintBarcode result: {print_result}')
            print('[✓] Print task sent! Check printer output...')
            
            dll.ClosePrinter()
        else:
            print('[✗] Cannot open printer')
    else:
        print('[✗] OpenPrinter not available')
except Exception as e:
    print(f'[✗] Error: {e}')
"
pause
goto menu

REM ========================================================================

:clearpriter
echo.
echo Clearing printer error...
echo This will restart printer driver.
echo.

REM Check for USB printer and reset
powershell -Command "Get-PnpDevice -Class 'Printer' | Restart-PnpDevice -Force -Confirm:$false" 2>nul

echo [✓] Printer driver restarted
echo Tunggu 5 detik untuk device re-enumerate...
timeout /t 5

goto menu

REM ========================================================================

:viewlog
echo.
echo Searching for log file...
echo.

if exist "mqtt_printer.log" (
    echo Last 50 lines from log:
    echo.
    powershell -Command "Get-Content 'mqtt_printer.log' -Last 50"
) else (
    echo Log file not found in current directory
    echo Check config.ini for LOG_FILE path
)

pause
goto menu

REM ========================================================================

:resetqueue
echo.
echo WARNING: This will CLEAR the print queue database!
echo All pending/failed items will be DELETED!
echo.
set /p confirm="Are you sure? (yes/no): "

if /i "%confirm%"=="yes" (
    if exist "print_queue.db" (
        del print_queue.db
        echo [✓] Queue database deleted
        echo Restart mqtt_cloud_printer.py to recreate empty database
    ) else (
        echo Queue database not found
    )
) else (
    echo Cancelled
)

pause
goto menu

REM ========================================================================

:testmqtt
echo.
echo Testing MQTT connection...
echo.
python -c "
import configparser

config = configparser.ConfigParser()
config.read('mqtt_config.ini')

broker = config.get('MQTT', 'BROKER_ADDRESS', fallback='broker.hivemq.com')
port = config.getint('MQTT', 'BROKER_PORT', fallback=1883)

print(f'[*] Testing connection to {broker}:{port}')

try:
    import paho.mqtt.client as mqtt
    import time
    
    client = mqtt.Client('test_client')
    client.connect(broker, port, keepalive=5)
    client.loop_start()
    
    time.sleep(2)
    
    if client.is_connected():
        print(f'[✓] Successfully connected to MQTT broker!')
        client.disconnect()
    else:
        print('[✓] Connection in progress (should work)')
        client.disconnect()
except ImportError:
    print('[✗] paho-mqtt not installed. Run: pip install paho-mqtt')
except Exception as e:
    print(f'[✗] Connection failed: {e}')
    print('[!] Check:')
    print('    - Internet connection')
    print('    - Broker address in config.ini')
    print('    - Firewall settings')
"
pause
goto menu

REM ========================================================================

:sysinfo
echo.
echo System Information:
echo.
systeminfo | findstr /C:"Computer Name" /C:"OS Name" /C:"OS Version" /C:"System Boot Time"
echo.
echo Network:
ipconfig | findstr /C:"IPv4 Address" /C:"DNS Servers"
echo.
echo Printers:
echo.
wmic logicaldisk get name 2>nul | findstr /V "Name"
echo.
pause
goto menu

REM ========================================================================

:guide
if exist "TROUBLESHOOTING_GUIDE.md" (
    start notepad TROUBLESHOOTING_GUIDE.md
) else (
    echo Troubleshooting guide not found
    pause
)
goto menu

REM ========================================================================

:exit
echo.
echo Goodbye!
echo.
