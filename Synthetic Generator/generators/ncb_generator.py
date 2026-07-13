from pathlib import Path
import pandas as pd

from constants import NCB_STEPS

POLICY_PATH = Path("Synthetic Generator/data/policy_history.csv")

CLAIM_PATH = Path("Synthetic Generator/data/claim_history.csv")

POLICY_HISTORY = pd.read_csv(POLICY_PATH)

CLAIM_HISTORY = pd.read_csv(CLAIM_PATH)

claim_summary = (CLAIM_HISTORY.groupby("Policy_ID").size().rename("Claim_Count").reset_index())


POLICY_HISTORY = POLICY_HISTORY.drop(
    columns = ["Claim_Count","NCB"],
    errors = "ignore"
)

POLICY_HISTORY = POLICY_HISTORY.merge(
    claim_summary,
    on = "Policy_ID",
    how = "left"
)

POLICY_HISTORY["Claim_Count"] = (POLICY_HISTORY["Claim_Count"].fillna(0).astype(int))

POLICY_HISTORY["NCB"] = 0

def update_ncb():

    for policy_number, group in POLICY_HISTORY.groupby("Policy_Number"):
        group = group.sort_values("Policy_Tenure")

        current_step = 0

        for index , row in group.iterrows():

            POLICY_HISTORY.loc[index, "NCB"] = NCB_STEPS[current_step]

            if row["Claim_Count"] > 0:

                current_step = 0

            else:

                current_step = min(
                    current_step + 1,
                    len(NCB_STEPS) - 1
                )

    POLICY_HISTORY.to_csv(
        POLICY_PATH,
        index = False
    )

    print("Updated policy_history.csv with updated NCB values.")


# if __name__ == "__main__":

#     update_ncb()

#     df = pd.read_csv(POLICY_PATH)

#     print(df[
#         [
#             "Policy_Number",
#             "Policy_Tenure",
#             "Claim_Count",
#             "NCB"
#         ]
#     ].head(30))
        