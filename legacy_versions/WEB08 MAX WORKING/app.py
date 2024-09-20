from flask import Flask, render_template, request, redirect, session
#SESSION=COOKIES
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to your own secret key

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Change to your MySQL username
    password="8379",  # Change to your MySQL password
    database="timetable"  # Change to your MySQL database name
)

cursor = db.cursor() #for login only!!!
cur = db.cursor() #for py main code


#__________________LOGIN_AND_LOG_OUT_CODE___________________________________________________________
@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        day = request.form['day']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            session['day'] = day
            if user[2] == 'A':
                return redirect('/dashboard_admin')
            elif user[2] == 'U':
                return redirect('/dashboard_user')
            else:
                return "INVALID ROLE OF USER!"
        else:
            return "Invalid username or password"
    return render_template('login.html')

#------------------------------------------------------------------------------------------------------
@app.route('/dashboard_admin')
def dashboard_admin():
    if 'username' in session:
        username = session['username']
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        rawdata = cursor.fetchone()
        dayy = session['day']
        user= list(rawdata) + [dayy]
        return render_template('dashboard_admin.html', user=user)
    else:
        return redirect('/login')
    
@app.route('/dashboard_user') #to be developed
def dashboard_user():
    if 'username' in session:
        username = session['username']
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        return render_template('dashboard_user.html',user=user)
    else:
        return redirect('/login')
    
@app.route('/Logout')
def Logout():
    session.clear()#clear cookies
    return index()

#______________________________________________________LOGIN_AND_LOGOUT_CODE_OVER____________________________



#______________________________________________________ARRANGEMENT_FXN______________________________
@app.route('/DO_ARRANGEMENT', methods=['GET', 'POST'])
def DO_ARRANGEMENT():
    if request.method == 'POST':
        arr_day   = request.form['arr_day'] 
        absent = request.form['absent_teacher']
         #+++++======START
        #free classes
        free_class = []
        s2= "select * from {} where class is not null and ename ='{}' ".format(arr_day,absent)
        cur.execute(s2)
        recs = cur.fetchall()
        for rec in recs:
            free_class.append(rec[2])

        free_teacher =[]#free teacher classes
        for a in free_class :
            s3= "select * from "+arr_day+" where class is null and period IN ("+str(a)+");"
            cur.execute(s3)
            recds = cur.fetchall()
            free_teacher.append(recds)

        absent_class = [] #absent class
        freeclass = tuple(free_class)
        sql1 = "select class,period from {} where ename ='{}' and period IN {}; ".format(arr_day,absent,freeclass)
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
    else:
        return render_template('Arrangement.html')
#---------------------------------------------------------------------------------------------------------
@app.route('/diffrent_teacher')
def diffrent_teacher():
    return render_template('/Arrangement.html')

@app.route('/back_to_home_page')
def back_to_home_page():
    return dashboard_admin()
#___________________________ARRANGEMENTS_OVER____________________________



#__________________________VIEW_TODAY_TIMETABLE________________________________
@app.route('/VIEW_TIMETABLE', methods=['GET'])
def VIEW_TIMETABLE():
    if 'username' in session:
        day = session['day']
        sql5 = "select * from {}".format(day)
        cur.execute(sql5)
        alldat = cur.fetchall()
        return render_template('View_Day_timetable.html', output_list = alldat)
    else:
        return dashboard_admin()

@app.route('/Download_File', methods=['GET'])
def Download_File():
    day = session['day']
    sql5 = "select * from {}".format(day)
    cur.execute(sql5)
    output_list = cur.fetchall()

    from datetime import date
    filename= str(date.today())

    import csv
    lst2=[]
    for n in output_list:
        templst2=[]
        for k in list(n):
            if k is None :
                tempvare = "null "
                templst2.append(tempvare)
            else:
                templst2.append(k)
        lst2.append(templst2)
            
    with open("Download_files/"+filename+".csv","w",newline="")as file1:
        csvwriter= csv.writer(file1)
        
        csvwriter.writerows(lst2)
    print("exel saved in the file whare this ropgram is stored named as "+filename+".csv")
    from flask import send_file
    path = "Download_files/"+filename+".csv"
    return send_file(path,as_attachment=True)

#___________________________VIEW_TODAY_TIMETABLE_OVER___________________________



#________________________ADD_AND_REMOVE_USER_____________________________
@app.route('/ADD_USER', methods=['GET','POST'])
def ADD_USER():
    if request.method == 'POST':
        username_nusers = request.form['Newusername'] 
        password_nusers = request.form['password'] 
        mode_nusers = request.form['role'] 
        sql27 = "insert into users value('{}','{}','{}');".format(username_nusers,password_nusers,mode_nusers)
        cur.execute(sql27)
        db.commit()
        return Logout()
    else:
        return render_template('Add_User.html')
#------------------------------------------------------------------------    
@app.route('/REMOVE_USER', methods=['GET','POST'])
def REMOVE_USER():
    cursor.execute("SELECT username FROM users")
    userdetails = cursor.fetchall()
    return render_template('Remove_User.html', output_list1 = userdetails)

    #______--------

@app.route('/Delete_User', methods=['GET','POST'])
def Delete_User():
    if request.method == 'POST':
        arr_day   = request.form['userToRemove']
        print(arr_day)
        if arr_day == "DEFAULT":
            return back_to_home_page()
        else:
            sql14 = "delete from users where username = '{}';".format(arr_day)
            cur.execute(sql14)
            db.commit()
            return Logout()
    else:
        return render_template('Remove_User.html')
#___________________ADD_AND_REMOVE_USER_OVER_____________________________      
        
        

#__________________INSERT_DATA___________________________________________
@app.route('/INSERT_DATA', methods=['GET','POST'])
def INSERT_DATA():
    if request.method == 'POST':
        day = request.form['insert_day']
        print(day)
        locat = request.form['locatio']
        print(locat)
        import csv 
        with open(locat,"r",newline="")as file1:
            flrdr = csv.reader(file1)
            for n in flrdr:
                if n[1]== "null":
                    s3= "insert into {} values('{}',{},{});".format(day,n[0],n[1],str(n[2]) )
                    cur.execute(s3)
                    db.commit()
                    print("null record added successfully")
                else:
                    s3= "insert into {} values('{}','{}',{});".format(day,n[0],n[1],str(n[2]) )
                    cur.execute(s3)
                    db.commit()
                    print("work record added successfully")
            sql22 = "select * from {}".format(day)
            cur.execute(sql22)
            alldat = cur.fetchall()
            return render_template('View_Day_timetable.html', output_list = alldat)
    else:
        return render_template("Insert_Data.html")
#__________________INSERT_DATA_OVER_____________________________________



#+________________________________________________________________________________
if __name__ == "__main__":
    app.run(debug=True)