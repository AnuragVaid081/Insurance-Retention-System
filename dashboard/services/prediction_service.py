from pathlib import Path

import joblib
import pandas as pd

from models.training_features import MODEL_FEATURES


# ==========================================================
# Paths
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

MASTER_DATABASE = (
    ROOT
    / "Synthetic_Generator"
    / "data"
    / "model_dataset.csv"
)

MODEL_PATH = (
    ROOT
    /"models"
    / "saved_models"
    / "random_forest.pkl"
)


# ==========================================================
# Load Model
# ==========================================================

model = joblib.load(MODEL_PATH)


# ==========================================================
# Load Master Database
# ==========================================================

def load_master_database():

    return pd.read_csv(
        MASTER_DATABASE,
        parse_dates=["RID", "RED"]
    )


# ==========================================================
# Retrieve Policy History
# ==========================================================

def get_policy_history(master_df, policy_number):

    history = master_df[
        master_df["Policy_Number"] == policy_number
    ]

    history = history.sort_values("RID")

    return history


# ==========================================================
# Build Prediction Dataset
# ==========================================================

def build_prediction_dataset(
    renewal_sheet,
    master_df
):

    prediction_rows = []

    missing_policies = []

    for _, renewal in renewal_sheet.iterrows():

        policy_number = renewal["Policy_Number"]

        history = get_policy_history(
            master_df,
            policy_number
        )

        if history.empty:

            missing_policies.append(policy_number)

            continue

        latest_record = (
            history
            .sort_values("RID")
            .iloc[-1]
        )

        prediction_rows.append(latest_record)

    prediction_df = pd.DataFrame(
        prediction_rows
    )

    print("Prediction DF Columns:")
    print(prediction_df.columns.tolist())
    return prediction_df, missing_policies

# ==========================================================
# Predict
# ==========================================================

def predict(prediction_df):

    X = prediction_df[MODEL_FEATURES]

    probabilities = model.predict_proba(X)[:, 1]

    results = prediction_df.copy()

    results["Renewal_Probability"] = (
        probabilities * 100
    ).round(2)

    return results


# ==========================================================
# Add Priority
# ==========================================================

def segment_predictions(results):

    def priority(prob):

        if prob >= 80:
            return "🟢 Low"

        elif prob >= 50:
            return "🟡 Medium"

        return "🔴 High"

    results["Priority"] = (
        results["Renewal_Probability"]
        .apply(priority)
    )

    return results


# ==========================================================
# Complete Pipeline
# ==========================================================

def predict_monthly_renewals(renewal_sheet):

    master_df = load_master_database()

    prediction_df, missing_policies = build_prediction_dataset(
        renewal_sheet,
        master_df
    )

    results = predict(prediction_df)

    results = segment_predictions(results)

    return results, missing_policies