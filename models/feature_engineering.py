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
            "Area"
        ],
        errors= "ignore"
    )

    # ==========================================
    # Save
    # ==========================================

    dataset.to_csv(
        OUTPUT_PATH,
        index= False
    )

    print(f"Saved {len(dataset)} rows to {OUTPUT_PATH}")

    return dataset


# if __name__ == "__main__":

#     df = build_model_dataset()

#     pd.set_option("display.max_columns", None)
#     pd.set_option("display.width", None)

#     print(df.head())


