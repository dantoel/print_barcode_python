import pymysql
from datetime import date
from datetime import timedelta
import matPrint00
import spsPrint00
from time import sleep

connect = pymysql.connect(user='root', password='',
                              host='192.168.10.0',
                              database='reka')
cursor =connect.cursor()

angka=0
while (True):
    connect.commit()
    matPrint00.cetakBarcode(cursor, connect)
    spsPrint00.cetakBarcode(cursor, connect)

    angka=angka+1
    if(angka>99):
        angka=0
    print("-----",angka,"-----")
    sleep(1)

print("selesai")
