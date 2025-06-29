# generate the 100000 record CSV file
#
import polars as pl
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any

def get_product_data() -> Dict[str, np.ndarray]:
    """Return product names and their corresponding categories."""
    names = np.asarray(
        [
            "Laptop",
            "Smartphone",
            "Desk",
            "Chair",
            "Monitor",
            "Printer",
            "Paper",
            "Pen",
            "Notebook",
            "Coffee Maker",
            "Cabinet",
            "Plastic Cups",
        ]
    )
    categories = np.asarray(
        [
            "Electronics",
            "Electronics",
            "Office",
            "Office",
            "Electronics",
            "Electronics",
            "Stationery",
            "Stationery",
            "Stationery",
            "Electronics",
            "Office",
            "Sundry",
        ]
    )
    return {"names": names, "categories": categories}

def generate_order_data(nrows: int) -> Dict[str, Any]:
    """Generate order data for the specified number of rows."""
    product_data = get_product_data()
    names = product_data["names"]
    categories = product_data["categories"]
    
    product_id = np.random.randint(len(names), size=nrows)
    quantity = np.random.randint(1, 11, size=nrows)
    price = np.random.randint(199, 10000, size=nrows) / 100
    
    # Generate random dates between 2010-01-01 and 2023-12-31
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = (end_date - start_date).days
    
    # Create random dates as np.array and convert to string format
    order_dates = np.array([
        (start_date + timedelta(days=np.random.randint(0, date_range))).strftime('%Y-%m-%d') 
        for _ in range(nrows)
    ])
    
    # Define columns
    columns = {
        "order_id": np.arange(nrows),
        "order_date": order_dates,
        "customer_id": np.random.randint(100, 1000, size=nrows),
        "customer_name": [f"Customer_{i}" for i in np.random.randint(2**15, size=nrows)],
        "product_id": product_id + 200,
        "product_names": names[product_id],
        "categories": categories[product_id],
        "quantity": quantity,
        "price": price,
        "total": price * quantity,
    }
    
    return columns

def create_dataframe(data: Dict[str, Any]) -> pl.DataFrame:
    """Create a Polars DataFrame from the given data."""
    return pl.DataFrame(data)

def save_to_csv(df: pl.DataFrame, filename: str) -> None:
    """Save the DataFrame to a CSV file."""
    df.write_csv(filename, separator=',', include_header=True)

def generate(nrows: int, filename: str) -> None:
    """Generate sales data and save to CSV file.
    
    Args:
        nrows: Number of rows to generate
        filename: Output CSV filename
    """
    data = generate_order_data(nrows)
    df = create_dataframe(data)
    save_to_csv(df, filename)

# Generate 100,000 rows of data with random order_date and save to CSV
if __name__ == "__main__":
    generate(100_000, "sales_data/sales_data.csv")