import random
from pathlib import Path
import string

import pandas as pd
from faker import Faker

from datetime import datetime, timedelta

from constants import AREA_INFO
from constants import CURRENT_YEAR

fake = Faker("en_IN")

random.seed(42)
Faker.seed(42)


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)
pd.set_option("display.expand_frame_repr", False)


CUSTOMER_MASTER = pd.read_csv(Path("Synthetic_Generator/data")/"customer_master.csv")

VEHICLES_PER_CUSTOMER = {
    1: 0.78,
    2: 0.17,
    3: 0.04,
    4: 0.01
}



VEHICLE_CATALOG = {

# MARUTI SUZUKI

    "Maruti Suzuki": {

        "Swift": {
            "type": "Hatchback",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1197,
            "ex_showroom_price": (400000, 800000)
        },

        "Baleno": {
            "type": "Hatchback",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1197,
            "ex_showroom_price": (500000, 900000)
        },

        "WagonR": {
            "type": "Hatchback",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1197,
            "ex_showroom_price": (350000, 750000)
        },

        "Brezza": {
            "type": "SUV",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1462,
            "ex_showroom_price": (700000, 1200000)
        }
    },

    # HYNDAI

    "Hyundai": {
        "Creta": {
        "type": "SUV",
        "fuel": ["Petrol", "Diesel"],
        "engine_cc": 1497,
        "ex_showroom_price": (900000, 1800000)
    },

        "Venue": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 1197,
            "ex_showroom_price": (700000, 1400000)
    },

        "i20": {
            "type": "Hatchback",
            "fuel": ["Petrol"],
            "engine_cc": 1197,
            "ex_showroom_price": (500000, 1000000)
    },

        "Verna": {
            "type": "Sedan",
            "fuel": ["Petrol"],
            "engine_cc": 1497,
            "ex_showroom_price": (800000, 1500000)
        }
    },

    # TATA

    "Tata": {
        "Nexon": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 1199,
            "ex_showroom_price": (700000, 1400000)
        },

        "Punch": {
            "type": "SUV",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1199,
            "ex_showroom_price": (600000, 1100000)
        },

        "Altroz": {
            "type": "Hatchback",
            "fuel": ["Petrol", "Diesel", "CNG"],
            "engine_cc": 1199,
            "ex_showroom_price": (600000, 1000000)
        },

        "Tiago": {
            "type": "Hatchback",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1199,
         "ex_showroom_price": (450000, 850000)
        },

        "Harrier": {
            "type": "SUV",
            "fuel": ["Diesel"],
            "engine_cc": 1956,
            "ex_showroom_price": (1400000, 2600000)
        }

    },

# MAHINDRA

    "Mahindra": {
   
        "Scorpio-N": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 2198,
            "ex_showroom_price": (1500000, 2800000)
        },

        "Scorpio Classic": {
            "type": "SUV",
            "fuel": ["Diesel"],
            "engine_cc": 2184,
            "ex_showroom_price": (1100000, 1900000)
        },

        "Thar": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 2184,
            "ex_showroom_price": (1200000, 2200000)
        },

        "XUV700": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 1999,
            "ex_showroom_price": (1800000, 3500000)
        },

        "Bolero": {
            "type": "SUV",
            "fuel": ["Diesel"],
            "engine_cc": 1493,
            "ex_showroom_price": (700000, 1200000)
        }
    },

# KIA

    "Kia": {
        "Seltos": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 1497,
            "ex_showroom_price": (1000000, 2200000)
        },

        "Sonet": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 1197,
            "ex_showroom_price": (700000, 1500000)
        },

        "Carens": {
            "type": "MPV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 1497,
            "ex_showroom_price": (1100000, 2200000)
        }
    },

# TOYOTA

    "Toyota":{
        "Innova Crysta": {
            "type": "MPV",
            "fuel": ["Diesel"],
            "engine_cc": 2393,
            "ex_showroom_price": (1600000, 2800000)
        },

        "Innova Hycross": {
            "type": "MPV",
            "fuel": ["Petrol", "Hybrid"],
            "engine_cc": 1987,
            "ex_showroom_price": (2200000, 3600000)
        },

        "Fortuner": {
            "type": "SUV",
            "fuel": ["Diesel", "Petrol"],
            "engine_cc": 2755,
            "ex_showroom_price": (3000000, 5500000)
        },

        "Glanza": {
            "type": "Hatchback",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1197,
            "ex_showroom_price": (600000, 1000000)
        }
    },

# HONDA

    "Honda": {

        "City": {
            "type": "Sedan",
            "fuel": ["Petrol"],
            "engine_cc": 1498,
            "ex_showroom_price": (900000, 1800000)
        },

        "Amaze": {
            "type": "Sedan",
            "fuel": ["Petrol"],
            "engine_cc": 1199,
            "ex_showroom_price": (600000, 1000000)
        },

        "Elevate": {
            "type": "SUV",
            "fuel": ["Petrol"],
            "engine_cc": 1498,
            "ex_showroom_price": (1100000, 1900000)
        }
    },
    
# RENAULT

    "Renault":{
        
        "Kwid": {
            "type": "Hatchback",
            "fuel": ["Petrol"],
            "engine_cc": 999,
            "ex_showroom_price": (300000, 600000)
        },

        "Kiger": {
            "type": "SUV",
            "fuel": ["Petrol"],
            "engine_cc": 999,
            "ex_showroom_price": (600000, 1100000)
        },

        "Triber": {
            "type": "MPV",
            "fuel": ["Petrol"],
            "engine_cc": 999,
            "ex_showroom_price": (550000, 1000000)
        }
    },
   


}

MAKE_DISTRIBUTION = {
    "Maruti Suzuki": 0.38,
    "Hyundai": 0.16,
    "Tata": 0.14,
    "Mahindra": 0.10,
    "Kia": 0.07,
    "Toyota": 0.06,
    "Honda": 0.05,
    "Renault": 0.04
}

MANUFACTURING_YEAR_WEIGHTS = {

    2025: 12,
    2024: 15,
    2023: 14,
    2022: 12,
    2021: 10,
    2020: 9,
    2019: 8,
    2018: 7,
    2017: 6,
    2016: 5,
    2015: 4,
    2014: 3,
    2013: 2,
    2012: 2,
    2011: 1,
    2010: 1
}

DEPRECIATION_RATE = {

    0: 0.05,   # < 1 year
    1: 0.15,
    2: 0.20,
    3: 0.30,
    4: 0.40,
    5: 0.50,
    6: 0.55,
    7: 0.60,
    8: 0.65,
    9: 0.70,
    10: 0.75
}


# HELPER FUNCTIONS

def generate_vehicle_id(index):
    return f"VEH{10000 + index}"

def generate_make_model():

    make = random.choices(
        population = list(MAKE_DISTRIBUTION.keys()),
        weights = list(MAKE_DISTRIBUTION.values()),
        k = 1
    )[0]

    model = random.choice(
        list(VEHICLE_CATALOG[make].keys())
    ) 

    vehicle = VEHICLE_CATALOG[make][model]

    return make, model, vehicle

"""
Generates the make and model of each vehcile consisting of their type, fuel type, engine_cc, IDV, as per the dictionary above 
in order to create a much realisitic dataset
"""

# Registration number generation

USED_REGISTRATION_NUMBER = set()

def generate_registration_number(customer_area):

    while True:

        rto = AREA_INFO[customer_area]["rto"]

        series = "".join(
            random.choices(string.ascii_uppercase,k=2)
        )

        number = random.randint(1000, 9999)

        registration_number =  f"{rto}{series}{number}"

        if registration_number not in USED_REGISTRATION_NUMBER:
            
            USED_REGISTRATION_NUMBER.add(registration_number)

            return registration_number,rto
        
# for area in [
#     "Gandhi Nagar",
#     "Kathua",
#     "Rajouri",
#     "Samba"
# ]:

#     registration, rto = generate_registration_number(area)

#     print(area)
#     print(registration)
#     print(rto)
#     print()

def generate_manufacturing_year():
    return random.choices(
        population = list(MANUFACTURING_YEAR_WEIGHTS.keys()),
        weights = list(MANUFACTURING_YEAR_WEIGHTS.values()),
        k = 1
    )[0]


# Function to generate the first registration year of the car

def generate_first_registration_year(manufacturing_year):

    month = random.randint(1,12)

    day = random.randint(1,28)

    manufacturing_date = datetime(
        manufacturing_year,
        month,
        day
    )
    registration_delay = random.randint(0,365)

    first_registration_date = (
        manufacturing_date + timedelta(days = registration_delay)
    )
    return first_registration_date

# Fucntion to calculate the vehicle age

def calculate_vehicle_age(manufacturing_age):
    return CURRENT_YEAR - manufacturing_age

# Function to generate IDV for the vehicle

def generate_idv(vehicle,vehicle_age):

    base_price = random.randint(*vehicle["ex_showroom_price"])

    depreciation = DEPRECIATION_RATE.get(vehicle_age,0.75)

    idv = int(
        base_price * (1-depreciation)
    )

    return idv

# Function to generate the vehicle with the help of helper functuions above

def generate_vehicle(customer, vehicle_index):

    # Generate Vehcile ID
    vehicle_id = generate_vehicle_id(vehicle_index)

    # Generate Make, Model and Vehicle Specifications
    make, model, vehicle = generate_make_model() 

    # Generate Registration number and RTO
    registration_number, rto = generate_registration_number(
        customer["Customer_Area"]
    )
   
    # Manufacturing Year
    manufacturing_year = generate_manufacturing_year()

    # Vehicle Age
    vehicle_age = calculate_vehicle_age(
        manufacturing_year
    )

    vehicle_first_registration_year = generate_first_registration_year(manufacturing_year) 


    # Fuel Type
    fuel_type = random.choice(vehicle["fuel"])

    #IDV
    idv = generate_idv(vehicle, vehicle_age)

    # Create Vehicle Record

    vehcile_record = {
        "Vehicle_ID": vehicle_id,

        "Customer_ID": customer["Customer_ID"],

        "Registration_Number": registration_number,

        "RTO": rto,

        "Make": make,

        "Model": model,

        "Vehicle_Type": vehicle["type"],

        "Fuel_Type": fuel_type,

        "Engine_CC": vehicle["engine_cc"],

        "Manufacturing_Year": manufacturing_year,

        "Vehicle_First_Registration_Date": vehicle_first_registration_year,

        "Vehicle_Age": vehicle_age,

        "IDV": idv
    }
    return vehcile_record


def generate_vehicle_count():

    return random.choices(
        population = list(VEHICLES_PER_CUSTOMER.keys()),
        weights = list(VEHICLES_PER_CUSTOMER.values()),
        k = 1,
    )[0]

def generate_vehicle_master():

    vehicles = []

    vehicle_index = 0

    for _, customer in CUSTOMER_MASTER.iterrows():

        vehicle_count = generate_vehicle_count()

        for _ in range(vehicle_count):

            vehicle = generate_vehicle(
                customer,
                vehicle_index
            )

            vehicles.append(vehicle)

            vehicle_index +=1

    df_vehicles = pd.DataFrame(vehicles)


    output_dir = Path("Synthetic_Generator/data")
    output_dir.mkdir(exist_ok = True)

    output_file = output_dir / "vehicle_master.csv"

    df_vehicles.to_csv(
        output_file,
        index = False
    )

    print(
        f"Saved {len(df_vehicles)} vehicles to {output_file}"
    )

    return df_vehicles

df_vehicles = generate_vehicle_master()


   
# merged = df_vehicles.merge(
#     CUSTOMER_MASTER,
#     on="Customer_ID"
# )

# print(
#     merged[
#         ["Customer_Area",
#          "RTO",
#          "Registration_Number"]
#     ].head()
# )


if __name__ == "__main__":

    df_vehicles = generate_vehicle_master()

    print(df_vehicles.head())