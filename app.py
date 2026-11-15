"""Enterprise Sales & Expense Analytics Dashboard.

Provides executive financial KPIs, department expense allocations,
regional profitability comparisons, and 3-month linear revenue forecasting.
"""

import os
import streamlit as st
import pandas as pd

from analytics_engine import (
    calculate_kpis,
    filter_records,
    aggregate_by_month,
    aggregate_by_dimension,
    forecast_next_period
)

st.set_page_config(
    page_title="BizPulse: Sales & Expense Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #047857; margin-bottom: 0.2rem; }
    .sub-title { font-size: 1.05rem; color: #4B5563; margin-bottom: 1.5rem; }
    .metric-card { background-color: #F3F4F6; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #047857; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 BizPulse: Sales & Expense Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">24-Month Commercial Financial Health, Unit Economics & Predictive Forecasting | Built by Prachi Zala</div>', unsafe_allow_html=True)

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sales_expense_data.csv")

@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)

df_raw = load_data()

if df_raw.empty:
    st.error("Financial records dataset not found. Please run generate_data.py first.")
    st.stop()

# Sidebar Filters
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/combo-chart.png", width=120)
    st.subheader("🔍 Financial Filters")

    years = ["All"] + sorted([str(y) for y in df_raw["year"].unique()])
    selected_year = st.selectbox("Fiscal Year:", years, index=0)

    regions = ["All"] + sorted(list(df_raw["region"].unique()))
    selected_region = st.selectbox("Commercial Region:", regions, index=0)

    departments = ["All"] + sorted(list(df_raw["department"].unique()))
    selected_dept = st.selectbox("Department:", departments, index=0)

    st.markdown("---")
    st.markdown("### 👩‍💻 Developer")
    st.markdown("**Prachi Zala**  \nBCA Student, Ahmedabad  \n[GitHub Profile](https://github.com/prachizala)")

# Apply filters
records_dict = df_raw.to_dict(orient="records")
filtered_records = filter_records(
    records_dict,
    year=int(selected_year) if selected_year != "All" else None,
    region=selected_region,
    department=selected_dept
)

# High Level KPIs
kpis = calculate_kpis(filtered_records)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Revenue", f"₹{kpis['total_revenue']:,.2f}")
c2.metric("Total Expenses", f"₹{kpis['total_expense']:,.2f}")
c3.metric("Net Profit", f"₹{kpis['net_profit']:,.2f}", delta=f"{kpis['profit_margin_pct']}% margin")
c4.metric("Avg Margin", f"{kpis['profit_margin_pct']:.1f}%")
c5.metric("Transactions", f"{kpis['total_transactions']:,}")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Revenue vs Expense Trajectory",
    "🏢 Department Unit Economics",
    "🗺️ Regional Performance",
    "📑 Detailed Ledger & CSV"
])

# -----------------------------------------------------------------------------
# TAB 1: MONTHLY TRAJECTORY & FORECAST
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Monthly Financial Trajectory (2024 - 2025)")
    monthly_data = aggregate_by_month(filtered_records)

    if monthly_data:
        df_month = pd.DataFrame(monthly_data)
        df_month["date"] = pd.to_datetime(df_month["date"])
        df_month = df_month.set_index("date")

        st.line_chart(df_month[["revenue_inr", "expense_inr", "net_profit_inr"]])

        st.subheader("🔮 3-Month Linear Revenue Forecast")
        forecast = forecast_next_period(monthly_data, steps=3)
        fc1, fc2, fc3 = st.columns(3)
        fc1.metric("Projected Month +1", f"₹{forecast['projected_revenues'][0]:,.2f}")
        fc2.metric("Projected Month +2", f"₹{forecast['projected_revenues'][1]:,.2f}")
        fc3.metric("Projected Month +3", f"₹{forecast['projected_revenues'][2]:,.2f}")

        st.caption(f"Estimated Monthly Growth Slope: ₹{forecast['slope']:+,.2f}/month (~{forecast['average_growth_rate']:.2f}% avg rate)")
    else:
        st.warning("No records found matching the selected filters.")

# -----------------------------------------------------------------------------
# TAB 2: DEPARTMENT BREAKDOWN
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Departmental Revenue & Margin Breakdown")
    dept_summary = aggregate_by_dimension(filtered_records, "department")
    if dept_summary:
        df_dept = pd.DataFrame(dept_summary)
        col_chart, col_tbl = st.columns([1.2, 1])

        with col_chart:
            st.bar_chart(df_dept.set_index("department")[["revenue_inr", "expense_inr"]])

        with col_tbl:
            st.dataframe(
                df_dept.rename(columns={
                    "department": "Department",
                    "revenue_inr": "Revenue (INR)",
                    "expense_inr": "Expense (INR)",
                    "net_profit_inr": "Net Profit",
                    "profit_margin_pct": "Margin %"
                }),
                use_container_width=True
            )

# -----------------------------------------------------------------------------
# TAB 3: REGIONAL PERFORMANCE
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("Commercial Performance Across Geographic Regions")
    region_summary = aggregate_by_dimension(filtered_records, "region")
    if region_summary:
        df_reg = pd.DataFrame(region_summary)
        col_reg_bar, col_reg_tbl = st.columns([1.2, 1])
        with col_reg_bar:
            st.bar_chart(df_reg.set_index("region")[["revenue_inr", "net_profit_inr"]])
        with col_reg_tbl:
            st.dataframe(df_reg, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 4: RAW LEDGER & EXPORT
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("Filtered Financial Transactions Ledger")
    df_filtered = pd.DataFrame(filtered_records)
    st.dataframe(df_filtered, use_container_width=True)

    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Ledger (CSV)",
        data=csv_data,
        file_name="filtered_sales_expense_data.csv",
        mime="text/csv"
    )
