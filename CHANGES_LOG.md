# Changes Log - Work Package 4: Small Feature Upgrades

## Summary of Changes

### 1. Analytics Engine Period Comparison Logic (`analytics_engine.py`)
- Implemented `calculate_period_comparisons(monthly_records: List[Dict[str, Any]]) -> Dict[str, Any]`:
  - Computes Year-over-Year (YoY: 2024 vs 2025) growth metrics for Gross Revenue, Operating Expenses, and Net Operating Profit.
  - Generates chronological Quarter-over-Quarter (QoQ) metrics across 8 fiscal quarters (`2024-Q1` through `2025-Q4`), calculating sequential period revenue growth % and profit growth %.
  - Gracefully handles empty records and zero-revenue edge cases.

### 2. Streamlit Dashboard Integration (`app.py`)
- Added **Tab 4: 📊 YoY & QoQ Variance Analytics**:
  - Highlights FY 2024 vs FY 2025 revenue, expense, and net profit deltas with colored delta metrics.
  - Renders interactive Quarter-over-Quarter revenue growth velocity charts.
  - Renders a clean comparison table detailing quarterly financial performance and period-over-period percentages.
- Shifted raw ledger export to Tab 5.

### 3. Automated Unit Test Suite (`tests/test_analytics.py`)
- Added `test_calculate_period_comparisons_empty` verifying default return schema and boundary handling.
- Added `test_calculate_period_comparisons_yoy_and_qoq` testing mathematical accuracy of YoY revenue growth (+19.05%) and sequential QoQ growth rates.
- All 8 unit tests pass 100% (`Ran 8 tests in 0.001s ... OK`).

### 4. Documentation (`README.md`)
- Updated features list to document the YoY & QoQ Variance Analytics capabilities.

## Items Skipped & Rationale
- None.

## Manual Steps Needed
- None. Run `streamlit run app.py` and open Tab 4 to view the YoY & QoQ analytics.
