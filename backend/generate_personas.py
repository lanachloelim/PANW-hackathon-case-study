from datasets import load_dataset
import pandas as pd
import numpy as np
import random
from datetime import datetime

# ------------------------------------
# Load base dataset (for merchant names)
# ------------------------------------
ds = load_dataset("mitulshah/transaction-categorization")
df = pd.DataFrame(ds["train"])

# Filter US-only
df_us = df[df["country"] == "USA"].copy()

# ------------------------------------
# Persona configuration
# ------------------------------------
PERSONA_CONFIG = {
    "student": {
        "monthly_txns": (30, 50),
        "monthly_income_range": (800, 2000)
    },
    "freelancer": {
        "monthly_txns": (40, 70),
        "monthly_income_range": (3000, 8000)
    },
    "saver": {
        "monthly_txns": (25, 45),
        "monthly_income_range": (4000, 7000)
    }
}

# ------------------------------------
# Category amount ranges
# ------------------------------------
AMOUNT_RANGES = {
    "Food & Dining": (5, 50),
    "Transportation": (2, 100),
    "Shopping & Retail": (5, 300),
    "Entertainment & Recreation": (5, 150),
    "Healthcare & Medical": (20, 500),
    "Utilities & Services": (50, 300),
    "Financial Services": (50, 1000),
    "Government & Legal": (50, 500),
    "Charity & Donations": (5, 200)
}

def generate_amount(category):
    low, high = AMOUNT_RANGES.get(category, (5, 50))
    return round(random.uniform(low, high), 2)

# ------------------------------------
# Generate monthly transactions
# ------------------------------------
def generate_persona_transactions(
    persona: str,
    start_year=2022,
    end_year=2024
) -> pd.DataFrame:

    rows = []
    config = PERSONA_CONFIG[persona]

    months = pd.period_range(
        start=f"{start_year}-01",
        end=f"{end_year}-12",
        freq="M"
    )

    expense_pool = df_us[df_us["category"] != "Income"]

    for period in months:
        year, month = period.year, period.month
        n_txns = random.randint(*config["monthly_txns"])

        # ---- Income (1–2 per month) ----
        for _ in range(random.randint(1, 2)):
            rows.append({
                "transaction_description": "Income",
                "category": "Income",
                "country": "USA",
                "currency": "USD",
                "user_id": persona,
                "amount": round(
                    random.uniform(*config["monthly_income_range"]), 2
                ),
                "date": datetime(year, month, random.randint(1, 5))
            })

        # ---- Expenses ----
        sampled = expense_pool.sample(n=n_txns, replace=True)

        for _, row in sampled.iterrows():
            rows.append({
                "transaction_description": row["transaction_description"],
                "category": row["category"],
                "country": "USA",
                "currency": "USD",
                "user_id": persona,
                "amount": generate_amount(row["category"]),
                "date": datetime(year, month, random.randint(1, 28))
            })

    return pd.DataFrame(rows)

# ------------------------------------
# Subscriptions
# ------------------------------------
SUBSCRIPTIONS = {
    "student": [
        ("Netflix", "Entertainment & Recreation", (10, 15)),
        ("Spotify", "Entertainment & Recreation", (5, 10)),
        ("Gym", "Healthcare & Medical", (15, 30))
    ],
    "freelancer": [
        ("Adobe Creative Cloud", "Shopping & Retail", (20, 50)),
        ("Dropbox", "Utilities & Services", (10, 15)),
        ("Spotify", "Entertainment & Recreation", (5, 10))
    ],
    "saver": [
        ("Netflix", "Entertainment & Recreation", (10, 15)),
        ("Gym", "Healthcare & Medical", (20, 40)),
        ("Hulu", "Entertainment & Recreation", (5, 10))
    ]
}

def generate_subscription_transactions(
    persona: str,
    start_year=2022,
    months=36
) -> pd.DataFrame:

    rows = []
    subs = SUBSCRIPTIONS[persona]

    for merchant, category, amount_range in subs:
        for i in range(months):
            year = start_year + (i // 12)
            month = (i % 12) + 1
            rows.append({
                "transaction_description": merchant,
                "category": category,
                "country": "USA",
                "currency": "USD",
                "user_id": persona,
                "amount": round(random.uniform(*amount_range), 2),
                "date": datetime(year, month, random.randint(1, 28))
            })

    return pd.DataFrame(rows)

# ------------------------------------
# Build final dataset
# ------------------------------------
persona_dfs = [
    generate_persona_transactions("student"),
    generate_persona_transactions("freelancer"),
    generate_persona_transactions("saver")
]

subscription_dfs = [
    generate_subscription_transactions("student"),
    generate_subscription_transactions("freelancer"),
    generate_subscription_transactions("saver")
]

final_df = pd.concat(persona_dfs + subscription_dfs)
final_df = final_df.sort_values(["user_id", "date"]).reset_index(drop=True)

final_df.to_csv("us_persona_transactions_with_subscriptions.csv", index=False)

print("✅ Dataset generated successfully")
print(final_df.groupby("user_id").size())
