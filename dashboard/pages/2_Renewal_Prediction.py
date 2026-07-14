from pathlib import Path
import sys

import pandas as pd
import streamlit as st

# ==========================================================
# Project Imports
# ==========================================================

DASHBOARD_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = DASHBOARD_DIR.parent

sys.path.insert(0, str(DASHBOARD_DIR))
sys.path.insert(0, str(ROOT_DIR))

from dashborad_styles import *
from services.prediction_service import predict_monthly_renewals

load_css()

# ==========================================================
# Page Config
# ==========================================================

st.title("📂 Monthly Renewal Predictor")

st.caption(
    "Upload the monthly renewal sheet received from management."
)

# ==========================================================
# Upload
# ==========================================================

uploaded_file = st.file_uploader(
    "Upload Monthly Renewal Sheet",
    type=["xlsx", "xls"]
)

if uploaded_file is None:
    st.info("Please upload the monthly renewal sheet.")
    st.stop()

renewal_sheet = pd.read_excel(uploaded_file)

# ==========================================================
# Required Columns
# ==========================================================

REQUIRED_COLUMNS = [
    "Policy_Number",
    "IMD_Code",
    "RID",
    "RED",
    "NCB"
]

missing_columns = [
    col
    for col in REQUIRED_COLUMNS
    if col not in renewal_sheet.columns
]

if missing_columns:

    st.error(
        "The uploaded file is missing the following columns:"
    )

    st.write(missing_columns)

    st.stop()

# ==========================================================
# Preview
# ==========================================================

st.success(
    f"{len(renewal_sheet)} policies loaded successfully."
)

with st.expander("Preview Uploaded File", expanded=False):

    st.dataframe(
        renewal_sheet.head(10),
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# Run Prediction
# ==========================================================

if st.button(
    "🚀 Run AI Prediction",
    use_container_width=True
):

    with st.spinner("Generating predictions..."):

        results, missing_policies = predict_monthly_renewals(
            renewal_sheet
        )

    # ======================================================
    # Missing Policies
    # ======================================================

    if missing_policies:

        st.warning(
            f"{len(missing_policies)} policies could not be matched with the master database."
        )

        with st.expander("View Missing Policies"):

            st.write(missing_policies)

    # ======================================================
    # KPI Cards
    # ======================================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Policies Processed",
        len(results)
    )

    col2.metric(
        "Missing Policies",
        len(missing_policies)
    )

    col3.metric(
        "High Priority",
        (
            results["Priority"] == "🔴 High"
        ).sum()
    )

    col4.metric(
        "Average Renewal Probability",
        f"{results['Renewal_Probability'].mean():.1f}%"
    )

    st.divider()

    # ======================================================
    # Priority Filter
    # ======================================================

    priority = st.selectbox(

        "Filter by Priority",

        [
            "All",
            "🔴 High",
            "🟡 Medium",
            "🟢 Low"
        ]
    )

    filtered_results = results.copy()

    if priority != "All":

        filtered_results = filtered_results[
            filtered_results["Priority"] == priority
        ]

    # ======================================================
    # Display Results
    # ======================================================

    display_columns = [

        "Policy_Number",

        "Customer_Area",

        "Channel_Type",

        "Make",

        "Model",

        "Premium",

        "NCB",

        "Claim_Count",

        "Renewal_Probability",

        "Priority"

    ]

    st.dataframe(

        filtered_results[
            display_columns
        ],

        use_container_width=True,

        hide_index=True

    )

    # ======================================================
    # Download
    # ======================================================

    csv = filtered_results.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="⬇ Download Prediction Results",

        data=csv,

        file_name="Monthly_Renewal_Predictions.csv",

        mime="text/csv"

    )