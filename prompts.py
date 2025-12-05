def carbon_prompt(total, details):
    return f"""
Act as a sustainability expert.

The user’s daily carbon footprint is **{total:.2f} kg CO₂/day**.

Here are the activity details:
{details}

Please provide:
1. A friendly explanation of where the emissions come from.
2. Three personalized recommendations to reduce CO₂.
3. A simple comparison to average national emissions (keep approximate).
"""
