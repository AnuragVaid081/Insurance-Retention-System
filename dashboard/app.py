import streamlit as st

from dashborad_styles import load_css

load_css()

st.set_page_config(
    page_title="Renewal Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:

    st.markdown("# 🟡 Renewal Intelligence")

    st.caption("X Y Z Insurance")

    st.divider()

    st.success("Machine Learning Powered")

    st.divider()

    st.caption("Version 1.0")

st.sidebar.title("Navigation")

st.title("📊 Renewal Intelligence Dashboard")

st.markdown(
"""
Welcome to the **Renewal Intelligence Dashboard**.

Use the navigation panel on the left to explore:

- 📈 Portfolio Overview
- 🎯 Renewal Predictions
- 🏢 Channel Analysis
- 🤖 Model Insights
"""
)

st.info(
    "This dashboard is designed to assist renewal managers in prioritising renewals using machine learning insights."
)