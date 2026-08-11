import re

CATEGORY_PATTERNS = {

    "Competitor Pricing": [
        r"\bcd\s*\d*\b",
        r"competitor",
        r"lower\s+premium",
        r"less\s+premium",
        r"better\s+premium",
        r"better\s+quote",
        r"cheaper",
        r"discount",
        r"disc",
        r"quotation"
    ],

    "Switched Insurer": [
        r"other\s+insurance",
        r"other\s+insurer",
        r"policy\s+done",
        r"renewed\s+outside",
        r"own\s+agency"
        r"done\s+in",
        r"\bicici\b",
        r"\backo\b",
        r"\bhdfc\b",
        r"\btata\b",
        r"\bliberty\b",
        r"\breliance\b",
        r"\biffco\b",
        r"\boriental\b",
        r"\bunited\b",
        r"\buniversal\b",
        r"\bsbi\b",
        r"\bbajaj\b",
        r"\bnew\s+india\b"
    ],

    "Vehicle Sold": [
        r"vehicle.*sold",
        r"car.*sold",
        r"sold.*vehicle",
        r"ownership.*transfer",
        r"transfer.*ownership"
    ],

    "Customer Unavailable": [
        r"army",
        r"posted?",
        r"dubai",
        r"abroad",
        r"foreign",
        r"shifted",
        r"migrated",
        r"call"

        r"not\s+trace",
        r"not\s+ident",
        r"not\s+reach",
        r"not\s+contact",
        r"not\s+pick"
        r"hung\s+up\s+call"

        r"unable\s+to\s+contact",
        r"could\s+not\s+contact",
        r"call\s+not\s+connecting",
        r"call\s+not\s+connect"
        r"custmoer\s+not\s+identify"

        r"wrong\s+number",
        r"wrong\s+no."
        r"invalid\s+number",
        r"number\s+changed",

        r"switched?\s+off",
        r"phone\s+off",
        r"mobile\s+off",

        r"customer\s+unavailable",
        r"out\s+of\s+station",
        r"Customer not pick the call"
    ],

    "Claim Related": [
        r"\bclaim\b",
        r"cashless",
        r"garage",
        r"repair",
        r"settlement",
        r"claim\s+issue",
        r"claim\s+pending",
        r"claim\s+reject"
    ],

    "Relationship Issues": [
        r"sub\s*agent",
        r"relationship",
        r"\brm\b",
        r"partner",
        r"service\s+issue"
    ],

    "Product Limitation": [
        r"nil\s*dep",
        r"zero\s*dep",
        r"add[\s-]?on",
        r"coverage",
        r"policy\s+feature"
    ],

    "Premium Increase": [
        r"premium",
        r"costly",
        r"expensive"
    ],

    "Documentation Issues": [
        r"\brc\b",
        r"document",
        r"\bnoc\b",
        r"kyc",
        r"hypothecation"
    ],

    "Vehicle Not in Use": [
        r"scrap",
        r"life\s+expire",
        r"vehicle\s+expire",
        r"not\s+using",
        r"off\s+road"
    ],

    "Financial Constraints": [
        r"financial",
        r"budget",
        r"cannot\s+afford",
        r"cash\s+problem"
    ]
}

class FactExtractor:

    def extract(self, tool_name, data):

        if data is None:
            return []

        if tool_name == "status_breakdown":
            return self._status_breakdown(data)

        elif tool_name == "renewal_distribution":
            return self._renewal_distribution(data)

        elif tool_name == "veh_age_analysis":
            return self._vehicle_age(data)

        elif tool_name == "imd_summary":
            return self._imd_summary(data)

        elif tool_name == "search_similar_remarks":
            return self._remarks(data)

        return []


    def _status_breakdown(self, data):


        if isinstance(data,dict):
            data = next(iter(data.values()))

        statistics = {}

        for row in data:

            statistics[row["STATUS"]] = {
                "count": row["policy_count"],
                "percentage": float(row["percentage"])
            }

        renewed = statistics.get("Renewed", {}).get("percentage", 0)

        if renewed >= 70:
            fact = "Renewal performance is healthy."

        elif renewed >= 50:
            fact = "Renewal performance is moderate."

        else:
            fact = "Renewal performance requires attention."

        return [{
            "title": "Renewal Performance",
            "fact": fact,
            "statistics": statistics,
            "source": "status_breakdown"
        }]

    

    def _renewal_distribution(self, data):

        if isinstance(data,dict):
            data = next(iter(data.values()))

        statistics = {}

        dominant = None

        for row in data:

            statistics[row["renewal_number"]] = {
                "count": row["policy_count"],
                "percentage": float(row["percentage"])
            }

            if dominant is None or row["percentage"] > dominant["percentage"]:
                dominant = row

        fact = (
            f"The portfolio is concentrated around "
            f"renewal stage {dominant['renewal_number']}."
        )

        return [{
            "title": "Customer Tenure",
            "fact": fact,
            "statistics": statistics,
            "source": "renewal_distribution"
        }]

    def _vehicle_age(self, data):

        avg = float(data["average_age"])

        if avg >= 7:

            fact = "The portfolio contains predominantly older vehicles."

        elif avg >= 5:

            fact = "The portfolio has a balanced vehicle age profile."

        else:

            fact = "The portfolio consists mainly of newer vehicles."

        return [{
            "title": "Vehicle Portfolio",
            "fact": fact,
            "statistics": {
                "Average Age": avg,
                "Minimum Age": data["minimum_age"],
                "Maximum Age": data["maximum_age"],
                "0-3 Years": data["age_0_3"],
                "4-7 Years": data["age_4_7"],
                "8-10 Years": data["age_8_10"],
                "Above 10 Years": data["age_above_10"]
            },
            "source": "veh_age_analysis"
        }]

    def _imd_summary(self, data):

        branch = data["branch_statistics"]

        high = data["high_performers"]
        average = data["average_performers"]
        low = data["low_performers"]

        fact = (
            f"The branch has {branch['total_imds']} significant IMDs. "
            f"{len(high)} are classified as high performers, "
            f"{len(average)} as average performers and "
            f"{len(low)} as low performers."
        )

        return [{
            "title": "IMD Landscape",

            "fact": fact,

            "statistics": {
                "Total IMDs": branch["total_imds"],
                "Average Renewal Rate": branch["average_renewal_rate"],
                "Average Portfolio Size": branch["average_portfolio_size"],
                "Minimum Portfolio Considered": branch["minimum_portfolio_considered"],

                "High Performing IMDs": [
                    {
                        "IMD": imd["imd_code"],
                        "Renewal Rate": imd["renewal_rate"],
                        "Portfolio": imd["portfolio_size"],
                        "Average Vehicle Age": imd["average_vehicle_age"],
                        "Minimum Vehicle Age": imd["minimum_vehicle_age"],
                        "Maximum Vehicle Age": imd["maximum_vehicle_age"],
                        "0-3 Years": imd["age_0_3"],
                        "4-7 Years": imd["age_4_7"],
                        "8-10 Years": imd["age_8_10"],
                        "Above 10 Years": imd["age_above_10"]
                    }
                    for imd in high
                ],

                "Average Performing IMDs": [
                    {
                        "IMD": imd["imd_code"],
                        "Renewal Rate": imd["renewal_rate"],
                        "Portfolio": imd["portfolio_size"],
                        "Average Vehicle Age": imd["average_vehicle_age"],
                        "Minimum Vehicle Age": imd["minimum_vehicle_age"],
                        "Maximum Vehicle Age": imd["maximum_vehicle_age"],
                        "0-3 Years": imd["age_0_3"],
                        "4-7 Years": imd["age_4_7"],
                        "8-10 Years": imd["age_8_10"],
                        "Above 10 Years": imd["age_above_10"]
                    }
                    for imd in average
                ],

                "Low Performing IMDs": [
                    {
                        "IMD": imd["imd_code"],
                        "Renewal Rate": imd["renewal_rate"],
                        "Portfolio": imd["portfolio_size"],
                        "Average Vehicle Age": imd["average_vehicle_age"],
                        "Minimum Vehicle Age": imd["minimum_vehicle_age"],
                        "Maximum Vehicle Age": imd["maximum_vehicle_age"],
                        "0-3 Years": imd["age_0_3"],
                        "4-7 Years": imd["age_4_7"],
                        "8-10 Years": imd["age_8_10"],
                        "Above 10 Years": imd["age_above_10"]
                    }
                    for imd in low
                ]
            },

            "source": "imd_summary"
        }]

    def _remarks(self, data):

        if isinstance(data, dict):
            data = data.get("results", [])

        categories = {
            "Competitor Pricing": 0,
            "Customer Unavailable": 0,
            "Vehicle Sold": 0,
            "Claim Related": 0,
            "Relationship Issues": 0,
            "Product Limitation": 0,
            "Premium Increase": 0,
            "Switched Insurer": 0,
            "Documentation Issues": 0,
            "Vehicle Not in Use": 0,
            "Financial Constraints": 0,
            "Other": 0
        }

        examples = {
            category: []
            for category in categories
        }

        for row in data:

            remark = (
                (row.get("REMARKS") or "")
                .strip()
            )

            if not remark:
                continue

            remark_lower = remark.lower()

            if "co varun" in remark_lower:
                continue

            category = "Other"

            for category_name, patterns in CATEGORY_PATTERNS.items():
                if any(
                    re.search(pattern, remark_lower, re.IGNORECASE)
                    for pattern in patterns
                ):
                    category = category_name
                    break

            categories[category] += 1

            if len(examples[category]) < 3:
                examples[category].append(remark)

        total = sum(categories.values())

        statistics = {}

        for category, count in categories.items():

            statistics[category] = {
                "count": count,
                "percentage": round(
                    count * 100 / total,
                    2
                ) if total else 0
            }

        dominant = max(categories, key=categories.get)

        return [{
            
            "statistics": statistics,

            "examples": examples,

            "source": "search_similar_remarks"
        }]