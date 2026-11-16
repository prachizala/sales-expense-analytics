"""Financial Analytics & Trend Modeling Engine.

Provides core KPI metrics, department and regional rollups,
margin analysis, and simple linear revenue forecasting.
"""

import math
from typing import List, Dict, Any, Optional
from collections import defaultdict


def calculate_kpis(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Computes high-level financial KPIs across a list of financial entries."""
    if not records:
        return {
            "total_revenue": 0.0,
            "total_expense": 0.0,
            "net_profit": 0.0,
            "profit_margin_pct": 0.0,
            "total_transactions": 0,
            "record_count": 0
        }

    total_revenue = sum(float(r["revenue_inr"]) for r in records)
    total_expense = sum(float(r["expense_inr"]) for r in records)
    net_profit = total_revenue - total_expense
    margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0.0
    total_tx = sum(int(r.get("transaction_count", 0)) for r in records)

    return {
        "total_revenue": round(total_revenue, 2),
        "total_expense": round(total_expense, 2),
        "net_profit": round(net_profit, 2),
        "profit_margin_pct": round(margin, 2),
        "total_transactions": total_tx,
        "record_count": len(records)
    }


def filter_records(
    records: List[Dict[str, Any]],
    year: Optional[int] = None,
    region: Optional[str] = None,
    department: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Filters dataset records according to provided dimensions."""
    filtered = []
    for r in records:
        if year and int(r["year"]) != int(year):
            continue
        if region and region != "All" and r["region"] != region:
            continue
        if department and department != "All" and r["department"] != department:
            continue
        filtered.append(r)
    return filtered


def aggregate_by_month(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Aggregates monthly revenue, expenses, and profits sorted chronologically."""
    monthly_map = defaultdict(lambda: {"revenue": 0.0, "expense": 0.0, "transactions": 0})

    for r in records:
        d = r["date"]
        monthly_map[d]["revenue"] += float(r["revenue_inr"])
        monthly_map[d]["expense"] += float(r["expense_inr"])
        monthly_map[d]["transactions"] += int(r.get("transaction_count", 0))

    sorted_dates = sorted(monthly_map.keys())
    result = []
    for d in sorted_dates:
        rev = round(monthly_map[d]["revenue"], 2)
        exp = round(monthly_map[d]["expense"], 2)
        profit = round(rev - exp, 2)
        margin = round((profit / rev * 100), 2) if rev > 0 else 0.0
        result.append({
            "date": d,
            "revenue_inr": rev,
            "expense_inr": exp,
            "net_profit_inr": profit,
            "profit_margin_pct": margin,
            "transaction_count": monthly_map[d]["transactions"]
        })
    return result


def aggregate_by_dimension(records: List[Dict[str, Any]], dimension_key: str) -> List[Dict[str, Any]]:
    """Groups financial performance by a category dimension (e.g., department, region)."""
    groups = defaultdict(lambda: {"revenue": 0.0, "expense": 0.0})

    for r in records:
        k = r.get(dimension_key, "Unknown")
        groups[k]["revenue"] += float(r["revenue_inr"])
        groups[k]["expense"] += float(r["expense_inr"])

    result = []
    for k, val in groups.items():
        rev = round(val["revenue"], 2)
        exp = round(val["expense"], 2)
        profit = round(rev - exp, 2)
        margin = round((profit / rev * 100), 2) if rev > 0 else 0.0
        result.append({
            dimension_key: k,
            "revenue_inr": rev,
            "expense_inr": exp,
            "net_profit_inr": profit,
            "profit_margin_pct": margin
        })

    # Sort descending by revenue
    result.sort(key=lambda x: x["revenue_inr"], reverse=True)
    return result


def forecast_next_period(monthly_series: List[Dict[str, Any]], steps: int = 3) -> Dict[str, Any]:
    """Performs an Ordinary Least Squares (OLS) linear trend projection for revenue.

    Returns estimated slope, intercept, and forecasted revenue for upcoming periods.
    """
    n = len(monthly_series)
    if n < 2:
        return {
            "slope": 0.0,
            "intercept": 0.0,
            "projected_revenues": [0.0] * steps,
            "average_growth_rate": 0.0
        }

    x_vals = list(range(n))
    y_vals = [m["revenue_inr"] for m in monthly_series]

    x_mean = sum(x_vals) / n
    y_mean = sum(y_vals) / n

    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, y_vals))
    denominator = sum((x - x_mean) ** 2 for x in x_vals)

    slope = numerator / denominator if denominator != 0 else 0.0
    intercept = y_mean - (slope * x_mean)

    projected = []
    for step in range(1, steps + 1):
        future_x = (n - 1) + step
        pred = round(max(0.0, intercept + slope * future_x), 2)
        projected.append(pred)

    avg_growth = round((slope / y_mean * 100), 2) if y_mean > 0 else 0.0

    return {
        "slope": round(slope, 2),
        "intercept": round(intercept, 2),
        "projected_revenues": projected,
        "average_growth_rate": avg_growth
    }


def calculate_period_comparisons(monthly_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Computes Year-over-Year (YoY: 2024 vs 2025) and Quarter-over-Quarter (QoQ) growth analytics.

    Accepts either raw financial transaction records or aggregated monthly entries.
    Returns:
    - yoy: high-level Year-over-Year variance across Revenue, Expense, and Net Profit.
    - qoq: chronologically sorted quarterly records with period-over-period growth rates.
    """
    if not monthly_records:
        return {
            "yoy": {
                "revenue_2024": 0.0,
                "revenue_2025": 0.0,
                "revenue_growth_pct": 0.0,
                "expense_2024": 0.0,
                "expense_2025": 0.0,
                "expense_growth_pct": 0.0,
                "net_profit_2024": 0.0,
                "net_profit_2025": 0.0,
                "profit_growth_pct": 0.0
            },
            "qoq": [],
            "latest_qoq_growth_pct": 0.0
        }

    yearly_data = defaultdict(lambda: {"revenue": 0.0, "expense": 0.0})
    quarterly_data = defaultdict(lambda: {"revenue": 0.0, "expense": 0.0})

    for r in monthly_records:
        date_str = str(r.get("date", ""))
        rev = float(r.get("revenue_inr", 0.0))
        exp = float(r.get("expense_inr", 0.0))

        if "-" in date_str:
            parts = date_str.split("-")
            year = int(parts[0])
            month = int(parts[1])
        else:
            year = int(r.get("year", 2024))
            month = int(r.get("month", 1))

        quarter = (month - 1) // 3 + 1
        q_key = f"{year}-Q{quarter}"

        yearly_data[year]["revenue"] += rev
        yearly_data[year]["expense"] += exp
        quarterly_data[q_key]["revenue"] += rev
        quarterly_data[q_key]["expense"] += exp

    # Year-over-Year metrics (2024 vs 2025)
    rev_2024 = round(yearly_data[2024]["revenue"], 2)
    rev_2025 = round(yearly_data[2025]["revenue"], 2)
    exp_2024 = round(yearly_data[2024]["expense"], 2)
    exp_2025 = round(yearly_data[2025]["expense"], 2)
    profit_2024 = round(rev_2024 - exp_2024, 2)
    profit_2025 = round(rev_2025 - exp_2025, 2)

    rev_growth = round(((rev_2025 - rev_2024) / rev_2024 * 100), 2) if rev_2024 > 0 else 0.0
    exp_growth = round(((exp_2025 - exp_2024) / exp_2024 * 100), 2) if exp_2024 > 0 else 0.0
    profit_growth = round(((profit_2025 - profit_2024) / abs(profit_2024) * 100), 2) if profit_2024 != 0 else 0.0

    # Quarter-over-Quarter metrics
    sorted_quarters = sorted(quarterly_data.keys())
    qoq_list = []
    prev_rev = None
    prev_profit = None

    for q in sorted_quarters:
        q_rev = round(quarterly_data[q]["revenue"], 2)
        q_exp = round(quarterly_data[q]["expense"], 2)
        q_profit = round(q_rev - q_exp, 2)

        rev_growth_pct = round(((q_rev - prev_rev) / prev_rev * 100), 2) if prev_rev and prev_rev > 0 else None
        profit_growth_pct = round(((q_profit - prev_profit) / abs(prev_profit) * 100), 2) if prev_profit and prev_profit != 0 else None

        qoq_list.append({
            "quarter": q,
            "revenue_inr": q_rev,
            "expense_inr": q_exp,
            "net_profit_inr": q_profit,
            "revenue_growth_pct": rev_growth_pct,
            "profit_growth_pct": profit_growth_pct
        })
        prev_rev = q_rev
        prev_profit = q_profit

    latest_qoq = 0.0
    if qoq_list and qoq_list[-1]["revenue_growth_pct"] is not None:
        latest_qoq = qoq_list[-1]["revenue_growth_pct"]

    return {
        "yoy": {
            "revenue_2024": rev_2024,
            "revenue_2025": rev_2025,
            "revenue_growth_pct": rev_growth,
            "expense_2024": exp_2024,
            "expense_2025": exp_2025,
            "expense_growth_pct": exp_growth,
            "net_profit_2024": profit_2024,
            "net_profit_2025": profit_2025,
            "profit_growth_pct": profit_growth
        },
        "qoq": qoq_list,
        "latest_qoq_growth_pct": latest_qoq
    }
