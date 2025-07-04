# Weather API Log Collection with Grafana Loki and Alloy

A complete setup for collecting and visualizing logs from a real weather API service using Grafana Loki and Grafana Alloy.

## System Architecture & Data Flow

```mermaid
graph TB
    %% External APIs
    subgraph "External Weather APIs"
        OWM[OpenWeatherMap API]
        WAPI[WeatherAPI.com]
    end
    
    %% User/Client
    subgraph "User/Client"
        USER[User/Client]
        BROWSER[Browser]
    end
    
    %% Main Application
    subgraph "Weather API Service"
        WA[Weather API<br/>Flask App<br/>Port: 5001]
        WA --> |Fetches weather data| OWM
        WA --> |Fallback API| WAPI
    end
    
    %% Log Collection Pipeline
    subgraph "Log Collection Pipeline"
        ALLOY[Grafana Alloy<br/>Log Collector<br/>Port: 12345]
        LOKI[Grafana Loki<br/>Log Storage<br/>Port: 3100]
    end
    
    %% Visualization
    subgraph "Visualization & Monitoring"
        GRAFANA[Grafana<br/>Dashboard & Queries<br/>Port: 3000]
    end
    
    %% Data Flow
    USER --> |HTTP Request| WA
    BROWSER --> |HTTP Request| WA
    WA --> |Generates logs| ALLOY
    ALLOY --> |Collects & forwards| LOKI
    LOKI --> |Stores logs| LOKI
    GRAFANA --> |Queries logs| LOKI
    USER --> |View dashboards| GRAFANA
    
    %% Styling
    classDef service fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef external fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef user fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef storage fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    
    class WA,ALLOY,GRAFANA service
    class OWM,WAPI external
    class USER,BROWSER user
    class LOKI storage
```

### Component Details

| Component | Purpose | Port | Key Features |
|-----------|---------|------|--------------|
| **Weather API** | Flask application that fetches real weather data | 5001 | • Fetches from multiple weather APIs<br/>• Generates structured logs<br/>• Handles errors gracefully |
| **Grafana Alloy** | Log collection agent | 12345 | • Collects logs from Docker containers<br/>• Processes and forwards to Loki<br/>• Provides collection metrics |
| **Grafana Loki** | Log storage and indexing | 3100 | • Stores logs efficiently<br/>• Provides LogQL query interface<br/>• Scales horizontally |
| **Grafana** | Visualization and querying | 3000 | • Interactive dashboards<br/>• LogQL query interface<br/>• Real-time log viewing |

### Data Flow Steps

1. **User Request**: User/client makes HTTP request to Weather API
2. **Weather Fetch**: API fetches weather data from external services
3. **Log Generation**: API generates structured logs for each operation
4. **Log Collection**: Alloy collects logs from the API container
5. **Log Storage**: Loki receives and stores the logs with indexing
6. **Log Querying**: Grafana queries Loki using LogQL
7. **Visualization**: Results displayed in Grafana dashboards

### Log Types & Processing

```mermaid
graph LR
    subgraph "Log Generation"
        INFO[Info Logs<br/>API requests, responses]
        WARN[Warning Logs<br/>Temperature/humidity alerts]
        ERROR[Error Logs<br/>API failures, timeouts]
    end
    
    subgraph "Log Processing"
        COLLECT[Alloy Collection]
        STORE[Loki Storage]
        QUERY[Grafana Query]
    end
    
    INFO --> COLLECT
    WARN --> COLLECT
    ERROR --> COLLECT
    COLLECT --> STORE
    STORE --> QUERY
```

## Quick Start

### 1. Start Everything
```bash
# Start all services
docker compose up -d

# Check all services are running
docker compose ps
```

### 2. Access Grafana
- URL: http://localhost:3000
- No login required (anonymous access enabled)

### 3. View Logs in Grafana
1. Click Explore (compass icon) in Grafana
2. Select Loki data source
3. Use this query: {container="grafana-loki-alloy_implementation-weather-app-1"}
4. Click Run Query

### 4. Generate Test Logs
```bash
# Trigger weather API calls to generate logs
curl http://localhost:5001/weather

# Or visit in browser: http://localhost:5001/weather
```

## Testing

This project includes testing:

### Run Tests
```bash
# Install testing dependencies
pip install -r requirements.txt

# Run all tests with coverage
pytest

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m api           # API tests only
```

### Test Coverage
- Unit Tests: Weather API functionality, log generation, error handling
- Integration Tests: Docker services, Loki API, log collection pipeline
- Coverage Target: ≥80% overall coverage

### Test Categories
- Weather API Tests: Flask endpoints, business logic, data validation
- Integration Tests: Service health, log pipeline, configuration validation
- Docker Tests: Service configuration, port mapping, health checks

Detailed Testing Guide: See the test files in the tests/ directory.

## Quick Commands Reference

### Start/Stop Services
```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Restart all services
docker compose restart

# View running services
docker compose ps
```

### Check Logs
```bash
# View Alloy logs (log collector)
docker compose logs alloy

# View weather app logs
docker compose logs weather-app

# View Loki logs (log storage)
docker compose logs loki

# View Grafana logs
docker compose logs grafana
```

### Test Log Collection
```bash
# Check if logs are being collected
curl "http://localhost:3100/loki/api/v1/labels"

# Query logs directly from Loki
curl "http://localhost:3100/loki/api/v1/query_range?query={container=\"grafana-loki-alloy_implementation-weather-app-1\"}"

# Count error logs
curl "http://localhost:3100/loki/api/v1/query_range?query={container=\"grafana-loki-alloy_implementation-weather-app-1\"} |= \"error\"" | jq '.data.result[0].values | length'
```

### Generate Test Data
```bash
# Trigger weather API calls
curl http://localhost:5001/weather

# Trigger multiple calls
for i in {1..5}; do curl http://localhost:5001/weather; sleep 2; done

# Check weather app status
curl http://localhost:5001/status
```

## Working Log Queries

Use these queries in Grafana Explore:

```logql
# All weather app logs
{container="grafana-loki-alloy_implementation-weather-app-1"}

# Weather API requests
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "Fetching weather data"

# Error logs
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "error"

# API errors specifically
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "API error"

# Info logs
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "INFO"

# Specific city logs
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "London"
```

Complete Query Examples: [example-queries.md](example-queries.md)

## Troubleshooting

### "No logs volume available" Error
Solution: Use the correct label in your query:
- Wrong: {source="weather-api"}
- Correct: {container="grafana-loki-alloy_implementation-weather-app-1"}

### Services Not Starting
```bash
# Check Docker is running
docker --version

# Check available ports
lsof -i :3000  # Grafana
lsof -i :3100  # Loki
lsof -i :5001  # Weather API
lsof -i :12345 # Alloy UI
```

### No Logs Appearing
```bash
# 1. Check if weather app is generating logs
docker compose logs weather-app

# 2. Check if Alloy is collecting logs
docker compose logs alloy

# 3. Check if Loki is receiving logs
docker compose logs loki

# 4. Generate test logs
curl http://localhost:5001/weather
```

### Restart Everything
```bash
# Complete restart
docker compose down
docker compose up -d

# Wait for services to start
sleep 30

# Generate test logs
curl http://localhost:5001/weather
```

## Architecture

```
Weather API (Flask) -> Alloy -> Loki -> Grafana
```

- Weather API: Python Flask app that fetches real weather data
- Alloy: Collects logs from Docker containers
- Loki: Stores and indexes the logs
- Grafana: Visualizes and queries the logs

## Services

| Service | Port | Purpose | Status Check |
|---------|------|---------|--------------|
| Weather API | 5001 | Generates weather logs | curl http://localhost:5001/status |
| Grafana | 3000 | Log visualization | curl http://localhost:3000 |
| Loki | 3100 | Log storage | curl http://localhost:3100/ready |
| Alloy | 12345 | Log collection | curl http://localhost:12345/ready |

## Log Types Generated

### Info Logs
- API requests: "Fetching weather data for [city]"
- Successful responses: "Weather data received for [city]: [temp]°C, [humidity]% humidity"

### Warning Logs
- High temperature alerts: "High temperature alert for [city]: [temp]°C"
- Low temperature alerts: "Low temperature alert for [city]: [temp]°C"
- High humidity alerts: "High humidity alert for [city]: [humidity]%"

### Error Logs
- API errors: "API error for [city]: HTTP [status]"
- Timeout errors: "Timeout error fetching weather for [city]"
- Connection errors: "Connection error fetching weather for [city]"

## Monitored Cities

The service monitors weather for these cities:
- London, New York, Tokyo, Paris, Sydney
- Berlin, Moscow, Beijing, Mumbai, Cairo
- Rio de Janeiro, Mexico City, Toronto, Seoul, Bangkok

## Manual Testing

Trigger weather API calls manually:
- Random city: http://localhost:5001/weather
- Specific city: http://localhost:5001/weather/London
- Service status: http://localhost:5001/status

## Prerequisites

- Docker
- Docker Compose
- Python 3.8+ (for testing)

## Files

- docker-compose.yml - Service definitions
- config.alloy - Alloy log collection configuration
- app.py - Weather API Flask application
- loki-config.yaml - Loki storage configuration
- requirements.txt - Python dependencies
- Dockerfile - Weather app container build
- tests/ - Comprehensive test suite
- example-queries.md - LogQL query examples

## Important Notes

1. Use the correct labels: The logs use container labels, not source labels
2. Wait for startup: Services may take 30-60 seconds to fully start
3. Generate logs: Visit http://localhost:5001/weather to generate test logs
4. Check status: Use the quick commands above to verify everything is working
5. Run tests: Use pytest to verify functionality and get coverage reports


