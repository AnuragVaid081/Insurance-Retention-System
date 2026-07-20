from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

LLM_PATH = ROOT / "dashboard" / "services" / "llm"

sys.path.insert(0,str(LLM_PATH))

from llm_service import LLMService
from schemas import (
    PolicyContext,
    Remark
)

remarks = [

    Remark(
        timestamp=datetime.now(),
        author="RM",
        text="Customer is comparing premium with ICICI Lombard."
    ),

    Remark(
        timestamp=datetime.now(),
        author="RM",
        text="Customer has renewed with us for the last four years."
    ),

    Remark(
        timestamp=datetime.now(),
        author="RM",
        text="Requested callback after salary credit."
    )

]

historical_insights = [

    "Customer has renewed consecutively for four years.",

    "No claims in the last three policy terms.",

    "Premium increased by 6% compared to last renewal.",

    "Customer belongs to a high-retention segment."

]


current_policy = {

    "Policy_Type": "Private Car",

    "Premium": 18250,

    "NCB": "35%",

    "Vehicle_Age": 5,

    "Claims_Last_Year": 0,

    "Insured_Declared_Value": 540000,

    "Channel": "Agent"

}


context = PolicyContext(

    policy_number="POL123456",

    customer_id="CUS98765",

    base_probability=82.4,

    current_policy=current_policy,

    historical_insights=historical_insights,

    remarks=remarks

)


service = LLMService()

result = service.analyze_policy(context)


print("=" * 60)

print("Prediction Explanation")

print(result.prediction_explanation)

print()

print("=" * 60)

print("Remark Adjustments")

for adjustment in result.remark_adjustments:

    print(adjustment)

print()

print("=" * 60)

print("Overall Summary")

print(result.overall_summary)

print()

print("=" * 60)

print("Recommendation")

print(result.recommendation)