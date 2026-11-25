import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'academic_records.db')

def get_db_connection():
    """Create and return a database connection with dict-like row access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_columns(conn):
    """Ensure newly added columns exist in the table."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(predictions)")
    existing_cols = {row['name'] for row in cursor.fetchall()}
    
    new_cols = {
        'current_semester': "TEXT DEFAULT 'Semester 5'",
        'internal_marks': "REAL DEFAULT 75.0",
        'num_subjects': "INTEGER DEFAULT 6",
        'daily_study_hours': "REAL DEFAULT 2.5",
        'social_media_hours': "REAL DEFAULT 2.0",
        'study_sessions_per_week': "INTEGER DEFAULT 5",
        'attends_coaching': "TEXT DEFAULT 'No'",
        'academic_confidence': "TEXT DEFAULT 'Moderate'",
        'performance_category': "TEXT DEFAULT 'Good'",
        'strengths': "TEXT DEFAULT '[]'",
        'improvements': "TEXT DEFAULT '[]'",
        'analysis_summary': "TEXT DEFAULT ''",
        'is_sample': "INTEGER DEFAULT 0"
    }
    
    for col, col_def in new_cols.items():
        if col not in existing_cols:
            try:
                cursor.execute(f"ALTER TABLE predictions ADD COLUMN {col} {col_def}")
            except Exception:
                pass
    
    # Mark seeded benchmark records as sample data
    try:
        cursor.execute("UPDATE predictions SET is_sample = 1 WHERE student_id IN ('STU-2024-101', 'STU-2024-102', 'STU-2024-103', 'STU-2024-104', 'STU-2024-105')")
    except Exception:
        pass

    conn.commit()

def init_db():
    """Initialize database tables and seed baseline benchmark records if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            student_id TEXT NOT NULL,
            gender TEXT,
            department TEXT,
            current_semester TEXT DEFAULT 'Semester 5',
            previous_grade REAL NOT NULL,
            internal_marks REAL DEFAULT 75.0,
            assignments_completed_pct REAL NOT NULL,
            attendance_percentage REAL NOT NULL,
            num_subjects INTEGER DEFAULT 6,
            daily_study_hours REAL DEFAULT 2.5,
            study_hours_per_week REAL NOT NULL,
            social_media_hours REAL DEFAULT 2.0,
            sleep_hours REAL NOT NULL,
            study_sessions_per_week INTEGER DEFAULT 5,
            extracurricular_hours REAL NOT NULL,
            attends_coaching TEXT DEFAULT 'No',
            academic_confidence TEXT DEFAULT 'Moderate',
            stress_level INTEGER NOT NULL,
            parental_involvement TEXT NOT NULL,
            internet_access TEXT NOT NULL,
            predicted_score REAL NOT NULL,
            predicted_gpa REAL NOT NULL,
            predicted_grade_letter TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            confidence_score REAL NOT NULL,
            factor_breakdown TEXT,
            recommendations TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    ensure_columns(conn)
    
    # Check if we should insert initial benchmark sample records
    cursor.execute('SELECT COUNT(*) FROM predictions')
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_records = [
            (
                "Aarav Sharma", "STU-2024-101", "Male", "Computer Science",
                24.0, 94.5, 88.0, 7.5, 96.0, 4.0, 3, "High", "Yes",
                91.8, 3.92, "A+", "Low Risk", 95.4,
                json.dumps({"attendance": 9.5, "study_hours": 9.0, "past_grade": 9.2, "consistency": 9.6}),
                json.dumps([
                    "Outstanding academic trajectory! Maintain this momentum.",
                    "Consider taking on research or competitive coding challenges.",
                    "Sustain regular sleep patterns (7.5 hrs) during final exams."
                ]),
                "2026-11-20 10:15:00"
            ),
            (
                "Priya Patel", "STU-2024-102", "Female", "Electronics",
                16.0, 84.0, 76.5, 6.5, 85.0, 6.0, 5, "Medium", "Yes",
                79.4, 3.45, "B+", "Low Risk", 92.1,
                json.dumps({"attendance": 8.0, "study_hours": 7.5, "past_grade": 7.8, "consistency": 8.2}),
                json.dumps([
                    "Solid foundation. Boosting weekly study by 3-4 hours can elevate you to an A grade.",
                    "Focus revision on mid-term weakness areas.",
                    "Optimize study technique with spaced repetition."
                ]),
                "2026-11-21 14:30:00"
            ),
            (
                "Rohan Verma", "STU-2024-103", "Male", "Information Technology",
                8.0, 68.0, 58.0, 5.0, 62.0, 14.0, 8, "Low", "Yes",
                54.2, 2.15, "D", "High Risk", 89.6,
                json.dumps({"attendance": 5.0, "study_hours": 4.5, "past_grade": 5.5, "consistency": 5.2}),
                json.dumps([
                    "High Academic Alert: Attendance (68%) is below the required 75% college threshold.",
                    "Urgent: Reduce non-academic extracurricular load from 14h to under 6h.",
                    "Increase structured revision to at least 15 hours per week.",
                    "Schedule one-on-one consultation with department academic advisor."
                ]),
                "2026-11-22 09:45:00"
            ),
            (
                "Ananya Iyer", "STU-2024-104", "Female", "Data Science",
                19.5, 89.0, 81.0, 7.0, 90.0, 5.0, 4, "High", "Yes",
                84.6, 3.68, "A", "Low Risk", 94.0,
                json.dumps({"attendance": 8.8, "study_hours": 8.5, "past_grade": 8.2, "consistency": 8.9}),
                json.dumps([
                    "Strong performance profile across all core indicators.",
                    "Leverage peer study groups to master advanced concepts.",
                    "Continue maintaining healthy work-life balance."
                ]),
                "2026-11-23 11:20:00"
            ),
            (
                "Kavita Rao", "STU-2024-105", "Female", "Mechanical Engineering",
                11.0, 72.5, 64.0, 6.0, 70.0, 8.0, 7, "Medium", "Yes",
                63.5, 2.70, "C", "Moderate Risk", 90.5,
                json.dumps({"attendance": 6.8, "study_hours": 6.0, "past_grade": 6.4, "consistency": 6.7}),
                json.dumps([
                    "Moderate risk detected: Score is approaching lower boundary of safe progression.",
                    "Improve attendance above 80% to capture essential lecture insights.",
                    "Target assignment completion to reach 85%+.",
                    "Implement a weekly self-test routine."
                ]),
                "2026-11-23 16:50:00"
            )
        ]
        
        cursor.executemany('''
            INSERT INTO predictions (
                student_name, student_id, gender, department,
                study_hours_per_week, attendance_percentage, previous_grade,
                sleep_hours, assignments_completed_pct, extracurricular_hours,
                stress_level, parental_involvement, internet_access,
                predicted_score, predicted_gpa, predicted_grade_letter,
                risk_level, confidence_score, factor_breakdown,
                recommendations, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_records)
    
    conn.commit()
    conn.close()

def save_prediction(data):
    """Save a student prediction record and return its ID."""
    conn = get_db_connection()
    ensure_columns(conn)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (
            student_name, student_id, gender, department, current_semester,
            previous_grade, internal_marks, assignments_completed_pct, attendance_percentage, num_subjects,
            daily_study_hours, study_hours_per_week, social_media_hours, sleep_hours, study_sessions_per_week,
            extracurricular_hours, attends_coaching, academic_confidence, stress_level,
            parental_involvement, internet_access,
            predicted_score, performance_category, predicted_gpa, predicted_grade_letter,
            risk_level, confidence_score, analysis_summary, strengths, improvements, factor_breakdown, recommendations
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['student_name'],
        data['student_id'],
        data.get('gender', 'Not Specified'),
        data.get('department', 'General'),
        data.get('current_semester', 'Semester 5'),
        float(data['previous_grade']),
        float(data.get('internal_marks', 75.0)),
        float(data['assignments_completed_pct']),
        float(data['attendance_percentage']),
        int(data.get('num_subjects', 6)),
        float(data.get('daily_study_hours', 2.5)),
        float(data['study_hours_per_week']),
        float(data.get('social_media_hours', 2.0)),
        float(data['sleep_hours']),
        int(data.get('study_sessions_per_week', 5)),
        float(data.get('extracurricular_hours', 4)),
        data.get('attends_coaching', 'No'),
        data.get('academic_confidence', 'Moderate'),
        int(data.get('stress_level', 5)),
        data.get('parental_involvement', 'Medium'),
        data.get('internet_access', 'Yes'),
        float(data['predicted_score']),
        data.get('performance_category', 'Good'),
        float(data['predicted_gpa']),
        data['predicted_grade_letter'],
        data['risk_level'],
        float(data['confidence_score']),
        data.get('analysis_summary', ''),
        json.dumps(data.get('strengths', [])),
        json.dumps(data.get('improvements', [])),
        json.dumps(data.get('factor_breakdown', {})),
        json.dumps(data.get('recommendations', []))
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_prediction_by_id(pred_id):
    """Retrieve a single prediction by ID."""
    conn = get_db_connection()
    ensure_columns(conn)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predictions WHERE id = ?', (pred_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        record = dict(row)
        try:
            record['factor_breakdown'] = json.loads(record['factor_breakdown']) if record.get('factor_breakdown') else {}
        except Exception:
            record['factor_breakdown'] = {}
        try:
            record['recommendations'] = json.loads(record['recommendations']) if record.get('recommendations') else []
        except Exception:
            record['recommendations'] = []
        try:
            record['strengths'] = json.loads(record['strengths']) if record.get('strengths') else []
        except Exception:
            record['strengths'] = []
        try:
            record['improvements'] = json.loads(record['improvements']) if record.get('improvements') else []
        except Exception:
            record['improvements'] = []
            
        # Ensure performance_category is populated
        if not record.get('performance_category'):
            score = float(record.get('predicted_score', 75.0))
            if score >= 85.0:
                record['performance_category'] = 'Excellent'
            elif score >= 70.0:
                record['performance_category'] = 'Good'
            elif score >= 55.0:
                record['performance_category'] = 'Average'
            else:
                record['performance_category'] = 'Needs Improvement'
                
        return record
    return None

def get_all_predictions():
    """Retrieve all predictions ordered by newest first."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predictions ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        d = dict(r)
        try:
            d['recommendations'] = json.loads(d['recommendations']) if d['recommendations'] else []
        except Exception:
            d['recommendations'] = []
        results.append(d)
    return results

def get_dashboard_metrics():
    """Calculate aggregated analytics across all stored predictions."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM predictions')
    total = cursor.fetchone()[0]
    
    if total == 0:
        conn.close()
        return {
            "total": 0, "avg_score": 0, "avg_gpa": 0,
            "low_risk": 0, "moderate_risk": 0, "high_risk": 0,
            "grade_distribution": {"A+": 0, "A": 0, "B+": 0, "B": 0, "C": 0, "D": 0, "F": 0},
            "avg_study_hours": 0, "avg_attendance": 0
        }
    
    cursor.execute('SELECT AVG(predicted_score), AVG(predicted_gpa), AVG(study_hours_per_week), AVG(attendance_percentage) FROM predictions')
    avg_score, avg_gpa, avg_study, avg_att = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE risk_level = 'Low Risk'")
    low_risk = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE risk_level = 'Moderate Risk'")
    moderate_risk = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE risk_level = 'High Risk'")
    high_risk = cursor.fetchone()[0]
    
    cursor.execute("SELECT predicted_grade_letter, COUNT(*) FROM predictions GROUP BY predicted_grade_letter")
    grades = dict(cursor.fetchall())
    grade_distribution = {
        "A+": grades.get("A+", 0),
        "A": grades.get("A", 0),
        "B+": grades.get("B+", 0),
        "B": grades.get("B", 0),
        "C": grades.get("C", 0),
        "D": grades.get("D", 0),
        "F": grades.get("F", 0)
    }
    
    conn.close()
    return {
        "total": total,
        "avg_score": round(avg_score or 0, 1),
        "avg_gpa": round(avg_gpa or 0, 2),
        "low_risk": low_risk,
        "moderate_risk": moderate_risk,
        "high_risk": high_risk,
        "grade_distribution": grade_distribution,
        "avg_study_hours": round(avg_study or 0, 1),
        "avg_attendance": round(avg_att or 0, 1)
    }

def delete_prediction(pred_id):
    """Delete a prediction record by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM predictions WHERE id = ?', (pred_id,))
    conn.commit()
    conn.close()
    return True

def has_user_predictions():
    """Check if any actual user-submitted prediction exists (is_sample = 0)."""
    conn = get_db_connection()
    ensure_columns(conn)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM predictions WHERE is_sample = 0')
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def get_latest_prediction():
    """
    Get the most relevant student prediction:
    Prefers the latest user-submitted prediction (is_sample = 0).
    Falls back to latest sample prediction if no user predictions exist yet.
    """
    conn = get_db_connection()
    ensure_columns(conn)
    cursor = conn.cursor()
    
    # Try getting latest user prediction first
    cursor.execute('SELECT id FROM predictions WHERE is_sample = 0 ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    if not row:
        cursor.execute('SELECT id FROM predictions ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        
    conn.close()
    if row:
        return get_prediction_by_id(row['id'])
    return None

def get_subject_breakdown_for_student(student_record):
    """
    Generates realistic subject-wise performance marks based on the student's 
    overall predicted score and academic department.
    """
    if not student_record:
        return {}
        
    base = float(student_record.get('predicted_score', 75.0))
    dept = student_record.get('department', 'Computer Science & AI')
    
    if 'Computer' in dept or 'AI' in dept or 'Data' in dept or 'Information' in dept:
        subjects = [
            ("Machine Learning & AI", round(min(99.0, max(35.0, base + 2.5)), 1)),
            ("Data Structures & Algorithms", round(min(99.0, max(35.0, base - 1.5)), 1)),
            ("Database Systems (SQL)", round(min(99.0, max(35.0, base + 3.0)), 1)),
            ("Computer Networks", round(min(99.0, max(35.0, base - 2.0)), 1)),
            ("Discrete Math & Stats", round(min(99.0, max(35.0, base - 3.5)), 1)),
            ("Software Engineering", round(min(99.0, max(35.0, base + 4.0)), 1))
        ]
    elif 'Electronics' in dept:
        subjects = [
            ("Digital Signal Processing", round(min(99.0, max(35.0, base - 2.0)), 1)),
            ("VLSI Design", round(min(99.0, max(35.0, base + 1.5)), 1)),
            ("Microprocessors & Embedded", round(min(99.0, max(35.0, base + 2.0)), 1)),
            ("Signals and Systems", round(min(99.0, max(35.0, base - 3.0)), 1)),
            ("Analog Circuits", round(min(99.0, max(35.0, base + 0.5)), 1)),
            ("Engineering Mathematics", round(min(99.0, max(35.0, base - 1.5)), 1))
        ]
    elif 'Mechanical' in dept:
        subjects = [
            ("Thermodynamics", round(min(99.0, max(35.0, base - 2.5)), 1)),
            ("Fluid Mechanics", round(min(99.0, max(35.0, base - 1.0)), 1)),
            ("Strength of Materials", round(min(99.0, max(35.0, base + 2.0)), 1)),
            ("Manufacturing Processes", round(min(99.0, max(35.0, base + 3.5)), 1)),
            ("Machine Design", round(min(99.0, max(35.0, base + 0.5)), 1)),
            ("Applied Dynamics", round(min(99.0, max(35.0, base - 1.5)), 1))
        ]
    else:
        subjects = [
            ("Core Theory I", round(min(99.0, max(35.0, base + 1.0)), 1)),
            ("Applied Analytics", round(min(99.0, max(35.0, base - 1.5)), 1)),
            ("Practical Lab & Project", round(min(99.0, max(35.0, base + 4.5)), 1)),
            ("Quantitative Reasoning", round(min(99.0, max(35.0, base - 3.0)), 1)),
            ("Specialization Elective", round(min(99.0, max(35.0, base + 2.0)), 1)),
            ("Professional Communications", round(min(99.0, max(35.0, base + 3.0)), 1))
        ]
    return dict(subjects)
