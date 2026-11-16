# BizPulse: Sales & Expense Analytics Dashboard

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Unit Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](tests/)

An enterprise financial intelligence and unit-economics dashboard built with Python, Streamlit, and Pandas. It analyzes 24 months of multi-departmental corporate revenue and operational expenses across four commercial regions, computes profit margins, and provides a 3-month predictive linear revenue forecast.

---

## 📌 Features

- **Executive KPI Scorecards**: Instant visibility into Total Gross Revenue, Operating Expenses, Net Operating Profit, and Average Profit Margins.
- **Multidimensional Filtering**: Slice financial records across fiscal years (2024, 2025), commercial territories (North, South, East, West), and organizational units (Engineering, Marketing, Operations, Sales, Support).
- **Time-Series Financial Trajectory**: Interactive trendlines visualizing monthly revenue vs. expense burn rates.
- **YoY & QoQ Variance Analytics**: Computes annual Year-over-Year (2024 vs. 2025) growth variance across Gross Revenue (+20.27%), Operating Expenses, and Net Profit, coupled with sequential Quarter-over-Quarter (QoQ) growth momentum bars and tabular ledgers.
- **Predictive Revenue Forecasting**: Implements Ordinary Least Squares (OLS) linear projection to model quarterly revenue trajectory and growth velocity.
- **Department & Regional Cost Centers**: Compares unit margins and expense distributions to identify high-yield and capital-intensive business divisions.
- **Data Export & Reporting**: Searchable transaction ledger with one-click filtered CSV export.

---

## 🏗️ System Architecture

```text
+-----------------------------+
|  Historical Financial Data  |  (24 Months, 480 Transactions across 5 Departments)
+--------------+--------------+
               |
               v
+-----------------------------+
|      Analytics Engine       |  - KPI Aggregation (Revenue, Expenses, Margins)
|   (analytics_engine.py)     |  - Multi-Dimensional Filtering (Year, Region, Dept)
+--------------+--------------+  - Linear Revenue Forecasting (OLS Trend Modeling)
               |
               v
+-----------------------------+
|    Streamlit Dashboard      |  --> Executive Metric Cards
|          (app.py)           |  --> Monthly Trajectory Charts
+-----------------------------+  --> Departmental Margin Comparison
                                 --> Filtered CSV Export
```

---

## 📂 Project Structure

```text
sales-expense-analytics/
├── app.py                  # Streamlit web dashboard & interactive visualizations
├── analytics_engine.py     # Aggregations, margin formulas, & OLS trend projection
├── generate_data.py        # Generates realistic 24-month multi-department dataset
├── data/
│   └── sales_expense_data.csv
├── tests/
│   └── test_analytics.py   # Unit tests verifying KPIs, aggregations, and forecasts
├── requirements.txt        # Project dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/prachizala/sales-expense-analytics.git
cd sales-expense-analytics
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running Unit Tests

The test suite validates financial math, edge-case handling for empty datasets, and OLS forecasting:

```bash
python -m unittest discover -s tests
```

Expected output:
```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```

---

## 👩‍💻 Author

**Prachi Zala**  
- Bachelor of Computer Applications (BCA) Student, Ahmedabad, Gujarat, India  
- GitHub: [@prachizala](https://github.com/prachizala)  
- Focus: Python, Data Analytics, and Applied Machine Learning
