"""
Example test file demonstrating basic unit testing concepts.

This file contains simple examples that you can use as templates
for writing your own tests. Each example shows a different testing pattern.
"""

import pytest
from typing import List, Dict, Any


# ============================================================================
# Example 1: Testing Simple Functions
# ============================================================================

def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b


def divide_numbers(a: int, b: int) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


class TestSimpleFunctions:
    """Test cases for simple mathematical functions."""
    
    def test_add_numbers_positive(self):
        """Test adding two positive numbers."""
        # Arrange
        a = 5
        b = 3
        
        # Act
        result = add_numbers(a, b)
        
        # Assert
        assert result == 8
    
    def test_add_numbers_negative(self):
        """Test adding negative numbers."""
        result = add_numbers(-5, -3)
        assert result == -8
    
    def test_add_numbers_zero(self):
        """Test adding with zero."""
        result = add_numbers(5, 0)
        assert result == 5
    
    def test_multiply_numbers(self):
        """Test multiplication."""
        result = multiply_numbers(4, 5)
        assert result == 20
    
    def test_divide_numbers_success(self):
        """Test successful division."""
        result = divide_numbers(10, 2)
        assert result == 5.0
    
    def test_divide_numbers_by_zero(self):
        """Test that division by zero raises an exception."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide_numbers(10, 0)


# ============================================================================
# Example 2: Testing Data Processing Functions
# ============================================================================

def process_list(numbers: List[int]) -> List[int]:
    """Double each number in the list."""
    return [num * 2 for num in numbers]


def filter_even_numbers(numbers: List[int]) -> List[int]:
    """Filter out odd numbers, keeping only even ones."""
    return [num for num in numbers if num % 2 == 0]


def calculate_average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)


class TestDataProcessing:
    """Test cases for data processing functions."""
    
    def test_process_list_normal(self):
        """Test processing a normal list of numbers."""
        input_data = [1, 2, 3, 4]
        expected = [2, 4, 6, 8]
        result = process_list(input_data)
        assert result == expected
    
    def test_process_list_empty(self):
        """Test processing an empty list."""
        result = process_list([])
        assert result == []
    
    def test_process_list_single_item(self):
        """Test processing a list with one item."""
        result = process_list([5])
        assert result == [10]
    
    def test_filter_even_numbers(self):
        """Test filtering even numbers."""
        input_data = [1, 2, 3, 4, 5, 6]
        expected = [2, 4, 6]
        result = filter_even_numbers(input_data)
        assert result == expected
    
    def test_filter_even_numbers_no_evens(self):
        """Test filtering when no even numbers exist."""
        input_data = [1, 3, 5, 7]
        result = filter_even_numbers(input_data)
        assert result == []
    
    def test_calculate_average_normal(self):
        """Test calculating average of normal list."""
        input_data = [1.0, 2.0, 3.0, 4.0]
        result = calculate_average(input_data)
        assert result == 2.5
    
    def test_calculate_average_empty_list(self):
        """Test that average calculation fails for empty list."""
        with pytest.raises(ValueError, match="Cannot calculate average of empty list"):
            calculate_average([])


# ============================================================================
# Example 3: Testing with Fixtures
# ============================================================================

@pytest.fixture
def sample_user_data():
    """Provide sample user data for testing."""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }


@pytest.fixture
def sample_numbers():
    """Provide sample numbers for testing."""
    return [1, 2, 3, 4, 5]


def validate_user_data(user_data: Dict[str, Any]) -> bool:
    """Validate user data has required fields."""
    required_fields = ["name", "email", "age"]
    return all(field in user_data for field in required_fields)


def count_positive_numbers(numbers: List[int]) -> int:
    """Count how many positive numbers are in the list."""
    return len([num for num in numbers if num > 0])


class TestWithFixtures:
    """Test cases demonstrating fixture usage."""
    
    def test_validate_user_data_valid(self, sample_user_data):
        """Test validation with valid user data."""
        result = validate_user_data(sample_user_data)
        assert result is True
    
    def test_validate_user_data_missing_field(self, sample_user_data):
        """Test validation with missing field."""
        # Remove a required field
        del sample_user_data["email"]
        result = validate_user_data(sample_user_data)
        assert result is False
    
    def test_count_positive_numbers(self, sample_numbers):
        """Test counting positive numbers."""
        result = count_positive_numbers(sample_numbers)
        assert result == 5  # All numbers in sample_numbers are positive
    
    def test_count_positive_numbers_with_negatives(self):
        """Test counting positive numbers with negative numbers present."""
        numbers = [-1, 0, 1, -2, 3]
        result = count_positive_numbers(numbers)
        assert result == 2  # Only 1 and 3 are positive


# ============================================================================
# Example 4: Parameterized Tests
# ============================================================================

def is_palindrome(text: str) -> bool:
    """Check if a string is a palindrome."""
    # Remove spaces and convert to lowercase
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def square_root(number: float) -> float:
    """Calculate the square root of a number."""
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return number ** 0.5


@pytest.mark.parametrize("input_text,expected", [
    ("racecar", True),
    ("A man a plan a canal Panama", True),
    ("hello", False),
    ("", True),  # Empty string is considered palindrome
    ("a", True),  # Single character is palindrome
    ("12321", True),
    ("12345", False),
])
def test_is_palindrome(input_text, expected):
    """Test palindrome detection with various inputs."""
    result = is_palindrome(input_text)
    assert result == expected


@pytest.mark.parametrize("input_number,expected", [
    (4, 2.0),
    (9, 3.0),
    (16, 4.0),
    (0, 0.0),
    (1, 1.0),
])
def test_square_root_valid(input_number, expected):
    """Test square root calculation with valid inputs."""
    result = square_root(input_number)
    assert result == expected


@pytest.mark.parametrize("input_number", [-1, -4, -9])
def test_square_root_negative(input_number):
    """Test that square root fails for negative numbers."""
    with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
        square_root(input_number)


# ============================================================================
# Example 5: Testing Edge Cases and Error Conditions
# ============================================================================

def safe_divide(a: float, b: float) -> float:
    """Safely divide a by b, handling edge cases."""
    if b == 0:
        raise ValueError("Division by zero")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    return a / b


def process_string(text: str) -> str:
    """Process a string, handling various edge cases."""
    if text is None:
        raise ValueError("Input cannot be None")
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    if text.strip() == "":
        return "EMPTY"
    return text.strip().upper()


class TestEdgeCases:
    """Test cases for edge cases and error conditions."""
    
    def test_safe_divide_normal(self):
        """Test normal division."""
        result = safe_divide(10, 2)
        assert result == 5.0
    
    def test_safe_divide_by_zero(self):
        """Test division by zero."""
        with pytest.raises(ValueError, match="Division by zero"):
            safe_divide(10, 0)
    
    def test_safe_divide_invalid_types(self):
        """Test division with invalid types."""
        with pytest.raises(TypeError, match="Both arguments must be numbers"):
            safe_divide("10", 2)
    
    def test_process_string_normal(self):
        """Test normal string processing."""
        result = process_string("  hello world  ")
        assert result == "HELLO WORLD"
    
    def test_process_string_empty(self):
        """Test processing empty string."""
        result = process_string("   ")
        assert result == "EMPTY"
    
    def test_process_string_none(self):
        """Test processing None input."""
        with pytest.raises(ValueError, match="Input cannot be None"):
            process_string(None)
    
    def test_process_string_invalid_type(self):
        """Test processing invalid type."""
        with pytest.raises(TypeError, match="Input must be a string"):
            process_string(123)


# ============================================================================
# Example 6: Testing with Mocks (Basic Example)
# ============================================================================

from unittest.mock import patch, MagicMock


def get_user_info(user_id: int) -> Dict[str, Any]:
    """Get user information from a database."""
    # This would normally connect to a database
    # For testing, we'll mock this behavior
    if user_id <= 0:
        raise ValueError("Invalid user ID")
    
    # Simulate database call
    return {"id": user_id, "name": f"User {user_id}", "email": f"user{user_id}@example.com"}


def send_email(to_email: str, subject: str, message: str) -> bool:
    """Send an email (would normally use an email service)."""
    # This would normally send an actual email
    # For testing, we'll mock this behavior
    if not to_email or "@" not in to_email:
        raise ValueError("Invalid email address")
    
    # Simulate email sending
    return True


class TestWithMocks:
    """Test cases demonstrating basic mocking."""
    
    @patch('tests.test_examples.send_email')
    def test_send_email_success(self, mock_send_email):
        """Test successful email sending with mock."""
        # Configure the mock
        mock_send_email.return_value = True
        
        # Test the function
        result = send_email("test@example.com", "Subject", "Message")
        
        # Verify the mock was called correctly
        mock_send_email.assert_called_once_with("test@example.com", "Subject", "Message")
        assert result is True
    
    def test_send_email_invalid_address(self):
        """Test email sending with invalid address."""
        with pytest.raises(ValueError, match="Invalid email address"):
            send_email("", "Subject", "Message")
    
    def test_get_user_info_valid(self):
        """Test getting user info with valid ID."""
        result = get_user_info(1)
        expected = {"id": 1, "name": "User 1", "email": "user1@example.com"}
        assert result == expected
    
    def test_get_user_info_invalid_id(self):
        """Test getting user info with invalid ID."""
        with pytest.raises(ValueError, match="Invalid user ID"):
            get_user_info(0)


# ============================================================================
# Example 7: Testing File Operations (with temporary files)
# ============================================================================

import tempfile
import os


def save_data_to_file(data: str, filename: str) -> bool:
    """Save data to a file."""
    try:
        with open(filename, 'w') as f:
            f.write(data)
        return True
    except Exception:
        return False


def read_data_from_file(filename: str) -> str:
    """Read data from a file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found")
    
    with open(filename, 'r') as f:
        return f.read()


class TestFileOperations:
    """Test cases for file operations."""
    
    def test_save_and_read_file(self):
        """Test saving data to file and reading it back."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            filename = tmp_file.name
        
        try:
            # Test saving data
            test_data = "Hello, World!"
            success = save_data_to_file(test_data, filename)
            assert success is True
            
            # Verify file exists
            assert os.path.exists(filename)
            
            # Test reading data back
            read_data = read_data_from_file(filename)
            assert read_data == test_data
        
        finally:
            # Clean up
            if os.path.exists(filename):
                os.unlink(filename)
    
    def test_read_nonexistent_file(self):
        """Test reading a file that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            read_data_from_file("nonexistent_file.txt")


# ============================================================================
# Example 8: Testing Performance and Timing
# ============================================================================

import time


def slow_function() -> str:
    """A function that takes some time to execute."""
    time.sleep(0.1)  # Simulate some processing time
    return "Done"


class TestPerformance:
    """Test cases for performance-related testing."""
    
    def test_slow_function_completes(self):
        """Test that slow function completes successfully."""
        result = slow_function()
        assert result == "Done"
    
    def test_slow_function_timing(self):
        """Test that slow function completes within reasonable time."""
        start_time = time.time()
        result = slow_function()
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        assert result == "Done"
        assert execution_time < 0.2  # Should complete in less than 200ms


# ============================================================================
# Example 9: Testing with Different Data Types
# ============================================================================

def process_mixed_data(data: Any) -> str:
    """Process different types of data and return a string representation."""
    if isinstance(data, str):
        return f"String: {data}"
    elif isinstance(data, int):
        return f"Integer: {data}"
    elif isinstance(data, list):
        return f"List with {len(data)} items"
    elif isinstance(data, dict):
        return f"Dictionary with {len(data)} keys"
    else:
        return f"Unknown type: {type(data).__name__}"


class TestDataTypes:
    """Test cases for different data types."""
    
    def test_process_string(self):
        """Test processing string data."""
        result = process_mixed_data("hello")
        assert result == "String: hello"
    
    def test_process_integer(self):
        """Test processing integer data."""
        result = process_mixed_data(42)
        assert result == "Integer: 42"
    
    def test_process_list(self):
        """Test processing list data."""
        result = process_mixed_data([1, 2, 3])
        assert result == "List with 3 items"
    
    def test_process_dict(self):
        """Test processing dictionary data."""
        result = process_mixed_data({"a": 1, "b": 2})
        assert result == "Dictionary with 2 keys"
    
    def test_process_unknown_type(self):
        """Test processing unknown data type."""
        result = process_mixed_data(3.14)
        assert result == "Unknown type: float"


# ============================================================================
# Example 10: Testing with Setup and Teardown
# ============================================================================

class TestWithSetup:
    """Test cases demonstrating setup and teardown."""
    
    def setup_method(self):
        """Set up test data before each test method."""
        self.test_data = [1, 2, 3, 4, 5]
        self.test_string = "hello world"
    
    def teardown_method(self):
        """Clean up after each test method."""
        self.test_data = None
        self.test_string = None
    
    def test_with_setup_data(self):
        """Test using data set up in setup_method."""
        result = process_list(self.test_data)
        expected = [2, 4, 6, 8, 10]
        assert result == expected
    
    def test_with_setup_string(self):
        """Test using string data set up in setup_method."""
        result = process_string(self.test_string)
        assert result == "HELLO WORLD"


# ============================================================================
# Running the Examples
# ============================================================================

if __name__ == "__main__":
    # This section demonstrates how to run tests programmatically
    print("Running example tests...")
    
    # Test simple functions
    assert add_numbers(2, 3) == 5
    assert multiply_numbers(4, 5) == 20
    
    # Test data processing
    assert process_list([1, 2, 3]) == [2, 4, 6]
    assert filter_even_numbers([1, 2, 3, 4]) == [2, 4]
    
    print("All basic tests passed!") 