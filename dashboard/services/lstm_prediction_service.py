from pathlib import Path

import numpy as np
import pandas as pd

import sys



from tensorflow.keras.models import load_model


# ==========================================================
# Paths
# ==========================================================

ROOT = Path(__file__).resolve().parent.parent.parent
PATH_MODEL = ROOT / "models"
PATH_PREPROCCESING = PATH_MODEL / "preprocessing"

MODEL_DIR = ROOT / "saved_models"

DATASET = (
    ROOT
    / "Synthetic Generator"
    / "data"
    / "model_dataset.csv"
)


sys.path.insert(0,str(PATH_MODEL))

from training_features import MODEL_FEATURES
from preprocessing.tabular_preprocessing import fit_preprocessor
from preprocessing.tabular_preprocessing import (
    transform_for_lstm
)

# ==========================================================
# Load Assets
# ==========================================================

MODEL = load_model(
    MODEL_DIR / "lstm_model.keras"
)


print("DATASET PATH:")
print(DATASET.resolve())

MASTER_DATA = pd.read_csv(DATASET)

print(MASTER_DATA.head())
print("Immediately after reading CSV:")
print(MASTER_DATA[["Make", "Model", "Customer_Area"]].head())

print(MASTER_DATA[[
    "Make",
    "Model",
    "Customer_Area"
]].head())


print("Before transform:")
print(MASTER_DATA[["Make", "Model", "Customer_Area"]].head())

MODEL_DATA = transform_for_lstm(MASTER_DATA)


# ==========================================================
# Priority
# ==========================================================

def assign_priority(probability):

    if probability < 40:

        return "🔴 High"

    elif probability < 70:

        return "🟡 Medium"

    else:

        return "🟢 Low"


# ==========================================================
# Prediction
# ==========================================================

def predict_monthly_renewals_lstm(renewal_sheet):

    results = []

    missing_policies = []

    for _, renewal in renewal_sheet.iterrows():

        policy_number = renewal["Policy_Number"]

        display_policy = MASTER_DATA[
            MASTER_DATA["Policy_Number"] == policy_number
        ]

        model_policy = MODEL_DATA[
            MODEL_DATA["Policy_Number"] == policy_number
        ]


        if display_policy.empty:

            missing_policies.append(policy_number)

            continue

        display_policy = display_policy.copy()

        # --------------------------------------------------
        # Update live values from uploaded sheet
        # --------------------------------------------------

        if "NCB" in renewal_sheet.columns:

            display_policy.loc["NCB"] = renewal["NCB"]

        
        # --------------------------------------------------
        # Feature Matrix
        # --------------------------------------------------
        
        X = model_policy[MODEL_FEATURES].values.astype(np.float32)

        # Sequence length = 1 (Demo)
        X = X.reshape(
            X.shape[0],
            1,
            X.shape[1]
        )

        probability = MODEL.predict(
            X,
            verbose=0
        )[0][0]

        probability = round(
            probability * 100,
            1
        )

        output = {

            "Policy_Number": display_policy.iloc[0]["Policy_Number"],

            "IMD_Code": display_policy.iloc[0]["IMD_Code"],

            "Policy_Tenure": display_policy.iloc[0]["Policy_Tenure"],

            "Customer_Area": display_policy.iloc[0]["Customer_Area"],

            "Channel_Type": display_policy.iloc[0]["Channel_Type"],

            "Make": display_policy.iloc[0]["Make"],

            "Model": display_policy.iloc[0]["Model"],

            "Premium": display_policy.iloc[0]["Premium"],

            "NCB": renewal["NCB"],

            "Claim_Count": display_policy.iloc[0]["Claim_Count"],

            "Renewal_Probability": probability,

            "Priority": assign_priority(probability)

        }

        results.append(output)

    return pd.DataFrame(results), missing_policies