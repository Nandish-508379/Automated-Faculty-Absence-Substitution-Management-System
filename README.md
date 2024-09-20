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
| **`WEB05 arrangement wrking`** | `v0.5` | Successfully verified faculty substitution logic over HTTP request cycles. |
| **`WEB06`** | `v0.6` | Route refinement, module dependency tracking, and error checks. |
| **`WEB07 ARRANGEMENTS DONE`** | `v0.7` | Complete implementation of multi-teacher free-period matching matrix in `app.py`. |
| **`WEB08 MAX WORKING`** | `v0.8` | Added master schedule viewing, CSV download export, user addition/removal, and day deletion. |
| **`WEB09 ALL WORKING`** | `v0.9` | Fully integrated web app with initialization scripts and `Download_files` structure. |
| **`WEB10 ENHANCED INITIALISATION`** | `v1.0` | Production Master Release: Dual-database engine (MySQL + automatic SQLite fallback), dual-interface timetable matrix grid, CSV file upload, and modern offline design system. |
| **`2024 SMART_INDIA_HACKATHON_PRESENTATION`** | - | Clean, packaged presentation edition prepared for the Smart India Hackathon showcase. |

*(All historical version directories are preserved and documented inside [`legacy_versions/`](file:///e:/2024_006%20WEB_TIMETABLE_MANAGEMENT%20SYSTEM/legacy_versions).)*

---

## 📂 Repository Structure

```text
├── app.py                     # Primary Application Entry Point (Run this!)
├── run.bat                    # One-Click Windows Launcher
├── requirements.txt           # Project Dependencies (Flask, mysql-connector-python)
├── .env.example               # Environment Configuration Template
├── .gitignore                 # GitHub Ignore Rules (Excludes secrets, db, cache)
├── templates/                 # Production Web Templates (Dual Grid/List UI)
├── static/                    # Offline CSS Design System
├── INITIALISE/                # DB Setup Scripts & Sample Data (newrecc.csv)
├── Download_files/            # Directory for Exported Timetable CSVs
├── 2024 SMART_INDIA_.../      # Smart India Hackathon Presentation Package
└── legacy_versions/           # Archived Chronological Code History (WEB01 - WEB10)
```

---

## ⚙️ Quick Start & Running the Application

### 1. Installation
Install project dependencies:
```bash
pip install -r requirements.txt
```

### 2. Launching the Application
Run the root application (or double-click `run.bat` on Windows):
```bash
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

---

## 🏷️ Publishing to GitHub with Release Tags

To publish the complete project to GitHub with official version tags (`v0.1` to `v1.0`):

```bash
# 1. Initialize Git repository
git init

# 2. Stage all clean files and commit
git add .
git commit -m "feat: Automated Faculty Absence & Substitution Management System (v1.0 Production)"

# 3. Create historical release tags for GitHub
git tag -a v0.1 -m "Version 0.1 - Initial CLI to Flask Prototype (KV AFS Yelahanka)"
git tag -a v0.2 -m "Version 0.2 - Modular Route Architecture (MSRIT)"
git tag -a v0.3 -m "Version 0.3 - Decoupled Arrangement Engine"
git tag -a v0.4 -m "Version 0.4 - Refined Absent Teacher Queries"
git tag -a v0.5 -m "Version 0.5 - HTTP Substitution Integration"
git tag -a v0.6 -m "Version 0.6 - Module Dependency Specifications"
git tag -a v0.7 -m "Version 0.7 - Multi-Faculty Arrangement Completion"
git tag -a v0.8 -m "Version 0.8 - Timetable Viewing & Exporting"
git tag -a v0.9 -m "Version 0.9 - Database Initializer Scripts"
git tag -a v1.0 -m "Version 1.0 - Production Release (Smart India Hackathon Presentation Edition)"

# 4. Link your GitHub remote and push with tags
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git branch -M main
git push -u origin main --tags
```

---

## 📄 License & Attribution

```text
Automated Faculty Absence & Substitution Management System
Project ID: 006/2024
Year: 2024
Author: M Nandish
All Rights Reserved.
```
