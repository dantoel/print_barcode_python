import datetime
##import modulKonektor01
from time import sleep
import sys              #sistem
import string, datetime
from time import sleep
import os
from ctypes import *
import os.path

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
        mydll.SetSizetext(0,3)
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

cetakBarcode01('P25000K100001', 'nama', 'ws')

