════════════════════════════════════════════════════════════════════════════════
                            MULAI DI SINI ⭐
════════════════════════════════════════════════════════════════════════════════

🎯 TUJUAN SISTEM:
   Mencetak barcode otomatis dari database production_schedule
   dengan status 'Ready'

📍 DATABASE:
   Host: 192.168.12.250
   User: admin-reka
   Tabel: production_schedule
   Status: WHERE production_proggress = 'Ready'

════════════════════════════════════════════════════════════════════════════════

🚀 CARA TERMUDAH:

   👉 Double-click file: MENU_UTAMA.bat

   Anda akan mendapat menu:
   [1] Print semua data
   [2] Test print (limit)
   [3] Debug mode
   [4] Test database
   [5] Lihat log

════════════════════════════════════════════════════════════════════════════════

⚡ QUICK START (5 langkah):

   1️⃣  Double-click: TEST_DATABASE.bat
       Tunggu hasil "✓ SEMUA TEST BERHASIL"

   2️⃣  Double-click: MENU_UTAMA.bat
       Pilih opsi [2] (TEST PRINT)

   3️⃣  Pilih jumlah: 1 (test satu item dulu)
       Lihat barcode keluar dari printer

   4️⃣  Jika OK, jalankan lagi MENU_UTAMA.bat
       Pilih opsi [1] (PRINT SEMUA DATA)

   5️⃣  Konfirmasi dengan "Y" saat diminta
       Biarkan berjalan sampai selesai

════════════════════════════════════════════════════════════════════════════════

📋 DATA YANG AKAN DICETAK (dari database):

   Format setiap barcode:
   ┌──────────────────────┐
   │     Workstation      │ ← Workshop
   │    Product Name      │ ← Nama Produk
   │ [======BARCODE=====] │ ← ID Product (1D Barcode)
   └──────────────────────┘

   Contoh dari data Anda:
   ┌──────────────────────┐
   │        WS01          │
   │  Distribusi K1/K3    │
   │ [===686A18101-11===] │
   └──────────────────────┘

════════════════════════════════════════════════════════════════════════════════

🛠️  JIKA ADA ERROR:

   ❌ Script tutup langsung?
      → Gunakan .bat file (sudah disediakan)

   ❌ "Database connection failed"?
      → Double-click TEST_DATABASE.bat

   ❌ "Printer not found"?
      → Cek printer terhubung USB
      → Jalankan DEBUG_CETAK.bat

   ❌ Tidak tahu apa yang salah?
      → Lihat file cetak_log.txt
      → atau jalankan DEBUG_CETAK.bat

════════════════════════════════════════════════════════════════════════════════

📂 FILE-FILE TERSEDIA:

   🔴 PENTING (start dari sini):
   - MENU_UTAMA.bat              ← Menu utama
   - TEST_DATABASE.bat           ← Test database
   - PANDUAN_CEPAT.txt           ← Panduan singkat

   🟡 UNTUK TESTING:
   - TEST_PRINT.bat              ← Test dengan limit
   - DEBUG_CETAK.bat             ← Debug mode

   🟢 UNTUK REFERENSI:
   - README_CETAK_DATABASE.md    ← Detail guide
   - DOKUMENTASI_LENGKAP.txt     ← Technical doc
   - FILE_SUMMARY.txt            ← File list

════════════════════════════════════════════════════════════════════════════════

✅ PRE-CHECK SEBELUM MULAI:

   ☐ Printer thermal terhubung dan hidup
   ☐ Kertas barcode ada di printer
   ☐ Komputer terhubung ke jaringan
   ☐ Database server 192.168.12.250 accessible

════════════════════════════════════════════════════════════════════════════════

💡 TIPS:

   ✓ Selalu TEST PRINT dulu sebelum cetak semua
   ✓ Cek VIEW_LOG.bat untuk melihat history
   ✓ Gunakan DEBUG_CETAK.bat jika ada error
   ✓ Simpan cetak_log.txt untuk audit trail

════════════════════════════════════════════════════════════════════════════════

Siap? Mari kita mulai!

👉 Double-click MENU_UTAMA.bat

════════════════════════════════════════════════════════════════════════════════
