# 📋 CETAK BARCODE DARI DATABASE - Panduan Lengkap

## 🎯 Fitur

- ✅ Koneksi otomatis ke database MySQL
- ✅ Query otomatis data dengan status "Ready" 
- ✅ Print barcode otomatis dengan ID produk dan nama produk
- ✅ Logging lengkap untuk debugging
- ✅ User-friendly dengan konfirmasi sebelum print
- ✅ Error handling yang detail

## 📋 Konfigurasi Database

**Host:** `192.168.12.250`
**User:** `admin-reka`
**Password:** `J@debx132`
**Database:** `reka`
**Tabel:** `production_schedule`

**Query yang dijalankan:**
```sql
SELECT id_product, product, line 
FROM production_schedule 
WHERE production_proggress = 'Ready'
ORDER BY id_product ASC
```

## 📁 File-File yang Dibuat

```
C:\ws\KodeArduinoUtama\printer02\
│
├── 🐍 cetak_dari_database.py          ← Main script (Python)
│
├── 🔧 Batch Files untuk kemudahan:
│   ├── CETAK_DARI_DATABASE.bat        ← Cetak semua data Ready
│   ├── TEST_PRINT.bat                 ← Test dengan limit item
│   ├── DEBUG_CETAK.bat                ← Debug mode dengan verbose
│   ├── TEST_DATABASE.bat              ← Test koneksi database
│   └── VIEW_LOG.bat                   ← Lihat log file
│
├── 📝 Script Python Pendukung:
│   └── test_database_connection.py    ← Test koneksi DB
│
├── ⚙️ Konfigurasi:
│   └── config.ini                     ← File konfigurasi (opsional)
│
└── 📊 Log:
    └── cetak_log.txt                  ← Semua history print
```

## 🚀 Cara Menggunakan

### Opsi 1: Simple Print (Recommended untuk User)
**Double-click:** `CETAK_DARI_DATABASE.bat`

Proses:
1. Koneksi ke database
2. Query semua data dengan status "Ready"
3. Tampilkan daftar data yang akan dicetak
4. Minta konfirmasi user
5. Print semua item
6. Tampilkan summary

### Opsi 2: Test Print (Limit Tertentu)
**Double-click:** `TEST_PRINT.bat`

Pilih jumlah item:
- Test (1 item)
- Small batch (5 item)
- Full batch (semua item)

### Opsi 3: Debug Mode (Jika Ada Error)
**Double-click:** `DEBUG_CETAK.bat`

Output detail setiap step:
- Koneksi database
- Query execution
- DLL loading
- Printer initialization
- Print commands

### Opsi 4: Test Database Connection
**Double-click:** `TEST_DATABASE.bat`

Cek:
- Koneksi ke database
- Query ke tabel
- Lihat data yang Ready

### Opsi 5: Lihat Log File
**Double-click:** `VIEW_LOG.bat`

Tampilkan semua history print dalam file `cetak_log.txt`

## 💻 Command Line Usage (Advanced)

Buka PowerShell/CMD dan jalankan:

```bash
cd C:\ws\KodeArduinoUtama\printer02

# Normal print
python cetak_dari_database.py

# Debug mode
python cetak_dari_database.py --debug

# Limit 5 item
python cetak_dari_database.py --limit 5

# Debug mode dengan limit
python cetak_dari_database.py --debug --limit 3
```

## 🔧 Troubleshooting

### Error: "DLL file tidak ditemukan"
- Pastikan file `Msprintsdk.dll` ada di folder `C:\ws\KodeArduinoUtama\printer02\`

### Error: "Koneksi database gagal"
**Solution:**
1. Jalankan `TEST_DATABASE.bat` untuk diagnosa
2. Cek konfigurasi di `config.ini`
3. Cek koneksi network ke `192.168.12.250`
4. Pastikan credentials benar: `admin-reka` / `J@debx132`

### Error: "Printer tidak ditemukan"
- Pastikan printer thermal terhubung via USB
- Jalankan `DEBUG_CETAK.bat` untuk lihat detail error
- Cek status printer di Device Manager

### Script langsung menutup tanpa pesan
- Jalankan via batch file (`.bat`) bukan langsung Python
- Atau gunakan Python di Command Prompt untuk melihat error

## 📊 Format Data yang Dicetak

Setiap label barcode berisi:

```
┌──────────────────────┐
│    [WORKSTATION]     │
│     [PRODUCT]        │
│  ┌──────────────────┐│
│  │ 686A18101-11     ││  ← Barcode
│  │ (1D Barcode)     ││
│  └──────────────────┘│
└──────────────────────┘
```

Contoh dengan data dari screenshot:
```
        WS01
    Distribusi K1/K3
  ┌──────────────────┐
  │ 686A18101-11     │
  │ (1D Barcode)     │
  └──────────────────┘
```

## 📝 Log File

Semua aktivitas dicatat di: `C:\ws\KodeArduinoUtama\printer02\cetak_log.txt`

Contoh isi log:
```
[2026-01-02 10:15:30] ========== STARTING PRINT FROM DATABASE ==========
[2026-01-02 10:15:30] ✓ Koneksi database berhasil
[2026-01-02 10:15:31] ✓ Query berhasil, ditemukan 3 data siap cetak
[2026-01-02 10:15:32] ✓ Cetak BERHASIL: 686A18101-11 - Distribusi K1/K3
[2026-01-02 10:15:33] ✓ Cetak BERHASIL: 506E12001 - Panel AC Endwall KCI
[2026-01-02 10:15:34] ✓ Cetak BERHASIL: 496A18001 - PIDS A
[2026-01-02 10:15:34] SUMMARY: Total=3, Berhasil=3, Gagal=0
```

## ⚙️ Konfigurasi Custom

Edit file `config.ini` jika ada perubahan:
- Database host
- Username/password
- Nama tabel
- Nama kolom
- Default workshop

## 📌 Notes

- ✅ Script otomatis confirm sebelum print (prevent salah cetak)
- ✅ Bisa di-pause dengan Ctrl+C
- ✅ Auto-pause di akhir (tekan Enter untuk keluar)
- ✅ Unicode support untuk karakter Indonesia
- ✅ Semua log tersimpan untuk audit trail

## 🆘 Support

Jika ada masalah:
1. Jalankan `TEST_DATABASE.bat` → diagnosa
2. Jalankan `DEBUG_CETAK.bat` → lihat detail error
3. Cek file `cetak_log.txt` → lihat history
4. Contact developer dengan copy paste isi log file

---

**Created:** 2026-01-02  
**Database:** 192.168.12.250  
**Table:** production_schedule  
**Status Filter:** production_proggress = 'Ready'
