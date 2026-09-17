# Student Performance Prediction and Early Risk Identification Using Machine Learning

> **Subtitle:** An AI-powered academic analytics platform for predicting final marks, overall performance, and identifying students requiring early academic support.

---

## 📌 1. Project Overview
The **Student Performance Prediction and Early Risk Identification System** (**StudentIQ**) is an end-to-end data analytics and machine learning solution built for higher technical education (B.Tech Computer Science and Data Science). It empowers faculty advisors and department heads to monitor student academic progress, predict end-of-semester examination outcomes, evaluate multi-factor academic risk profiles, and deliver timely academic support.

---

## 🎯 2. Problem Statement
In higher engineering education, retroactive evaluation (grading at the end of a semester) often leaves insufficient time to assist struggling students. Students carrying pending backlogs, low internal test marks, or declining class attendance frequently fall into academic risk undetected.

This project addresses this problem by leveraging machine learning algorithms (Regression and Multi-Class Classification) alongside a transparent rule-based risk evaluation engine to deliver predictive insight and actionable recommendations prior to final semester examinations.

---

## 🏆 3. Objectives
- **Predict Final Marks:** Train and compare regression models to estimate continuous end-term examination scores (0–100).
- **Classify Overall Performance:** Train separate classification models to categorize students into academic bands (`Excellent`, `Good`, `Average`, `At Risk`).
- **Early Risk Detection:** Compute transparent rule-based academic risk indicators (`LOW RISK`, `MEDIUM RISK`, `HIGH RISK`).
- **Interactive Analytics Dashboard:** Deliver dynamic Plotly visualizations filtered across Department, Year, Semester, Gender, and Risk levels.
- **Actionable Student Guidance:** Automatically generate personalized academic recommendations based on student performance input attributes.
- **Persistence & BI Readiness:** Log prediction logs in SQLite and provide Power BI optimized export datasets.

---

## ⭐ 4. Key Features
- **Dual ML Engine:** Simultaneous regression for marks and classification for performance bands.
- **Dynamic Streamlit SaaS Dashboard:** KPI metric cards, Plotly distribution plots, correlation heatmaps, and automated cohort insights.
- **Interactive Live Prediction:** Form input with instant mark estimation, grade classification, risk indicator score, and customized recommendations.
- **Model Comparison View (Viva Mode):** Complete metrics tables ($R^2$, MAE, RMSE, Accuracy, Precision, Recall, F1-Score), actual vs predicted scatter plots, error histograms, and confusion matrices.
- **Data Quality & Audit Module:** Automated schema validation, out-of-bound checks, and duplicate detection reporting.
- **Student Records Datatable:** Searchable, filterable student records table with CSV export.
- **Power BI Compatibility:** Ready-to-use exported CSV (`student_performance_powerbi.csv`) with calculated attendance and study bands for enterprise BI tools.

---

## 📊 5. Dataset
The project includes a synthetic dataset of **500 B.Tech engineering student records** generated with realistic statistical dependencies.

| Feature Column | Description | Valid Range |
| :--- | :--- | :--- |
| `Student_ID` | Unique Student Identifier | `STU1001` - `STU1500` |
| `Student_Name` | Full Name | String |
| `Department` | Engineering Specialization | CSE, Data Science, AI & ML, IT |
| `Year` / `Semester` | Academic Year (1-4) & Semester (1-8) | Integer |
| `Attendance` | Class Attendance Percentage | 0% – 100% |
| `Study_Hours` | Self-Study Hours per Day | 0 – 12 hrs/day |
| `Assignment_Score` | Average Assignment Assessment | 0 – 100 |
| `Internal_Marks` | Mid-Term Examination Score | 0 – 100 |
| `Previous_Semester_Marks` | Cumulative Past Semester Score | 0 – 100 |
| `Assignment_Completion` | Percentage of Completed Assignments | 0% – 100% |
| `Class_Participation` | Classroom & Lab Engagement Score | 0% – 100% |
| `Backlogs` | Uncleared Pending Backlog Papers | 0 – 5 |
| `Sleep_Hours` | Daily Sleep Duration | 3 – 10 hrs/day |
| `Final_Marks` | End-Semester Exam Score (Target 1) | 0 – 100 |
| `Overall_Performance` | Performance Category (Target 2) | Excellent, Good, Average, At Risk |

---

## 🧹 6. Data Processing & Quality Pipeline
- Out-of-bounds validation checks on attendance ($0-100\%$), marks ($0-100$), and study/sleep hours.
- Missing values handled via median imputation for numerical features and mode for categoricals.
- Duplicate record filtering on `Student_ID`.
- Export of `processed_data.csv` and `student_performance_powerbi.csv`.

---

## 📈 7. Exploratory Data Analysis (EDA)
The system includes 15 interactive Plotly visualizations:
1. Overall Performance Distribution (Pie Chart)
2. Attendance vs Final Marks (Scatter Plot + Trendline)
3. Study Hours vs Final Marks
4. Assignment Score vs Final Marks
5. Internal Marks vs Final Marks
6. Previous Semester Marks vs Final Marks
7. Assignment Completion vs Final Marks
8. Class Participation vs Final Marks
9. Backlogs vs Final Marks
10. Sleep Hours vs Final Marks
11. Department-wise Performance (Grouped Bar Chart)
12. Year-wise Performance
13. Semester-wise Performance
14. Gender-wise Performance
15. Feature Correlation Heatmap

---

## 🤖 8. Machine Learning Models
All models are evaluated on an 80/20 train/test split with `random_state=42` using Scikit-Learn `Pipeline` abstractions.

### 9. Final Marks Prediction (Regression)
- **Linear Regression** ($R^2 = 0.9062$, $MAE = 3.64$) — Best Selected Model
- **Decision Tree Regressor**
- **Random Forest Regressor**
- **KNN Regressor**

Evaluation Metrics: MAE, RMSE, $R^2$ Score. Saved to `models/final_marks_model.pkl`.

### 10. Overall Performance Prediction (Classification)
- **Logistic Regression** ($F1 = 0.7439$, $Acc = 75.0\%$) — Best Selected Model
- **Decision Tree Classifier**
- **Random Forest Classifier**
- **KNN Classifier**

Evaluation Metrics: Accuracy, Precision, Recall, F1-Score, Confusion Matrix. Saved to `models/overall_performance_model.pkl`.

*Note: Target leakage is prevented by excluding `Final_Marks` from classification input features.*

---

## ⚠️ 11. Student Risk Identification Layer
Transparent rule engine evaluating multi-indicator thresholds:
- **HIGH RISK (Red):** Critical backlogs ($\ge 3$), attendance $< 60\%$, internal marks $< 50$, or predicted 'At Risk' status.
- **MEDIUM RISK (Amber):** Borderline attendance ($60-75\%$), pending backlogs ($1-2$), or low daily study hours.
- **LOW RISK (Green):** Strong attendance, clean backlogs, and solid internal test performance.

*Academic Disclaimer: This indicator is an academic-support tool and not a medical or psychological diagnosis.*

---

## 🖥️ 12. Dashboard UI & Pages
- **Overview (app.py):** Home Overview, 4 Core KPI cards, Performance Breakdown, Early Risk Summary.
- **Page 1 (1_Analytics.py):** Analytics Dashboard organized into 4 dimensions (Academic Performance, Academic Drivers, Student Behavior, Data Relationships).
- **Page 2 (2_Prediction.py):** Single Student ID Auto-Fill Lookup & Bulk CSV Upload Batch Prediction.
- **Page 3 (3_Risk_Insights.py):** Risk Score Hero Banner, Risk Drivers Checklist, and Numbered Recommendations.
- **Page 4 (4_Students.py):** Searchable Datatable, Prediction Logs, and CSV Export.
- **Page 5 (5_Model_Performance.py):** Viva/Demo Model Comparison, Actual vs Predicted Plots, Error Histograms, Confusion Matrix Heatmap, and Feature Importances.
- **Page 6 (6_About.py):** Project Vision, Problem Statement, Academic Disclaimer, and Architecture.

---

## 🛠️ 13. Technology Stack
- **Language:** Python 3.10+
- **Frontend / Web UI:** Streamlit, Custom HTML/CSS System
- **Data Processing:** Pandas, NumPy
- **Visualizations:** Plotly Express, Plotly Graph Objects, Seaborn, Matplotlib
- **Machine Learning:** Scikit-Learn, Joblib
- **Database:** SQLite (`student_performance.db`)

---

## 🏗️ 14. Project Architecture & 15. Folder Structure
## 💻 16. Installation & 17. Running the Project
### Prerequisites
Python 3.10+ installed.
### Step 1: Clone Repository
```bash
git clone https://github.com/kondatejaswini/student-performance-prediction.git
cd student-performance-prediction
Step 2: Install Dependencies
pip install -r requirements.txt
Step 3: Run Application
streamlit run app.py
📊 18. Power BI Integration
To import data into Power BI:

Open Power BI Desktop 
→
→ Click Get Data 
→
→ Text/CSV.
Select data/student_performance_powerbi.csv.
Use pre-calculated columns Attendance_Band, Study_Hours_Band, and Risk_Category for slicers.
☁️ 23. Streamlit Cloud Deployment
Push repository to GitHub (kondatejaswini/student-performance-prediction).
Log into Streamlit Community Cloud.
Connect repository and select app.py (or student performance/app.py) as main file path.
         
