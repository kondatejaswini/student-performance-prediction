"""
StudentIQ — Main Application Entrypoint: Overview Page.
Premium SaaS + Academic Intelligence Design.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np

from src.utils import apply_custom_css, render_kpi_card
from src.database import init_db, sync_csv_to_db, get_all_students
from src.data_generation import generate_student_dataset
from src.data_cleaning import validate_and_clean_data, prepare_powerbi_export
from src.train_regression import train_and_evaluate_regression
from src.train_classification import train_and_evaluate_classification
from src.eda import plot_performance_distribution, plot_group_bar

st.set_page_config(
    page_title="StudentIQ — Performance Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()

# Auto-Initialize Pipeline Data & Models
def initialize_system():
    init_db()
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    processed_path = os.path.join(data_dir, "processed_data.csv")
    reg_model_path = os.path.join(models_dir, "final_marks_model.pkl")
    clf_model_path = os.path.join(models_dir, "overall_performance_model.pkl")
    
    if not os.path.exists(processed_path):
        raw_df = generate_student_dataset(500)
        raw_path = os.path.join(data_dir, "student_performance.csv")
        raw_df.to_csv(raw_path, index=False)
        clean_df, _, _ = validate_and_clean_data(raw_df)
        clean_df.to_csv(processed_path, index=False)
        pbi_df = prepare_powerbi_export(clean_df)
        pbi_df.to_csv(os.path.join(data_dir, "student_performance_powerbi.csv"), index=False)
        sync_csv_to_db(processed_path)

    if not (os.path.exists(reg_model_path) and os.path.exists(clf_model_path)):
        df = pd.read_csv(processed_path)
        train_and_evaluate_regression(df)
        train_and_evaluate_classification(df)

initialize_system()

# Sidebar Navigation Header
st.sidebar.markdown("<h2 style='color:#172554; font-family:Manrope;'>STUDENT<b>IQ</b></h2>", unsafe_allow_html=True)
st.sidebar.caption("Academic Intelligence Platform")
st.sidebar.markdown("---")

# Header Section
st.title("Student Performance Intelligence")
st.caption("Predict academic outcomes. Identify risk early.")

st.markdown("<br>", unsafe_allow_html=True)

# Fetch Student Records Data
data_path = os.path.join(os.path.dirname(__file__), "data", "processed_data.csv")
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    df = get_all_students()
    if not df.empty:
        df.columns = [c.title() for c in df.columns]

if "Risk_Level" not in df.columns:
    df["Risk_Level"] = np.where(
        df["Overall_Performance"] == "At Risk", "HIGH RISK",
        np.where(df["Overall_Performance"] == "Average", "MEDIUM RISK", "LOW RISK")
    )

# 4 Core KPI Cards
col1, col2, col3, col4 = st.columns(4)

total_students = len(df)
avg_marks = f"{df['Final_Marks'].mean():.1f}"
avg_att = f"{df['Attendance'].mean():.1f}%"
high_risk_count = len(df[df["Risk_Level"] == "HIGH RISK"])

with col1:
    render_kpi_card("Students Tracked", str(total_students), "Active Batch Records", "#172554")
with col2:
    render_kpi_card("Average Final Marks", f"{avg_marks}", "Out of 100", "#10B981")
with col3:
    render_kpi_card("Average Attendance", avg_att, "Target 75%", "#6366F1")
with col4:
    render_kpi_card("Students Requiring Attention", str(high_risk_count), "High Risk Status", "#EF4444")

st.markdown("<br><br>", unsafe_allow_html=True)

# Performance Overview Section
st.subheader("Performance Overview")

chart_col1, chart_col2 = st.columns([1.2, 1])

with chart_col1:
    fig_dept = plot_group_bar(df, "Department", "Department Performance Breakdown")
    st.plotly_chart(fig_dept, use_container_width=True)

with chart_col2:
    fig_pie = plot_performance_distribution(df)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Early Risk Summary Section
st.subheader("Early Risk Summary")

risk_c1, risk_c2, risk_c3 = st.columns(3)

med_risk_count = len(df[df["Risk_Level"] == "MEDIUM RISK"])
low_risk_count = len(df[df["Risk_Level"] == "LOW RISK"])

with risk_c1:
    st.markdown(
        f"""
        <div class="saas-card" style="border-left: 4px solid #EF4444;">
            <span class="badge-high">HIGH RISK</span>
            <h3 style="margin-top:12px; margin-bottom:4px;">{high_risk_count} Students</h3>
            <p style="color:#64748B; font-size:0.85rem; margin:0;">Requires immediate intervention & counseling</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with risk_c2:
    st.markdown(
        f"""
        <div class="saas-card" style="border-left: 4px solid #F59E0B;">
            <span class="badge-med">MEDIUM RISK</span>
            <h3 style="margin-top:12px; margin-bottom:4px;">{med_risk_count} Students</h3>
            <p style="color:#64748B; font-size:0.85rem; margin:0;">Borderline metrics; monitor study consistency</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with risk_c3:
    st.markdown(
        f"""
        <div class="saas-card" style="border-left: 4px solid #10B981;">
            <span class="badge-low">LOW RISK</span>
            <h3 style="margin-top:12px; margin-bottom:4px;">{low_risk_count} Students</h3>
            <p style="color:#64748B; font-size:0.85rem; margin:0;">Healthy academic trajectory & attendance</p>
        </div>
        """,
        unsafe_allow_html=True
    )
