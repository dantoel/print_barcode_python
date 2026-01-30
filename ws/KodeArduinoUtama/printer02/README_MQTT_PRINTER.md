# MQTT Barcode Printer - Dokumentasi Setup

## 📋 Daftar File Baru

```
✓ mqtt_config.ini                  - File konfigurasi (EDIT INI!)
✓ mqtt_printer_service.py          - Script service utama (JANGAN EDIT)
✓ RUN_MQTT_SERVICE.bat             - Launcher batch (DOUBLE-CLICK INI)
✓ SETUP_MQTT_NODERED.md            - Panduan setup MQTT & Node-RED
✓ README_MQTT_PRINTER.md           - Dokumentasi (FILE INI)
```

---

## 🚀 Quick Start (3 Langkah)

### Step 1: Install MQTT Broker
Baca file: `SETUP_MQTT_NODERED.md`

Pilih salah satu:
- **Opsi 1** (Recommended): Install Mosquitto lokal
- **Opsi 2**: Gunakan public MQTT broker (test.mosquitto.org)
- **Opsi 3**: Docker

### Step 2: Edit Konfigurasi
Edit file: `mqtt_config.ini`

```ini
[MQTT]
BROKER_ADDRESS=192.168.1.100    ← Ganti dengan IP Anda!
BROKER_PORT=1883
```

### Step 3: Jalankan Service
Double-click: `RUN_MQTT_SERVICE.bat`

---

## 📝 Konfigurasi Detail

### A. MQTT Configuration

```ini
[MQTT]
# IP atau hostname MQTT broker Anda
BROKER_ADDRESS=localhost

# Port MQTT (default 1883)
BROKER_PORT=1883

# ID untuk koneksi MQTT
CLIENT_ID=barcode_printer_01

# Keep-alive interval
KEEPALIVE=60

# Topic untuk terima data barcode dari Node-RED
TOPIC_BARCODE_INPUT=printer/barcode/print

# Topic untuk kirim status printer
TOPIC_STATUS_OUTPUT=printer/barcode/status

# Topic untuk perintah/command
TOPIC_COMMAND=printer/barcode/command
```

### B. Printer Configuration

```ini
[PRINTER]
# Path ke DLL printer
DLL_PATH=C:\KodeArduinoUtama\printer02\Msprintsdk.dll

# Alignment: 0=left, 1=center, 2=right
ALIGNMENT=1

# Font size
FONT_WIDTH=2
FONT_HEIGHT=2

# Enable/disable komponen cetak
ENABLE_BARCODE=1
ENABLE_PRODUCT_NAME=1
ENABLE_LINE_NAME=1

# Jumlah kertas feed setelah print
PAPER_FEED=2
```

### C. Logging Configuration

```ini
[LOGGING]
# Path log file
LOG_FILE=C:\KodeArduinoUtama\printer02\mqtt_printer.log

# Log level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO

# Maksimal log file size (bytes)
LOG_MAX_SIZE=1048576

# Jumlah backup log files
LOG_BACKUP_COUNT=5
```

---

## 📡 MQTT Integration dengan Node-RED

### Konfigurasi MQTT di Node-RED

1. **MQTT-Broker Node:**
   - Server: `192.168.1.100` (IP Anda)
   - Port: `1883`
   - Client ID: `node-red-client`

2. **MQTT-Out Node untuk Cetak:**
   - Topic: `printer/barcode/print`
   - Payload: JSON (lihat format di bawah)

3. **MQTT-In Node untuk Status:**
   - Topic: `printer/barcode/status`
   - Output: Parsed object

### Format Payload dari Node-RED

**Untuk mencetak barcode:**
```json
{
  "barcode": "SKU-2026-001",
  "product": "Motor Pump",
  "line": "Line 1"
}
```

**Fields:**
- `barcode` (string, **WAJIB**) - Data barcode/QR code
- `product` (string, optional) - Nama produk
- `line` (string, optional) - Nama line/workstation

**Contoh Payload Minimal:**
```json
{
  "barcode": "12345"
}
```

---

## 🔧 Command dari Node-RED

Kirim ke topic `printer/barcode/command`:

### 1. Status Check
```json
{
  "command": "status"
}
```
Response: Status printer (ready/not_ready)

### 2. Reinit Printer
```json
{
  "command": "init"
}
```
Response: Success atau error

### 3. Stop Service
```json
{
  "command": "stop"
}
```
Service akan dihentikan

---

## 📊 Response/Status dari Printer

Topic: `printer/barcode/status`

### Success Response
```json
{
  "status": "success",
  "message": "Barcode 'SKU-001' berhasil dicetak",
  "timestamp": "2026-01-29T10:30:45.123456",
  "printer_ready": true
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Barcode kosong dalam payload",
  "timestamp": "2026-01-29T10:30:45.123456",
  "printer_ready": false
}
```

### Status Response
```json
{
  "status": "online",
  "message": "Printer ready",
  "timestamp": "2026-01-29T10:30:45.123456",
  "printer_ready": true
}
```

---

## 🐛 Troubleshoot

### Service tidak connect ke MQTT

**Cek 1: MQTT Broker running?**
```powershell
# Jika pakai Mosquitto
Get-Service mosquitto | Format-List

# Atau ping MQTT IP
ping 192.168.1.100
```

**Cek 2: IP dan Port benar?**
```ini
BROKER_ADDRESS=192.168.1.100  ← Sesuai hasil ipconfig
BROKER_PORT=1883
```

**Cek 3: Firewall?**
- Buka firewall untuk port 1883

### Printer tidak cetak

**Cek log file:**
```
C:\KodeArduinoUtama\printer02\mqtt_printer.log
```

**Common issues:**
- DLL path salah
- Printer USB not connected
- Printer driver issue

### Payload tidak ter-parse

**Check format JSON:**
```json
{
  "barcode": "value",
  "product": "value",
  "line": "value"
}
```

Pastikan pakai double quote, bukan single quote.

---

## 📝 Node-RED Flow Example

Minimal flow:

```
[Inject] 
  ↓
[Function] - Generate data
  ↓
[MQTT Out] - Topic: printer/barcode/print
  ↓
[MQTT In] - Topic: printer/barcode/status
  ↓
[Debug] - Show status
```

### Inject Node:
```json
{
  "barcode": "TEST-001",
  "product": "Test Item",
  "line": "Test Line"
}
```

### Function Node (optional):
```javascript
// Generate dynamic barcode
let timestamp = Date.now();
msg.payload = {
  "barcode": "P" + timestamp,
  "product": msg.payload.product || "Auto",
  "line": msg.payload.line || "Line 1"
};
return msg;
```

### MQTT Out Config:
- Server: Your MQTT Broker IP
- Port: 1883
- Topic: `printer/barcode/print`
- QoS: 1
- Retain: false

---

## 📊 Monitoring & Logging

### Real-time Monitoring
Terminal akan menampilkan:
```
2026-01-29 10:30:45 - INFO - Starting service
2026-01-29 10:30:46 - INFO - Connected to MQTT broker
2026-01-29 10:30:50 - INFO - Message received: barcode=SKU-001
2026-01-29 10:30:51 - INFO - Barcode printed successfully
```

### Log File
```
C:\KodeArduinoUtama\printer02\mqtt_printer.log
```

**Log Levels:**
- `DEBUG` - Detail untuk troubleshoot
- `INFO` - Normal operation
- `WARNING` - Potential issues
- `ERROR` - Critical errors

---

## 🔄 Service Architecture

```
Node-RED
   ↓
MQTT Broker (192.168.1.100:1883)
   ↓
mqtt_printer_service.py
   ├→ Load DLL
   ├→ Init Printer
   └→ Listen to MQTT topic
        ↓
    Parse JSON
        ↓
    Print Barcode
        ↓
    Publish Status
        ↓
Node-RED (Status Topic)
```

---

## ⚡ Performance Tips

1. **Set Log Level ke INFO** (bukan DEBUG) untuk production
2. **Monitor log file size** - backup lama otomatis
3. **Keep MQTT broker responsive** - cek network latency
4. **Ensure USB printer connection stable**

---

## 📞 Quick Reference

| File | Gunakan Untuk |
|------|---------------|
| `mqtt_config.ini` | Edit konfigurasi |
| `mqtt_printer_service.py` | Script utama (jangan edit) |
| `RUN_MQTT_SERVICE.bat` | Jalankan service |
| `SETUP_MQTT_NODERED.md` | Setup MQTT & Node-RED |
| `mqtt_printer.log` | Lihat log |

---

## 🎯 Next Steps

1. ✅ Install MQTT Broker (Mosquitto)
2. ✅ Edit `mqtt_config.ini` dengan IP Anda
3. ✅ Double-click `RUN_MQTT_SERVICE.bat`
4. ✅ Setup Node-RED MQTT connection
5. ✅ Test dengan Inject node

**Status:** Service siap digunakan!

---

Last Updated: 2026-01-29
