import sys
import os
from ctypes import *
from time import sleep
import traceback
from datetime import datetime

# Setup logging file
LOG_FILE = os.path.join(os.path.dirname(__file__), "cetak_barcode_log.txt")

def log_message(message):
    """Log message to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except:
        pass

def cetakBarcode01(id1, nama, ws, debug=False):
    """
    Fungsi cetak QR code dengan debug mode
    
    Args:
        id1: QR code value
        nama: Nama produk
        ws: Workstation code
        debug: Enable debug mode (True/False)
    """
    id1 = id1.strip()
    
    try:        
        barcode = id1
        name = nama
        ws1 = ws
        
        if debug:
            log_message("\n" + "="*50)
            log_message("DEBUG MODE: ON")
            log_message("="*50)
            log_message(f"[1] Input validation:")
            log_message(f"    - Barcode: {barcode}")
            log_message(f"    - Nama: {name}")
            log_message(f"    - Workstation: {ws1}")
        
        # Step 1: Check DLL file exists
        dll_path = r"C:\ws\KodeArduinoUtama\printer02\Msprintsdk.dll"
        if debug:
            log_message(f"\n[2] Checking DLL file:")
            log_message(f"    - Path: {dll_path}")
            log_message(f"    - Exists: {os.path.exists(dll_path)}")
            if not os.path.exists(dll_path):
                log_message(f"    ⚠️  WARNING: DLL file not found!")
                log_message(f"\n    Checking alternative paths...")
                
                # Check untuk alternative paths
                alt_paths = [
                    os.path.join(os.path.dirname(__file__), "Msprintsdk.dll"),
                    r"D:\ws\KodeArduinoUtama\printer02\Msprintsdk.dll",
                    os.path.expandvars(r"%USERPROFILE%\ws\KodeArduinoUtama\printer02\Msprintsdk.dll"),
                ]
                
                for alt_path in alt_paths:
                    exists = os.path.exists(alt_path)
                    log_message(f"    - {alt_path}: {exists}")
                    if exists:
                        dll_path = alt_path
                        log_message(f"    ✓ Found at: {dll_path}")
                        break
        
        # Step 2: Load DLL
        if debug:
            log_message(f"\n[3] Loading DLL...")
        
        try:
            mydll = cdll.LoadLibrary(dll_path)
            if debug:
                log_message(f"    ✓ DLL loaded successfully from: {dll_path}")
            log_message("✓ DLL berhasil dimuat")
        except OSError as dll_error:
            log_message(f"    ✗ FAILED to load DLL: {dll_error}")
            log_message(f"\n    SOLUSI:")
            log_message(f"    1. Pastikan file Msprintsdk.dll ada di folder:")
            log_message(f"       {dll_path}")
            log_message(f"\n    2. Jika tidak ada, cek folder:")
            log_message(f"       - Folder saat ini: {os.path.dirname(__file__)}")
            log_message(f"\n    3. Download Microsoft Visual C++ Redistributable jika belum ada")
            log_message(f"\n    4. Pastikan Python 32-bit atau 64-bit sesuai DLL")
            return False
        
        # Step 3: Printer initialization
        if debug:
            log_message(f"\n[4] Initializing printer...")
        
        try:
            setting = mydll.SetUsbportauto()
            if debug:
                log_message(f"    - SetUsbportauto() returned: {setting}")
            
            setting2 = mydll.SetInit()
            if debug:
                log_message(f"    - SetInit() returned: {setting2}")
            
            mydll.SetClean()
            if debug:
                log_message(f"    - SetClean() executed")
            
            mydll.SetAlignment(2)
            mydll.SetSizechar(2, 2, 0, 0)
            
            status = mydll.GetStatus()
            if debug:
                log_message(f"    - Printer Status: {status}")
            
            log_message("✓ Printer berhasil diinisialisasi")
            
        except AttributeError as attr_error:
            log_message(f"    ✗ FAILED: Printer function not found: {attr_error}")
            log_message(f"    - Check if DLL is correct version")
            log_message(f"\n    SOLUSI:")
            log_message(f"    - DLL mungkin versi salah atau tdk kompatibel")
            log_message(f"    - Verifikasi dengan vendor printer")
            return False
        
        # Step 4: Prepare strings for printing
        if debug:
            log_message(f"\n[5] Preparing print strings...")
        
        string1 = barcode
        string2 = name
        string3 = " " + ws1
        
        try:
            b_string1 = string1.encode('utf-8')
            b_string2 = string2.encode('utf-8')
            b_string3 = string3.encode('utf-8')
            
            if debug:
                log_message(f"    - Barcode (encoded): {b_string1}")
                log_message(f"    - Product Name (encoded): {b_string2}")
                log_message(f"    - Workstation (encoded): {b_string3}")
            
            log_message("✓ String preparation berhasil")
        
        except UnicodeEncodeError as encode_error:
            log_message(f"    ✗ FAILED: String encoding error: {encode_error}")
            return False
        
        # Step 5: Print operations
        if debug:
            log_message(f"\n[6] Executing print commands...")
        
        try:
            mydll.SetAlignment(1)
            mydll.SetSizetext(1, 1)  # WS01 normal size (1x1)
            mydll.PrintString(b_string3, 0)
            if debug:
                log_message(f"    - PrintString(workstation) executed")
            
            mydll.PrintChargeRow()
            
            mydll.SetSizetext(1, 1)
            mydll.PrintString(b_string2, 0)
            if debug:
                log_message(f"    - PrintString(product name) executed")
            
            # Parse and optimize barcode data
            original_data = string1
            barcode_data = string1
            
            # Check if data matches pattern: 683A18101/K3-153/45
            # Extract: ProductNo-SerialNo (683A18101-153)
            if '/' in original_data and '-' in original_data:
                try:
                    parts = original_data.split('/')
                    if len(parts) >= 3:
                        product_no = parts[0]  # 683A18101
                        middle_part = parts[1]  # K3-153
                        
                        # Extract serial number from middle part (after -)
                        if '-' in middle_part:
                            serial_no = middle_part.split('-')[1]  # 153
                            barcode_data = f"{product_no}-{serial_no}"  # 683A18101-153
                            
                            log_message(f"    ℹ Data optimized for barcode:")
                            log_message(f"      Original: {original_data}")
                            log_message(f"      Product No: {product_no}")
                            log_message(f"      Serial No: {serial_no}")
                            log_message(f"      Barcode: {barcode_data}")
                except Exception as parse_error:
                    log_message(f"    ! Could not parse data format, using original")
                    if debug:
                        log_message(f"      Parse error: {parse_error}")
            
            # Print full original data as large text (for human reading)
            mydll.PrintChargeRow()
            mydll.SetSizetext(1, 1)  # Normal text (1x1)
            b_original = original_data.encode('utf-8')
            mydll.PrintString(b_original, 0)
            mydll.PrintChargeRow()
            
            if debug:
                log_message(f"    - Full text printed: {original_data} (size: 1x1)")
            
            # Prepare barcode data
            b_barcode = barcode_data.encode('utf-8')
            data_length = len(barcode_data)
            
            if debug:
                log_message(f"    - Barcode data length: {data_length} characters")
            
            # Add space before printing barcode
            mydll.PrintChargeRow()
            
            # Print barcode - try different types
            qrcode_result = None
            print_success = False
            
            # STRATEGY 1: Standard barcode (Type 2 = EAN/UPC compatible)
            if not print_success:
                try:
                    qrcode_result = mydll.Print1Dbar(2, 60, 1, 2, 4, b_barcode)
                    print_success = True
                    log_message(f"    ✓ Barcode printed: {barcode_data} (Standard Type 2)")
                    if debug:
                        log_message(f"      Print1Dbar(2, 60, 1, 2, 4) returned: {qrcode_result}")
                except Exception as e:
                    if debug:
                        log_message(f"    - Type 2 attempt failed: {e}")
            
            # STRATEGY 2: Try Code128 (Type 73 - supports alphanumeric)
            if not print_success:
                try:
                    mydll.PrintChargeRow()
                    qrcode_result = mydll.Print1Dbar(73, 60, 2, 2, 0, b_barcode)
                    print_success = True
                    log_message(f"    ✓ Barcode printed: {barcode_data} (Code128 Type 73)")
                    if debug:
                        log_message(f"      Print1Dbar(73, 60, 2, 2, 0) returned: {qrcode_result}")
                except Exception as e:
                    if debug:
                        log_message(f"    - Type 73 (Code128) attempt failed: {e}")
            
            # STRATEGY 3: Try QR Code
            if not print_success:
                try:
                    mydll.PrintChargeRow()
                    qrcode_result = mydll.Print2Dbar(6, 5, b_barcode)
                    print_success = True
                    log_message(f"    ✓ QR Code printed: {barcode_data}")
                except Exception as e:
                    if debug:
                        log_message(f"    - QR Code attempt failed: {e}")
            
            if not print_success:
                log_message(f"    ✗ Barcode print failed - all methods attempted")
            
            mydll.PrintChargeRow()
            mydll.PrintChargeRow()
            mydll.PrintChargeRow()
            mydll.PrintChargeRow()
            mydll.PrintChargeRow()
            
            mydll.PrintCutpaper(1)
            if debug:
                log_message(f"    - PrintCutpaper() executed")
            
            mydll.SetClose()
            if debug:
                log_message(f"    - SetClose() executed")
            
            log_message("✓ Print commands executed successfully")
        
        except Exception as print_error:
            log_message(f"    ✗ FAILED during print operation: {print_error}")
            return False
        
        sleep(2)
        log_message("\n✅ Cetak QR code BERHASIL!")
        
        if debug:
            log_message("="*50)
            log_message("DEBUG MODE: Completed successfully")
            log_message("="*50 + "\n")
        
        return True
        
    except Exception as e:
        log_message(f"\n✗ ERROR (Unexpected): {e}")
        log_message(f"\nFull traceback:")
        log_message(traceback.format_exc())
        log_message(f"Gagal cetak QR code")
        return False

if __name__ == "__main__":
    """
    Script untuk manual printing QR code
    
    Cara penggunaan:
    1. Double-click file ini (akan minta input)
    2. Run via command line:
       python cetak_manual.py "686A18101-11" "Nama Produk" "WS01"
       python cetak_manual.py "686A18101-11" "Nama Produk" "WS01" --debug
    
    Log file: cetak_barcode_log.txt (di folder yang sama)
    """
    
    # Clear log file pada awal jika size > 10MB
    try:
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 10 * 1024 * 1024:
            os.remove(LOG_FILE)
    except:
        pass
    
    log_message("\n" + "="*60)
    log_message("MANUAL QR CODE PRINTING SYSTEM")
    log_message("="*60)
    log_message(f"Log file: {LOG_FILE}")
    
    debug_mode = False
    
    if len(sys.argv) > 1:
        # Check if --debug flag is present
        if "--debug" in sys.argv:
            debug_mode = True
            sys.argv.remove("--debug")
        
        barcode_value = sys.argv[1]
        product_name = sys.argv[2] if len(sys.argv) > 2 else "Produk"
        workstation = sys.argv[3] if len(sys.argv) > 3 else "WS01"
    else:
        # Interactive mode - untuk double-click
        log_message("\n[MODE] Interactive mode (no command line arguments)")
        log_message("")
        
        print("\n" + "="*60)
        print("MANUAL BARCODE PRINTING")
        print("="*60)
        print("")
        
        try:
            barcode_value = input("➤ Masukkan barcode value (default: 686A18101-11): ").strip() or "686A18101-11"
            log_message(f"Barcode input: {barcode_value}")
        except:
            barcode_value = "686A18101-11"
            log_message(f"Barcode (default): {barcode_value}")
        
        try:
            product_name = input("➤ Masukkan nama produk (default: Produk): ").strip() or "Produk"
            log_message(f"Product name input: {product_name}")
        except:
            product_name = "Produk"
            log_message(f"Product name (default): {product_name}")
        
        try:
            workstation = input("➤ Masukkan workstation (default: WS01): ").strip() or "WS01"
            log_message(f"Workstation input: {workstation}")
        except:
            workstation = "WS01"
            log_message(f"Workstation (default): {workstation}")
        
        try:
            debug_input = input("➤ Enable debug mode? (y/n, default: n): ").strip().lower() or "n"
            debug_mode = debug_input == "y"
            log_message(f"Debug mode: {debug_mode}")
        except:
            debug_mode = False
            log_message(f"Debug mode (default): {debug_mode}")
        
        print("")
    
    log_message(f"\nMencetak barcode:")
    log_message(f"  Barcode      : {barcode_value}")
    log_message(f"  Produk       : {product_name}")
    log_message(f"  Workstation  : {workstation}")
    log_message(f"  Debug Mode   : {'ENABLED' if debug_mode else 'DISABLED'}")
    
    print(f"\nMencetak barcode:")
    print(f"  Barcode      : {barcode_value}")
    print(f"  Produk       : {product_name}")
    print(f"  Workstation  : {workstation}")
    print(f"  Debug Mode   : {'ENABLED' if debug_mode else 'DISABLED'}")
    print(f"\n  Log file     : {LOG_FILE}")
    print("")
    
    result = cetakBarcode01(barcode_value, product_name, workstation, debug=debug_mode)
    
    log_message("\n" + "="*60)
    if result:
        log_message("STATUS: BERHASIL ✅")
    else:
        log_message("STATUS: GAGAL ❌")
        log_message(f"\nCek log file untuk detail error: {LOG_FILE}")
    log_message("="*60 + "\n")
    
    print("="*60)
    if result:
        print("STATUS: BERHASIL ✅")
    else:
        print("STATUS: GAGAL ❌")
        print(f"\nUntuk melihat detail error, buka file:")
        print(f"{LOG_FILE}")
    print("="*60)
    print("\nTekan ENTER untuk menutup window ini...")
    
    try:
        input()
    except:
        pass
