import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import database
from models.predictor import predict_academic_performance

app = Flask(__name__)
app.secret_key = 'academic-ai-prediction-super-secret-key-2026'

# Ensure database is initialized on startup
database.init_db()

@app.route('/')
def index():
    """Home page route with live summary metrics and feature highlights."""
    stats = database.get_dashboard_metrics()
    return render_template('index.html', stats=stats)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Prediction form and submission handler with strict input validation."""
    if request.method == 'POST':
        try:
            # 1. Personal & Academic Details
            student_name = request.form.get('student_name', '').strip()
            student_id = request.form.get('student_id', '').strip()
            current_semester = request.form.get('current_semester', 'Semester 5')
            department = request.form.get('department', 'Computer Science & AI')
            
            if not student_name:
                flash('Please enter the student full name.', 'error')
                return redirect(url_for('predict'))
            if not student_id:
                flash('Please enter the enrollment or student ID.', 'error')
                return redirect(url_for('predict'))

            # 2. Academic Information
            previous_grade = float(request.form.get('previous_grade', 75.0))
            internal_marks = float(request.form.get('internal_marks', 75.0))
            assignments = float(request.form.get('assignments_completed_pct', 80.0))
            attendance = float(request.form.get('attendance_percentage', 85.0))
            num_subjects = int(request.form.get('num_subjects', 6))

            # Validate impossible percentages
            if attendance < 0 or attendance > 100:
                flash('Invalid Attendance: Attendance percentage must be between 0% and 100%.', 'error')
                return redirect(url_for('predict'))
            if previous_grade < 0 or previous_grade > 100:
                flash('Invalid Previous Grade: Marks must be between 0% and 100%.', 'error')
                return redirect(url_for('predict'))
            if internal_marks < 0 or internal_marks > 100:
                flash('Invalid Internal Marks: Internal marks must be between 0% and 100%.', 'error')
                return redirect(url_for('predict'))
            if assignments < 0 or assignments > 100:
                flash('Invalid Assignment Rate: Assignment completion percentage must be between 0% and 100%.', 'error')
                return redirect(url_for('predict'))
            if num_subjects < 1 or num_subjects > 15:
                flash('Invalid Subjects Count: Number of subjects must be between 1 and 15.', 'error')
                return redirect(url_for('predict'))

            # 3. Study Habits
            daily_study = float(request.form.get('daily_study_hours', 2.5))
            study_hours = float(request.form.get('study_hours_per_week', 15.0))
            social_media = float(request.form.get('social_media_hours', 2.0))
            sleep_hours = float(request.form.get('sleep_hours', 7.0))
            study_sessions = int(request.form.get('study_sessions_per_week', 5))

            if daily_study < 0 or daily_study > 24:
                flash('Daily study hours must be between 0 and 24 hours.', 'error')
                return redirect(url_for('predict'))
            if study_hours < 0 or study_hours > 100:
                flash('Weekly study hours must be between 0 and 100 hours.', 'error')
                return redirect(url_for('predict'))
            if social_media < 0 or social_media > 24:
                flash('Social media hours must be between 0 and 24 hours.', 'error')
                return redirect(url_for('predict'))
            if sleep_hours < 1 or sleep_hours > 20:
                flash('Sleep hours must be between 1 and 20 hours.', 'error')
                return redirect(url_for('predict'))
            if study_sessions < 1 or study_sessions > 21:
                flash('Study sessions per week must be between 1 and 21.', 'error')
                return redirect(url_for('predict'))

            # 4. Additional Factors
            extracurricular = float(request.form.get('extracurricular_hours', 4.0))
            attends_coaching = request.form.get('attends_coaching', 'No')
            academic_confidence = request.form.get('academic_confidence', 'Moderate')
            stress_level = int(request.form.get('stress_level', 5))
            parental = request.form.get('parental_involvement', 'Medium')
            internet = request.form.get('internet_access', 'Yes')

            raw_input = {
                'student_name': student_name,
                'student_id': student_id,
                'current_semester': current_semester,
                'department': department,
                'previous_grade': previous_grade,
                'internal_marks': internal_marks,
                'assignments_completed_pct': assignments,
                'attendance_percentage': attendance,
                'num_subjects': num_subjects,
                'daily_study_hours': daily_study,
                'study_hours_per_week': study_hours,
                'social_media_hours': social_media,
                'sleep_hours': sleep_hours,
                'study_sessions_per_week': study_sessions,
                'extracurricular_hours': extracurricular,
                'attends_coaching': attends_coaching,
                'academic_confidence': academic_confidence,
                'stress_level': stress_level,
                'parental_involvement': parental,
                'internet_access': internet
            }

            # Run AI prediction model
            prediction_output = predict_academic_performance(raw_input)

            # Combine input and output data for persistence
            full_record = {**raw_input, **prediction_output}

            # Save in SQLite
            pred_id = database.save_prediction(full_record)

            flash('Performance forecast computed successfully!', 'success')
            return redirect(url_for('result', pred_id=pred_id))

        except ValueError as ve:
            flash(f'Numerical format error: Please ensure all numeric inputs are valid numbers. ({str(ve)})', 'error')
            return redirect(url_for('predict'))
        except Exception as e:
            flash(f'Error processing prediction: {str(e)}', 'error')
            return redirect(url_for('predict'))

    return render_template('predict.html')

@app.route('/result/<int:pred_id>')
def result(pred_id):
    """Detailed prediction results view with interactive charts and prescriptions."""
    record = database.get_prediction_by_id(pred_id)
    if not record:
        flash('Prediction record not found.', 'warning')
        return redirect(url_for('predict'))
    
    # Also fetch average metrics for benchmark comparison
    metrics = database.get_dashboard_metrics()
    return render_template('result.html', record=record, metrics=metrics)

@app.route('/dashboard')
def dashboard():
    """Comprehensive student academic analytics dashboard."""
    has_user_data = database.has_user_predictions()
    predictions = database.get_all_predictions()
    metrics = database.get_dashboard_metrics()
    
    selected_id = request.args.get('id')
    if selected_id:
        try:
            latest_student = database.get_prediction_by_id(int(selected_id))
        except (ValueError, TypeError):
            latest_student = database.get_latest_prediction()
    else:
        latest_student = database.get_latest_prediction()
        
    subject_scores = database.get_subject_breakdown_for_student(latest_student)
    
    return render_template(
        'dashboard.html',
        predictions=predictions,
        metrics=metrics,
        latest_student=latest_student,
        has_user_data=has_user_data,
        subject_scores=subject_scores
    )

@app.route('/about')
def about():
    """About the project page with AI methodology, feature weights, and project scope."""
    return render_template('about.html')

@app.route('/delete/<int:pred_id>', methods=['POST', 'GET'])
def delete_record(pred_id):
    """Delete a prediction record."""
    database.delete_prediction(pred_id)
    flash(f'Record #{pred_id} deleted successfully.', 'info')
    return redirect(url_for('dashboard'))

# REST API Endpoints for interactive/client-side integrations
@app.route('/api/predict', methods=['POST'])
def api_predict():
    """JSON API to compute prediction dynamically without page reload."""
    try:
        data = request.get_json(force=True)
        result = predict_academic_performance(data)
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """JSON API returning dashboard metrics and grade distributions."""
    metrics = database.get_dashboard_metrics()
    return jsonify(metrics)

if __name__ == '__main__':
    # Initialize DB and start server on port 5000
    print("=" * 60)
    print("  AI-Based Academic Performance Prediction System")
    print("  Starting Flask Server at http://127.0.0.1:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
