#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================
MQTT Barcode Printer Service - V2 (NEW SETUP)
========================================================================
Script untuk menerima data barcode dari Node-RED via MQTT
dan mencetak ke printer thermal.

Author: System Integration
Version: 2.0
Date: 2026-01-29

Fitur:
- Load config dari mqtt_config.ini
- MQTT connection dengan auto-reconnect
- Barcode printing dengan DLL
- Comprehensive logging
- Status monitoring
========================================================================
"""

import paho.mqtt.client as mqtt
import json
import sys
import logging
import os
import time
import configparser
from datetime import datetime
from ctypes import *
from pathlib import Path
from threading import Thread, Lock

# ========================================================================
# CONSTANT
# ========================================================================

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "mqtt_config.ini")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ========================================================================
# CLASS: ConfigManager
# ========================================================================

class ConfigManager:
    """Load dan manage konfigurasi dari file mqtt_config.ini"""
    
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.load()
    
    def load(self):
        """Load konfigurasi dari file"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file tidak ditemukan: {self.config_file}")
        
        self.config.read(self.config_file)
    
    def get(self, section, key, default=None):
        """Get value dari config"""
        try:
            return self.config.get(section, key)
        except:
            return default
    
    def getint(self, section, key, default=0):
        """Get integer value dari config"""
        try:
            return self.config.getint(section, key)
        except:
            return default
    
    def getbool(self, section, key, default=False):
        """Get boolean value dari config"""
        try:
            return self.config.getboolean(section, key)
        except:
            return default

# ========================================================================
# LOAD CONFIGURATION
# ========================================================================

try:
    cfg = ConfigManager(CONFIG_FILE)
    
    # MQTT Configuration
    BROKER_ADDRESS = cfg.get("MQTT", "BROKER_ADDRESS", "localhost")
    BROKER_PORT = cfg.getint("MQTT", "BROKER_PORT", 1883)
    CLIENT_ID = cfg.get("MQTT", "CLIENT_ID", "barcode_printer_01")
    KEEPALIVE = cfg.getint("MQTT", "KEEPALIVE", 60)
    
    TOPIC_BARCODE_INPUT = cfg.get("MQTT", "TOPIC_BARCODE_INPUT", "printer/barcode/print")
    TOPIC_STATUS_OUTPUT = cfg.get("MQTT", "TOPIC_STATUS_OUTPUT", "printer/barcode/status")
    TOPIC_COMMAND = cfg.get("MQTT", "TOPIC_COMMAND", "printer/barcode/command")
    
    # Printer Configuration
    DLL_PATH = cfg.get("PRINTER", "DLL_PATH", "C:\\KodeArduinoUtama\\printer02\\Msprintsdk.dll")
    ALIGNMENT = cfg.getint("PRINTER", "ALIGNMENT", 1)
    FONT_WIDTH = cfg.getint("PRINTER", "FONT_WIDTH", 2)
    FONT_HEIGHT = cfg.getint("PRINTER", "FONT_HEIGHT", 2)
    ENABLE_BARCODE = cfg.getbool("PRINTER", "ENABLE_BARCODE", True)
    ENABLE_PRODUCT_NAME = cfg.getbool("PRINTER", "ENABLE_PRODUCT_NAME", True)
    ENABLE_LINE_NAME = cfg.getbool("PRINTER", "ENABLE_LINE_NAME", True)
    PAPER_FEED = cfg.getint("PRINTER", "PAPER_FEED", 2)
    
    # Logging Configuration
    LOG_FILE = cfg.get("LOGGING", "LOG_FILE", "C:\\KodeArduinoUtama\\printer02\\mqtt_printer.log")
    LOG_LEVEL = cfg.get("LOGGING", "LOG_LEVEL", "INFO")
    LOG_MAX_SIZE = cfg.getint("LOGGING", "LOG_MAX_SIZE", 1048576)
    LOG_BACKUP_COUNT = cfg.getint("LOGGING", "LOG_BACKUP_COUNT", 5)
    
    # Debug Configuration
    DEBUG_MODE = cfg.getbool("DEBUG", "DEBUG_MODE", False)
    DEBUG_CONSOLE = cfg.getbool("DEBUG", "DEBUG_CONSOLE", False)
    DEBUG_SAVE_PAYLOAD = cfg.getbool("DEBUG", "DEBUG_SAVE_PAYLOAD", False)
    DEBUG_PAYLOAD_DIR = cfg.get("DEBUG", "DEBUG_PAYLOAD_DIR", "C:\\KodeArduinoUtama\\printer02\\debug")
    
    print(f"[CONFIG] Configuration loaded from: {CONFIG_FILE}")
    
except Exception as e:
    print(f"[ERROR] Failed to load configuration: {str(e)}")
    sys.exit(1)

# ========================================================================
# SETUP LOGGING
# ========================================================================

# Create log directory if not exists
log_dir = os.path.dirname(LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL))

# File handler dengan rotation
from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=LOG_MAX_SIZE,
    backupCount=LOG_BACKUP_COUNT
)
file_handler.setLevel(getattr(logging, LOG_LEVEL))

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ========================================================================
# GLOBAL VARIABLES
# ========================================================================

mqtt_client = None
printer_dll = None
is_connected = False
is_printer_ready = False
print_lock = Lock()

# ========================================================================
# PRINTER FUNCTIONS
# ========================================================================

def load_printer_dll():
    """Load printer DLL"""
    global printer_dll
    
    try:
        if not os.path.exists(DLL_PATH):
            logger.error(f"DLL tidak ditemukan: {DLL_PATH}")
            return False
        
        printer_dll = cdll.LoadLibrary(DLL_PATH)
        logger.info(f"Printer DLL berhasil dimuat dari: {DLL_PATH}")
        return True
    except Exception as e:
        logger.error(f"Gagal memuat DLL: {str(e)}")
        return False

def init_printer():
    """Inisialisasi printer"""
    global is_printer_ready
    
    try:
        if printer_dll is None:
            logger.warning("Printer DLL belum dimuat")
            return False
        
        # Set USB port otomatis
        result = printer_dll.SetUsbportauto()
        logger.debug(f"SetUsbportauto result: {result}")
        
        # Inisialisasi printer
        result = printer_dll.SetInit()
        logger.debug(f"SetInit result: {result}")
        
        # Cleaning
        printer_dll.SetClean()
        logger.debug("Printer cleaning done")
        
        # Check status
        status = printer_dll.GetStatus()
        logger.info(f"Printer status: {status}")
        
        is_printer_ready = True
        return True
    except Exception as e:
        logger.error(f"Gagal inisialisasi printer: {str(e)}")
        is_printer_ready = False
        return False

def print_barcode(barcode_data, product_name="", line_name=""):
    """
    Cetak barcode ke printer
    
    Args:
        barcode_data (str): Data barcode
        product_name (str): Nama produk
        line_name (str): Nama line
    
    Returns:
        tuple: (success: bool, message: str)
    """
    with print_lock:
        try:
            if printer_dll is None:
                msg = "Printer DLL tidak dimuat"
                logger.error(msg)
                return False, msg
            
            if not is_printer_ready:
                msg = "Printer tidak ready"
                logger.error(msg)
                return False, msg
            
            logger.info(f"Mulai cetak barcode: {barcode_data}")
            
            # Alignment
            printer_dll.SetAlignment(ALIGNMENT)
            
            # Set font size
            printer_dll.SetSizechar(FONT_WIDTH, FONT_HEIGHT, 0, 0)
            
            # ===== CETAK BARCODE =====
            if ENABLE_BARCODE:
                barcode_bytes = barcode_data.encode('utf-8')
                printer_dll.PrintBarcode(barcode_bytes, 73, 2, 2, 0, 0)  # Code128
                logger.debug(f"Barcode printed: {barcode_data}")
            
            # ===== CETAK NAMA PRODUK =====
            if ENABLE_PRODUCT_NAME and product_name:
                printer_dll.PrintChargeRow()
                printer_dll.SetAlignment(0)  # Left
                printer_dll.SetSizetext(1, 2)
                product_bytes = product_name.encode('utf-8')
                printer_dll.PrintString(product_bytes, 0)
                logger.debug(f"Product name printed: {product_name}")
            
            # ===== CETAK LINE/WORKSTATION =====
            if ENABLE_LINE_NAME and line_name:
                printer_dll.PrintChargeRow()
                printer_dll.SetAlignment(0)  # Left
                printer_dll.SetSizetext(1, 1)
                line_bytes = line_name.encode('utf-8')
                printer_dll.PrintString(line_bytes, 0)
                logger.debug(f"Line name printed: {line_name}")
            
            # Paper feed
            for _ in range(PAPER_FEED):
                printer_dll.PrintChargeRow()
            
            msg = f"Barcode '{barcode_data}' berhasil dicetak"
            logger.info(msg)
            return True, msg
            
        except Exception as e:
            msg = f"Error saat mencetak: {str(e)}"
            logger.error(msg)
            return False, msg

# ========================================================================
# MQTT CALLBACKS
# ========================================================================

def on_connect(client, userdata, flags, rc):
    """Callback saat connect ke MQTT broker"""
    global is_connected
    
    if rc == 0:
        logger.info(f"✓ Connected ke MQTT broker: {BROKER_ADDRESS}:{BROKER_PORT}")
        is_connected = True
        
        # Subscribe ke topics
        client.subscribe(TOPIC_BARCODE_INPUT)
        logger.info(f"  Subscribe ke: {TOPIC_BARCODE_INPUT}")
        
        client.subscribe(TOPIC_COMMAND)
        logger.info(f"  Subscribe ke: {TOPIC_COMMAND}")
        
        # Publish status online
        publish_status("online", "Printer ready")
    else:
        logger.error(f"✗ Gagal connect ke broker. Error code: {rc}")
        is_connected = False

def on_disconnect(client, userdata, rc):
    """Callback saat disconnect dari MQTT"""
    global is_connected
    is_connected = False
    
    if rc == 0:
        logger.info("Disconnected dari broker")
    else:
        logger.warning(f"Unexpected disconnect dari broker. Code: {rc}")

def on_message(client, userdata, msg):
    """Callback saat menerima message"""
    try:
        logger.debug(f"Message diterima dari: {msg.topic}")
        
        # Parse JSON
        payload = json.loads(msg.payload.decode())
        logger.debug(f"Payload: {payload}")
        
        # Debug: save payload jika enabled
        if DEBUG_SAVE_PAYLOAD:
            save_debug_payload(payload)
        
        # Handle barcode print
        if msg.topic == TOPIC_BARCODE_INPUT:
            handle_barcode_print(payload)
        
        # Handle command
        elif msg.topic == TOPIC_COMMAND:
            handle_command(payload)
            
    except json.JSONDecodeError as e:
        logger.error(f"Error parse JSON: {str(e)}")
        publish_status("error", "Format JSON tidak valid")
    except Exception as e:
        logger.error(f"Error memproses message: {str(e)}")
        publish_status("error", f"Error: {str(e)}")

def on_log(client, userdata, level, buf):
    """Callback MQTT logging"""
    if DEBUG_MODE:
        if level == mqtt.MQTT_LOG_ERR:
            logger.error(f"MQTT: {buf}")
        elif level == mqtt.MQTT_LOG_WARNING:
            logger.warning(f"MQTT: {buf}")

# ========================================================================
# MESSAGE HANDLERS
# ========================================================================

def handle_barcode_print(payload):
    """Handle print barcode request"""
    # Extract data
    barcode = payload.get("barcode", "").strip()
    product = payload.get("product", "").strip()
    line = payload.get("line", "").strip()
    
    if not barcode:
        msg = "Barcode kosong dalam payload"
        logger.warning(msg)
        publish_status("error", msg)
        return
    
    logger.info(f"Print request - Barcode: {barcode}, Product: {product}, Line: {line}")
    
    # Print barcode
    success, message = print_barcode(barcode, product, line)
    
    # Publish status
    if success:
        publish_status("success", message)
    else:
        publish_status("error", message)

def handle_command(payload):
    """Handle command dari MQTT"""
    command = payload.get("command", "").lower()
    
    logger.info(f"Command diterima: {command}")
    
    if command == "init":
        if init_printer():
            publish_status("success", "Printer inisialisasi ulang berhasil")
        else:
            publish_status("error", "Gagal inisialisasi printer")
    
    elif command == "status":
        status = "ready" if is_printer_ready else "not_ready"
        publish_status("info", f"Printer status: {status}")
    
    elif command == "stop":
        logger.info("Stop command diterima")
        publish_status("info", "Service akan dihentikan...")
        sys.exit(0)
    
    else:
        logger.warning(f"Unknown command: {command}")
        publish_status("error", f"Unknown command: {command}")

# ========================================================================
# HELPER FUNCTIONS
# ========================================================================

def publish_status(status_type, message):
    """Publish status ke MQTT"""
    try:
        if mqtt_client and is_connected:
            payload = json.dumps({
                "status": status_type,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "printer_ready": is_printer_ready
            })
            mqtt_client.publish(TOPIC_STATUS_OUTPUT, payload, qos=1)
            logger.debug(f"Status published: {status_type}")
    except Exception as e:
        logger.error(f"Gagal publish status: {str(e)}")

def save_debug_payload(payload):
    """Save payload ke file untuk debugging"""
    try:
        if not os.path.exists(DEBUG_PAYLOAD_DIR):
            os.makedirs(DEBUG_PAYLOAD_DIR, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = os.path.join(DEBUG_PAYLOAD_DIR, f"payload_{timestamp}.json")
        
        with open(filename, 'w') as f:
            json.dump(payload, f, indent=2)
        
        logger.debug(f"Payload saved: {filename}")
    except Exception as e:
        logger.error(f"Error saving payload: {str(e)}")

def connect_mqtt():
    """Connect ke MQTT broker"""
    global mqtt_client
    
    try:
        mqtt_client = mqtt.Client(CLIENT_ID)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_disconnect = on_disconnect
        mqtt_client.on_message = on_message
        mqtt_client.on_log = on_log
        
        logger.info(f"Connecting to MQTT broker: {BROKER_ADDRESS}:{BROKER_PORT}")
        mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT, keepalive=KEEPALIVE)
        
        return True
    except Exception as e:
        logger.error(f"Gagal connect ke MQTT: {str(e)}")
        return False

# ========================================================================
# MAIN
# ========================================================================

def main():
    """Main function"""
    logger.info("="*70)
    logger.info("MQTT BARCODE PRINTER SERVICE V2 - STARTING")
    logger.info("="*70)
    
    # Print config
    logger.info(f"[CONFIG] MQTT Broker: {BROKER_ADDRESS}:{BROKER_PORT}")
    logger.info(f"[CONFIG] Topic Input: {TOPIC_BARCODE_INPUT}")
    logger.info(f"[CONFIG] Topic Status: {TOPIC_STATUS_OUTPUT}")
    logger.info(f"[CONFIG] DLL Path: {DLL_PATH}")
    logger.info("")
    
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
    logger.info("[MQTT] Connecting to broker...")
    if not connect_mqtt():
        logger.error("Critical: Tidak bisa connect ke MQTT!")
        return False
    
    # Start MQTT loop
    mqtt_client.loop_start()
    
    logger.info("")
    logger.info("="*70)
    logger.info("✓ SERVICE RUNNING")
    logger.info("="*70)
    logger.info(f"Waiting for messages on: {TOPIC_BARCODE_INPUT}")
    logger.info("")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        logger.info("Service stopped")
        return True
    except Exception as e:
        logger.error(f"Fatal error in main loop: {str(e)}")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        return False

# ========================================================================
# ENTRY POINT
# ========================================================================

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
