import time
import sqlite3

dbname = "test.db"



def createTable():
	conn = sqlite3.connect(dbname)
	cursor = conn.cursor()
	cursor.execute('drop table user')
	cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
	conn.commit()
	cursor.close()
	conn.close()

def longjob():
	time.sleep(15)
	conn = sqlite3.connect(dbname)
	cursor = conn.cursor()
	cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
	conn.commit()
	cursor.close()
	conn.close()
	print("done")