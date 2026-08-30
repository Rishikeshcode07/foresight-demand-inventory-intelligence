import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Project FORESIGHT", layout="wide", page_icon="📦")

DATA_DIR = Path(__file__).parent / "data"


@st.cache_data
def load_data():
    weekly = pd.read_parquet(DATA_DIR / "weekly_sku_features.parquet")
    risk = pd.read_parquet(DATA_DIR / "risk_scores.parquet")
    forecast = pd.read_parquet(DATA_DIR / "forecast_vs_actual.parquet")
    return weekly, risk, forecast


try:
    weekly, risk, forecast = load_data()
except FileNotFoundError as e:
    st.error(
        "Data files not found. Make sure weekly_sku_features.parquet, risk_scores.parquet, "
        f"and forecast_vs_actual.parquet are in a 'data/' folder next to app.py.\n\n{e}"
    )
    st.stop()

st.sidebar.title("Project FORESIGHT")
st.sidebar.caption("Demand & Inventory Intelligence")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Sales Analytics", "Forecast", "Inventory", "Risk Dashboard", "Product Details", "Executive Summary"],
)

CATEGORIES = sorted(weekly["category"].dropna().unique().tolist())


def wape(actual, pred):
    actual, pred = np.asarray(actual, dtype=float), np.asarray(pred, dtype=float)
    denom = np.abs(actual).sum()
    return np.abs(actual - pred).sum() / denom if denom > 0 else np.nan


# ---------------------------------------------------------------- HOME
if page == "Home":
    st.title("NorthBay Living — Demand & Inventory Intelligence")
    st.caption(f"Data through {weekly['week_start'].max().date()}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"Rs. {weekly['revenue'].sum()/1e6:,.1f}M")
    c2.metric("Total Units Sold", f"{weekly['units_sold'].sum():,.0f}")
    c3.metric("SKUs Flagged 'Reorder Now'", int((risk["decision"] == "Reorder now").sum()) if len(risk) else 0)
    c4.metric("SKUs Flagged 'Markdown/Clear'", int((risk["decision"] == "Markdown/clear").sum()) if len(risk) else 0)

    st.subheader("Revenue Trend")
    monthly = (
        weekly.assign(month=weekly["week_start"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)["revenue"].sum()
    )
    st.plotly_chart(px.line(monthly, x="month", y="revenue", title="Monthly Revenue"), width='stretch')

    st.subheader("Inventory Risk at a Glance")
    if len(risk):
        decision_counts = risk["decision"].value_counts().reset_index()
        decision_counts.columns = ["decision", "count"]
        st.plotly_chart(
            px.pie(decision_counts, names="decision", values="count", title="SKU Risk Distribution"),
            width='stretch',
        )
    else:
        st.info("No risk data available yet.")

# ---------------------------------------------------------- SALES ANALYTICS
elif page == "Sales Analytics":
    st.title("Sales Analytics")

    selected_categories = st.multiselect("Filter by category", CATEGORIES, default=CATEGORIES)
    filtered = weekly[weekly["category"].isin(selected_categories)] if selected_categories else weekly.iloc[0:0]

    if filtered.empty:
        st.warning("No data for the selected filters. Choose at least one category.")
    else:
        c1, c2 = st.columns(2)
        c1.metric("Revenue (filtered)", f"Rs. {filtered['revenue'].sum()/1e6:,.1f}M")
        c2.metric("Units Sold (filtered)", f"{filtered['units_sold'].sum():,.0f}")

        trend = filtered.groupby("week_start", as_index=False)["revenue"].sum()
        st.plotly_chart(px.line(trend, x="week_start", y="revenue", title="Weekly Revenue"), width='stretch')

        by_cat = filtered.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
        st.plotly_chart(
            px.bar(by_cat, x="revenue", y="category", orientation="h", title="Revenue by Category"),
            width='stretch',
        )

        promo_effect = filtered.groupby("promo_flag", as_index=False)["units_sold"].mean()
        promo_effect["promo_flag"] = promo_effect["promo_flag"].map({True: "Promo week", False: "No promo"})
        st.plotly_chart(
            px.bar(promo_effect, x="promo_flag", y="units_sold", title="Avg. Units Sold: Promo vs. No Promo"),
            width='stretch',
        )

# ---------------------------------------------------------------- FORECAST
elif page == "Forecast":
    st.title("Demand Forecast")
    st.caption("Model performance on the most recent backtest window (never seen during training).")

    if forecast.empty:
        st.info("No forecast data available yet.")
    else:
        model_wape = wape(forecast["units_sold"], forecast["predicted_units"])
        c1, c2 = st.columns(2)
        c1.metric("Model WAPE (lower is better)", f"{model_wape:.1%}" if pd.notna(model_wape) else "N/A")
        c2.caption("WAPE = total forecast error as a share of total actual demand.")

        sku_options = sorted(forecast["sku_id"].unique().tolist())
        selected_sku = st.selectbox("Choose a SKU to inspect", sku_options)

        sku_data = forecast[forecast["sku_id"] == selected_sku].sort_values("week_start")
        if sku_data.empty:
            st.warning("No forecast history for this SKU.")
        else:
            chart_data = sku_data.melt(
                id_vars="week_start", value_vars=["units_sold", "predicted_units"],
                var_name="series", value_name="units",
            )
            chart_data["series"] = chart_data["series"].map({"units_sold": "Actual", "predicted_units": "Forecast"})
            st.plotly_chart(
                px.line(chart_data, x="week_start", y="units", color="series",
                        title=f"Actual vs. Forecast — {selected_sku}"),
                width='stretch',
            )

# --------------------------------------------------------------- INVENTORY
elif page == "Inventory":
    st.title("Inventory Position")

    if risk.empty:
        st.info("No inventory data available yet.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Stock on Hand", f"{risk['total_stock_on_hand'].sum():,.0f} units")
        c2.metric("Total Safety Stock", f"{risk['total_safety_stock'].sum():,.0f} units")
        c3.metric("SKUs Tracked", f"{len(risk):,}")

        valid_weeks = risk["weeks_of_stock_on_hand"].dropna()
        if len(valid_weeks):
            st.plotly_chart(
                px.histogram(
                    risk, x="weeks_of_stock_on_hand", nbins=50,
                    title="Distribution: Weeks of Stock on Hand per SKU",
                    range_x=[0, valid_weeks.quantile(0.95)],
                ),
                width='stretch',
            )
        else:
            st.info("No stock-coverage data to chart.")

        st.subheader("Full Inventory Table")
        st.dataframe(
            risk[["sku_id", "total_stock_on_hand", "total_safety_stock", "total_reorder_point",
                  "expected_weekly_demand", "weeks_of_stock_on_hand", "decision"]]
            .sort_values("weeks_of_stock_on_hand"),
            width='stretch',
        )

# ----------------------------------------------------------- RISK DASHBOARD
elif page == "Risk Dashboard":
    st.title("Stockout & Overstock Risk")

    if risk.empty:
        st.info("No risk data available yet.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Reorder now", int((risk["decision"] == "Reorder now").sum()))
        c2.metric("Markdown/clear", int((risk["decision"] == "Markdown/clear").sum()))
        c3.metric("Watch/volatile", int((risk["decision"] == "Watch/volatile").sum()))
        c4.metric("Healthy", int((risk["decision"] == "Healthy").sum()))

        decision_filter = st.selectbox("Show list for:", ["Reorder now", "Markdown/clear", "Watch/volatile", "Healthy"])
        subset = risk[risk["decision"] == decision_filter].sort_values("expected_weekly_demand", ascending=False)

        if subset.empty:
            st.info(f"No SKUs currently in '{decision_filter}'.")
        else:
            st.dataframe(
                subset[["sku_id", "total_stock_on_hand", "total_safety_stock",
                        "expected_weekly_demand", "weeks_of_stock_on_hand"]],
                width='stretch',
            )
        st.caption(
            "Risk rules validated against the dataset's own ground-truth answer key "
            "(sku_inventory_flags.csv) — see the Week 3 report for precision/recall figures."
        )

# ---------------------------------------------------------- PRODUCT DETAILS
elif page == "Product Details":
    st.title("Product Details")

    all_skus = sorted(weekly["sku_id"].unique().tolist())
    selected_sku = st.selectbox("Search for a SKU", all_skus)

    sku_weekly = weekly[weekly["sku_id"] == selected_sku].sort_values("week_start")
    sku_risk = risk[risk["sku_id"] == selected_sku] if len(risk) else risk

    if sku_weekly.empty:
        st.warning("No sales history for this SKU.")
    else:
        info = sku_weekly.iloc[-1]
        c1, c2, c3 = st.columns(3)
        c1.metric("Category", info["category"])
        c2.metric("Brand", info["brand"])
        c3.metric("List Price", f"Rs. {info['unit_price']:,.2f}")

        st.plotly_chart(
            px.line(sku_weekly, x="week_start", y="units_sold", title="Weekly Units Sold"),
            width='stretch',
        )

        if len(sku_risk):
            r = sku_risk.iloc[0]
            st.subheader("Current Risk Status")
            st.write(f"**Decision:** {r['decision']}")
            st.write(
                f"Stock on hand: {r['total_stock_on_hand']:,.0f} units | "
                f"Safety stock: {r['total_safety_stock']:,.0f} units | "
                f"Expected weekly demand: {r['expected_weekly_demand']:,.1f} units"
            )
        else:
            st.info("No current inventory snapshot for this SKU.")

# --------------------------------------------------------- EXECUTIVE SUMMARY
elif page == "Executive Summary":
    st.title("Executive Summary")
    st.caption("Project FORESIGHT — Demand & Inventory Intelligence")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue Analyzed", f"Rs. {weekly['revenue'].sum()/1e9:,.2f}B")
    c2.metric("SKUs at Stockout Risk", int((risk["decision"] == "Reorder now").sum()) if len(risk) else 0)
    c3.metric("SKUs Overstocked", int((risk["decision"] == "Markdown/clear").sum()) if len(risk) else 0)

    st.markdown(
        """
**Key findings:**
- Revenue is heavily concentrated: the top 20% of SKUs generate roughly 73% of total revenue.
- A weekly, SKU-level demand forecast was built and backtested against a seasonal-naive baseline
  across three rolling windows, beating the baseline on every window.
- Stockout and overstock risk scoring was validated directly against this dataset's own
  ground-truth answer key, rather than left as an unverified assumption.
- Recommended actions are prioritised below by expected weekly demand — see the Risk Dashboard
  page for the full, filterable list.
"""
    )

    if len(risk):
        top_priority = (
            risk[risk["decision"] == "Reorder now"]
            .sort_values("expected_weekly_demand", ascending=False)
            .head(10)
        )
        if not top_priority.empty:
            st.subheader("Top 10 Priority Reorders")
            st.dataframe(
                top_priority[["sku_id", "total_stock_on_hand", "expected_weekly_demand"]],
                width='stretch',
            )
        else:
            st.info("No SKUs currently flagged for reorder.")
