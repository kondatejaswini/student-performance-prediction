"""
Classification Pipeline Training Module for Student Performance Prediction System.
Trains, evaluates, and selects the best model for predicting Overall Performance category.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

NUMERIC_FEATURES = [
    "Attendance", "Study_Hours", "Assignment_Score", "Internal_Marks",
    "Previous_Semester_Marks", "Assignment_Completion", "Class_Participation",
    "Backlogs", "Sleep_Hours"
]

CATEGORICAL_FEATURES = ["Gender", "Department", "Year", "Semester"]
TARGET = "Overall_Performance"
CATEGORIES = ["Excellent", "Good", "Average", "At Risk"]

def train_and_evaluate_classification(df: pd.DataFrame) -> dict:
    """Trains classification models, evaluates Accuracy, Precision, Recall, F1, Confusion Matrix."""
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES)
        ]
    )
    
    models = {
        "Logistic Regression": LogisticRegression(max_iter=500, random_state=42),
        "Decision Tree Classifier": DecisionTreeClassifier(max_depth=6, random_state=42),
        "Random Forest Classifier": RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
        "KNN Classifier": KNeighborsClassifier(n_neighbors=7)
    }
    
    results = {}
    best_model_name = None
    best_f1 = -float("inf")
    best_pipeline = None
    
    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", model)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
        cm = confusion_matrix(y_test, y_pred, labels=CATEGORIES).tolist()
        
        results[name] = {
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1": round(f1, 4),
            "Confusion_Matrix": cm
        }
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_pipeline = pipeline

    # Extract Feature Importances
    feature_importance_dict = {}
    if hasattr(best_pipeline.named_steps["classifier"], "feature_importances_"):
        ohe = best_pipeline.named_steps["preprocessor"].named_transformers_["cat"]
        cat_feature_names = ohe.get_feature_names_out(CATEGORICAL_FEATURES).tolist()
        all_feature_names = NUMERIC_FEATURES + cat_feature_names
        importances = best_pipeline.named_steps["classifier"].feature_importances_
        feature_importance_dict = dict(zip(all_feature_names, [round(f, 4) for f in importances]))

    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    # Save best classification model
    model_save_path = os.path.join(models_dir, "overall_performance_model.pkl")
    joblib.dump(best_pipeline, model_save_path)
    
    summary = {
        "best_model_name": best_model_name,
        "categories": CATEGORIES,
        "results": results,
        "feature_importances": feature_importance_dict
    }
    
    return summary

if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed_data.csv")
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        summary = train_and_evaluate_classification(df)
        print("Classification Model Training Completed Successfully!")
        print(f"Best Classification Model: {summary['best_model_name']}")
        print("Results Table:")
        for m, metrics in summary['results'].items():
            print(f"  {m}: Acc={metrics['Accuracy']}, Prec={metrics['Precision']}, Rec={metrics['Recall']}, F1={metrics['F1']}")
    else:
        print(f"Data file not found at {data_path}")
