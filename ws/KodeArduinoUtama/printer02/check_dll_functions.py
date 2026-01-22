"""
Script untuk melihat semua fungsi yang tersedia di Msprintsdk.dll
"""
import ctypes
import os

dll_path = r"C:\ws\KodeArduinoUtama\printer02\Msprintsdk.dll"

print("="*70)
print("CHECKING DLL FUNCTIONS")
print("="*70)
print(f"\nDLL Path: {dll_path}")
print(f"Exists: {os.path.exists(dll_path)}")

if not os.path.exists(dll_path):
    # Try alternative path
    dll_path = os.path.join(os.path.dirname(__file__), "Msprintsdk.dll")
    print(f"\nTrying alternative: {dll_path}")
    print(f"Exists: {os.path.exists(dll_path)}")

if os.path.exists(dll_path):
    print("\n" + "="*70)
    print("LOADING DLL...")
    print("="*70)
    
    try:
        mydll = ctypes.cdll.LoadLibrary(dll_path)
        print("✓ DLL loaded successfully!")
        
        print("\n" + "="*70)
        print("TESTING QR CODE / 2D BARCODE FUNCTIONS:")
        print("="*70)
        
        # List of possible QR code function names
        qr_functions = [
            "Print2Dbar",
            "Print2DBar",
            "PrintQRcode",
            "PrintQRCode",
            "PrintQR",
            "Print2D",
            "PrintBarcode2D",
            "Print2DBarcode",
            "PrintQRbar",
            "PrintQRBar",
            "SetQRcode",
            "SetQRCode",
        ]
        
        print("\nChecking which functions exist:\n")
        found_functions = []
        
        for func_name in qr_functions:
            try:
                func = getattr(mydll, func_name)
                print(f"  ✓ {func_name} - FOUND!")
                found_functions.append(func_name)
            except AttributeError:
                print(f"  ✗ {func_name} - Not found")
        
        print("\n" + "="*70)
        print("SUMMARY:")
        print("="*70)
        
        if found_functions:
            print(f"\n✓ Found {len(found_functions)} QR code function(s):")
            for func in found_functions:
                print(f"  - {func}")
        else:
            print("\n✗ No QR code functions found!")
            print("\nPossible reasons:")
            print("  1. Printer DLL does not support QR code")
            print("  2. Function names are different")
            print("  3. QR code requires additional setup")
            
        print("\n" + "="*70)
        print("TESTING 1D BARCODE (for comparison):")
        print("="*70)
        
        try:
            func = getattr(mydll, "Print1Dbar")
            print("  ✓ Print1Dbar - FOUND (1D Barcode works)")
        except AttributeError:
            print("  ✗ Print1Dbar - Not found")
            
    except Exception as e:
        print(f"\n✗ Error loading DLL: {e}")
else:
    print("\n✗ DLL file not found!")

print("\n" + "="*70)
print("Press ENTER to close...")
input()
