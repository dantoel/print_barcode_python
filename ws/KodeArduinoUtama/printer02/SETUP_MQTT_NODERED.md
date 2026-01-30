# Setup MQTT Broker & Node-RED Baru

## 🚀 Pilihan Setup

Pilih salah satu sesuai preferensi:

### **OPSI 1: Install Mosquitto (MQTT Broker) di PC Anda**
**Paling recommended untuk development/testing**

#### Step 1: Download & Install Mosquitto
1. Download: https://mosquitto.org/download/
2. Pilih Windows installer (`.exe`)
3. Install dengan default settings
4. Default port: `1883`

#### Step 2: Verify Mosquitto Running
```bash
# Buka Command Prompt / PowerShell
# Mosquitto akan running di background

# Test dengan subscribe ke topic
mosquitto_sub -h localhost -t "test"

# Di terminal lain, test publish
mosquitto_pub -h localhost -t "test" -m "hello"
```

**Mosquitto Default Location:**
- `C:\Program Files\mosquitto\` (Windows)
- Config file: `C:\Program Files\mosquitto\mosquitto.conf`

**Default IP untuk Mosquitto:**
- `localhost` atau `127.0.0.1` (local machine)
- `192.168.x.x` (network machine - cek IP dengan `ipconfig`)

---

### **OPSI 2: Gunakan Online MQTT Broker**
**Untuk testing cepat tanpa install**

Popular free brokers:
- **HiveMQ**: `broker.hivemq.com:1883`
- **EMQ**: `broker.emqx.io:1883`
- **Mosquitto**: `test.mosquitto.org:1883`

---

### **OPSI 3: Docker Mosquitto**
**Jika sudah install Docker**

```bash
docker run -d -p 1883:1883 -p 9001:9001 eclipse-mosquitto
```

---

## 🎯 Setup Rekomendasi (OPSI 1 - Mosquitto Local)

### 1. Install Mosquitto

**Download dari:** https://mosquitto.org/download/

Pilih: `mosquitto-2.0.x-install-windows-x64.exe` (atau sesuai OS)

**Install Steps:**
1. Run installer
2. Next → Next → Install
3. Di bagian "Broker", pastikan `Install as Service` ✓
4. Finish

### 2. Verify Installation

Buka PowerShell/CMD:
```powershell
# Check mosquitto service
Get-Service | findstr mosquitto

# Or try connect
mosquitto_sub -h localhost -t "test"
```

### 3. Dapatkan IP Address PC Anda

```powershell
ipconfig
```

Cari `IPv4 Address` sesuai network Anda:
```
Ethernet adapter Ethernet:
   IPv4 Address . . . . . . . . . . . . : 192.168.1.100
```

Gunakan IP ini untuk Node-RED dan script printer!

---

## 🔴 Node-RED Setup

### Install Node-RED

**Via npm (recommended):**
```bash
npm install -g node-red
```

**Run Node-RED:**
```bash
node-red
```

**Akses di browser:**
```
http://localhost:1880
```

### Install MQTT Nodes di Node-RED

1. Buka Node-RED
2. Menu ☰ → Manage Palette
3. Search: `mqtt`
4. Install: `node-red-contrib-mqtt-broker` atau cukup gunakan built-in MQTT nodes

---

## 📝 Konfigurasi File

Setelah install, anda perlu:

1. **Update file konfigurasi** dengan IP MQTT Anda
2. **Update script Python** dengan IP MQTT
3. **Setup Node-RED MQTT connection**

---

## ✅ Checklist Sebelum Start

- [ ] Mosquitto installed & running
- [ ] IP Address MQTT tercatat
- [ ] Node-RED installed & running
- [ ] Python paho-mqtt installed
- [ ] Printer connected via USB

---

## 🔗 Referensi

- Mosquitto Docs: https://mosquitto.org/documentation/
- Node-RED Docs: https://nodered.org/docs/
- MQTT Basics: https://www.hivemq.com/mqtt-essentials/

---

**Setelah selesai setup, beri tahu saya IP MQTT Anda dan kami buat konfigurasi lengkapnya!**
