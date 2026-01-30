# 🚀 QUICK START - MQTT Cloud Barcode Printer

## ✅ Setup Selesai!

Broker cloud **GRATIS** dari HiveMQ sudah dikonfigurasi:
- **Broker**: `broker.hivemq.com`
- **Port**: `1883`
- **Status**: ✅ Tested & Working

---

## 📋 Cara Menggunakan (3 Langkah)

### 1️⃣ Di PC PRINTER (192.168.14.210)

**Jalankan service:**
```
Double-click: RUN_CLOUD_PRINTER.bat
```

Atau via terminal:
```powershell
cd "d:\Kode Program\print_barcode_python\ws\KodeArduinoUtama\printer02"
python mqtt_cloud_printer.py
```

**Pastikan muncul:**
```
✅ Connected to MQTT: broker.hivemq.com:1883
   Subscribed to: printer/barcode/print
✅ SERVICE RUNNING
```

---

### 2️⃣ Di PC NODE-RED (subnet berbeda - OK!)

**Import flow:**
1. Buka Node-RED: `http://localhost:1880`
2. Menu → Import → Clipboard
3. Copy isi file: `node_red_flow_mqtt_printer.json`
4. Paste & Import
5. **Deploy**

**Flow sudah include:**
- MQTT Broker config → `broker.hivemq.com:1883`
- Test Barcode inject button
- Status monitoring
- Command buttons

---

### 3️⃣ TEST!

Di Node-RED, klik button **"Test Barcode"**

Akan kirim JSON:
```json
{
  "barcode": "SKU-2026-001",
  "product": "Motor Pump",
  "line": "Line 1"
}
```

**Di PC Printer, akan muncul:**
```
📩 Message from: printer/barcode/print
   Payload: {'barcode': 'SKU-2026-001', ...}
✅ Print SUCCESS - Barcode: SKU-2026-001
```

**Di Node-RED Debug panel:**
```json
{
  "status": "success",
  "message": "Barcode 'SKU-2026-001' berhasil dicetak",
  "timestamp": "2026-01-29T...",
  "printer_ready": true
}
```

---

## 📡 Format Data dari Node-RED

**Topic:** `printer/barcode/print`

**Payload (JSON):**
```json
{
  "barcode": "BARCODE-123",      ← WAJIB
  "product": "Nama Produk",      ← Opsional
  "line": "Line 1"               ← Opsional
}
```

**Minimal:**
```json
{
  "barcode": "12345"
}
```

---

## 🎯 Topics MQTT

| Topic | Tipe | Fungsi |
|-------|------|--------|
| `printer/barcode/print` | Subscribe | Terima request cetak |
| `printer/barcode/status` | Publish | Kirim status printer |
| `printer/barcode/command` | Subscribe | Terima command |

---

## 🔧 Commands

**Cek status printer:**
```json
{"command": "status"}
```

**Reinit printer:**
```json
{"command": "init"}
```

**Stop service:**
```json
{"command": "stop"}
```

---

## ⚠️ Troubleshoot

### Service tidak connect
```
❌ Pastikan PC printer ada koneksi INTERNET
✅ Test dengan: python test_cloud_connection.py
```

### Node-RED tidak connect
```
❌ Pastikan PC Node-RED ada koneksi INTERNET
✅ Cek broker config di Node-RED: broker.hivemq.com:1883
```

### Printer tidak cetak
```
✅ Cek log: C:\KodeArduinoUtama\printer02\mqtt_printer.log
✅ Pastikan DLL path benar
✅ Pastikan USB printer connected
```

---

## 📊 Arsitektur

```
[Node-RED PC]
    ↓ (Internet)
    ↓
[broker.hivemq.com] ← Cloud MQTT Broker (GRATIS)
    ↓ (Internet)
    ↓
[Printer PC]
    → Cetak barcode via DLL
```

**✅ Keuntungan:**
- ✅ Tidak perlu setting IP/subnet
- ✅ Kedua PC bisa di network berbeda
- ✅ 100% GRATIS
- ✅ Tidak perlu install Mosquitto
- ✅ Ready to use!

---

## 📝 Files

| File | Fungsi |
|------|--------|
| `mqtt_config.ini` | Config (sudah set ke cloud) |
| `mqtt_cloud_printer.py` | Service printer |
| `RUN_CLOUD_PRINTER.bat` | Launcher |
| `node_red_flow_mqtt_printer.json` | Flow Node-RED |
| `test_cloud_connection.py` | Test koneksi |

---

## 🎉 Ready to Use!

1. ✅ Konfigurasi cloud broker sudah set
2. ✅ Test koneksi berhasil
3. ✅ Flow Node-RED ready
4. ✅ Script Python ready

**Sekarang tinggal:**
1. Jalankan `RUN_CLOUD_PRINTER.bat` di PC printer
2. Import flow di Node-RED
3. Deploy & Test!

---

**Selamat mencoba! 🚀**

Jika ada masalah, cek log file atau contact support.
