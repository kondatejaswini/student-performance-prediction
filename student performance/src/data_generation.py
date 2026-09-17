"""
Data Generation Module for Student Performance Prediction System.
Generates realistic synthetic dataset with correlated student features.
Default size: 500 student records.
"""

import os
import numpy as np
import pandas as pd

FIRST_NAMES = [
    "Aarav", "Aditi", "Aditya", "Akash", "Ananya", "Aniket", "Arjun", "Bhavya", "Dev", "Divya",
    "Gaurav", "Isha", "Karan", "Kavya", "Manish", "Meera", "Neha", "Nikhil", "Pooja", "Pranav",
    "Priya", "Rahul", "Rhea", "Rohan", "Sanjana", "Sharad", "Shruti", "Siddharth", "Sneha", "Tanvi",
    "Utkarsh", "Varun", "Vedant", "Vikram", "Yash", "Zoya", "Aman", "Rishabh", "Tanya", "Tarun"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Patel", "Reddy", "Nair", "Joshi", "Rao",
    "Chaudhary", "Mehta", "Deshmukh", "Kulkarni", "Bhat", "Iyer", "Agarwal", "Saxena", "Das", "Banerjee"
]

DEPARTMENTS = [
    "Computer Science and Engineering",
    "Data Science",
    "Artificial Intelligence & Machine Learning",
    "Information Technology"
]

GENDERS = ["Male", "Female", "Other"]

def generate_student_dataset(n_samples: int = 500, seed: int = 42) -> pd.DataFrame:
    """Generates synthetic student performance data with realistic statistical dependencies."""
    np.random.seed(seed)
    
    # Basic Demographics
    student_ids = [f"STU{1001 + i}" for i in range(n_samples)]
    firsts = np.random.choice(FIRST_NAMES, size=n_samples)
    lasts = np.random.choice(LAST_NAMES, size=n_samples)
    student_names = [f"{f} {l}" for f, l in zip(firsts, lasts)]
    
    years = np.random.choice([1, 2, 3, 4], size=n_samples, p=[0.25, 0.25, 0.25, 0.25])
    # Semester based on year (Year 1 -> Sem 1 or 2, etc.)
    semesters = []
    for y in years:
        sem = (y - 1) * 2 + np.random.choice([1, 2])
        semesters.append(sem)
    
    ages = np.array(years) + 17 + np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2])
    genders = np.random.choice(GENDERS, size=n_samples, p=[0.52, 0.46, 0.02])
    departments = np.random.choice(DEPARTMENTS, size=n_samples, p=[0.35, 0.30, 0.20, 0.15])
    
    # Latent student capability (0 to 1 score influencing multiple factors)
    capability = np.random.beta(a=3, b=2, size=n_samples)
    
    # Correlated academic inputs
    attendance = np.clip(capability * 70 + np.random.normal(25, 12, size=n_samples), 10, 100).round(1)
    study_hours = np.clip(capability * 8 + np.random.normal(2, 1.8, size=n_samples), 0.5, 12.0).round(1)
    assignment_score = np.clip(capability * 60 + np.random.normal(30, 10, size=n_samples), 0, 100).round(1)
    internal_marks = np.clip(capability * 65 + np.random.normal(25, 12, size=n_samples), 0, 100).round(1)
    previous_sem_marks = np.clip(capability * 60 + np.random.normal(28, 12, size=n_samples), 0, 100).round(1)
    assignment_completion = np.clip(attendance * 0.7 + capability * 30 + np.random.normal(0, 8, size=n_samples), 0, 100).round(1)
    class_participation = np.clip(attendance * 0.6 + capability * 30 + np.random.normal(0, 10, size=n_samples), 0, 100).round(1)
    
    # Backlogs (negatively correlated with capability and attendance)
    backlog_prob = np.clip(1.0 - capability - (attendance / 200.0), 0.05, 0.95)
    backlogs = np.random.binomial(n=5, p=backlog_prob * 0.6)
    
    # Sleep hours (moderate sleep is best, extreme low sleep reduces performance)
    sleep_hours = np.clip(np.random.normal(6.8, 1.3, size=n_samples), 3.0, 10.0).round(1)
    sleep_penalty = np.where(sleep_hours < 5, (5 - sleep_hours) * 2.5, 0) + np.where(sleep_hours > 9, (sleep_hours - 9) * 1.5, 0)
    
    # Calculate Final Marks using realistic multi-factor equation + noise
    weighted_score = (
        0.26 * internal_marks +
        0.22 * previous_sem_marks +
        0.18 * assignment_score +
        0.15 * attendance +
        0.10 * (study_hours / 12.0 * 100.0) +
        0.05 * assignment_completion +
        0.04 * class_participation -
        3.50 * backlogs -
        sleep_penalty +
        np.random.normal(0, 4.5, size=n_samples)
    )
    
    final_marks = np.clip(weighted_score, 0, 100).round(1)
    
    # Categorize Overall Performance
    # 85-100 -> Excellent, 70-84 -> Good, 50-69 -> Average, 0-49 -> At Risk
    performance_categories = []
    for mark in final_marks:
        if mark >= 85.0:
            performance_categories.append("Excellent")
        elif mark >= 70.0:
            performance_categories.append("Good")
        elif mark >= 50.0:
            performance_categories.append("Average")
        else:
            performance_categories.append("At Risk")
            
    df = pd.DataFrame({
        "Student_ID": student_ids,
        "Student_Name": student_names,
        "Age": ages,
        "Gender": genders,
        "Department": departments,
        "Year": years,
        "Semester": semesters,
        "Attendance": attendance,
        "Study_Hours": study_hours,
        "Assignment_Score": assignment_score,
        "Internal_Marks": internal_marks,
        "Previous_Semester_Marks": previous_sem_marks,
        "Assignment_Completion": assignment_completion,
        "Class_Participation": class_participation,
        "Backlogs": backlogs,
        "Sleep_Hours": sleep_hours,
        "Final_Marks": final_marks,
        "Overall_Performance": performance_categories
    })
    
    return df

if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "student_performance.csv")
    
    dataset = generate_student_dataset(n_samples=500)
    dataset.to_csv(csv_path, index=False)
    print(f"Dataset successfully created with {len(dataset)} records at {csv_path}")
