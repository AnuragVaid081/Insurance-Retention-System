from dashborad_styles import load_css

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st
import requests


# ==========================================================
# Project Imports
# ==========================================================

DASHBOARD_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = DASHBOARD_DIR.parent

sys.path.insert(0, str(DASHBOARD_DIR))
sys.path.insert(0, str(ROOT_DIR))

from dashboard.services.llm.analyze_channel import analyze_channel

load_css()

# ==========================================================
# Load Dataset
# ==========================================================

DATASET = (
    ROOT_DIR
    / "Synthetic_Generator"
    / "data"
    / "model_dataset.csv"
)


@st.cache_data
def load_data():

    return pd.read_csv(DATASET)


df = load_data()

# ==========================================================
# Page
# ==========================================================

st.title("📊 Channel Analysis Dashboard")

st.caption(
    "Executive overview of channel performance followed by individual channel analytics."
)


# ==========================================================
# Executive Overview
# ==========================================================

st.header("Executive Overview")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(

    "Total Policies",

    f"{len(df):,}"

)

kpi2.metric(

    "Total IMDs",

    df["IMD_Code"].nunique()

)

kpi3.metric(

    "Overall Renewal Rate",

    f"{df['Renewed'].mean()*100:.1f}%"

)

kpi4.metric(

    "Average Premium",

    f"₹ {df['Premium'].mean()/1000:,.1f}K"

)

st.divider()

channel_summary = (

    df

    .groupby("Channel_Type")

    .agg(

        Policies=("Policy_Number", "count"),

        Renewal_Rate=("Renewed", "mean"),

        Average_Premium=("Premium", "mean"),

        Average_Claims=("Claim_Count", "mean")

    )

    .reset_index()

)

channel_summary["Renewal_Rate"] *= 100

left, right = st.columns([2, 1])

with left:

    st.subheader("Renewal Rate by Channel")

    fig = px.bar(

        channel_summary.sort_values(
            "Renewal_Rate"
        ),

        x="Renewal_Rate",

        y="Channel_Type",

        orientation="h",

        text="Renewal_Rate"

    )

    fig.update_traces(

        texttemplate="%{text:.1f}%"

    )

    fig.update_layout(

        xaxis_title="Renewal Rate (%)",

        yaxis_title="",

        height=350

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )


with right:

    st.subheader("Business Distribution")

    fig = px.pie(

        channel_summary,

        values="Policies",

        names="Channel_Type",

        hole=0.5

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

st.subheader("Channel Comparison")

display = channel_summary.copy()

display["Renewal_Rate"] = (
    display["Renewal_Rate"]
    .round(1)
)

display["Average_Premium"] = (
    display["Average_Premium"]
    .round(0)
)

display["Average_Claims"] = (
    display["Average_Claims"]
    .round(2)
)

st.dataframe(

    display,

    use_container_width=True,

    hide_index=True

)

st.divider()


# ==========================================================
# Individual Channel Analysis
# ==========================================================

for channel in sorted(df["Channel_Type"].unique()):

    st.header(f"📌 {channel} Performance")

    channel_df = df[
        df["Channel_Type"] == channel
    ].copy()

    # ======================================================
    # Channel KPIs
    # ======================================================

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(

        "Policies",

        len(channel_df)

    )

    kpi2.metric(

        "IMDs",

        channel_df["IMD_Code"].nunique()

    )

    kpi3.metric(

        "Renewal Rate",

        f"{channel_df['Renewed'].mean()*100:.1f}%"

    )

    kpi4.metric(

        "Average Premium",

        f"₹ {channel_df['Premium'].mean()/1000:,.1f}K"

    )

    st.divider()


    # ======================================================
    # IMD Summary
    # ======================================================

    imd_summary = (

        channel_df

        .groupby("IMD_Code")

        .agg(

            Portfolio_Size=("Policy_Number", "count"),

            Renewal_Rate=("Renewed", "mean"),

            Average_Premium=("Premium", "mean"),

            Total_Claims=("Claim_Count", "sum"),

            Average_NCB=("NCB", "mean"),

            Average_Tenure=("Policy_Tenure", "mean")

        )

        .reset_index()

    )

    imd_summary["Renewal_Rate"] *= 100

    # ======================================================
    # Top & Bottom IMDs
    # ======================================================

    left, right = st.columns(2)

    with left:

        st.subheader("🟢 Top Performing IMDs")

        top = (

            imd_summary

            .sort_values(

                "Renewal_Rate",

                ascending=False

            )

            .head(10)

        )

        fig = px.bar(

            top.sort_values("Renewal_Rate"),

            x="Renewal_Rate",

            y="IMD_Code",

            orientation="h",

            text="Renewal_Rate"

        )

        fig.update_traces(

            texttemplate="%{text:.1f}%"

        )

        fig.update_layout(

            height=420,

            xaxis_title="Renewal Rate (%)",

            yaxis_title=""

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        st.subheader("🔴 Lowest Performing IMDs")

        bottom = (

            imd_summary

            .sort_values(

                "Renewal_Rate"

            )

            .head(10)

        )

        fig = px.bar(

            bottom,

            x="Renewal_Rate",

            y="IMD_Code",

            orientation="h",

            text="Renewal_Rate"

        )

        fig.update_traces(

            texttemplate="%{text:.1f}%"

        )

        fig.update_layout(

            height=420,

            xaxis_title="Renewal Rate (%)",

            yaxis_title=""

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    # ======================================================
    # Portfolio Analysis
    # ======================================================

    st.subheader("📈 Portfolio Size vs Renewal Rate")

    fig = px.scatter(

        imd_summary,

        x="Portfolio_Size",

        y="Renewal_Rate",

        size="Portfolio_Size",

        hover_name="IMD_Code",

        color="Renewal_Rate",

        height=500

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # Detailed IMD Table
    # ======================================================

    st.subheader("📋 IMD Performance Summary")

    display = (

        imd_summary

        .sort_values(

            "Renewal_Rate",

            ascending=False

        )

    )

    display["Renewal_Rate"] = (

        display["Renewal_Rate"]

        .round(1)

    )

    display["Average_Premium"] = (

        display["Average_Premium"]

        .round(0)

    )

    display["Average_Tenure"] = (

        display["Average_Tenure"]

        .round(1)

    )

    st.dataframe(

        display,

        use_container_width=True,

        hide_index=True

    )
    
    # ======================================================
    # LLM analysis
    # ======================================================

    imd_profiles = []

    for _, row in imd_summary.iterrows():
        
        imd_code = row["IMD_Code"]

        imd_df = channel_df[channel_df["IMD_Code"] == imd_code]

        remarks =  imd_df["Last_Remark"].dropna().astype(str).tolist()

        remark_history = "\n".join(f"- {remark}" for remark in remarks)

        imd_profiles.append(
            
            f"""
        
        IMD Code: {imd_code}

        Portfolio Size: {int(row["Portfolio_Size"])}

        Renewal Rate: {row["Renewal_Rate"]}

        Average Premium: ₹{row["Average_Premium"]}

        Average NCB: {row["Average_NCB"]}

        Average Policy Tenure: {row["Average_Tenure"]}

        Total Claims: {int(row["Total_Claims"])}

        Remark History:

        {remark_history}

        ----------------------------------------
        """

        )

        prompt = f"""
        
        You are a senior insurance renewal strategy consultant for an Indian motor insurance company.

        Below is the complete performance summary of every IMD (Insurance Marketing Department) operating in the Jammu branch.

        Your task is to analyse the branch and explain the differences in renewal performance between IMDs.

        For every IMD:

        • Explain why its renewal rate is high or low.

        • Compare it with other IMDs.

        • Identify behavioural patterns.

        • Analyse remark history.

        • Explain possible reasons for customer retention or churn.

        • Identify recurring operational issues.

        • Highlight best-performing IMDs.

        • Highlight struggling IMDs.

        Finally provide:

        1. Executive Summary (Do not List every statistic from the content just summarise them to your best understanding.)

        2. Common Success Factors

        3. Common Failure Factors

        4. Remark Pattern Analysis

        5. Recommendations for Renewal Managers

        IMPORTANT:

        Do not invent facts.

        DO NOT FORGET TO PROVIDE ALL 5 FIGURES ASKED ABOVE.

        Remarks such as "Payment expected today" are not bad remarks, they only require follow ups.

        All claim amounts should be denoted in Rupees.

        All percentages should be between 0 to 100, apply decimals correctly.

        All numerical metrics to be rounded off to 2 decimal places.

        Only draw conclusions from the supplied data.

        Branch Data:

        {''.join(imd_profiles)}
        """

    if st.button("🤖 AI Channel Analysis",key= f"ai_analysis_{channel}", use_container_width=True):
        with st.spinner("Analyzing channel performance..."):
            channel_analysis = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:7b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout = 300
            )
            channel_analysis.raise_for_status()

            channel_analysis = channel_analysis.json()["response"]
            st.markdown(channel_analysis)

    csv = display.to_csv(

        index=False

    ).encode("utf-8")

    st.download_button(

        f"⬇ Download {channel} Report",

        data=csv,

        file_name=f"{channel}_Analysis.csv",

        mime="text/csv",

        key=f"download_{channel}"

    )

    st.divider()

