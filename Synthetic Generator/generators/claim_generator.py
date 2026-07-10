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

def generate_claim_date(rid,red):

    rid = pd.to_datetime(rid)
    red = pd.to_datetime(red)

    days = (red - rid).days

    offset = random.randint(0,days)

    return rid + timedelta(days = offset)

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

def generate_claim(policy, claim_id):

    severity = generate_claim_severity()

    claim = {

        "Claim_ID": claim_id,

        "Policy_ID": policy["Policy_ID"],

        "Claim_Date": generate_claim_date(policy["RID"],policy["RED"]),

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


def generate_claim_history():

    claims = []

    claim_index = 0

    for _, policy in POLICY_HISTORY.iterrows():

        claim_count = generate_claim_count()

        for _ in range(claim_count):

            claim = generate_claim(
                policy , generate_claim_id(claim_index)
            )

            claims.append(claim)

            claim_index += 1

    df_claims = pd.DataFrame(claims)

    output_dir = Path("Synthetic Generator/data")
    output_dir.mkdir(exist_ok= True)

    output_file = output_dir / "claim_history.csv"

    df_claims.to_csv(output_file, index = False)


    print(f"Saved {len(df_claims)} claims to {output_file}")

    return df_claims


# TEST BLOCK

if __name__ == "__main__":

    df_claims = generate_claim_history()

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)

    print(df_claims.head(10).to_string(index=False))

    print("\nDataset Shape:", df_claims.shape)

    print("\nUnique Claim IDs:",
          df_claims["Claim_ID"].is_unique)

    print("\nPolicies With Claims:",
          df_claims["Policy_ID"].nunique())

    print("\nClaim Severity Distribution:\n")
    print(df_claims["Claim_Severity"].value_counts())


print(df_claims["Claim_ID"].is_unique)