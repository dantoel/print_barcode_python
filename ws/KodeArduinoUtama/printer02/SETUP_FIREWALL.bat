@echo off
REM =====================================================
REM Setup Firewall Rules for MQTT
REM =====================================================
REM Run as Administrator!

setlocal enabledelayedexpansion

cls

echo.
echo =====================================================
echo MQTT FIREWALL SETUP
echo =====================================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This script requires Administrator privileges!
    echo.
    echo Please:
    echo 1. Right-click on this file
    echo 2. Select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

echo Adding firewall rules for MQTT...
echo.

REM Rule 1: MQTT 1883 Outbound
echo [*] Adding rule: MQTT 1883 Outbound...
powershell -Command "New-NetFirewallRule -DisplayName 'MQTT 1883 Outbound' -Direction Outbound -Protocol TCP -RemotePort 1883 -Action Allow -ErrorAction SilentlyContinue" >nul 2>&1
if %errorlevel% equ 0 (
    echo     ✓ MQTT 1883 Outbound: Added
) else (
    echo     ! MQTT 1883 Outbound: Already exists or error
)

REM Rule 2: MQTT 8883 Outbound
echo [*] Adding rule: MQTT 8883 Outbound...
powershell -Command "New-NetFirewallRule -DisplayName 'MQTT 8883 Outbound' -Direction Outbound -Protocol TCP -RemotePort 8883 -Action Allow -ErrorAction SilentlyContinue" >nul 2>&1
if %errorlevel% equ 0 (
    echo     ✓ MQTT 8883 Outbound: Added
) else (
    echo     ! MQTT 8883 Outbound: Already exists or error
)

REM Rule 3: DNS (Port 53)
echo [*] Adding rule: DNS Outbound (Port 53)...
powershell -Command "New-NetFirewallRule -DisplayName 'DNS Outbound' -Direction Outbound -Protocol UDP -RemotePort 53 -Action Allow -ErrorAction SilentlyContinue" >nul 2>&1
if %errorlevel% equ 0 (
    echo     ✓ DNS Outbound: Added
) else (
    echo     ! DNS Outbound: Already exists or error
)

echo.
echo =====================================================
echo Firewall rules setup complete!
echo =====================================================
echo.
echo Rules added:
echo - MQTT 1883 (Unencrypted)
echo - MQTT 8883 (TLS)
echo - DNS 53 (For hostname resolution)
echo.

pause

exit /b 0
