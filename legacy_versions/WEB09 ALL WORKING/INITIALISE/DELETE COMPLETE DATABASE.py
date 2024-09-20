# TO DELETE ALL DATA FROM SQL

import mysql.connector as proj
con = proj.connect(host = "localhost" ,user = "root", passwd= "8379", database = "mysql" )
cur = con.cursor()

sql9 = "drop database timetable;"
cur.execute(sql9)
con.commit()
con.close()
print("DATA SUCCESSFULLY REMOVED/DELETED FROM SQL")
