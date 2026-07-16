from pathlib import Path
import sys


import plotly.express as px
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
from services.shap_service import explain_prediction
from services.lstm_prediction_service import (
    predict_monthly_renewals_lstm
)

if "shap_cache" not in st.session_state:
    st.session_state.shap_cache = {}

if "results" not in st.session_state:
    st.session_state.results = None

if "missing_policies" not in st.session_state:
    st.session_state.missing_policies = []

if "renewal_sheet" not in st.session_state:
    st.session_state.renewal_sheet = None



load_css()

# ==========================================================
# Page Config
# ==========================================================

st.title("📂 Monthly Renewal Predictor")

st.caption(
    "Upload the monthly renewal sheet received from management."
)

model_type = st.radio(

    "Prediction Model",

    [

        "Random Forest",

        "LSTM"

    ],

    horizontal=True

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

if uploaded_file is not None:

    st.session_state.renewal_sheet = pd.read_excel(
        uploaded_file
    )

renewal_sheet = st.session_state.renewal_sheet

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

    if model_type == "Random Forest":

        (
            st.session_state.results,
            st.session_state.missing_policies
        ) = predict_monthly_renewals(
            renewal_sheet
        )

    else:

        (
            st.session_state.results,
            st.session_state.missing_policies
        ) = predict_monthly_renewals_lstm(
            renewal_sheet
        )

if st.session_state.results is not None:


    # ======================================================
    # Missing Policies
    # ======================================================

    if st.session_state.missing_policies:

        st.warning(
            f"{len(st.session_state.missing_policies)} policies could not be matched with the master database."
        )

        with st.expander("View Missing Policies"):

            st.write(st.session_state.missing_policies)

    # ======================================================
    # KPI Cards
    # ======================================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Policies Processed",
        len(st.session_state.results)
    )

    col2.metric(
        "Missing Policies",
        len(st.session_state.missing_policies)
    )

    col3.metric(
        "High Priority",
        (
            st.session_state.results["Priority"] == "🔴 High"
        ).sum()
    )

    col4.metric(
        "Average Renewal Probability",
        f"{st.session_state.results['Renewal_Probability'].mean():.1f}%"
    )

    st.divider()

    left, right = st.columns([5,2])

    with left:

        filter_col, search_col = st.columns([1,2])

        with filter_col:

            priority = st.selectbox(
                "Filter by Priority",
                [
                    "All",
                    "🔴 High",
                    "🟡 Medium",
                    "🟢 Low"
                ]
            )

        with search_col:

            search = st.text_input(
                "🔎 Search Policy Number"
            )

        filtered_results = st.session_state.results.copy()

        if priority != "All":

            filtered_results = filtered_results[
                filtered_results["Priority"] == priority
            ]

        if search:

            filtered_results = filtered_results[
                filtered_results["Policy_Number"]
                .astype(str)
                .str.contains(
                    search,
                    case=False
                )
            ]

        display_columns = [

            "Policy_Number",

            "IMD_Code",

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

            filtered_results[display_columns],

            use_container_width=True,

            hide_index=True

        )
    
    # ======================================================
    # SHAP explainaibility
    # ======================================================

    if model_type == "Random Forest":

        with right:

            st.markdown(
                "<h3 style='margin-top:0px;'>🔍 AI Explanation</h3>",
                unsafe_allow_html=True
    )

            if not filtered_results.empty:

                selected_policy = st.selectbox(

                    "Select Policy",

                    filtered_results["Policy_Number"]

                )

                selected_row = filtered_results[
                    filtered_results["Policy_Number"]
                    ==
                    selected_policy
                ].iloc[0]

                if selected_policy not in st.session_state.shap_cache:

                    st.session_state.shap_cache[selected_policy] = (
                        explain_prediction(selected_row)
                    )

                explanation = (
                    st.session_state.shap_cache[selected_policy]
                )

                # positive = explanation[
                #     explanation["Contribution"] > 0
                #     ].head(5)

                # negative = explanation[
                #     explanation["Contribution"] < 0
                #     ].head(5)

                positive = (
                    explanation[
                        explanation["Contribution"] > 0
                    ]
                    .sort_values("Contribution", ascending=False)
                    .head(5)
                )

                negative = (
                    explanation[
                        explanation["Contribution"] < 0
                    ]
                    .copy()
                )

                negative["Contribution"] = negative["Contribution"].abs()

                negative = (
                    negative
                    .sort_values("Contribution", ascending=False)
                    .head(5)
                )
                
                # st.markdown("#### 🟢 Increased Renewal Probability")

                # st.dataframe(

                #     positive,

                #     hide_index=True,

                #     use_container_width=True

                # )

                # st.markdown("#### 🔴 Reduced Renewal Probability")

                # st.dataframe(
                #     negative,
                #     hide_index=True,
                #     use_container_width=True
                # )

                st.markdown("#### 🟢 Factors Increasing Renewal")

                fig_positive = px.bar(

                    positive,

                    x="Contribution",

                    y="Feature",

                    orientation="h",

                    text="Contribution"

                )

                fig_positive.update_layout(

                    height=260,

                    margin=dict(
                        l=10,
                        r=10,
                        t=10,
                        b=10
                    ),

                    yaxis=dict(
                        categoryorder="total ascending"
                    )

                )

                

                fig_positive.update_traces(
                    texttemplate = "%{x:.3f}",
                    textposition = "outside"
                )

                st.plotly_chart(
                    fig_positive,
                    use_container_width=True
                )

                st.markdown("#### 🔴 Factors Reducing Renewal")

                fig_negative = px.bar(

                    negative,

                    x="Contribution",

                    y="Feature",

                    orientation="h",

                    text="Contribution"

                )

                fig_negative.update_layout(

                    height=260,

                    margin=dict(
                        l=10,
                        r=10,
                        t=10,
                        b=10
                    ),

                    yaxis=dict(
                        categoryorder="total ascending"
                    )

                )

                fig_negative.update_traces(
                    texttemplate = "%{x:.3f}",
                    textposition = "outside"
                )

                st.plotly_chart(
                    fig_negative,
                    use_container_width=True
                )

            else:

                st.info("No policies found.")

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