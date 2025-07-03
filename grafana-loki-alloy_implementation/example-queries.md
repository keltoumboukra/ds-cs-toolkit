# Example LogQL Queries for Weather API Logs

Use these queries in Grafana Explore (http://localhost:3000) to analyze your weather API logs.

## Basic Queries

### View all weather logs
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"}
```

### View logs from weather app container
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"}
```

### View all application logs
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"}
```

## API Request Queries

### Find API requests
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "Fetching weather data"
```

### Find successful API responses
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "Weather data received"
```

### Find API errors
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "API error"
```

## City-Specific Queries

### Find logs for specific cities
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "London"
```
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "Tokyo"
```
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "New York"
```

### Find temperature data for cities
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "°C"
```

### Find humidity data
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "% humidity"
```

## Temperature Alert Queries

### Find high temperature alerts
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "High temperature alert"
```

### Find low temperature alerts
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "Low temperature alert"
```

### Find all temperature alerts
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "temperature alert"
```

## Humidity Alert Queries

### Find high humidity alerts
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "High humidity alert"
```

### Find humidity data
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "humidity"
```

## Error Queries

### Find timeout errors
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "Timeout error"
```

### Find connection errors
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "Connection error"
```

### Find all error logs
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "error"
```

## Weather Description Queries

### Find weather descriptions
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "cloudy"
```
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "rain"
```
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "sunny"
```

## Advanced Queries

### Combine multiple conditions
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "error" |= "London"
```

### Exclude certain terms
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} != "info" != "debug"
```

### Time-based filtering (last hour)
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "error" [1h]
```

### Count API requests by city
```logql
sum by (city) (count_over_time({container="grafana-loki-alloy_implementation-weather-app-1"} |= "Fetching weather data" [5m]))
```

### Count errors over time
```logql
sum(count_over_time({container="grafana-loki-alloy_implementation-weather-app-1"} |= "error" [5m]))
```

### Count temperature alerts
```logql
sum(count_over_time({container="grafana-loki-alloy_implementation-weather-app-1"} |= "temperature alert" [5m]))
```

## Performance Queries

### Find slow API responses
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "timeout"
```

### Find connection issues
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "connection"
```

## Real-time Monitoring

### Monitor API requests in real-time
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "Fetching weather data" [5m]
```

### Monitor errors in real-time
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "error" [5m]
```

### Monitor temperature alerts
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "temperature alert" [5m]
```

## Additional Useful Queries

### View all available labels
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"}
```

### Filter by log level
```logql
{container="grafana-loki-alloy_implementation-weather-app-1", detected_level="error"}
```

### Filter by log level
```logql
{container="grafana-loki-alloy_implementation-weather-app-1", detected_level="info"}
```

### Find HTTP requests
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "GET /weather"
```

### Find werkzeug logs (Flask framework)
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"} |= "werkzeug"
```

## Tips

1. Use `|=` for case-sensitive text matching
2. Use `=~` for regex matching
3. Use `!=` to exclude terms
4. Add time ranges like `[5m]`, `[1h]`, `[24h]` to limit results
5. Use `count_over_time()` for aggregations
6. Use `sum by (label)` to group results by labels
7. The weather service fetches data every 10-30 seconds for random cities
8. You can manually trigger weather requests by visiting `http://localhost:5001/weather`
9. Temperature alerts are generated when temp > 30°C or < 0°C
10. Humidity alerts are generated when humidity > 80%
11. **Important:** Use `{container="grafana-loki-alloy_implementation-weather-app-1"}` 