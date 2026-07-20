from pathlib import Path
import pandas as pd

from constants import (
    BASE_PREMIUM_RATE,
    CLAIM_LOADING
) 

POLCIY_PATH = Path("Synthetic_Generator/data/policy_history.csv")

def calculate_premium(row):

    base_preemium = row["IDV"] * BASE_PREMIUM_RATE

    claim_count =  min(row["Claim_Count"], 3)

    loading_factor = CLAIM_LOADING[claim_count]

    premium = (
        base_preemium * loading_factor * (1 - row["NCB"]/100)
    )

    return round(premium,2)


def update_premium():

    policy_history = pd.read_csv(POLCIY_PATH)

    policy_history = policy_history.drop(
        columns = ["Premium"],
        errors = "ignore"
    )

    policy_history["Premium"] = (
        policy_history.apply(calculate_premium, axis = 1)
    )

    policy_history.to_csv(
        POLCIY_PATH,
        index = False
    )

    print("Policy History updated with premium succesfully")

    return policy_history

if __name__ == "__main__":

    df = update_premium()

    pd.set_option("display.max_columns",None)
    pd.set_option("display.width",None)

    print(
        df[
            [
                "Policy_Number",
                "Policy_Tenure",
                "IDV",
                "Claim_Count",
                "NCB",
                "Premium"
            ]
        ].head(30).to_string(index = False)
    )