#!/usr/bin/env python3
"""
Test Internet Connection dan MQTT Broker Connectivity
"""

import socket
import sys
import time

def test_internet():
    """Test general internet connection"""
    print("="*60)
    print("TEST 1: Internet Connection")
    print("="*60)
    
    try:
        # Try to resolve DNS
        result = socket.gethostbyname("google.com")
        print("✓ DNS Resolution: OK")
        print(f"  Google IP: {result}")
        return True
    except Exception as e:
        print(f"✗ DNS Resolution: FAILED")
        print(f"  Error: {str(e)}")
        print("\nSolusi:")
        print("- Pastikan PC terkoneksi ke internet")
        print("- Cek router/WiFi")
        print("- Cek DNS settings")
        return False

def test_mqtt_broker(broker, port=1883):
    """Test MQTT broker connectivity"""
    print("\n" + "="*60)
    print(f"TEST 2: MQTT Broker ({broker}:{port})")
    print("="*60)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        result = sock.connect_ex((broker, port))
        sock.close()
        
        if result == 0:
            print(f"✓ MQTT Broker: ONLINE")
            print(f"  Broker: {broker}:{port}")
            return True
        else:
            print(f"✗ MQTT Broker: OFFLINE atau BLOCKED")
            print(f"  Broker: {broker}:{port}")
            print(f"  Error Code: {result}")
            
            if result == 11001:
                print("\nKemungkinan: DNS Resolution Failed")
            elif result == 110 or result == 10060:
                print("\nKemungkinan: Connection Timeout (Firewall?)")
            
            return False
    except Exception as e:
        print(f"✗ Connection Test FAILED")
        print(f"  Error: {str(e)}")
        return False

def test_firewall():
    """Suggest firewall rules"""
    print("\n" + "="*60)
    print("TEST 3: Firewall Rules")
    print("="*60)
    print("\nJika broker timeout, coba buka firewall:")
    print("\nRun as Administrator di PowerShell:")
    print("""
New-NetFirewallRule -DisplayName "MQTT 1883 Outbound" `
  -Direction Outbound -Protocol TCP -RemotePort 1883 -Action Allow

New-NetFirewallRule -DisplayName "MQTT 8883 Outbound" `
  -Direction Outbound -Protocol TCP -RemotePort 8883 -Action Allow
""")

def main():
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║    MQTT Broker Connectivity Diagnostic Tool               ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Test 1: Internet
    internet_ok = test_internet()
    
    if not internet_ok:
        print("\n⚠️  Internet tidak terhubung!")
        print("Tidak bisa proceed dengan test MQTT")
        return False
    
    # Test 2: HiveMQ Broker
    hivemq_ok = test_mqtt_broker("broker.hivemq.com", 1883)
    
    # Test 3: Alternative Broker
    mosquitto_ok = test_mqtt_broker("test.mosquitto.org", 1883)
    
    # Test 4: Firewall suggestion
    test_firewall()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Internet Connection: {'OK' if internet_ok else 'FAILED'}")
    print(f"HiveMQ Broker: {'OK' if hivemq_ok else 'FAILED'}")
    print(f"Mosquitto Broker: {'OK' if mosquitto_ok else 'FAILED'}")
    
    print("\nRekomendasi:")
    if internet_ok and hivemq_ok:
        print("✓ Setup OK - Gunakan broker.hivemq.com")
    elif internet_ok and mosquitto_ok:
        print("⚠️  HiveMQ down - Gunakan test.mosquitto.org sebagai alternative")
    else:
        print("✗ Koneksi gagal - Cek internet dan firewall")
    
    print("\n")

if __name__ == "__main__":
    main()
