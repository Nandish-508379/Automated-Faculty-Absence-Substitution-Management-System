"""
=============================================================================
AUTOMATED FACULTY ABSENCE & SUBSTITUTION MANAGEMENT SYSTEM
Project ID: 006/2024 | Year: 2024
Author & Rights Holder: M Nandish
Enterprise Production Edition

PROPRIETARY & NON-COMMERCIAL NOTICE:
Copyright (c) 2024 M Nandish. All Rights Reserved.
Any copying, reproduction, editing, modification, updating, redistribution,
or use of this software, in whole or in part, requires the prior express
written and exclusive permission of the author.
Strictly prohibited for commercial use.
=============================================================================
"""

import os
import io
import csv
import sqlite3
from datetime import date
from flask import Flask, render_template, request, redirect, session, send_file, flash

app = Flask(__name__)
# Secret key from environment or secure 2024 fallback
app.secret_key = os.environ.get('SECRET_KEY', 'timetable_management_system_2024_006_sec_key')

# ---------------------------------------------------------------------------
# Database Configuration & Dual-Engine Manager (MySQL + Standalone Fallback)
# ---------------------------------------------------------------------------
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '8379')
DB_NAME = os.environ.get('DB_NAME', 'timetable')

VALID_DAYS = {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB_PATH = os.path.join(BASE_DIR, 'timetable.db')
SAMPLE_CSV_PATH = os.path.join(BASE_DIR, 'INITIALISE', 'newrecc.csv')

class DatabaseManager:
    """
    Manages connection to MySQL database with automatic, transparent fallback
    to SQLite when MySQL service is offline or not installed.
    """
    def __init__(self):
        self.engine = 'mysql'
        self.mysql_conn = None
        self._init_connection()

    def _init_connection(self):
        try:
            import mysql.connector
            self.mysql_conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                connect_timeout=2
            )
            self.engine = 'mysql'
            print("[INFO] Successfully connected to MySQL database: 'timetable'")
        except Exception as e:
            print(f"[NOTICE] MySQL unavailable ({e}). Running seamlessly with local SQLite database.")
            self.engine = 'sqlite'
            self._init_sqlite_db()

    def _init_sqlite_db(self):
        """Initializes SQLite schema and default seed data if database is fresh."""
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cur = conn.cursor()
        for day in VALID_DAYS:
            cur.execute(f"CREATE TABLE IF NOT EXISTS {day} (ename TEXT, class TEXT, period INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, role TEXT)")
        
        # Seed default users
        cur.execute("INSERT OR IGNORE INTO users VALUES ('admin', '1234', 'A')")
        cur.execute("INSERT OR IGNORE INTO users VALUES ('user', '1234', 'U')")
        
        # Check if monday table has data; if empty, load from newrecc.csv
        cur.execute("SELECT COUNT(*) FROM monday")
        count = cur.fetchone()[0]
        if count == 0 and os.path.exists(SAMPLE_CSV_PATH):
            with open(SAMPLE_CSV_PATH, 'r', newline='', encoding='utf-8-sig', errors='ignore') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3:
                        ename = row[0].strip()
                        cls = row[1].strip()
                        try:
                            period = int(row[2].strip())
                        except (ValueError, TypeError):
                            continue
                        # Populate all days with initial schedule for instant testing
                        for day in VALID_DAYS:
                            cur.execute(f"INSERT INTO {day} VALUES (?, ?, ?)", (ename, cls, period))
            print(f"[INFO] Populated initial timetable records from '{SAMPLE_CSV_PATH}' into SQLite.")
        conn.commit()
        conn.close()

    def get_cursor(self):
        """Returns a cursor and active connection."""
        if self.engine == 'mysql':
            try:
                if not self.mysql_conn.is_connected():
                    self.mysql_conn.reconnect(attempts=2, delay=1)
                return self.mysql_conn.cursor(), self.mysql_conn
            except Exception:
                # If MySQL dropped, fallback to SQLite
                self.engine = 'sqlite'
                self._init_sqlite_db()

        conn = sqlite3.connect(SQLITE_DB_PATH)
        return conn.cursor(), conn

    def query(self, sql, params=None, fetch='all', commit=False):
        """Unified query execution supporting both MySQL (%s) and SQLite (?) syntax."""
        cursor, conn = self.get_cursor()
        try:
            if self.engine == 'sqlite':
                # Convert %s placeholders to ? for sqlite
                sql = sql.replace('%s', '?')
            
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            if commit:
                conn.commit()

            result = None
            if fetch == 'one':
                result = cursor.fetchone()
            elif fetch == 'all':
                result = cursor.fetchall()

            if self.engine == 'sqlite' and not commit:
                conn.close()
            return result
        except Exception as e:
            print(f"[DB ERROR] Query failed: {sql} | Error: {e}")
            if self.engine == 'sqlite':
                conn.close()
            raise e

db = DatabaseManager()

# ---------------------------------------------------------------------------
# Authentication & Session Management
# ---------------------------------------------------------------------------
@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        day = request.form.get('day', 'monday').lower().strip()

        if day not in VALID_DAYS:
            day = 'monday'

        try:
            user = db.query(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password),
                fetch='one'
            )
            if user:
                session['username'] = username
                session['day'] = day
                session['role'] = user[2]
                if user[2] == 'A':
                    return redirect('/dashboard_admin')
                elif user[2] == 'U':
                    return redirect('/dashboard_user')
                else:
                    return render_template('login.html', error="Invalid user role configuration.")
            else:
                return render_template('login.html', error="Invalid username or password.")
        except Exception as e:
            return render_template('login.html', error=f"Database error: {e}")

    return render_template('login.html')

@app.route('/Change_Password', methods=['GET', 'POST'])
@app.route('/change_password', methods=['GET', 'POST'])
@app.route('/CHANGE_PWD', methods=['GET', 'POST'])
@app.route('/change_pwd', methods=['GET', 'POST'])
def Change_Password():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        new_password = request.form.get('New_PWD_1', '').strip()
        username = session['username']
        if new_password:
            db.query(
                "UPDATE users SET password=%s WHERE username=%s",
                (new_password, username),
                commit=True
            )
        return Logout()
    return render_template('Change_PWD.html')

@app.route('/dashboard_admin')
def dashboard_admin():
    if 'username' in session and session.get('role') == 'A':
        username = session['username']
        rawdata = db.query("SELECT * FROM users WHERE username=%s", (username,), fetch='one')
        if not rawdata:
            return redirect('/login')
        dayy = session.get('day', 'monday')
        user = list(rawdata) + [dayy]
        return render_template('dashboard_admin.html', user=user)
    return redirect('/login')

@app.route('/dashboard_user')
def dashboard_user():
    if 'username' in session:
        username = session['username']
        rawdata = db.query("SELECT * FROM users WHERE username=%s", (username,), fetch='one')
        if not rawdata:
            return redirect('/login')
        dayy = session.get('day', 'monday')
        user = list(rawdata) + [dayy]
        return render_template('dashboard_user.html', user=user)
    return redirect('/login')

@app.route('/Logout')
def Logout():
    session.clear()
    return redirect('/login')

# ---------------------------------------------------------------------------
# Faculty Arrangement & Substitution Algorithm
# ---------------------------------------------------------------------------
@app.route('/do_arrangement', methods=['GET', 'POST'])
@app.route('/Arrangement', methods=['GET', 'POST'])
@app.route('/arrangement', methods=['GET', 'POST'])
def do_arrangement():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        arr_day = request.form.get('day', session.get('day', 'monday')).lower().strip()
        if arr_day not in VALID_DAYS:
            arr_day = 'monday'
        session['day'] = arr_day

        absent = request.form.get('absent_teacher', '').strip().lower()

        # Step 1: Find all periods taught by absent teacher
        # Exclude free periods ('null' or 'null ')
        query_absent = f"SELECT ename, class, period FROM {arr_day} WHERE LOWER(TRIM(ename)) = %s AND LOWER(TRIM(class)) != 'null'"
        absent_records = db.query(query_absent, (absent,))

        if not absent_records:
            return render_template('arr_output.html', output_list=[], absent_teacher=absent)

        absent_periods = [r[2] for r in absent_records]

        # Step 2: Find free teachers during those exact periods
        # A teacher is free if TRIM(class) == 'null'
        query_free = f"SELECT ename, class, period FROM {arr_day} WHERE LOWER(TRIM(class)) = 'null' AND LOWER(TRIM(ename)) != %s"
        free_records = db.query(query_free, (absent,))

        # Group free teachers by period
        free_by_period = {}
        for row in free_records:
            t_name, _, prd = row
            if prd not in free_by_period:
                free_by_period[prd] = []
            free_by_period[prd].append(t_name)

        # Step 3: Construct arrangement matrix [period, class, free_teacher, period]
        # Step 3: Construct arrangement matrix and period status tracking
        arrangement_matrix = []
        period_sub_info = {}
        for absent_class_row in absent_records:
            t_name, assigned_class, prd = absent_class_row
            available_teachers = free_by_period.get(prd, [])
            for free_teacher in available_teachers:
                arrangement_matrix.append([prd, assigned_class, free_teacher, prd])

            has_free = len(available_teachers) > 0
            assigned_teacher = available_teachers[0] if has_free else None
            period_sub_info[prd] = {
                'class': assigned_class,
                'has_free': has_free,
                'assigned_teacher': assigned_teacher,
                'free_teachers': available_teachers,
                'free_teachers_str': ", ".join(available_teachers) if has_free else "None"
            }

        # Step 4: Construct Timetable Matrix Grid for the second interface
        sql_day = f"SELECT ename, class, period FROM {arr_day} ORDER BY period ASC, ename ASC"
        all_day_data = db.query(sql_day)
        teachers = sorted(list(set(row[0] for row in all_day_data if row[0])))
        periods = [1, 2, 3, 4, 5, 6, 7, 8]
        matrix_grid = {t: {p: 'Free' for p in periods} for t in teachers}
        for row in all_day_data:
            t, cls, p = row[0], row[1], row[2]
            if t in matrix_grid and p in matrix_grid[t]:
                if cls and cls.strip().lower() not in ('null', ''):
                    matrix_grid[t][p] = cls.strip().upper()
                else:
                    matrix_grid[t][p] = 'Free'

        substitute_duties = {}
        for prd, s_info in period_sub_info.items():
            if s_info['assigned_teacher']:
                substitute_duties[(s_info['assigned_teacher'].lower(), prd)] = {
                    'class': s_info['class'],
                    'absent_teacher': absent
                }

        return render_template(
            'arr_output.html',
            output_list=arrangement_matrix,
            absent_teacher=absent,
            arr_day=arr_day,
            teachers=teachers,
            periods=periods,
            matrix_grid=matrix_grid,
            period_sub_info=period_sub_info,
            substitute_duties=substitute_duties
        )

    return render_template('Arrangement.html')

@app.route('/diffrent_teacher')
def diffrent_teacher():
    return render_template('Arrangement.html')

@app.route('/back_to_home_page')
def back_to_home_page():
    if session.get('role') == 'A':
        return redirect('/dashboard_admin')
    return redirect('/dashboard_user')

# ---------------------------------------------------------------------------
# Timetable Viewing & Exporting
# ---------------------------------------------------------------------------
@app.route('/VIEW_TIMETABLE', methods=['GET'])
@app.route('/view_timetable', methods=['GET'])
def VIEW_TIMETABLE():
    if 'username' in session:
        day = session.get('day', 'monday')
        if day not in VALID_DAYS:
            day = 'monday'
        sql5 = f"SELECT ename, class, period FROM {day} ORDER BY period ASC, ename ASC"
        alldat = db.query(sql5)

        # Prepare Institutional Timetable Matrix (Table Grid View)
        teachers = sorted(list(set(row[0] for row in alldat if row[0])))
        periods = [1, 2, 3, 4, 5, 6, 7, 8]
        matrix_grid = {t: {p: 'Free' for p in periods} for t in teachers}
        for row in alldat:
            t, cls, p = row[0], row[1], row[2]
            if t in matrix_grid and p in matrix_grid[t]:
                if cls and cls.strip().lower() not in ('null', ''):
                    matrix_grid[t][p] = cls.strip().upper()
                else:
                    matrix_grid[t][p] = 'Free'

        return render_template(
            'View_Day_timetable.html',
            output_list=alldat,
            teachers=teachers,
            periods=periods,
            matrix_grid=matrix_grid,
            day=day
        )
    return redirect('/login')

@app.route('/Download_File', methods=['GET'])
@app.route('/download_file', methods=['GET'])
def Download_File():
    if 'username' not in session:
        return redirect('/login')

    day = session.get('day', 'monday')
    if day not in VALID_DAYS:
        day = 'monday'

    sql5 = f"SELECT ename, class, period FROM {day} ORDER BY period ASC, ename ASC"
    output_list = db.query(sql5)

    download_dir = os.path.join(BASE_DIR, 'Download_files')
    os.makedirs(download_dir, exist_ok=True)

    filename = f"{day}_timetable_{date.today()}"
    filepath = os.path.join(download_dir, f"{filename}.csv")

    with open(filepath, "w", newline="", encoding="utf-8") as file1:
        csvwriter = csv.writer(file1)
        csvwriter.writerow(["Teacher", "Class", "Period"])
        for row in output_list:
            cls = "null" if row[1] is None or row[1].strip() == '' else row[1]
            csvwriter.writerow([row[0], cls, row[2]])

    return send_file(filepath, as_attachment=True, download_name=f"{filename}.csv")

# ---------------------------------------------------------------------------
# User Administration
# ---------------------------------------------------------------------------
@app.route('/ADD_USER', methods=['GET', 'POST'])
@app.route('/add_user', methods=['GET', 'POST'])
def ADD_USER():
    if session.get('role') != 'A':
        return redirect('/login')

    if request.method == 'POST':
        username_nusers = request.form.get('Newusername', '').strip()
        password_nusers = request.form.get('password', '').strip()
        mode_nusers = request.form.get('role', 'U').strip()

        if username_nusers and password_nusers:
            if db.engine == 'sqlite':
                db.query(
                    "INSERT OR REPLACE INTO users VALUES (%s, %s, %s)",
                    (username_nusers, password_nusers, mode_nusers),
                    commit=True
                )
            else:
                db.query(
                    "REPLACE INTO users VALUES (%s, %s, %s)",
                    (username_nusers, password_nusers, mode_nusers),
                    commit=True
                )
        return Logout()
    return render_template('Add_User.html')

@app.route('/REMOVE_USER', methods=['GET', 'POST'])
@app.route('/remove_user', methods=['GET', 'POST'])
def REMOVE_USER():
    if session.get('role') != 'A':
        return redirect('/login')

    userdetails = db.query("SELECT username FROM users ORDER BY username ASC")
    return render_template('Remove_user.html', output_list1=userdetails)

@app.route('/Delete_User', methods=['GET', 'POST'])
def Delete_User():
    if session.get('role') != 'A':
        return redirect('/login')

    if request.method == 'POST':
        user_to_delete = request.form.get('userToRemove', 'DEFAULT').strip()
        if user_to_delete != "DEFAULT":
            db.query("DELETE FROM users WHERE username = %s", (user_to_delete,), commit=True)
            if session.get('username') == user_to_delete:
                return Logout()
        return redirect('/dashboard_admin')
    return render_template('Remove_user.html')

# ---------------------------------------------------------------------------
# Data Ingestion & Timetable Operations
# ---------------------------------------------------------------------------
@app.route('/INSERT_DATA', methods=['GET', 'POST'])
@app.route('/insert_data', methods=['GET', 'POST'])
def INSERT_DATA():
    if session.get('role') != 'A':
        return redirect('/login')

    if request.method == 'POST':
        day = request.form.get('insert_day', 'monday').lower().strip()
        if day not in VALID_DAYS:
            day = 'monday'
        session['day'] = day

        csv_file = request.files.get('csv_file')
        locat = request.form.get('locatio', '').strip()

        records_to_insert = []

        def extract_csv_records(stream_or_file):
            valid_recs = []
            reader = csv.reader(stream_or_file)
            for row in reader:
                if not row or len(row) < 3:
                    continue
                ename = row[0].strip()
                cls = row[1].strip()
                try:
                    p_val = int(row[2].strip())
                    if ename:
                        valid_recs.append((ename, cls, p_val))
                except (ValueError, TypeError):
                    # Gracefully skip header rows (e.g. Teacher,Class,Period) or invalid numbers
                    continue
            return valid_recs

        # Option A: Direct browser file upload
        if csv_file and csv_file.filename != '':
            stream = io.StringIO(csv_file.stream.read().decode("utf-8-sig", errors="ignore"))
            records_to_insert = extract_csv_records(stream)
        # Option B: Server / relative file path
        elif locat:
            target_path = locat if os.path.isabs(locat) else os.path.join(BASE_DIR, locat)
            if os.path.exists(target_path):
                with open(target_path, "r", newline="", encoding="utf-8-sig", errors="ignore") as f:
                    records_to_insert = extract_csv_records(f)

        # Insert records into selected day's table
        if records_to_insert:
            for rec in records_to_insert:
                db.query(f"INSERT INTO {day} VALUES (%s, %s, %s)", rec, commit=True)

        return redirect('/VIEW_TIMETABLE')

    return render_template("Insert_Data.html")

@app.route('/DELETE_COMPLETE_DAY', methods=['GET', 'POST'])
@app.route('/delete_complete_day', methods=['GET', 'POST'])
def DELETE_COMPLETE_DAY():
    if session.get('role') != 'A':
        return redirect('/login')

    if request.method == 'POST':
        day = request.form.get('Selete_Day_del', '').lower().strip()
        if day in VALID_DAYS:
            db.query(f"DELETE FROM {day}", commit=True)
        return redirect('/dashboard_admin')
    return render_template("Delete_Complete_Day.html")

@app.route('/REMOVE_TEACHER_DATA', methods=['GET', 'POST'])
@app.route('/remove_teacher_data', methods=['GET', 'POST'])
@app.route('/REMOVE_TEACHER_DEF_DAY', methods=['GET', 'POST'])
@app.route('/remove_teacher_def_day', methods=['GET', 'POST'])
def REMOVE_TEACHER_DATA():
    if session.get('role') != 'A':
        return redirect('/login')

    day = session.get('day', 'monday')
    if day not in VALID_DAYS:
        day = 'monday'

    if request.method == 'POST':
        teacher = request.form.get('teacherToRemove', 'DEFAULT').strip()
        if teacher != "DEFAULT":
            db.query(f"DELETE FROM {day} WHERE ename = %s", (teacher,), commit=True)
        return redirect('/dashboard_admin')

    teach_details = db.query(f"SELECT DISTINCT ename FROM {day} WHERE ename IS NOT NULL ORDER BY ename ASC")
    return render_template('Remove_Teacher_data.html', output_list2=teach_details)

# ---------------------------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "="*70)
    print("AUTOMATED FACULTY ABSENCE & SUBSTITUTION MANAGEMENT SYSTEM (2024)")
    print("Project ID: 006/2024 | Author: M Nandish | All Rights Reserved")
    print("Notice: Exclusive written permission required for copy/edit/use.")
    print("        Commercial use is strictly prohibited.")
    print("Default Admin Credentials:  Username: admin  | Password: 1234")
    print("Default User Credentials:   Username: user   | Password: 1234")
    print("Web Server Port: http://127.0.0.1:5000")
    print("="*70 + "\n")
    try:
        # use_reloader=False prevents Werkzeug from raising SystemExit(3)
        # when running under IDE debuggers (e.g. debugpy) or standard sessions
        app.run(debug=True, port=5000, use_reloader=False)
    except SystemExit:
        pass
