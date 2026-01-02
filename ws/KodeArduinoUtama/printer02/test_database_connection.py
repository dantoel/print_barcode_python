"""
Test script untuk mengecek koneksi database
Jalankan script ini untuk memastikan database connection bekerja dengan baik
"""

import sys
import pymysql
from datetime import datetime

def write_log(message):
    """Print dan log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)

def test_connection():
    """Test database connection"""
    
    write_log("=" * 70)
    write_log("TEST DATABASE CONNECTION")
    write_log("=" * 70)
    write_log("")
    
    # Konfigurasi
    config = {
        'host': '192.168.12.250',
        'user': 'admin-reka',
        'password': 'J@debx132',
        'database': 'ppc_reka',
        'charset': 'utf8mb4',
    }
    
    write_log("Konfigurasi:")
    write_log(f"  Host: {config['host']}")
    write_log(f"  User: {config['user']}")
    write_log(f"  Database: {config['database']}")
    write_log("")
    
    # Test 1: Connection
    write_log("[1/3] Testing basic connection...")
    try:
        connection = pymysql.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset=config['charset']
        )
        write_log("  ✓ Connection BERHASIL")
        connection.close()
    except pymysql.Error as e:
        write_log(f"  ✗ Connection GAGAL: {e}")
        return False
    except Exception as e:
        write_log(f"  ✗ ERROR: {e}")
        return False
    
    write_log("")
    
    # Test 2: Select query
    write_log("[2/3] Testing SELECT query...")
    try:
        connection = pymysql.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset=config['charset'],
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM production_schedule")
        result = cursor.fetchone()
        total_rows = result['total']
        
        write_log(f"  ✓ Query BERHASIL - Total baris: {total_rows}")
        
        cursor.close()
        connection.close()
    except pymysql.Error as e:
        write_log(f"  ✗ Query GAGAL: {e}")
        return False
    except Exception as e:
        write_log(f"  ✗ ERROR: {e}")
        return False
    
    write_log("")
    
    # Test 3: Check data Ready
    write_log("[3/3] Checking data dengan status 'Ready'...")
    try:
        connection = pymysql.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset=config['charset'],
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = connection.cursor()
        
        query = """
            SELECT 
                id_product,
                product,
                production_proggress
            FROM production_schedule
            WHERE production_proggress = 'Ready'
            LIMIT 10
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if len(rows) > 0:
            write_log(f"  ✓ Ditemukan {len(rows)} data dengan status 'Ready':")
            for idx, row in enumerate(rows, 1):
                write_log(f"      {idx}. {row['id_product']} - {row['product']}")
        else:
            write_log(f"  ℹ Tidak ada data dengan status 'Ready'")
        
        cursor.close()
        connection.close()
    except pymysql.Error as e:
        write_log(f"  ✗ Query GAGAL: {e}")
        return False
    except Exception as e:
        write_log(f"  ✗ ERROR: {e}")
        return False
    
    write_log("")
    write_log("=" * 70)
    write_log("✓ SEMUA TEST BERHASIL")
    write_log("=" * 70)
    write_log("")
    
    return True

if __name__ == "__main__":
    try:
        success = test_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh user")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
    finally:
        input("\nTekan Enter untuk keluar...")
