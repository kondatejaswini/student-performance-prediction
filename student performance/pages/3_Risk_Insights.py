"""
Streamlit Page — Risk Insights.
Visually simple academic risk assessment, risk score badge, drivers, and numbered recommendations.
"""

import os
import streamlit as st
import pandas as pd
from src.utils import apply_custom_css, render_kpi_card
from src.risk_analysis import evaluate_academic_risk
from src.database import get_all_students

st.set_page_config(page_title="Risk Insights — StudentIQ", page_icon="⚠️", layout="wide")
apply_custom_css()

st.title("Academic Risk Assessment")
st.caption("Identify academic friction drivers and targeted student intervention actions.")

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
    st.error("No dataset loaded.")
    st.stop()

# Student Selector
student_options = [
    f"{row['Student_ID']} — {row['Student_Name']} ({row['Department']})"
    for _, row in df.iterrows()
]

selected_student = st.selectbox("Select Student Profile", options=student_options, index=0)

if selected_student:
    stu_id_key = selected_student.split(" — ")[0]
    match = df[df["Student_ID"] == stu_id_key]
    
    if not match.empty:
        s = match.iloc[0].to_dict()
        risk_info = evaluate_academic_risk(s)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Risk Score Hero Banner
        r_col1, r_col2 = st.columns([1, 2])
        
        with r_col1:
            st.markdown(
                f"""
                <div class="saas-card" style="text-align:center; padding:32px 20px;">
                    <div style="color:#64748B; font-size:0.85rem; font-weight:600; letter-spacing:0.05em;">RISK SCORE</div>
                    <div style="font-family:'Manrope',sans-serif; font-size:4rem; font-weight:800; color:{risk_info['risk_color']}; line-height:1;">{risk_info['risk_score']}</div>
                    <div style="margin-top:12px;">
                        <span style="background-color:{risk_info['risk_color']}20; color:{risk_info['risk_color']}; padding:6px 16px; border-radius:9999px; font-weight:700; font-size:0.9rem;">
                            {risk_info['risk_level']}
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with r_col2:
            st.markdown(
                f"""
                <div class="saas-card" style="height:100%;">
                    <h4 style="margin-top:0; color:#172554;">Assessment Summary</h4>
                    <p style="color:#334155; font-size:0.95rem; line-height:1.6;">{risk_info['summary']}</p>
                    <p style="color:#94A3B8; font-size:0.8rem; margin-top:20px;">{risk_info['disclaimer']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        d_col, a_col = st.columns(2)
        
        with d_col:
            st.markdown("### Risk Drivers")
            st.markdown("---")
            
            att_check = "✓" if s["Attendance"] >= 75 else "⚠"
            int_check = "✓" if s["Internal_Marks"] >= 65 else "⚠"
            back_check = "✓" if s["Backlogs"] == 0 else "⚠"
            study_check = "✓" if s["Study_Hours"] >= 4.0 else "⚠"
            
            st.markdown(f"**Attendance ({s['Attendance']}%)** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `{att_check}`")
            st.markdown(f"**Internal Marks ({s['Internal_Marks']}/100)** &nbsp;&nbsp; `{int_check}`")
            st.markdown(f"**Backlogs ({s['Backlogs']} papers)** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `{back_check}`")
            st.markdown(f"**Study Hours ({s['Study_Hours']} hrs/d)** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `{study_check}`")

        with a_col:
            st.markdown("### Recommended Actions")
            st.markdown("---")
            
            actions = []
            if s["Attendance"] < 75:
                actions.append("Improve attendance above 75% target threshold")
            else:
                actions.append("Maintain current consistent attendance")
                
            if s["Study_Hours"] < 4.0:
                actions.append("Increase daily self-study to at least 4.0 hours")
            else:
                actions.append("Continue regular self-study consistency")
                
            if s["Internal_Marks"] < 65:
                actions.append("Focus on internal mid-term assessment preparation")
            else:
                actions.append("Maintain strong internal test performance")

            if s["Backlogs"] > 0:
                actions.append(f"Clear {s['Backlogs']} pending backlog paper(s) in re-exams")

            for i, act in enumerate(actions, start=1):
                st.markdown(f"**`0{i}`** &nbsp;&nbsp; {act}")
