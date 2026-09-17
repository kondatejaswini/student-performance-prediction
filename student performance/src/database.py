"""
Database Abstraction Module for Student Performance Prediction System.
Handles SQLite database initialization, record persistence, and prediction logging.
Designed for easy extension to MySQL or PostgreSQL.
"""

import os
import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__), "..", "student_performance.db")

def get_connection():
    """Establishes connection to SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes database schema for students and prediction history."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Students Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                student_name TEXT,
                age INTEGER,
                gender TEXT,
                department TEXT,
                year INTEGER,
                semester INTEGER,
                attendance REAL,
                study_hours REAL,
                assignment_score REAL,
                internal_marks REAL,
                previous_semester_marks REAL,
                assignment_completion REAL,
                class_participation REAL,
                backlogs INTEGER,
                sleep_hours REAL,
                final_marks REAL,
                overall_performance TEXT
            )
        """)
        
        # Prediction History Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prediction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                student_id TEXT,
                department TEXT,
                year INTEGER,
                attendance REAL,
                study_hours REAL,
                internal_marks REAL,
                previous_marks REAL,
                backlogs INTEGER,
                predicted_final_marks REAL,
                predicted_overall_performance TEXT,
                risk_level TEXT,
                regression_model TEXT,
                classification_model TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database Initialization Error: {e}")
        return False

def sync_csv_to_db(csv_path: str):
    """Populates SQLite students table from cleaned CSV file if empty."""
    if not os.path.exists(csv_path):
        return
    try:
        df = pd.read_csv(csv_path)
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]
        
        if count == 0:
            df.columns = [c.lower() for c in df.columns]
            df.to_sql("students", conn, if_exists="append", index=False)
            conn.commit()
            print(f"Synced {len(df)} student records to SQLite database.")
        conn.close()
    except Exception as e:
        print(f"Error syncing CSV to DB: {e}")

def save_prediction(prediction_data: dict) -> bool:
    """Saves a prediction entry into prediction_history table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO prediction_history (
                timestamp, student_id, department, year, attendance, study_hours,
                internal_marks, previous_marks, backlogs, predicted_final_marks,
                predicted_overall_performance, risk_level, regression_model, classification_model
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            prediction_data.get("student_id", "GUEST"),
            prediction_data.get("department", "CSE"),
            int(prediction_data.get("year", 1)),
            float(prediction_data.get("attendance", 0)),
            float(prediction_data.get("study_hours", 0)),
            float(prediction_data.get("internal_marks", 0)),
            float(prediction_data.get("previous_semester_marks", 0)),
            int(prediction_data.get("backlogs", 0)),
            float(prediction_data.get("predicted_marks", 0)),
            prediction_data.get("predicted_performance", "Unknown"),
            prediction_data.get("risk_level", "Unknown"),
            prediction_data.get("regression_model", "Random Forest"),
            prediction_data.get("classification_model", "Random Forest")
        ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving prediction: {e}")
        return False

def get_prediction_history(limit: int = 50) -> pd.DataFrame:
    """Fetches recent prediction history entries."""
    try:
        conn = get_connection()
        df = pd.read_sql_query(
            f"SELECT * FROM prediction_history ORDER BY id DESC LIMIT {limit}", conn
        )
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching history: {e}")
        return pd.DataFrame()

def get_all_students() -> pd.DataFrame:
    """Fetches all student records from database."""
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM students", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching students: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    init_db()
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed_data.csv")
    sync_csv_to_db(data_dir)
