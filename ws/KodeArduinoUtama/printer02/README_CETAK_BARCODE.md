# PANDUAN CETAK BARCODE MANUAL

## Cara Menggunakan di Komputer Client

### Opsi 1: Double-Click File Batch (Paling Mudah)
1. Buka folder: `printer02`
2. Double-click file: **`CETAK_BARCODE.bat`**
3. Program akan otomatis membuka command window
4. Masukkan barcode value, nama produk, dan workstation
5. Tekan ENTER untuk cetak
6. Window akan ditutup setelah selesai

### Opsi 2: Double-Click File Python
1. Buka folder: `printer02`
2. Double-click file: **`cetak_manual.py`**
3. Masukkan input sesuai prompt
4. Tekan ENTER untuk cetak

### Opsi 3: Run via Command Line
```cmd
cd C:\ws\KodeArduinoUtama\printer02
python cetak_manual.py
```

Atau dengan parameter:
```cmd
python cetak_manual.py "686A18101-11" "Nama Produk" "WS01"
```

Debug mode:
```cmd
python cetak_manual.py "686A18101-11" "Nama Produk" "WS01" --debug
```

---

## Debugging Jika Ada Error

### File Log Otomatis
Setiap kali script dijalankan, log tersimpan otomatis di:
```
cetak_barcode_log.txt
```

Buka file ini dengan Notepad untuk melihat detail error.

### Error Umum & Solusi

#### 1. "DLL file not found"
**Penyebab:** File `Msprintsdk.dll` tidak ada di folder

**Solusi:**
- Pastikan file `Msprintsdk.dll` ada di folder `printer02`
- Jika tidak ada, copy dari folder lain yang memilikinya

#### 2. "Could not find module"
**Penyebab:** Path DLL salah atau library dependencies tidak lengkap

**Solusi:**
- Install Microsoft Visual C++ Redistributable
  - Download dari: https://support.microsoft.com/en-us/help/2977003
  - Install versi yang sesuai (x86 atau x64)

#### 3. "Printer function not found"
**Penyebab:** DLL versi salah atau tidak kompatibel

**Solusi:**
- Verifikasi DLL dengan vendor printer
- Pastikan DLL untuk printer MStar (atau printer yang Anda gunakan)

#### 4. Script berjalan tapi printer tidak cetak
**Penyebab:** USB printer tidak terhubung atau driver tidak terinstall

**Solusi:**
- Check Device Manager, printer harus terdeteksi
- Install driver printer dari CD atau website vendor
- Restart komputer setelah install driver

---

## Struktur Parameter

### Input 1: Barcode Value
Contoh: `686A18101-11`
- Nilai yang akan ditampilkan sebagai barcode
- Format bisa sesuai kebutuhan

### Input 2: Nama Produk
Contoh: `Produk ABC`
- Nama yang ditampilkan di label
- Bisa nama material atau nama produk jadi

### Input 3: Workstation
Contoh: `WS01`
- Kode workstation/mesin
- Ditampilkan di label untuk identifikasi lokasi cetak

---

## Troubleshooting Advanced

### Jika log file terlalu besar (>10MB)
- Script akan otomatis menghapus dan membuat log baru
- Tidak perlu tindakan manual

### Jika tetap error setelah semua langkah
1. Buka `cetak_barcode_log.txt`
2. Copy seluruh isi file
3. Kirimkan ke IT support dengan informasi:
   - Windows version
   - Python version (jalankan: `python --version`)
   - Printer model
   - Error message dari log file

---

## Testing Quick Start

### Test 1: Check Python
Buka Command Prompt dan ketik:
```cmd
python --version
```
Harus menunjukkan versi Python (contoh: Python 3.9.0)

### Test 2: Check DLL
Buka Command Prompt dan ketik:
```cmd
cd C:\ws\KodeArduinoUtama\printer02
dir Msprintsdk.dll
```
Harus menampilkan file `Msprintsdk.dll`

### Test 3: Run Debug Mode
```cmd
cd C:\ws\KodeArduinoUtama\printer02
python cetak_manual.py "TEST123" "Test Product" "WS01" --debug
```
Lihat detail output untuk debugging

---

## Info File

| File | Fungsi |
|------|--------|
| `cetak_manual.py` | Script utama (Python) |
| `CETAK_BARCODE.bat` | Launcher batch (double-click) |
| `cetak_barcode_log.txt` | Log file otomatis |
| `Msprintsdk.dll` | Driver printer (harus ada) |

---

**Dibuat**: 30 Desember 2025  
**Versi**: 1.0  
**Support**: Contact IT Team
