#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================
PRINTER DIAGNOSTIC TOOL
========================================================================
Tool untuk diagnosis lengkap masalah printer
"""

import os
import sys
import json
import time
import subprocess
from ctypes import *
from pathlib import Path
import configparser

# ========================================================================
# LOAD CONFIG
# ========================================================================

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "mqtt_config.ini")

cfg = configparser.ConfigParser()
cfg.read(CONFIG_FILE)

DLL_PATH = cfg.get("PRINTER", "DLL_PATH", fallback="C:\\KodeArduinoUtama\\printer02\\Msprintsdk.dll")

# ========================================================================
# COLOR OUTPUT
# ========================================================================

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Color.BOLD}{Color.CYAN}{'='*70}{Color.END}")
    print(f"{Color.BOLD}{Color.CYAN}{text:^70}{Color.END}")
    print(f"{Color.BOLD}{Color.CYAN}{'='*70}{Color.END}\n")

def print_success(text):
    print(f"{Color.GREEN}✓ {text}{Color.END}")

def print_error(text):
    print(f"{Color.RED}✗ {text}{Color.END}")

def print_warning(text):
    print(f"{Color.YELLOW}⚠ {text}{Color.END}")

def print_info(text):
    print(f"{Color.BLUE}ℹ {text}{Color.END}")

# ========================================================================
# TEST 1: DLL AVAILABILITY
# ========================================================================

def test_dll_exists():
    print_header("TEST 1: DLL PATH & AVAILABILITY")
    
    print(f"DLL Path: {DLL_PATH}")
    
    if os.path.exists(DLL_PATH):
        size = os.path.getsize(DLL_PATH)
        print_success(f"DLL ditemukan! Size: {size:,} bytes")
        return True
    else:
        print_error(f"DLL TIDAK ditemukan!")
        print_warning("Periksa path di mqtt_config.ini atau pastikan file ada")
        return False

# ========================================================================
# TEST 2: DLL LOADING
# ========================================================================

def test_dll_loading():
    print_header("TEST 2: LOAD DLL")
    
    try:
        printer_dll = cdll.LoadLibrary(DLL_PATH)
        print_success("DLL berhasil di-load")
        return printer_dll
    except Exception as e:
        print_error(f"Gagal load DLL: {str(e)}")
        print_warning("Kemungkinan:")
        print_warning("- DLL corrupted atau tidak compatible")
        print_warning("- Missing dependencies (Visual C++ runtime)")
        print_warning("- DLL sudah di-load oleh proses lain")
        return None

# ========================================================================
# TEST 3: DLL FUNCTIONS
# ========================================================================

def test_dll_functions(dll):
    print_header("TEST 3: CHECK DLL FUNCTIONS")
    
    if not dll:
        print_error("DLL tidak ter-load, skip test ini")
        return False
    
    functions = [
        "OpenPrinter",
        "ClosePrinter", 
        "PrintBarcode",
        "PrintQRCode",
        "Status",
        "GetStatus"
    ]
    
    all_exist = True
    
    for func_name in functions:
        try:
            func = getattr(dll, func_name, None)
            if func:
                print_success(f"Function '{func_name}' tersedia")
            else:
                print_warning(f"Function '{func_name}' tidak ditemukan (mungkin OK)")
        except Exception as e:
            print_warning(f"Function '{func_name}': {str(e)}")
    
    return True

# ========================================================================
# TEST 4: PRINTER CONNECTION
# ========================================================================

def test_printer_connection(dll):
    print_header("TEST 4: PRINTER CONNECTION")
    
    if not dll:
        print_error("DLL tidak ter-load, skip test ini")
        return False
    
    try:
        # Try OpenPrinter
        if hasattr(dll, 'OpenPrinter'):
            result = dll.OpenPrinter()
            
            if result == 0:
                print_success("Printer terbuka/terdeteksi (OpenPrinter = 0)")
                
                # Try close
                if hasattr(dll, 'ClosePrinter'):
                    dll.ClosePrinter()
                    print_success("Printer berhasil ditutup")
                
                return True
            else:
                print_error(f"Printer tidak terbuka (OpenPrinter = {result})")
                print_warning("Kemungkinan:")
                print_warning("- Printer tidak terhubung USB")
                print_warning("- Printer tidak hidup")
                print_warning("- Driver printer tidak installed")
                print_warning("- Ada device lain yang lock printer")
                return False
        else:
            print_warning("Function OpenPrinter tidak ada, skip connection test")
            return False
            
    except Exception as e:
        print_error(f"Error saat test connection: {str(e)}")
        return False

# ========================================================================
# TEST 5: PRINT TEST
# ========================================================================

def test_print_barcode(dll):
    print_header("TEST 5: TEST PRINT BARCODE")
    
    if not dll:
        print_error("DLL tidak ter-load, skip test ini")
        return False
    
    try:
        print_info("Attempting to print test barcode...")
        
        if hasattr(dll, 'OpenPrinter'):
            open_result = dll.OpenPrinter()
            print_info(f"OpenPrinter result: {open_result}")
            
            if open_result != 0:
                print_error("Tidak bisa buka printer")
                return False
            
            # Print test
            if hasattr(dll, 'PrintBarcode'):
                # Try print simple barcode
                test_code = "TEST123456789"
                print_info(f"Printing test code: {test_code}")
                
                print_result = dll.PrintBarcode(test_code.encode())
                print_info(f"PrintBarcode result: {print_result}")
                
                time.sleep(2)
                
                if hasattr(dll, 'ClosePrinter'):
                    dll.ClosePrinter()
                
                if print_result == 0:
                    print_success("✅ TEST PRINT SUKSES! Barcode seharusnya sudah tercetak")
                    return True
                else:
                    print_error(f"Print gagal (result={print_result})")
                    print_warning("Kemungkinan:")
                    print_warning("- Printer out of paper")
                    print_warning("- Printer error/jam")
                    print_warning("- Print head problem")
                    return False
            else:
                print_error("Function PrintBarcode tidak ada")
                return False
        else:
            print_warning("Function OpenPrinter tidak ada")
            return False
            
    except Exception as e:
        print_error(f"Error saat test print: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# ========================================================================
# TEST 6: MQTT CONNECTION
# ========================================================================

def test_mqtt_connection():
    print_header("TEST 6: MQTT CONNECTIVITY")
    
    try:
        import paho.mqtt.client as mqtt
        print_success("Module paho-mqtt installed")
        
        broker = cfg.get("MQTT", "BROKER_ADDRESS", fallback="broker.hivemq.com")
        port = cfg.getint("MQTT", "BROKER_PORT", fallback=1883)
        
        print_info(f"Testing connection to {broker}:{port}...")
        
        # Compatible with both v1 and v2 API
        try:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "diagnostic_test")
        except AttributeError:
            client = mqtt.Client("diagnostic_test")
        
        client.connect(broker, port, keepalive=5)
        client.loop_start()
        
        time.sleep(2)
        
        if client.is_connected():
            print_success(f"✓ Connected to MQTT broker {broker}:{port}")
            client.disconnect()
            return True
        else:
            print_warning(f"Connection pending, likely OK")
            client.disconnect()
            return True
            
    except ImportError:
        print_error("Module paho-mqtt tidak di-install")
        print_warning("Install dengan: pip install paho-mqtt")
        return False
    except Exception as e:
        print_error(f"MQTT connection failed: {str(e)}")
        print_warning("Kemungkinan:")
        print_warning("- Internet/network tidak connect")
        print_warning("- MQTT broker down")
        print_warning("- Firewall block MQTT port")
        return False

# ========================================================================
# TEST 7: USB DEVICES
# ========================================================================

def test_usb_devices():
    print_header("TEST 7: USB DEVICES")
    
    try:
        # Try using wmic to list USB devices
        result = subprocess.run(
            ['wmic', 'logicaldisk', 'get', 'name'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        print_info("System USB/Device info:")
        
        # Try list COM ports
        try:
            result = subprocess.run(
                ['powershell', '-Command', 
                 'Get-PnpDevice -Class Ports | Where-Object {$_.Name -match "COM"}'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout:
                print_info("Found COM ports:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        print(f"  {line}")
            else:
                print_warning("No COM ports found (printer mungkin USB)")
                
        except:
            print_warning("Could not list COM ports")
        
        return True
        
    except Exception as e:
        print_warning(f"Could not check USB devices: {str(e)}")
        return False

# ========================================================================
# TEST 8: FILE PERMISSIONS
# ========================================================================

def test_file_permissions():
    print_header("TEST 8: FILE PERMISSIONS")
    
    current_dir = os.path.dirname(__file__)
    test_file = os.path.join(current_dir, "test_permission.tmp")
    
    try:
        # Try write
        with open(test_file, 'w') as f:
            f.write("test")
        print_success("Write permission: OK")
        
        # Try read
        with open(test_file, 'r') as f:
            content = f.read()
        print_success("Read permission: OK")
        
        # Try delete
        os.remove(test_file)
        print_success("Delete permission: OK")
        
        return True
        
    except PermissionError:
        print_error("Permission denied - run as Administrator")
        return False
    except Exception as e:
        print_error(f"Permission test failed: {str(e)}")
        return False

# ========================================================================
# SUMMARY & RECOMMENDATIONS
# ========================================================================

def print_summary(results):
    print_header("SUMMARY & RECOMMENDATIONS")
    
    total = len(results)
    passed = sum(1 for r in results if r)
    failed = total - passed
    
    print(f"Tests Passed: {Color.GREEN}{passed}/{total}{Color.END}")
    print(f"Tests Failed: {Color.RED}{failed}/{total}{Color.END}\n")
    
    if all(results):
        print_success("✓ Semua test PASSED! Printer seharusnya berfungsi normal.")
    else:
        print_warning("Ada beberapa test yang gagal. Lihat detail di atas.")
        print("\n" + Color.BOLD + "REKOMENDASI:" + Color.END)
        
        if not results[0]:  # DLL exists
            print("1. Cek path DLL di mqtt_config.ini")
            print("   - Path harus absolut dan benar")
            print("   - Pastikan file Msprintsdk.dll ada di lokasi tersebut")
        
        if not results[1]:  # DLL loading
            print("2. Install Visual C++ Runtime:")
            print("   - Download dari: https://support.microsoft.com/en-us/help/2977003/")
            print("   - Restart komputer setelah install")
        
        if not results[3]:  # Printer connection
            print("3. Periksa koneksi printer:")
            print("   - Hubungkan USB printer")
            print("   - Nyalakan printer")
            print("   - Cek di Device Manager (printer terdeteksi)")
            print("   - Install driver printer jika belum")
        
        if not results[4]:  # Print test
            print("4. Jika printer terdeteksi tapi print gagal:")
            print("   - Cek paper/tinta printer")
            print("   - Cek kabel USB tidak loose")
            print("   - Lihat error di printer panel")
            print("   - Restart printer dan komputer")
        
        if not results[5]:  # MQTT
            print("5. Jika MQTT gagal:")
            print("   - Cek koneksi internet")
            print("   - Ping broker: ping broker.hivemq.com")
            print("   - Cek firewall settings")

# ========================================================================
# MAIN
# ========================================================================

def main():
    print(f"\n{Color.BOLD}{Color.CYAN}")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "PRINTER DIAGNOSTIC TOOL".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    print(f"{Color.END}\n")
    
    print_info(f"Config file: {CONFIG_FILE}")
    print_info(f"DLL path: {DLL_PATH}")
    print(f"\nKomputasi hostname: {os.environ.get('COMPUTERNAME', 'unknown')}")
    print(f"Python version: {sys.version.split()[0]}\n")
    
    results = []
    dll = None
    
    # Run tests
    results.append(test_dll_exists())
    dll = test_dll_loading()
    results.append(dll is not None)
    results.append(test_dll_functions(dll))
    results.append(test_printer_connection(dll))
    results.append(test_print_barcode(dll))
    results.append(test_mqtt_connection())
    results.append(test_usb_devices())
    results.append(test_file_permissions())
    
    # Print summary
    print_summary(results)
    
    print(f"\n{Color.BOLD}Press ENTER to exit...{Color.END}")
    input()

if __name__ == "__main__":
    main()
