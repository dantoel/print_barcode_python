#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnostic Tool - Check Printer Connection & Status
"""

import sys
import os
from ctypes import *

DLL_PATH = r"C:\KodeArduinoUtama\printer02\Msprintsdk.dll"

print("="*70)
print("PRINTER DIAGNOSTIC TOOL")
print("="*70)
print(f"\nDLL Path: {DLL_PATH}")

# Step 1: Check DLL exists
print("\n[1] Checking DLL file...")
if os.path.exists(DLL_PATH):
    print(f"    ✓ DLL found: {DLL_PATH}")
else:
    print(f"    ✗ DLL NOT found: {DLL_PATH}")
    print("    Solusi: Pastikan path DLL benar")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Step 2: Load DLL
print("\n[2] Loading DLL...")
try:
    printer_dll = cdll.LoadLibrary(DLL_PATH)
    print("    ✓ DLL loaded successfully")
except Exception as e:
    print(f"    ✗ Failed to load DLL: {str(e)}")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Step 3: Initialize printer
print("\n[3] Initializing printer...")
try:
    result = printer_dll.SetUsbportauto()
    print(f"    SetUsbportauto: {result}")
    
    result = printer_dll.SetInit()
    print(f"    SetInit: {result}")
    
    printer_dll.SetClean()
    print("    SetClean: OK")
    
except Exception as e:
    print(f"    ✗ Init failed: {str(e)}")
    input("\nPress Enter to exit...")
    sys.exit(1)

# Step 4: Get printer status
print("\n[4] Getting printer status...")
try:
    status = printer_dll.GetStatus()
    print(f"    Status code: {status}")
    
    if status == 1:
        print("    ✓ Printer READY")
    elif status == 8:
        print("    ⚠️ Printer NOT READY (Status 8)")
        print("    Possible issues:")
        print("       - USB cable not connected properly")
        print("       - Printer power OFF")
        print("       - No paper loaded")
        print("       - Paper jam")
        print("       - Printer cover open")
    else:
        print(f"    ⚠️ Unknown status: {status}")
        
except Exception as e:
    print(f"    ✗ Failed to get status: {str(e)}")

# Step 5: Test print (if status OK)
print("\n[5] Attempting test print...")
try:
    if status == 1:
        # Print test string
        printer_dll.SetAlignment(1)
        printer_dll.SetSizetext(2, 2)
        test_string = "=== TEST PRINT ===".encode('utf-8')
        printer_dll.PrintString(test_string, 0)
        
        # Feed paper
        for _ in range(3):
            printer_dll.PrintChargeRow()
        
        # Cut paper
        printer_dll.PrintCutpaper(1)
        
        from time import sleep
        sleep(2)
        
        printer_dll.SetClose()
        
        print("    ✓ Test print command sent!")
        print("    Check printer for output...")
    else:
        print(f"    ⊗ Skipped (printer status: {status})")
        
except Exception as e:
    print(f"    ✗ Test print failed: {str(e)}")

print("\n" + "="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70)

if status == 8:
    print("\n⚠️ PRINTER STATUS 8 - SOLUSI:")
    print("1. Cabut dan pasang kembali USB printer")
    print("2. Pastikan printer menyala (lampu hijau)")
    print("3. Pastikan ada kertas")
    print("4. Tutup cover printer dengan benar")
    print("5. Restart printer (cabut-pasang power)")
    print("6. Restart PC jika masih gagal")

print("\n")
input("Press Enter to exit...")
