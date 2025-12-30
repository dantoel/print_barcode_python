#THIS CODE IS TO BE MERGED WITH MACHINE 1
#from signal import pause
#mosquitto -v

import datetime
import modulKonektor01
import paho.mqtt.client as mqtt
from time import sleep
import program04
import broker
#import keyboard

##connect = modulKonektor01.connect
##cursor = modulKonektor01.connect.cursor()

#ngambil data WS di CONFIG.txt
file = open(r"CONFIG.txt","r")
lines = file.readlines()
ws = str(lines[7]).strip()

#ws="ws03"
clientName00=ws+"00"
clientName01=ws+"01"
clientName02=ws+"02"
clientName03=ws+"03"

broker_address=broker.broker_address
connect = modulKonektor01.connect
cursor = modulKonektor01.connect.cursor()

tanda1=0
tanda2=0
data1=""
data2=""
angka=0
oprWs=0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    
def on_message(client, userdata, msg):
    global oprWs
    try:
        if (msg.topic == "oprWs"):
            oprWs=1
            data1=msg.payload.decode()
        if (msg.topic == "WS2"):
            tanda2=1
            data2=msg.payload.decode()
    except:
        print(msg.topic)
        print("masalah di penerimaan")
                         
client = mqtt.Client(clientName00)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, 1883)
client.subscribe("oprWs")
client.loop_start()

client1 = mqtt.Client(clientName01)
client1.on_connect = on_connect
client1.on_message = on_message
client1.connect(broker_address, 1883)
client1.subscribe("WS2")
client1.loop_start()

client3 = mqtt.Client(clientName03)
client3.on_connect = on_connect
client3.on_message = on_message
client3.connect(broker_address, 1883)
client3.subscribe("update")
client3.loop_start()
sleep(5)


def tampilkanData(con00, cur00):
    try:
        q00="select * from cpl_jadwal"
        con00.commit()
        cur00.execute(q00)
        tabel00=cur00.fetchall()
        for row00 in tabel00:
            print(row00)
    except:
         print("tidak berhasil tampilkan data")

def penawaranJadwal(cur00, con00):
    con00.commit()
    q00="select count(*) from cpl_jadwalproduk00 where stasiunKerja='"+ws+"'"
    cur00.execute(q00)
    tabel00=cur00.fetchone()
    jml00=int(tabel00[0])
    if(jml00>0):
        q01="select * from cpl_jadwalproduk00 where stasiunKerja='"+ws+"' order "
        q01=q01+"BY rencanaSelesai DESC, produk"
        cur00.execute(q01)
        tabel01=cur00.fetchone()
        produk01=tabel01[0]
        proses01=tabel01[1]
        start01=tabel01[2]
        finish01=tabel01[3]
        durasi01=tabel01[5]
        jdw=program04.periksaJadwalDiWs(ws, start01, finish01, durasi01, con00, cur00)
        q02="insert into cpl_jadwalws00(produk, proses, rencanaMulai, "
        q02=q02+"rencanaSelesai, stasiunKerja) values('"+produk01+"','"
        q02=q02+proses01+"','"+str(jdw[0])+"','"+str(jdw[1])+"','"+ws+"')"
        cur00.execute(q02)
        con00.commit()


angka=0
kriteria=1
while(kriteria):
    angka=angka+1
    if(angka>90):
        kriteria=0
    if(oprWs==1):
        oprWs=0
        penawaranJadwal(cursor, connect)
        print("pesan sudah dieksekusi")
        client.publish("laporWs",1)
        angka=0
    print(ws, "tunggu pesan (",angka,")" )
    sleep(1)
print("selesai")




