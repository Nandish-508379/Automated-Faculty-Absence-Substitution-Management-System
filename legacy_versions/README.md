# Archive: Developmental Version History (WEB01 to WEB10)

This directory preserves the complete chronological code history of the **Automated Faculty Absence & Substitution Management System** from initial CLI migration to the stable enterprise edition.

---

## 📅 Chronological Version Roadmap

| Directory | Tag | Core Milestone Description | Key Technical Addition |
| :--- | :--- | :--- | :--- |
| **`WEB01`** | `v0.1` | **Initial Flask Prototype:** Ported CLI script to web routes. | Basic login form and session cookie foundation. |
| **`WEB02`** | `v0.2` | **Route Structuring:** Separated admin endpoints while retaining CLI reference. | Route dispatching and day session tracking. |
| **`WEB03`** | `v0.3` | **Algorithm Decoupling:** Separated arrangement logic into `arran.py`. | Modularization of algorithm components. |
| **`WEB04`** | `v0.4` | **Arrangement Testing:** Refined query lookups for absent teachers. | Query parameter passing and result filtering. |
| **`WEB05 arrangement wrking`** | `v0.5` | **Substitution Working:** First working HTTP request-response cycle. | Working period collision checks. |
| **`WEB06`** | `v0.6` | **Module Tracking:** Added dependency specifications (`all modules.txt`). | Requirements tracking and error checks. |
| **`WEB07 ARRANGEMENTS DONE`** | `v0.7` | **Core Logic Completed:** Full multi-teacher substitution matrix completed. | End-to-end arrangement algorithm in `app.py`. |
| **`WEB08 MAX WORKING`** | `v0.8` | **Feature Complete:** Added timetable viewing, CSV export, and user management. | `VIEW_TIMETABLE`, CSV generation, and user routes. |
| **`WEB09 ALL WORKING`** | `v0.9` | **Operational Release:** Automated database initialization scripts. | `INITIALISE PROGRAM.py`, `DELETE COMPLETE DATABASE.py`. |
| **`WEB10 ENHANCED INITIALISATION`** | `v1.0` | **Production Master Release:** Dual-database engine (MySQL + SQLite fallback), dual-interface timetable matrix grid, CSV file upload, and modern offline design system. | Dual-engine database adapter, matrix grid view, and security hardening. |

---

## 📌 Active Production Code
The current active, runnable production version of the application is located at the **repository root directory** (`/app.py`).
To run the latest release:
```bash
python app.py
```
