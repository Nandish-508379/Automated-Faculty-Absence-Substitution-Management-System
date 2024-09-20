# Automated Faculty Absence & Substitution Management System

[![Project ID](https://img.shields.io/badge/Project%20ID-006%2F2024-blue.svg)](https://github.com/)
[![Year](https://img.shields.io/badge/Year-2024-green.svg)](https://github.com/)
[![Edition](https://img.shields.io/badge/Smart%20India%20Hackathon-Presentation%20Edition-orange.svg)](https://github.com/)
[![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)](https://github.com/)

**Automated Faculty Absence & Substitution Management System** is a full-featured web-based institutional scheduling and teacher substitution allocation platform. It automatically detects absent faculty members, identifies free periods, and computes clash-free substitute faculty assignments in seconds.

---

## 📌 Project Information

- **Project Title:** Automated Faculty Absence & Substitution Management System
- **Project ID:** `006/2024`
- **Creation Year:** `2024`
- **Author & Rights Holder:** M Nandish (All Rights Reserved)
- **Competition & Presentation:** Smart India Hackathon Presentation Edition

---

## 🎓 Academic Heritage & Genesis

This project has an authentic, multi-year developmental lineage spanning school and university coursework through national competition presentation:

1. **2022 – Foundational CLI Engine (Class 12 CBSE Mini Project):**
   - **Institution:** Kendriya Vidyalaya AFS Yelahanka, Bengaluru (Class 12, 2022).
   - **Domain:** Computer Science Mini Project (Python + MySQL).
   - **Scope:** Conceived and built the core substitution algorithm (`main.py`) to solve the real-world administrative challenge of daily manual timetable substitution slips for faculty on leave.

2. **2023 – Web Architecture Integration (MSRIT):**
   - **Institution:** M. S. Ramaiah Institute of Technology (MSRIT, 2023).
   - **Course:** *Introduction to Web Development*.
   - **Scope:** Transformed the standalone CLI script into an interactive web application using Python Flask, establishing the progressive versions `WEB01` through `WEB07`.

3. **2024 – Comprehensive Enterprise System (Project ID: 006/2024):**
   - **Milestone:** Full system redesign (`WEB08` through `WEB10`).
   - **Enhancements:** Dual-database architecture (MySQL + zero-config SQLite fallback), robust CSV data ingestion, printable official timetable documents, offline design system, and packaged for the **Smart India Hackathon Presentation Edition**.

---

## 🚀 Key Features

1. **Automated Faculty Substitution Engine:**
   - Detects all periods where an absent faculty member has assigned classes.
   - Cross-references the master schedule for teachers with free slots (`null`) during those exact periods.
   - Generates an instant substitution matrix with zero slot collisions.

2. **Master Timetable Management:**
   - Supports 6-day academic cycles (Monday through Saturday) with up to 8 periods per day.
   - Interactive, searchable timetable view with live instant filtering by teacher or class.
   - Printable layout (`@media print`) formatted specifically for official institutional printouts.

3. **Data Ingestion & Export:**
   - **Direct Browser CSV Upload:** Drag and drop or browse CSV timetable files directly through the web UI.
   - **Workspace File Path Import:** Import from local workspace data files (e.g. `INITIALISE/newrecc.csv`).
   - **One-Click CSV Export:** Download active day timetables formatted with headers and period numbers.

4. **Role-Based Access Control (RBAC):**
   - **Administrator (`role: A`):** Full control over arrangements, schedule imports, data purging, teacher schedule deletion, and user credential provisioning.
   - **Faculty / User (`role: U`):** Access to view daily timetables, search schedules, view arrangement matrices, and change account passwords.

5. **Resilient Dual-Database Architecture:**
   - **Production Engine:** Native support for MySQL (`timetable` database).
   - **Zero-Config Standalone Engine:** Automatic fallback to SQLite (`timetable.db`) with automatic schema creation and initial data seeding if MySQL is offline or not installed. Enables immediate out-of-the-box testing without setup hurdles.

6. **Modern Design System:**
   - Clean, professional aesthetic using curated CSS tokens, glassmorphism cards, and responsive grids.
   - Dedicated styling across desktop, tablet, mobile, and printed slips.

---

## 📈 Version Progression & Evolution

| Version | Milestone & Progression Description |
| :--- | :--- |
| **`WEB01`** | Initial migration from CLI (`main.py`) to web-based Flask framework; basic login prototype. |
| **`WEB02`** | Route structuring and separation of web endpoints; CLI script preserved for verification. |
| **`WEB03` - `WEB04`** | Decoupled core arrangement algorithm into dedicated module (`arran.py`). |
| **`WEB05 arrangement wrking`** | Successfully verified faculty substitution logic over HTTP request cycles. |
| **`WEB06`** | Route refinement, module dependency tracking, and error checks. |
| **`WEB07 ARRANGEMENTS DONE`** | Complete implementation of multi-teacher free-period matching matrix in `app.py`. |
| **`WEB08 MAX WORKING`** | Added master schedule viewing, CSV download export, user addition/removal, and day deletion. |
| **`WEB09 ALL WORKING`** | Fully integrated web app with initialization scripts and `Download_files` structure. |
| **`WEB10 ENHANCED INITIALISATION`** | **Primary Stable Release:** Dual-database engine (MySQL + automatic SQLite fallback), browser CSV uploads, SQL injection protection, complete modern CSS design system, and Project ID `006/2024` branding. |
| **`2024 SMART_INDIA_HACKATHON_PRESENTATION`** | Clean, packaged presentation edition prepared for the Smart India Hackathon showcase. |

---

## ⚙️ Quick Start & Running the Application

### 1. Prerequisites
- Python 3.8+ (Tested with Python 3.10, 3.12, 3.14)
- Flask (`pip install flask`)
- MySQL Connector (`pip install mysql-connector-python`)

### 2. Launching the Application
Navigate to the primary release folder and run:
```bash
cd "WEB10 ENHANCED INITIALISATION"
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. Default Login Credentials
| Role | Username | Password | Default Day | Permissions |
| :--- | :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `1234` | Monday | Full Administrative Access |
| **Faculty / User** | `user` | `1234` | Monday | Read Timetables & View Arrangements |

*(Tip: The login page includes one-click autofill buttons for rapid testing.)*

### 4. Testing Faculty Substitution
1. Sign in as `admin`.
2. Click **"Compute Arrangements"** (or open `/do_arrangement`).
3. Select Day: **Monday**.
4. Enter Absent Teacher code: `kvgs` (or `sj`, `anu`, `gn`, `him`).
5. Click **"Compute Arrangements"**.
6. View the generated substitution matrix with substitute teachers and period numbers.

---

## 🗄️ Database Setup (Optional for Production MySQL)

The system automatically operates on a standalone embedded SQLite database if MySQL is not running. To connect to a dedicated MySQL instance:

1. Configure MySQL credentials in `.env` (or copy from `.env.example`):
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=timetable
   ```
2. Initialize database schema:
   ```bash
   cd "WEB10 ENHANCED INITIALISATION/INITIALISE"
   python "INITIALISE PROGRAM.py"
   ```

---

## 🔒 GitHub & Security Exclusions

The repository includes a comprehensive `.gitignore` and template `.env.example`:
- Hardcoded database passwords and sensitive environment configurations are excluded via `.env`.
- Personal local file paths have been replaced with standard relative paths and browser file uploads.
- Python caches (`__pycache__/`, `*.pyc`), SQLite test databases (`*.db`), and temporary user-generated CSV downloads are excluded from version control.

---

## 📄 License & Attribution

```text
Automated Faculty Absence & Substitution Management System
Project ID: 006/2024
Year: 2024
Author: M Nandish
All Rights Reserved.
```
