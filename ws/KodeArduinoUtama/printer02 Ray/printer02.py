##import pymssql          #koneksi remote ke database
import modulKonektor01
##import broker
import sys              #sistem
import string, datetime
from time import sleep
import os
from ctypes import *
import os.path

connect = modulKonektor01.connect
cursor = modulKonektor01.connect.cursor()



def tulis_lcd(msg):
    file = open("C:\\KodeArduinoUtama\\lcd_msg.txt", 'w')
    file.write(msg)
    file.close()
 
def tulis_buzzer(msg):
    file = open("C:\\KodeArduinoUtama\\buzzer_msg.txt", 'w')
    file.write(msg)
    file.close()


#beberapa definisi fungsi bukan peringatan    

def hitungJumlahData(ws1):
  ws1=ws1.strip()
  q00="select count(*) from MAT_D_STATUSBARCODE where printTime is null and workstation='"+ws1+"'"
  #q00="select count(*) from MAT_D_STATUSBARCODE where printTime is null"
  cursor.execute(q00)
  tabel0=cursor.fetchall()
  balikS=str(tabel0[0][0])
  balik=int(balikS)
  return balik

def cariIdMaterialPrint(ws1):
  ws1=ws1.strip()
  id1=""
  try:
    q00="select top 1 * from MAT_D_STATUSBARCODE where printTime is null and workstation='"+ws1+"' order by ID"
#     q00="select top 1 * from MAT_D_STATUSBARCODE where printTime is null order by ID"
    cursor.execute(q00)
    tabel0=cursor.fetchall()  
    id1=str(tabel0[0][0])
    id1=id1.strip()
  except:
    print("Gagal mencari material")
    tulis_lcd("1 ")
    tulis_buzzer("2")
    sleep(4)
  return id1

def cariNamaMaterial(id1):
  nama=""
  id1=id1.strip()
  try:
      q00="SELECT C.nama FROM mat_r_materialtype c,(SELECT A.materialTypeCode OwO FROM mat_d_materialstock A WHERE A.id='"
      q00=q00+id1+"')B WHERE B.OwO=C.code"
##      q00="select top 1 A1.ID, A1.MAT from (select A.ID, A.PURCHASEID, A.[ORDER], B.MATERIALTYPECODE MAT1, C.IDNODEOUTPUT, "
##      q00=q00+"D.MATERIALTYPECODE, E.NAME NAME1, F.NAME NAME2, case when E.NAME is not null then E.NAME when F.NAME is not null then "
##      q00=q00+"F.NAME end MAT from MAT_D_MATERIALSTOCK A left join MAT_D_PURCHASEITEM B on A.PURCHASEID=B.PURCHASEID and "
##      q00=q00+"A.[ORDER]=B.ID left join PRD_D_OPERATION C on A.ID=C.OPERATIONOUTPUT left join PRD_R_PRODUCTTYPESTRUCTURE D on "
##      q00=q00+"C.IDNODEOUTPUT=D.IDNODE left join MAT_R_MATERIALTYPE E on B.MATERIALTYPECODE=E.CODE left join "
##      q00=q00+"PRD_R_PRODUCTTYPESTRUCTURE F on C.IDNODEOUTPUT=F.IDNODE and D.MATERIALTYPECODE=F.MATERIALTYPECODE)A1 where A1.ID='"
##      q00=q00+id1+"'"
      cursor.execute(q00)
      tabel0=cursor.fetchall()
      nama=str(tabel0[0][1])      
  except:
      print("Gagal mencari nama material")
      tulis_lcd("2")
      tulis_buzzer("2")
      sleep(4)
  return nama

def updateStatusPrint(id1):
  try:
      id1=id1.strip()
      q00="update mat_d_statusBarcode set printTime=current_timestamp where id='"+id1+"'"      
      cursor.execute(q00)
      connection.commit()
      print("coba try")
  except:
      #programGagalStatusBarcode()
      print("coba except")
      sleep(4)

def cetakBarcode(id1, nama, ws):
    id1=id1.strip()
    balik=0
    global cetakGagal
    try:        
        barcode = id1
        name = nama
        ws1 = ws
        
        mydll = cdll.LoadLibrary("C:\\KodeArduinoUtama\\printer02\\Msprintsdk.dll")
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
        mydll.SetSizetext(2,4)
        mydll.PrintString(b_string3,0)
        mydll.PrintChargeRow()
        mydll.SetSizetext(1,1)
        mydll.PrintString(b_string2,0)
        print(mydll.Print1Dbar(2,50,1,2,4,b_string1))
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
        tulis_lcd("3")
        tulis_buzzer("1")
        updateStatusPrint(id1)
        
    except Exception as e:
        print(e)
        tulis_lcd("4")
        tulis_buzzer("2")
        print("gagal cetak barcode")
        sleep(5)    
        #os.remove(""+id1+".png")
    return balik
    
def my_callback(evt):
    global statusCetak
    print(evt.description)
    if(evt.description == "Job completed."):
        statusCetak = 1
    else:
        statusCetak = 0
    
##program untuk ws
file = open(r"C:\KodeArduinoUtama\data_ws.txt","r")
lines = file.readlines()
ws1 = str(lines[7])


chekKoneksi=0
hitung00=0
delta=1
chekDataMate=0
statusCetak=0
cetakGagal = 0

while(True):
  hitung00=0
  try:
    connect = modulKonektor01.connect
    cursor = modulKonektor01.connect.cursor()
    chekKoneksi=1
    print("koneksi berhasil")
    print("")    
  except:    
    hitung00=5
    print("koneksi gagal")
    sleep(5)

   
  while(hitung00<5):
        try:
            print("iterasi ke = ",hitung00)
            jmlData=hitungJumlahData(ws1)
            print("jumlah data = ", jmlData)

            if(jmlData>0):
                id1=cariIdMaterialPrint(ws1)
                print("id1 = ",id1)
                if(id1!=""):
                    nama=cariNamaMaterial(id1)
                    print("nama = ", nama)
                    if(nama!=""):
                        cetakBarcode(id1, nama, ws1)                           
                    else:
                        print("gagal buat stiker")
                else:
                    print("gagal cari nama")
            else:
                print("material sudah dicetak semua")
        except Exception as e:
            print(e)
            delta=2

        hitung00=hitung00+delta
        print("")
        sleep(3)
  sleep(1)
  print("akhir siklus")
    

if(chekKoneksi==1):
    connection.close()


print("selesai")
##
