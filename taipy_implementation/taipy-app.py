from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd
import datetime
from taipy_logic import (
    load_and_process_csv_data,
    get_categories_list,
    get_date_range,
    process_data_changes,
    should_apply_changes
)

# Load CSV data
csv_file_path = r"sales_data/sales_data.csv"

# Load and process data using the logic module
raw_data = load_and_process_csv_data(csv_file_path)

# Get categories and date range using the logic module
categories = get_categories_list(raw_data)
start_date, end_date = get_date_range(raw_data)

# Initialize state variables
selected_category = "All Categories"
selected_tab = "Revenue Over Time"
total_revenue = "$0.00"
total_orders = 0
avg_order_value = "$0.00"
top_category = "N/A"
revenue_data = pd.DataFrame(columns=["order_date", "revenue"])
category_data = pd.DataFrame(columns=["categories", "revenue"])
top_products_data = pd.DataFrame(columns=["product_names", "revenue"])

def apply_changes(state):
    """Apply changes using the logic module."""
    try:
        # Use the logic module to process data changes
        result = process_data_changes(
            raw_data, state.start_date, state.end_date, state.selected_category
        )
        
        # Update state with results
        state.raw_data = result["filtered_data"]
        state.revenue_data = result["revenue_data"]
        state.category_data = result["category_data"]
        state.top_products_data = result["top_products_data"]
        state.total_revenue = result["total_revenue"]
        state.total_orders = result["total_orders"]
        state.avg_order_value = result["avg_order_value"]
        state.top_category = result["top_category"]
        
        print(f"Updated metrics - Revenue: {state.total_revenue}, Orders: {state.total_orders}")
        
    except Exception as e:
        print(f"Error in apply_changes: {e}")
        import traceback
        traceback.print_exc()

def on_change(state, var_name, var_value):
    """Handle state changes from UI controls"""
    print(f"State change detected: {var_name} = {var_value}")
    
    # Use the logic module to determine if changes should be applied
    if should_apply_changes(var_name):
        apply_changes(state)

def on_init(state):
    """Initialize the app when it first loads"""
    print("Initializing app...")
    apply_changes(state)

def get_partial_visibility(tab_name, selected_tab):
    """Determine if a tab should be visible based on selection."""
    return "block" if tab_name == selected_tab else "none"

with tgb.Page() as page:
    tgb.text("# Sales Performance Dashboard", mode="md")
    
    # Filters section
    with tgb.part(class_name="card"):
        with tgb.layout(columns="1 1 2"):  # Arrange elements in 3 columns
            with tgb.part():
                tgb.text("Filter From:")
                tgb.date("{start_date}")
            with tgb.part():
                tgb.text("To:")
                tgb.date("{end_date}")
            with tgb.part():
                tgb.text("Filter by Category:")
                tgb.selector(
                    value="{selected_category}",
                    lov=categories,
                    dropdown=True,
                    width="300px"
                )
   
    # Metrics section
    tgb.text("## Key Metrics", mode="md")
    with tgb.layout(columns="1 1 1 1"):
        with tgb.part(class_name="metric-card"):
            tgb.text("### Total Revenue", mode="md")
            tgb.text("{total_revenue}")
        with tgb.part(class_name="metric-card"):
            tgb.text("### Total Orders", mode="md")
            tgb.text("{total_orders}")
        with tgb.part(class_name="metric-card"):
            tgb.text("### Average Order Value", mode="md")
            tgb.text("{avg_order_value}")
        with tgb.part(class_name="metric-card"):
            tgb.text("### Top Category", mode="md")
            tgb.text("{top_category}")

    tgb.text("## Visualizations", mode="md")
    # Selector for visualizations with reduced width
    with tgb.part(style="width: 50%;"):  # Reduce width of the dropdown
        tgb.selector(
            value="{selected_tab}",
            lov=["Revenue Over Time", "Revenue by Category", "Top Products"],
            dropdown=True,
            width="360px",  # Reduce width of the dropdown
        )

    # Conditional rendering of charts based on selected_tab
    with tgb.part(render="{selected_tab == 'Revenue Over Time'}"):
        tgb.chart(
            data="{revenue_data}",
            x="order_date",
            y="revenue",
            type="line",
            title="Revenue Over Time",
        )

    with tgb.part(render="{selected_tab == 'Revenue by Category'}"):
        tgb.chart(
            data="{category_data}",
            x="categories",
            y="revenue",
            type="bar",
            title="Revenue by Category",
        )

    with tgb.part(render="{selected_tab == 'Top Products'}"):
        tgb.chart(
            data="{top_products_data}",
            x="product_names",
            y="revenue",
            type="bar",
            title="Top Products",
        )

    # Raw Data Table
    tgb.text("## Raw Data", mode="md")
    tgb.table(data="{raw_data}")

Gui(page).run(
    title="Sales Dashboard",
    dark_mode=False,
    debug=True,
    port="auto",
    allow_unsafe_werkzeug=True,
    async_mode="threading"
)