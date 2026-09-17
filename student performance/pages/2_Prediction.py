"""
Streamlit Page — Prediction.
Main Showcase Feature: Select Student ID, auto-fill profile & indicators, run AI prediction,
and view clean prediction result card.
"""

import os
import streamlit as st
import pandas as pd
from src.utils import apply_custom_css, render_kpi_card
from src.prediction import predict_student_performance, predict_batch_students
from src.database import save_prediction, get_all_students

st.set_page_config(page_title="Prediction — StudentIQ", page_icon="🔮", layout="wide")
apply_custom_css()

st.title("Predict Student Performance")
st.caption("Select a student profile to predict marks, overall grade, and academic risk.")

st.markdown("<br>", unsafe_allow_html=True)

tab_single, tab_batch = st.tabs(["Single Student Prediction", "Bulk CSV Upload Batch Prediction"])

# Load dataset for auto-fill lookups
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed_data.csv")
if os.path.exists(data_path):
    records_df = pd.read_csv(data_path)
else:
    records_df = get_all_students()
    if not records_df.empty:
        records_df.columns = [c.title() for c in records_df.columns]

# ----------------- TAB 1: SINGLE STUDENT PREDICTION -----------------
with tab_single:
    student_options = ["-- Select Student ID --"]
    if not records_df.empty:
        student_options += [
            f"{row['Student_ID']} — {row['Student_Name']} ({row['Department']})"
            for _, row in records_df.iterrows()
        ]
        
    selected_option = st.selectbox(
        "Select Student ID",
        options=student_options,
        index=1 if len(student_options) > 1 else 0
    )

    # Default values
    def_id = "STU1001"
    def_name = "Alex Rivera"
    def_gender = "Male"
    def_dept = "Computer Science and Engineering"
    def_age = 20
    def_year = 3
    def_sem = 5
    def_att = 82.0
    def_study = 4.5
    def_assign_score = 78.0
    def_internal = 74.0
    def_prev = 71.0
    def_assign_comp = 85.0
    def_part = 70.0
    def_backlogs = 0
    def_sleep = 7.0

    if selected_option != "-- Select Student ID --":
        stu_id_key = selected_option.split(" — ")[0]
        match_row = records_df[records_df["Student_ID"] == stu_id_key]
        if not match_row.empty:
            r = match_row.iloc[0]
            def_id = str(r["Student_ID"])
            def_name = str(r.get("Student_Name", "Student"))
            def_gender = str(r.get("Gender", "Male"))
            def_dept = str(r.get("Department", "Computer Science and Engineering"))
            def_age = int(r.get("Age", 20))
            def_year = int(r.get("Year", 3))
            def_sem = int(r.get("Semester", 5))
            def_att = float(r.get("Attendance", 82.0))
            def_study = float(r.get("Study_Hours", 4.5))
            def_assign_score = float(r.get("Assignment_Score", 78.0))
            def_internal = float(r.get("Internal_Marks", 74.0))
            def_prev = float(r.get("Previous_Semester_Marks", 71.0))
            def_assign_comp = float(r.get("Assignment_Completion", 85.0))
            def_part = float(r.get("Class_Participation", 70.0))
            def_backlogs = int(r.get("Backlogs", 0))
            def_sleep = float(r.get("Sleep_Hours", 7.0))

    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("predict_form"):
        st.markdown("### Student Profile")
        st.markdown("---")
        
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1:
            student_id = st.text_input("Student ID", value=def_id)
            age = st.number_input("Age", min_value=17, max_value=30, value=def_age)
        with p_col2:
            gender_opts = ["Male", "Female", "Other"]
            gender_idx = gender_opts.index(def_gender) if def_gender in gender_opts else 0
            gender = st.selectbox("Gender", options=gender_opts, index=gender_idx)
            year = st.selectbox("Year", options=[1, 2, 3, 4], index=max(0, def_year-1))
        with p_col3:
            dept_opts = [
                "Computer Science and Engineering",
                "Data Science",
                "Artificial Intelligence & Machine Learning",
                "Information Technology"
            ]
            dept_idx = dept_opts.index(def_dept) if def_dept in dept_opts else 0
            department = st.selectbox("Department", options=dept_opts, index=dept_idx)
            semester = st.selectbox("Semester", options=[1, 2, 3, 4, 5, 6, 7, 8], index=max(0, def_sem-1))

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Academic Indicators")
        st.markdown("---")

        i_col1, i_col2 = st.columns(2)
        with i_col1:
            internal_marks = st.slider("Internal Marks", min_value=0.0, max_value=100.0, value=float(def_internal), step=1.0)
            prev_sem_marks = st.slider("Previous Semester Marks", min_value=0.0, max_value=100.0, value=float(def_prev), step=1.0)
            assignment_score = st.slider("Assignment Score", min_value=0.0, max_value=100.0, value=float(def_assign_score), step=1.0)
            attendance = st.slider("Attendance Percentage (%)", min_value=0.0, max_value=100.0, value=float(def_att), step=1.0)

        with i_col2:
            study_hours = st.slider("Daily Study Hours (hrs/day)", min_value=0.0, max_value=14.0, value=float(def_study), step=0.5)
            backlogs = st.number_input("Pending Backlogs", min_value=0, max_value=10, value=def_backlogs)
            assignment_comp = st.slider("Assignment Completion (%)", min_value=0.0, max_value=100.0, value=float(def_assign_comp), step=1.0)
            sleep_hours = st.slider("Sleep Hours", min_value=2.0, max_value=12.0, value=float(def_sleep), step=0.5)
            participation = float(def_part)

        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.form_submit_button("Predict Performance", use_container_width=True)

    input_data = {
        "Student_ID": student_id,
        "Gender": gender,
        "Department": department,
        "Age": age,
        "Year": year,
        "Semester": semester,
        "Attendance": attendance,
        "Study_Hours": study_hours,
        "Assignment_Score": assignment_score,
        "Internal_Marks": internal_marks,
        "Previous_Semester_Marks": prev_sem_marks,
        "Assignment_Completion": assignment_comp,
        "Class_Participation": participation,
        "Backlogs": backlogs,
        "Sleep_Hours": sleep_hours
    }

    # Execute Prediction
    res = predict_student_performance(input_data)

    if "error" not in res:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#172554;'>PREDICTION RESULT</h3>", unsafe_allow_html=True)
        
        # Result Header Row
        res_c1, res_c2, res_c3 = st.columns(3)
        with res_c1:
            render_kpi_card("Predicted Final Marks", f"{res['predicted_marks']} / 100", f"Model: {res['regression_model']}", "#172554")
        with res_c2:
            perf_color = "#10B981" if res['predicted_performance'] in ["Excellent", "Good"] else "#F59E0B"
            render_kpi_card("Performance Category", f"{res['predicted_performance'].upper()}", "Academic Band", perf_color)
        with res_c3:
            render_kpi_card("Risk Level", f"{res['risk_level']}", f"Risk Score: {res['risk_score']} / 100", res['risk_color'])

        st.markdown("<br>", unsafe_allow_html=True)

        col_kf, col_sa = st.columns(2)
        with col_kf:
            st.markdown(
                """
                <div class="saas-card">
                    <h4 style="margin-top:0; color:#172554;">Key Factors</h4>
                """,
                unsafe_allow_html=True
            )
            for driver in res['risk_drivers']:
                st.markdown(f"✓ **{driver}**")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_sa:
            st.markdown(
                """
                <div class="saas-card">
                    <h4 style="margin-top:0; color:#172554;">Suggested Actions</h4>
                """,
                unsafe_allow_html=True
            )
            for sug in res['suggestions']:
                st.markdown(f"→ {sug}")
            st.markdown("</div>", unsafe_allow_html=True)

        # Log prediction to DB
        input_data["predicted_marks"] = res["predicted_marks"]
        input_data["predicted_performance"] = res["predicted_performance"]
        input_data["risk_level"] = res["risk_level"]
        input_data["regression_model"] = res["regression_model"]
        input_data["classification_model"] = res["classification_model"]
        input_data["student_id"] = student_id
        save_prediction(input_data)

# ----------------- TAB 2: BULK CSV BATCH PREDICTION -----------------
with tab_batch:
    st.markdown("### Bulk Dataset CSV Prediction")
    uploaded_file = st.file_uploader("Upload Student Dataset (CSV)", type=["csv"])

    if uploaded_file is not None:
        try:
            raw_input_df = pd.read_csv(uploaded_file)
            st.dataframe(raw_input_df.head(5), use_container_width=True)
            
            if st.button("Run Batch AI Predictions", use_container_width=True):
                predicted_df = predict_batch_students(raw_input_df)
                st.success(f"Processed predictions for {len(predicted_df)} students!")
                st.dataframe(predicted_df, use_container_width=True)
                
                out_csv = predicted_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Predicted Dataset (CSV)",
                    data=out_csv,
                    file_name="student_predictions_output.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Error processing CSV: {e}")
