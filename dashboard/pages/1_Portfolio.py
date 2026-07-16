import streamlit as st
import sys
from pathlib import Path

import plotly.express as px

from dashborad_styles import load_css

DASHBOARD_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(DASHBOARD_DIR))


from utils import load_data


load_css()

df = load_data()



st.title("📈 Portfolio Overview")

# ==========================================
# KPI Cards
# ==========================================

total_policies = len(df)

renewed = int(df["Renewed"].sum())

renewal_rate = df["Renewed"].mean() * 100

high_risk = len(df[df["Renewed"] == 0])

average_premium = df["Premium"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📄 Active Portfolio",
        f"{total_policies:,}"
    )

with col2:

    st.metric(
        "🟡 Expected Renewal Rate",
        f"{renewal_rate:.1f}%"
    )

with col3:

    st.metric(
        "🚨 Priority Renewals",
        f"{high_risk:,}"
    )

with col4:

    st.metric(
        "💰 Avg Premium",
        f"₹{average_premium:,.0f}"
    )

    # ==========================================
# First Row
# ==========================================

col1, col2 = st.columns(2)

with col1:

    trend = (
        df
        .groupby(df["RID"].dt.to_period("M"))
        .size()
        .reset_index(name="Policies")
    )

    trend["RID"] = trend["RID"].astype(str)

    fig = px.line(

        trend,

        x="RID",

        y="Policies",

        markers=True,

        title="Monthly Policy Trend"

    )
    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F1117",
    plot_bgcolor="#0F1117",
    font=dict(color="#F8FAFC"),
    margin=dict(l=20, r=20, t=50, b=20)
)

    st.plotly_chart(
        fig,
        width= "stretch"
    )

with col2:

    fig = px.pie(

        df,

        names="Vehicle_Type",

        title="Vehicle Distribution"

    )

    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F1117",
    plot_bgcolor="#0F1117",
    font=dict(color="#F8FAFC"),
    margin=dict(l=20, r=20, t=50, b=20)
)

    st.plotly_chart(
        fig,
        width= "stretch"
    )

    # ==========================================
# Second Row
# ==========================================

col1, col2 = st.columns(2)

with col1:

    channel_counts = (

        df["Channel_Type"]

        .value_counts()

        .reset_index()

    )

    channel_counts.columns = [

        "Channel",

        "Policies"

    ]

    fig = px.bar(

        channel_counts,

        x="Channel",

        y="Policies",

        title="Policies by Channel"

    )

    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F1117",
    plot_bgcolor="#0F1117",
    font=dict(color="#F8FAFC"),
    margin=dict(l=20, r=20, t=50, b=20)
)

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with col2:

    fig = px.histogram(

        df,

        x="Premium",

        nbins=30,

        title="Premium Distribution"

    )

    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F1117",
    plot_bgcolor="#0F1117",
    font=dict(color="#F8FAFC"),
    margin=dict(l=20, r=20, t=50, b=20)
)

    st.plotly_chart(

        fig,

        width= "stretch"

    )

    # ==========================================
# Recent Policies
# ==========================================

st.subheader("Recent Policies")

recent = (

    df

    [

        [

            "Policy_Number",

            "Make",

            "Model",

            "Premium",

            "Renewed"

        ]

    ]

    .sort_values(

        "Policy_Number",

        ascending=False

    )

    .head(20)

)

st.dataframe(

    recent,

    width = "stretch",

    hide_index=True

)

