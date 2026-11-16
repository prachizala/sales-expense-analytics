import unittest
import sys
import os

# Add root folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analytics_engine import (
    calculate_kpis,
    filter_records,
    aggregate_by_month,
    aggregate_by_dimension,
    forecast_next_period,
    calculate_period_comparisons
)


class TestAnalyticsEngine(unittest.TestCase):
    """Test suite for financial calculations, aggregations, and forecasts."""

    def setUp(self):
        self.sample_data = [
            {"date": "2024-01-01", "year": 2024, "region": "North", "department": "Sales", "revenue_inr": 100000.0, "expense_inr": 40000.0, "transaction_count": 50},
            {"date": "2024-01-01", "year": 2024, "region": "South", "department": "Engineering", "revenue_inr": 80000.0, "expense_inr": 50000.0, "transaction_count": 30},
            {"date": "2024-02-01", "year": 2024, "region": "North", "department": "Sales", "revenue_inr": 120000.0, "expense_inr": 50000.0, "transaction_count": 60},
            {"date": "2025-01-01", "year": 2025, "region": "East", "department": "Marketing", "revenue_inr": 150000.0, "expense_inr": 60000.0, "transaction_count": 70},
        ]

    def test_calculate_kpis(self):
        kpi = calculate_kpis(self.sample_data)
        self.assertEqual(kpi["total_revenue"], 450000.0)
        self.assertEqual(kpi["total_expense"], 200000.0)
        self.assertEqual(kpi["net_profit"], 250000.0)
        # Margin: (250000 / 450000) * 100 = 55.56%
        self.assertAlmostEqual(kpi["profit_margin_pct"], 55.56, places=1)
        self.assertEqual(kpi["total_transactions"], 210)
        self.assertEqual(kpi["record_count"], 4)

    def test_calculate_kpis_empty(self):
        kpi = calculate_kpis([])
        self.assertEqual(kpi["total_revenue"], 0.0)
        self.assertEqual(kpi["net_profit"], 0.0)
        self.assertEqual(kpi["profit_margin_pct"], 0.0)

    def test_filter_records(self):
        # Filter by year 2024
        res_2024 = filter_records(self.sample_data, year=2024)
        self.assertEqual(len(res_2024), 3)

        # Filter by region North
        res_north = filter_records(self.sample_data, region="North")
        self.assertEqual(len(res_north), 2)

        # Filter by department Sales
        res_sales = filter_records(self.sample_data, department="Sales")
        self.assertEqual(len(res_sales), 2)

        # Multi-filter
        res_multi = filter_records(self.sample_data, year=2024, region="North", department="Sales")
        self.assertEqual(len(res_multi), 2)

    def test_aggregate_by_month(self):
        monthly = aggregate_by_month(self.sample_data)
        self.assertEqual(len(monthly), 3)  # Jan 2024, Feb 2024, Jan 2025
        jan_2024 = monthly[0]
        self.assertEqual(jan_2024["date"], "2024-01-01")
        self.assertEqual(jan_2024["revenue_inr"], 180000.0)
        self.assertEqual(jan_2024["expense_inr"], 90000.0)
        self.assertEqual(jan_2024["net_profit_inr"], 90000.0)

    def test_aggregate_by_dimension(self):
        dept_summary = aggregate_by_dimension(self.sample_data, "department")
        # Sales has 100k + 120k = 220k, should be first
        self.assertEqual(dept_summary[0]["department"], "Sales")
        self.assertEqual(dept_summary[0]["revenue_inr"], 220000.0)
        self.assertEqual(dept_summary[0]["net_profit_inr"], 130000.0)

    def test_forecast_next_period(self):
        # Upward trend series
        series = [
            {"date": "2024-01-01", "revenue_inr": 100000.0},
            {"date": "2024-02-01", "revenue_inr": 120000.0},
            {"date": "2024-03-01", "revenue_inr": 140000.0},
        ]
        forecast = forecast_next_period(series, steps=2)
        # Step +20,000 per period
        self.assertAlmostEqual(forecast["slope"], 20000.0, places=1)
        self.assertEqual(len(forecast["projected_revenues"]), 2)
        # Step 1 should be 160000, Step 2 should be 180000
        self.assertAlmostEqual(forecast["projected_revenues"][0], 160000.0, places=0)
        self.assertAlmostEqual(forecast["projected_revenues"][1], 180000.0, places=0)

    def test_calculate_period_comparisons_empty(self):
        res = calculate_period_comparisons([])
        self.assertEqual(res["yoy"]["revenue_growth_pct"], 0.0)
        self.assertEqual(len(res["qoq"]), 0)

    def test_calculate_period_comparisons_yoy_and_qoq(self):
        records = [
            # 2024-Q1
            {"date": "2024-01-01", "revenue_inr": 100000.0, "expense_inr": 60000.0},
            {"date": "2024-02-01", "revenue_inr": 100000.0, "expense_inr": 60000.0},
            # 2024-Q2
            {"date": "2024-04-01", "revenue_inr": 220000.0, "expense_inr": 120000.0},
            # 2025-Q1
            {"date": "2025-01-01", "revenue_inr": 250000.0, "expense_inr": 150000.0},
            {"date": "2025-02-01", "revenue_inr": 250000.0, "expense_inr": 150000.0},
        ]
        res = calculate_period_comparisons(records)

        # 2024 total rev = 420,000, 2025 total rev = 500,000
        # YoY growth = (500000 - 420000) / 420000 * 100 = 19.05%
        self.assertEqual(res["yoy"]["revenue_2024"], 420000.0)
        self.assertEqual(res["yoy"]["revenue_2025"], 500000.0)
        self.assertAlmostEqual(res["yoy"]["revenue_growth_pct"], 19.05, places=1)

        # QoQ verification
        self.assertGreaterEqual(len(res["qoq"]), 2)
        q1_2024 = res["qoq"][0]
        self.assertEqual(q1_2024["quarter"], "2024-Q1")
        self.assertEqual(q1_2024["revenue_inr"], 200000.0)
        self.assertIsNone(q1_2024["revenue_growth_pct"])  # First quarter has no predecessor

        q2_2024 = res["qoq"][1]
        self.assertEqual(q2_2024["quarter"], "2024-Q2")
        self.assertEqual(q2_2024["revenue_inr"], 220000.0)
        # Growth: (220k - 200k) / 200k = +10.0%
        self.assertAlmostEqual(q2_2024["revenue_growth_pct"], 10.0, places=1)


if __name__ == "__main__":
    unittest.main()
