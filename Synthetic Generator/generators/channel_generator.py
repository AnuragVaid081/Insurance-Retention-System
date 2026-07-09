import random
from pathlib import Path

import pandas as pd
from faker import Faker

from datetime import datetime

from constants import AREA_INFO

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)
pd.set_option("display.expand_frame_repr", False)

fake = Faker('en_IN')
random.seed(42)
Faker.seed(42)

# Dictionary of all the channel types and their corresponding probabilities
 
CHANNEL_TYPES = {
    "POSP" : 0.45,
    "Prime Broker" : 0.25,
    "Agency" : 0.15,
    "Dealer" : 0.10,
    "Bancassurance" : 0.05
}

# Portfolio size assigned to each channel type

PORTFOLIO_SIZE = {
    "POSP" : (20,100),
    "Prime Broker" : (150,600),
    "Agency" : (80,300),
    "Dealer" : (50,250),
    "Bancassurance" : (200,800)
}



# Activity Status
# This describes the probability of a IMD recieving a new policy 

ACTIVE_STATUS = {
    "Active" : 0.97,
    "Inactive" : 0.03
}

# Dictionary of all of the different areas within Jammu and their direct mapping to their respective districts to prevent impossible combinations 

# List of Districts

DISTRICTS = [
    "Jammu",
    "Samba",
    "Kathua",
    "Udhampur",
    "Reasi",
    "Rajouri",
    "Poonch",
    "Ramban",
    "Doda",
    "Kishtwar"
]

# Assigning weights to each area based on their population and economic activity to ensure that the generated data is
#  representative of the actual distribution of channels across different areas in Jammu

CHANNEL_AREA_WEIGHTS = {

    # PRIME BROKERS

    "Prime Broker": {
        "Gandhi Nagar": 12,
        "Trikuta Nagar": 10,
        "Channi Himmat": 9,
        "Jewel Chowk": 9,
        "Canal Road": 8,
        "Bakshi Nagar": 7,
        "Narwal": 7,
        "Bari Brahmana": 8,
        "Kathua": 7,
        "Udhampur": 6,
        "Janipur": 2,
        "Rajouri": 1,
        "Poonch": 1
    },

        #POSP

        "POSP": {
        "Gandhi Nagar": 5,
        "Janipur": 6,
        "Talab Tillo": 6,
        "Rehari": 5,
        "Satwari": 5,
        "Akhnoor": 5,
        "R.S. Pura": 5,
        "Bishnah": 5,
        "Samba": 5,
        "Kathua": 5,
        "Rajouri": 4,
        "Poonch": 4,
        "Doda": 3,
        "Kishtwar": 3
    },

        # AGENCY

        "Agency": {
        "Gandhi Nagar": 8,
        "Trikuta Nagar": 7,
        "Janipur": 6,
        "Talab Tillo": 6,
        "Kathua": 5,
        "Samba": 5,
        "Udhampur": 5,
        "Rajouri": 3,
        "Poonch": 3
    },

        # DEALER

        "Dealer": {
        "Narwal": 12,
        "Gandhi Nagar": 10,
        "Bari Brahmana": 10,
        "Kathua": 8,
        "Samba": 7,
        "Udhampur": 6
    },

        # BANCASSURANCE

        "Bancassurance": {
        "Gandhi Nagar": 10,
        "Kathua": 8,
        "Udhampur": 7,
        "Samba": 7,
        "Rajouri": 6,
        "Poonch": 5
    }
}

# Naming options separated for a combination of prefixes and suffixes to create unique channel names

NAME_PREFIX = [
    "Sharma",
    "Mahajan",
    "Dogra",
    "Khajuria",
    "Gupta",
    "Raina",
    "Verma",
    "Gupta",
    "Mahindra",
    "Trikuta",
    "Jammu",
    "North",
    "Reliable",
    "Elite",
    "Secure",
    "Royal"
]

NAME_MIDDLE = [
    "Prime",
    "Secure",
    "Reliable",
    "Elite",
    "Capital",
    "Shield",
    "Trust",
    "Unity",
    "Pioneer",
    "Vertex",
    "Apex",
    "Royal",
    "Smart",
    "Future",
    "Vision",
    "Global",
    "Summit",
    "Fortune",
    "Integrity",
    "Guardian"
]

NAME_SUFFIX = [
    "Insurance",
    "Insurance Services",
    "Insurance Point",
    "Insurance Solutions",
    "Risk Advisors",
    "Insurance Hub",
    "Insurance Associates",
    "Insurance Consultants"
]


"""THE FOLLOWING ARE HELPER FUNCTIONS DESIGNED TO HELP THE MAIN GENERATOR IN GENERATING THE RANDOMISED RECORD FOR EACH IMD"""


# Area selection function

def get_area(CHANNEL_TYPES):
    area_weights = CHANNEL_AREA_WEIGHTS[CHANNEL_TYPES]

    return random.choices(
        population = list(area_weights.keys()),
        weights = list(area_weights.values()),
        k = 1
    )[0]

"""
    Returns a weighted random area based on the distribution channel.
"""
    
# IMD Generation function

def generate_imd(index):
    return f"IMD{10000 + index}"

"""
        Generates a unique IMD (Insurance Marketing Distributor) identifier based on the provided index. 
        The identifier is formatted as "IMD" followed by a number starting from 10000, ensuring uniqueness for each generated IMD. 
"""


# Function to create entity names for the various distribution channels based on the naming options proviede above

USED_ENTITY_NAMES = set()

def generate_entity_name():
        
        name = (
            f"{random.choice(NAME_PREFIX)} " 
            f"{random.choice(NAME_MIDDLE)} " 
            f"{random.choice(NAME_SUFFIX)}"
        )
    
        while name in USED_ENTITY_NAMES:
         name = (
             f"{random.choice(NAME_PREFIX)}"
             f"{random.choice(NAME_MIDDLE)}"
             f"{random.choice(NAME_SUFFIX)}"
         )

        USED_ENTITY_NAMES.add(name)
        
        return name
    
"""
Generates a Unique Entity name to represent the distributers 
"""

# TEST CODE

# for _ in range(25):
#    print(generate_entity_name())
# print(len(USED_ENTITY_NAMES))

# Function to generate channel type associated with each distributer

def generate_channel_type():
    return random.choices(
        population = list(CHANNEL_TYPES.keys()),
        weights= list(CHANNEL_TYPES.values()),
        k = 1
    )[0]

# TEST CODE

# for i in range(10):
#     print(generate_channel_type())

# Function to generate portfolio size for each channel

def generate_portfolio_size(channel_type):
    min_size,max_size = PORTFOLIO_SIZE[channel_type]
    portfolio_size = random.randint(min_size,max_size)
    return portfolio_size

"""
Generates the portfolio size logically with relation to each channel type with accordance to the ranges provided at the top
"""
# TEST CODE

# for channel in CHANNEL_TYPES.keys():
#     print(channel)

#     for _ in range(5):
#         print(generate_portfolio_size(channel))

# Function to randomly generate the onboarding year of each distributor ranging from 2016 - 2025

def generate_onboarding_date():

    year = random.choices(
        population = [2016,2017,2018,2019,2020,2021,2022,2023,2024,2025],
        weights = [2,3,5,8,10,12,16,18,16,10],
        k = 1,
    )[0]

    month = random.randint(1,12)

    day = random.randint(1,28)

    return datetime(year, month, day).strftime("%Y-%m-%d")



# def generate_year_onboarded():
#     return random.randint(*ONBOARD_YEAR)

"""
Generates the onboarding year for the distributor with the insurrer
"""

# Function to generate the activation status for the distributor, meaning can they get new policies?

def generate_activation_status():
    return random.choices(
        population = list(ACTIVE_STATUS.keys()),
        weights = list(ACTIVE_STATUS.values()),
        k = 1
    )[0]

"""
Generates the activation status for each distributor,
Active meaning they can get new policies and renewals,
Inactive meaning they cannot get new policies or renewals anymore 
"""

def generate_channels(n_channels):

    channels = []

    for i in range  (n_channels):

        channel_type = generate_channel_type()

        area = get_area(channel_type)

        district = AREA_INFO[area]["district"]

        channel = {
            "IMD_Code": generate_imd(i),
            "Entity_Name": generate_entity_name(),
            "Channel_Type": channel_type,
            "Area": area,
            "District": district,
            "Portfolio_Size": generate_portfolio_size(channel_type),
            "Year_Onboarded": generate_onboarding_date(),
            "Active_Status": generate_activation_status()
        }

        channels.append(channel)
    
    df_channels = pd.DataFrame(channels)    

    output_dir = Path("Synthetic Generator/data")
    output_dir.mkdir(exist_ok= True)

    output_file = output_dir / "channel_master.csv"

    df_channels.to_csv(output_file,index = False)

    print(f"Saved {len(df_channels)} channels to {output_file}")

    return df_channels
    


df_channels = generate_channels(500)





