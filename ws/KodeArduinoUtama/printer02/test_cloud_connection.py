#!/usr/bin/env python3
"""Quick test koneksi ke HiveMQ Cloud Broker"""

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ BERHASIL connect ke broker.hivemq.com!")
        print("   Cloud MQTT broker siap digunakan!")
        client.disconnect()
    else:
        print(f"❌ Gagal connect. Error code: {rc}")

print("Testing koneksi ke HiveMQ Cloud Broker...")
print("Broker: broker.hivemq.com:1883")
print("")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "test_connection")
client.on_connect = on_connect

try:
    print("Connecting...")
    client.connect("broker.hivemq.com", 1883, 60)
    client.loop_start()
    time.sleep(3)
    client.loop_stop()
    print("\nTest selesai!")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\nPastikan PC terkoneksi ke internet!")
