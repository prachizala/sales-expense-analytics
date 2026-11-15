"""Dataset Generator for Sales & Expense Analytics Dashboard.

Synthesizes realistic 24-month multi-department financial logs
across 4 commercial regions with revenue, operational expenses, and margins.
"""

import csv
import os
import random

def generate_financial_records(num_months: int = 24) -> list:
    random.seed(42)
    departments = ["Engineering", "Marketing", "Operations", "Sales", "Support"]
    regions = ["North", "South", "East", "West"]
    categories = {
        "Engineering": ["Cloud Infrastructure", "Dev Tools", "Hardware"],
        "Marketing": ["Digital Ads", "Events & PR", "Content Creation"],
        "Operations": ["Office Rent", "Logistics", "Utilities"],
        "Sales": ["Client Dinners", "Travel & Stays", "CRM Software"],
        "Support": ["Helpdesk Licenses", "Telephony", "Training"]
    }

    records = []
    # Dates from 2024-01 to 2025-12
    for m_idx in range(num_months):
        year = 2024 + (m_idx // 12)
        month = (m_idx % 12) + 1
        date_str = f"{year}-{month:02d}-01"

        # Growth factor over time
        growth = 1.0 + (m_idx * 0.02)

        for dept in departments:
            for region in regions:
                cat = random.choice(categories[dept])
                base_rev = random.randint(180000, 420000) * growth
                # Marketing and Sales generate direct revenue, others support operations
                if dept in ["Sales", "Marketing"]:
                    revenue = round(base_rev * 1.5, 2)
                elif dept == "Engineering":
                    revenue = round(base_rev * 1.1, 2)
                else:
                    revenue = round(base_rev * 0.8, 2)

                base_exp = random.randint(75000, 240000) * (growth * 0.95)
                expense = round(base_exp, 2)
                profit = round(revenue - expense, 2)
                margin_pct = round((profit / revenue) * 100, 2) if revenue > 0 else 0.0
                tx_count = random.randint(35, 180)

                records.append({
                    "date": date_str,
                    "year": year,
                    "month": month,
                    "region": region,
                    "department": dept,
                    "category": cat,
                    "revenue_inr": revenue,
                    "expense_inr": expense,
                    "net_profit_inr": profit,
                    "profit_margin_pct": margin_pct,
                    "transaction_count": tx_count
                })

    return records


def main():
    records = generate_financial_records()
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "sales_expense_data.csv")

    headers = [
        "date", "year", "month", "region", "department", "category",
        "revenue_inr", "expense_inr", "net_profit_inr", "profit_margin_pct", "transaction_count"
    ]

    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} financial records at: {csv_path}")


if __name__ == "__main__":
    main()
