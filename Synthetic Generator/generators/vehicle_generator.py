import random
from pathlib import Path
import string

import pandas as pd
from faker import Faker

from constants import AREA_INFO

fake = Faker("en_IN")

random.seed(42)
Faker.seed(42)


CUSTOMER_MASTER = pd.read_csv(Path("Synthetic Generator/data")/"customer_master.csv")

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
            "idv": (400000, 800000)
        },

        "Baleno": {
            "type": "Hatchback",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1197,
            "idv": (500000, 900000)
        },

        "WagonR": {
            "type": "Hatchback",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1197,
            "idv": (350000, 750000)
        },

        "Brezza": {
            "type": "SUV",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1462,
            "idv": (700000, 1200000)
        }
    },

    # HYNDAI

    "Hyundai": {
        "Creta": {
        "type": "SUV",
        "fuel": ["Petrol", "Diesel"],
        "engine_cc": 1497,
        "idv": (900000, 1800000)
    },

        "Venue": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 1197,
            "idv": (700000, 1400000)
    },

        "i20": {
            "type": "Hatchback",
            "fuel": ["Petrol"],
            "engine_cc": 1197,
            "idv": (500000, 1000000)
    },

        "Verna": {
            "type": "Sedan",
            "fuel": ["Petrol"],
            "engine_cc": 1497,
            "idv": (800000, 1500000)
        }
    },

    # TATA

    "Tata": {
        "Nexon": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 1199,
            "idv": (700000, 1400000)
        },

        "Punch": {
            "type": "SUV",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1199,
            "idv": (600000, 1100000)
        },

        "Altroz": {
            "type": "Hatchback",
            "fuel": ["Petrol", "Diesel", "CNG"],
            "engine_cc": 1199,
            "idv": (600000, 1000000)
        },

        "Tiago": {
            "type": "Hatchback",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1199,
         "idv": (450000, 850000)
        },

        "Harrier": {
            "type": "SUV",
            "fuel": ["Diesel"],
            "engine_cc": 1956,
            "idv": (1400000, 2600000)
        }

    },

# MAHINDRA

    "Mahindra": {
   
        "Scorpio-N": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 2198,
            "idv": (1500000, 2800000)
        },

        "Scorpio Classic": {
            "type": "SUV",
            "fuel": ["Diesel"],
            "engine_cc": 2184,
            "idv": (1100000, 1900000)
        },

        "Thar": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 2184,
            "idv": (1200000, 2200000)
        },

        "XUV700": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 1999,
            "idv": (1800000, 3500000)
        },

        "Bolero": {
            "type": "SUV",
            "fuel": ["Diesel"],
            "engine_cc": 1493,
            "idv": (700000, 1200000)
        }
    },

# KIA

    "Kia": {
        "Seltos": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 1497,
            "idv": (1000000, 2200000)
        },

        "Sonet": {
            "type": "SUV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 1197,
            "idv": (700000, 1500000)
        },

        "Carens": {
            "type": "MPV",
            "fuel": ["Petrol", "Diesel"],
            "engine_cc": 1497,
            "idv": (1100000, 2200000)
        }
    },

# TOYOTA

    "Toyota":{
        "Innova Crysta": {
            "type": "MPV",
            "fuel": ["Diesel"],
            "engine_cc": 2393,
            "idv": (1600000, 2800000)
        },

        "Innova Hycross": {
            "type": "MPV",
            "fuel": ["Petrol", "Hybrid"],
            "engine_cc": 1987,
            "idv": (2200000, 3600000)
        },

        "Fortuner": {
            "type": "SUV",
            "fuel": ["Diesel", "Petrol"],
            "engine_cc": 2755,
            "idv": (3000000, 5500000)
        },

        "Glanza": {
            "type": "Hatchback",
            "fuel": ["Petrol", "CNG"],
            "engine_cc": 1197,
            "idv": (600000, 1000000)
        }
    },

# HONDA

    "Honda": {

        "City": {
            "type": "Sedan",
            "fuel": ["Petrol"],
            "engine_cc": 1498,
            "idv": (900000, 1800000)
        },

        "Amaze": {
            "type": "Sedan",
            "fuel": ["Petrol"],
            "engine_cc": 1199,
            "idv": (600000, 1000000)
        },

        "Elevate": {
            "type": "SUV",
            "fuel": ["Petrol"],
            "engine_cc": 1498,
            "idv": (1100000, 1900000)
        }
    },
    
# RENAULT

    "Renault":{
        
        "Kwid": {
            "type": "Hatchback",
            "fuel": ["Petrol"],
            "engine_cc": 999,
            "idv": (300000, 600000)
        },

        "Kiger": {
            "type": "SUV",
            "fuel": ["Petrol"],
            "engine_cc": 999,
            "idv": (600000, 1100000)
        },

        "Triber": {
            "type": "MPV",
            "fuel": ["Petrol"],
            "engine_cc": 999,
            "idv": (550000, 1000000)
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

