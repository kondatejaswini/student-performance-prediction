"""
EDA Visualization Module for Student Performance Prediction System.
Generates minimal, elegant Plotly visualizations styled for Premium SaaS theme.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

try:
    import statsmodels.api as sm
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False

COLOR_PRIMARY = "#172554"
COLOR_ACCENT = "#6366F1"
COLOR_PERFORMANCE = {
    "Excellent": "#10B981", # Green
    "Good": "#6366F1",      # Indigo
    "Average": "#F59E0B",   # Amber
    "At Risk": "#EF4444"    # Red
}

COLOR_RISK = {
    "LOW RISK": "#10B981",
    "MEDIUM RISK": "#F59E0B",
    "HIGH RISK": "#EF4444"
}

def plot_performance_distribution(df: pd.DataFrame) -> go.Figure:
    """Pie/Donut chart showing distribution of overall performance categories."""
    counts = df["Overall_Performance"].value_counts().reset_index()
    counts.columns = ["Category", "Count"]
    fig = px.pie(
        counts,
        values="Count",
        names="Category",
        color="Category",
        color_discrete_map=COLOR_PERFORMANCE,
        hole=0.5,
        title="Performance Distribution"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        template="plotly_white",
        margin=dict(t=40, b=20, l=20, r=20),
        font=dict(family="Inter, sans-serif", color="#334155")
    )
    return fig

def plot_risk_distribution(df: pd.DataFrame) -> go.Figure:
    """Donut chart showing risk level distribution."""
    if "Risk_Level" not in df.columns:
        df["Risk_Level"] = np.where(
            df["Overall_Performance"] == "At Risk", "HIGH RISK",
            np.where(df["Overall_Performance"] == "Average", "MEDIUM RISK", "LOW RISK")
        )
    counts = df["Risk_Level"].value_counts().reset_index()
    counts.columns = ["Risk_Level", "Count"]
    fig = px.pie(
        counts,
        values="Count",
        names="Risk_Level",
        color="Risk_Level",
        color_discrete_map=COLOR_RISK,
        hole=0.5,
        title="Academic Risk Distribution"
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        template="plotly_white",
        margin=dict(t=40, b=20, l=20, r=20),
        font=dict(family="Inter, sans-serif", color="#334155")
    )
    return fig

def plot_scatter_vs_final(df: pd.DataFrame, x_col: str, title: str) -> go.Figure:
    """Scatter plot comparing any numeric factor against Final Marks."""
    hover_cols = [c for c in ["Student_ID", "Student_Name", "Department"] if c in df.columns]
    use_trend = "ols" if (HAS_STATSMODELS and len(df) > 5) else None
    
    try:
        fig = px.scatter(
            df,
            x=x_col,
            y="Final_Marks",
            color="Overall_Performance",
            color_discrete_map=COLOR_PERFORMANCE,
            hover_data=hover_cols,
            trendline=use_trend,
            title=title,
            labels={x_col: x_col.replace("_", " "), "Final_Marks": "Final Marks (0-100)"}
        )
    except Exception:
        fig = px.scatter(
            df,
            x=x_col,
            y="Final_Marks",
            color="Overall_Performance",
            color_discrete_map=COLOR_PERFORMANCE,
            hover_data=hover_cols,
            trendline=None,
            title=title,
            labels={x_col: x_col.replace("_", " "), "Final_Marks": "Final Marks (0-100)"}
        )
        
    fig.update_layout(
        template="plotly_white",
        margin=dict(t=40, b=20, l=20, r=20),
        font=dict(family="Inter, sans-serif", color="#334155")
    )
    return fig

def plot_group_bar(df: pd.DataFrame, group_col: str, title: str) -> go.Figure:
    """Grouped bar chart showing average Final Marks."""
    temp_df = df.copy()
    temp_df[group_col] = temp_df[group_col].astype(str)
    grp = temp_df.groupby(group_col)["Final_Marks"].agg(["mean", "count"]).reset_index()
    grp["mean"] = grp["mean"].round(1)
    
    fig = px.bar(
        grp,
        x=group_col,
        y="mean",
        text="mean",
        color_discrete_sequence=["#172554"],
        title=title,
        labels={group_col: group_col.replace("_", " "), "mean": "Average Final Marks"}
    )
    fig.update_traces(texttemplate='%{text}', textposition='outside', marker_color='#172554')
    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        margin=dict(t=40, b=20, l=20, r=20),
        font=dict(family="Inter, sans-serif", color="#334155")
    )
    return fig

def plot_correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """Correlation heatmap of numerical features."""
    num_df = df.select_dtypes(include=[np.number])
    corr = num_df.corr().round(2)
    
    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Feature Correlation Matrix"
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(t=40, b=20, l=20, r=20),
        font=dict(family="Inter, sans-serif", color="#334155")
    )
    return fig

def plot_feature_importance(importance_dict: dict) -> go.Figure:
    """Bar chart for model feature importance."""
    if not importance_dict:
        return go.Figure()
    
    imp_df = pd.DataFrame(list(importance_dict.items()), columns=["Feature", "Importance"])
    imp_df = imp_df.sort_values(by="Importance", ascending=True).tail(8)
    
    fig = px.bar(
        imp_df,
        x="Importance",
        y="Feature",
        orientation="h",
        text="Importance",
        color_discrete_sequence=["#6366F1"],
        title="Top Feature Importance"
    )
    fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
    fig.update_layout(
        template="plotly_white",
        margin=dict(t=40, b=20, l=20, r=20),
        font=dict(family="Inter, sans-serif", color="#334155")
    )
    return fig
