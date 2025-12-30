import datetime
import modulKonektor01


#fungsi ini adalah fungsi untuk mencari jadwal relatif terhadap jadwal yang telah ada,
#jadwal juga dikaitkan dengan hari libur, sabtu & minggu, serta jam istirahat. fungsi
#ini adalah contoh.

def periksaJadwalThdJadwalYgAda(ws00, start00, finish00, durasi):
  q00="select * from prd_d_operation where scheduledStartOperation is not null and "
  q00=q00+"finishOperation is null"
  q00=q00+" and workstation='"+ws00+"' order by scheduledStartOperation desc"
  connect = modulKonektor01.connect
  connect.reconnect() 
  cursor = modulKonektor01.connect.cursor()
  cursor.execute(q00)
  tabel00=cursor.fetchall()
  print("---nilai awal---")
  print(start00, finish00, durasi)
  cursor.close()
  connect.close()
  jdw=periksaJadwalThdIstirahat(start00, finish00, durasi)
  start00=jdw[0]  
  finish00=jdw[1]
  print("istirahat awal")
  print(start00, finish00, durasi)
  
  #jdw=periksaWeekEnd(start00, finish00, durasi)
  jdw=periksaTabelHoliday(start00, finish00, durasi, con00, cur00)
  start00=jdw[0]  
  finish00=jdw[1]
  print("libur awal")
  print(start00, finish00, durasi)
  angka=0
  for row00 in tabel00:
    #indeks S menyatakan jadwal yang sudah ada
    startS=row00[8]    
    finishS=row00[9]
    print(startS, finishS, durasi,'pembanding')
    jdw=datetime05.periksaKesamaanJadwal(startS, finishS, start00, finish00, durasi)    
    start00=jdw[0]  
    finish00=jdw[1]
    print(start00, finish00, durasi)
    jdw=periksaJadwalThdIstirahat(start00, finish00, durasi)
    start00=jdw[0]  
    finish00=jdw[1]
    print("istirahat")
    print(start00, finish00, durasi)
    #jdw=periksaWeekEnd(start00, finish00, durasi)
    jdw=periksaTabelHoliday(start00, finish00, durasi, con00, cur00)
    start00=jdw[0]  
    finish00=jdw[1]
    print("libur")
    print(start00, finish00, durasi)
  print("---selesai---")
    
  return start00, finish00, durasi

#fungsi ini menggeser jadwal agar jadwal yang baru tidak berpotongan dengan jadwal
#yang lama. akhiran S menunjukkan jadwal baru, akhiran Is menunjukkan jadwal lama
def geserJadwal01(awalIs, akhirIs, awalS, akhirS, durasi):
  durasi=int(durasi)
  akhirS=awalIs
  dt=datetime.timedelta(minutes=durasi)
  awalS=akhirS-dt
  return awalS, akhirS, durasi

#fungsi ini memeriksa apakah dua buah jadwal saling berpotongan. fungsi ini
#mengembalikan jadwal baru yang sudah tidak berpotongan dengan jadwal manapun
def periksaKesamaanJadwal(awalS, akhirS, awalB, akhirB, durasi):
  #awalS=datetime.datetime.strptime(awalS, '%Y-%m-%d %H:%M:%S')
  #indeks S menunjukkan jadwal yang sudah ada
  #indeks B menunjukkan jadwal baru
  ct00='00'
  if((awalS==awalB) and (akhirS==akhirB)):
    ct00='01'
    
  if((awalS==awalB) and (akhirS>akhirB)):
    ct00='01'
    
        
  if((awalS<awalB) and (akhirS==akhirB)):
    ct00='01'
    

  if((awalS<awalB) and (akhirS>akhirB)):
    ct00='01'
    

  if((awalS==awalB) and (akhirS<akhirB)):
    ct00='01'
    print("5")

  if((awalS>awalB) and (akhirS==akhirB)):
    ct00='01'
    print("6")

  if((awalS>awalB) and (akhirS<akhirB)):
    ct00='01'
    

  if((awalS<awalB) and (akhirS<akhirB) and (akhirS>awalB)):
    ct00='01'
    

  if((awalS>awalB) and (akhirS>akhirB) and (awalS<akhirB)):
    ct00='01'
    
 
  if(ct00=='01'):
    jadwal=geserJadwal01(awalS, akhirS, awalB, akhirB, durasi)
    awalB=jadwal[0]
    akhirB=jadwal[1]

  return awalB, akhirB, durasi

#fungsi ini memeriksa jadwal baru apakah beririsan dengan jadwal yang sudah ada di ws
#fungsi ini belum melibatkan pemeriksaan waktu istirahat
def periksaJadwalDiWs(ws00, start00, finish00, durasi, con00, cur00):
  con00.commit()
  q00="select * from prd_d_operasi where rencanaMulai is not null and "
  q00=q00+"selesai is null and stasiunKerja='"+ws00+"' and rencanaMulai <= '"
  q00=q00+str(finish00)+"' order by rencanaMulai desc"
  cur00.execute(q00)
  tabel00=cur00.fetchall()
  for row00 in tabel00:
    startS=row00[1]    
    finishS=row00[2]
    jdw=periksaJadwalThdIstirahat(start00, finish00, durasi, con00, cur00)
    start00=jdw[0]    
    finish00=jdw[1]
    jdw=periksaTabelHoliday(start00, finish00, durasi, con00, cur00)
    start00=jdw[0]    
    finish00=jdw[1]
    jdw=periksaKesamaanJadwal(startS, finishS, start00, finish00, durasi)
    start00=jdw[0]    
    finish00=jdw[1]
  jdw=periksaJadwalThdIstirahat(start00, finish00, durasi, con00, cur00)
  start00=jdw[0]    
  finish00=jdw[1]
  jdw=periksaTabelHoliday(start00, finish00, durasi, con00, cur00)
  start00=jdw[0]    
  finish00=jdw[1]
  return start00, finish00, durasi

def periksaJadwalThdIstirahat(start, finish, durasi, con00, cur00):
  con00.commit()
  q01="select * from gen_r_waktuIstirahat where berlaku is null order by mulai desc"
  cur00.execute(q01)
  tabel02=cur00.fetchall()
  for row02 in tabel02:
    awalIs=row02[0]
    akhirIs=row02[1]
    jdw01=periksaJamIstirahat(awalIs, akhirIs, start, finish, durasi, con00, cur00)
    start=jdw01[0]
    finish=jdw01[1]
  return start, finish, durasi

def periksaJamIstirahat(awalIs, akhirIs, awalS, akhirS, durasi, con00, cur00):
  #memeriksa apakah suatu jadwal operasi beririsan dengan waktu istirahat
  #indeks Is menyatakan waktu istirahat
  #indeks S menyataan waktu jadwal operasi
  
  awal00=awalIs
  akhir00=akhirIs
  #awal00 dan akhir00 adalah waktu jam istirahat setelah dimodifikasi

  awal01=awalS
  akhir01=akhirS
  #selang waktu yang akan dikembalikan oleh fungsi

  dateS=akhirS.date()
  dateIs=akhirIs.date()
  delta=dateS-dateIs
  angka=int(delta.days)
  dd=datetime.timedelta(days=angka)
  akhir00=akhirIs+dd
  awal00=awalIs+dd
  #indeks nol menyatakan waktu istirahat

  ct00='00'

  #jadwal berimpit dengan waktu istirahat, geser jadwal
  if((awalS==awal00) and (akhirS==akhir00)):
    ct00='01'

  #awal istirahat=awal jadwal, akhir istirahat lebih dari akhir jadwal
  #geser jadwal
  if((akhirS<akhir00) and (awalS==awal00)):
    ct00='02'

  #akhir istirahat=akhir istirahat, awal istirahat kurang dari awal jadwal
  #geser jadwal
  if((akhirS==akhir00) and (awal00<awalS)):
    ct00='03'

  #jadwal berada di dalam waktu istirahat
  #geser jadwal
  if((akhir00>akhirS) and (awal00<awalS)):
    ct00='04'

  #jadwal lebih lama dari waktu istirahat, awal istirahat=awal jadwal
  #awal jadwal dimundurkan
  if((awal00==awalS) and (akhir00<akhirS)):
    ct00='05'

  #jadwal lebih lama dari waktu istirahat, akhir istirahat=akhir jadwal
  #geser jadwal
  if((awalS<awal00) and (akhirS==akhir00)):
    ct00='06'

  #waktu istirahat di dalam jadwal
  #awal jadwal dimundurkan
  if((akhirS>akhir00) and (awalS<awal00)):#slide 9
    ct00='07'

  #waktu istirahat bersilangan dengan jadwal, jadwal berada lebih ke kanan
  #awal jadwal dimundurkan versi 01
  if((akhirS>akhir00) and (awalS>awal00) and (awalS<akhir00)):
    ct00='08'

  #waktu istirahat bersilangan dengan jadwal, jadwal berada lebih ke kiri
  #geser jadwal
  if((akhirS<akhir00) and (awalS<awal00) and (awal00<akhirS)):
    ct00='09'
  
  if((ct00=='01') or (ct00=='02') or (ct00=='03') or (ct00=='04')
     or (ct00=='06') or (ct00=='09')):
     jadwal=geserJadwal01(awal00, akhir00, awal01, akhir01,durasi)
     awal01=jadwal[0]
     akhir01=jadwal[1]
     durasi=jadwal[2]
  if((ct00=='05') or (ct00=='07')):
    jadwal=ekstenStart00(awal00, akhir00, awal01, akhir01,durasi)
    awal01=jadwal[0]
    akhir01=jadwal[1]
    durasi=jadwal[2]
  if(ct00=='08'):
    jadwal=ekstenStart01(awal00, akhir00, awal01, akhir01,durasi)
    awal01=jadwal[0]
    akhir01=jadwal[1]
    durasi=jadwal[2]


  #pemeriksaan bila waktu istirahat diajukan sehari
  dd=datetime.timedelta(days=1)
  akhir00=akhir00+dd
  awal00=awal00+dd
  ct00='00'  

  if((awalS==awal00) and (akhirS==akhir00)):
    ct00='01'
    

  if((akhirS<akhir00) and (awalS==awal00)):
    ct00='02'
    

  if((akhirS==akhir00) and (awal00<awalS)):
    ct00='03'

  if((akhir00>akhirS) and (awal00<awalS)):
    ct00='04'

  if((awal00==awalS) and (akhir00<akhirS)):
    ct00='05'

  if((awalS<awal00) and (akhirS==akhir00)):
    ct00='06'

  if((akhirS>akhir00) and (awalS<awal00)):
    ct00='07'

  if((akhirS>akhir00) and (awalS>awal00)and (awalS<akhir00)):
    ct00='08'

  if((akhirS<akhir00) and (awalS<awal00) and (awal00<akhirS)):
    ct00='09'

  if((ct00=='01') or (ct00=='02') or (ct00=='03') or (ct00=='04')
     or (ct00=='06') or (ct00=='09')):
     jadwal=geserJadwal01(awal00, akhir00, awal01, akhir01,durasi)
     awal01=jadwal[0]
     akhir01=jadwal[1]
     durasi=jadwal[2]
  if((ct00=='05') or (ct00=='07')):
    jadwal=ekstenStart00(awal00, akhir00, awal01, akhir01,durasi)
    awal01=jadwal[0]
    akhir01=jadwal[1]
    durasi=jadwal[2]
  if(ct00=='08'):
    jadwal=ekstenStart01(awal00, akhir00, awal01, akhir01,durasi)
    awal01=jadwal[0]
    akhir01=jadwal[1]
    durasi=jadwal[2]    
                          
  return awal01, akhir01, durasi

def ekstenStart01(awalIs, akhirIs, awalS, akhirS, durasi):
  dJadwal=selisihWaktuDlmMnt(awalS, akhirS)
  if(int(dJadwal)==int(durasi)):
    dWaktu=selisihWaktuDlmMnt(awalS, akhirIs)
    dt=datetime.timedelta(minutes=dWaktu)
    awalS=awalIs-dt
  return awalS, akhirS, durasi

def ekstenStart00(awalIs, akhirIs, awalS, akhirS, durasi):
  #bila belum pernah dieksten maka akan dieksten
  #bila pernah dieksten maka akan digeser
  #dilakukan bila waktu istirahat lebih pendek dari jadwal
  dJadwal=selisihWaktuDlmMnt(awalS, akhirS)
  if(int(dJadwal)==int(durasi)):
    dIstirahat=selisihWaktuDlmMnt(awalIs, akhirIs)
    dt=datetime.timedelta(minutes=dIstirahat)
    awalS=awalS-dt
  return awalS, akhirS, durasi

def selisihWaktuDlmMnt(awal, akhir):
  #menghitung selisih waktu dalam menit, mengembalikan nilai integer
  dTime=akhir-awal
  detik=dTime.total_seconds()
  kembali=int(detik/60)
  return kembali

def periksaWeekEnd(start00, finish00, durasi, con00, cur00):
  start=start00.weekday()
  finish=finish00.weekday()
  kriteria=0
  if(finish>4):
    jdw=geserWeekEnd(start00, finish00, durasi, con00, cur00)
    kriteria=1
  if((start>4) and (finish<=4)):
    jdw=ekstenWeekEnd(start00, finish00, durasi)
    kriteria=1
  if(kriteria==1):
    start00=jdw[0]
    finish00=jdw[1]
  return start00, finish00, durasi

def ekstenWeekEnd(start00, finish00, durasi):
  hari=start00.weekday()
  dd=datetime.timedelta(days=0)
  if(hari==6):
    dd=datetime.timedelta(days=2)
  if(hari==5):
    dd=datetime.timedelta(days=2)
  start00=start00-dd
  return start00, finish00, durasi

def geserWeekEnd(start00, finish00, durasi, con00, cur00):
  con00.commit()
  q00="select * from gen_r_waktuIstirahat where berlaku is null order by mulai desc"
  cur00.execute(q00)
  tabel00=cur00.fetchone()
  tgl00=tabel00[0]
  waktu=str(tgl00.time())
  hari=finish00.weekday()
  dd=datetime.timedelta(days=0)
  dd=datetime.timedelta(days=0)
  if(hari==6):
    dd=datetime.timedelta(days=2)
  if(hari==5):
    dd=datetime.timedelta(days=2)
  finish00=finish00-dd
  tgl01=str(finish00.date())
  tgl02=tgl01+" "+waktu
  finish00=datetime.datetime.strptime(tgl02, '%Y-%m-%d %H:%M:%S')
  dds=datetime.timedelta(minutes=int(durasi))
  start00=finish00-dds
  print("geser weekEnd sampai sini")
  return start00, finish00,durasi

#-----mulai fungsi periksa hari libur-----
def periksaTabelHoliday(start00, finish00, durasi, con00, cur00):
  con00.commit()
  jdw=periksaWeekEnd(start00, finish00, durasi, con00, cur00)
  start00=jdw[0]
  finish00=jdw[1]
  q00="SELECT *, datediff(DATE(CURRENT_TIMESTAMP), DATE(hariLibur)) delta FROM "
  q00=q00+"gen_r_harilibur WHERE (datediff(DATE(CURRENT_TIMESTAMP), "
  q00=q00+"DATE(hariLibur)))<100 ORDER BY hariLibur DESC"
  cur00.execute(q00)
  tabel00=cur00.fetchall()
  for row00 in tabel00:
    date1=row00[0]
    jdw=periksaHoliday(date1, start00, finish00, durasi, con00, cur00)
    start00=jdw[0]
    finish00=jdw[1]
    jdw=periksaWeekEnd(start00, finish00, durasi, con00, cur00)
    start00=jdw[0]
    finish00=jdw[1]
  return start00, finish00, durasi

def periksaHoliday(date1, start00, finish00, durasi, con00, cur00):
  nilStart00=periksaKesamaanTanggal(date1, start00)
  nilFinish00=periksaKesamaanTanggal(date1, finish00)
  jdw=start00, finish00, durasi
  if(nilFinish00=='1'):
    jdw=geserHoliday(start00, finish00, durasi, con00, cur00)
  if((nilStart00=='1') and (nilFinish00!='1')):
    jdw=ekstenHoliday(start00, finish00, durasi)
  start00=jdw[0]
  finish00=jdw[1]
  return start00, finish00, durasi

def periksaKesamaanTanggal(date1, date2):
  #memeriksa apakah date1 dan date2 mempunyai tanggal yang sama
  #mengembalikan string 1 bila kedua hari sama
  y1=date1.year
  m1=date1.month
  d1=date1.day
  y2=date2.year
  m2=date2.month
  d2=date2.day
  kembali=0
  if((y1==y2) and (m1==m2) and (d1==d2)):
    kembali=1
  kembaliS=str(kembali)
  return kembaliS

def geserHoliday(start00, finish00, durasi, con00, cur00):
  con00.commit()
  q00="select * from gen_r_waktuIstirahat where berlaku is null order by mulai"
  q00=q00+" desc"
  cur00.execute(q00)
  tabel00=cur00.fetchone()
  tgl00=tabel00[0]
  waktu=str(tgl00.time())
  dd=datetime.timedelta(days=1)
  finish00=finish00-dd
  tgl01=str(finish00.date())
  tgl02=tgl01+" "+waktu
  finish00=datetime.datetime.strptime(tgl02, '%Y-%m-%d %H:%M:%S')
  dds=datetime.timedelta(minutes=int(durasi))
  start00=finish00-dds
  return start00, finish00,durasi

def ekstenHoliday(start00, finish00, durasi):
  dd=datetime.timedelta(days=1)
  start00=start00-dd
  return start00, finish00, durasi





##dateS="2022-06-17 00:00:00"
##awalIs="2022-06-19 16:15:00"
##akhirIs="2022-06-19 16:30:00"
##
###jadwal
##awalS="2022-06-20 07:30:00"
##akhirS="2022-06-20 06:00:00"
##delta=180
##
##dateSD=datetime.datetime.strptime(dateS, '%Y-%m-%d %H:%M:%S')
##awalIsD=datetime.datetime.strptime(awalIs, '%Y-%m-%d %H:%M:%S')
##akhirIsD=datetime.datetime.strptime(akhirIs, '%Y-%m-%d %H:%M:%S')
##
##awalSD=datetime.datetime.strptime(awalS, '%Y-%m-%d %H:%M:%S')
##akhirSD=datetime.datetime.strptime(akhirS, '%Y-%m-%d %H:%M:%S')
##
###jadwal=periksaKesamaanJadwal(awalSD, akhirSD, awalSD, akhirSD, delta)
##jadwal=periksaKesamaanJadwal(awalIsD, akhirIsD, awalSD, akhirSD, delta)
##print(jadwal[0])
##print(jadwal[1])
##print(jadwal[2])

##q00=periksaJadwalDiWs("ws4", awalIs, akhirIs, 180)
##cursor.execute(q00)
##tabel00=cursor.fetchall()
##for row00 in tabel00:
##  print(row00)

##jdw=periksaJadwalDiWs("ws4", awalSD, akhirSD, 15)
##print(jdw[0])
##print(jdw[1])

##jadwal=periksaJamIstirahat(awalIsD, akhirIsD, awalSD, akhirSD, 90)
##print(jadwal[0])
##print(jadwal[1])
##print(jadwal[2])

#hasil=periksaKesamaanTanggal(awalIsD, akhirIsD)
#print(hasil)

#jdw=periksaHoliday(dateSD,awalIsD, akhirIsD,15, connect, cursor)
##jdw=periksaTabelHoliday(awalIsD, akhirIsD,15, connect, cursor)
##print(jdw[0], jdw[1])
##

##jdw=periksaJadwalThdIstirahat(awalSD, akhirSD, 100, connect, cursor)
##jdw=periksaJadwalDiWs('ws02', awalSD, akhirSD, 90, connect, cursor)
##print(jdw[0])
##print(jdw[1])
##print("selesai")
