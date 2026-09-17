"""
Regression Pipeline Training Module for Student Performance Prediction System.
Trains, evaluates, and selects the best model for predicting Final Marks.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

NUMERIC_FEATURES = [
    "Attendance", "Study_Hours", "Assignment_Score", "Internal_Marks",
    "Previous_Semester_Marks", "Assignment_Completion", "Class_Participation",
    "Backlogs", "Sleep_Hours"
]

CATEGORICAL_FEATURES = ["Gender", "Department", "Year", "Semester"]
TARGET = "Final_Marks"

def train_and_evaluate_regression(df: pd.DataFrame) -> dict:
    """Trains regression models, evaluates MAE, RMSE, R2, and saves the best model."""
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES)
        ]
    )
    
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree Regressor": DecisionTreeRegressor(max_depth=6, random_state=42),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42),
        "KNN Regressor": KNeighborsRegressor(n_neighbors=7)
    }
    
    results = {}
    best_model_name = None
    best_r2 = -float("inf")
    best_pipeline = None
    
    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("regressor", model)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4),
            "R2": round(r2, 4),
            "y_test": y_test.tolist(),
            "y_pred": y_pred.tolist()
        }
        
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_pipeline = pipeline

    # Extract Feature Importances if best model is Random Forest or Decision Tree
    feature_importance_dict = {}
    if hasattr(best_pipeline.named_steps["regressor"], "feature_importances_"):
        ohe = best_pipeline.named_steps["preprocessor"].named_transformers_["cat"]
        cat_feature_names = ohe.get_feature_names_out(CATEGORICAL_FEATURES).tolist()
        all_feature_names = NUMERIC_FEATURES + cat_feature_names
        importances = best_pipeline.named_steps["regressor"].feature_importances_
        feature_importance_dict = dict(zip(all_feature_names, [round(f, 4) for f in importances]))

    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    # Save best regression model
    model_save_path = os.path.join(models_dir, "final_marks_model.pkl")
    joblib.dump(best_pipeline, model_save_path)
    
    summary = {
        "best_model_name": best_model_name,
        "results": results,
        "feature_importances": feature_importance_dict,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES
    }
    
    return summary

if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed_data.csv")
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        summary = train_and_evaluate_regression(df)
        print("Regression Model Training Completed Successfully!")
        print(f"Best Regression Model: {summary['best_model_name']}")
        print("Results Table:")
        for m, metrics in summary['results'].items():
            print(f"  {m}: MAE={metrics['MAE']}, RMSE={metrics['RMSE']}, R2={metrics['R2']}")
    else:
        print(f"Data file not found at {data_path}")
