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
# Run all tests (including Taipy implementation tests)
python -m pytest tests/ -v
python -m pytest taipy_implementation/tests/ -v

# Run specific project tests
python -m pytest taipy_implementation/tests/ -v
```

### 4. Run Tests with Coverage
```bash
python -m pytest tests/ --cov=. --cov-report=term-missing
python -m pytest taipy_implementation/tests/ --cov=taipy_implementation --cov-report=term-missing
```

## Important: Use the Correct Command

**Always specify the `tests/` directory** to avoid conflicts:

```bash
# CORRECT - Run only your project's tests
python -m pytest tests/ -v
python -m pytest taipy_implementation/tests/ -v

# AVOID - This tries to collect tests from all installed packages
python -m pytest
```

## Test Results

- **58 tests** for Taipy implementation (data generation and business logic modules)
- **97% overall coverage** across all testable code
- All tests should pass in under 1 second

## Other Useful Commands

```bash
# Run specific test file
python -m pytest taipy_implementation/tests/test_data_generation.py -v

# Run specific test function
python -m pytest taipy_implementation/tests/test_data_generation.py::TestGetProductData::test_returns_expected_structure -v

# Generate HTML coverage report
python -m pytest taipy_implementation/tests/ --cov=taipy_implementation --cov-report=html
```

## Troubleshooting

If you get import errors or missing dependencies:
```bash
pip install -r requirements.txt
```

If tests are slow or have conflicts, make sure you're using the correct test directory in the command.

## Project Structure

```
ds-cs-toolkit/
├── taipy_implementation/
│   ├── tests/
│   │   ├── test_data_generation.py     # Tests for data generation (29 tests)
│   │   └── test_taipy_logic.py         # Tests for business logic (29 tests)
│   ├── data_generation.py              # Data generation module (100% coverage)
│   ├── taipy_logic.py                  # Business logic module (96% coverage)
│   ├── taipy-app.py                    # Main Taipy application
│   ├── sales_data/                     # Data directory
│   ├── requirements.txt                # Taipy-specific dependencies
│   └── README.md                       # Taipy project documentation
├── tests/                              # Main repository tests (if any)
├── pytest.ini                          # Pytest config
├── .coveragerc                         # Coverage config
└── requirements.txt                    # Main repository dependencies
```

## Coverage Summary

- **`taipy_implementation/data_generation.py`**: 100% coverage (29 tests)
- **`taipy_implementation/taipy_logic.py`**: 96% coverage (29 tests)
- **Overall**: 97% coverage (58 tests total)

## Running Taipy Implementation Tests

To run tests specifically for the Taipy implementation:

```bash
cd taipy_implementation
python -m pytest tests/ -v
```

Or from the root directory:

```bash
python -m pytest taipy_implementation/tests/ -v
```

That's it! Your tests should run successfully with these instructions.
