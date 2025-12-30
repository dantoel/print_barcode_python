import mysql.connector
import pymysql


file = open(r"CONFIG.txt","r")
lines = file.readlines()

#masukin data dari CONFIG.txt ke variabel
ipserver = str(lines[8]).strip() #.strip() untuk buang "enter" di string
namadatabase = str(lines[9]).strip()
namauser = str(lines[10]).strip()
katasandi = str(lines[11]).strip()

#connect = pymysql.connect(user='ws', password='12345',
#                              host='192.168.1.100',
#                              database='risproskosong')

connect = pymysql.connect(user=namauser, password=katasandi,
                              host=ipserver,
                              database=namadatabase)
