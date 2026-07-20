from pathlib import Path
import pandas as pd

# ==========================================================
# Paths
# ==========================================================

ROOT = Path(__file__).resolve().parent.parent

MODEL_DATASET = (
    ROOT /
    "data" /
    "model_dataset.csv"
)

OUTPUT_FOLDER = (
    ROOT /
    "test_files"
)

OUTPUT_FOLDER.mkdir(exist_ok=True)

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv(
    MODEL_DATASET,
    parse_dates=["RID", "RED"]
)

# ==========================================================
# Available Renewal Months
# ==========================================================

# ==========================================================
# Available Renewal Months (Latest Year Only)
# ==========================================================

latest_year = df["RED"].dt.year.max()

df_current = df[
    df["RED"].dt.year == latest_year
]

available = (
    df_current.assign(
        Renewal_Month=df_current["RED"].dt.to_period("M")
    )
    .groupby("Renewal_Month")
    .size()
    .reset_index(name="Policies")
    .sort_values("Renewal_Month")
)

print("\n==============================================")
print("Available Renewal Months")
print("==============================================\n")

for i, row in available.iterrows():

    month = row["Renewal_Month"].strftime("%B %Y")

    print(
        f"{i+1}. {month} ({row['Policies']} policies)"
    )

# ==========================================================
# User Selection
# ==========================================================

while True:

    try:

        choice = int(
            input(
                "\nSelect Month Number: "
            )
        )

        if 1 <= choice <= len(available):

            break

        print("Invalid selection.")

    except ValueError:

        print("Enter a valid number.")

selected_period = available.iloc[
    choice - 1
]["Renewal_Month"]

# ==========================================================
# Filter Policies
# ==========================================================

renewals = df[
    df["RED"].dt.to_period("M") == selected_period
].copy()

# ==========================================================
# Columns for Renewal Manager
# ==========================================================

required_columns = [

    "Policy_Number",

    "Polciy_Holder_Name",

    "Make",

    "Model",

    "IMD_Code",

    "RID",

    "RED",

    "NCB"

]

existing_columns = [

    c

    for c in required_columns

    if c in renewals.columns

]

renewals = renewals[
    existing_columns
]

# ==========================================================
# Sort
# ==========================================================

renewals = renewals.sort_values(
    "RED"
)

# ==========================================================
# Save
# ==========================================================

filename = (
    f"Renewal_List_"
    f"{selected_period.year}_"
    f"{selected_period.month:02d}.xlsx"
)

output_path = OUTPUT_FOLDER / filename

renewals.to_excel(
    output_path,
    index=False
)

# ==========================================================
# Summary
# ==========================================================

print("\n==============================================")
print("Renewal Sheet Generated Successfully")
print("==============================================")

print(f"\nFile Name : {filename}")

print(
    f"Policies  : {len(renewals)}"
)

print(
    f"Period    : {selected_period.strftime('%B %Y')}"
)

print(
    f"Location  : {output_path}"
)

print("\nDone.\n")