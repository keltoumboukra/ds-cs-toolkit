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