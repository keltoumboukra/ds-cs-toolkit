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
python -m pytest tests/ --cov=. --cov-report=term-missing
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

- **58 tests** for data generation and business logic modules
- **97% overall coverage** across all testable code
- All tests should pass in under 1 second

## Other Useful Commands

```bash
# Run specific test file
python -m pytest tests/test_data_generation.py -v

# Run specific test function
python -m pytest tests/test_data_generation.py::TestGetProductData::test_returns_expected_structure -v

# Generate HTML coverage report
python -m pytest tests/ --cov=. --cov-report=html
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
│   ├── test_data_generation.py     # Tests for data generation (29 tests)
│   └── test_taipy_logic.py         # Tests for business logic (29 tests)
├── data_generation.py              # Data generation module (100% coverage)
├── taipy_logic.py                  # Business logic module (96% coverage)
├── pytest.ini                      # Pytest config
├── .coveragerc                     # Coverage config
└── requirements.txt                # Dependencies
```

## Coverage Summary

- **`data_generation.py`**: 100% coverage (29 tests)
- **`taipy_logic.py`**: 96% coverage (29 tests)
- **Overall**: 97% coverage (58 tests total)

That's it! Your tests should run successfully with these instructions.
