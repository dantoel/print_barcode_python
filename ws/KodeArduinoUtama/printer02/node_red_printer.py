#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================
Script untuk mencetak barcode dari data yang dikirim Node-RED via MQTT
========================================================================
Author: Node-RED Integration
Date: 2026
Description: 
    Script ini menerima data dari Node-RED melalui MQTT broker,
    kemudian mencetak barcode ke printer thermal menggunakan DLL.
========================================================================
"""

import paho.mqtt.client as mqtt
import json
import sys
import logging
from datetime import datetime
from ctypes import *
import os
import time
from threading import Thread

# ========================================================================
# KONFIGURASI
# ========================================================================

BROKER_ADDRESS = "192.168.1.103"
BROKER_PORT = 1883
MQTT_TOPIC_BARCODE = "node-red/barcode/print"  # Topic untuk barcode
MQTT_TOPIC_STATUS = "node-red/barcode/status"   # Topic untuk status

DLL_PATH = "C:\\KodeArduinoUtama\\printer02\\Msprintsdk.dll"
LOG_FILE = "C:\\KodeArduinoUtama\\printer02\\node_red_printer.log"

# ========================================================================
# SETUP LOGGING
# ========================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ========================================================================
# GLOBAL VARIABLES
# ========================================================================

client = None
printer_dll = None
is_connected = False

# ========================================================================
# FUNGSI PRINTER
# ========================================================================

def load_printer_dll():
    """Load printer DLL"""
    try:
        if not os.path.exists(DLL_PATH):
            logger.error(f"DLL tidak ditemukan: {DLL_PATH}")
            return False
        
        global printer_dll
        printer_dll = cdll.LoadLibrary(DLL_PATH)
        logger.info("Printer DLL berhasil dimuat")
        return True
    except Exception as e:
        logger.error(f"Gagal memuat DLL: {str(e)}")
        return False

def init_printer():
    """Inisialisasi printer"""
    try:
        if printer_dll is None:
            logger.warning("Printer DLL belum dimuat")
            return False
        
        # Set USB port otomatis
        result = printer_dll.SetUsbportauto()
        logger.info(f"SetUsbportauto result: {result}")
        
        # Inisialisasi printer
        result = printer_dll.SetInit()
        logger.info(f"SetInit result: {result}")
        
        # Cleaning
        printer_dll.SetClean()
        
        # Check status
        status = printer_dll.GetStatus()
        logger.info(f"Printer status: {status}")
        
        return True
    except Exception as e:
        logger.error(f"Gagal inisialisasi printer: {str(e)}")
        return False

def print_barcode(barcode_data, product_name="", line_name=""):
    """
    Cetak barcode ke printer
    
    Args:
        barcode_data (str): Data barcode/QR code
        product_name (str): Nama produk (opsional)
        line_name (str): Nama line/workstation (opsional)
    
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    try:
        if printer_dll is None:
            logger.error("Printer DLL tidak dimuat")
            return False
        
        logger.info(f"Mulai cetak barcode: {barcode_data}")
        
        # Alignment center
        printer_dll.SetAlignment(2)
        
        # Set font size
        printer_dll.SetSizechar(2, 2, 0, 0)
        
        # ===== CETAK BARCODE =====
        barcode_bytes = barcode_data.encode('utf-8')
        printer_dll.PrintBarcode(barcode_bytes, 73, 2, 2, 0, 0)  # Code128 barcode
        
        # ===== CETAK NAMA PRODUK =====
        if product_name:
            printer_dll.PrintChargeRow()  # Line break
            printer_dll.SetAlignment(1)  # Left alignment
            printer_dll.SetSizetext(1, 2)
            product_bytes = product_name.encode('utf-8')
            printer_dll.PrintString(product_bytes, 0)
        
        # ===== CETAK LINE/WORKSTATION =====
        if line_name:
            printer_dll.PrintChargeRow()  # Line break
            printer_dll.SetAlignment(1)  # Left alignment
            printer_dll.SetSizetext(1, 1)
            line_bytes = line_name.encode('utf-8')
            printer_dll.PrintString(line_bytes, 0)
        
        # Feed paper
        printer_dll.PrintChargeRow()
        printer_dll.PrintChargeRow()
        
        # Cut paper
        printer_dll.PrintChargeRow()
        
        logger.info(f"Barcode berhasil dicetak: {barcode_data}")
        return True
        
    except Exception as e:
        logger.error(f"Error saat mencetak barcode: {str(e)}")
        return False

# ========================================================================
# MQTT CALLBACKS
# ========================================================================

def on_connect(client, userdata, flags, rc):
    """Callback saat terhubung ke MQTT broker"""
    global is_connected
    
    if rc == 0:
        logger.info("Terhubung ke MQTT broker")
        is_connected = True
        
        # Subscribe ke topic barcode
        client.subscribe(MQTT_TOPIC_BARCODE)
        logger.info(f"Subscribe ke topic: {MQTT_TOPIC_BARCODE}")
        
        # Publish status online
        client.publish(MQTT_TOPIC_STATUS, json.dumps({
            "status": "online",
            "timestamp": datetime.now().isoformat(),
            "message": "Printer ready"
        }))
    else:
        logger.error(f"Gagal terhubung ke broker. Code: {rc}")
        is_connected = False

def on_disconnect(client, userdata, rc):
    """Callback saat disconnected dari MQTT broker"""
    global is_connected
    is_connected = False
    logger.warning(f"Disconnected dari broker. Code: {rc}")

def on_message(client, userdata, msg):
    """Callback saat menerima message dari MQTT"""
    try:
        logger.info(f"Message diterima dari topic: {msg.topic}")
        logger.info(f"Payload: {msg.payload.decode()}")
        
        # Parse JSON payload
        payload = json.loads(msg.payload.decode())
        
        # Extract data
        barcode = payload.get("barcode", "")
        product = payload.get("product", "")
        line = payload.get("line", "")
        
        if not barcode:
            logger.warning("Barcode kosong dalam payload")
            publish_status("error", "Barcode kosong")
            return
        
        # Print barcode
        success = print_barcode(barcode, product, line)
        
        # Publish status
        if success:
            publish_status("success", f"Barcode '{barcode}' berhasil dicetak")
        else:
            publish_status("error", f"Gagal mencetak barcode '{barcode}'")
            
    except json.JSONDecodeError as e:
        logger.error(f"Error decode JSON: {str(e)}")
        publish_status("error", "Format JSON tidak valid")
    except Exception as e:
        logger.error(f"Error saat memproses message: {str(e)}")
        publish_status("error", f"Error: {str(e)}")

def on_log(client, userdata, level, buf):
    """Callback untuk logging MQTT"""
    if level == mqtt.MQTT_LOG_INFO:
        logger.debug(f"MQTT Info: {buf}")
    elif level == mqtt.MQTT_LOG_WARNING:
        logger.warning(f"MQTT Warning: {buf}")
    elif level == mqtt.MQTT_LOG_ERR:
        logger.error(f"MQTT Error: {buf}")

# ========================================================================
# HELPER FUNCTIONS
# ========================================================================

def publish_status(status_type, message):
    """Publish status ke MQTT"""
    try:
        if client and is_connected:
            payload = json.dumps({
                "status": status_type,
                "message": message,
                "timestamp": datetime.now().isoformat()
            })
            client.publish(MQTT_TOPIC_STATUS, payload)
    except Exception as e:
        logger.error(f"Gagal publish status: {str(e)}")

def connect_mqtt():
    """Hubung ke MQTT broker"""
    global client
    
    try:
        client = mqtt.Client("node_red_printer")
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message
        client.on_log = on_log
        
        logger.info(f"Menghubung ke MQTT broker: {BROKER_ADDRESS}:{BROKER_PORT}")
        client.connect(BROKER_ADDRESS, BROKER_PORT, keepalive=60)
        
        return True
    except Exception as e:
        logger.error(f"Gagal connect ke MQTT broker: {str(e)}")
        return False

# ========================================================================
# MAIN FUNCTION
# ========================================================================

def main():
    """Main function"""
    logger.info("="*70)
    logger.info("STARTING NODE-RED BARCODE PRINTER")
    logger.info("="*70)
    
    # Load printer DLL
    if not load_printer_dll():
        logger.error("Gagal memuat printer DLL. Program dihentikan.")
        return False
    
    # Initialize printer
    if not init_printer():
        logger.warning("Warning: Printer tidak siap, tapi program akan lanjut...")
    
    # Connect to MQTT
    if not connect_mqtt():
        logger.error("Gagal connect ke MQTT broker. Program dihentikan.")
        return False
    
    # Start MQTT loop
    client.loop_start()
    
    logger.info("Program berjalan. Menunggu message dari Node-RED...")
    logger.info(f"Subscribe ke topic: {MQTT_TOPIC_BARCODE}")
    logger.info(f"Publish status ke topic: {MQTT_TOPIC_STATUS}")
    
    try:
        # Keep program running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Program dihentikan oleh user")
        client.loop_stop()
        client.disconnect()
        return True
    except Exception as e:
        logger.error(f"Error dalam main loop: {str(e)}")
        client.loop_stop()
        client.disconnect()
        return False

# ========================================================================
# ENTRY POINT
# ========================================================================

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
