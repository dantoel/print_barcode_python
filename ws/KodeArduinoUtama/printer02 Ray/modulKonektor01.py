import mysql.connector
import pymysql

connect = mysql.connector.connect(user='ws', password='12345',
                              host='172.16.0.101',
                              database='rispros')
