from pathlib import Path
import pandas as pd
import random

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
import Synthetic_Generator.generators.constants

# ==========================
# Load Datasets
# ==========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "Synthetic_Generator" / "data"


CHANNEL_MASTER = pd.read_csv(DATA_DIR / "channel_master.csv")

CUSTOMER_MASTER = pd.read_csv(DATA_DIR / "customer_master.csv")

VEHICLE_MASTER = pd.read_csv(DATA_DIR / "vehicle_master.csv")

POLICY_HISTORY = pd.read_csv(DATA_DIR / "policy_history.csv")


# ==========================
# Merge Policy + Customer
# ==========================


dataset = POLICY_HISTORY.merge(
    CUSTOMER_MASTER,
    on = "Customer_ID",
    how= "left",
)

# ==========================
# Merge Vehicle
# ==========================

dataset = dataset.merge(
    VEHICLE_MASTER,
    on = "Vehicle_ID",
    how = "left",
)

# ==========================
# Merge Channel
# ==========================

dataset = dataset.merge(
    CHANNEL_MASTER,
    on = "IMD_Code",
    how = "left",
)

# ==========================
# Create Target Variable
# ==========================

dataset["Renewed"] = 0

for policy_number, group in dataset.groupby("Policy_Number"):

    group = group.sort_values("Policy_Tenure")

    renewed_rows = group.index[:-1]

    dataset.loc[renewed_rows,"Renewed"] = 1


    def assign_remark(row):
        if row["Renewed"] == 1:
            return random.choice(Synthetic_Generator.generators.constants.POSITIVE_REMARKS)

        if row["Claim_Count"] > 2:
            return "Claim experience poor"

        if row["Premium"] > 25000:
            return "Premium too high"

        return random.choice(Synthetic_Generator.generators.constants.NEGATIVE_REMARKS)

    dataset["Last_Remark"] = dataset.apply(assign_remark, axis=1)

# ==========================
# Sort Dataset 
# ==========================

output_dir = DATA_DIR
output_dir.mkdir(exist_ok= True)

output_file = output_dir / "renewal_training_dataset.csv"

dataset.to_csv(output_file, index = False)

print(f"Saved {len(dataset)} rows to {output_file}")


