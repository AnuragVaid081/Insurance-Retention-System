import pandas as pd


CURRENT_YEAR = 2026

POLICY_STATUS = [
    "Active",
    "Renewed",
    "Lapsed",
    "Cancelled",
    "Expired"
]

AREA_INFO = {

    # ===================== Jammu Urban =====================

    "Gandhi Nagar": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 12
    },

    "Trikuta Nagar": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 8
    },

    "Channi Himmat": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 6
    },

    "Shastri Nagar": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 5
    },

    "Bakshi Nagar": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 5
    },

    "Talab Tillo": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 10
    },

    "Janipur": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 10
    },

    "Rehari": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 9
    },

    "Canal Road": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 6
    },

    "Jewel Chowk": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 5
    },

    "Satwari": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 9
    },

    "Narwal": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 5
    },

    "Bahu Plaza": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 8
    },

    # ===================== Jammu Rural =====================

    "Akhnoor": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 5
    },

    "Bishnah": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 5
    },

    "R.S. Pura": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 6
    },

    "Marh": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 3
    },

    "Arnia": {
        "district": "Jammu",
        "rto": "JK02",
        "weight": 3
    },

    # ===================== Samba =====================

    "Samba": {
        "district": "Samba",
        "rto": "JK08",
        "weight": 5
    },

    "Vijaypur": {
        "district": "Samba",
        "rto": "JK08",
        "weight": 4
    },

    "Bari Brahmana": {
        "district": "Samba",
        "rto": "JK08",
        "weight": 7
    },

    "Ghagwal": {
        "district": "Samba",
        "rto": "JK08",
        "weight": 3
    },

    # ===================== Kathua =====================

    "Kathua": {
        "district": "Kathua",
        "rto": "JK04",
        "weight": 4
    },

    "Lakhanpur": {
        "district": "Kathua",
        "rto": "JK04",
        "weight": 2
    },

    "Hiranagar": {
        "district": "Kathua",
        "rto": "JK04",
        "weight": 3
    },

    "Dayalachak": {
        "district": "Kathua",
        "rto": "JK04",
        "weight": 2
    },

    "Bani": {
        "district": "Kathua",
        "rto": "JK04",
        "weight": 1
    },

    "Billawar": {
        "district": "Kathua",
        "rto": "JK04",
        "weight": 2
    },

    # ===================== Udhampur =====================

    "Udhampur": {
        "district": "Udhampur",
        "rto": "JK14",
        "weight": 3
    },

    "Chenani": {
        "district": "Udhampur",
        "rto": "JK14",
        "weight": 2
    },

    "Ramnagar": {
        "district": "Udhampur",
        "rto": "JK14",
        "weight": 2
    },

    # ===================== Reasi =====================

    "Reasi": {
        "district": "Reasi",
        "rto": "JK20",
        "weight": 2
    },

    "Katra": {
        "district": "Reasi",
        "rto": "JK20",
        "weight": 6
    },

    # ===================== Rajouri =====================

    "Rajouri": {
        "district": "Rajouri",
        "rto": "JK11",
        "weight": 3
    },

    "Nowshera": {
        "district": "Rajouri",
        "rto": "JK11",
        "weight": 2
    },

    "Sunderbani": {
        "district": "Rajouri",
        "rto": "JK11",
        "weight": 2
    },

    # ===================== Poonch =====================

    "Poonch": {
        "district": "Poonch",
        "rto": "JK12",
        "weight": 3
    },

    "Mendhar": {
        "district": "Poonch",
        "rto": "JK12",
        "weight": 2
    },

    "Surankote": {
        "district": "Poonch",
        "rto": "JK12",
        "weight": 2
    },

    # ===================== Ramban =====================

    "Ramban": {
        "district": "Ramban",
        "rto": "JK19",
        "weight": 2
    },

    "Banihal": {
        "district": "Ramban",
        "rto": "JK19",
        "weight": 2
    },

    # ===================== Doda =====================

    "Doda": {
        "district": "Doda",
        "rto": "JK06",
        "weight": 2
    },

    "Bhaderwah": {
        "district": "Doda",
        "rto": "JK06",
        "weight": 2
    },

    # ===================== Kishtwar =====================

    "Kishtwar": {
        "district": "Kishtwar",
        "rto": "JK17",
        "weight": 1
    },

    "Padder": {
        "district": "Kishtwar",
        "rto": "JK17",
        "weight": 1
    }

}


NCB_STEPS = [
    0,
    20,
    25,
    35,
    45,
    50
]

BASE_PREMIUM_RATE = 0.03

CLAIM_LOADING = {
    0: 1.00,
    1: 1.10,
    2: 1.20,
    3: 1.30
}


# REMARK GENERATOR CONSTANTS


POSITIVE_REMARKS = [
    "Customer confirmed renewal",
    "Premium accepted",
    "Waiting for payment",
    "Payment expected today",
    "Renewal in progress",
    "Documents shared",
    "Long-term customer",
    "Customer satisfied",
]

NEUTRAL_REMARKS = [
    "Call after salary",
    "Requested callback",
    "Busy, call later",
    "Follow-up pending",
    "Waiting for response",
    "Quote shared",
    "Agent to follow up",
    "Out of station",
]

NEGATIVE_REMARKS = [
    "Vehicle sold",
    "Comparing with ICICI",
    "Comparing competitor quotes",
    "Premium too high",
    "Customer not interested",
    "Renewed with competitor",
    "Payment delayed",
    "No response after follow-up",
    "Claim experience poor",
    "Agent lost customer",
]