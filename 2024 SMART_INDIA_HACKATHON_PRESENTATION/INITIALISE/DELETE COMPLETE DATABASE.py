"""
=============================================================================
TIMETABLE MANAGEMENT SYSTEM - DATABASE PURGE UTILITY
Project ID: 006/2024 | Year: 2024
Smart India Hackathon Presentation Edition
=============================================================================
"""

import os
import mysql.connector as proj

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '8379')

try:
    con = proj.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD)
    cur = con.cursor()
    cur.execute("DROP DATABASE IF EXISTS timetable;")
    con.commit()
    con.close()
    print("[SUCCESS] Database 'timetable' successfully purged from MySQL.")
except Exception as e:
    print(f"[ERROR] Could not purge MySQL database: {e}")
