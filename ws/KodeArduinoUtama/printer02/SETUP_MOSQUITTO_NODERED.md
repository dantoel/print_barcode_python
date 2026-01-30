# Setup MQTT Mosquitto Lokal untuk Node-RED & Barcode Printer

## 📋 Daftar Config

| File | Fungsi |
|------|--------|
| `SETUP_MOSQUITTO.md` | Panduan install Mosquitto |
| `mosquitto_config.ini` | Config untuk Mosquitto lokal |
| `node_red_flow_mosquitto.json` | Flow Node-RED untuk Mosquitto |

---

## 🚀 Step 1: Install Mosquitto

### Download
- Windows: https://mosquitto.org/download/
- Pilih: `mosquitto-2.0.x-install-windows-x64.exe`

### Install Steps
1. Run installer
2. Next → Next → Install
3. Centang `Install as Service`
4. Finish

### Verify Installation
```powershell
# Check service status
Get-Service | findstr mosquitto

# Hasil harusnya: mosquitto ... Running
```

---

## 🔧 Step 2: Konfigurasi Mosquitto

### Edit Config File
Lokasi: `C:\Program Files\mosquitto\mosquitto.conf`

**Tambahkan/Pastikan ada:**
```conf
# Network
listener 1883 0.0.0.0
allow_anonymous true

# Logging
log_dest file C:\Program Files\mosquitto\log\mosquitto.log
log_dest console
log_type all
log_timestamp true
```

### Restart Service
```powershell
# Stop
net stop mosquitto

# Start
net start mosquitto
```

---

## 📡 Step 3: Configure Printer Service

Edit file: `mqtt_config.ini`

```ini
[MQTT]
BROKER_ADDRESS=localhost
BROKER_PORT=1883
CLIENT_ID=barcode_printer_01
```

---

## 🎯 Step 4: Setup Node-RED

### Install Node-RED
```bash
npm install -g node-red
```

### Run Node-RED
```bash
node-red
```

Akses: `http://localhost:1880`

### Import Flow
1. Menu ☰ → Import
2. Copy isi file: `node_red_flow_mosquitto.json`
3. Paste & Import
4. Deploy

### MQTT Broker Config di Node-RED
- **Server**: `localhost`
- **Port**: `1883`
- **Client ID**: `node-red-client`
- **Username**: kosong
- **Password**: kosong
- **Use TLS**: OFF

---

## 📊 Topics (Sama seperti sebelumnya)

| Topic | Direction | Fungsi |
|-------|-----------|--------|
| `printer/barcode/print` | → (Kirim) | Barcode data dari Node-RED |
| `printer/barcode/status` | ← (Terima) | Status printer |
| `printer/barcode/command` | → (Kirim) | Command (status/init/stop) |

---

## ✅ Test Koneksi

### Test Mosquitto Running
```powershell
mosquitto_sub -h localhost -t "test"

# Di terminal lain:
mosquitto_pub -h localhost -t "test" -m "hello"
```

### Cek Log
```
C:\Program Files\mosquitto\log\mosquitto.log
```

---

## 🎯 Flow Diagram

```
[Node-RED PC]
     ↓ (localhost:1883)
[Mosquitto Broker]
     ↓ (localhost:1883)
[Printer PC - mqtt_cloud_printer.py]
```

**Note:** Jika printer PC berbeda, gunakan:
```ini
BROKER_ADDRESS=<IP_Node_RED_PC>
```

Contoh: `BROKER_ADDRESS=192.168.1.100` (IP PC Node-RED)

---

## ⚠️ Troubleshoot

### Mosquitto tidak start
```powershell
# Check log
Get-Content "C:\Program Files\mosquitto\log\mosquitto.log" -Tail 20

# Restart
net stop mosquitto
net start mosquitto
```

### Port 1883 sudah dipakai
```powershell
netstat -ano | findstr 1883

# Kill process jika perlu
taskkill /PID <PID> /F
```

### Node-RED tidak connect
- Pastikan `localhost` atau IP address benar
- Pastikan Mosquitto service running
- Cek firewall port 1883

---

## 📝 Keuntungan Mosquitto Lokal

✓ Tidak perlu internet  
✓ Kontrol penuh  
✓ Data tetap lokal  
✓ Lebih cepat  

---

Sudah siap setup Mosquitto?
