"""
Utility Helpers Module for Streamlit UI Styling and Components.
Implements Premium SaaS + Academic Intelligence Design Tokens.
"""

import streamlit as st

def apply_custom_css():
    """Injects Premium SaaS Light Slate & Navy CSS styles into Streamlit."""
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@600;700;800&display=swap');

        /* Global Font & Theme Baseline */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, sans-serif;
            color: #1E293B;
        }

        h1, h2, h3, h4, .stTitle, .stHeader {
            font-family: 'Manrope', -apple-system, sans-serif !important;
            color: #172554 !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }

        /* Clean SaaS Card Component */
        .saas-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03);
            margin-bottom: 20px;
        }

        /* Metric Card Container */
        .kpi-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 20px;
            text-align: left;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
            transition: all 0.2s ease;
        }
        
        .kpi-card:hover {
            border-color: #CBD5E1;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.06);
        }
        
        .kpi-title {
            color: #64748B;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }
        
        .kpi-value {
            color: #172554;
            font-family: 'Manrope', sans-serif;
            font-size: 2.1rem;
            font-weight: 800;
            line-height: 1.1;
        }
        
        .kpi-subtext {
            color: #94A3B8;
            font-size: 0.78rem;
            margin-top: 6px;
        }

        /* Risk Pill Badges */
        .badge-low {
            background-color: #DCFCE7;
            color: #15803D;
            padding: 4px 12px;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.8rem;
            display: inline-block;
        }
        
        .badge-med {
            background-color: #FEF3C7;
            color: #B45309;
            padding: 4px 12px;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.8rem;
            display: inline-block;
        }

        .badge-high {
            background-color: #FEE2E2;
            color: #B91C1C;
            padding: 4px 12px;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.8rem;
            display: inline-block;
        }

        /* Minimalist Table */
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }
        
        .styled-table th {
            background-color: #F8FAFC;
            color: #475569;
            font-weight: 600;
            text-align: left;
            padding: 12px 16px;
            border-bottom: 1px solid #E2E8F0;
        }
        
        .styled-table td {
            padding: 12px 16px;
            border-bottom: 1px solid #F1F5F9;
        }

        /* Remove default Streamlit padding clutter */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def render_kpi_card(title: str, value: str, subtext: str = "", color: str = "#172554"):
    """Renders a minimalist Premium SaaS KPI card."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value" style="color: {color};">{value}</div>
            <div class="kpi-subtext">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
