import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import warnings
import os
import tempfile
from cachetools import cached, TTLCache

warnings.filterwarnings("ignore", category=FutureWarning, module="seaborn")

# ------------------------------------------------------------------
# 1) Load CSV data once
# ------------------------------------------------------------------
csv_data = None

def load_csv_data():
    global csv_data
    
    dtype_dict = {
        "order_id": "Int64",
        "customer_id": "Int64",
        "product_id": "Int64",
        "quantity": "Int64",
        "price": "float",
        "total": "float",
        "customer_name": "string",
        "product_names": "string",
        "categories": "string"
    }
    
    csv_data = pd.read_csv(
        "sales_data/sales_data.csv",
        parse_dates=["order_date"],
        dayfirst=True,
        low_memory=False,
        dtype=dtype_dict
    )

load_csv_data()

# ------------------------------------------------------------------
# 2) Cache unique categories
# ------------------------------------------------------------------
cache = TTLCache(maxsize=128, ttl=300)

@cached(cache)
def get_unique_categories():
    global csv_data
    if csv_data is None:
        return []
    cats = sorted(csv_data['categories'].dropna().unique().tolist())
    cats = [cat.capitalize() for cat in cats]
    return cats

def get_date_range():
    global csv_data
    if csv_data is None or csv_data.empty:
        return None, None
    return csv_data['order_date'].min(), csv_data['order_date'].max()

def filter_data(start_date, end_date, category):
    global csv_data

    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    df = csv_data.loc[
        (csv_data['order_date'] >= pd.to_datetime(start_date)) &
        (csv_data['order_date'] <= pd.to_datetime(end_date))
    ].copy()

    if category != "All Categories":
        df = df.loc[df['categories'].str.capitalize() == category].copy()

    return df

def get_dashboard_stats(start_date, end_date, category):
    df = filter_data(start_date, end_date, category)
    if df.empty:
        return (0, 0, 0, "N/A")

    df['revenue'] = df['price'] * df['quantity']
    total_revenue = df['revenue'].sum()
    total_orders = df['order_id'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    cat_revenues = df.groupby('categories')['revenue'].sum().sort_values(ascending=False)
    top_category = cat_revenues.index[0] if not cat_revenues.empty else "N/A"

    return (total_revenue, total_orders, avg_order_value, top_category.capitalize())

def get_data_for_table(start_date, end_date, category):
    df = filter_data(start_date, end_date, category)
    if df.empty:
        return pd.DataFrame()

    df = df.sort_values(by=["order_id", "order_date"], ascending=[True, False]).copy()

    columns_order = [
        "order_id", "order_date", "customer_id", "customer_name",
        "product_id", "product_names", "categories", "quantity",
        "price", "total"
    ]
    columns_order = [col for col in columns_order if col in df.columns]
    df = df[columns_order].copy()

    df['revenue'] = df['price'] * df['quantity']
    return df

def get_plot_data(start_date, end_date, category):
    df = filter_data(start_date, end_date, category)
    if df.empty:
        return pd.DataFrame()
    df['revenue'] = df['price'] * df['quantity']
    plot_data = df.groupby(df['order_date'].dt.date)['revenue'].sum().reset_index()
    plot_data.rename(columns={'order_date': 'date'}, inplace=True)
    return plot_data

# ------------------------------------------------------------------
# 3) Revenue by category
# ------------------------------------------------------------------

def get_revenue_by_category(start_date, end_date, category):
    df = filter_data(start_date, end_date, category)
    if df.empty:
        return pd.DataFrame()
    df['revenue'] = df['price'] * df['quantity']
    cat_data = df.groupby('categories')['revenue'].sum().reset_index()
    cat_data = cat_data.sort_values(by='revenue', ascending=False)
    return cat_data

# ------------------------------------------------------------------
# 4) Top products
# ------------------------------------------------------------------

def get_top_products(start_date, end_date, category):
    df = filter_data(start_date, end_date, category)
    if df.empty:
        return pd.DataFrame()
    df['revenue'] = df['price'] * df['quantity']
    prod_data = df.groupby('product_names')['revenue'].sum().reset_index()
    prod_data = prod_data.sort_values(by='revenue', ascending=False).head(10)
    return prod_data

# ------------------------------------------------------------------
# 5) Create matplotlib figure
# ------------------------------------------------------------------

def create_matplotlib_figure(data, x_col, y_col, title, xlabel, ylabel, orientation='v'):
    plt.figure(figsize=(10, 6))
    if data.empty:
        plt.text(0.5, 0.5, 'No data available', ha='center', va='center')
    else:
        if orientation == 'v':
            plt.bar(data[x_col], data[y_col])
            plt.xticks(rotation=45, ha='right')
        else:
            plt.barh(data[x_col], data[y_col])
            plt.gca().invert_yaxis() 

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        plt.savefig(tmpfile.name)
    plt.close()
    return tmpfile.name

# ------------------------------------------------------------------
# 6) Update dashboard
# ------------------------------------------------------------------

def update_dashboard(start_date, end_date, category):
    total_revenue, total_orders, avg_order_value, top_category = get_dashboard_stats(start_date, end_date, category)

    # Generate plots
    revenue_data = get_plot_data(start_date, end_date, category)
    category_data = get_revenue_by_category(start_date, end_date, category)
    top_products_data = get_top_products(start_date, end_date, category)

    revenue_over_time_path = create_matplotlib_figure(
        revenue_data, 'date', 'revenue',
        "Revenue Over Time", "Date", "Revenue"
    )
    revenue_by_category_path = create_matplotlib_figure(
        category_data, 'categories', 'revenue',
        "Revenue by Category", "Category", "Revenue"
    )
    top_products_path = create_matplotlib_figure(
        top_products_data, 'product_names', 'revenue',
        "Top Products", "Revenue", "Product Name", orientation='h'
    )

    # Data table
    table_data = get_data_for_table(start_date, end_date, category)

    return (
        revenue_over_time_path,
        revenue_by_category_path,
        top_products_path,
        table_data,
        total_revenue,
        total_orders,
        avg_order_value,
        top_category
    )

# ------------------------------------------------------------------
# 7) Create dashboard
# ------------------------------------------------------------------    

def create_dashboard():
    min_date, max_date = get_date_range()
    
    if min_date is None or max_date is None:
        min_date = pd.Timestamp(datetime.datetime.now())
        max_date = pd.Timestamp(datetime.datetime.now())
    else:
        # Ensure they are pandas Timestamp objects
        if isinstance(min_date, str):
            min_date = pd.to_datetime(min_date)
        if isinstance(max_date, str):
            max_date = pd.to_datetime(max_date)

    default_start_date = min_date
    default_end_date = max_date

    with gr.Blocks(css="""
        footer {display: none !important;}
        .tabs {border: none !important;}  
        .gr-plot {border: none !important; box-shadow: none !important;}
    """) as dashboard:
        
        gr.Markdown("# Sales Performance Dashboard")

        # Filters row
        with gr.Row():
            start_date = gr.DateTime(
                label="Start Date",
                value=default_start_date.strftime('%Y-%m-%d'),
                include_time=False,
                type="datetime"
            )
            end_date = gr.DateTime(
                label="End Date",
                value=default_end_date.strftime('%Y-%m-%d'),
                include_time=False,
                type="datetime"
            )
            category_filter = gr.Dropdown(
                choices=["All Categories"] + get_unique_categories(),
                label="Category",
                value="All Categories"
            )

        gr.Markdown("# Key Metrics")

        # Stats row
        with gr.Row():
            total_revenue = gr.Number(label="Total Revenue", value=0)
            total_orders = gr.Number(label="Total Orders", value=0)
            avg_order_value = gr.Number(label="Average Order Value", value=0)
            top_category = gr.Textbox(label="Top Category", value="N/A")

        gr.Markdown("# Visualisations")
        # Tabs for Plots
        with gr.Tabs():
            with gr.Tab("Revenue Over Time"):
                revenue_over_time_image = gr.Image(label="Revenue Over Time", container=False)
            with gr.Tab("Revenue by Category"):
                revenue_by_category_image = gr.Image(label="Revenue by Category", container=False)
            with gr.Tab("Top Products"):
                top_products_image = gr.Image(label="Top Products", container=False)

        gr.Markdown("# Raw Data")
        # Data Table (below the plots)
        data_table = gr.DataFrame(
            label="Sales Data",
            type="pandas",
            interactive=False
        )

        # When filters change, update everything
        for f in [start_date, end_date, category_filter]:
            f.change(
                fn=lambda s, e, c: update_dashboard(s, e, c),
                inputs=[start_date, end_date, category_filter],
                outputs=[
                    revenue_over_time_image, 
                    revenue_by_category_image, 
                    top_products_image,
                    data_table,
                    total_revenue, 
                    total_orders,
                    avg_order_value, 
                    top_category
                ]
            )

        # Initial load
        dashboard.load(
            fn=lambda: update_dashboard(default_start_date.strftime('%Y-%m-%d'), default_end_date.strftime('%Y-%m-%d'), "All Categories"),
            outputs=[
                revenue_over_time_image, 
                revenue_by_category_image, 
                top_products_image,
                data_table,
                total_revenue, 
                total_orders,
                avg_order_value, 
                top_category
            ]
        )

    return dashboard

if __name__ == "__main__":
    dashboard = create_dashboard()
    dashboard.launch(share=True)