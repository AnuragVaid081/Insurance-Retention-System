from pathlib import Path
import pandas as pd



POLICY_HISTORY = pd.read_csv(
    Path("Synthetic Generator/data/policy_history.csv")
)

CLAIM_HISTORY = pd.read_csv(
    Path("Synthetic Generator/data/claim_history.csv")
)

NCB_PROGRESSION = {
    1: 0,
    2: 20,
    3: 25,
    4: 35,
    5: 45,
    6: 50
}

claim_summary = (CLAIM_HISTORY.groupby("Policy_ID").size().rename("Claim_Count"))


POLICY_HISTORY = POLICY_HISTORY.merge(claim_summary,on="Policy_ID",how="left")

POLICY_HISTORY["Claim_Count"] = (POLICY_HISTORY["Claim_Count"].fillna(0).astype(int))

def calculate_ncb(policy):

    if policy["Claim_Count"] > 0:
        return 0
    
    tenure = min(policy["Policy_Tenure"],6)

    return NCB_PROGRESSION[tenure]



for _, policy in POLICY_HISTORY.head(30).iterrows():

    print(

        policy["Policy_Tenure"],

        policy["Claim_Count"],

        calculate_ncb(policy)

    )