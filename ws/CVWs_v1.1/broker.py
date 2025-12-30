#jaringan safaluna
#broker_address ="192.168.100.82"
#jaringan Dago
#broker_address ="192.168.0.105"
#jaringan rispro
#broker_address = "192.168.1.100"

file = open(r"CONFIG.txt","r")
lines = file.readlines()

#masukin data dari CONFIG.txt ke variabel
broker_address = str(lines[8]).strip()