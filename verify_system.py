"""
Comprehensive End-to-End System Audit & Demonstration Verification
Validates every page, route, database table, form validation, chart and asset.
"""
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(__file__))

import database
database.init_db()
import app

def run_audit():
    client = app.app.test_client()
    print("=" * 65)
    print("  AI-Based Academic Performance Prediction System - Master Audit")
    print("=" * 65)

    # 1. Routes
    print("\n[1/6] Testing All Page Routes...")
    routes = ['/', '/predict', '/dashboard', '/about']
    for r in routes:
        res = client.get(r)
        assert res.status_code == 200, f"Route {r} returned {res.status_code}"
        print(f"  + Route {r:<15} [200 OK]")

    # 2. Static Assets
    print("\n[2/6] Auditing Static Assets...")
    assets = [
        '/static/css/style.css',
        '/static/js/main.js',
        '/static/js/form.js',
        '/static/js/dashboard.js'
    ]
    for s in assets:
        res = client.get(s)
        assert res.status_code == 200, f"Asset {s} failed"
        assert len(res.data) > 50, f"Asset {s} is empty"
        print(f"  + Asset {s:<25} [{len(res.data):>6} bytes]")

    # 3. Form Validation
    print("\n[3/6] Testing Impossible Value Form Validation...")
    # Attendance > 100
    res_inv1 = client.post('/predict', data={
        'student_name': 'Test User', 'student_id': 'T-01', 'attendance_percentage': '130'
    }, follow_redirects=True)
    assert res_inv1.status_code == 200
    assert b'Invalid Attendance' in res_inv1.data
    print("  + Impossible attendance (>100%) rejected successfully")

    # Negative marks
    res_inv2 = client.post('/predict', data={
        'student_name': 'Test User', 'student_id': 'T-02', 'previous_grade': '-10'
    }, follow_redirects=True)
    assert res_inv2.status_code == 200
    assert b'Invalid Previous Grade' in res_inv2.data
    print("  + Negative previous grade rejected successfully")

    # Empty Name
    res_inv3 = client.post('/predict', data={
        'student_name': '', 'student_id': 'T-03'
    }, follow_redirects=True)
    assert res_inv3.status_code == 200
    assert b'Please enter the student full name' in res_inv3.data
    print("  + Empty student name rejected successfully")

    # 4. Valid Form Submission & Results Page
    print("\n[4/6] Testing End-to-End Prediction Submission...")
    student_payload = {
        'student_name': 'Ananya Deshmukh',
        'student_id': 'STU-2026-DEMO',
        'current_semester': 'Semester 6',
        'department': 'Computer Science & AI',
        'previous_grade': '88.5',
        'internal_marks': '91.0',
        'assignments_completed_pct': '96.0',
        'attendance_percentage': '94.0',
        'num_subjects': '6',
        'daily_study_hours': '3.5',
        'study_hours_per_week': '22.0',
        'social_media_hours': '1.5',
        'sleep_hours': '7.5',
        'study_sessions_per_week': '6',
        'extracurricular_hours': '4.0',
        'attends_coaching': 'No - Pure Self Study',
        'academic_confidence': 'High',
        'stress_level': '3',
        'parental_involvement': 'High',
        'internet_access': 'Yes'
    }
    post_res = client.post('/predict', data=student_payload, follow_redirects=True)
    assert post_res.status_code == 200
    html = post_res.data.decode('utf-8')
    assert 'Ananya Deshmukh' in html
    assert 'STU-2026-DEMO' in html
    assert 'Download Report' in html
    assert 'gaugeCircle' in html
    assert 'comparisonBarChart' in html
    assert 'Personalized Academic Analysis' in html
    assert 'Identified Academic Strengths' in html
    assert 'Areas for Improvement' in html
    assert 'Personalized Study Recommendations' in html
    print("  + Form processed, saved to SQLite, and redirected to Result Page")
    print("  + All 9 Results elements verified (Gauge, Comparison Bar, Strengths, Recommendations, Download)")

    # 5. Dashboard Verification
    print("\n[5/6] Testing Automatic Dashboard Update...")
    dash_res = client.get('/dashboard')
    assert dash_res.status_code == 200
    dash_html = dash_res.data.decode('utf-8')
    assert 'Ananya Deshmukh' in dash_html, "Dashboard did not update with latest student"
    assert 'STU-2026-DEMO' in dash_html
    assert 'Attendance Overview' in dash_html
    assert 'Study Hours Overview' in dash_html
    assert 'progressLineChart' in dash_html
    assert 'subjectBarChart' in dash_html
    assert 'Export CSV' in dash_html
    assert 'studentProfileSelect' in dash_html
    print("  + Dashboard automatically updated with latest student")
    print("  + Profile card, overview widgets, progress line chart, subject chart, and history table verified")

    # 6. REST API Endpoints
    print("\n[6/6] Testing REST JSON Endpoints...")
    api_res = client.post('/api/predict', json={'study_hours_per_week': 20, 'attendance_percentage': 90, 'previous_grade': 85})
    assert api_res.status_code == 200
    assert api_res.get_json()['status'] == 'success'
    print("  + POST /api/predict [200 OK]")

    stats_res = client.get('/api/stats')
    assert stats_res.status_code == 200
    total = stats_res.get_json()['total']
    print(f"  + GET /api/stats [200 OK] (Total records: {total})")

    print("\n" + "=" * 65)
    print("  AUDIT RESULT: ALL CHECKS PASSED WITH 100% SUCCESS!")
    print("  WEBSITE IS PRESENTATION-READY FOR COLLEGE DEMONSTRATION")
    print("=" * 65)

if __name__ == '__main__':
    run_audit()
