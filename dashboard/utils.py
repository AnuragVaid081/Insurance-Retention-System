from pathlib import Path
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT / "Synthetic Generator" / "data" / "model_dataset.csv"
)

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_PATH)

    df["RID"] = pd.to_datetime(df["RID"])

    df["RED"] = pd.to_datetime(df["RED"])

    return df