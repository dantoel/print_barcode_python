##import pymysql
from datetime import datetime
##from datetime import date
##from datetime import timedelta
from time import sleep
import sys              #sistem
import string, datetime
import os
from ctypes import *
import os.path



##connect = pymysql.connect(user='root', password='',
##                              host='192.168.10.173',
##                              database='reka')
##cursor =connect.cursor()

def periksaDataBaru(cur00):
  q00="select count(*) from spsprint where waktu02 is null"
  cur00.execute(q00)
  tabel00=cur00.fetchone()
  jml00=int(tabel00[0])
  return jml00

def ambilDataPrint(cur00, con00):
  jml00=periksaDataBaru(cur00)
  if(jml00>0):
    q01="select * from spsprint where waktu02 is null order by waktu01"
    cur00.execute(q01)
    tabel01=cur00.fetchone()
    sps01=tabel01[0]
    wkt01=tabel01[1]
    q02="SELECT distinct B0.id, B0.jnsProduk, B0.namaJnsPrd, B1.nama lini \
        FROM (SELECT A0.id, A0.jnsProduk, A1.namaJnsPrd FROM sps A0 \
        LEFT JOIN jenisproduk A1 ON A0.jnsProduk=A1.idJnsPrd)B0 LEFT JOIN \
        (SELECT A0.proses, A1.jenisProduk, A2.stasiunKerja, A3.liniProduksi, \
        A4.nama FROM operasi A0 LEFT JOIN proses A1 ON A0.proses=A1.idProses \
        LEFT JOIN penugasanstasiunkerja A2 ON A0.proses=A2.proses \
        LEFT JOIN stasiunkerja A3 ON A2.stasiunKerja=A3.idStasiunKerja \
        LEFT JOIN liniproduksi A4 ON A3.liniProduksi=A4.idLiniProduksi \
        WHERE A2.akhir IS NULL)B1 ON B0.jnsProduk=B1.jenisProduk \
        WHERE B0.id='"+sps01+"' limit 1"
    cur00.execute(q02)
    tabel02=cur00.fetchone()
    idSps=tabel02[0]
    nama=tabel02[2]
    lini=tabel02[3]
    q03="update spsprint set waktu02=current_timestamp where \
         waktu01='"+str(wkt01)+"'"
    cur00.execute(q03)
    con00.commit()
    return idSps, nama, lini

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
        mydll.SetSizetext(1,3)
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

##angka=0
##while True:
##  connect.commit()
##  cetakBarcode(cursor, connect)
##  angka=angka+1
##  if(angka>99):
##    angka=0
##  print("-----",angka,"-----")
##  sleep(1)
  
  
  
##cetakBarcode(cursor, connect)
