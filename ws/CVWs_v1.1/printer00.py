import datetime
import modulKonektor01
from time import sleep
import sys  
import string, datetime
from time import sleep
import os
from ctypes import *
import os.path

connect = modulKonektor01.connect
cursor = modulKonektor01.connect.cursor()

def tulis_lcd(msg):
    file = open("KodePC_lcd_msg.txt", 'w')
    file.write(msg)
    file.close()
 
def tulis_buzzer(msg):
    file = open("KodePC_buzzer_msg.txt", 'w')
    file.write(msg)
    file.close()

def cariNamaBerdasarId1(ws00, cur00):
    q00="SELECT Z0.id, Z0.namaMaterial from (SELECT A0.id, A0.purchaseID, "
    q00=q00+"A0.materialTypeCode, A2.nama, A3.proses, A4.nodalOutput, "
    q00=q00+"A5.nama namaNodal, A0.quantity, ifnull(A1.jumlah,0) AS terpakai, "
    q00=q00+"(A0.quantity-ifnull(A1.jumlah,0)) as sisa, case when A2.nama "
    q00=q00+"IS NOT NULL then A2.nama when A5.nama IS NOT NULL then A5.nama "
    q00=q00+"END AS namaMaterial, case 	when A2.nama IS NOT NULL then "
    q00=q00+"A0.materialTypeCode when A2.nama IS NULL then A4.nodalOutput "
    q00=q00+"END AS matCode, A6.workstationCode wsMaterial FROM "
    q00=q00+"mat_d_materialstock01 A0 LEFT JOIN (SELECT id_material, "
    q00=q00+"ifnull(SUM(jumlah),0) as jumlah FROM mat_d_inputoperasi GROUP BY "
    q00=q00+"id_material)A1 ON A0.id=A1.id_material LEFT JOIN "
    q00=q00+"mat_r_materialtype A2 ON A0.materialTypeCode=A2.code LEFT JOIN "
    q00=q00+"prd_d_operasi A3 ON A0.id=A3.output LEFT JOIN prd_r_proses A4 ON "
    q00=q00+"A3.proses=A4.id LEFT JOIN prd_r_strukturjnsprd A5 ON "
    q00=q00+"A4.nodalOutput=A5.idNodal LEFT JOIN mat_d_materialonws01 A6 ON "
    q00=q00+"A0.id=A6.materialStock WHERE A6.logout IS NULL)Z0 WHERE "
    q00=q00+"Z0.id=(SELECT id FROM mat_d_statusbarcode01 WHERE workstation='"
    q00=q00+ws00+"' AND STATUS IS NULL LIMIT 1)"
    cur00.execute(q00)
    tabel00=cur00.fetchone()
    id00=tabel00[0]
    nama00=tabel00[1]
    return id00, nama00

def cariNamaBerdasarId(ws00, con00, cur00):
    con00.commit()
    q00="SELECT Z0.id, Z0.matCode, Z0.namaMaterial, Z0.sisa, Z0.wsMaterial "
    q00=q00+"FROM (SELECT A.id, A.purchaseItem purchaseId, B.materialTypeCode, "
    q00=q00+"C.nama, D.proses, E.nodalOutput, F.nama namaNodal, A.quantity, "
    q00=q00+"ifnull(A1.jumlah,0) terpakai, (A.quantity-ifnull(A1.jumlah,0)) "
    q00=q00+"sisa, case when C.nama IS NOT NULL then C.nama when F.nama IS "
    q00=q00+"NOT NULL then F.nama END AS namaMaterial, case when C.nama  "
    q00=q00+"IS NOT NULL then B.materialTypeCode when C.nama IS NULL then "
    q00=q00+"E.nodalOutput END AS matCode, G.workstationCode wsMaterial "
    q00=q00+"FROM mat_d_materialstock A LEFT JOIN mat_d_purchaseitem B ON "
    q00=q00+"A.purchaseItem=B.id_item LEFT JOIN mat_r_materialtype C ON "
    q00=q00+"B.materialTypeCode=C.code LEFT JOIN prd_d_operasi D ON "
    q00=q00+"A.id=D.output LEFT JOIN prd_r_proses E ON D.proses=E.id LEFT "
    q00=q00+"JOIN prd_r_strukturjnsprd F ON E.nodalOutput=F.idNodal LEFT "
    q00=q00+"JOIN (SELECT id_material, ifnull(SUM(jumlah),0) as jumlah "
    q00=q00+"FROM mat_d_inputoperasi GROUP BY id_material)A1 ON "
    q00=q00+"A.id=A1.id_material LEFT JOIN mat_d_materialonws01 G ON "
    q00=q00+"A.id=G.materialStock WHERE G.logout IS NULL)Z0 WHERE "
    q00=q00+"Z0.id=(SELECT id FROM mat_d_statusbarcode WHERE workstation='"
    q00=q00+ws00+"' AND STATUS IS NULL LIMIT 1)"
    cur00.execute(q00)
    tabel00=cur00.fetchone()
    id00=tabel00[0]
    nama00=tabel00[2]
    return id00, nama00

def cetakBarcode(ws00, cur00, con00):
    con00.commit()
    q00="select count(*) from mat_d_statusbarcode where workstation='"+ws00
    q00=q00+"' and status is null"
    cur00.execute(q00)
    tabel00=cur00.fetchone()
    jml00=int(tabel00[0])
    if(jml00>0):
        hasil=cariNamaBerdasarId(ws00, con00, cur00)
        print(hasil[0])
        print(hasil[1])
        print(ws00)
        print('')

        cetakBarcode01(hasil[0],hasil[1],ws00)  
        
        q01="update mat_d_statusbarcode set status=current_timeStamp where "
        q01=q01+"id='"+hasil[0]+"' and workstation='"+ws00+"' and status is null"
        cur00.execute(q01)
        con00.commit()

def cetakBarcode01(id1, nama, ws):
    id1=id1.strip()
    balik=0
    global cetakGagal
    try:        
        barcode = id1
        name = nama
        ws1 = ws
        
        mydll = cdll.LoadLibrary("C:\\ws\\KodeArduinoUtama\\printer02\\Msprintsdk.dll")
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
        mydll.PrintChargeRow()
        mydll.SetSizetext(2,4)
        mydll.PrintString(b_string3,0)
        
        mydll.SetSizetext(2,2)
        mydll.PrintString(b_string2,0)
        
        
        print(mydll.Print1Dbar(2,50,1,2,4,b_string1))
        mydll.PrintChargeRow()
        mydll.PrintChargeRow()
        mydll.PrintChargeRow()
        mydll.PrintChargeRow()
        mydll.PrintCutpaper(1)
        mydll.SetClose()        
                
        global statusCetak
        sleep(10)
        print("Berhasil print")
        tulis_lcd("3")
        tulis_buzzer("1")
        
    except Exception as e:
        print(e)
        tulis_lcd("4")
        tulis_buzzer("2")
        print("gagal cetak barcode")
        sleep(5)    
    return balik

##program untuk ws
file = open(r"CONFIG.txt","r")
lines = file.readlines()
ws1 = str(lines[7])
ws1=ws1.strip()

hitung=0
while(True):
    if(hitung>9):
        hitung=0
    print("---",hitung, "---")
    cetakBarcode('WS07', cursor, connect)
    hitung=hitung+1
    sleep(1)
    


