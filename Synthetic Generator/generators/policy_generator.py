from pathlib import Path
import random
import pandas as pd
from datetime import timedelta
from datetime import datetime
from copy import deepcopy

from constants import CURRENT_YEAR
from constants import POLICY_STATUS

from constants import *


SIMULATION_DATE = datetime(2026, 7, 1)

CHANNEL_MASTER = pd.read_csv(
    Path("Synthetic Generator/data") / "channel_master.csv"
)

CUSTOMER_MASTER = pd.read_csv(
    Path("Synthetic Generator/data") / "customer_master.csv"
)

VEHICLE_MASTER = pd.read_csv(
    Path("Synthetic Generator/data") / "vehicle_master.csv"
)


POLICY_YEAR_WEIGHTS = {

    2016: 1,
    2017: 2,
    2018: 4,
    2019: 7,
    2020: 10,
    2021: 13,
    2022: 17,
    2023: 20,
    2024: 16,
    2025: 10
}


def generate_policy_number(index):
    return f"POL{10000 + index}"

def generate_policy_id(index):
    return f"PID{10000 + index}"

# Makes sure that IMD assigned to the customer is in their vicinity

def assign_imd(customer): 

    # Filter IMDs eligible to operate in the same district
    eligible_imds = CHANNEL_MASTER[
        CHANNEL_MASTER["District"] == customer["District"]
    ]

    if eligible_imds.empty:
        eligible_imds = CHANNEL_MASTER

    selected_imd = eligible_imds.sample(
        n = 1,
        weights = "Portfolio_Size"
    ).iloc[0]

    return selected_imd

# Function to generate the initial Risk Inspection Date (RID) 

def generate_initial_rid(Vehicle_First_Registration_Date,Year_Onboarded):

    earliest_possible_rid = max(Vehicle_First_Registration_Date,Year_Onboarded)

    lastest_possible_rid = datetime(2025,12,31)

    available_days = (lastest_possible_rid - earliest_possible_rid).days

    if available_days <= 0:
        return lastest_possible_rid
    
    random_offset = random.randint(0,available_days)

    return (earliest_possible_rid + timedelta(days = random_offset))

# Function to generate the Risk Expiration Date (RED)

def generate_red(rid):
    return rid + timedelta(days = 364)

# Function to generate the policy with vehicle as its input

def generate_initial_policy(vehicle,customer,policy_number,policy_id):
   
    imd = assign_imd(customer)

    rid = generate_initial_rid(
        pd.to_datetime(vehicle["Vehicle_First_Registration_Date"]),
        pd.to_datetime(imd["Year_Onboarded"])
        )
    
    red = generate_red(rid)

    policy_status = "Active"

    premium = round(vehicle["IDV"] * random.uniform(0.018,0.032),2)

    policy = {

        "Policy_ID": policy_id,

        "Policy_Number": policy_number,

        "Customer_ID": customer["Customer_ID"],

        "Vehicle_ID": vehicle["Vehicle_ID"],

        "IMD_Code": imd["IMD_Code"],

        "RID": rid,

        "RED": red,
        
        "IDV": vehicle["IDV"],

        "Policy_Tenure": 1,

        "Policy_Term": 365,

        "Policy_Status": policy_status

    }

    return policy


def should_renew(policy):                       # WILL BE UPDATED LATER

    return True


def generate_policy_chain(initial_policy):

    policies = []

    current_policy = deepcopy(initial_policy)

    policies.append(current_policy)

    while True:

        next_policy = deepcopy(current_policy)

        next_policy["RID"] = (
            next_policy["RID"] + timedelta(days=365)
        )

        if next_policy ["RID"] > SIMULATION_DATE:
            break

        if not should_renew(current_policy):
            break

        next_policy["RED"] = (
            current_policy["RED"] + timedelta(days=365)
        )

        next_policy["Policy_Tenure"] += 1
        
        next_policy["Policy_Status"] = "Active"

        policies.append(next_policy)

        current_policy = next_policy

    return policies
        
    

def generate_policy_history():

    policies = []

    policy_number_index = 0
    policy_id_index = 0

    for _, vehicle in VEHICLE_MASTER.iterrows():

        customer = CUSTOMER_MASTER[
            CUSTOMER_MASTER["Customer_ID"] == vehicle["Customer_ID" ]
        ].iloc[0]

        initial_policy = generate_initial_policy(
            vehicle,customer,generate_policy_number(policy_number_index),generate_policy_id(policy_id_index)
        )

        policy_chain = generate_policy_chain(initial_policy)

        for policy in policy_chain:
            policy["Policy_ID"] = generate_policy_id(policy_id_index)

            policies.append(policy)

            policy_id_index += 1
            policy_number_index += 1


    df_policies = pd.DataFrame(policies)

    output_dir = Path("Synthetic Generator/data")
    output_dir.mkdir(exist_ok = True)

    output_file = output_dir / "policy_history.csv"

    df_policies.to_csv(output_file, index = False)

    print(f"Saved {len(df_policies)} policies to {output_file}")

    return df_policies


if __name__ == "__main__":

    df_policies = generate_policy_history()

    # Display settings
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    print("\nFirst 10 Policies:\n")
    print(df_policies.head(10).to_string(index=False))

    print("\nDataset Shape:", df_policies.shape)

    print("\nUnique Policy IDs:",
          df_policies["Policy_ID"].is_unique)

    print("Unique Policy Numbers:",
          df_policies["Policy_Number"].is_unique)

    print("Unique Vehicle IDs:",
          df_policies["Vehicle_ID"].nunique())

    print("Unique Customers:",
          df_policies["Customer_ID"].nunique())

    print("\nPolicy Status Distribution:\n")
    print(df_policies["Policy_Status"].value_counts())

    print("\nRID Range:")
    print(df_policies["RID"].min(), "to", df_policies["RID"].max())


if __name__ == "__main__":

    df_policies = generate_policy_history()

    print(df_policies.head())


