"""
Unit tests for data_generation module.

This module demonstrates best practices for unit testing:
1. Test isolation - each test is independent
2. Descriptive test names - clearly state what is being tested
3. Arrange-Act-Assert pattern - setup, execute, verify
4. Edge case testing - test boundary conditions
5. Mocking external dependencies when needed
6. Type hints and docstrings for clarity
"""

import pytest
import numpy as np
import polars as pl
from datetime import datetime
from unittest.mock import patch, mock_open
import tempfile
import os

# Import the functions we want to test
from taipy_implementation.data_generation import (
    get_product_data,
    generate_order_data,
    create_dataframe,
    save_to_csv,
    generate
)


class TestGetProductData:
    """Test cases for the get_product_data function."""
    
    def test_returns_expected_structure(self):
        """Test that get_product_data returns the expected dictionary structure."""
        # Arrange & Act
        result = get_product_data()
        
        # Assert
        assert isinstance(result, dict)
        assert "names" in result
        assert "categories" in result
        assert isinstance(result["names"], np.ndarray)
        assert isinstance(result["categories"], np.ndarray)
    
    def test_names_and_categories_have_same_length(self):
        """Test that names and categories arrays have the same length."""
        # Arrange & Act
        result = get_product_data()
        
        # Assert
        assert len(result["names"]) == len(result["categories"])
    
    def test_contains_expected_products(self):
        """Test that the product data contains expected product names."""
        # Arrange & Act
        result = get_product_data()
        
        # Assert
        expected_products = ["Laptop", "Smartphone", "Desk", "Chair", "Monitor"]
        for product in expected_products:
            assert product in result["names"]
    
    def test_contains_expected_categories(self):
        """Test that the product data contains expected categories."""
        # Arrange & Act
        result = get_product_data()
        
        # Assert
        expected_categories = ["Electronics", "Office", "Stationery", "Sundry"]
        for category in expected_categories:
            assert category in result["categories"]


class TestGenerateOrderData:
    """Test cases for the generate_order_data function."""
    
    def test_returns_expected_structure(self):
        """Test that generate_order_data returns the expected dictionary structure."""
        # Arrange
        nrows = 10
        
        # Act
        result = generate_order_data(nrows)
        
        # Assert
        assert isinstance(result, dict)
        expected_columns = [
            "order_id", "order_date", "customer_id", "customer_name",
            "product_id", "product_names", "categories", "quantity", "price", "total"
        ]
        for column in expected_columns:
            assert column in result
    
    def test_generates_correct_number_of_rows(self):
        """Test that the function generates the correct number of rows."""
        # Arrange
        nrows = 50
        
        # Act
        result = generate_order_data(nrows)
        
        # Assert
        for key, value in result.items():
            if isinstance(value, (list, np.ndarray)):
                assert len(value) == nrows
    
    def test_order_id_is_sequential(self):
        """Test that order_id values are sequential starting from 0."""
        # Arrange
        nrows = 10
        
        # Act
        result = generate_order_data(nrows)
        
        # Assert
        expected_order_ids = list(range(nrows))
        assert list(result["order_id"]) == expected_order_ids
    
    def test_quantity_bounds(self):
        """Test that quantity values are within expected bounds (1-10)."""
        # Arrange
        nrows = 100
        
        # Act
        result = generate_order_data(nrows)
        
        # Assert
        quantities = result["quantity"]
        assert all(1 <= q <= 10 for q in quantities)
    
    def test_price_bounds(self):
        """Test that price values are within expected bounds (1.99-100.00)."""
        # Arrange
        nrows = 100
        
        # Act
        result = generate_order_data(nrows)
        
        # Assert
        prices = result["price"]
        assert all(1.99 <= p <= 100.00 for p in prices)
    
    def test_total_calculation(self):
        """Test that total is correctly calculated as price * quantity."""
        # Arrange
        nrows = 10
        
        # Act
        result = generate_order_data(nrows)
        
        # Assert
        for i in range(nrows):
            expected_total = result["price"][i] * result["quantity"][i]
            assert abs(result["total"][i] - expected_total) < 0.01
    
    def test_date_format(self):
        """Test that dates are in the correct format (YYYY-MM-DD)."""
        # Arrange
        nrows = 10
        
        # Act
        result = generate_order_data(nrows)
        
        # Assert
        for date_str in result["order_date"]:
            # Try to parse the date string
            datetime.strptime(date_str, '%Y-%m-%d')
    
    def test_date_range(self):
        """Test that dates are within the expected range (2010-2023)."""
        # Arrange
        nrows = 100
        
        # Act
        result = generate_order_data(nrows)
        
        # Assert
        start_date = datetime(2010, 1, 1)
        end_date = datetime(2023, 12, 31)
        
        for date_str in result["order_date"]:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            assert start_date <= date_obj <= end_date
    
    def test_customer_id_bounds(self):
        """Test that customer_id values are within expected bounds (100-999)."""
        # Arrange
        nrows = 100
        
        # Act
        result = generate_order_data(nrows)
        
        # Assert
        customer_ids = result["customer_id"]
        assert all(100 <= cid <= 999 for cid in customer_ids)
    
    def test_product_id_bounds(self):
        """Test that product_id values are within expected bounds (200+)."""
        # Arrange
        nrows = 100
        
        # Act
        result = generate_order_data(nrows)
        
        # Assert
        product_ids = result["product_id"]
        assert all(pid >= 200 for pid in product_ids)
    
    def test_zero_rows(self):
        """Test edge case: generating data with 0 rows."""
        # Arrange
        nrows = 0
        
        # Act
        result = generate_order_data(nrows)
        
        # Assert
        for key, value in result.items():
            if isinstance(value, (list, np.ndarray)):
                assert len(value) == 0


class TestCreateDataframe:
    """Test cases for the create_dataframe function."""
    
    def test_creates_polars_dataframe(self):
        """Test that create_dataframe returns a Polars DataFrame."""
        # Arrange
        test_data = {
            "col1": [1, 2, 3],
            "col2": ["a", "b", "c"]
        }
        
        # Act
        result = create_dataframe(test_data)
        
        # Assert
        assert isinstance(result, pl.DataFrame)
    
    def test_dataframe_has_correct_columns(self):
        """Test that the DataFrame has the expected columns."""
        # Arrange
        test_data = {
            "col1": [1, 2, 3],
            "col2": ["a", "b", "c"]
        }
        
        # Act
        result = create_dataframe(test_data)
        
        # Assert
        assert result.columns == ["col1", "col2"]
    
    def test_dataframe_has_correct_data(self):
        """Test that the DataFrame contains the correct data."""
        # Arrange
        test_data = {
            "col1": [1, 2, 3],
            "col2": ["a", "b", "c"]
        }
        
        # Act
        result = create_dataframe(test_data)
        
        # Assert
        assert result["col1"].to_list() == [1, 2, 3]
        assert result["col2"].to_list() == ["a", "b", "c"]
    
    def test_empty_data(self):
        """Test edge case: creating DataFrame with empty data."""
        # Arrange
        test_data = {}
        
        # Act
        result = create_dataframe(test_data)
        
        # Assert
        assert isinstance(result, pl.DataFrame)
        assert len(result.columns) == 0


class TestSaveToCsv:
    """Test cases for the save_to_csv function."""
    
    def test_saves_dataframe_to_csv(self):
        """Test that save_to_csv successfully writes a DataFrame to CSV."""
        # Arrange
        test_data = {
            "col1": [1, 2, 3],
            "col2": ["a", "b", "c"]
        }
        df = pl.DataFrame(test_data)
        
        # Use a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            filename = tmp_file.name
        
        try:
            # Act
            save_to_csv(df, filename)
            
            # Assert
            assert os.path.exists(filename)
            
            # Verify file contents
            with open(filename, 'r') as f:
                content = f.read()
                assert "col1,col2" in content  # Header
                assert "1,a" in content  # Data
                assert "2,b" in content
                assert "3,c" in content
        
        finally:
            # Cleanup
            if os.path.exists(filename):
                os.unlink(filename)
    
    def test_creates_file_with_header(self):
        """Test that the CSV file includes headers."""
        # Arrange
        test_data = {"col1": [1], "col2": ["a"]}
        df = pl.DataFrame(test_data)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            filename = tmp_file.name
        
        try:
            # Act
            save_to_csv(df, filename)
            
            # Assert
            with open(filename, 'r') as f:
                first_line = f.readline().strip()
                assert first_line == "col1,col2"
        
        finally:
            if os.path.exists(filename):
                os.unlink(filename)


class TestGenerate:
    """Test cases for the main generate function."""
    
    @patch('taipy_implementation.data_generation.save_to_csv')
    @patch('taipy_implementation.data_generation.create_dataframe')
    @patch('taipy_implementation.data_generation.generate_order_data')
    def test_generate_calls_functions_in_order(self, mock_generate_data, mock_create_df, mock_save):
        """Test that generate calls the helper functions in the correct order."""
        # Arrange
        nrows = 10
        filename = "test.csv"
        mock_data = {"test": "data"}
        mock_df = pl.DataFrame(mock_data)
        
        mock_generate_data.return_value = mock_data
        mock_create_df.return_value = mock_df
        
        # Act
        generate(nrows, filename)
        
        # Assert
        mock_generate_data.assert_called_once_with(nrows)
        mock_create_df.assert_called_once_with(mock_data)
        mock_save.assert_called_once_with(mock_df, filename)
    
    def test_generate_creates_valid_csv_file(self):
        """Integration test: verify that generate creates a valid CSV file."""
        # Arrange
        nrows = 5
        filename = "test_sales.csv"
        
        try:
            # Act
            generate(nrows, filename)
            
            # Assert
            assert os.path.exists(filename)
            
            # Verify file structure
            with open(filename, 'r') as f:
                lines = f.readlines()
                assert len(lines) == nrows + 1  # +1 for header
                
                # Check header
                header = lines[0].strip()
                expected_columns = [
                    "order_id", "order_date", "customer_id", "customer_name",
                    "product_id", "product_names", "categories", "quantity", "price", "total"
                ]
                for column in expected_columns:
                    assert column in header
        
        finally:
            # Cleanup
            if os.path.exists(filename):
                os.unlink(filename)


# Test fixtures for common test data
@pytest.fixture
def sample_order_data():
    """Fixture providing sample order data for testing."""
    return {
        "order_id": [0, 1, 2],
        "order_date": ["2020-01-01", "2020-01-02", "2020-01-03"],
        "customer_id": [100, 101, 102],
        "customer_name": ["Customer_1", "Customer_2", "Customer_3"],
        "product_id": [200, 201, 202],
        "product_names": ["Laptop", "Smartphone", "Desk"],
        "categories": ["Electronics", "Electronics", "Office"],
        "quantity": [1, 2, 3],
        "price": [999.99, 599.99, 299.99],
        "total": [999.99, 1199.98, 899.97]
    }


@pytest.fixture
def sample_dataframe(sample_order_data):
    """Fixture providing a sample Polars DataFrame for testing."""
    return pl.DataFrame(sample_order_data)


# Parameterized tests for better coverage
@pytest.mark.parametrize("nrows", [0, 1, 10, 100])
def test_generate_order_data_various_sizes(nrows):
    """Test generate_order_data with various row counts."""
    result = generate_order_data(nrows)
    
    for key, value in result.items():
        if isinstance(value, (list, np.ndarray)):
            assert len(value) == nrows


@pytest.mark.parametrize("invalid_nrows", [-1, -10])
def test_generate_order_data_invalid_sizes(invalid_nrows):
    """Test that generate_order_data handles invalid row counts appropriately."""
    # This should raise an error for negative values
    with pytest.raises(ValueError):
        generate_order_data(invalid_nrows) 