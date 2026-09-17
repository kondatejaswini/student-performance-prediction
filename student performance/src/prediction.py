"""
Prediction & Inference Module for Student Performance Prediction System.
Loads saved models, computes final marks & overall performance, evaluates risk,
and generates actionable student recommendations (both single and batch CSV mode).
"""

import os
import joblib
import pandas as pd
from src.risk_analysis import evaluate_academic_risk

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
REGRESSION_MODEL_PATH = os.path.join(MODELS_DIR, "final_marks_model.pkl")
CLASSIFICATION_MODEL_PATH = os.path.join(MODELS_DIR, "overall_performance_model.pkl")

_reg_model = None
_clf_model = None

def load_models():
    """Loads stored regression and classification models."""
    global _reg_model, _clf_model
    if _reg_model is None and os.path.exists(REGRESSION_MODEL_PATH):
        _reg_model = joblib.load(REGRESSION_MODEL_PATH)
    if _clf_model is None and os.path.exists(CLASSIFICATION_MODEL_PATH):
        _clf_model = joblib.load(CLASSIFICATION_MODEL_PATH)
    return _reg_model, _clf_model

def generate_academic_suggestions(input_data: dict) -> list[str]:
    """Generates personalized academic guidance based on student inputs."""
    suggestions = []
    
    attendance = float(input_data.get("Attendance", 0))
    study_hours = float(input_data.get("Study_Hours", 0))
    assignment_comp = float(input_data.get("Assignment_Completion", 0))
    internal = float(input_data.get("Internal_Marks", 0))
    backlogs = int(input_data.get("Backlogs", 0))
    sleep = float(input_data.get("Sleep_Hours", 7))
    participation = float(input_data.get("Class_Participation", 0))

    if attendance < 75.0:
        suggestions.append(f"🎯 **Improve Class Attendance**: Current attendance ({attendance:.1f}%) is below the recommended 75% target threshold.")
    if study_hours < 4.0:
        suggestions.append(f"⏱️ **Increase Self-Study Hours**: Dedicated self-study ({study_hours:.1f} hrs/day) should be increased to at least 4-5 hours daily.")
    if internal < 65.0:
        suggestions.append(f"📝 **Focus on Internal Assessments**: Mid-term marks ({internal:.1f}/100) are a critical predictor of final term outcomes.")
    if assignment_comp < 80.0:
        suggestions.append(f"📋 **Complete Pending Assignments**: Completion rate ({assignment_comp:.1f}%) requires immediate submission of outstanding coursework.")
    if backlogs > 0:
        suggestions.append(f"⚠️ **Backlog Remediation**: prioritize clearing {backlogs} pending backlog paper(s) during upcoming re-examinations.")
    if participation < 60.0:
        suggestions.append(f"🗣️ **Active Class Participation**: Engage in lab demonstrations and interactive lectures to reinforce conceptual understanding.")
    if sleep < 6.0:
        suggestions.append(f"🛌 **Optimize Rest & Sleep Schedule**: Sleeping {sleep:.1f} hours/day is suboptimal; aim for 7-8 hours for cognitive recovery.")

    if not suggestions:
        suggestions.append("🌟 **Maintain Excellent Trajectory**: Current academic metrics are strong! Continue consistent daily study and revision habits.")

    return suggestions

def predict_student_performance(input_data: dict) -> dict:
    """
    Computes regression prediction, classification prediction, risk evaluation, and suggestions for a single student.
    """
    reg_model, clf_model = load_models()
    
    if reg_model is None or clf_model is None:
        return {
            "error": "Trained machine learning models are missing. Please train models first."
        }
        
    df_input = pd.DataFrame([input_data])
    
    # Predict Final Marks
    predicted_marks = float(reg_model.predict(df_input)[0])
    predicted_marks = max(0.0, min(100.0, round(predicted_marks, 1)))
    
    # Predict Overall Performance Category
    predicted_performance = str(clf_model.predict(df_input)[0])
    
    # Combine data for risk assessment
    combined_data = input_data.copy()
    combined_data["predicted_marks"] = predicted_marks
    combined_data["predicted_performance"] = predicted_performance
    
    risk_info = evaluate_academic_risk(combined_data)
    suggestions = generate_academic_suggestions(input_data)
    
    reg_name = type(reg_model.named_steps["regressor"]).__name__
    clf_name = type(clf_model.named_steps["classifier"]).__name__

    return {
        "predicted_marks": predicted_marks,
        "predicted_performance": predicted_performance,
        "risk_level": risk_info["risk_level"],
        "risk_score": risk_info["risk_score"],
        "risk_color": risk_info["risk_color"],
        "risk_summary": risk_info["summary"],
        "risk_drivers": risk_info["drivers"],
        "suggestions": suggestions,
        "regression_model": reg_name,
        "classification_model": clf_name
    }

def predict_batch_students(df: pd.DataFrame) -> pd.DataFrame:
    """
    Accepts a DataFrame of student records, predicts Final_Marks, Overall_Performance,
    Risk_Level, Risk_Score, and Actionable Suggestions for every student in batch mode.
    Returns the enriched DataFrame with prediction columns.
    """
    reg_model, clf_model = load_models()
    if reg_model is None or clf_model is None:
        raise ValueError("Trained machine learning models are missing. Please train models first.")
        
    out_df = df.copy()
    
    # Required features expected by models
    req_cols = [
        "Attendance", "Study_Hours", "Assignment_Score", "Internal_Marks",
        "Previous_Semester_Marks", "Assignment_Completion", "Class_Participation",
        "Backlogs", "Sleep_Hours", "Gender", "Department", "Year", "Semester"
    ]
    
    for c in req_cols:
        if c not in out_df.columns:
            raise ValueError(f"Missing required column in uploaded dataset: '{c}'")
            
    # Predict Final Marks
    pred_marks = reg_model.predict(out_df[req_cols])
    out_df["Predicted_Final_Marks"] = [max(0.0, min(100.0, round(float(m), 1))) for m in pred_marks]
    
    # Predict Overall Performance
    pred_perf = clf_model.predict(out_df[req_cols])
    out_df["Predicted_Overall_Performance"] = pred_perf
    
    # Evaluate Risk Level & Risk Score & Top Suggestion
    risk_levels = []
    risk_scores = []
    recommendations = []
    
    for idx, row in out_df.iterrows():
        input_data = row.to_dict()
        input_data["predicted_marks"] = row["Predicted_Final_Marks"]
        input_data["predicted_performance"] = row["Predicted_Overall_Performance"]
        
        risk_info = evaluate_academic_risk(input_data)
        sugs = generate_academic_suggestions(input_data)
        
        risk_levels.append(risk_info["risk_level"])
        risk_scores.append(risk_info["risk_score"])
        clean_sug = " | ".join([
            s.replace("**", "").replace("🎯 ", "").replace("⏱️ ", "").replace("📝 ", "").replace("📋 ", "").replace("⚠️ ", "").replace("🗣️ ", "").replace("🛌 ", "").replace("🌟 ", "") 
            for s in sugs[:2]
        ])
        recommendations.append(clean_sug)
        
    out_df["Risk_Level"] = risk_levels
    out_df["Risk_Score"] = risk_scores
    out_df["Recommended_Actions"] = recommendations
    
    return out_df
