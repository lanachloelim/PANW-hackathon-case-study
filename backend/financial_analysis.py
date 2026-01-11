import pandas as pd
from collections import defaultdict

CSV_PATH = "data/us_persona_transactions_with_subscriptions.csv"
df = pd.read_csv(CSV_PATH, parse_dates=["date"])

df["amount"] = df["amount"].astype(float)
df["month"] = df["date"].dt.to_period("M").astype(str)

all_months = sorted(df["month"].unique())
latest_month = all_months[-1]
last_6_months = all_months[-6:]
last_12_months = all_months[-12:]


def sort_and_round_categories(cat_dict: dict) -> dict:
    return dict(
        sorted(
            ((k, round(v, 2)) for k, v in cat_dict.items()),
            key=lambda x: x[1],
            reverse=True
        )
    )


def detect_recent_gray_charges(user_df: pd.DataFrame) -> list:
    """
    Detect subscriptions / gray charges that were synthetically injected:
    - Same merchant
    - Same (or very similar) amount
    - Appears in >= 3 of the last 6 months
    """

    recent_df = user_df[
        (user_df["month"].isin(last_6_months)) &
        (user_df["category"] != "Income")
    ].copy()

    grouped = (
        recent_df
        .groupby(["transaction_description", "category"])
        .agg(
            months_active=("month", "nunique"),
            avg_amount=("amount", "mean"),
            last_seen=("date", "max")
        )
        .reset_index()
    )

    # Threshold: appears in at least half of last 6 months
    subs = grouped[grouped["months_active"] >= 3]

    results = []
    for _, row in subs.iterrows():
        latest_txn = recent_df[
            recent_df["transaction_description"] == row["transaction_description"]
        ].sort_values("date", ascending=False).iloc[0]

        results.append({
            "merchant": row["transaction_description"],
            "category": row["category"],
            "average_amount": round(row["avg_amount"], 2),
            "months_detected": int(row["months_active"]),
            "last_charge_date": latest_txn["date"],
            "last_charge_amount": round(latest_txn["amount"], 2)
        })

    return sorted(
        results,
        key=lambda x: x["last_charge_date"],
        reverse=True
    )


def get_user_financial_summary(user_id: str) -> dict:
    if user_id not in df["user_id"].unique():
        raise ValueError(f"User ID '{user_id}' not found in dataset.")

    user_all = df[df["user_id"] == user_id].copy()

    # -----------------------------
    # Month-by-month summary
    # -----------------------------
    month_summary = {}
    for month in all_months:
        subset = user_all[user_all["month"] == month]

        income_total = subset[subset["category"] == "Income"]["amount"].sum()
        expenses_total = subset[subset["category"] != "Income"]["amount"].sum()
        net_total = income_total - expenses_total

        raw_category_breakdown = (
            subset[subset["category"] != "Income"]
            .groupby("category")["amount"]
            .sum()
            .to_dict()
        )

        category_breakdown = sort_and_round_categories(raw_category_breakdown)

        month_summary[month] = {
            "income": round(income_total, 2),
            "expenses": round(expenses_total, 2),
            "net": round(net_total, 2),
            "category_breakdown": category_breakdown
        }

    # -----------------------------
    # Aggregate summaries
    # -----------------------------
    def aggregate_summary(months):
        inc = sum(month_summary[m]["income"] for m in months)
        exp = sum(month_summary[m]["expenses"] for m in months)
        net = sum(month_summary[m]["net"] for m in months)

        avg_inc = inc / len(months)
        avg_exp = exp / len(months)
        avg_net = net / len(months)

        combined_categories = defaultdict(float)
        for m in months:
            for cat, amt in month_summary[m]["category_breakdown"].items():
                combined_categories[cat] += amt

        combined_categories = sort_and_round_categories(combined_categories)

        return {
            "income": round(inc, 2),
            "expenses": round(exp, 2),
            "net": round(net, 2),
            "average_income": round(avg_inc, 2),
            "average_expenses": round(avg_exp, 2),
            "average_net": round(avg_net, 2),
            "category_breakdown": combined_categories
        }

    # -----------------------------
    # Final summaries
    # -----------------------------
    last_12_months_summary = aggregate_summary(last_12_months)
    last_6_months_summary = aggregate_summary(last_6_months)
    latest_month_summary = aggregate_summary([latest_month])

    # -----------------------------
    # Recent transactions
    # -----------------------------
    recent_transactions = (
        user_all.sort_values("date", ascending=False)
        .head(10)[["date", "transaction_description", "category", "amount"]]
        .to_dict(orient="records")
    )

    # -----------------------------
    # Gray charges / subscriptions
    # -----------------------------
    recent_gray_charges = detect_recent_gray_charges(user_all)

    return {
        "user_id": user_id,
        "latest_month": latest_month,
        "month_by_month": month_summary,
        "latest_month_summary": latest_month_summary,
        "last_6_months_summary": last_6_months_summary,
        "last_12_months_summary": last_12_months_summary,
        "recent_transactions": recent_transactions,
        "recent_gray_charges": recent_gray_charges
    }
