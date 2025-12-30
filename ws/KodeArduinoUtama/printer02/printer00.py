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
    file = open("C:\\ws\\KodeArduinoUtama\\lcd_msg.txt", 'w')
    file.write(msg)
    file.close()
 
def tulis_buzzer(msg):
    file = open("C:\\ws\\KodeArduinoUtama\\buzzer_msg.txt", 'w')
    file.write(msg)
    file.close()

def cariNamaBerdasarId(ws00, cur00):
    q00="SELECT X1.id, X0.namaMaterial, X1.workstation FROM "
    q00=q00+"mat_d_statusbarcode X1 LEFT JOIN (SELECT Y0.id, "
    q00=q00+"Y0.purchaseId, Y0.materialTypeCode, Y0.nama, Y0.proses, "
    q00=q00+"Y0.nodalOutput, Y0.mat2, Y0.namaNodal, Y0.quantity, Y0.terpakai, "
    q00=q00+"Y0.sisa, case when Y0.nama IS NOT NULL then Y0.nama when "
    q00=q00+"Y0.namaNodal IS NOT NULL then Y0.namaNodal END as namaMaterial, "
    q00=q00+"case when Y0.nama IS NOT NULL then Y0.materialTypeCode when "
    q00=q00+"Y0.nama IS NULL then Y0.mat2 end as matCode, Y0.wsMaterial FROM "
    q00=q00+"(SELECT A.id, A.purchaseItem purchaseId, B.materialTypeCode, "
    q00=q00+"C.nama, D.proses, E.nodalOutput, H.materialTypeCode mat2, "
    q00=q00+"F.nama namaNodal, A.quantity, ifnull(A1.jumlah,0) terpakai, "
    q00=q00+"(A.quantity-ifnull(A1.jumlah,0)) sisa, G.workstationCode "
    q00=q00+"wsMaterial FROM mat_d_materialstock A LEFT JOIN "
    q00=q00+"mat_d_purchaseitem B ON A.purchaseItem=B.id_item LEFT JOIN "
    q00=q00+"mat_r_materialtype C ON B.materialTypeCode=C.code LEFT JOIN "
    q00=q00+"prd_d_operasi D ON A.id=D.output LEFT JOIN prd_r_proses E ON "
    q00=q00+"D.proses=E.id LEFT JOIN prd_r_strukturjnsprd F ON "
    q00=q00+"E.nodalOutput=F.idNodal LEFT JOIN (SELECT id_material, "
    q00=q00+"ifnull(SUM(jumlah),0) as jumlah FROM mat_d_inputoperasi GROUP "
    q00=q00+"BY id_material)A1 ON A.id=A1.id_material LEFT JOIN "
    q00=q00+"mat_d_materialonws01 G ON A.id=G.materialStock LEFT JOIN "
    q00=q00+"prd_r_strukturjnsprd H ON E.nodalOutput=H.idNodal WHERE G.logout "
    q00=q00+"IS NULL AND (D.proses NOT IN (SELECT id FROM prd_r_proses WHERE "
    q00=q00+"id LIKE 'Z%' AND id LIKE '%A00%') OR D.proses IS NULL) UNION ALL "
    q00=q00+"SELECT Z0.id, Z0.purchaseId, Z0.materialTypeCode, Z0.nama, "
    q00=q00+"Z0.proses, Z0.nodalOutput, Z0.jnsProduk mat2, Z0.nama1 namaNodal, "
    q00=q00+"Z0.quantity, Z0.terpakai, Z0.sisa, Z0.wsMaterial  from "
    q00=q00+"(SELECT A.id, A.purchaseItem purchaseId, B.materialTypeCode, "
    q00=q00+"C.nama, D.proses, E.nodalOutput, H.materialTypeCode mat, "
    q00=q00+"F.nama namaNodal, A.quantity, ifnull(A1.jumlah,0) terpakai, "
    q00=q00+"(A.quantity-ifnull(A1.jumlah,0)) sisa, G.workstationCode "
    q00=q00+"wsMaterial, F.jnsProduk, I.nama nama1 FROM mat_d_materialstock "
    q00=q00+"A LEFT JOIN mat_d_purchaseitem B ON A.purchaseItem=B.id_item "
    q00=q00+"LEFT JOIN mat_r_materialtype C ON B.materialTypeCode=C.code "
    q00=q00+"LEFT JOIN prd_d_operasi D ON A.id=D.output LEFT JOIN "
    q00=q00+"prd_r_proses E ON D.proses=E.id LEFT JOIN prd_r_strukturjnsprd "
    q00=q00+"F ON E.nodalOutput=F.idNodal LEFT JOIN (SELECT id_material, "
    q00=q00+"ifnull(SUM(jumlah),0) as jumlah FROM mat_d_inputoperasi GROUP "
    q00=q00+"BY id_material)A1 ON A.id=A1.id_material LEFT JOIN "
    q00=q00+"mat_d_materialonws01 G ON A.id=G.materialStock LEFT JOIN "
    q00=q00+"prd_r_strukturjnsprd H ON E.nodalOutput=H.idNodal LEFT JOIN "
    q00=q00+"prd_r_jenisproduk I ON F.jnsproduk=I.id WHERE G.logout IS "
    q00=q00+"NULL AND D.proses LIKE 'Z%' AND D.proses LIKE '%A00%')Z0)Y0)X0 "
    q00=q00+"ON X1.id=X0.id WHERE X1.`status` IS NULL AND X1.workstation='"
    q00=q00+ws00+"' ORDER BY X1.id LIMIT 1"
    cur00.execute(q00)
    tabel00=cur00.fetchone()
    print(tabel00)
    id00=tabel00[0]
    nama00=tabel00[1]
    return id00, nama00

def cetakBarcode(ws00, cur00, con00):
    con00.commit()
    q00="select count(*) from mat_d_statusbarcode where workstation='"+ws00
    q00=q00+"' and status is null"
    cur00.execute(q00)
    tabel00=cur00.fetchone()
    jml00=int(tabel00[0])
    if(jml00>0):
        hasil=cariNamaBerdasarId(ws00, cur00)
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
        mydll.SetSizetext(2,3)
        mydll.PrintString(b_string3,0)
        mydll.PrintChargeRow()
        
        mydll.SetSizetext(1,1)
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
file = open(r"C:\ws\KodeArduinoUtama\data_ws.txt","r")
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



