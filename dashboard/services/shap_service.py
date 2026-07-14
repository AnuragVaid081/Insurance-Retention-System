from pathlib import Path
import sys

import joblib
import pandas as pd
import shap

# ==========================================================
# Paths
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "models"))

from models.training_features import MODEL_FEATURES

MODEL_DIR = ROOT / "models" / "saved_models"

DISPLAY_NAMES = {

    "remainder__NCB": "No Claim Bonus",

    "remainder__Premium": "Premium",

    "remainder__Policy_Tenure": "Renewal Number",

    "remainder__Vehicle_Age": "Vehicle Age",

    "remainder__Claim_Count": "Claim Count",

    "remainder__Previous_NCB": "Previous NCB",

    "remainder__Years_With_Channel": "Years With Channel",

    "remainder__Total_Claim_Amount": "Claim Amount",

    "categorical__Customer_Area": "Customer Area",

    "categorical__Make": "Vehicle Make",

    "categorical__Model": "Vehicle Model",

    "categorical__Fuel_Type": "Fuel Type",

    "categorical__Vehicle_Type": "Vehicle Type",

    "categorical__Channel_Type": "Sales Channel"
}

# ==========================================================
# Load Objects
# ==========================================================

preprocessor = joblib.load(
    MODEL_DIR / "preprocessor.pkl"
)

rf_model = joblib.load(
    MODEL_DIR / "random_forest_model.pkl"
)

explainer = shap.TreeExplainer(rf_model)

# Cache feature names
FEATURE_NAMES = preprocessor.get_feature_names_out()


# ==========================================================
# Explain Prediction
# ==========================================================

def explain_prediction(row):

    # Convert Series to DataFrame
    row_df = pd.DataFrame([row])

    # Keep only model features
    row_df = row_df[MODEL_FEATURES]

    # Apply preprocessing
    X_processed = preprocessor.transform(row_df)

    # Generate SHAP values
    shap_result = explainer(X_processed)

    # ---------- Handle SHAP API differences ----------
    if hasattr(shap_result, "values"):
        values = shap_result.values

        # Binary classifier
        if values.ndim == 3:
            values = values[0, :, 1]

        elif values.ndim == 2:
            values = values[0]

        else:
            values = values.flatten()

    else:
        # Older SHAP fallback
        values = explainer.shap_values(X_processed)

        if isinstance(values, list):
            values = values[1][0]
        else:
            values = values[0]

    explanation = pd.DataFrame(
        {
            "Feature": FEATURE_NAMES,
            "Contribution": values,
        }
    )

    explanation["Impact"] = explanation["Contribution"].abs()

    explanation = (
        explanation
        .sort_values("Impact", ascending=False)
        .drop(columns="Impact")
        .reset_index(drop=True)
    )

    explanation["Feature"] = (
    explanation["Feature"]
    .map(DISPLAY_NAMES)
    .fillna(explanation["Feature"])
)

    return explanation