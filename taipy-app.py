from taipy.gui import Gui
import taipy.gui.builder as tgb
import pandas as pd
import datetime

# Load CSV data
csv_file_path = r"sales_data/sales_data.csv"

try:
    raw_data = pd.read_csv(
        csv_file_path,
        parse_dates=["order_date"],
        dayfirst=False,  # Changed from True to False
        low_memory=False  # Suppress dtype warning
    )
    # Check if 'total' column exists and rename to 'revenue' if needed
    if "total" in raw_data.columns:
        raw_data["revenue"] = raw_data["total"]
    elif "revenue" not in raw_data.columns:
        raw_data["revenue"] = raw_data["quantity"] * raw_data["price"]
    print(f"Data loaded successfully: {raw_data.shape[0]} rows")
    print(f"Columns: {raw_data.columns.tolist()}")
    print(f"Date range: {raw_data['order_date'].min()} to {raw_data['order_date'].max()}")
except Exception as e:
    print(f"Error loading CSV: {e}")
    raw_data = pd.DataFrame()

categories = ["All Categories"] + raw_data["categories"].dropna().unique().tolist()

# Define the visualization options as a proper list
chart_options = ["Revenue Over Time", "Revenue by Category", "Top Products"]

# Convert string dates to datetime objects first
start_date = pd.to_datetime(raw_data["order_date"].min()).date() if not raw_data.empty else datetime.date(2020, 1, 1)
end_date = pd.to_datetime(raw_data["order_date"].max()).date() if not raw_data.empty else datetime.date(2023, 12, 31)
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
    try:
        filtered_data = raw_data[
            (raw_data["order_date"] >= pd.to_datetime(state.start_date)) &
            (raw_data["order_date"] <= pd.to_datetime(state.end_date))
        ]
        if state.selected_category != "All Categories":
            filtered_data = filtered_data[filtered_data["categories"] == state.selected_category]

        # Ensure we have data to work with
        if filtered_data.empty:
            print("No data found for the selected filters")
            state.revenue_data = pd.DataFrame(columns=["order_date", "revenue"])
            state.category_data = pd.DataFrame(columns=["categories", "revenue"])
            state.top_products_data = pd.DataFrame(columns=["product_names", "revenue"])
            state.raw_data = filtered_data
            state.total_revenue = "$0.00"
            state.total_orders = 0
            state.avg_order_value = "$0.00"
            state.top_category = "N/A"
            return

        # Create revenue data for line chart
        revenue_by_date = filtered_data.groupby("order_date")["revenue"].sum().reset_index()
        state.revenue_data = revenue_by_date.sort_values("order_date")
        print("Revenue Data:")
        print(state.revenue_data.head())

        # Create category data for bar chart
        category_revenue = filtered_data.groupby("categories")["revenue"].sum().reset_index()
        state.category_data = category_revenue.sort_values("revenue", ascending=False)
        print("Category Data:")
        print(state.category_data.head())

        # Create top products data
        top_products = (
            filtered_data.groupby("product_names")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        state.top_products_data = top_products
        print("Top Products Data:")
        print(state.top_products_data.head())

        # Update metrics
        state.raw_data = filtered_data
        state.total_revenue = f"${filtered_data['revenue'].sum():,.2f}"
        state.total_orders = filtered_data["order_id"].nunique()
        state.avg_order_value = f"${filtered_data['revenue'].sum() / max(filtered_data['order_id'].nunique(), 1):,.2f}"
        state.top_category = (
            filtered_data.groupby("categories")["revenue"].sum().idxmax()
            if not filtered_data.empty else "N/A"
        )
        
        print(f"Updated metrics - Revenue: {state.total_revenue}, Orders: {state.total_orders}")
        
    except Exception as e:
        print(f"Error in apply_changes: {e}")
        import traceback
        traceback.print_exc()

def on_change(state, var_name, var_value):
    """Handle state changes from UI controls"""
    print(f"State change detected: {var_name} = {var_value}")
    
    # Only apply changes for filter-related variables
    if var_name in ["start_date", "end_date", "selected_category"]:
        apply_changes(state)
    # For selected_tab, we don't need to recalculate data, just update the display

def on_init(state):
    """Initialize the app when it first loads"""
    print("Initializing app...")
    apply_changes(state)

def get_partial_visibility(tab_name, selected_tab):
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