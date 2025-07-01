"""
Business logic extracted from taipy-app.py for better testability.
This module contains the core data processing functions that can be unit tested.
"""

import pandas as pd
import datetime
from typing import Dict, Any, Optional

def get_partial_visibility(tab_name: str, selected_tab: str) -> str:
    """Determine if a tab should be visible based on selection."""
    return "block" if tab_name == selected_tab else "none"

def load_and_process_csv_data(csv_file_path: str) -> pd.DataFrame:
    """Load and process CSV data with error handling."""
    try:
        raw_data = pd.read_csv(
            csv_file_path,
            parse_dates=["order_date"],
            dayfirst=False,
            low_memory=False
        )
        
        # Check if 'total' column exists and rename to 'revenue' if needed
        if "total" in raw_data.columns:
            raw_data["revenue"] = raw_data["total"]
        elif "revenue" not in raw_data.columns:
            raw_data["revenue"] = raw_data["quantity"] * raw_data["price"]
            
        return raw_data
        
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

def get_categories_list(raw_data: pd.DataFrame) -> list:
    """Get list of categories including 'All Categories'."""
    if raw_data.empty:
        return ["All Categories"]
    
    categories = raw_data["categories"].dropna().unique().tolist()
    return ["All Categories"] + categories

def get_date_range(raw_data: pd.DataFrame) -> tuple:
    """Get start and end dates from the data."""
    if raw_data.empty:
        return datetime.date(2020, 1, 1), datetime.date(2023, 12, 31)
    
    start_date = pd.to_datetime(raw_data["order_date"].min()).date()
    end_date = pd.to_datetime(raw_data["order_date"].max()).date()
    return start_date, end_date

def filter_data_by_date_and_category(
    raw_data: pd.DataFrame, 
    start_date: datetime.date, 
    end_date: datetime.date, 
    selected_category: str
) -> pd.DataFrame:
    """Filter data by date range and category."""
    if raw_data.empty:
        return raw_data
    
    # Filter by date range
    filtered_data = raw_data[
        (raw_data["order_date"] >= pd.to_datetime(start_date)) &
        (raw_data["order_date"] <= pd.to_datetime(end_date))
    ]
    
    # Filter by category if not "All Categories"
    if selected_category != "All Categories":
        filtered_data = filtered_data[filtered_data["categories"] == selected_category]
    
    return filtered_data

def create_revenue_data(filtered_data: pd.DataFrame) -> pd.DataFrame:
    """Create revenue data for line chart."""
    if filtered_data.empty:
        return pd.DataFrame(columns=["order_date", "revenue"])
    
    revenue_by_date = filtered_data.groupby("order_date")["revenue"].sum().reset_index()
    return revenue_by_date.sort_values("order_date")

def create_category_data(filtered_data: pd.DataFrame) -> pd.DataFrame:
    """Create category data for bar chart."""
    if filtered_data.empty:
        return pd.DataFrame(columns=["categories", "revenue"])
    
    category_revenue = filtered_data.groupby("categories")["revenue"].sum().reset_index()
    return category_revenue.sort_values("revenue", ascending=False)

def create_top_products_data(filtered_data: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    """Create top products data for bar chart."""
    if filtered_data.empty:
        return pd.DataFrame(columns=["product_names", "revenue"])
    
    top_products = (
        filtered_data.groupby("product_names")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
        .reset_index()
    )
    return top_products

def calculate_metrics(filtered_data: pd.DataFrame) -> Dict[str, Any]:
    """Calculate key metrics from filtered data."""
    if filtered_data.empty:
        return {
            "total_revenue": "$0.00",
            "total_orders": 0,
            "avg_order_value": "$0.00",
            "top_category": "N/A"
        }
    
    total_revenue = filtered_data["revenue"].sum()
    total_orders = filtered_data["order_id"].nunique()
    avg_order_value = total_revenue / max(total_orders, 1)
    
    # Find top category
    if not filtered_data.empty:
        top_category = filtered_data.groupby("categories")["revenue"].sum().idxmax()
    else:
        top_category = "N/A"
    
    return {
        "total_revenue": f"${total_revenue:,.2f}",
        "total_orders": total_orders,
        "avg_order_value": f"${avg_order_value:,.2f}",
        "top_category": top_category
    }

def process_data_changes(
    raw_data: pd.DataFrame,
    start_date: datetime.date,
    end_date: datetime.date,
    selected_category: str
) -> Dict[str, Any]:
    """Main function to process data changes and return all computed data."""
    # Filter data
    filtered_data = filter_data_by_date_and_category(
        raw_data, start_date, end_date, selected_category
    )
    
    # Create visualization data
    revenue_data = create_revenue_data(filtered_data)
    category_data = create_category_data(filtered_data)
    top_products_data = create_top_products_data(filtered_data)
    
    # Calculate metrics
    metrics = calculate_metrics(filtered_data)
    
    return {
        "filtered_data": filtered_data,
        "revenue_data": revenue_data,
        "category_data": category_data,
        "top_products_data": top_products_data,
        **metrics
    }

def should_apply_changes(var_name: str) -> bool:
    """Determine if changes should be applied based on variable name."""
    return var_name in ["start_date", "end_date", "selected_category"] 