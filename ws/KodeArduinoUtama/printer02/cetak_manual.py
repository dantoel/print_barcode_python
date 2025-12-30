import sys
from ctypes import *
from time import sleep

def cetakBarcode01(id1, nama, ws):
    id1 = id1.strip()
    try:        
        barcode = id1
        name = nama
        ws1 = ws
        
        mydll = cdll.LoadLibrary(r"C:\ws\KodeArduinoUtama\printer02\Msprintsdk.dll")
        print('Connecting to printer...')
        setting = mydll.SetUsbportauto()
        print(f'USB Port Setting: {setting}')
        setting2 = mydll.SetInit()
        print(f'Initialization: {setting2}')
        mydll.SetClean()
        
        mydll.SetAlignment(2)
        mydll.SetSizechar(2, 2, 0, 0)
        print(f"Printer Status: {mydll.GetStatus()}")
        
        string1 = barcode
        string2 = name
        string3 = " " + ws1
        b_string1 = string1.encode('utf-8')
        b_string2 = string2.encode('utf-8')
        b_string3 = string3.encode('utf-8')

        mydll.SetAlignment(1)
        mydll.SetSizetext(0, 0)
        mydll.PrintString(b_string3, 0)
        mydll.PrintChargeRow()
        mydll.SetSizetext(1, 2)
        mydll.PrintString(b_string2, 0)
        barcode_result = mydll.Print1Dbar(2, 60, 1, 2, 4, b_string1)
        print(f'Barcode Print Result: {barcode_result}')
        mydll.PrintChargeRow()
        mydll.PrintChargeRow()
        mydll.PrintChargeRow()
        mydll.PrintChargeRow()
        mydll.PrintChargeRow()
        mydll.PrintCutpaper(1)
        mydll.SetClose()
        
        sleep(2)
        print("✓ Cetak barcode BERHASIL!")
        return True
        
    except Exception as e:
        print(f"✗ ERROR: {e}")
        print("Gagal cetak barcode")
        return False

if __name__ == "__main__":
    # Contoh penggunaan:
    # python cetak_manual.py "686A18101-11" "Nama Produk" "WS01"
    
    if len(sys.argv) > 1:
        barcode_value = sys.argv[1]
        product_name = sys.argv[2] if len(sys.argv) > 2 else "Produk"
        workstation = sys.argv[3] if len(sys.argv) > 3 else "WS01"
    else:
        # Input manual jika tidak ada argument
        barcode_value = input("Masukkan barcode value (default: 686A18101-11): ") or "686A18101-11"
        product_name = input("Masukkan nama produk (default: Produk): ") or "Produk"
        workstation = input("Masukkan workstation (default: WS01): ") or "WS01"
    
    print(f"\nMencetak barcode:")
    print(f"  Barcode  : {barcode_value}")
    print(f"  Produk   : {product_name}")
    print(f"  Workstation: {workstation}\n")
    
    cetakBarcode01(barcode_value, product_name, workstation)
