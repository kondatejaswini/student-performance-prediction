# Student Performance Prediction and Early Risk Identification Using Machine Learning

> **Subtitle:** An AI-powered academic analytics platform for predicting final marks, overall performance, and identifying students requiring early academic support.

---

## 📌 1. Project Overview
The **Student Performance Prediction and Early Risk Identification System** is an end-to-end data analytics and machine learning solution built for higher technical education (B.Tech Computer Science and Data Science). It empowers faculty advisors and department heads to monitor student academic progress, predict end-of-semester examination outcomes, evaluate multi-factor academic risk profiles, and deliver timely academic support.

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
The project includes a synthetic dataset of **1,200 B.Tech engineering student records** generated with realistic statistical dependencies.

| Feature Column | Description | Valid Range |
| :--- | :--- | :--- |
| `Student_ID` | Unique Student Identifier | `STU1001` - `STU2200` |
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
- **Linear Regression**
- **Decision Tree Regressor**
- **Random Forest Regressor** (Default Best Model)
- **KNN Regressor**

Evaluation Metrics: MAE, RMSE, $R^2$ Score. Saved to `models/final_marks_model.pkl`.

### 10. Overall Performance Prediction (Classification)
- **Logistic Regression**
- **Decision Tree Classifier**
- **Random Forest Classifier** (Default Best Model)
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
- **Page 1 (app.py):** Home Overview, Workflow Diagram, Tech Stack & Disclaimers.
- **Page 2 (1_Dashboard.py):** Analytics Dashboard with KPI Cards, Dynamic Filters, Plotly Visualizations, and Auto Insights.
- **Page 3 (2_Predict_Performance.py):** Live Student Prediction Form, Marks & Grade Output, Risk Score, and Personal Recommendations.
- **Page 4 (3_Model_Performance.py):** Viva/Demo Model Comparison, Actual vs Predicted Plots, Error Histograms, Confusion Matrix Heatmap, and Feature Importances.
- **Page 5 (4_Student_Records.py):** Searchable Student Datatable, Prediction History Logs, and CSV Export.
- **Page 6 (5_Data_Quality.py):** Data Hygiene Audit Report & Summary Statistics.
- **Page 7 (6_About.py):** Project Background, Methodology, Limitations, and Roadmap.

---

## 🛠️ 13. Technology Stack
- **Language:** Python 3.10+
- **Frontend / Web UI:** Streamlit, Custom HTML/CSS
- **Data Processing:** Pandas, NumPy
- **Visualizations:** Plotly Express, Plotly Graph Objects, Seaborn, Matplotlib
- **Machine Learning:** Scikit-Learn, Joblib
- **Database:** SQLite (`student_performance.db`)

---

## 🏗️ 14. Project Architecture & 15. Folder Structure

```
student-performance-prediction/
│
├── data/
│   ├── student_performance.csv
│   ├── processed_data.csv
│   └── student_performance_powerbi.csv
│
├── models/
│   ├── final_marks_model.pkl
│   ├── overall_performance_model.pkl
│   └── model_metadata.pkl
│
├── src/
│   ├── __init__.py
│   ├── data_generation.py
│   ├── data_cleaning.py
│   ├── eda.py
│   ├── train_regression.py
│   ├── train_classification.py
│   ├── prediction.py
│   ├── risk_analysis.py
│   ├── database.py
│   └── utils.py
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Predict_Performance.py
│   ├── 3_Model_Performance.py
│   ├── 4_Student_Records.py
│   ├── 5_Data_Quality.py
│   └── 6_About.py
│
├── .streamlit/
│   └── config.toml
│
├── notebooks/
│   └── student_analysis.ipynb
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── student_performance.db
```

---

## 💻 16. Installation & 17. Running the Project

### Prerequisites
Python 3.10+ installed.

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/your-username/student-performance-prediction.git
cd student-performance-prediction

# Create Virtual Environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Full Pipeline & Start Application
```bash
# 1. Generate & clean synthetic dataset
python src/data_generation.py
python src/data_cleaning.py

# 2. Train regression and classification models
python src/train_regression.py
python src/train_classification.py

# 3. Initialize Database
python src/database.py

# 4. Launch Streamlit Application
streamlit run app.py
```
App will open automatically at `http://localhost:8501`.

---

## 📊 18. Power BI Integration
To import data into Power BI:
1. Open Power BI Desktop $\rightarrow$ Click **Get Data** $\rightarrow$ **Text/CSV**.
2. Select `data/student_performance_powerbi.csv`.
3. Use pre-calculated columns `Attendance_Band`, `Study_Hours_Band`, and `Risk_Category` for slicers.

---

## ☁️ 23. Deployment Readiness (Streamlit Cloud)
1. Push repository to GitHub.
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect repository and select `app.py` as entrypoint.

---

## 👤 24. Author & License
- **Author:** Computer Science & Data Science Final Year Project
- **License:** MIT License
