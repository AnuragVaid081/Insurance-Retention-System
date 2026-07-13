from pathlib import Path
import pandas as pd

# ==========================
# Paths
# ==========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "Synthetic Generator" / "data"

INPUT_PATH = DATA_DIR / "renewal_training_dataset.csv"

OUTPUT_PATH = DATA_DIR / "model_dataset.csv"

def build_model_dataset():

    dataset = pd.read_csv(INPUT_PATH)
    
    dataset["RID"] = pd.to_datetime(dataset["RID"])
    dataset["RED"] = pd.to_datetime(dataset["RED"])

    dataset["Manufacturing_Year"] = pd.to_numeric(
    dataset["Manufacturing_Year"],
    errors="coerce"
)

    dataset["Year_Onboarded"] = pd.to_datetime(
    dataset["Year_Onboarded"]
)
    


    dataset = dataset.fillna(0)
    # ==========================================
    # Rename Columns
    # ==========================================

    dataset = dataset.rename(
        columns={
            "IDV_x": "IDV",
            "Claim_Amount": "Total_Claim_Amount",
            "District_x": "District"
        }
    )

    # ==========================================
    # Drop Duplicate Columns
    # ==========================================

    dataset = dataset.drop(
        columns= [
            "IDV_y",
            "Customer_ID_y",
            "District_y"
        ],
        errors= "ignore"
    )

    # ==========================================
    # Drop Unnecessary Columns
    # ==========================================

    dataset = dataset.drop(
        columns= [
            # IDs
            "Policy_ID",
            "Customer_ID_x",
            "Vehicle_ID",
            "IMD_Code",

            # Personal Information
            "Polciy_Holder_Name",
            "Mobile_Number",

            # Registration Details
            "Registration_Number",

            # Operational Fields
            "Policy_Status",
            "Entity_Name",
            "Active_Status",

            # Channel Area
            "Area",

            # Policy term (is same for everyone i.e 1 year)
            "Policy_Term"
        ],
        errors= "ignore"
    )

    dataset = dataset.sort_values(["Policy_Number","Policy_Tenure"])

    dataset["Previous_Premium"] = (dataset.groupby("Policy_Number")["Premium"].shift(1))

    dataset["Premium_Change"] = (
        dataset["Premium"] - dataset["Previous_Premium"]
    ).round(4)

    dataset["Premium_Change_Percentage"] = (
        dataset["Premium_Change"] / dataset["Previous_Premium"]
    )*100

    dataset["Premium_Change_Percentage"] = (
        dataset["Premium_Change_Percentage"].round(4).fillna(0)
    )

    dataset["Previous_NCB"] = (
        dataset
        .groupby("Policy_Number")["NCB"]
        .shift(1)
        .fillna(0)
    )

    dataset["Previous_Claim_Count"] = (
        dataset
        .groupby("Policy_Number")["Claim_Count"]
        .shift(1)
        .fillna(0)
    )

    dataset["RID"] = pd.to_datetime(dataset["RID"])

    dataset["Vehicle_Age_At_Renewal"] = (
        dataset["RID"].dt.year - dataset["Manufacturing_Year"]
    )

    dataset["Years_With_Channel"] = (
        dataset["RID"].dt.year - dataset["Year_Onboarded"].dt.year
    )

    dataset["Years_With_Channel"] = (
        dataset["Years_With_Channel"].clip(lower=0)
    )

    dataset["Premium_to_IDV_Ratio"] = (
    dataset["Premium"] /
    dataset["IDV"]
    ).round(4)

    dataset = dataset.drop(
    columns=[
        "Year_Onboarded",
        "Manufacturing_Year",
        "Vehicle_Age_At_Renewal",
        "District",
        "RTO"
        ],
    errors="ignore"
)

    print(dataset[["RID", "Years_With_Channel"]].head(20))

    print(dataset["Years_With_Channel"].describe())

    dataset["Previous_Premium"] = dataset["Previous_Premium"].fillna(0)

    dataset["Premium_Change"] = dataset["Premium_Change"].fillna(0)

    # ==========================================
    # Save
    # ==========================================

    dataset.to_csv(
        OUTPUT_PATH,
        index= False
    )

    print(f"Saved {len(dataset)} rows to {OUTPUT_PATH}")

    return dataset




if __name__ == "__main__":

    df = build_model_dataset()

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)

    print(df.head())


