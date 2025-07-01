import pytest
import pandas as pd
import datetime
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import taipy_logic
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from taipy_implementation.taipy_logic import (
    get_partial_visibility,
    load_and_process_csv_data,
    get_categories_list,
    get_date_range,
    filter_data_by_date_and_category,
    create_revenue_data,
    create_category_data,
    create_top_products_data,
    calculate_metrics,
    process_data_changes,
    should_apply_changes
)

class TestTaipyLogic:
    """Test cases for taipy_logic.py functions."""
    
    def setup_method(self):
        """Set up test data before each test."""
        # Create sample data for testing
        self.sample_data = pd.DataFrame({
            'order_id': [1, 2, 3, 4, 5, 6, 7, 8],
            'order_date': pd.to_datetime([
                '2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04',
                '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08'
            ]),
            'customer_id': [100, 101, 102, 103, 104, 105, 106, 107],
            'customer_name': ['Customer_1', 'Customer_2', 'Customer_3', 'Customer_4',
                             'Customer_5', 'Customer_6', 'Customer_7', 'Customer_8'],
            'product_id': [201, 202, 203, 204, 205, 206, 207, 208],
            'product_names': ['Laptop', 'Smartphone', 'Desk', 'Chair', 'Monitor',
                             'Printer', 'Paper', 'Pen'],
            'categories': ['Electronics', 'Electronics', 'Office', 'Office', 'Electronics',
                          'Electronics', 'Stationery', 'Stationery'],
            'quantity': [1, 2, 1, 3, 1, 1, 10, 5],
            'price': [999.99, 599.99, 299.99, 199.99, 399.99, 299.99, 9.99, 1.99],
            'total': [999.99, 1199.98, 299.99, 599.97, 399.99, 299.99, 99.90, 9.95],
            'revenue': [999.99, 1199.98, 299.99, 599.97, 399.99, 299.99, 99.90, 9.95]
        })

    def test_get_partial_visibility_matching_tab(self):
        """Test get_partial_visibility when tab names match."""
        result = get_partial_visibility("Revenue Over Time", "Revenue Over Time")
        assert result == "block"
    
    def test_get_partial_visibility_non_matching_tab(self):
        """Test get_partial_visibility when tab names don't match."""
        result = get_partial_visibility("Revenue Over Time", "Revenue by Category")
        assert result == "none"
    
    def test_get_partial_visibility_with_different_tabs(self):
        """Test get_partial_visibility with various tab combinations."""
        assert get_partial_visibility("Top Products", "Top Products") == "block"
        assert get_partial_visibility("Revenue by Category", "Top Products") == "none"
        assert get_partial_visibility("Revenue Over Time", "Revenue by Category") == "none"

    @patch('pandas.read_csv')
    def test_load_and_process_csv_data_success(self, mock_read_csv):
        """Test successful CSV data loading."""
        mock_read_csv.return_value = self.sample_data
        
        result = load_and_process_csv_data("test.csv")
        
        assert not result.empty
        assert "revenue" in result.columns
        assert len(result) == 8
        mock_read_csv.assert_called_once()

    @patch('pandas.read_csv')
    def test_load_and_process_csv_data_failure(self, mock_read_csv):
        """Test CSV data loading failure."""
        mock_read_csv.side_effect = FileNotFoundError("File not found")
        
        result = load_and_process_csv_data("nonexistent.csv")
        
        assert result.empty
        mock_read_csv.assert_called_once()

    @patch('pandas.read_csv')
    def test_load_and_process_csv_data_calculate_revenue(self, mock_read_csv):
        """Test CSV loading when revenue needs to be calculated."""
        data_without_revenue = self.sample_data.drop(columns=['revenue'])
        mock_read_csv.return_value = data_without_revenue
        
        result = load_and_process_csv_data("test.csv")
        
        assert not result.empty
        assert "revenue" in result.columns
        # Revenue should be calculated as quantity * price
        expected_revenue = data_without_revenue['quantity'] * data_without_revenue['price']
        pd.testing.assert_series_equal(result['revenue'], expected_revenue, check_names=False)

    def test_get_categories_list_with_data(self):
        """Test getting categories list from data."""
        result = get_categories_list(self.sample_data)
        
        expected_categories = ["All Categories", "Electronics", "Office", "Stationery"]
        assert result == expected_categories

    def test_get_categories_list_empty_data(self):
        """Test getting categories list from empty data."""
        empty_data = pd.DataFrame()
        result = get_categories_list(empty_data)
        
        assert result == ["All Categories"]

    def test_get_date_range_with_data(self):
        """Test getting date range from data."""
        start_date, end_date = get_date_range(self.sample_data)
        
        assert start_date == datetime.date(2023, 1, 1)
        assert end_date == datetime.date(2023, 1, 8)

    def test_get_date_range_empty_data(self):
        """Test getting date range from empty data."""
        empty_data = pd.DataFrame()
        start_date, end_date = get_date_range(empty_data)
        
        assert start_date == datetime.date(2020, 1, 1)
        assert end_date == datetime.date(2023, 12, 31)

    def test_filter_data_by_date_and_category_all_categories(self):
        """Test filtering data with 'All Categories' selected."""
        start_date = datetime.date(2023, 1, 2)
        end_date = datetime.date(2023, 1, 6)
        
        result = filter_data_by_date_and_category(
            self.sample_data, start_date, end_date, "All Categories"
        )
        
        assert len(result) == 5  # 5 rows in date range
        assert result['order_date'].min() >= pd.to_datetime('2023-01-02')
        assert result['order_date'].max() <= pd.to_datetime('2023-01-06')

    def test_filter_data_by_date_and_category_specific_category(self):
        """Test filtering data with specific category."""
        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date(2023, 1, 8)
        
        result = filter_data_by_date_and_category(
            self.sample_data, start_date, end_date, "Electronics"
        )
        
        assert len(result) == 4  # 4 Electronics items
        assert all(cat == "Electronics" for cat in result['categories'])

    def test_filter_data_by_date_and_category_no_matches(self):
        """Test filtering data with no matches."""
        start_date = datetime.date(2024, 1, 1)
        end_date = datetime.date(2024, 1, 5)
        
        result = filter_data_by_date_and_category(
            self.sample_data, start_date, end_date, "All Categories"
        )
        
        assert len(result) == 0

    def test_filter_data_by_date_and_category_empty_data(self):
        """Test filtering empty data."""
        empty_data = pd.DataFrame()
        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date(2023, 1, 5)
        
        result = filter_data_by_date_and_category(
            empty_data, start_date, end_date, "All Categories"
        )
        
        assert result.empty

    def test_create_revenue_data_with_data(self):
        """Test creating revenue data from filtered data."""
        result = create_revenue_data(self.sample_data)
        
        assert not result.empty
        assert list(result.columns) == ["order_date", "revenue"]
        assert len(result) == 8  # 8 unique dates
        assert result['revenue'].sum() == self.sample_data['revenue'].sum()

    def test_create_revenue_data_empty_data(self):
        """Test creating revenue data from empty data."""
        empty_data = pd.DataFrame()
        result = create_revenue_data(empty_data)
        
        assert result.empty
        assert list(result.columns) == ["order_date", "revenue"]

    def test_create_category_data_with_data(self):
        """Test creating category data from filtered data."""
        result = create_category_data(self.sample_data)
        
        assert not result.empty
        assert list(result.columns) == ["categories", "revenue"]
        assert len(result) == 3  # 3 categories
        # Should be sorted by revenue descending
        assert result['revenue'].iloc[0] >= result['revenue'].iloc[1]

    def test_create_category_data_empty_data(self):
        """Test creating category data from empty data."""
        empty_data = pd.DataFrame()
        result = create_category_data(empty_data)
        
        assert result.empty
        assert list(result.columns) == ["categories", "revenue"]

    def test_create_top_products_data_with_data(self):
        """Test creating top products data from filtered data."""
        result = create_top_products_data(self.sample_data, limit=5)
        
        assert not result.empty
        assert list(result.columns) == ["product_names", "revenue"]
        assert len(result) == 5  # Limited to 5 products
        # Should be sorted by revenue descending
        assert result['revenue'].iloc[0] >= result['revenue'].iloc[1]

    def test_create_top_products_data_empty_data(self):
        """Test creating top products data from empty data."""
        empty_data = pd.DataFrame()
        result = create_top_products_data(empty_data)
        
        assert result.empty
        assert list(result.columns) == ["product_names", "revenue"]

    def test_calculate_metrics_with_data(self):
        """Test calculating metrics from filtered data."""
        result = calculate_metrics(self.sample_data)
        
        assert "total_revenue" in result
        assert "total_orders" in result
        assert "avg_order_value" in result
        assert "top_category" in result
        
        assert result["total_orders"] == 8
        assert result["top_category"] == "Electronics"  # Highest revenue category
        assert result["total_revenue"].startswith("$")

    def test_calculate_metrics_empty_data(self):
        """Test calculating metrics from empty data."""
        empty_data = pd.DataFrame()
        result = calculate_metrics(empty_data)
        
        assert result["total_revenue"] == "$0.00"
        assert result["total_orders"] == 0
        assert result["avg_order_value"] == "$0.00"
        assert result["top_category"] == "N/A"

    def test_process_data_changes_complete_flow(self):
        """Test the complete data processing flow."""
        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date(2023, 1, 8)
        
        result = process_data_changes(
            self.sample_data, start_date, end_date, "All Categories"
        )
        
        # Check all expected keys are present
        expected_keys = [
            "filtered_data", "revenue_data", "category_data", 
            "top_products_data", "total_revenue", "total_orders", 
            "avg_order_value", "top_category"
        ]
        for key in expected_keys:
            assert key in result
        
        # Check data is processed correctly
        assert len(result["filtered_data"]) == 8
        assert not result["revenue_data"].empty
        assert not result["category_data"].empty
        assert not result["top_products_data"].empty
        assert result["total_orders"] == 8

    def test_process_data_changes_with_category_filter(self):
        """Test data processing with category filter."""
        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date(2023, 1, 8)
        
        result = process_data_changes(
            self.sample_data, start_date, end_date, "Electronics"
        )
        
        assert len(result["filtered_data"]) == 4  # Only Electronics
        assert result["top_category"] == "Electronics"

    def test_process_data_changes_no_matches(self):
        """Test data processing with no matching data."""
        start_date = datetime.date(2024, 1, 1)
        end_date = datetime.date(2024, 1, 5)
        
        result = process_data_changes(
            self.sample_data, start_date, end_date, "All Categories"
        )
        
        assert len(result["filtered_data"]) == 0
        assert result["total_revenue"] == "$0.00"
        assert result["total_orders"] == 0

    def test_should_apply_changes_filter_variables(self):
        """Test should_apply_changes with filter variables."""
        assert should_apply_changes("start_date") == True
        assert should_apply_changes("end_date") == True
        assert should_apply_changes("selected_category") == True

    def test_should_apply_changes_non_filter_variables(self):
        """Test should_apply_changes with non-filter variables."""
        assert should_apply_changes("selected_tab") == False
        assert should_apply_changes("total_revenue") == False
        assert should_apply_changes("random_variable") == False

    def test_edge_case_single_row_data(self):
        """Test processing with single row of data."""
        single_row_data = self.sample_data.head(1)
        
        result = process_data_changes(
            single_row_data, 
            datetime.date(2023, 1, 1), 
            datetime.date(2023, 1, 1), 
            "All Categories"
        )
        
        assert len(result["filtered_data"]) == 1
        assert result["total_orders"] == 1
        assert result["avg_order_value"] == result["total_revenue"]

    def test_edge_case_zero_quantity_price(self):
        """Test processing with zero quantity/price data."""
        zero_data = self.sample_data.copy()
        zero_data.loc[0, 'quantity'] = 0
        zero_data.loc[0, 'price'] = 0
        zero_data.loc[0, 'total'] = 0
        zero_data.loc[0, 'revenue'] = 0
        
        result = calculate_metrics(zero_data)
        
        assert result["total_orders"] == 8
        assert result["total_revenue"].startswith("$") 