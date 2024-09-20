from flask import Flask, render_template, request, redirect, session
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

cursor = db.cursor()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        users = cursor.fetchall()
        for rec in users:
            if rec[0] == username:
                if rec[2] == 'A':
                    return redirect('/dashboard_admin')
                elif rec[2] == 'U':
                    return redirect('/dashboard_user')
                else:
                    return "INVALID ROLE OF USER!"
    return render_template('login.html')

@app.route('/dashboard_admin')
def dashboard_admin():
    return render_template('dashboard_admin.html')
    
@app.route('/dashboard_user')
def dashboard_user():
    return render_template('dashboard_user.html')

if __name__ == "__main__":
    app.run(debug= True)