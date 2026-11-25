# AI-Based Academic Performance Prediction System

A modern, professional, and fully functional web application developed with **HTML, CSS, JavaScript, Python Flask, and SQLite** for college capstone presentations and academic performance analytics.

---

## 🌟 Key Features

1. **Intelligent Predictive Engine (`models/predictor.py`)**:
   - Synthesizes 8+ multidimensional academic and lifestyle indicators:
     - Prior Semester Percentage / CGPA
     - Lecture Attendance Percentage (critical 75% threshold monitoring)
     - Weekly Dedicated Self-Study Hours
     - Coursework / Assignment Completion Rate
     - Sleep Duration & Circadian Recovery
     - Academic Stress Index (1–10 scale)
     - Extracurricular Load
     - Parental / Mentorship Support
     - Internet & Educational Resource Access
   - Outputs:
     - **Predicted Final Percentage** (e.g., `87.4%`)
     - **Semester GPA** on a 4.0 scale (e.g., `3.82`)
     - **Letter Grade** (`A+`, `A`, `B+`, `B`, `C`, `D`, `F`)
     - **Early Risk Assessment Level** (`Low Risk`, `Moderate Risk`, `High Risk`)
     - **Model Confidence Score** (e.g., `94.8%`)
     - **Personalized Algorithmic Prescriptions** (actionable advice to elevate grades)

2. **Five Comprehensive Pages**:
   - 🏠 **Home Page (`/`)**: Hero banner, live inference preview, 3-step workflow, capability cards, and summary stats.
   - 🪄 **Student Prediction Form (`/predict`)**: Categorized form with real-time slider badges, auto-fill presets (*Top Performer*, *Average Student*, *At-Risk*), and validation.
   - 📊 **Prediction Results Page (`/result/<id>`)**: Comprehensive student scorecards, risk badges, **Radar Chart** (benchmark vs 90%+ cohort), **Factor Impact Bar Chart**, tailored AI recommendations, and an **Interactive What-If Scenario Simulator**.
   - 📈 **Student Dashboard (`/dashboard`)**: KPI overview cards, **Grade Distribution Doughnut Chart**, **Risk Breakdown Bar Chart**, real-time search, risk filter, and historical SQLite records.
   - ℹ️ **About the Project (`/about`)**: Educational data science methodology, mathematical feature weightings, ethical AI principles, and tech stack overview.

3. **Design & Theme**:
   - Academic analytics palette: **Navy Blue** (`#0f172a`), **Crisp White** (`#ffffff`), **Light Blue** (`#38bdf8`), and **Subtle Purple** (`#6366f1`).
   - Card-based responsive layout with smooth transitions, hover effects, and mobile-friendly navigation.

---

## 📁 Project Structure

```
academic-performance-prediction/
│
├── app.py                      # Flask backend, routing, session, REST endpoints
├── database.py                 # SQLite schema initialization and CRUD helper methods
├── academic_records.db         # SQLite database file (auto-generated on first run)
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows one-click start script
├── README.md                   # Complete documentation
│
├── models/
│   └── predictor.py            # Academic performance prediction & recommendation algorithms
│
├── static/
│   ├── css/
│   │   └── style.css           # Master stylesheet (Navy/Blue/Purple dashboard theme)
│   └── js/
│       ├── main.js             # Mobile navigation, toast alerts, global utilities
│       ├── form.js             # Range sliders, preset profiles, submit animations
│       └── dashboard.js        # Chart.js radar, bar, doughnut charts & table search/filters
│
└── templates/
    ├── base.html               # Shared master layout, navbar, footer, CDNs
    ├── index.html              # 1. Home page
    ├── predict.html            # 2. Student prediction form
    ├── result.html             # 3. Prediction results & What-If simulator
    ├── dashboard.html          # 4. Student dashboard & cohort analytics
    └── about.html              # 5. About the project & methodology
```

---

## 🚀 How to Run the Website

### Option 1: One-Click Startup (Windows)
Double-click `run.bat` inside this folder. It will launch the Flask application and display the local server address.

### Option 2: Standard Terminal / Command Prompt
1. Open terminal inside the project directory:
   ```bash
   cd C:\Users\Sanvi\.gemini\antigravity\scratch\academic-performance-prediction
   ```
2. Install dependencies (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🧪 REST API Endpoints
- `POST /api/predict` — Pass raw JSON parameters to receive immediate JSON prediction metrics.
- `GET /api/stats` — Retrieve aggregated dashboard stats and grade distributions.
