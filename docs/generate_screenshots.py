import os
import sys
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db

os.makedirs('docs/screenshots', exist_ok=True)
edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

def snap(html_data, filename, width=1366, height=850):
    content = html_data.replace('/static/', '../../static/')
    temp_file = os.path.abspath(f'docs/screenshots/temp_{filename}.html')
    out_png = os.path.abspath(f'docs/screenshots/{filename}.png')
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content)
    cmd = [edge, '--headless', '--disable-gpu', f'--window-size={width},{height}', f'--screenshot={out_png}', f'file:///{temp_file}']
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print(f'Captured {filename}.png ({os.path.getsize(out_png)} bytes)')

client = app.test_client()

# 1. Login Page
res = client.get('/login')
snap(res.data.decode('utf-8'), '01_login_page', 1366, 880)

# Set admin session
with client.session_transaction() as sess:
    sess['username'] = 'admin'
    sess['role'] = 'A'
    sess['day'] = 'monday'

# 2. Admin Dashboard
res = client.get('/dashboard_admin')
snap(res.data.decode('utf-8'), '02_admin_dashboard', 1366, 850)

# 3. User Dashboard
with client.session_transaction() as sess:
    sess['username'] = 'user'
    sess['role'] = 'U'
    sess['day'] = 'monday'
res = client.get('/dashboard_user')
snap(res.data.decode('utf-8'), '03_user_dashboard', 1366, 850)

# Revert to admin
with client.session_transaction() as sess:
    sess['username'] = 'admin'
    sess['role'] = 'A'
    sess['day'] = 'monday'

# 4. Master Timetable Grid View
res = client.get('/VIEW_TIMETABLE')
raw_html = res.data.decode('utf-8')
snap(raw_html, '04_master_timetable_grid', 1366, 850)

# 5. Master Timetable List View
list_html = raw_html.replace('id="gridView" class="view-section active"', 'id="gridView" class="view-section"').replace('id="listView" class="view-section"', 'id="listView" class="view-section active"')
snap(list_html, '05_master_timetable_list', 1366, 850)

# 6. Faculty Absence Arrangement Request Page
res = client.get('/Arrangement')
snap(res.data.decode('utf-8'), '06_arrangement_request', 1366, 850)

# 7. Substitution Allocation Output (Absence = 'kvgs')
res = client.post('/do_arrangement', data={'day': 'monday', 'absent_teacher': 'kvgs'})
raw_arr_html = res.data.decode('utf-8')
snap(raw_arr_html, '07_substitution_matrix_grid', 1366, 920)

# 8. Substitution Allocation List View
list_arr_html = raw_arr_html.replace('id="gridView" class="view-section active"', 'id="gridView" class="view-section"').replace('id="listView" class="view-section"', 'id="listView" class="view-section active"')
snap(list_arr_html, '08_substitution_table_list', 1366, 850)

# 9. CSV Data Ingestion Portal
res = client.get('/INSERT_DATA')
snap(res.data.decode('utf-8'), '09_import_timetable_csv', 1366, 900)

# 10. User Account Provisioning (Add User)
res = client.get('/ADD_USER')
snap(res.data.decode('utf-8'), '10_add_user_rbac', 1366, 850)

# 11. User Account De-provisioning (Remove User)
res = client.get('/REMOVE_USER')
snap(res.data.decode('utf-8'), '11_remove_user', 1366, 850)

# 12. Purge Faculty Schedule
res = client.get('/REMOVE_TEACHER_DEF_DAY')
snap(res.data.decode('utf-8'), '12_purge_faculty_schedule', 1366, 850)

# 13. Purge Complete Day
res = client.get('/DELETE_COMPLETE_DAY')
snap(res.data.decode('utf-8'), '13_purge_complete_day', 1366, 850)

# 14. Change Password
res = client.get('/CHANGE_PWD')
snap(res.data.decode('utf-8'), '14_change_password', 1366, 850)

print('All 14 screenshots successfully generated!')
