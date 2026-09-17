"""
Student Risk Analysis Module for Student Performance Prediction System.
Provides transparent rule-based academic risk evaluation and personalized risk driver summaries.
"""

def evaluate_academic_risk(student_data: dict) -> dict:
    """
    Evaluates academic risk based on multi-indicator academic threshold rules.
    
    Parameters:
        student_data: dict containing keys like Attendance, Internal_Marks, Backlogs,
                      Study_Hours, Assignment_Completion, predicted_marks, predicted_performance.
                      
    Returns:
        dict containing risk_level, risk_score, risk_color, drivers, and recommendations.
    """
    attendance = float(student_data.get("Attendance", 75))
    internal = float(student_data.get("Internal_Marks", 70))
    backlogs = int(student_data.get("Backlogs", 0))
    study_hours = float(student_data.get("Study_Hours", 4))
    completion = float(student_data.get("Assignment_Completion", 75))
    pred_marks = float(student_data.get("predicted_marks", 70))
    pred_perf = str(student_data.get("predicted_performance", "Good"))
    
    risk_points = 0
    risk_reasons = []

    # Rule 1: Backlogs
    if backlogs >= 3:
        risk_points += 35
        risk_reasons.append(f"Critical backlogs count ({backlogs} backlogs pending)")
    elif backlogs >= 1:
        risk_points += 18
        risk_reasons.append(f"Pending backlogs present ({backlogs} backlog(s))")

    # Rule 2: Attendance
    if attendance < 60:
        risk_points += 30
        risk_reasons.append(f"Critically low attendance ({attendance:.1f}%)")
    elif attendance < 75:
        risk_points += 15
        risk_reasons.append(f"Borderline attendance below target 75% ({attendance:.1f}%)")

    # Rule 3: Internal Assessment
    if internal < 50:
        risk_points += 25
        risk_reasons.append(f"Low internal marks ({internal:.1f}/100)")
    elif internal < 65:
        risk_points += 10
        risk_reasons.append(f"Moderate internal marks ({internal:.1f}/100)")

    # Rule 4: Predicted Performance
    if pred_perf == "At Risk" or pred_marks < 50:
        risk_points += 30
        risk_reasons.append(f"Model predicts 'At Risk' status (Predicted Final: {pred_marks:.1f}/100)")
    elif pred_perf == "Average" or pred_marks < 70:
        risk_points += 12
        risk_reasons.append(f"Model predicts average performance range ({pred_marks:.1f}/100)")

    # Rule 5: Study Hours & Assignment Completion
    if study_hours < 2.0:
        risk_points += 12
        risk_reasons.append(f"Insufficient daily study hours ({study_hours:.1f} hrs/day)")
        
    if completion < 60:
        risk_points += 10
        risk_reasons.append(f"Low assignment completion rate ({completion:.1f}%)")

    # Determine overall Risk Level
    if risk_points >= 40:
        risk_level = "HIGH RISK"
        risk_color = "#EF4444" # Red
        summary = "Student requires immediate academic counseling, attendance monitoring, and backlog clearing strategy."
    elif risk_points >= 20:
        risk_level = "MEDIUM RISK"
        risk_color = "#F59E0B" # Amber
        summary = "Student shows moderate academic friction. Recommended to boost study hours and assignment completion."
    else:
        risk_level = "LOW RISK"
        risk_color = "#10B981" # Green
        summary = "Student displays healthy academic trajectory. Maintain current study patterns."

    if not risk_reasons:
        risk_reasons.append("Strong attendance, clear backlogs, and solid internal performance metrics.")

    return {
        "risk_level": risk_level,
        "risk_score": min(risk_points, 100),
        "risk_color": risk_color,
        "summary": summary,
        "drivers": risk_reasons,
        "disclaimer": "This academic risk score is an indicative academic-support tool and not a psychological or medical assessment."
    }
