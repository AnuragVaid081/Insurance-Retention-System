from pathlib import Path
from datetime import timedelta
import random
import pandas as pd

from constants import *


POLICY_HISTORY = pd.read_csv("Synthetic Generator/data/policy_history.csv")

CLAIM_COUNT_DISTRIBUTION = {
    0: 82,
    1: 15,
    2: 2.5,
    3: 0.5
}

CLAIM_SEVERITY_DISTRIBUTION = {
    "Minor": 70,
    "Moderate": 25,
    "Major": 5
}

CLAIM_SEVERITY_PERCENTAGE = {

    "Minor": (0.05, 0.15),

    "Moderate": (0.15, 0.35),

    "Major": (0.35, 0.70)

}


# Helper Functions

def generate_claim_id(index):

    return f"CLM{10000 + index}"

def generate_claim_count():

    return random.choices(
        population = list(CLAIM_COUNT_DISTRIBUTION.keys()),
        weights = list(CLAIM_COUNT_DISTRIBUTION.values()),
        k = 1
    )[0]

def generate_claim_dates(rid, red, claim_count):

    rid = pd.to_datetime(rid)
    red = pd.to_datetime(red)

    total_days = (red - rid).days

    if claim_count == 0:
        return []
    
    #Cannot have more unique dates than the ones in the policy period
    claim_count = min(claim_count, total_days + 1)

    random_offsets = sorted(
        random.sample(
            range(total_days + 1),
            claim_count
        )
    )          

    return [
        rid + timedelta(days =offset)
        for offset in random_offsets
    ]

def generate_claim_severity():

    return random.choices(
        population = list(CLAIM_SEVERITY_DISTRIBUTION.keys()),
        weights = list(CLAIM_SEVERITY_DISTRIBUTION.values()),
        k = 1
    )[0]


def generate_claim_amount(idv, severity):

    lower, upper =  CLAIM_SEVERITY_PERCENTAGE[severity]

    claim_amount = idv * random.uniform(lower,upper)

    return round (claim_amount,2)

# for _ in range(10):

#     severity = generate_claim_severity()

#     amount = generate_claim_amount(
#         800000,
#         severity
#     )

#     print(severity, amount)

def generate_claim(policy, claim_id, claim_date):

    severity = generate_claim_severity()

    claim = {

        "Claim_ID": claim_id,

        "Policy_ID": policy["Policy_ID"],

        "Claim_Date": claim_date,

        "Claim_Severity": severity,

        "Claim_Amount": generate_claim_amount(policy["IDV"],severity),

    }
    return claim


# policy = POLICY_HISTORY.iloc[0]

# claim = generate_claim(
#     policy,
#     generate_claim_id(0)
# )

# print(claim)

# def update_policy_claim_summary(df_policies, df_claims):
#     claim_summary = (

#     df_claims

#     .groupby("Policy_ID")

#     .agg({

#         "Claim_ID": "count",

#         "Claim_Amount": "sum"

#     })

#     .rename(columns={

#         "Claim_ID": "Claim_Count"

#     })

# )
    
#     df_policies = df_policies.merge(

#     claim_summary,

#     on="Policy_ID",

#     how="left"

# )
    
#     df_policies["Claim_Count"] = (

#     df_policies["Claim_Count"]

#     .fillna(0)

#     .astype(int)

# )
#     df_policies["Claim_Amount"] = (

#     df_policies["Claim_Amount"]

#     .fillna(0)

#     .round(2)

# )
#     policy_path = "Synthetic Generator/data/policy_history.csv"
#     df_policies.to_csv(
#     policy_path,
#     index=False
# )
#     return df_policies


def generate_claim_history():

    claims = []

    claim_index = 0

    for _, policy in POLICY_HISTORY.iterrows():

        claim_count = generate_claim_count()

        claim_dates = generate_claim_dates(policy["RID"], policy["RED"],claim_count)

        for claim_date in claim_dates:
            
            claim = generate_claim(policy,generate_claim_id(claim_index),claim_date)

            claims.append(claim)

            claim_index += 1

    df_claims = pd.DataFrame(claims)

    output_dir = Path("Synthetic Generator/data")
    output_dir.mkdir(exist_ok= True)

    output_file = output_dir / "claim_history.csv"

    df_claims.to_csv(output_file, index = False)

    policy_path = "Synthetic Generator/data/policy_history.csv"

    df_policies = pd.read_csv(policy_path)

    # df_policies = update_policy_claim_summary(
    #     df_policies,
    #     df_claims
    # )
    print("Updated policy_history.csv with the claim summary")


    print(f"Saved {len(df_claims)} claims to {output_file}")

    return df_claims




# TEST BLOCK

if __name__ == "__main__":

    df_claims = generate_claim_history()

    # Display Settings
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    print("\nFirst 10 Claims:\n")
    print(df_claims.head(10).to_string(index=False))

    print("\nDataset Shape:", df_claims.shape)

    print("\nUnique Claim IDs:",
          df_claims["Claim_ID"].is_unique)

    print("Policies With Claims:",
          df_claims["Policy_ID"].nunique())

    print("\nClaim Count by Severity:\n")
    print(df_claims["Claim_Severity"].value_counts())

    # ---------------------------
    # Validation Checks
    # ---------------------------

    merged = df_claims.merge(
        POLICY_HISTORY[
            ["Policy_ID", "RID", "RED"]
        ],
        on="Policy_ID"
    )

    merged["Claim_Date"] = pd.to_datetime(merged["Claim_Date"])
    merged["RID"] = pd.to_datetime(merged["RID"])
    merged["RED"] = pd.to_datetime(merged["RED"])

    print(
        "\nAll Claim Dates Valid:",
        (
            (merged["Claim_Date"] >= merged["RID"]) &
            (merged["Claim_Date"] <= merged["RED"])
        ).all()
    )

    duplicate_dates = (
        df_claims
        .groupby(["Policy_ID", "Claim_Date"])
        .size()
        .max()
    )

    print(
        "Maximum Claims On Same Date For One Policy:",
        duplicate_dates
    )


# print(df_claims["Claim_ID"].is_unique)