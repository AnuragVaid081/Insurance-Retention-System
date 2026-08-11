from db import get_connection
from fastmcp import FastMCP
from ollama import embed
from typing import Annotated
from typing import Literal



mcp = FastMCP("Insurance AI")

# @mcp.tool()
# def branch_summary(imd_channel):
#     """
#     Return Branch level statistics.
#     """

#     conn = get_connection()
#     cur = conn.cursor()


#     cur.execute("""
#     SELECT
#         COUNT(*) total_policies,
#         AVG(\"TBR_Veh_Age\") average_vehicle_age,
#         AVG(\"renewal_number\") average_renewal_stage
#     FROM \"April_Month_Renewals\"
#     WHERE \"IMD_Channel\" = %s;  
# """,(imd_channel,))

#     result = cur.fetchone()

#     cur.close()
#     conn.close()

#     return result



@mcp.tool()
def imd_summary(imd_channel):
    """
    Returns a branch-wide summary of IMD performance.

    IMDs are evaluated using BOTH renewal rate and portfolio size.

    Small portfolios are excluded from comparison to avoid misleading
    conclusions.

    Returns representative High, Average and Low performing IMDs.

    Always call this tool before analysing individual IMDs.

    Use this tool whenever the user asks about:
    - IMD performance
    - Channel performance
    - High performing IMDs
    - Weak IMDs
    - Executive IMD analysis
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    WITH imd_stats AS (

        SELECT

            \"New_IMD_Code\",

            COUNT(*) AS portfolio_size,

            COUNT(*) FILTER(
                WHERE \"STATUS\"=\'Renewed\'
            ) AS renewed,

            COUNT(*) FILTER(
                WHERE \"STATUS\"=\'Follow up\'
            ) AS follow_up,

            COUNT(*) FILTER(
                WHERE \"STATUS\"=\'Lost\'
            ) AS lost,

            ROUND(
                COUNT(*) FILTER(
                    WHERE \"STATUS\"=\'Renewed\'
                ) * 100.0 / COUNT(*),
            2) AS renewal_rate,

            ROUND(AVG(\"TBR_Veh_Age\"),2) AS average_vehicle_age,

            MIN(\"TBR_Veh_Age\") AS minimum_vehicle_age,

            MAX(\"TBR_Veh_Age\") AS maximum_vehicle_age,

                COUNT(*) FILTER(
                    WHERE \"TBR_Veh_Age\" BETWEEN 0 AND 3 
                ) AS age_0_3,

                COUNT(*) FILTER(
                    WHERE \"TBR_Veh_Age\" BETWEEN 4 AND 7
                ) AS age_4_7,

                COUNT(*) FILTER(
                WHERE \"TBR_Veh_Age\" BETWEEN 8 AND 10
                ) AS age_8_10,

                COUNT(*) FILTER(
                WHERE \"TBR_Veh_Age\" > 10
                ) AS age_above_10           

        FROM \"April_Month_Renewals\"

        WHERE \"IMD_Channel\" = %s

        GROUP BY \"New_IMD_Code\"

        HAVING COUNT(*) >= 3
    ),

    branch_stats AS (

        SELECT

            ROUND(AVG(renewal_rate),2) AS avg_renewal_rate,

            ROUND(AVG(portfolio_size),2) AS avg_portfolio_size,

            COUNT(*) AS total_imds

        FROM imd_stats

    )

    SELECT

        i.*,

        b.total_imds,

        b.avg_renewal_rate,

        b.avg_portfolio_size,

        CASE

            WHEN
                i.renewal_rate >= b.avg_renewal_rate + 5
                AND
                i.portfolio_size >= b.avg_portfolio_size

            THEN 'High'

            WHEN
                i.renewal_rate <= b.avg_renewal_rate - 5

            THEN 'Low'

            ELSE 'Average'

        END AS performance_category

    FROM imd_stats i

    CROSS JOIN branch_stats b

    ORDER BY

        performance_category,

        portfolio_size DESC,

        renewal_rate DESC;

    """, (imd_channel,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    if not rows:
        return {
            "branch_statistics": {},
            "high_performers": [],
            "average_performers": [],
            "low_performers": []
        }

    branch_statistics = {
        "total_imds": rows[0]["total_imds"],
        "average_renewal_rate": float(rows[0]["avg_renewal_rate"]),
        "average_portfolio_size": float(rows[0]["avg_portfolio_size"]),
        "minimum_portfolio_considered": 3
    }

    high = []
    average = []
    low = []

    for row in rows:

        record = {
            "imd_code": row["New_IMD_Code"],
            "portfolio_size": row["portfolio_size"],
            "renewal_rate": float(row["renewal_rate"]),
            "renewed": row["renewed"],
            "follow_up": row["follow_up"],
            "lost": row["lost"],

            "average_vehicle_age": float(row["average_vehicle_age"]),
            "minimum_vehicle_age": row["minimum_vehicle_age"],
            "maximum_vehicle_age": row["maximum_vehicle_age"],

            "age_0_3": row["age_0_3"],
            "age_4_7": row["age_4_7"],
            "age_8_10": row["age_8_10"],
            "age_above_10": row["age_above_10"]
        }

        if row["performance_category"] == "High":
            high.append(record)

        elif row["performance_category"] == "Average":
            average.append(record)

        else:
            low.append(record)

    return {
        "branch_statistics": branch_statistics,
        "high_performers": high[:5],
        "average_performers": average[:5],
        "low_performers": low[:5]
    }

@mcp.tool()
def status_breakdown(imd_channel,New_IMD_Code: Annotated[int, "Single IMD code returned by get_imd_codes"] | None = None):
    """
    Returns the distribution of policy statuses.

    If an IMD code is provided, returns the status breakdown for that IMD.
    Otherwise, returns the branch-wide status distribution.

    Use this tool whenever the user asks about:
    - Renewed policies
    - Pending policies
    - Lost policies
    - Status distribution
    
    """

    conn = get_connection()
    cur = conn.cursor()

    if New_IMD_Code:

        cur.execute("""
            SELECT
                \"STATUS\",
                COUNT(*) AS policy_count,
                ROUND(
                    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2
                ) AS percentage
                FROM \"April_Month_Renewals\"
                WHERE \"IMD_Channel\" = %s
                AND \"New_IMD_Code\" = %s
                GROUP BY \"STATUS\"
                ORDER BY policy_count DESC;
        """,(imd_channel,New_IMD_Code,))

    else:

        cur.execute("""
            SELECT
            \"STATUS\",
            COUNT(*) AS policy_count,
            ROUND(
                COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2
            ) AS percentage
            FROM \"April_Month_Renewals\"
            WHERE \"IMD_Channel\" = %s
            GROUP BY \"STATUS\"
            ORDER BY policy_count DESC;
        """,(imd_channel,))

    result = cur.fetchall()

    cur.close()
    conn.close()

    return result



@mcp.tool()
def renewal_distribution(imd_channel,New_IMD_Code: Annotated[int, "Single IMD code returned by get_imd_codes"] | None = None):
    """
    Returns the distribution of policies across renewal stages.

    If an IMD code is provided, returns the renewal distribution for that IMD.
    Otherwise, returns the branch-wide distribution.

    Use this tool whenever the user asks about:
    - Renewal stages
    - Customer tenure
    - Renewal distribution
    - Customer maturity
    """


    conn = get_connection()
    cur = conn.cursor()

    if New_IMD_Code:

        cur.execute("""
            SELECT
                \"renewal_number\",
                COUNT(*) AS policy_count,
                ROUND(
                COUNT(*) * 100 / SUM(COUNT(*)) OVER(),2 
                ) AS percentage
            FROM \"April_Month_Renewals\"
            WHERE \"IMD_Channel\" = %s
            AND \"New_IMD_Code\" = %s
            GROUP BY \"renewal_number\"
            ORDER BY \"renewal_number\";
        """,(imd_channel,New_IMD_Code,))

    else:

        cur.execute("""
            SELECT
                \"renewal_number\",
                COUNT(*) AS policy_count,
                ROUND(
                COUNT(*) * 100 / SUM(COUNT(*)) OVER(),2 
                ) AS percentage
            FROM \"April_Month_Renewals\"
            WHERE \"IMD_Channel\" = %s
            GROUP BY \"renewal_number\"
            ORDER BY \"renewal_number\";            
        """,(imd_channel,))

    result = cur.fetchall()

    cur.close()
    conn.close()

    return result

@mcp.tool()
def get_imd_codes(imd_channel):
    """
    Returns a list of IMD codes for a given channel.

    Use this tool whenever you are asked about:
    - IMD codes
    - List of IMDs
    - IMD identifiers

    Only use this tool when you need to IMD codes for analysis like segmenting IMDs or comparing their performance.
    Only remember the string values of the IMD codes like 1184318, 1194226, 1164366
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT \"New_IMD_Code\"
        FROM \"April_Month_Renewals\"
        WHERE \"IMD_Channel\" = %s;
    """,(imd_channel,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "imd_codes":[
            row["New_IMD_Code"] 
            for row in rows
        ]
    }

@mcp.tool()
def veh_age_analysis(imd_channel,New_IMD_Code: Annotated[int, "Single IMD code returned by get_imd_codes"] | None = None):
    """
    Returns vehicle age statistics and distribution.

    If an IMD code is provided, returns statistics for that IMD.
    Otherwise, returns branch-wide statistics.

    Use this tool whenever the user asks about:
    - Vehicle age
    - Age distribution
    - Portfolio age
    - Average vehicle age
    """

    conn = get_connection()
    cur = conn.cursor()

    if New_IMD_Code:

        cur.execute("""
            SELECT
                COUNT(*) AS total_policies,

                ROUND(AVG(\"TBR_Veh_Age\"),2) AS average_age,

                MIN(\"TBR_Veh_Age\") AS minimum_age,

                MAX(\"TBR_Veh_Age\") AS maximum_age,

                COUNT(*) FILTER(
                    WHERE \"TBR_Veh_Age\" BETWEEN 0 AND 3 
                ) AS age_0_3,

                COUNT(*) FILTER(
                    WHERE \"TBR_Veh_Age\" BETWEEN 4 AND 7
                ) AS age_4_7,

                COUNT(*) FILTER(
                WHERE \"TBR_Veh_Age\" BETWEEN 8 AND 10
                ) AS age_8_10,

                COUNT(*) FILTER(
                WHERE \"TBR_Veh_Age\" > 10
                ) AS age_above_10

            FROM \"April_Month_Renewals\"
            WHERE \"IMD_Channel\" = %s
            AND \"New_IMD_Code\" = %s;
        """,(imd_channel,New_IMD_Code,))


    else:
        cur.execute("""
            SELECT
                COUNT(*) AS total_policies,

                ROUND(AVG(\"TBR_Veh_Age\"),2) AS average_age,

                MIN(\"TBR_Veh_Age\") AS minimum_age,

                MAX(\"TBR_Veh_Age\") AS maximum_age,

                COUNT(*) FILTER(
                    WHERE \"TBR_Veh_Age\" BETWEEN 0 AND 3 
                ) AS age_0_3,

                COUNT(*) FILTER(
                    WHERE \"TBR_Veh_Age\" BETWEEN 4 AND 7
                ) AS age_4_7,

                COUNT(*) FILTER(
                WHERE \"TBR_Veh_Age\" BETWEEN 8 AND 10
                ) AS age_8_10,

                COUNT(*) FILTER(
                WHERE \"TBR_Veh_Age\" > 10
                ) AS age_above_10

            FROM \"April_Month_Renewals\"
            WHERE \"IMD_Channel\" = %s;


        """,(imd_channel,))

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result


@mcp.tool()
def search_similar_remarks(
    imd_channel,
    category: Literal[
        "competitor_pricing",
        "relationship_issue",
        "customer_unavailable",
        "product_limitation",
        "premium_increase",
        "other"
    ]
):
    """
    Searches historical lost policy remarks using semantic similarity.

    category must be one of:

    - competitor_pricing
    - relationship_issue
    - customer_unavailable
    - product_limitation
    - premium_increase
    - other

    Always use one of the above categories.
    Never generate free-form search queries.

    Use this tool whenever investigating the causes of lost business.
    """

    QUERY_MAP = {
        "competitor_pricing":
            "Competitor pricing CD CD0 CD1 Discount cheaper premium",

        "relationship_issue":
            "Sub Agent Case RM Relationship Manager relationship issue",

        "customer_unavailable":
            "Customer in Army Customer in Dubai Customer shifted Customer unavailable",

        "product_limitation":
            "Nil Dep Not Covered Zero Dep product limitation",

        "premium_increase":
            "Premium increase premium too high expensive renewal",

        "other":
            "Other miscellaneous business loss reasons"
    }

    query = QUERY_MAP[category]

    response = embed(
        model="nomic-embed-text",
        input=query
    )

    query_embedding = response["embeddings"][0]

    vector = "[" + ",".join(map(str, query_embedding)) + "]"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT

            \"Policy_Number\",

            \"New_IMD_Code\",

            \"renewal_number\",

            \"TBR_Veh_Age\",

            \"STATUS\",

            \"REMARKS\",

            ROUND(
                (
                    (1 - (\"embedding\" <=> %s::vector)
                ) * 100)::numeric,
            2) AS similarity_score

        FROM \"April_Month_Renewals\"

        WHERE \"IMD_Channel\" = %s
        AND \"STATUS\" = \'Lost\'

        ORDER BY \"embedding\" <=> %s::vector;
    """,
    (
        vector,
        imd_channel,
        vector,
    ))

    results = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "category": category,
        "query_used": query,
        "matches_found": len(results),
        "results": results
    }
    


if __name__ == "__main__":
    mcp.run()