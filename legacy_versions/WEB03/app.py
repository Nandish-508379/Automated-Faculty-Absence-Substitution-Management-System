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


@app.route('/run_arrangements', methods=['POST'])
def run_arrangements():
    import subprocess
        # Replace 'python_program.py' with the name of your Python program file
    subprocess.run(['python', 'arran.py'])
    print("ARRANGEMENTS DONE SUCCESSFULLY")






if __name__ == "__main__":
    app.run(debug=True)
