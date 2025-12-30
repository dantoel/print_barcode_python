import sys
import os
from ctypes import *
from time import sleep
import traceback

def cetakBarcode01(id1, nama, ws, debug=False):
    """
    Fungsi cetak barcode dengan debug mode
    
    Args:
        id1: Barcode value
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
            print("\n" + "="*50)
            print("DEBUG MODE: ON")
            print("="*50)
            print(f"[1] Input validation:")
            print(f"    - Barcode: {barcode}")
            print(f"    - Nama: {name}")
            print(f"    - Workstation: {ws1}")
        
        # Step 1: Check DLL file exists
        dll_path = r"C:\ws\KodeArduinoUtama\printer02\Msprintsdk.dll"
        if debug:
            print(f"\n[2] Checking DLL file:")
            print(f"    - Path: {dll_path}")
            print(f"    - Exists: {os.path.exists(dll_path)}")
            if not os.path.exists(dll_path):
                print(f"    ⚠️  WARNING: DLL file not found!")
        
        # Step 2: Load DLL
        if debug:
            print(f"\n[3] Loading DLL...")
        
        try:
            mydll = cdll.LoadLibrary(dll_path)
            if debug:
                print(f"    ✓ DLL loaded successfully")
        except OSError as dll_error:
            print(f"    ✗ FAILED to load DLL: {dll_error}")
            print(f"    Common causes:")
            print(f"    - DLL file not found at {dll_path}")
            print(f"    - Missing Microsoft Visual C++ Runtime")
            print(f"    - 32-bit vs 64-bit Python mismatch")
            return False
        
        # Step 3: Printer initialization
        if debug:
            print(f"\n[4] Initializing printer...")
        
        try:
            setting = mydll.SetUsbportauto()
            if debug:
                print(f"    - SetUsbportauto() returned: {setting}")
            
            setting2 = mydll.SetInit()
            if debug:
                print(f"    - SetInit() returned: {setting2}")
            
            mydll.SetClean()
            if debug:
                print(f"    - SetClean() executed")
            
            mydll.SetAlignment(2)
            mydll.SetSizechar(2, 2, 0, 0)
            
            status = mydll.GetStatus()
            if debug:
                print(f"    - Printer Status: {status}")
            
        except AttributeError as attr_error:
            print(f"    ✗ FAILED: Printer function not found: {attr_error}")
            print(f"    - Check if DLL is correct version")
            return False
        
        # Step 4: Prepare strings for printing
        if debug:
            print(f"\n[5] Preparing print strings...")
        
        string1 = barcode
        string2 = name
        string3 = " " + ws1
        
        try:
            b_string1 = string1.encode('utf-8')
            b_string2 = string2.encode('utf-8')
            b_string3 = string3.encode('utf-8')
            
            if debug:
                print(f"    - Barcode (encoded): {b_string1}")
                print(f"    - Product Name (encoded): {b_string2}")
                print(f"    - Workstation (encoded): {b_string3}")
        
        except UnicodeEncodeError as encode_error:
            print(f"    ✗ FAILED: String encoding error: {encode_error}")
            return False
        
        # Step 5: Print operations
        if debug:
            print(f"\n[6] Executing print commands...")
        
        try:
            mydll.SetAlignment(1)
            mydll.SetSizetext(0, 0)
            mydll.PrintString(b_string3, 0)
            if debug:
                print(f"    - PrintString(workstation) executed")
            
            mydll.PrintChargeRow()
            
            mydll.SetSizetext(1, 2)
            mydll.PrintString(b_string2, 0)
            if debug:
                print(f"    - PrintString(product name) executed")
            
            barcode_result = mydll.Print1Dbar(2, 60, 1, 2, 4, b_string1)
            if debug:
                print(f"    - Print1Dbar(barcode) returned: {barcode_result}")
            
            mydll.PrintChargeRow()
            mydll.PrintChargeRow()
            mydll.PrintChargeRow()
            mydll.PrintChargeRow()
            mydll.PrintChargeRow()
            
            mydll.PrintCutpaper(1)
            if debug:
                print(f"    - PrintCutpaper() executed")
            
            mydll.SetClose()
            if debug:
                print(f"    - SetClose() executed")
        
        except Exception as print_error:
            print(f"    ✗ FAILED during print operation: {print_error}")
            return False
        
        sleep(2)
        print("\n✓ Cetak barcode BERHASIL!")
        
        if debug:
            print("="*50)
            print("DEBUG MODE: Completed successfully")
            print("="*50 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR (Unexpected): {e}")
        print(f"\nFull traceback:")
        traceback.print_exc()
        print(f"\nGagal cetak barcode")
        return False

if __name__ == "__main__":
    # Contoh penggunaan:
    # python cetak_manual.py "686A18101-11" "Nama Produk" "WS01"
    # python cetak_manual.py "686A18101-11" "Nama Produk" "WS01" --debug
    
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
        # Input manual jika tidak ada argument
        print("\n" + "="*50)
        print("MANUAL BARCODE PRINTING")
        print("="*50)
        
        barcode_value = input("Masukkan barcode value (default: 686A18101-11): ") or "686A18101-11"
        product_name = input("Masukkan nama produk (default: Produk): ") or "Produk"
        workstation = input("Masukkan workstation (default: WS01): ") or "WS01"
        debug_input = input("Enable debug mode? (y/n, default: n): ").lower() or "n"
        debug_mode = debug_input == "y"
    
    print(f"\nMencetak barcode:")
    print(f"  Barcode      : {barcode_value}")
    print(f"  Produk       : {product_name}")
    print(f"  Workstation  : {workstation}")
    print(f"  Debug Mode   : {'ENABLED' if debug_mode else 'DISABLED'}")
    
    cetakBarcode01(barcode_value, product_name, workstation, debug=debug_mode)
