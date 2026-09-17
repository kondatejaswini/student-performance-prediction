"""
Streamlit Page — Students Directory.
Clean datatable with columns (ID, Name, Dept, Mark, Risk), quick search, filter, and CSV Export.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np

from src.utils import apply_custom_css
from src.database import get_all_students, get_prediction_history

st.set_page_config(page_title="Students — StudentIQ", page_icon="👥", layout="wide")
apply_custom_css()

st.title("Students Directory")
st.caption("Search, filter, and export student records.")

st.markdown("<br>", unsafe_allow_html=True)

# Load data
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed_data.csv")
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    df = get_all_students()
    if not df.empty:
        df.columns = [c.title() for c in df.columns]

if df.empty:
    st.error("No student data available.")
    st.stop()

if "Risk_Level" not in df.columns:
    df["Risk_Level"] = np.where(
        df["Overall_Performance"] == "At Risk", "HIGH RISK",
        np.where(df["Overall_Performance"] == "Average", "MEDIUM RISK", "LOW RISK")
    )

tab_dir, tab_logs = st.tabs(["Students Table", "SQLite Prediction Logs"])

# ----------------- TAB 1: STUDENTS DIRECTORY -----------------
with tab_dir:
    s_col, f_col1, f_col2 = st.columns([2, 1, 1])
    with s_col:
        search_query = st.text_input("Search student...", placeholder="Enter Student ID or Name...")
    with f_col1:
        dept_filter = st.multiselect("Department", options=df["Department"].unique(), default=df["Department"].unique())
    with f_col2:
        risk_filter = st.multiselect("Risk Level", options=df["Risk_Level"].unique(), default=df["Risk_Level"].unique())

    # Filter data
    filtered = df[
        (df["Department"].isin(dept_filter)) &
        (df["Risk_Level"].isin(risk_filter))
    ]

    if search_query:
        q = search_query.lower()
        filtered = filtered[
            filtered["Student_ID"].str.lower().str.contains(q) |
            filtered["Student_Name"].str.lower().str.contains(q)
        ]

    # Select clean display columns: ID, Name, Dept, Mark, Risk
    display_df = filtered[[
        "Student_ID", "Student_Name", "Department", "Final_Marks", "Risk_Level", "Attendance", "Study_Hours"
    ]].rename(columns={
        "Student_ID": "ID",
        "Student_Name": "Name",
        "Department": "Dept",
        "Final_Marks": "Mark",
        "Risk_Level": "Risk"
    })

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    csv_bytes = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Export CSV",
        data=csv_bytes,
        file_name="student_records_export.csv",
        mime="text/csv",
        use_container_width=True
    )

# ----------------- TAB 2: PREDICTION LOGS -----------------
with tab_logs:
    history_df = get_prediction_history(limit=100)
    if history_df.empty:
        st.info("No prediction logs recorded yet.")
    else:
        st.dataframe(history_df, use_container_width=True, hide_index=True)
