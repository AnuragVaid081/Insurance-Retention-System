from pathlib import Path
import sys

import streamlit as st
import pandas as pd

DASHBOARD_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DASHBOARD_DIR))

from utils import load_data
from dashborad_styles import *

load_css()

df = load_data()

st.title("📞 Renewal Predictions")

st.caption(
    "Identify policies that require immediate renewal attention."
)

st.sidebar.header("Filters")

selected_area = st.sidebar.selectbox(

    "Customer Area",

    ["All"] + sorted(df["Customer_Area"].unique().tolist())

)

selected_channel = st.sidebar.selectbox(

    "Channel",

    ["All"] + sorted(df["Channel_Type"].unique().tolist())

)

selected_vehicle = st.sidebar.selectbox(

    "Vehicle Type",

    ["All"] + sorted(df["Vehicle_Type"].unique().tolist())

)

search_policy = st.sidebar.text_input(

    "Search Policy Number"

)

filtered_df = df.copy()

if selected_area != "All":

    filtered_df = filtered_df[
        filtered_df["Customer_Area"] == selected_area
    ]

if selected_channel != "All":

    filtered_df = filtered_df[
        filtered_df["Channel_Type"] == selected_channel
    ]

if selected_vehicle != "All":

    filtered_df = filtered_df[
        filtered_df["Vehicle_Type"] == selected_vehicle
    ]

if search_policy:

    filtered_df = filtered_df[

        filtered_df["Policy_Number"]

        .str.contains(

            search_policy,

            case=False

        )

    ]

display_columns = [

    "Policy_Number",

    "Customer_Area",

    "Channel_Type",

    "Make",

    "Model",

    "Premium",

    "NCB",

    "Claim_Count",

    "Policy_Tenure"

]

st.dataframe(

    filtered_df[display_columns],

    use_container_width=True,

    hide_index=True

)