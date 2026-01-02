"""
Script untuk troubleshooting koneksi database
Test network connectivity dan MySQL server
"""

import socket
import pymysql
import subprocess
import platform

def test_ping(host):
    """Test ping ke server"""
    print(f"\n[1/4] Testing PING ke {host}...")
    
    # Windows menggunakan -n, Linux/Mac menggunakan -c
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    try:
        # Ping 4 kali
        result = subprocess.run(
            ['ping', param, '4', host],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"  ✓ PING BERHASIL - Host {host} dapat dijangkau")
            return True
        else:
            print(f"  ✗ PING GAGAL - Host {host} tidak dapat dijangkau")
            print(f"  Detail: {result.stdout}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ✗ PING TIMEOUT - Host {host} tidak merespon")
        return False
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        return False

def test_port(host, port=3306):
    """Test apakah port MySQL terbuka"""
    print(f"\n[2/4] Testing PORT {port} di {host}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"  ✓ PORT {port} TERBUKA - MySQL server listening")
            return True
        else:
            print(f"  ✗ PORT {port} TERTUTUP - MySQL server tidak listening atau firewall block")
            return False
    except socket.timeout:
        print(f"  ✗ PORT {port} TIMEOUT - Tidak dapat terhubung")
        return False
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        return False

def test_mysql_connection(host, user, password, database):
    """Test koneksi MySQL dengan credentials"""
    print(f"\n[3/4] Testing MySQL CONNECTION...")
    print(f"  Host: {host}")
    print(f"  User: {user}")
    print(f"  Database: {database}")
    
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            connect_timeout=10,
            charset='utf8mb4'
        )
        
        print(f"  ✓ KONEKSI BERHASIL")
        
        # Test simple query
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"  MySQL Version: {version[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except pymysql.err.OperationalError as e:
        error_code, error_msg = e.args
        print(f"  ✗ KONEKSI GAGAL (Error {error_code})")
        
        if error_code == 2003:
            print(f"  Penyebab: Server tidak dapat dijangkau atau port tertutup")
            print(f"  Solusi: ")
            print(f"    - Cek MySQL service running di server")
            print(f"    - Cek firewall di server membuka port 3306")
            print(f"    - Pastikan IP {host} benar")
        elif error_code == 1045:
            print(f"  Penyebab: Username atau password salah")
            print(f"  Solusi: Verifikasi credentials")
        elif error_code == 1049:
            print(f"  Penyebab: Database '{database}' tidak ada")
            print(f"  Solusi: Buat database atau cek nama database")
        else:
            print(f"  Detail: {error_msg}")
        
        return False
    
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        return False

def test_database_table(host, user, password, database, table):
    """Test apakah table ada di database"""
    print(f"\n[4/4] Testing TABLE '{table}'...")
    
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            connect_timeout=10
        )
        
        cursor = connection.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table}'")
        result = cursor.fetchone()
        
        if result:
            print(f"  ✓ TABLE '{table}' DITEMUKAN")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  Total baris: {count}")
            
            cursor.close()
            connection.close()
            return True
        else:
            print(f"  ✗ TABLE '{table}' TIDAK DITEMUKAN")
            
            # List available tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            if tables:
                print(f"  Table yang tersedia:")
                for tbl in tables:
                    print(f"    - {tbl[0]}")
            
            cursor.close()
            connection.close()
            return False
    
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        return False

def main():
    print("=" * 70)
    print("DATABASE CONNECTION TROUBLESHOOTING")
    print("=" * 70)
    
    # Konfigurasi
    HOST = '192.168.12.250'
    PORT = 3306
    USER = 'admin-reka'
    PASSWORD = 'J@debx132'
    DATABASE = 'ppc_reka'
    TABLE = 'production_schedule'
    
    print(f"\nTarget Server:")
    print(f"  IP: {HOST}")
    print(f"  Port: {PORT}")
    print(f"  Database: {DATABASE}")
    
    # Run tests
    test_results = []
    
    test_results.append(("PING", test_ping(HOST)))
    test_results.append(("PORT", test_port(HOST, PORT)))
    test_results.append(("MySQL Connection", test_mysql_connection(HOST, USER, PASSWORD, DATABASE)))
    test_results.append(("Table Check", test_database_table(HOST, USER, PASSWORD, DATABASE, TABLE)))
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    for test_name, result in test_results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {test_name:20} : {status}")
    
    print("\n" + "=" * 70)
    
    # Recommendations
    failed_tests = [name for name, result in test_results if not result]
    
    if not failed_tests:
        print("\n✅ SEMUA TEST BERHASIL - Database siap digunakan!")
    else:
        print("\n❌ ADA MASALAH YANG PERLU DIPERBAIKI:")
        print("\nRekomendasi:")
        
        if "PING" in failed_tests:
            print("\n1. PING GAGAL:")
            print(f"   - Verifikasi IP address: {HOST}")
            print(f"   - Cek koneksi network")
            print(f"   - Pastikan server hidup")
            print(f"   - Test: ping {HOST} -n 10")
        
        if "PORT" in failed_tests:
            print("\n2. PORT TERTUTUP:")
            print(f"   - Cek MySQL service running di server")
            print(f"   - Cek firewall server (Windows Firewall / iptables)")
            print(f"   - Cek MySQL bind-address di my.cnf")
            print(f"   - Test dari server: netstat -an | findstr 3306")
        
        if "MySQL Connection" in failed_tests:
            print("\n3. KONEKSI GAGAL:")
            print(f"   - Verifikasi username: {USER}")
            print(f"   - Verifikasi password")
            print(f"   - Cek user permissions: GRANT ALL ON {DATABASE}.* TO '{USER}'@'%'")
        
        if "Table Check" in failed_tests:
            print("\n4. TABLE TIDAK ADA:")
            print(f"   - Verifikasi nama table: {TABLE}")
            print(f"   - Import database schema jika belum")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh user")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
    finally:
        input("\nTekan Enter untuk keluar...")
