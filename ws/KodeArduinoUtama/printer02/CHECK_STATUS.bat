@echo off
REM ========================================================================
REM STATUS CHECK - Lihat detail status printer & queue
REM ========================================================================

setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo                      PRINTER STATUS CHECK
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python tidak ter-install
    pause
    exit /b 1
)

REM Create temp Python script
(
echo import sqlite3
echo import os
echo import json
echo from datetime import datetime
echo from pathlib import Path
echo import configparser
echo.
echo CONFIG_FILE = "mqtt_config.ini"
echo cfg = configparser.ConfigParser()
echo cfg.read(CONFIG_FILE)
echo.
echo QUEUE_DB = "print_queue.db"
echo DLL_PATH = cfg.get("PRINTER", "DLL_PATH", fallback="N/A"^)
echo.
echo print("="*70^)
echo print("PRINTER STATUS".center(70^)^)
echo print("="*70^)
echo print()
echo.
echo print(f"DLL Path: {DLL_PATH}"^)
echo print(f"DLL Exists: {os.path.exists(DLL_PATH)}"^)
echo print(f"Queue DB: {QUEUE_DB}"^)
echo print(f"Queue DB Exists: {os.path.exists(QUEUE_DB)}"^)
echo print()
echo.
echo if os.path.exists(QUEUE_DB^):
echo     conn = sqlite3.connect(QUEUE_DB^)
echo     cursor = conn.cursor()
echo.
echo     print("="*70^)
echo     print("QUEUE STATISTICS".center(70^)^)
echo     print("="*70^)
echo     print()
echo.
echo     cursor.execute('SELECT COUNT(*) FROM print_queue WHERE status="pending"'^)
echo     pending = cursor.fetchone()[0]
echo     cursor.execute('SELECT COUNT(*) FROM print_queue WHERE status="printed"'^)
echo     printed = cursor.fetchone()[0]
echo     cursor.execute('SELECT COUNT(*) FROM print_queue WHERE status="failed"'^)
echo     failed = cursor.fetchone()[0]
echo.
echo     print(f"Pending: {pending}"^)
echo     print(f"Printed: {printed}"^)
echo     print(f"Failed:  {failed}"^)
echo     print()
echo.
echo     if pending ^> 0:
echo         print("="*70^)
echo         print("PENDING ITEMS (Next 10^)".center(70^)^)
echo         print("="*70^)
echo         cursor.execute('''
echo             SELECT id, barcode, product, line, created_at, attempted_count
echo             FROM print_queue
echo             WHERE status="pending"
echo             ORDER BY created_at ASC
echo             LIMIT 10
echo         '''^ )
echo         for row in cursor.fetchall(^):
echo             print(f"ID: {row[0]} | Barcode: {row[1]} | Product: {row[2]} | Line: {row[3]}"^)
echo             print(f"  Created: {row[4]} | Attempts: {row[5]}"^)
echo.
echo     if failed ^> 0:
echo         print()
echo         print("="*70^)
echo         print("FAILED ITEMS".center(70^)^)
echo         print("="*70^)
echo         cursor.execute('''
echo             SELECT id, barcode, attempted_count, last_error
echo             FROM print_queue
echo             WHERE status="failed"
echo             LIMIT 5
echo         '''^ )
echo         for row in cursor.fetchall(^):
echo             print(f"ID: {row[0]} | Barcode: {row[1]} | Attempts: {row[2]}"^)
echo             print(f"  Error: {row[3]}"^)
echo.
echo     conn.close()
echo else:
echo     print("Queue database not found"^)
echo.
echo print()
echo print("="*70^)
) > _status_check.py

python _status_check.py

REM Cleanup
del _status_check.py

echo.
echo.
echo Press ENTER to exit...
pause
