# 🚀 Quick Start Guide

## Start the Weather Log Collection Stack

```bash
# Start all services
docker compose up -d

# Wait 15 seconds for services to start
sleep 15
```

## Access Your Logs

1. **Open Grafana:** http://localhost:3000
   - No login required (anonymous access enabled)

2. **View Weather Logs:**
   - Click **Explore** in Grafana
   - Select **Loki** data source
   - Use query: `{source="weather-api"}`

## Test the Weather API

- **Random city:** http://localhost:5001/weather
- **Specific city:** http://localhost:5001/weather/London
- **Service status:** http://localhost:5001/status

## Useful Log Queries

```logql
# All weather logs
{source="weather-api"}

# API requests
{source="weather-api"} |= "Fetching weather data"

# Errors
{source="weather-api"} |= "error"

# Temperature alerts
{source="weather-api"} |= "temperature alert"

# Specific city
{source="weather-api"} |= "London"
```

## Stop the Stack

```bash
docker compose down
```

## Troubleshooting

```bash
# Check service status
docker compose ps

# View logs
docker compose logs alloy
docker compose logs weather-app

# Restart services
docker compose restart
```

## What You'll See

The weather service automatically fetches weather data every 10-30 seconds and generates:
- **Info logs:** API requests and responses
- **Warning logs:** Temperature/humidity alerts
- **Error logs:** API errors, timeouts, connection issues

All logs are collected by Alloy, stored in Loki, and visualized in Grafana with labels:
- `source="weather-api"`
- `platform="docker"`
- `app="weather-service"` 