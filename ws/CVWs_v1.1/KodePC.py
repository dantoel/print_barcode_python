import serial                                       #Serial imported for Serial communication
import time                                         #Required to use delay functions   
from time import sleep
import socket   
from datetime import datetime
import os

def lcd_msg_0():
    file = open(r"KodePC_lcd_msg.txt","w")
    file.write("0")
    file.close()

def msg_0(): #Buzzer
    file = open(r"KodePC_buzzer_msg.txt", 'w')
    file.write("0")
    file.close()

def get_ws(): #LCD
    file = open(r"CONFIG.txt","r")
    lines = file.readlines()
    ws = str(lines[7]).strip() #strip untuk buang "enter" di string
    return ws

#Kode Mulai dari sini
file = open(r"CONFIG.txt","r")
lines = file.readlines()
COMusb = str(lines[14]).strip() 

ArduinoUnoSerial = serial.Serial(COMusb,9600)       #membuat koneksi serial ke port 5 dengan  nama ArduinoUnoSerialData                                                             #wait for 2 secounds for the communication to get established
print (ArduinoUnoSerial.readline())                 #membaca data serial daro port 5 dan print
print ("Koneksi Selesai")

#inisasi kondisi awal buzzer_msg
file = open(r"KodePC_buzzer_msg.txt", 'w')
file.write("0") #inisiasi buzzer awal (=0) bisa diganti untuk tes buzzer.
file.close()

#inisasi kondisi awal lcd_msg
file = open(r"KodePC_lcd_msg.txt","w")
file.write("0") #inisiasi buzzer awal (=0) bisa diganti untuk tes buzzer.
file.close()
	
while (1==1):
    #Menampilkan kodeWS, tanggal, dan IP Mini PC di LCD
    ArduinoUnoSerial.write(bytes("WS : " + get_ws(), 'utf-8'))
    time.sleep(0.1)	
    ArduinoUnoSerial.write(bytes(datetime.now().strftime('%b %d  %H:%M:%S'),'utf-8')) 
    time.sleep(0.1)	
    ArduinoUnoSerial.write(bytes("IP : " + socket.gethostbyname(socket.gethostname()), 'utf-8'))
    time.sleep(0.1)
	
    #Menghidupkan buzer sesuai kondisi buzzer/buzzer_msg
    fileBuzz = open(r"KodePC_buzzer_msg.txt","r")
    lines = fileBuzz.readlines()
    fileBuzz.close()
    msg = lines[0]
    if msg == "1":
        msg_0()
        ArduinoUnoSerial.write(bytes("B1", 'utf-8'))
        time.sleep(0.5)
    elif msg == "2":
        msg_0()
        ArduinoUnoSerial.write(bytes("B2", 'utf-8'))
        time.sleep(1.1)
    elif msg == "3":
        msg_0()
        ArduinoUnoSerial.write(bytes("B3", 'utf-8'))
        time.sleep(0.1)

    #Tampilan LCD kostumise
    fileLCD = open(r"KodePC_lcd_msg.txt","r")
    lines = fileLCD.readlines()
    msg = lines[0]
    fileLCD.close()
    if msg != "0":
        lcd_msg_0()
        if msg[0] == "X" : #mengirimkan kode dan variabel
            ArduinoUnoSerial.write(bytes(msg, 'utf-8'))
        else: #mengirim kode tanpa mengirim variable
            ArduinoUnoSerial.write(bytes("Z" + msg, 'utf-8'))
        time.sleep(2.1)
	
    while ArduinoUnoSerial.in_waiting:
        data = ArduinoUnoSerial.readline()
        if data == b'Tom2\r\n':
            os.system("shutdown /s /t 1") #shutdown
        if data == b'Tom3\r\n':
            os.system("shutdown /r") #restart
	
#	print(ArduinoUnoSerial.readline())	
#	if (ArduinoUnoSerial.readline()) == b'Tom1\r\n':
#		print ("Tombol 1 Ditekan\r\n")
#		ArduinoUnoSerial.write(b'Tom1')
#		time.sleep(1)
#		ArduinoUnoSerial.flushInput()
#	if (ArduinoUnoSerial.readline()) == b'Tom2\r\n':
#		print ("Tombol 2 Ditekan\r\n")
#		ArduinoUnoSerial.write(b'Bol2')
#		time.sleep(1)
#		ArduinoUnoSerial.flushInput()
#    os.system("shutdown /s /t 1")

#os.system("shutdown /s") #shutdown
#os.system("shutdown /r") #restart
#os.system("shutdown /l") #logoff
#os.system("shutdown /h") #hibernate
	
