import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

random.seed(42)
Faker.seed(42)

from constants import AREA_INFO 

# Customer ID generator (Sequential)

def generate_customer_id(index):
    return f"CUST{10000 + index}"

USED_CUSTOMER_NAMES = set()

def generate_names():
    while True:
        name = fake.name()

        if name not in USED_CUSTOMER_NAMES:
            USED_CUSTOMER_NAMES.add(name)
            return name

"""
Generates Realistic Indian names with no duplication 
"""

USED_CUSTOMER_PHONE_NUMBERS = set()


def generate_mobile_number():
    while True:
        first_digit = random.choices(["6","7","8","9"])[0]

        remaining_digits = "".join(random.choices("0123456789",k=9))

        mobile_number = first_digit + remaining_digits

        if mobile_number not in USED_CUSTOMER_PHONE_NUMBERS:
            USED_CUSTOMER_PHONE_NUMBERS.add(mobile_number)
            return mobile_number

# for i in range(10):
#     print(generate_mobile_number())

def generate_customer_area():

    return random.choices(
        population = list(AREA_INFO.keys()),
        weights = [area["weight"] for area in AREA_INFO.values()],
        k = 1
    )[0]

def generate_customers(n_customers):

    customers = []

    for i in range(n_customers):

        area = generate_customer_area()
        district = AREA_INFO[area]["district"]

        customer = {
            "Customer_ID": generate_customer_id(i),
            "Polciy_Holder_Name": generate_names(),
            "Mobile_Number": generate_mobile_number(),
            "Customer_Area": area,
            "District": district
        }

        customers.append(customer)
    df_customers = pd.DataFrame(customers)

    output_dir = Path("Synthetic Generator/data")
    output_dir.mkdir(exist_ok = True)

    output_file = output_dir / "customer_master.csv"

    df_customers.to_csv(output_file, index = False)

    print(f"Saved {len(df_customers)} customers to {output_file}")

    return df_customers


df_customers = generate_customers(1000)
