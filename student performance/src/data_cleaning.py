"""
Data Cleaning & Quality Pipeline Module for Student Performance Prediction System.
Handles validation, out-of-bound checks, missing values, duplicate detection, and Power BI export.
"""

import os
import pandas as pd
import numpy as np

def validate_and_clean_data(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    """
    Validates data bounds, cleans invalid rows, handles missing values,
    and returns (cleaned_df, quality_metrics, invalid_df).
    """
    df = raw_df.copy()
    initial_records = len(df)
    
    # Track statistics
    quality_report = {
        "total_records": initial_records,
        "total_columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_records": int(df.duplicated(subset=["Student_ID"]).sum()),
        "invalid_records": 0,
        "clean_records": 0
    }
    
    # Handle missing values if any
    if quality_report["missing_values"] > 0:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        categorical_cols = df.select_dtypes(include=["object"]).columns
        for c in categorical_cols:
            df[c] = df[c].fillna(df[c].mode()[0])
            
    # Drop duplicate Student IDs if present
    df = df.drop_duplicates(subset=["Student_ID"])
    
    # Validation rules
    valid_attendance = (df["Attendance"] >= 0) & (df["Attendance"] <= 100)
    valid_study = (df["Study_Hours"] >= 0) & (df["Study_Hours"] <= 16)
    valid_assignment = (df["Assignment_Score"] >= 0) & (df["Assignment_Score"] <= 100)
    valid_internal = (df["Internal_Marks"] >= 0) & (df["Internal_Marks"] <= 100)
    valid_prev = (df["Previous_Semester_Marks"] >= 0) & (df["Previous_Semester_Marks"] <= 100)
    valid_completion = (df["Assignment_Completion"] >= 0) & (df["Assignment_Completion"] <= 100)
    valid_participation = (df["Class_Participation"] >= 0) & (df["Class_Participation"] <= 100)
    valid_backlogs = (df["Backlogs"] >= 0) & (df["Backlogs"] <= 10)
    valid_sleep = (df["Sleep_Hours"] >= 2) & (df["Sleep_Hours"] <= 12)
    valid_final = (df["Final_Marks"] >= 0) & (df["Final_Marks"] <= 100)
    
    valid_mask = (
        valid_attendance & valid_study & valid_assignment & valid_internal &
        valid_prev & valid_completion & valid_participation & valid_backlogs &
        valid_sleep & valid_final
    )
    
    clean_df = df[valid_mask].copy()
    invalid_df = df[~valid_mask].copy()
    
    quality_report["invalid_records"] = len(invalid_df)
    quality_report["clean_records"] = len(clean_df)
    
    return clean_df, quality_report, invalid_df


def prepare_powerbi_export(df: pd.DataFrame) -> pd.DataFrame:
    """Prepares Power BI optimized schema with rich calculated fields."""
    pbi_df = df.copy()
    
    # Add calculated attributes for Power BI dashboards
    pbi_df["Risk_Category"] = np.where(
        pbi_df["Overall_Performance"] == "At Risk", "High Risk",
        np.where(pbi_df["Overall_Performance"] == "Average", "Medium Risk", "Low Risk")
    )
    
    pbi_df["Attendance_Band"] = pd.cut(
        pbi_df["Attendance"],
        bins=[-1, 50, 75, 90, 100],
        labels=["<50% (Critical)", "50-75% (Warning)", "75-90% (Good)", ">90% (Excellent)"]
    )
    
    pbi_df["Study_Hours_Band"] = pd.cut(
        pbi_df["Study_Hours"],
        bins=[-1, 2, 5, 8, 16],
        labels=["<2 Hrs (Low)", "2-5 Hrs (Moderate)", "5-8 Hrs (High)", ">8 Hrs (Intense)"]
    )
    
    pbi_df["Grade_Point"] = np.where(
        pbi_df["Final_Marks"] >= 90, 10.0,
        np.where(pbi_df["Final_Marks"] >= 80, 9.0,
        np.where(pbi_df["Final_Marks"] >= 70, 8.0,
        np.where(pbi_df["Final_Marks"] >= 60, 7.0,
        np.where(pbi_df["Final_Marks"] >= 50, 6.0, 4.0))))
    )
    
    return pbi_df


if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    raw_path = os.path.join(base_dir, "student_performance.csv")
    processed_path = os.path.join(base_dir, "processed_data.csv")
    pbi_path = os.path.join(base_dir, "student_performance_powerbi.csv")
    
    if os.path.exists(raw_path):
        raw_df = pd.read_csv(raw_path)
        clean_df, report, _ = validate_and_clean_data(raw_df)
        clean_df.to_csv(processed_path, index=False)
        
        pbi_df = prepare_powerbi_export(clean_df)
        pbi_df.to_csv(pbi_path, index=False)
        print("Data cleaning & Power BI export completed successfully!")
        print(f"Report: {report}")
    else:
        print(f"Raw data file not found at {raw_path}")
