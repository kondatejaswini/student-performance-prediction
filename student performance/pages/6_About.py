"""
Streamlit Page — About.
Clean minimalist overview of project vision, problem statement, academic disclaimer, architecture.
"""

import streamlit as st
from src.utils import apply_custom_css

st.set_page_config(page_title="About — StudentIQ", page_icon="ℹ️", layout="wide")
apply_custom_css()

st.title("About StudentIQ")
st.caption("Student Performance Prediction and Early Risk Identification Platform.")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="saas-card">
        <h3 style="margin-top:0; color:#172554;">Vision & Problem Statement</h3>
        <p style="color:#334155; line-height:1.6;">
            Traditional university grading operates retroactively—evaluating students only after semester examinations conclude. 
            <b>StudentIQ</b> addresses this gap by transforming mid-term academic indicators (attendance, internal test scores, study habits, assignment completion, backlogs, and sleep routine) into predictive foresight and early risk warnings.
        </p>
    </div>

    <div class="saas-card">
        <h3 style="margin-top:0; color:#172554;">Academic Support Disclaimer</h3>
        <p style="color:#334155; line-height:1.6;">
            This system is designed strictly as an <b>academic support tool</b> for faculty advisors and students. 
            Predictions and risk indicators represent statistical projections to facilitate timely academic intervention and must never be used as definitive judgments of a student's innate capabilities.
        </p>
    </div>

    <div class="saas-card">
        <h3 style="margin-top:0; color:#172554;">System Architecture & Stack</h3>
        <ul>
            <li><b>Core Engine:</b> Python 3.10+, Scikit-learn, Pandas, NumPy, Joblib</li>
            <li><b>UI & Analytics:</b> Streamlit, Plotly, Custom HTML/CSS System</li>
            <li><b>Persistence:</b> SQLite (<code>student_performance.db</code>)</li>
            <li><b>BI Export:</b> Power BI Compatible CSV Export (<code>student_performance_powerbi.csv</code>)</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)
