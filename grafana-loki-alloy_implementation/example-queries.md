# Example LogQL Queries for Weather API Logs

Use these queries in Grafana Explore (http://localhost:3000) to analyze your weather API logs.

## Basic Queries

### View all weather logs
```logql
{source="weather-api"}
```

### View logs from weather app container
```logql
{container="grafana-loki-alloy_implementation-weather-app-1"}
```

### View all application logs
```logql
{app="weather-service"}
```

## API Request Queries

### Find API requests
```logql
{source="weather-api"} |= "Fetching weather data"
```

### Find successful API responses
```logql
{source="weather-api"} |= "Weather data received"
```

### Find API errors
```logql
{source="weather-api"} |= "API error"
```

## City-Specific Queries

### Find logs for specific cities
```logql
{source="weather-api"} |= "London"
```
```logql
{source="weather-api"} |= "Tokyo"
```
```logql
{source="weather-api"} |= "New York"
```

### Find temperature data for cities
```logql
{source="weather-api"} |= "°C"
```

### Find humidity data
```logql
{source="weather-api"} |= "% humidity"
```

## Temperature Alert Queries

### Find high temperature alerts
```logql
{source="weather-api"} |= "High temperature alert"
```

### Find low temperature alerts
```logql
{source="weather-api"} |= "Low temperature alert"
```

### Find all temperature alerts
```logql
{source="weather-api"} |= "temperature alert"
```

## Humidity Alert Queries

### Find high humidity alerts
```logql
{source="weather-api"} |= "High humidity alert"
```

### Find humidity data
```logql
{source="weather-api"} |= "humidity"
```

## Error Queries

### Find timeout errors
```logql
{source="weather-api"} |= "Timeout error"
```

### Find connection errors
```logql
{source="weather-api"} |= "Connection error"
```

### Find all error logs
```logql
{source="weather-api"} |= "error"
```

## Weather Description Queries

### Find weather descriptions
```logql
{source="weather-api"} |= "cloudy"
```
```logql
{source="weather-api"} |= "rain"
```
```logql
{source="weather-api"} |= "sunny"
```

## Advanced Queries

### Combine multiple conditions
```logql
{source="weather-api"} |= "error" |= "London"
```

### Exclude certain terms
```logql
{source="weather-api"} != "info" != "debug"
```

### Time-based filtering (last hour)
```logql
{source="weather-api"} |= "error" [1h]
```

### Count API requests by city
```logql
sum by (city) (count_over_time({source="weather-api"} |= "Fetching weather data" [5m]))
```

### Count errors over time
```logql
sum(count_over_time({source="weather-api"} |= "error" [5m]))
```

### Count temperature alerts
```logql
sum(count_over_time({source="weather-api"} |= "temperature alert" [5m]))
```

## Performance Queries

### Find slow API responses
```logql
{source="weather-api"} |= "timeout"
```

### Find connection issues
```logql
{source="weather-api"} |= "connection"
```

## Real-time Monitoring

### Monitor API requests in real-time
```logql
{source="weather-api"} |= "Fetching weather data" [5m]
```

### Monitor errors in real-time
```logql
{source="weather-api"} |= "error" [5m]
```

### Monitor temperature alerts
```logql
{source="weather-api"} |= "temperature alert" [5m]
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