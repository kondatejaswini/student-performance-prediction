"""
Streamlit Page — Model Performance.
Faculty/Viva/Demo Mode: Summary metric cards for Regression & Classification, Actual vs Predicted,
Confusion Matrix, Feature Importance, and Residual Distribution.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.utils import apply_custom_css, render_kpi_card
from src.train_regression import train_and_evaluate_regression
from src.train_classification import train_and_evaluate_classification
from src.eda import plot_feature_importance

st.set_page_config(page_title="Model Performance — StudentIQ", page_icon="⚙️", layout="wide")
apply_custom_css()

st.title("Model Performance")
st.caption("Machine learning evaluation metrics, confusion matrices, and feature importance for viva demonstration.")

st.markdown("<br>", unsafe_allow_html=True)

data_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed_data.csv")
if not os.path.exists(data_path):
    st.error("Data file missing.")
    st.stop()

df = pd.read_csv(data_path)

@st.cache_data
def get_evals(dataframe):
    r_sum = train_and_evaluate_regression(dataframe)
    c_sum = train_and_evaluate_classification(dataframe)
    return r_sum, c_sum

with st.spinner("Loading evaluation metrics..."):
    reg_sum, clf_sum = get_evals(df)

# Regression Summary Box & Classification Summary Box
col_r_sum, col_c_sum = st.columns(2)

best_reg = reg_sum["results"][reg_sum["best_model_name"]]
best_clf = clf_sum["results"][clf_sum["best_model_name"]]

with col_r_sum:
    st.markdown(
        f"""
        <div class="saas-card" style="border-top:4px solid #172554;">
            <h4 style="margin-top:0; color:#172554;">Regression ({reg_sum['best_model_name']})</h4>
            <div style="display:flex; justify-content:space-between; margin-top:16px;">
                <div><small style="color:#64748B;">R² Score</small><h3 style="margin:0; color:#172554;">{best_reg['R2']}</h3></div>
                <div><small style="color:#64748B;">MAE</small><h3 style="margin:0; color:#172554;">{best_reg['MAE']}</h3></div>
                <div><small style="color:#64748B;">RMSE</small><h3 style="margin:0; color:#172554;">{best_reg['RMSE']}</h3></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_c_sum:
    st.markdown(
        f"""
        <div class="saas-card" style="border-top:4px solid #10B981;">
            <h4 style="margin-top:0; color:#172554;">Classification ({clf_sum['best_model_name']})</h4>
            <div style="display:flex; justify-content:space-between; margin-top:16px;">
                <div><small style="color:#64748B;">Accuracy</small><h3 style="margin:0; color:#10B981;">{(best_clf['Accuracy']*100):.1f}%</h3></div>
                <div><small style="color:#64748B;">F1 Score</small><h3 style="margin:0; color:#10B981;">{best_clf['F1']}</h3></div>
                <div><small style="color:#64748B;">Precision</small><h3 style="margin:0; color:#10B981;">{best_clf['Precision']}</h3></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# 4 Key Model Performance Visualizations
p_col1, p_col2 = st.columns(2)

with p_col1:
    y_test = best_reg["y_test"]
    y_pred = best_reg["y_pred"]
    fig_act = px.scatter(
        x=y_test,
        y=y_pred,
        labels={"x": "Actual Final Marks", "y": "Predicted Final Marks"},
        title="Actual vs Predicted Marks",
        color_discrete_sequence=["#172554"]
    )
    fig_act.add_trace(go.Scatter(x=[0, 100], y=[0, 100], mode="lines", name="Ideal", line=dict(color="#EF4444", dash="dash")))
    fig_act.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=20, r=20))
    st.plotly_chart(fig_act, use_container_width=True)

with p_col2:
    cm = best_clf["Confusion_Matrix"]
    categories = clf_sum["categories"]
    fig_cm = px.imshow(
        cm,
        x=categories,
        y=categories,
        text_auto=True,
        color_continuous_scale="Blues",
        title="Confusion Matrix Heatmap"
    )
    fig_cm.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=20, r=20))
    st.plotly_chart(fig_cm, use_container_width=True)

p_col3, p_col4 = st.columns(2)

with p_col3:
    if reg_sum["feature_importances"]:
        st.plotly_chart(plot_feature_importance(reg_sum["feature_importances"]), use_container_width=True)
    else:
        st.info("Feature importance unavailable for current regressor.")

with p_col4:
    residuals = np.array(y_test) - np.array(y_pred)
    fig_res = px.histogram(
        residuals,
        nbins=25,
        title="Residual Error Distribution",
        labels={"value": "Prediction Error"},
        color_discrete_sequence=["#6366F1"]
    )
    fig_res.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=20, r=20))
    st.plotly_chart(fig_res, use_container_width=True)
