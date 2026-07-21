
from dashboard.services.lstm_prediction_service import LLM_CACHE, MASTER_DATA
from .llm_service import LLMService
from .schemas import PolicyContext, Remark
from datetime import datetime

import pandas as pd


def analyze_selected_policy(policy_number: str, base_probability: float):
    """
    Runs LLM analysis for a selected policy.

    Uses cached result if available
    """


    # -------------------------------
    # Return cached result
    # -------------------------------

    if policy_number in LLM_CACHE:
        return LLM_CACHE[policy_number]
    

    # -------------------------------
    # Load policy
    # -------------------------------
    policy = MASTER_DATA[MASTER_DATA["Policy_Number"]==policy_number]

    if policy.empty:
        raise ValueError(
            f"Policy {policy_number} not found."
        )
    
    policy = policy.iloc[0]

    # -------------------------------
    # Load Complete Policy History
    # -------------------------------

    policy_history = (
        MASTER_DATA[MASTER_DATA["Policy_Number"] == policy_number].sort_values("Policy_Tenure")
    )

    if policy_history.empty:
        raise ValueError(
            f"Policy {policy_number} not found"
        )
    
    # Latest Tenure

    current_policy = policy_history.iloc[-1]


    # -------------------------------
    # Previous Remarks
    # -------------------------------

    previous_remarks = []

    for _, row in policy_history.iloc[:-1].iterrows():

        if pd.notna(row["Last_Remark"]) and str(row["Last_Remark"]).strip():

            previous_remarks.append({

                "tenure": int(row["Policy_Tenure"]),

                "remark": row["Last_Remark"]

            })
    # -------------------------------
    # Build context
    # -------------------------------

    context = PolicyContext(

        policy_number = policy_number,

        historical_insights = {
            "previous_remarks": previous_remarks
        },

        base_probability = base_probability,

        current_policy = policy.to_dict(),

        remarks =[
            Remark(
                timestamp = datetime.now(),
                author = "Renewal Manager",
                text = policy["Last_Remark"]
            )
        ]
    )



    # -------------------------------
    # Call LLM
    # -------------------------------

    service = LLMService()

    analysis = service.analyze_policy(context)

    total_adjustment = sum(
        remark.adjustment for remark in analysis.remark_adjustments
    )

    final_probability = base_probability + total_adjustment

    final_probability = max(
        0,
        min(100, final_probability)
    )

    final_probability = round(final_probability,1)

    historical_insights = context.historical_insights


    # -------------------------------
    # Cache
    # -------------------------------

    result = {
        "Analysis": analysis,
        
        "Base_Probability": base_probability,

        "Adjustment": total_adjustment,

        "Historical_Insights": historical_insights,

        "Final_Probability": final_probability
    }

    LLM_CACHE[policy_number] = result

    return result