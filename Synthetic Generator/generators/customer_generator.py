import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

random.seed(42)
Faker.seed(42)

# Customer ID generator (Sequential)

def generate_customer_id(index):
    return f"CUST{10000 + index}"



GENDER_DISTRIBUTION = {
    "Male": 0.72,
    "Female": .28
}

def generate_gender():
    return random.choices(
        population = list(GENDER_DISTRIBUTION.keys()),
        weights = list(GENDER_DISTRIBUTION.values()),
        k = 1
    )[0]



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

for i in range(10):
    print(generate_mobile_number())

    """
    PENDING FUNCTION TO CODE HERE

    CUSTOMER_AREA_GENERATOR --> Will complete later as the link between IMD's location and
    customer location is highly relevent
    
    
    """