#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test koneksi dari Printer PC ke Node-RED PC
"""

import socket
import sys

NODE_RED_IP = "17.17.17.254"
MQTT_PORT = 1883

print("="*70)
print("TEST KONEKSI: PRINTER PC -> NODE-RED PC")
print("="*70)
print(f"\nTarget: {NODE_RED_IP}:{MQTT_PORT}")
print("\n" + "="*70)

# Test 1: Ping (ICMP)
print("\n[1] Testing PING...")
import subprocess
try:
    result = subprocess.run(
        ["ping", "-n", "4", NODE_RED_IP],
        capture_output=True,
        text=True,
        timeout=10
    )
    if "TTL=" in result.stdout or "Reply from" in result.stdout:
        print(f"    ✓ PING SUCCESS - PC {NODE_RED_IP} bisa dijangkau")
    else:
        print(f"    ✗ PING FAILED - PC {NODE_RED_IP} tidak merespon")
        print(f"    Output: {result.stdout[:200]}")
except Exception as e:
    print(f"    ✗ PING ERROR: {str(e)}")

# Test 2: TCP Connection ke port 1883
print(f"\n[2] Testing TCP connection ke port {MQTT_PORT}...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)

try:
    result = sock.connect_ex((NODE_RED_IP, MQTT_PORT))
    if result == 0:
        print(f"    ✓ PORT {MQTT_PORT} OPEN - Mosquitto berjalan!")
        sock.close()
    else:
        print(f"    ✗ PORT {MQTT_PORT} CLOSED/BLOCKED")
        print(f"    Kemungkinan:")
        print(f"       - Mosquitto belum diinstall di {NODE_RED_IP}")
        print(f"       - Mosquitto service tidak running")
        print(f"       - Firewall Windows block port 1883")
        sock.close()
except socket.timeout:
    print(f"    ✗ CONNECTION TIMEOUT")
    print(f"    Kemungkinan:")
    print(f"       - Firewall block port {MQTT_PORT}")
    print(f"       - Mosquitto config salah (tidak listen 0.0.0.0)")
    sock.close()
except Exception as e:
    print(f"    ✗ ERROR: {str(e)}")
    sock.close()

# Test 3: Hostname resolution
print(f"\n[3] Testing DNS resolution...")
try:
    hostname = socket.gethostbyaddr(NODE_RED_IP)
    print(f"    ✓ Hostname: {hostname[0]}")
except:
    print(f"    - Hostname tidak ditemukan (normal untuk IP lokal)")

print("\n" + "="*70)
print("SOLUSI:")
print("="*70)
print(f"""
Di komputer Node-RED ({NODE_RED_IP}):

1. Install Mosquitto:
   - Download: https://mosquitto.org/download/
   - Install dengan opsi "Install as Service"

2. Edit C:\\Program Files\\mosquitto\\mosquitto.conf
   Tambahkan baris:
   
   listener 1883 0.0.0.0
   allow_anonymous true

3. Restart Mosquitto service:
   
   net stop mosquitto
   net start mosquitto

4. Buka firewall untuk port 1883:
   
   netsh advfirewall firewall add rule name="Mosquitto MQTT" dir=in action=allow protocol=TCP localport=1883

5. Test ulang script ini

""")

print("="*70)
input("\nTekan Enter untuk keluar...")
