from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to your own secret key

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Change to your MySQL username
    password="8379",  # Change to your MySQL password
    database="your_database"  # Change to your MySQL database name
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
            return redirect('/dashboard')
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Welcome {session['username']}! This is the dashboard."
    else:
        return redirect('/login')

if __name__ == "__main__":
    app.run(debug= True)