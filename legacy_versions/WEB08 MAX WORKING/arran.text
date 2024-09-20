from flask import Flask, render_template, redirect, request
app = Flask(__name__)

import mysql.connector as proj
con = proj.connect(host = "localhost" ,user = "root", passwd= "8379", database = "timetable" )
cur = con.cursor() # cursor


@app.route('/')
def index():
    return render_template('Arrangement.html')

#_____________________________________________________________________________________
# ARRANGEMENT FXN
@app.route('/do_arrangement', methods=['GET', 'POST'])
def do_arrangement():
    if request.method == 'POST':
        day   = request.form['day'] 
        absent = request.form['absent_teacher']
         #+++++======START
        #free classes
        free_class = []
        s2= "select * from {} where class is not null and ename ='{}' ".format(day,absent)
        cur.execute(s2)
        recs = cur.fetchall()
        for rec in recs:
            free_class.append(rec[2])

        free_teacher =[]#free teacher classes
        for a in free_class :
            s3= "select * from "+day+" where class is null and period IN ("+str(a)+");"
            cur.execute(s3)
            recds = cur.fetchall()
            free_teacher.append(recds)

        absent_class = [] #absent class
        freeclass = tuple(free_class)
        sql1 = "select class,period from {} where ename ='{}' and period IN {}; ".format(day,absent,freeclass)
        cur.execute(sql1)
        cls = cur.fetchall()
        for n in cls:
            absent_class.append(n)

        #output creater
        otpt3=[]#output full list
        for m in absent_class:
            for k in free_teacher:
                for a in k:
                    if m[1]==a[2]:
                        outpt = [m[1],m[0],a[0],a[2]]
                        otpt3.append(outpt)
                        
        #output full list appended and ready [prd,sec,freeteach,free prd]
        return render_template('arr_output.html', output_list = otpt3)

    return render_template('Arrangement.html')

#____________________________________________________________________________________________________    
if __name__ == '__main__':
    import sys
    if sys.platform.startswith('win'):
        import os
        os.system("Set PYDEVD_DISABLE_FILE_VALIDATION=1")
    app.run(debug=True, port=5001, extra_files=None, use_reloader=False)
