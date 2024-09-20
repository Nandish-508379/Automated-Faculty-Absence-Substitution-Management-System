"""
=============================================================================
TIMETABLE MANAGEMENT SYSTEM - DATABASE INITIALIZATION
Project ID: 006/2024 | Year: 2024
Smart India Hackathon Presentation Edition
=============================================================================
"""

import os
import mysql.connector as proj

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '8379')

print("\n--- Connecting to MySQL Database Server ---")
try:
    con = proj.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD)
    cur = con.cursor()
    print("Connection established successfully!\n")

    cur.execute("CREATE DATABASE IF NOT EXISTS timetable;")
    print("[1/8] Database 'timetable' ensured.")

    cur.execute("USE timetable;")
    print("[2/8] Switched to database 'timetable'.")

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    for day in days:
        cur.execute(f"CREATE TABLE IF NOT EXISTS {day} (ename VARCHAR(10), class VARCHAR(5), period INT);")
    print("[3/8] Weekday timetable tables (Monday-Saturday) created.")

    cur.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(15) PRIMARY KEY, password VARCHAR(10), role CHAR(1));")
    print("[4/8] Users authentication table created.")

    cur.execute("INSERT IGNORE INTO users VALUES ('admin', '1234', 'A');")
    print("[5/8] Default administrator account seeded (admin / 1234).")

    cur.execute("INSERT IGNORE INTO users VALUES ('user', '1234', 'U');")
    print("[6/8] Default faculty user account seeded (user / 1234).")

    con.commit()
    con.close()
    print("\n" + "="*65)
    print("Database initialization complete! Ready to launch system.")
    print("Default Admin:  username = admin  |  password = 1234")
    print("Default User:   username = user   |  password = 1234")
    print("="*65 + "\n")

except Exception as err:
    print(f"\n[ERROR] Could not connect to MySQL server: {err}")
    print("Note: The Flask application (app.py) also includes an automatic")
    print("standalone SQLite fallback so you can run the system immediately.")
