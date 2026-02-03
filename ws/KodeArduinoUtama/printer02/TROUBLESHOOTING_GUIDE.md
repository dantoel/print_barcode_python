# PRINTER TROUBLESHOOTING GUIDE

## Quick Diagnosis

### ✅ Langkah 1: Jalankan Diagnostic
```batch
RUN_DIAGNOSTIC.bat
```

Ini akan test semua aspek printer dan memberikan rekomendasi spesifik.

---

## Common Issues & Solutions

### ❌ Issue: "Printer tidak terdeteksi" atau "Connection failed"

**Cek:**
1. Kabel USB printer terhubung ke komputer?
   ```powershell
   # Di Windows, buka Device Manager (devmgmt.msc)
   # Cari "Ports (COM & LPT)" - printer harus ada
   ```

2. Printer hidup?
   - Lihat lampu power di printer

3. Driver printer ter-install?
   ```powershell
   # Buka Device Manager
   # Jika ada "Unknown Device" dengan tanda tanya
   # Right-click > Update driver > Browse computer
   ```

4. Cek di diagnostic: TEST 4 & TEST 7

**Solusi:**
- Install driver printer dari CD atau website
- Cabut kabel USB, tunggu 5 detik, pasang lagi
- Restart komputer
- Restart printer

---

### ❌ Issue: "DLL tidak ditemukan"

**Error Message:**
```
✗ DLL TIDAK ditemukan!
```

**Penyebab:** Path DLL salah di `mqtt_config.ini`

**Solusi:**
1. Buka `mqtt_config.ini` dengan Notepad
2. Cari baris:
   ```ini
   [PRINTER]
   DLL_PATH=C:\KodeArduinoUtama\printer02\Msprintsdk.dll
   ```
3. Ubah path ke lokasi file `Msprintsdk.dll` yang benar
4. Save file
5. Jalankan diagnostic lagi

**Cara cari file:**
```powershell
# Buka PowerShell
Get-ChildItem -Path "C:\" -Recurse -Filter "Msprintsdk.dll" 2>$null
```

---

### ❌ Issue: "DLL gagal di-load"

**Error Message:**
```
✗ Gagal load DLL: ...
```

**Penyebab:** Missing Visual C++ Runtime atau DLL corrupted

**Solusi:**
1. Install Visual C++ Runtime:
   - Download: https://support.microsoft.com/en-us/help/2977003/
   - Pilih yang sesuai: x86 atau x64
   - Run installer
   - Restart komputer

2. Atau, copy DLL dari komputer yang sukses:
   - Dari komputer A (yang bisa print): Copy `Msprintsdk.dll`
   - Ke komputer B: Paste ke folder yang sama

---

### ❌ Issue: "OpenPrinter gagal" atau "Printer not ready"

**Error Message:**
```
✗ Printer tidak terbuka (OpenPrinter = 1)
```

**Penyebab:** Printer tidak connected, tidak hidup, atau ada masalah hardware

**Cek:**
1. **USB Connection:**
   ```powershell
   # Buka Device Manager
   # Cari "USB Printing Support" atau printer model
   # Tidak boleh ada tanda seru/tanya
   ```

2. **Printer Status:**
   - Lihat panel printer, ada error?
   - Centang paper, tinta, head

3. **Power Cycle:**
   ```batch
   REM Matikan printer
   REM Tunggu 10 detik
   REM Nyalakan lagi
   ```

4. **Reboot Komputer:**
   ```batch
   shutdown /r /t 0
   ```

---

### ❌ Issue: "Print task sukses tapi tidak ada output"

**Gejala:**
```
✓ PrintBarcode result: 0 (SUCCESS)
```
Tapi barcode tidak tercetak

**Penyebab:**
1. Paper habis
2. Printer error (jam, head problem)
3. Printer pause/offline
4. Kabel loose

**Solusi:**
1. Buka printer panel:
   - Cek kertas
   - Cek tinta/ribbon
   - Cek ada kertas masuk?

2. Lihat error di printer:
   - Banyak printer punya LCD/LED status
   - Baca manual printer untuk error code

3. Clear paper jam:
   - Buka printer
   - Keluarkan kertas yang tersangkut
   - Tutup lagi

4. Clean printer head:
   - Di beberapa printer ada menu "Maintenance" atau "Clean"
   - Jalankan cleaning cycle

5. Test dengan Windows Print:
   ```powershell
   # Buka Devices and Printers
   # Right-click printer > Print test page
   ```

---

### ❌ Issue: "MQTT connection failed"

**Error Message:**
```
✗ MQTT connection failed: ...
```

**Penyebab:** Network issue atau broker down

**Cek:**
1. Koneksi internet OK?
   ```powershell
   ping 8.8.8.8
   ping broker.hivemq.com
   ```

2. Firewall allow MQTT?
   ```powershell
   # Buka Windows Defender Firewall
   # Advanced Settings
   # Cek Inbound Rules
   ```

3. Broker address benar?
   - Buka `mqtt_config.ini`
   - Cek `BROKER_ADDRESS` dan `BROKER_PORT`
   - Default: `broker.hivemq.com:1883`

**Solusi:**
- Add firewall rule untuk port MQTT (1883)
- Cek config.ini
- Test ping broker
- Cek internet connection

---

## Advanced Troubleshooting

### 🔧 Test Printer via Command Line

```batch
REM Run Python interactive shell
python

REM Dalam Python:
from ctypes import *

REM Load DLL
dll = cdll.LoadLibrary("C:\\Path\\To\\Msprintsdk.dll")

REM Open printer
result = dll.OpenPrinter()
print(f"OpenPrinter: {result}")  # 0 = success

REM Close printer
dll.ClosePrinter()

REM Exit
exit()
```

### 🔧 Check DLL Functions

```powershell
REM Gunakan Dependency Walker
REM Download: https://www.dependencywalker.com/
REM Buka Msprintsdk.dll untuk lihat semua exported functions
```

### 🔧 View Full Error Log

```powershell
REM Buka file log
Get-Content "C:\KodeArduinoUtama\printer02\mqtt_printer.log" -Last 100

REM Atau dengan tail:
type "C:\KodeArduinoUtama\printer02\mqtt_printer.log"
```

### 🔧 Collect System Info

```batch
REM Simpan untuk debugging
echo System Information > diagnostics.txt
systeminfo >> diagnostics.txt
echo. >> diagnostics.txt
echo Network Configuration >> diagnostics.txt
ipconfig /all >> diagnostics.txt
echo. >> diagnostics.txt
echo Device List >> diagnostics.txt
wmic logicaldisk get name >> diagnostics.txt

REM Lihat hasil
notepad diagnostics.txt
```

---

## Multi-Printer Setup Issues

### ❌ Issue: Printer kedua tidak bisa print

**Cek:**
1. Setiap printer harus punya `CLIENT_ID` unik di `mqtt_config.ini`:
   ```ini
   # Komputer 1
   CLIENT_ID=barcode_printer_01
   
   # Komputer 2
   CLIENT_ID=barcode_printer_02
   ```

2. Setiap printer harus punya `DLL_PATH` sesuai lokasi:
   ```ini
   # Komputer 1 (D drive)
   DLL_PATH=D:\printer02\Msprintsdk.dll
   
   # Komputer 2 (C drive)
   DLL_PATH=C:\MyPrinterService\Msprintsdk.dll
   ```

3. Test diagnostic di setiap komputer:
   ```batch
   RUN_DIAGNOSTIC.bat
   ```

---

## Performance Troubleshooting

### ⚠️ Issue: Queue piling up (data menumpuk)

**Gejala:**
- Pending items terus bertambah
- Print lambat

**Cek:**
```powershell
REM Buka database queue
cd "C:\KodeArduinoUtama\printer02"
sqlite3 print_queue.db "SELECT COUNT(*) FROM print_queue WHERE status='pending';"

REM Lihat detail
sqlite3 print_queue.db "SELECT id, barcode, status, attempted_count FROM print_queue LIMIT 10;"
```

**Solusi:**
1. Printer speed setting:
   - Beberapa printer punya setting "Fast", "Normal", "Quality"
   - Ubah ke "Fast" untuk throughput lebih tinggi

2. Cek printer tidak error:
   ```batch
   RUN_DIAGNOSTIC.bat
   ```

3. Clear failed items:
   ```powershell
   sqlite3 print_queue.db "DELETE FROM print_queue WHERE status='failed' AND attempted_count >= 5;"
   ```

---

## Contact & Support

Jika diagnostic tidak bisa resolve, share:
1. Output dari `RUN_DIAGNOSTIC.bat`
2. File log: `mqtt_printer.log`
3. File config: `mqtt_config.ini` (tanpa password/key)
4. Printer model
5. Windows version

---

**Last Updated:** 2026-02-03
