# Unit Testing Guide

This guide explains how to create and run unit tests in this project, following industry best practices.

## Table of Contents

1. [What is Unit Testing?](#what-is-unit-testing)
2. [Why Unit Testing Matters](#why-unit-testing-matters)
3. [Testing Framework Setup](#testing-framework-setup)
4. [Writing Your First Test](#writing-your-first-test)
5. [Test Structure and Best Practices](#test-structure-and-best-practices)
6. [Advanced Testing Concepts](#advanced-testing-concepts)
7. [Running Tests](#running-tests)
8. [Test Coverage](#test-coverage)
9. [Common Testing Patterns](#common-testing-patterns)
10. [Troubleshooting](#troubleshooting)

## What is Unit Testing?

Unit testing is a software testing method where individual units (functions, methods, or classes) of source code are tested in isolation to determine if they are working correctly. A unit is the smallest testable part of an application.

### Key Characteristics of Unit Tests:

- **Fast**: Tests should run quickly (milliseconds, not seconds)
- **Isolated**: Each test should be independent of others
- **Repeatable**: Tests should produce the same results every time
- **Self-validating**: Tests should automatically pass or fail
- **Timely**: Tests should be written before or alongside the code they test

## Why Unit Testing Matters

### Benefits:

1. **Early Bug Detection**: Catch bugs before they reach production
2. **Documentation**: Tests serve as living documentation of how code should work
3. **Refactoring Confidence**: Make changes safely knowing tests will catch regressions
4. **Design Improvement**: Writing tests often reveals design flaws
5. **Regression Prevention**: Ensure new changes don't break existing functionality

### Industry Standards:

- **Test Coverage**: Aim for 80%+ code coverage
- **Test Speed**: Unit tests should run in under 1 second total
- **Test Isolation**: No test should depend on another test's state
- **Clear Naming**: Test names should clearly describe what they're testing

## Testing Framework Setup

We use **pytest** as our testing framework, which is the most popular Python testing library.

### Dependencies:

```bash
pytest>=7.4.0          # Main testing framework
pytest-cov>=4.1.0      # Coverage reporting
pytest-mock>=3.11.0    # Mocking capabilities
```

### Configuration Files:

- `pytest.ini`: Main pytest configuration
- `.coveragerc`: Coverage reporting configuration
- `tests/`: Directory containing all test files

## Writing Your First Test

### Basic Test Structure

```python
def test_function_name():
    """Test description of what this test does."""
    # Arrange - Set up test data and conditions
    input_data = "test"
    
    # Act - Call the function being tested
    result = function_to_test(input_data)
    
    # Assert - Verify the result is correct
    assert result == "expected_output"
```

### Example: Testing a Simple Function

```python
# Function to test
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

# Test for the function
def test_add_numbers():
    """Test that add_numbers correctly adds two positive integers."""
    # Arrange
    a = 5
    b = 3
    
    # Act
    result = add_numbers(a, b)
    
    # Assert
    assert result == 8
```

## Test Structure and Best Practices

### 1. Test Class Organization

Group related tests in classes:

```python
class TestDataProcessor:
    """Test cases for the DataProcessor class."""
    
    def test_process_valid_data(self):
        """Test processing of valid data."""
        # Test implementation
    
    def test_process_empty_data(self):
        """Test processing of empty data."""
        # Test implementation
    
    def test_process_invalid_data(self):
        """Test processing of invalid data."""
        # Test implementation
```

### 2. Descriptive Test Names

Use clear, descriptive test names that explain what is being tested:

```python
# Good test names
def test_user_creation_with_valid_email():
def test_user_creation_fails_with_invalid_email():
def test_user_creation_fails_with_empty_name():

# Bad test names
def test_user():
def test_creation():
def test_1():
```

### 3. Arrange-Act-Assert Pattern

Structure your tests with clear sections:

```python
def test_calculate_total_with_discount():
    """Test total calculation with discount applied."""
    # Arrange - Set up test data
    items = [{"price": 100, "quantity": 2}]
    discount_rate = 0.1
    
    # Act - Execute the function
    total = calculate_total(items, discount_rate)
    
    # Assert - Verify the result
    expected_total = 180  # 100 * 2 * 0.9
    assert total == expected_total
```

### 4. Test Documentation

Always include docstrings explaining what the test does:

```python
def test_validate_email_format():
    """Test that email validation correctly identifies valid and invalid formats.
    
    This test covers:
    - Valid email formats (user@domain.com)
    - Invalid formats (missing @, invalid domain)
    - Edge cases (empty string, None)
    """
```

## Advanced Testing Concepts

### 1. Fixtures

Fixtures provide reusable test data and setup:

```python
import pytest

@pytest.fixture
def sample_user_data():
    """Provide sample user data for testing."""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }

def test_user_creation(sample_user_data):
    """Test user creation with fixture data."""
    user = create_user(sample_user_data)
    assert user.name == sample_user_data["name"]
```

### 2. Parameterized Tests

Test multiple scenarios with a single test function:

```python
import pytest

@pytest.mark.parametrize("input_value,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (0, 0),
])
def test_square_function(input_value, expected):
    """Test square function with various inputs."""
    result = square(input_value)
    assert result == expected
```

### 3. Mocking

Mock external dependencies to isolate the unit being tested:

```python
from unittest.mock import patch, MagicMock

def test_send_email_with_mock():
    """Test email sending without actually sending emails."""
    with patch('email_service.send_email') as mock_send:
        # Configure the mock
        mock_send.return_value = True
        
        # Test the function
        result = notify_user("user@example.com", "Hello")
        
        # Verify the mock was called correctly
        mock_send.assert_called_once_with("user@example.com", "Hello")
        assert result is True
```

### 4. Testing Exceptions

Test that functions raise appropriate exceptions:

```python
import pytest

def test_divide_by_zero():
    """Test that division by zero raises ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_invalid_input_type():
    """Test that invalid input types raise TypeError."""
    with pytest.raises(TypeError):
        process_data("not_a_number")
```

## Running Tests

### Basic Commands

```bash
# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_data_generation.py

# Run specific test function
python -m pytest tests/test_data_generation.py::test_add_numbers

# Run tests matching a pattern
python -m pytest -k "test_add"
```

### Test Markers

Use markers to categorize and selectively run tests:

```python
import pytest

@pytest.mark.slow
def test_expensive_operation():
    """This test takes a long time to run."""
    pass

@pytest.mark.integration
def test_database_connection():
    """This test requires a database connection."""
    pass
```

Run tests by marker:
```bash
# Run only fast tests
python -m pytest -m "not slow"

# Run only integration tests
python -m pytest -m integration
```

## Test Coverage

### What is Coverage?

Test coverage measures how much of your code is executed during testing. It helps identify untested code paths.

### Running Coverage

```bash
# Run tests with coverage
python -m pytest --cov=your_module

# Generate detailed coverage report
python -m pytest --cov=your_module --cov-report=html

# Generate coverage report in terminal
python -m pytest --cov=your_module --cov-report=term-missing
```

### Coverage Goals

- **80% minimum**: Good starting point
- **90%+**: Excellent coverage
- **100%**: Perfect coverage (but not always necessary)

### Interpreting Coverage

- **Statements**: Lines of code executed
- **Branches**: Different code paths taken
- **Functions**: Functions called during testing
- **Lines**: Individual lines of code executed

## Common Testing Patterns

### 1. Testing Data Processing Functions

```python
def test_process_data_with_various_inputs():
    """Test data processing with different input types."""
    # Test with valid data
    assert process_data([1, 2, 3]) == [2, 4, 6]
    
    # Test with empty list
    assert process_data([]) == []
    
    # Test with single item
    assert process_data([5]) == [10]
    
    # Test with negative numbers
    assert process_data([-1, -2]) == [-2, -4]
```

### 2. Testing File Operations

```python
import tempfile
import os

def test_save_to_file():
    """Test saving data to a file."""
    # Use temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        filename = tmp_file.name
    
    try:
        # Test the function
        save_data_to_file("test content", filename)
        
        # Verify file was created and contains correct content
        assert os.path.exists(filename)
        with open(filename, 'r') as f:
            content = f.read()
            assert content == "test content"
    
    finally:
        # Clean up
        if os.path.exists(filename):
            os.unlink(filename)
```

### 3. Testing API Functions

```python
from unittest.mock import patch, Mock

def test_api_call_success():
    """Test successful API call."""
    with patch('requests.get') as mock_get:
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "success"}
        mock_get.return_value = mock_response
        
        # Test the function
        result = call_api("https://api.example.com/data")
        
        # Verify results
        assert result == {"data": "success"}
        mock_get.assert_called_once_with("https://api.example.com/data")

def test_api_call_failure():
    """Test API call failure."""
    with patch('requests.get') as mock_get:
        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Test that exception is raised
        with pytest.raises(APIError):
            call_api("https://api.example.com/data")
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure your test files can import the modules they're testing
2. **Test Isolation**: Ensure tests don't depend on each other
3. **Mock Configuration**: Verify mocks are set up correctly
4. **File Paths**: Use absolute paths or proper relative paths for file operations

### Debugging Tests

```bash
# Run tests with debug output
python -m pytest -v -s

# Run single test with debugger
python -m pytest tests/test_file.py::test_function -s --pdb

# Run tests with maximum verbosity
python -m pytest -vvv
```

### Best Practices Checklist

- [ ] Each test has a clear, descriptive name
- [ ] Tests are independent and can run in any order
- [ ] Tests use the Arrange-Act-Assert pattern
- [ ] Edge cases and error conditions are tested
- [ ] External dependencies are mocked
- [ ] Test coverage is above 80%
- [ ] Tests run quickly (under 1 second total)
- [ ] Tests are well-documented with docstrings

## Next Steps

1. **Practice**: Write tests for existing functions in your codebase
2. **Learn More**: Explore pytest documentation and advanced features
3. **Automate**: Set up continuous integration to run tests automatically
4. **Refactor**: Use test feedback to improve code design
5. **Collaborate**: Share testing knowledge with your team

Remember: Good tests are an investment in code quality and maintainability. The time spent writing tests is saved many times over in debugging and maintenance. 