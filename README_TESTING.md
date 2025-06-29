# Testing Setup Guide

This project has been set up with a comprehensive testing framework following industry best practices. This guide will help you understand how to use the testing infrastructure.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run All Tests

```bash
python -m pytest
```

### 3. Run Tests with Coverage

```bash
python -m pytest --cov=. --cov-report=term-missing
```

## Project Structure

```
ds-cs-toolkit/
├── tests/                          # Test directory
│   ├── __init__.py                 # Makes tests a Python package
│   └── test_data_generation.py     # Tests for data generation module
├── docs/
│   └── testing_guide.md            # Comprehensive testing guide
├── pytest.ini                      # Pytest configuration
├── .coveragerc                     # Coverage configuration
├── requirements.txt                # Project dependencies
└── README_TESTING.md               # This file
```

## What's Been Set Up

### 1. Testing Framework
- **pytest**: Main testing framework
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking capabilities

### 2. Configuration Files
- **pytest.ini**: Configures pytest behavior, coverage settings, and test discovery
- **.coveragerc**: Defines what should be included/excluded from coverage reports

### 3. Test Files
- **test_data_generation.py**: Comprehensive tests for the data generation module (100% coverage)

### 4. Documentation
- **docs/testing_guide.md**: Complete guide to unit testing concepts and best practices

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
python -m pytest tests/test_data_generation.py::TestGetProductData::test_returns_expected_structure

# Run tests matching a pattern
python -m pytest -k "test_add"
```

### Coverage Commands

```bash
# Run tests with coverage
python -m pytest --cov=.

# Generate HTML coverage report
python -m pytest --cov=. --cov-report=html

# Generate coverage report in terminal
python -m pytest --cov=. --cov-report=term-missing

# Run coverage for specific module
python -m pytest --cov=data_generation --cov-report=term-missing
```

### Test Markers

```bash
# Run only fast tests (exclude slow ones)
python -m pytest -m "not slow"

# Run only unit tests
python -m pytest -m unit

# Run only integration tests
python -m pytest -m integration
```

## Current Test Coverage

### data_generation.py: 100% Coverage ✅

The data generation module has comprehensive test coverage including:

- **get_product_data()**: Product names and categories
- **generate_order_data()**: Order data generation with various scenarios
- **create_dataframe()**: DataFrame creation
- **save_to_csv()**: File operations
- **generate()**: Main generation function

### Test Categories

1. **Unit Tests**: Test individual functions in isolation
2. **Edge Case Tests**: Test boundary conditions and error scenarios
3. **Integration Tests**: Test how functions work together
4. **Parameterized Tests**: Test multiple scenarios efficiently

## Learning Path

### 1. Study the Testing Guide
Read `docs/testing_guide.md` for comprehensive explanations of:
- Unit testing concepts
- Best practices
- Advanced techniques
- Common patterns

### 2. Practice with Your Code
Write tests for your own functions following the patterns shown in the existing tests.

### 3. Understand Coverage
Use coverage reports to identify untested code:

```bash
python -m pytest --cov=. --cov-report=html
```

Then open `htmlcov/index.html` in your browser to see detailed coverage.

## Best Practices Demonstrated

### 1. Test Organization
- Tests are organized in classes by functionality
- Clear, descriptive test names
- Comprehensive docstrings

### 2. Test Structure
- **Arrange-Act-Assert** pattern
- Independent tests (no dependencies between tests)
- Proper setup and teardown

### 3. Coverage
- 100% coverage for critical modules
- Edge case testing
- Error condition testing

### 4. File Operations
- File operations use temporary files for testing
- Proper cleanup after tests

## Adding New Tests

### 1. Create Test File
Create a new file in the `tests/` directory:

```python
# tests/test_your_module.py
import pytest
from your_module import your_function

def test_your_function():
    """Test description."""
    # Arrange
    input_data = "test"
    
    # Act
    result = your_function(input_data)
    
    # Assert
    assert result == "expected"
```

### 2. Follow Naming Conventions
- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

### 3. Use Appropriate Markers
```python
@pytest.mark.unit
def test_fast_function():
    pass

@pytest.mark.integration
def test_slow_function():
    pass
```

## Continuous Integration

The testing setup is ready for CI/CD integration. You can add these commands to your CI pipeline:

```yaml
# Example GitHub Actions step
- name: Run tests
  run: |
    pip install -r requirements.txt
    python -m pytest --cov=. --cov-report=xml
    python -m pytest --cov=. --cov-fail-under=80
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure your test files can import the modules they're testing
2. **Test Isolation**: Ensure tests don't depend on each other
3. **File Paths**: Use absolute paths or proper relative paths for file operations

### Debugging

```bash
# Run tests with debug output
python -m pytest -v -s

# Run single test with debugger
python -m pytest tests/test_file.py::test_function -s --pdb

# Run tests with maximum verbosity
python -m pytest -vvv
```

## Next Steps

1. **Read the Guide**: Go through `docs/testing_guide.md`
2. **Write Your Own Tests**: Start testing your own functions
3. **Improve Coverage**: Aim for 80%+ coverage on new code
4. **Automate**: Set up CI/CD to run tests automatically

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Python Testing Best Practices](https://realpython.com/python-testing/)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)

## Contributing

When adding new features or fixing bugs:

1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain or improve coverage
4. Follow the established patterns

Remember: Good tests are an investment in code quality and maintainability! 