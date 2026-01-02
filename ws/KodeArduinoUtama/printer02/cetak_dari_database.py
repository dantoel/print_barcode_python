"""
Script untuk mencetak barcode dari database MySQL
Terhubung ke production_schedule dan otomatis print item dengan status 'Ready'
"""

import sys
import os
from ctypes import *
from time import sleep
import traceback
import pymysql
from datetime import datetime

# ============================================================================
# KONFIGURASI DATABASE
# ============================================================================
DB_CONFIG = {
    'host': '192.168.12.250',
    'user': 'admin-reka',
    'password': 'J@debx132',
    'database': 'ppc_reka',  # Database production
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# ============================================================================
# PATH PRINTER DLL
# ============================================================================
DLL_PATH = r"C:\ws\KodeArduinoUtama\printer02\Msprintsdk.dll"

# ============================================================================
# LOG FILE
# ============================================================================
LOG_FILE = r"C:\ws\KodeArduinoUtama\printer02\cetak_log.txt"

def write_log(message):
    """Tulis message ke log file dan console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    
    print(log_message)
    
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_message + "\n")
    except Exception as e:
        print(f"WARNING: Tidak bisa write log: {e}")

def connect_database(debug=False):
    """
    Koneksi ke database MySQL dengan autocommit enabled
    
    Returns:
        tuple: (connection, cursor) atau (None, None) jika gagal
    """
    if debug:
        print("\n[DATABASE] Menghubungkan ke database...")
        print(f"  Host: {DB_CONFIG['host']}")
        print(f"  User: {DB_CONFIG['user']}")
        print(f"  Database: {DB_CONFIG['database']}")
    
    try:
        # Tambahkan autocommit=True untuk menghindari packet sequence error
        config = DB_CONFIG.copy()
        connection = pymysql.connect(**config)
        connection.autocommit(True)  # Enable autocommit
        cursor = connection.cursor()
        
        if debug:
            print(f"  ✓ Koneksi berhasil")
        
        write_log("✓ Koneksi database berhasil")
        return connection, cursor
    
    except pymysql.Error as db_error:
        error_msg = f"✗ GAGAL koneksi database: {db_error}"
        print(error_msg)
        write_log(error_msg)
        return None, None
    
    except Exception as e:
        error_msg = f"✗ ERROR: {e}"
        print(error_msg)
        write_log(error_msg)
        return None, None

def query_data_siap_cetak(cursor, debug=False):
    """
    Query data dari production_schedule dengan status 'Ready'
    
    Returns:
        list: List of dict berisi id_product, product, dan data lainnya
    """
    query = """
        SELECT 
            id_product,
            product,
            line,
            production_proggress
        FROM production_schedule
        WHERE production_proggress = 'Ready'
        ORDER BY id_product ASC
    """
    
def query_data_siap_cetak(cursor, debug=False):
    """
    Query data dari production_schedule dengan status 'Ready'
    
    Returns:
        list: List of dict berisi id_product, product, dan data lainnya
    """
    query = """
        SELECT 
            id_product,
            product,
            line,
            production_proggress
        FROM production_schedule
        WHERE production_proggress = 'Ready'
        ORDER BY id_product ASC
    """
    
    if debug:
        print("\n[DATABASE] Menjalankan query...")
        print(f"  Query: {query}")
    
    try:
        # Ping connection untuk memastikan masih hidup
        try:
            connection.ping(reconnect=True)
        except:
            pass
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if debug:
            print(f"  ✓ Query berhasil, ditemukan {len(rows)} record")
        
        if len(rows) > 0:
            write_log(f"✓ Query berhasil, ditemukan {len(rows)} data siap cetak")
        else:
            write_log("ℹ Tidak ada data dengan status 'Ready' untuk dicetak")
        
        return rows
    
    except pymysql.Error as db_error:
        error_msg = f"✗ ERROR Query: {db_error}"
        print(error_msg)
        write_log(error_msg)
        # Close and reconnect on error
        try:
            cursor.close()
        except:
            pass
        return []
    
    except Exception as e:
        error_msg = f"✗ ERROR: {e}"
        print(error_msg)
        write_log(error_msg)
        return []
        print(error_msg)
        write_log(error_msg)
        return []

def cetakBarcode01(id_product, product_name, line="Line 1", debug=False):
    """
    Fungsi cetak barcode ke printer thermal
    
    Args:
        id_product: Barcode value dari database
        product_name: Nama produk dari database
        line: Kode line/workstation
        debug: Enable debug mode
    
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    id_product = str(id_product).strip()
    product_name = str(product_name).strip()
    line = str(line).strip()
    
    try:
        if debug:
            print(f"\n[PRINTER] Mencetak barcode:")
            print(f"  - ID Product: {id_product}")
            print(f"  - Nama Produk: {product_name}")
            print(f"  - Line: {line}")
        
        # Check DLL file exists
        if debug:
            print(f"\n[PRINTER] Checking DLL file: {DLL_PATH}")
            print(f"  - Exists: {os.path.exists(DLL_PATH)}")
        
        if not os.path.exists(DLL_PATH):
            error_msg = f"✗ DLL file tidak ditemukan: {DLL_PATH}"
            print(error_msg)
            write_log(error_msg)
            return False
        
        # Load DLL
        if debug:
            print(f"[PRINTER] Loading DLL...")
        
        try:
            mydll = cdll.LoadLibrary(DLL_PATH)
            if debug:
                print(f"  ✓ DLL loaded successfully")
        except OSError as dll_error:
            error_msg = f"✗ FAILED to load DLL: {dll_error}"
            print(error_msg)
            write_log(error_msg)
            return False
        
        # Printer initialization
        if debug:
            print(f"[PRINTER] Initializing printer...")
        
        try:
            setting = mydll.SetUsbportauto()
            if debug:
                print(f"  - SetUsbportauto(): {setting}")
            
            setting2 = mydll.SetInit()
            if debug:
                print(f"  - SetInit(): {setting2}")
            
            mydll.SetClean()
            mydll.SetAlignment(2)
            mydll.SetSizechar(2, 2, 0, 0)
            
            status = mydll.GetStatus()
            if debug:
                print(f"  - Printer Status: {status}")
        
        except AttributeError as attr_error:
            error_msg = f"✗ Printer function not found: {attr_error}"
            print(error_msg)
            write_log(error_msg)
            return False
        
        # Prepare strings
        if debug:
            print(f"[PRINTER] Preparing strings...")
        
        string1 = id_product
        string2 = product_name
        string3 = " " + line
        
        try:
            b_string1 = string1.encode('utf-8')
            b_string2 = string2.encode('utf-8')
            b_string3 = string3.encode('utf-8')
        
        except UnicodeEncodeError as encode_error:
            error_msg = f"✗ String encoding error: {encode_error}"
            print(error_msg)
            write_log(error_msg)
            return False
        
        # Execute print commands
        if debug:
            print(f"[PRINTER] Executing print commands...")
        
        try:
            mydll.SetAlignment(1)
            mydll.SetSizetext(0, 0)
            mydll.PrintString(b_string3, 0)
            mydll.PrintChargeRow()
            
            mydll.SetSizetext(1, 2)
            mydll.PrintString(b_string2, 0)
            
            barcode_result = mydll.Print1Dbar(2, 60, 1, 2, 4, b_string1)
            if debug:
                print(f"  - Print1Dbar() returned: {barcode_result}")
            
            mydll.PrintChargeRow()
            mydll.PrintChargeRow()
            mydll.PrintChargeRow()
            mydll.PrintChargeRow()
            mydll.PrintChargeRow()
            mydll.PrintCutpaper(1)
            mydll.SetClose()
        
        except Exception as print_error:
            error_msg = f"✗ Print error: {print_error}"
            print(error_msg)
            write_log(error_msg)
            return False
        
        sleep(2)
        
        success_msg = f"✓ Cetak BERHASIL: {id_product} - {product_name}"
        print(success_msg)
        write_log(success_msg)
        
        return True
    
    except Exception as e:
        error_msg = f"✗ ERROR (Unexpected): {e}\n{traceback.format_exc()}"
        print(error_msg)
        write_log(error_msg)
        return False

def update_status_setelah_cetak(connection, cursor, id_product, debug=False):
    """
    Update status production_proggress setelah berhasil cetak
    
    Opsional: Ubah ke status 'Printed' atau status lain sesuai flow bisnis Anda
    """
    try:
        # PERHATIAN: Sesuaikan query ini dengan kolom dan nilai status yang sesuai
        # Saat ini commented, uncomment jika ingin auto-update status
        
        # query = f"UPDATE production_schedule SET production_proggress = 'Printed' WHERE id_product = '{id_product}'"
        # cursor.execute(query)
        # connection.commit()
        # write_log(f"✓ Status updated untuk {id_product}")
        
        pass
    
    except Exception as e:
        write_log(f"⚠ WARNING: Tidak bisa update status: {e}")

def main_loop(debug=False, limit=None):
    """
    Main loop: Koneksi DB -> Query data -> Print -> Loop
    
    Args:
        debug: Enable debug mode
        limit: Batasi jumlah item yang dicetak (None = unlimited)
    """
    write_log("=" * 70)
    write_log("STARTING PRINT FROM DATABASE")
    write_log("=" * 70)
    
    if debug:
        print("\n" + "="*70)
        print("DEBUG MODE: ENABLED")
        print("="*70)
    
    # Connect to database
    connection, cursor = connect_database(debug=debug)
    
    if connection is None or cursor is None:
        print("\n✗ Gagal terhubung ke database. Keluar.")
        write_log("✗ Gagal terhubung ke database. Program dihentikan.")
        return False
    
    try:
        # Query data siap cetak
        data_list = query_data_siap_cetak(cursor, debug=debug)
        
        if len(data_list) == 0:
            print("\n✓ Tidak ada data dengan status 'Ready' untuk dicetak")
            write_log("✓ Program selesai - tidak ada data Ready")
            return True
        
        # Print data summary
        print(f"\n{'='*70}")
        print(f"Ditemukan {len(data_list)} data siap cetak:")
        print(f"{'='*70}")
        for idx, row in enumerate(data_list, 1):
            print(f"{idx}. {row['id_product']} - {row['product']}")
        print(f"{'='*70}\n")
        
        # Confirm print
        if limit is None and len(data_list) > 1:
            response = input(f"\nCetak semua {len(data_list)} item? (y/n): ").strip().lower()
            if response != 'y':
                print("Dibatalkan oleh user")
                write_log("Dibatalkan oleh user")
                return False
        
        # Print each item
        cetak_count = 0
        for idx, row in enumerate(data_list, 1):
            if limit and idx > limit:
                print(f"\nBerhenti di item {idx-1} (limit={limit})")
                break
            
            id_product = row['id_product']
            product = row['product']
            line = row.get('line', 'Line 1')
            
            print(f"\n[{idx}/{len(data_list)}] Mencetak: {id_product} - {product}")
            
            if cetakBarcode01(id_product, product, line, debug=debug):
                cetak_count += 1
                # Uncomment untuk auto-update status setelah cetak
                # update_status_setelah_cetak(connection, cursor, id_product, debug=debug)
            else:
                print(f"  ✗ GAGAL mencetak {id_product}")
            
            sleep(1)
        
        # Summary
        print(f"\n{'='*70}")
        print(f"SUMMARY:")
        print(f"  Total Data: {len(data_list)}")
        print(f"  Berhasil Cetak: {cetak_count}")
        print(f"  Gagal: {len(data_list) - cetak_count}")
        print(f"{'='*70}\n")
        
        write_log(f"SUMMARY: Total={len(data_list)}, Berhasil={cetak_count}, Gagal={len(data_list)-cetak_count}")
        
        return True
    
    except Exception as e:
        error_msg = f"✗ ERROR: {e}\n{traceback.format_exc()}"
        print(error_msg)
        write_log(error_msg)
        return False
    
    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            write_log("Database connection closed")
        except Exception as close_error:
            write_log(f"Warning: Error saat close connection: {close_error}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Cetak barcode dari production_schedule database')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--limit', type=int, help='Limit jumlah item yang dicetak')
    
    args = parser.parse_args()
    
    try:
        success = main_loop(debug=args.debug, limit=args.limit)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh user (Ctrl+C)")
        write_log("Program dihentikan oleh user (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        traceback.print_exc()
        write_log(f"FATAL ERROR: {e}")
        sys.exit(1)
    finally:
        # Pause sebelum exit jika dijalankan dari Windows Explorer
        if sys.argv[0].endswith('.py'):
            input("\nTekan Enter untuk keluar...")
