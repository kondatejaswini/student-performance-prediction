"""
Streamlit Page — Analytics.
Organized into 4 clear analytical dimensions: Academic Performance, Academic Drivers, Student Behavior, and Data Relationships.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np

from src.utils import apply_custom_css
from src.eda import (
    plot_performance_distribution,
    plot_group_bar,
    plot_scatter_vs_final,
    plot_correlation_heatmap
)
from src.database import get_all_students

st.set_page_config(page_title="Analytics — StudentIQ", page_icon="📊", layout="wide")
apply_custom_css()

st.title("Academic Analytics")
st.caption("Explore student cohort metrics and driver relationships.")

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
    st.error("No dataset available.")
    st.stop()

# Sidebar Filters
st.sidebar.markdown("### Filters")
selected_dept = st.sidebar.multiselect("Department", options=df["Department"].unique(), default=df["Department"].unique())
selected_year = st.sidebar.multiselect("Academic Year", options=sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))

filtered_df = df[
    (df["Department"].isin(selected_dept)) &
    (df["Year"].isin(selected_year))
]

if filtered_df.empty:
    st.warning("No records match filter criteria.")
    st.stop()

# 4 Analytical Tabs
tab_perf, tab_drivers, tab_behavior, tab_corr = st.tabs([
    "Academic Performance",
    "Academic Drivers",
    "Student Behavior",
    "Data Relationships"
])

# ----------------- TAB 1: ACADEMIC PERFORMANCE -----------------
with tab_perf:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_performance_distribution(filtered_df), use_container_width=True)
    with c2:
        st.plotly_chart(plot_group_bar(filtered_df, "Department", "Department Performance"), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(plot_group_bar(filtered_df, "Year", "Year Performance"), use_container_width=True)
    with c4:
        st.plotly_chart(plot_group_bar(filtered_df, "Semester", "Semester Performance"), use_container_width=True)

# ----------------- TAB 2: ACADEMIC DRIVERS -----------------
with tab_drivers:
    d1, d2 = st.columns(2)
    with d1:
        st.plotly_chart(plot_scatter_vs_final(filtered_df, "Attendance", "Attendance vs Marks"), use_container_width=True)
    with d2:
        st.plotly_chart(plot_scatter_vs_final(filtered_df, "Internal_Marks", "Internal Marks vs Marks"), use_container_width=True)

    d3, d4 = st.columns(2)
    with d3:
        st.plotly_chart(plot_scatter_vs_final(filtered_df, "Study_Hours", "Study Hours vs Marks"), use_container_width=True)
    with d4:
        st.plotly_chart(plot_scatter_vs_final(filtered_df, "Assignment_Score", "Assignment Score vs Marks"), use_container_width=True)

    st.plotly_chart(plot_scatter_vs_final(filtered_df, "Previous_Semester_Marks", "Previous Semester vs Marks"), use_container_width=True)

# ----------------- TAB 3: STUDENT BEHAVIOR -----------------
with tab_behavior:
    b1, b2 = st.columns(2)
    with b1:
        st.plotly_chart(plot_scatter_vs_final(filtered_df, "Sleep_Hours", "Sleep vs Marks"), use_container_width=True)
    with b2:
        st.plotly_chart(plot_scatter_vs_final(filtered_df, "Backlogs", "Backlogs vs Marks"), use_container_width=True)

    b3, b4 = st.columns(2)
    with b3:
        st.plotly_chart(plot_scatter_vs_final(filtered_df, "Class_Participation", "Participation vs Marks"), use_container_width=True)
    with b4:
        st.plotly_chart(plot_scatter_vs_final(filtered_df, "Assignment_Completion", "Assignment Completion vs Marks"), use_container_width=True)

    st.plotly_chart(plot_group_bar(filtered_df, "Gender", "Gender Performance"), use_container_width=True)

# ----------------- TAB 4: DATA RELATIONSHIPS -----------------
with tab_corr:
    st.plotly_chart(plot_correlation_heatmap(filtered_df), use_container_width=True)
