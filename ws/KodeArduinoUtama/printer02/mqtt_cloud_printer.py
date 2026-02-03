#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================
MQTT Barcode Printer Service - Cloud Broker Edition
========================================================================
Menerima data dari Node-RED via MQTT Cloud Broker (HiveMQ)
dan mencetak barcode menggunakan fungsi dari printer02.py
========================================================================
"""

import paho.mqtt.client as mqtt
import json
import sys
import logging
import os
import time
import socket
import uuid
import configparser
import sqlite3
import traceback
from datetime import datetime
from ctypes import *
from pathlib import Path

# ========================================================================
# LOAD CONFIGURATION
# ========================================================================

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "mqtt_config.ini")

try:
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_FILE)
    
    BROKER_ADDRESS = cfg.get("MQTT", "BROKER_ADDRESS", fallback="broker.hivemq.com")
    BROKER_PORT = cfg.getint("MQTT", "BROKER_PORT", fallback=1883)
    CLIENT_ID = cfg.get("MQTT", "CLIENT_ID", fallback="barcode_printer_01")
    KEEPALIVE = cfg.getint("MQTT", "KEEPALIVE", fallback=60)
    
    TOPIC_BARCODE_INPUT = cfg.get("MQTT", "TOPIC_BARCODE_INPUT", fallback="printer/barcode/print")
    TOPIC_STATUS_OUTPUT = cfg.get("MQTT", "TOPIC_STATUS_OUTPUT", fallback="printer/barcode/status")
    TOPIC_COMMAND = cfg.get("MQTT", "TOPIC_COMMAND", fallback="printer/barcode/command")
    
    DLL_PATH = cfg.get("PRINTER", "DLL_PATH", fallback="C:\\KodeArduinoUtama\\printer02\\Msprintsdk.dll")
    
    LOG_FILE = cfg.get("LOGGING", "LOG_FILE", fallback="C:\\KodeArduinoUtama\\printer02\\mqtt_printer.log")
    LOG_LEVEL = cfg.get("LOGGING", "LOG_LEVEL", fallback="INFO")
    
    print(f"[CONFIG] Configuration loaded")
    print(f"[CONFIG] MQTT Broker: {BROKER_ADDRESS}:{BROKER_PORT}")
    
except Exception as e:
    print(f"[ERROR] Failed to load config: {str(e)}")
    sys.exit(1)

# ========================================================================
# SETUP LOGGING
# ========================================================================

log_dir = os.path.dirname(LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

# Create logger with UTF-8 encoding for emoji support
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL))

# File handler dengan UTF-8 encoding
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setLevel(getattr(logging, LOG_LEVEL))
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Console handler dengan UTF-8 encoding
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ========================================================================
# QUEUE & PERSISTENCE SETUP
# ========================================================================

QUEUE_DB_PATH = os.path.join(os.path.dirname(__file__), "print_queue.db")

class PrintQueue:
    """Manager untuk antrian print dengan persistent storage"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Inisialisasi database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS print_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    barcode TEXT NOT NULL,
                    product TEXT,
                    line TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    attempted_count INTEGER DEFAULT 0,
                    last_error TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info(f"Queue database initialized: {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to init queue database: {str(e)}")
    
    def add_to_queue(self, barcode, product, line):
        """Tambah item ke antrian"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO print_queue (barcode, product, line, status)
                VALUES (?, ?, ?, 'pending')
            ''', (barcode, product, line))
            
            conn.commit()
            queue_id = cursor.lastrowid
            conn.close()
            
            logger.info(f"✅ Added to queue (ID: {queue_id}): {barcode}")
            return queue_id
        except Exception as e:
            logger.error(f"Failed to add to queue: {str(e)}")
            return None
    
    def get_pending_queue(self):
        """Ambil semua item yang pending"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, barcode, product, line, attempted_count
                FROM print_queue
                WHERE status = 'pending'
                ORDER BY created_at ASC
                LIMIT 50
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Failed to get pending queue: {str(e)}")
            return []
    
    def mark_as_printed(self, queue_id):
        """Tandai item sebagai sudah tercetak"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE print_queue
                SET status = 'printed'
                WHERE id = ?
            ''', (queue_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✅ Queue item {queue_id} marked as printed")
            return True
        except Exception as e:
            logger.error(f"Failed to mark as printed: {str(e)}")
            return False
    
    def mark_as_failed(self, queue_id, error_msg):
        """Tandai item sebagai gagal (dengan limit retry)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE print_queue
                SET attempted_count = attempted_count + 1,
                    last_error = ?,
                    status = CASE
                        WHEN attempted_count >= 5 THEN 'failed'
                        ELSE 'pending'
                    END
                WHERE id = ?
            ''', (error_msg, queue_id))
            
            conn.commit()
            conn.close()
            
            logger.warning(f"Queue item {queue_id} retry (error: {error_msg[:50]})")
            return True
        except Exception as e:
            logger.error(f"Failed to mark as failed: {str(e)}")
            return False
    
    def get_queue_stats(self):
        """Ambil statistik antrian"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM print_queue WHERE status = "pending"')
            pending = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM print_queue WHERE status = "printed"')
            printed = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM print_queue WHERE status = "failed"')
            failed = cursor.fetchone()[0]
            
            conn.close()
            
            return {"pending": pending, "printed": printed, "failed": failed}
        except Exception as e:
            logger.error(f"Failed to get stats: {str(e)}")
            return {"pending": 0, "printed": 0, "failed": 0}

# Initialize queue manager
print_queue = PrintQueue(QUEUE_DB_PATH)

# ========================================================================
# GLOBAL VARIABLES
# ========================================================================

mqtt_client = None
printer_dll = None
is_connected = False
is_printer_ready = False
queue_processing_active = False

# ========================================================================
# MQTT CLIENT ID
# ========================================================================

def build_unique_client_id(base_client_id: str) -> str:
    """Build unique client id for multi-device connections."""
    host = socket.gethostname()
    pid = os.getpid()
    suffix = uuid.uuid4().hex[:6]
    return f"{base_client_id}_{host}_{pid}_{suffix}"

# ========================================================================
# QUEUE PROCESSING
# ========================================================================

def process_print_queue():
    """Proses antrian print jika printer siap"""
    global queue_processing_active
    
    if queue_processing_active:
        return
    
    queue_processing_active = True
    
    try:
        if not is_printer_ready:
            logger.debug("Printer not ready, skipping queue processing")
            queue_processing_active = False
            return
        
        pending = print_queue.get_pending_queue()
        
        if not pending:
            logger.debug("No pending items in queue")
            queue_processing_active = False
            return
        
        logger.info(f"Processing queue: {len(pending)} pending items")
        
        for item in pending:
            queue_id = item['id']
            barcode = item['barcode']
            product = item['product']
            line = item['line']
            attempted = item['attempted_count']
            
            logger.info(f"Processing queue item {queue_id} (attempt {attempted + 1})")
            
            # Cetak barcode
            success = cetakBarcode01(barcode, product, line)
            
            if success:
                print_queue.mark_as_printed(queue_id)
                publish_status("success", 
                              f"Queue item {queue_id}: Barcode '{barcode}' berhasil dicetak",
                              barcode=barcode, product=product, line=line, from_queue=True)
            else:
                print_queue.mark_as_failed(queue_id, "Print failed")
                
                if attempted + 1 >= 5:
                    publish_status("error",
                                  f"Queue item {queue_id}: Max retry reached untuk '{barcode}'",
                                  barcode=barcode)
                    logger.error(f"Queue item {queue_id} abandoned after 5 attempts")
        
        # Publish queue stats
        stats = print_queue.get_queue_stats()
        logger.info(f"Queue stats - Pending: {stats['pending']}, Printed: {stats['printed']}, Failed: {stats['failed']}")
        
    except Exception as e:
        logger.error(f"Error processing queue: {str(e)}")
    finally:
        queue_processing_active = False

# ========================================================================
# PRINTER FUNCTIONS (dari printer02.py)
# ========================================================================

def load_printer_dll():
    """Load printer DLL"""
    global printer_dll
    
    try:
        if not os.path.exists(DLL_PATH):
            logger.error(f"DLL tidak ditemukan: {DLL_PATH}")
            return False
        
        printer_dll = cdll.LoadLibrary(DLL_PATH)
        logger.info(f"Printer DLL berhasil dimuat: {DLL_PATH}")
        return True
    except Exception as e:
        logger.error(f"Gagal memuat DLL: {str(e)}")
        return False

def init_printer():
    """Inisialisasi printer"""
    global is_printer_ready
    
    try:
        if printer_dll is None:
            return False
        
        result = printer_dll.SetUsbportauto()
        logger.debug(f"SetUsbportauto: {result}")
        
        result = printer_dll.SetInit()
        logger.debug(f"SetInit: {result}")
        
        printer_dll.SetClean()
        
        status = printer_dll.GetStatus()
        logger.info(f"Printer status: {status}")
        
        is_printer_ready = True
        return True
    except Exception as e:
        logger.error(f"Gagal init printer: {str(e)}")
        is_printer_ready = False
        return False

def cetakBarcode01(id1, nama, ws):
    """
    Fungsi cetak barcode (sama seperti cetak_manual.py)
    
    Args:
        id1: Barcode data
        nama: Nama produk
        ws: Workstation/Line
    """
    try:
        if printer_dll is None:
            logger.error("Printer DLL not loaded")
            return False
        
        id1 = str(id1).strip()
        barcode = id1
        name = str(nama)
        ws1 = str(ws)
        
        logger.info(f"Printing - Barcode: {barcode}, Product: {name}, Line: {ws1}")
        
        # ===== STEP 1: INISIALISASI PRINTER =====
        setting = printer_dll.SetUsbportauto()
        logger.debug(f"SetUsbportauto: {setting}")
        
        setting2 = printer_dll.SetInit()
        logger.debug(f"SetInit: {setting2}")
        
        printer_dll.SetClean()
        
        # Set print quality
        try:
            printer_dll.SetDensity(15)  # Max darkness
            logger.debug("SetDensity(15) - Max darkness")
        except:
            pass
        
        try:
            printer_dll.SetSpeed(3)  # Medium speed
            logger.debug("SetSpeed(3) - Medium speed")
        except:
            pass
        
        printer_dll.SetAlignment(2)
        printer_dll.SetSizechar(2, 2, 0, 0)
        
        status = printer_dll.GetStatus()
        logger.info(f"Printer status: {status}")
        
        # HANDLE STATUS 8 - Printer not ready
        if status == 8:
            logger.warning("⚠️ Printer status 8 - attempting recovery...")
            printer_dll.SetClose()
            from time import sleep
            sleep(1)
            printer_dll.SetUsbportauto()
            printer_dll.SetInit()
            printer_dll.SetClean()
            status = printer_dll.GetStatus()
            logger.info(f"Status after recovery: {status}")
            
            if status != 1:
                logger.error("❌ Printer not ready! Check:")
                logger.error("   1. USB cable connected")
                logger.error("   2. Printer power ON")
                logger.error("   3. Paper loaded")
                logger.error("   4. No paper jam")
                return False
        
        # ===== STEP 2: ENCODE STRINGS =====
        string1 = barcode
        string2 = name
        string3 = " " + ws1
        
        b_string1 = string1.encode('utf-8')
        b_string2 = string2.encode('utf-8')
        b_string3 = string3.encode('utf-8')
        
        logger.debug(f"Barcode: {b_string1}")
        logger.debug(f"Product: {b_string2}")
        logger.debug(f"Workstation: {b_string3}")
        
        # ===== STEP 3: PRINT LAYOUT (SAMA SEPERTI cetak_manual.py) =====
        
        # Print workstation
        printer_dll.SetAlignment(1)
        printer_dll.SetSizetext(1, 1)  # Normal size
        printer_dll.PrintString(b_string3, 0)
        
        # Print product name (bigger font)
        printer_dll.SetSizetext(2, 2)  # Bigger font
        printer_dll.PrintString(b_string2, 0)
        
        # Print full barcode text (human readable)
        printer_dll.SetSizetext(1, 1)  # Normal size
        b_original = string1.encode('utf-8')
        printer_dll.PrintString(b_original, 0)
        logger.debug(f"Full text printed: {string1}")
        
        # ===== STEP 4: PRINT BARCODE (SAMA SEPERTI cetak_manual.py) =====
        
        # Parse barcode data (686A18103/K1-245/46 → 686A18103-245)
        original_data = string1
        barcode_data = string1
        
        if '/' in original_data and '-' in original_data:
            try:
                parts = original_data.split('/')
                if len(parts) >= 3:
                    product_no = parts[0]  # 686A18103
                    middle_part = parts[1]  # K1-245
                    
                    if '-' in middle_part:
                        serial_no = middle_part.split('-')[1]  # 245
                        barcode_data = f"{product_no}-{serial_no}"  # 686A18103-245
                        logger.info(f"Barcode parsed: {original_data} → {barcode_data}")
            except:
                pass
        
        b_barcode = barcode_data.encode('utf-8')
        print_success = False
        
        logger.info(f"Attempting to print barcode: {barcode_data}")
        
        # STRATEGY 1: Type 2 (EAN/UPC) - TANPA PrintChargeRow dulu!
        if not print_success:
            try:
                qrcode_result = printer_dll.Print1Dbar(2, 60, 1, 2, 4, b_barcode)
                print_success = True
                logger.info("✓ Barcode printed (Type 2)")
            except Exception as e:
                logger.warning(f"Type 2 failed: {str(e)[:100]}")
        
        # STRATEGY 2: Type 73 (Code128 - alphanumeric)
        if not print_success:
            try:
                printer_dll.PrintChargeRow()
                qrcode_result = printer_dll.Print1Dbar(73, 60, 2, 2, 0, b_barcode)
                print_success = True
                logger.info("✓ Barcode printed (Type 73 - Code128)")
            except Exception as e:
                logger.warning(f"Type 73 failed: {str(e)[:100]}")
        
        # STRATEGY 3: QR Code
        if not print_success:
            try:
                printer_dll.PrintChargeRow()
                qrcode_result = printer_dll.Print2Dbar(6, 5, b_barcode)
                print_success = True
                logger.info("✓ QR Code printed (Type 6)")
            except Exception as e:
                logger.warning(f"QR Code failed: {str(e)[:100]}")
        
        if not print_success:
            logger.error("❌ All barcode strategies failed!")
            return False
        
        # ===== STEP 5: FINISH =====
        # Paper feed after barcode
        for _ in range(5):
            printer_dll.PrintChargeRow()
        
        # Cut paper
        printer_dll.PrintCutpaper(1)
        
        # Wait for printer to finish
        from time import sleep
        sleep(2)
        
        printer_dll.SetClose()
        
        logger.info(f"Print SUCCESS - Barcode: {barcode}")
        return True
        
    except Exception as e:
        logger.error(f"Print FAILED: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

# ========================================================================
# MQTT CALLBACKS
# ========================================================================

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback saat connect ke MQTT (compatible with paho-mqtt v1 and v2)"""
    global is_connected
    
    if rc == 0:
        logger.info(f"Connected to MQTT: {BROKER_ADDRESS}:{BROKER_PORT}")
        is_connected = True
        
        client.subscribe(TOPIC_BARCODE_INPUT)
        logger.info(f"   Subscribed to: {TOPIC_BARCODE_INPUT}")
        
        client.subscribe(TOPIC_COMMAND)
        logger.info(f"   Subscribed to: {TOPIC_COMMAND}")
        
        # Publish status online
        status = {
            "status": "online",
            "message": "Printer ready",
            "timestamp": datetime.now().isoformat(),
            "printer_ready": is_printer_ready
        }
        client.publish(TOPIC_STATUS_OUTPUT, json.dumps(status))

def on_disconnect(client, userdata, rc, properties=None):
    """Callback saat disconnect (compatible with paho-mqtt v1 and v2)"""
    global is_connected
    is_connected = False
    
    if rc == 0:
        logger.info("Disconnected from broker")
    else:
        logger.warning(f"Unexpected disconnect. Code: {rc}")

def on_message(client, userdata, msg):
    """Callback saat menerima message"""
    try:
        logger.info(f"📩 Message from: {msg.topic}")
        
        payload = json.loads(msg.payload.decode())
        logger.info(f"   Payload: {payload}")
        
        if msg.topic == TOPIC_BARCODE_INPUT:
            handle_barcode_print(payload)
        elif msg.topic == TOPIC_COMMAND:
            handle_command(payload)
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        publish_status("error", "Format JSON tidak valid")
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        publish_status("error", f"Error: {str(e)}")

# ========================================================================
# MESSAGE HANDLERS
# ========================================================================

def handle_barcode_print(payload):
    """Handle print request - dengan queue fallback"""
    barcode = payload.get("barcode", "").strip()
    product = payload.get("product", "").strip()
    line = payload.get("line", "").strip()
    
    if not barcode:
        msg = "Barcode kosong dalam payload"
        logger.warning(msg)
        publish_status("error", msg)
        return
    
    logger.info(f"Print request - Barcode: {barcode}, Product: {product}, Line: {line}")
    
    # Jika printer siap, langsung cetak
    if is_printer_ready:
        success = cetakBarcode01(barcode, product, line)
        
        if success:
            message = f"Barcode '{barcode}' berhasil dicetak"
            publish_status("success", message, barcode=barcode, product=product, line=line)
        else:
            # Jika cetak gagal, tambah ke queue
            logger.warning(f"Print failed, adding to queue: {barcode}")
            queue_id = print_queue.add_to_queue(barcode, product, line)
            publish_status("warning", 
                          f"Print failed, added to queue (ID: {queue_id})",
                          barcode=barcode, queue_id=queue_id)
    else:
        # Jika printer tidak siap, langsung ke queue
        logger.warning(f"Printer not ready, adding to queue: {barcode}")
        queue_id = print_queue.add_to_queue(barcode, product, line)
        publish_status("warning",
                      f"Printer not ready, queued (ID: {queue_id})",
                      barcode=barcode, queue_id=queue_id)

def handle_command(payload):
    """Handle command - dengan queue management"""
    command = payload.get("command", "").lower()
    
    logger.info(f"Command received: {command}")
    
    if command == "init":
        if init_printer():
            publish_status("success", "Printer inisialisasi ulang berhasil")
            # Langsung proses queue setelah init berhasil
            time.sleep(1)
            process_print_queue()
        else:
            publish_status("error", "Gagal inisialisasi printer")
    
    elif command == "status":
        stats = print_queue.get_queue_stats()
        status_msg = f"Printer: {'ready' if is_printer_ready else 'not ready'}, Queue: {stats['pending']} pending, {stats['printed']} printed, {stats['failed']} failed"
        publish_status("info", status_msg)
    
    elif command == "process_queue":
        logger.info("Manual queue processing requested")
        process_print_queue()
        stats = print_queue.get_queue_stats()
        publish_status("info", f"Queue processed. Pending: {stats['pending']}, Printed: {stats['printed']}")
    
    elif command == "stop":
        logger.info("Stop command received")
        publish_status("info", "Service akan dihentikan...")
        mqtt_client.disconnect()
        sys.exit(0)
    
    else:
        logger.warning(f"Unknown command: {command}")
        publish_status("error", f"Unknown command: {command}")

def publish_status(status_type, message, **kwargs):
    """Publish status ke MQTT"""
    try:
        if mqtt_client and is_connected:
            payload = {
                "status": status_type,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "printer_ready": is_printer_ready
            }
            payload.update(kwargs)
            
            mqtt_client.publish(TOPIC_STATUS_OUTPUT, json.dumps(payload), qos=1)
            logger.debug(f"Status published: {status_type}")
    except Exception as e:
        logger.error(f"Failed to publish status: {str(e)}")

# ========================================================================
# MAIN
# ========================================================================

def main():
    """Main function"""
    global mqtt_client
    
    print("")
    print("="*70)
    print("MQTT BARCODE PRINTER SERVICE - CLOUD BROKER WITH QUEUE")
    print("="*70)
    print("")
    
    logger.info(f"MQTT Broker: {BROKER_ADDRESS}:{BROKER_PORT}")
    logger.info(f"Topic Input: {TOPIC_BARCODE_INPUT}")
    logger.info(f"Topic Status: {TOPIC_STATUS_OUTPUT}")
    logger.info(f"DLL Path: {DLL_PATH}")
    logger.info(f"Queue DB: {QUEUE_DB_PATH}")
    print("")
    
    # Load DLL
    logger.info("[PRINTER] Loading DLL...")
    if not load_printer_dll():
        logger.error("Critical: DLL tidak bisa dimuat!")
        return False
    
    # Init printer
    logger.info("[PRINTER] Initializing printer...")
    if not init_printer():
        logger.warning("Warning: Printer tidak siap, tapi service akan lanjut...")
    
    # Connect MQTT
    logger.info(f"[MQTT] Connecting to {BROKER_ADDRESS}...")
    
    try:
        # Compatible with both paho-mqtt v1.x and v2.x
        try:
            # Try v2.x API first
            unique_client_id = build_unique_client_id(CLIENT_ID)
            mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, unique_client_id)
            logger.debug("Using paho-mqtt v2.x API")
        except AttributeError:
            # Fall back to v1.x API
            unique_client_id = build_unique_client_id(CLIENT_ID)
            mqtt_client = mqtt.Client(unique_client_id)
            logger.debug("Using paho-mqtt v1.x API")
        
        mqtt_client.on_connect = on_connect
        mqtt_client.on_disconnect = on_disconnect
        mqtt_client.on_message = on_message
        
        # Set auto-reconnect with exponential backoff
        mqtt_client.reconnect_delay_set(min_delay=1, max_delay=32)
        
        # Use TLS/SSL for port 8883 (encrypted connection)
        if BROKER_PORT == 8883:
            logger.info("Using TLS/SSL encryption for port 8883...")
            mqtt_client.tls_set()
            mqtt_client.tls_insecure_set(True)  # Allow self-signed certs
        
        logger.info(f"Connecting to {BROKER_ADDRESS}:{BROKER_PORT}...")
        mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT, keepalive=KEEPALIVE)
        
    except Exception as e:
        logger.error(f"Failed to connect: {str(e)}")
        return False
    
    # Start loop
    mqtt_client.loop_start()
    
    print("")
    print("="*70)
    print("✅ SERVICE RUNNING WITH QUEUE PERSISTENCE")
    print("="*70)
    print(f"Waiting for messages from Node-RED...")
    print(f"Topic: {TOPIC_BARCODE_INPUT}")
    print(f"Queue Database: {QUEUE_DB_PATH}")
    print("")
    print("Press Ctrl+C to stop...")
    print("")
    
    try:
        # Queue processing loop
        last_queue_check = time.time()
        queue_check_interval = 10  # Cek queue setiap 10 detik
        
        while True:
            time.sleep(1)
            
            # Cek queue periodically
            current_time = time.time()
            if current_time - last_queue_check >= queue_check_interval:
                process_print_queue()
                last_queue_check = current_time
    
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        logger.info("Service stopped")
        return True
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
