from dashborad_styles import load_css

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================================
# Project Imports
# ==========================================================

DASHBOARD_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = DASHBOARD_DIR.parent

sys.path.insert(0, str(DASHBOARD_DIR))
sys.path.insert(0, str(ROOT_DIR))


load_css()

# ==========================================================
# Load Dataset
# ==========================================================

DATASET = (
    ROOT_DIR
    / "Synthetic Generator"
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

