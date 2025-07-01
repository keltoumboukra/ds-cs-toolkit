# Weather API Log Collection with Grafana Loki and Alloy

A complete setup for collecting and visualizing logs from a real weather API service using Grafana Loki and Grafana Alloy.

## 🚀 Quick Start

1. **Start the stack:**
   ```bash
   docker compose up -d
   ```

2. **Access Grafana:** http://localhost:3000
   - No login required (anonymous access enabled)

3. **View weather logs:**
   - Go to **Explore** in Grafana
   - Select **Loki** data source
   - Use query: `{source="weather-api"}`

4. **Test the weather API:**
   - Visit: http://localhost:5001/weather
   - This generates real weather API calls and logs

## 📊 What You'll See

The weather service generates real logs from OpenWeatherMap API calls:

- **Info logs:** API requests, successful weather data
- **Warning logs:** Temperature/humidity alerts
- **Error logs:** API errors, timeouts, connection issues

### Example Log Queries

```logql
# All weather logs
{source="weather-api"}

# Weather API requests
{source="weather-api"} |= "Fetching weather data"

# Temperature alerts
{source="weather-api"} |= "temperature alert"

# API errors
{source="weather-api"} |= "error"

# Specific city logs
{source="weather-api"} |= "London"
```

## 🏗️ Architecture

```
Weather API (Flask) → Alloy → Loki → Grafana
```

- **Weather API:** Python Flask app that fetches real weather data
- **Alloy:** Collects logs from Docker containers
- **Loki:** Stores and indexes the logs
- **Grafana:** Visualizes and queries the logs

## 🔧 Services

| Service | Port | Purpose |
|---------|------|---------|
| Weather API | 5001 | Generates weather logs |
| Grafana | 3000 | Log visualization |
| Loki | 3100 | Log storage |
| Alloy | 12345 | Log collection |

## 📝 Log Types Generated

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

## 🌍 Monitored Cities

The service monitors weather for these cities:
- London, New York, Tokyo, Paris, Sydney
- Berlin, Moscow, Beijing, Mumbai, Cairo
- Rio de Janeiro, Mexico City, Toronto, Seoul, Bangkok

## 🎯 Manual Testing

Trigger weather API calls manually:
- **Random city:** http://localhost:5001/weather
- **Specific city:** http://localhost:5001/weather/London
- **Service status:** http://localhost:5001/status

## 🛑 Stopping the Stack

```bash
docker compose down
```

## 🔍 Troubleshooting

**Check service status:**
```bash
docker compose ps
```

**View Alloy logs:**
```bash
docker compose logs alloy
```

**View weather app logs:**
```bash
docker compose logs weather-app
```

**Restart services:**
```bash
docker compose restart
```

## 📋 Prerequisites

- Docker
- Docker Compose

## 📄 Files

- `docker-compose.yml` - Service definitions
- `config.alloy` - Alloy log collection configuration
- `app.py` - Weather API Flask application
- `loki-config.yaml` - Loki storage configuration
- `requirements.txt` - Python dependencies
- `Dockerfile` - Weather app container build


