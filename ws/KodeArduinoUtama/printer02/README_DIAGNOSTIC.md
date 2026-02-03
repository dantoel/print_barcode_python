# PRINTER DIAGNOSTIC & TROUBLESHOOTING TOOLS

Kumpulan tools untuk debug dan troubleshoot masalah printer yang tidak bisa print.

## 🚀 Quick Start

### Jika printer tidak bisa print:

```batch
TROUBLESHOOT.bat
```

Menu ini akan guide Anda melalui troubleshooting steps.

---

## 📋 Available Tools

### 1. **TROUBLESHOOT.bat** (Recommended)
Menu interaktif untuk memilih troubleshooting action.

**Fitur:**
- Run Full Diagnostic
- Check printer status & queue
- Test print barcode
- Clear printer error
- View error log
- Reset queue
- Test MQTT connection
- Show system info

**Cara pakai:**
```batch
TROUBLESHOOT.bat
```

---

### 2. **RUN_DIAGNOSTIC.bat**
Jalankan semua diagnostic tests lengkap.

**Test yang dilakukan:**
1. DLL Path & Availability
2. Load DLL
3. Check DLL Functions
4. Printer Connection
5. Test Print Barcode
6. MQTT Connectivity
7. USB Devices
8. File Permissions

**Output:** Detailed report dengan rekomendasi fix

**Cara pakai:**
```batch
RUN_DIAGNOSTIC.bat
```

---

### 3. **CHECK_STATUS.bat**
Lihat status printer dan queue database.

**Informasi:**
- DLL path dan existence
- Queue statistics (pending/printed/failed)
- List pending items
- List failed items dengan error message

**Cara pakai:**
```batch
CHECK_STATUS.bat
```

---

### 4. **TROUBLESHOOTING_GUIDE.md**
Panduan lengkap troubleshooting untuk setiap error.

**Isi:**
- Common issues & solutions
- Advanced troubleshooting
- Multi-printer setup issues
- Performance troubleshooting
- Contact support

**Cara buka:**
```batch
notepad TROUBLESHOOTING_GUIDE.md
```

---

## 🔍 Common Error Diagnosis

### Error: "Printer tidak terdeteksi"
```bash
TROUBLESHOOT.bat → Option 1 (Full Diagnostic)
→ Look for TEST 4 & TEST 7 results
→ Follow recommendations
```

### Error: "DLL tidak ditemukan"
```bash
TROUBLESHOOT.bat → Option 1 (Full Diagnostic)
→ Look for TEST 1 result
→ Update DLL_PATH in mqtt_config.ini
```

### Error: "Print sukses tapi tidak ada output"
```bash
TROUBLESHOOT.bat → Option 3 (Test Print)
atau
RUN_DIAGNOSTIC.bat → Look for TEST 5
```

### Queue menumpuk (pending items banyak)
```bash
TROUBLESHOOT.bat → Option 2 (Check Status)
→ See how many pending items
→ Check if printer connection OK
```

---

## 📊 Understanding Test Results

### TEST 1: DLL Availability
**✓ PASS:** DLL ditemukan dan accessible
**✗ FAIL:** Path salah atau file tidak ada
**FIX:** Update `DLL_PATH` di `mqtt_config.ini`

### TEST 2: Load DLL
**✓ PASS:** DLL berhasil di-load ke memory
**✗ FAIL:** DLL corrupted atau missing dependencies
**FIX:** Install Visual C++ Runtime atau replace DLL

### TEST 3: DLL Functions
**✓ PASS:** Semua function ditemukan
**⚠ WARNING:** Beberapa function missing (OK jika tidak critical)
**✗ FAIL:** DLL tidak valid atau corrupt

### TEST 4: Printer Connection
**✓ PASS:** Printer terdeteksi dan siap
**✗ FAIL:** Printer tidak connected
**FIX:** Check USB cable, power, driver installation

### TEST 5: Print Test
**✓ PASS:** Barcode berhasil dicetak
**✗ FAIL:** Print command gagal
**FIX:** Check printer error, paper, head condition

### TEST 6: MQTT Connection
**✓ PASS:** MQTT broker connected
**✗ FAIL:** Network atau broker issue
**FIX:** Check internet, firewall, broker address

### TEST 7: USB Devices
**ℹ INFO:** List USB dan COM ports
**USE FOR:** Check if printer COM port listed

### TEST 8: File Permissions
**✓ PASS:** Read/Write/Delete permissions OK
**✗ FAIL:** Missing permissions
**FIX:** Run as Administrator

---

## 🛠️ Manual Troubleshooting

### Test DLL Loading via PowerShell

```powershell
# Test if DLL loads
[System.Reflection.Assembly]::LoadFile("C:\Path\To\Msprintsdk.dll")

# If success, DLL is OK
# If error, DLL corrupted or wrong arch (32-bit vs 64-bit)
```

### View Queue Database

```powershell
# Install sqlite3 if not available
# choco install sqlite (using Chocolatey)
# or download from https://www.sqlite.org/download.html

cd "C:\Path\To\Printer\Folder"
sqlite3 print_queue.db

# View all pending
SELECT * FROM print_queue WHERE status='pending';

# View stats
SELECT status, COUNT(*) FROM print_queue GROUP BY status;

# Clear failed
DELETE FROM print_queue WHERE status='failed';
```

### Check Printer via Device Manager

```powershell
# Open Device Manager
devmgmt.msc

# Look for:
# - Ports (COM & LPT) - printer should be listed as COM port
# - Universal Serial Bus controllers - printer USB device
# - Printers - printer should be listed
```

### View Service Logs

```powershell
# Tail logs
Get-Content -Path "C:\KodeArduinoUtama\printer02\mqtt_printer.log" -Tail 100 -Wait

# Or search for errors
Select-String "ERROR|FAIL" -Path "C:\KodeArduinoUtama\printer02\mqtt_printer.log" | Head -20
```

---

## 🚨 Emergency Recovery

### Reset Everything

If everything broken, do this:

```batch
REM 1. Stop service (Ctrl+C if running)

REM 2. Delete queue database (will recreate on start)
del print_queue.db

REM 3. Power cycle printer
REM    - Off
REM    - Wait 10 sec
REM    - On

REM 4. Restart PC
shutdown /r /t 0

REM 5. Run diagnostic
RUN_DIAGNOSTIC.bat

REM 6. Start service
start RUN_MQTT_CLOUD_PRINTER.bat
```

### Restore DLL from Backup

```batch
REM Copy from working computer
REM Source: Another PC's working folder
REM Destination: C:\Path\To\Broken\Folder\Msprintsdk.dll

xcopy "\\WORKING_PC\c$\MyPrinterService\Msprintsdk.dll" "C:\MyPrinterFolder\" /Y
```

---

## 📞 Support Information

When asking for help, provide:

1. **Diagnostic Output**
   ```batch
   RUN_DIAGNOSTIC.bat > diagnostic_output.txt 2>&1
   ```

2. **Configuration (without passwords)**
   ```batch
   copy mqtt_config.ini mqtt_config_redacted.ini
   REM Edit to remove sensitive data
   ```

3. **Error Log**
   ```batch
   copy mqtt_printer.log mqtt_printer_log.txt
   ```

4. **System Info**
   ```batch
   systeminfo > sysinfo.txt
   ```

5. **Queue Status**
   ```batch
   CHECK_STATUS.bat > queue_status.txt 2>&1
   ```

Attach semua file ini saat menghubungi support.

---

## 📝 Troubleshooting Checklist

### Before diagnosing:
- [ ] Service stopped
- [ ] Printer powered on
- [ ] USB cable connected
- [ ] No other software using printer
- [ ] Run as Administrator if needed

### After diagnosing:
- [ ] All 8 tests passed
- [ ] Barcode successfully printed
- [ ] Queue empty (0 pending items)
- [ ] No error messages in log

### If still not working:
- [ ] Collect all diagnostic output
- [ ] Check TROUBLESHOOTING_GUIDE.md for specific error
- [ ] Try on another computer
- [ ] Test printer with Windows Print Test Page
- [ ] Contact technical support

---

## 🔄 Regular Maintenance

Run these periodically:

**Daily:**
```batch
CHECK_STATUS.bat  REM Check queue status
```

**Weekly:**
```batch
RUN_DIAGNOSTIC.bat  REM Full diagnostic
```

**Monthly:**
```batch
TROUBLESHOOT.bat  REM Menu - check everything
```

---

**Last Updated:** 2026-02-03
**Version:** 1.0
