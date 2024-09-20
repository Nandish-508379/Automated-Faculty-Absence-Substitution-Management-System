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


#__________________LOGIN_AND_HOMEPAGE_CODE___________________________________________________________
@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
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
        user = cursor.fetchone()
        return render_template('dashboard_admin.html', user=user)
    else:
        return redirect('/login')
    
@app.route('/dashboard_user')
def dashboard_user():
    if 'username' in session:
        username = session['username']
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        return render_template('dashboard_user.html', user=user)
    else:
        return redirect('/login')
    
@app.route('/Logout')
def Logout():
    session.clear()#clear cookies
    return index()

#______________________________________________________MAIN_PROGRAM_OVER____________________________



#______________________________________________________ARRANGEMENT_FXN______________________________
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
#---------------------------------------------------------------------------------------------------------
@app.route('/diffrent_teacher')
def diffrent_teacher():
    return render_template('/Arrangement.html')

@app.route('/back_to_home_page')
def back_to_home_page():
    return dashboard_admin()
#___________________________ARRANGEMENTS_OVER____________________________



#__________________________VIEW_TIMETABLE________________________________




#________________________VIEW_TIMETABLE_OVER_____________________________




#+________________________________________________________________________________
if __name__ == "__main__":
    app.run(debug=True)
