from collections import Counter
from datetime import datetime
import random

# adjust these imports to match your project
from dashboard.services.lstm_prediction_service import MASTER_DATA
from dashboard.services.llm.schemas import (
    ChannelContext
)
from dashboard.services.llm.llm_service import LLMService

CHANNEL_CACHE = {}


def analyze_channel():

    imd_summaries = []

    for imd_code, df_imd in MASTER_DATA.groupby("IMD_Code"):

        renewal_rate = (
            df_imd["Renewed"].mean() * 100
            if "Renewed" in df_imd.columns
            else None
        )

        remarks = []

        for remark in df_imd["Last_Remark"].dropna():
            if str(remark).strip():
                remarks.append(str(remark))

        imd_summaries.append({
            "imd": imd_code,
            "renewal_rate": round(renewal_rate, 2),
            "policy_count": df_imd["Policy_Number"].nunique(),
            "avg_tenure": round(df_imd["Policy_Tenure"].mean(), 2),
            "avg_premium": round(df_imd["Premium"].mean(), 2),
            "top_remarks": Counter(remarks).most_common(10)
        })

    prompt = f"""
        You are a senior insurance renewal consultant.

        Below is the performance summary of every IMD in the Jammu branch.

        {imd_summaries}

        Analyse the branch as a whole.

        Identify:

        1. Which IMDs are performing best and why.

        2. Which IMDs are struggling and why.

        3. Compare successful IMDs with struggling IMDs.

        4. Analyse remark history patterns.

        5. Identify behavioural differences.

        6. Explain possible business reasons.

        7. Recommend actions for renewal managers.

        Do not invent facts.
        Base every conclusion only on the supplied information.

        Return the answer in markdown.
        """
    analysis = LLMService.analyze_channel(prompt)

    return analysis