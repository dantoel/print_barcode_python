# Node-RED Barcode Printer Integration

## 📋 Deskripsi
Script Python untuk menerima data barcode dari Node-RED melalui MQTT broker dan mencetak ke printer thermal.

## 🚀 Cara Penggunaan

### 1. **Setup Awal**
Pastikan Python dan library paho-mqtt sudah terinstall:
```bash
pip install paho-mqtt
```

### 2. **Jalankan Script**
Double-click file `RUN_NODE_RED_PRINTER.bat` atau jalankan via terminal:
```bash
python node_red_printer.py
```

### 3. **Konfigurasi Node-RED**
Dalam Node-RED, buat flow untuk mengirim data ke MQTT topic.

#### **MQTT Topic untuk Mengirim Data:**
```
node-red/barcode/print
```

#### **Format JSON yang Dikirim Node-RED:**
```json
{
  "barcode": "12345ABC",
  "product": "Nama Produk",
  "line": "Line 1"
}
```

**Parameter Penjelasan:**
- `barcode` (string, **WAJIB**) - Data barcode/QR code yang akan dicetak
- `product` (string, opsional) - Nama produk
- `line` (string, opsional) - Nama line/workstation

#### **Contoh Node-RED Flow:**

**Inject Node:**
```json
{
  "barcode": "SKU-2026-001",
  "product": "Motor Pump",
  "line": "Assembly Line 1"
}
```

**MQTT Out Node Configuration:**
- Server: `192.168.1.103:1883`
- Topic: `node-red/barcode/print`
- QoS: `1`
- Retain: `false`

### 4. **Monitor Status Printer**
Subscribe ke topic status untuk menerima feedback:
```
node-red/barcode/status
```

**Response Status:**
```json
{
  "status": "success",
  "message": "Barcode 'SKU-2026-001' berhasil dicetak",
  "timestamp": "2026-01-29T10:30:45.123456"
}
```

Status yang mungkin:
- `online` - Printer ready
- `success` - Barcode berhasil dicetak
- `error` - Ada error

## 🔧 Konfigurasi

Edit pada bagian **KONFIGURASI** di `node_red_printer.py`:

```python
BROKER_ADDRESS = "192.168.1.103"      # IP MQTT Broker
BROKER_PORT = 1883                     # Port MQTT
MQTT_TOPIC_BARCODE = "node-red/barcode/print"  # Topic input
MQTT_TOPIC_STATUS = "node-red/barcode/status"   # Topic output
```

## 📝 Logging

Log file: `C:\KodeArduinoUtama\printer02\node_red_printer.log`

Untuk melihat log realtime, buka terminal dan jalankan script.

## ⚠️ Troubleshoot

### Script tidak connect ke MQTT:
1. Cek IP MQTT Broker: `ping 192.168.1.103`
2. Cek koneksi network
3. Lihat log file untuk detail error

### Printer tidak cetak:
1. Cek DLL path: `C:\KodeArduinoUtama\printer02\Msprintsdk.dll`
2. Cek koneksi USB printer
3. Cek log file untuk detail error

### paho-mqtt module not found:
```bash
pip install paho-mqtt
```

## 📊 Flow Node-RED Contoh

```
[Inject] → [Function] → [MQTT Out]
  ↓
[MQTT In] ← [Status Topic]
  ↓
[Debug]
```

### Inject Node (contoh data):
```json
{
  "barcode": "PRODUCT-" & timestamp(),
  "product": "Item Name",
  "line": "WS-01"
}
```

### Function Node (generate dynamic data):
```javascript
let barcode = "P" + Math.floor(Math.random() * 100000);
msg.payload = {
  "barcode": barcode,
  "product": msg.payload.product || "Unknown",
  "line": msg.payload.line || "Default"
};
return msg;
```

## 🔗 Referensi
- Dokumentasi MQTT: https://mosquitto.org/
- Dokumentasi paho-mqtt: https://www.eclipse.org/paho/index.php?page=clients/python/index.php
- Dokumentasi Node-RED MQTT: https://flows.nodered.org/node/node-red-contrib-mqtt-broker

## 📞 Support
Untuk masalah teknis, check:
1. Log file di `C:\KodeArduinoUtama\printer02\node_red_printer.log`
2. Terminal output saat script berjalan
3. Status MQTT topic

---
Last Updated: 2026-01-29
