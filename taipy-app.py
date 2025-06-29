from taipy.gui import Gui
import pandas as pd
import datetime

# Load CSV data
csv_file_path = r"sales_data/sales_data.csv"

try:
    raw_data = pd.read_csv(
        csv_file_path,
        parse_dates=["order_date"],
        dayfirst=True,
        low_memory=False  # Suppress dtype warning
    )
    if "revenue" not in raw_data.columns:
        raw_data["revenue"] = raw_data["quantity"] * raw_data["price"]
    print(f"Data loaded successfully: {raw_data.shape[0]} rows")
except Exception as e:
    print(f"Error loading CSV: {e}")
    raw_data = pd.DataFrame()

categories = ["All Categories"] + raw_data["categories"].dropna().unique().tolist()

# Define the visualization options as a proper list
chart_options = ["Revenue Over Time", "Revenue by Category", "Top Products"]

start_date = raw_data["order_date"].min().date() if not raw_data.empty else datetime.date(2020, 1, 1)
end_date = raw_data["order_date"].max().date() if not raw_data.empty else datetime.date(2023, 12, 31)
selected_category = "All Categories"
selected_tab = "Revenue Over Time"  # Set default selected tab
total_revenue = "$0.00"
total_orders = 0
avg_order_value = "$0.00"
top_category = "N/A"
revenue_data = pd.DataFrame(columns=["order_date", "revenue"])
category_data = pd.DataFrame(columns=["categories", "revenue"])
top_products_data = pd.DataFrame(columns=["product_names", "revenue"])

def apply_changes(state):
    filtered_data = raw_data[
        (raw_data["order_date"] >= pd.to_datetime(state.start_date)) &
        (raw_data["order_date"] <= pd.to_datetime(state.end_date))
    ]
    if state.selected_category != "All Categories":
        filtered_data = filtered_data[filtered_data["categories"] == state.selected_category]

    state.revenue_data = filtered_data.groupby("order_date")["revenue"].sum().reset_index()
    state.revenue_data.columns = ["order_date", "revenue"]
    print("Revenue Data:")
    print(state.revenue_data.head())

    state.category_data = filtered_data.groupby("categories")["revenue"].sum().reset_index()
    state.category_data.columns = ["categories", "revenue"]
    print("Category Data:")
    print(state.category_data.head())

    state.top_products_data = (
        filtered_data.groupby("product_names")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    state.top_products_data.columns = ["product_names", "revenue"]
    print("Top Products Data:")
    print(state.top_products_data.head())

    state.raw_data = filtered_data
    state.total_revenue = f"${filtered_data['revenue'].sum():,.2f}"
    state.total_orders = filtered_data["order_id"].nunique()
    state.avg_order_value = f"${filtered_data['revenue'].sum() / max(filtered_data['order_id'].nunique(), 1):,.2f}"
    state.top_category = (
        filtered_data.groupby("categories")["revenue"].sum().idxmax()
        if not filtered_data.empty else "N/A"
    )

def on_change(state, var_name, var_value):
    if var_name in {"start_date", "end_date", "selected_category", "selected_tab"}:
        print(f"State change detected: {var_name} = {var_value}")  # Debugging
        apply_changes(state)

def on_init(state):
    apply_changes(state)

import taipy.gui.builder as tgb

def get_partial_visibility(tab_name, selected_tab):
    return "block" if tab_name == selected_tab else "none"

