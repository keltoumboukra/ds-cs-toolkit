# Taipy Sales Dashboard

A comprehensive sales performance dashboard built with Taipy, featuring interactive visualizations, data filtering, and real-time metrics calculation.

## Features

- **Interactive Dashboard**: Real-time sales performance visualization
- **Data Filtering**: Filter by date range and product categories
- **Multiple Visualizations**: 
  - Revenue over time (line chart)
  - Revenue by category (bar chart)
  - Top products (bar chart)
- **Key Metrics**: Total revenue, orders, average order value, and top category
- **Data Generation**: Generate synthetic sales data for testing
- **Comprehensive Testing**: 58 tests with 97% code coverage

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data (Optional)
If you don't have sales data, generate sample data:
```bash
python data_generation.py
```

### 3. Run the Dashboard
```bash
python taipy-app.py
```

The dashboard will open in your browser at `http://localhost:5000`

## Project Structure

```
taipy_implementation/
├── taipy-app.py              # Main Taipy application
├── taipy_logic.py            # Business logic and data processing
├── data_generation.py        # Synthetic data generation
├── sales_data/               # Data directory
│   └── sales_data.csv        # Sample sales data
├── tests/                    # Test suite
│   ├── test_taipy_logic.py   # Business logic tests (29 tests)
│   └── test_data_generation.py # Data generation tests (29 tests)
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Testing

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Tests with Coverage
```bash
python -m pytest tests/ --cov=. --cov-report=term-missing
```

### Run Specific Test Files
```bash
# Business logic tests
python -m pytest tests/test_taipy_logic.py -v

# Data generation tests
python -m pytest tests/test_data_generation.py -v
```

## Data Format

The application expects CSV data with the following columns:
- `order_id`: Unique order identifier
- `order_date`: Date of the order (YYYY-MM-DD format)
- `customer_id`: Customer identifier
- `customer_name`: Customer name
- `product_id`: Product identifier
- `product_names`: Product name
- `categories`: Product category
- `quantity`: Quantity ordered
- `price`: Unit price
- `total` or `revenue`: Total revenue for the order

## Key Functions

### Business Logic (`taipy_logic.py`)
- `load_and_process_csv_data()`: Load and validate CSV data
- `filter_data_by_date_and_category()`: Filter data by date range and category
- `process_data_changes()`: Main function for processing data changes
- `calculate_metrics()`: Calculate key performance metrics

### Data Generation (`data_generation.py`)
- `generate_order_data()`: Generate synthetic order data
- `generate()`: Generate and save data to CSV file

## Configuration

The application can be configured by modifying:
- Data file path in `taipy-app.py`
- Date ranges and categories in the UI
- Chart types and visualizations
- Number of records in data generation

## Troubleshooting

### Import Errors
Make sure you're running commands from the `taipy_implementation` directory:
```bash
cd taipy_implementation
python taipy-app.py
```

### Missing Dependencies
Install all required packages:
```bash
pip install -r requirements.txt
```

### Data Issues
If the dashboard shows no data:
1. Check that `sales_data/sales_data.csv` exists
2. Verify the CSV format matches the expected schema
3. Generate new sample data if needed

## Performance

- **Data Loading**: Optimized for datasets up to 100,000 records
- **Filtering**: Real-time filtering with minimal latency
- **Visualizations**: Responsive charts that update instantly
- **Memory Usage**: Efficient data processing with pandas

## Contributing

1. Follow the existing code structure
2. Add tests for new functionality
3. Maintain 97%+ code coverage
4. Update documentation for any changes

## License

This project is part of the ds-cs-toolkit collection. 