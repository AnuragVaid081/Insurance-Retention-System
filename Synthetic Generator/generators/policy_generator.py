from pathlib import Path
import random
import pandas as pd
from datetime import timedelta
from datetime import datetime

from constants import CURRENT_YEAR

from constants import *

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

def assign_imd():

    return CHANNEL_MASTER.sample(
        n = 1,
        weights = "Portfolio_Size"
    ).iloc[0]

def generate_initial_rid(onboarding_year):

  start_date = onboarding_year