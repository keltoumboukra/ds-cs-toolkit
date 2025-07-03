# ds-cs-toolkit
A growing collection of mini-projects exploring data science and computer science tools. Each folder is a hands-on experiment, comparison, or deep dive into a specific topic, framework, or library.

## Projects

### taipy_implementation/
A comprehensive sales performance dashboard built with Taipy, featuring interactive visualizations, data filtering, and real-time metrics calculation.

- **Interactive Dashboard**: Real-time sales performance visualization
- **Data Filtering**: Filter by date range and product categories  
- **Multiple Visualizations**: Revenue over time, by category, and top products
- **Comprehensive Testing**: 58 tests with 97% code coverage

[View Taipy Implementation →](taipy_implementation/README.md)

### dspy_implementation/
DSPy-based implementation for natural language processing and AI applications.

[View DSPy Implementation →](dspy_implementation/)

### grafana-loki-alloy_implementation/
A complete log collection and visualization stack using Grafana, Loki, and Alloy with a real weather API service.

- **Real-time Log Collection**: Weather API logs collected via Alloy
- **Log Storage & Querying**: Loki for efficient log storage and retrieval
- **Visualization Dashboard**: Grafana for log analysis and monitoring
- **Working Example**: Live weather API generating logs with API errors, info messages, and alerts

[View Grafana-Loki-Alloy Implementation →](grafana-loki-alloy_implementation/README.md)

## Getting Started

Each project in this toolkit is self-contained with its own requirements and documentation. Navigate to the specific project folder to get started:

```bash
# For Taipy dashboard
cd taipy_implementation
pip install -r requirements.txt
python taipy-app.py

# For DSPy implementation  
cd dspy_implementation
# Follow project-specific instructions

# For Grafana-Loki-Alloy stack
cd grafana-loki-alloy_implementation
docker compose up -d
# Access Grafana at http://localhost:3000
```

## Contributing

When adding new projects:
1. Create a new folder for your implementation
2. Include a comprehensive README.md
3. Add appropriate tests and documentation
4. Update this main README with project details
