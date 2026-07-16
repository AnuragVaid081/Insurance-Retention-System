from pathlib import Path

import joblib
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parent.parent.parent

MODEL_DIR = ROOT / "saved_models"

MODEL_DIR.mkdir(exist_ok=True)

# ==========================================================
# Columns
# ==========================================================

CATEGORICAL_COLUMNS = [

    "Make",

    "Model",

    "Vehicle_Type",

    "Fuel_Type",

    "Customer_Area",

    "Channel_Type"
]

NUMERIC_COLUMNS = [

    "Policy_Tenure",

    "Premium",

    "IDV",

    "Premium_to_IDV_Ratio",

    "Claim_Count",

    "Total_Claim_Amount",

    "NCB",

    "Previous_NCB",

    "Previous_Claim_Count",

    "Vehicle_Age",

    "Years_With_Channel"
]

# ==========================================================
# Main preprocessing
# ==========================================================

def fit_preprocessor(df):

    df = df.copy()

    label_encoders = {}

    # ----------------------------------------------
    # Encode categoricals
    # ----------------------------------------------

    for column in CATEGORICAL_COLUMNS:

        encoder = LabelEncoder()

        df[column] = encoder.fit_transform(
            df[column].astype(str)
        )

        label_encoders[column] = encoder

    # ----------------------------------------------
    # Scale numeric columns
    # ----------------------------------------------

    scaler = StandardScaler()

    df[NUMERIC_COLUMNS] = scaler.fit_transform(
        df[NUMERIC_COLUMNS]
    )

    # ----------------------------------------------
    # Save transformers
    # ----------------------------------------------

    joblib.dump(

        scaler,

        MODEL_DIR / "lstm_scaler.pkl"

    )

    joblib.dump(

        label_encoders,

        MODEL_DIR / "lstm_label_encoders.pkl"

    )

    return df

def transform_for_lstm(df):

    df = df.copy()

    print("Inside transform:")
    print(df[["Make", "Model", "Customer_Area"]].head())

    # ----------------------------------------------
    # Load transformers
    # ----------------------------------------------

    scaler = joblib.load(
        MODEL_DIR / "lstm_scaler.pkl"
    )

    label_encoders = joblib.load(
        MODEL_DIR / "lstm_label_encoders.pkl"
    )

    # ----------------------------------------------
    # Encode categoricals
    # ----------------------------------------------

    print(df[[
    "Make",
    "Model",
    "Customer_Area"
    ]].head())

    for column in CATEGORICAL_COLUMNS:

        encoder = label_encoders[column]

        df[column] = df[column].astype(str)

        unseen = ~df[column].isin(encoder.classes_)

        if unseen.any():

            print(
                f"Warning: unseen values found in {column}"
            )

            df.loc[unseen, column] = encoder.classes_[0]

        df[column] = encoder.transform(
            df[column]
        )

    # ----------------------------------------------
    # Scale numerics
    # ----------------------------------------------

    df[NUMERIC_COLUMNS] = scaler.transform(
        df[NUMERIC_COLUMNS]
    )

    return df