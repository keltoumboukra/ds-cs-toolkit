# Testing Setup Guide

This project has a testing framework set up. Here's how to run the tests.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 3. Run Tests
```bash
python -m pytest tests/ -v
```

### 4. Run Tests with Coverage
```bash
python -m pytest tests/ --cov=data_generation --cov-report=term-missing
```

## Important: Use the Correct Command

**Always specify the `tests/` directory** to avoid conflicts:

```bash
# CORRECT - Run only your project's tests
python -m pytest tests/ -v

# AVOID - This tries to collect tests from all installed packages
python -m pytest
```

## Test Results

- **29 tests** for the data generation module
- **100% coverage** for `data_generation.py`
- All tests should pass in under 1 second

## Other Useful Commands

```bash
# Run specific test file
python -m pytest tests/test_data_generation.py -v

# Run specific test function
python -m pytest tests/test_data_generation.py::TestGetProductData::test_returns_expected_structure -v

# Generate HTML coverage report
python -m pytest tests/ --cov=data_generation --cov-report=html
```

## Troubleshooting

If you get import errors or missing dependencies:
```bash
pip install -r requirements.txt
```

If tests are slow or have conflicts, make sure you're using `tests/` in the command.

## Project Structure

```
ds-cs-toolkit/
├── tests/
│   └── test_data_generation.py     # Your tests
├── data_generation.py              # Code being tested
├── pytest.ini                      # Pytest config
├── .coveragerc                     # Coverage config
└── requirements.txt                # Dependencies
```
