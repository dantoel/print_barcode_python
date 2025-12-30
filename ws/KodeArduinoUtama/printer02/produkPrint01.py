import pymysql
from datetime import datetime
from datetime import date
from datetime import timedelta
from time import sleep
import sys              #sistem
import string, datetime
import os
from ctypes import *
import os.path




connect = pymysql.connect(user='root', password='',
                              host='192.168.10.173',
                              database='reka')
cursor =connect.cursor()

def periksaDataBaru(cur00):
  q00="select count(*) from produkprint where waktu02 is null"
  cur00.execute(q00)
  tabel00=cur00.fetchone()
  jml00=int(tabel00[0])
  return jml00

def ambilDataPrint(cur00, con00):
  q00="SELECT A0.produk, A0.waktu01, A1.job, A2.jenisCar, A2.jenisProduk, \
  A3.namaJnsPrd FROM produkprint A0 LEFT JOIN produk A1 ON \
  A0.produk=A1.id LEFT JOIN job A2 ON A1.job=A2.idJob LEFT JOIN \
  jenisproduk A3 ON A2.jenisProduk=A3.idJnsPrd WHERE waktu02 IS NULL \
  ORDER BY waktu01 LIMIT 1"
  cur00.execute(q00)
  tabel00=cur00.fetchone()
  idPrd00=tabel00[0]
  wkt01=tabel00[1]
  car01=tabel00[3]
  nama=tabel00[5]
  id01=idPrd00[0:5]
  id02=idPrd00[-7:]
  id03=id01+id02
  q01="update produkprint set waktu02=current_timestamp where \
      waktu01='"+str(wkt01)+"'"
  cur00.execute(q01)
  con00.commit()
  return id03, car01, nama

def cetakBarcode01(id1, nama, ws):
    id1=id1.strip()
    balik=0
    global cetakGagal
    try:        
        barcode = id1
        name = nama
        ws1 = ws
        
        mydll = cdll.LoadLibrary("C:\\ws\\KodeArduinoUtama\\printer02\\Msprintsdk.dll")
        print('sampai sini')
        setting = mydll.SetUsbportauto()
        print(setting)
        setting2 = mydll.SetInit()
        print(setting2)
        mydll.SetClean()
        
        mydll.SetAlignment(2)
        mydll.SetSizechar(2,2,0,0)
        print("status "+str(mydll.GetStatus()))
        
        string1 = barcode
        string2 = name
        string3 = " " + ws1
        b_string1 = string1.encode('utf-8')
        b_string2 = string2.encode('utf-8')
        b_string3 = string3.encode('utf-8')

        mydll.SetAlignment(1)
        mydll.SetSizetext(0,0)
        mydll.PrintString(b_string3,0)
        mydll.PrintChargeRow()
        mydll.SetSizetext(1,2)
        mydll.PrintString(b_string2,0)
        print(mydll.Print1Dbar(2,60,1,2,4,b_string1))
        mydll.PrintChargeRow()
        mydll.PrintChargeRow()
        mydll.PrintChargeRow()
        mydll.PrintChargeRow()
        mydll.PrintChargeRow()
        mydll.PrintCutpaper(1)
        #mydll.SetMarkoffsetcut(0)
        #mydll.PrintMarkcutpaper(1)
        #mydll.PrintCutpaper(1)
        #mydll.PrintCutpaper(0)
        #print(r)
        mydll.SetClose()
        
                
        global statusCetak
        sleep(10)
        print("Berhasil print")
##        tulis_lcd("3")
##        tulis_buzzer("1")
        
    except Exception as e:
        print(e)
##        tulis_lcd("4")
##        tulis_buzzer("2")
        print("gagal cetak barcode")
        sleep(5)    
        #os.remove(""+id1+".png")
    return balik

def cetakBarcode(cur00, con00):
  jml=periksaDataBaru(cur00)
  if(jml>0):
    hasil=ambilDataPrint(cur00, con00)
    idSps=hasil[0]
    nama=hasil[1]
    lini=hasil[2]
    cetakBarcode01(idSps, nama, lini)

angka=0
while True:
  connect.commit()
  cetakBarcode(cursor, connect)
  angka=angka+1
  if(angka>99):
    angka=0
  print("-----",angka,"-----")
  sleep(1)
