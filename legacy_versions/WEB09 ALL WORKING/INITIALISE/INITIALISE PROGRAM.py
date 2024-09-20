#initialise 
import mysql.connector as proj
con = proj.connect(host = "localhost" ,user = "root", passwd= "8379", database = "mysql" )
cur = con.cursor()

sql9 = "create database timetable;"
sql10= "use timetable;"
sql1 = "create table monday(ename varchar(10), class varchar(5),period int);"
sql2 = "create table tuesday(ename varchar(10), class varchar(5),period int);"
sql3 = "create table wednesday(ename varchar(10), class varchar(5),period int);"
sql4 = "create table thursday(ename varchar(10), class varchar(5),period int);"
sql5 = "create table friday(ename varchar(10), class varchar(5),period int);"
sql6 = "create table saturday(ename varchar(10), class varchar(5),period int);"
sql7 = "create table users(username varchar(15), password varchar(10),role char(1));"
sql8 = "insert into users value('admin','1234','A')"
sql11 = "insert into users value('user','1234','U')"

cur.execute(sql9)
print("database created")
cur.execute(sql10)
print("database changed")
cur.execute(sql1)
print("table 1 is created")
cur.execute(sql2)
print("table 2 is created")
cur.execute(sql3)
print("table 3 is created")
cur.execute(sql4)
print("table 4 is created")
cur.execute(sql5)
print("table 5 is created")
cur.execute(sql6)
print("table 6 is created")
cur.execute(sql7)
print("table users is created")
cur.execute(sql8)
print("admin data added")
cur.execute(sql11)
print("users data added")
con.commit()
con.close()

print("tables created  !! good to go \n")
print('default ADMIN username= admin')
print('default password= 1234 \n')
print('default USER  username= user')
print('default password= 1234')