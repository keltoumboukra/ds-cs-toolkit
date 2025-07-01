#!/usr/bin/env python3
"""
Weather API service that generates real logs from API calls
"""

import logging
import time
import threading
import requests
import json
from datetime import datetime
from flask import Flask, jsonify, request
import os
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Weather API configuration
WEATHER_API_KEY = "demo"  # Using demo key for openweathermap
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Major cities for weather data
CITIES = [
    "London", "New York", "Tokyo", "Paris", "Sydney", 
    "Berlin", "Moscow", "Beijing", "Mumbai", "Cairo",
    "Rio de Janeiro", "Mexico City", "Toronto", "Seoul", "Bangkok"
]

def fetch_weather_data(city):
    """Fetch weather data for a city and log the process"""
    try:
        logger.info(f"Fetching weather data for {city}")
        
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            
            logger.info(f"Weather data received for {city}: {temp}°C, {humidity}% humidity, {description}")
            
            return {
                'city': city,
                'temperature': temp,
                'humidity': humidity,
                'description': description,
                'status': 'success'
            }
        else:
            logger.error(f"API error for {city}: HTTP {response.status_code} - {response.text}")
            return {
                'city': city,
                'status': 'error',
                'error': f"HTTP {response.status_code}"
            }
            
    except requests.exceptions.Timeout:
        logger.error(f"Timeout error fetching weather for {city}")
        return {
            'city': city,
            'status': 'error',
            'error': 'timeout'
        }
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error fetching weather for {city}")
        return {
            'city': city,
            'status': 'error',
            'error': 'connection_error'
        }
    except Exception as e:
        logger.error(f"Unexpected error fetching weather for {city}: {str(e)}")
        return {
            'city': city,
            'status': 'error',
            'error': str(e)
        }

def weather_monitor():
    """Background thread that continuously fetches weather data"""
    while True:
        try:
            # Pick a random city
            city = random.choice(CITIES)
            
            # Fetch weather data
            result = fetch_weather_data(city)
            
            # Log some additional metrics
            if result['status'] == 'success':
                temp = result['temperature']
                if temp > 30:
                    logger.warning(f"High temperature alert for {city}: {temp}°C")
                elif temp < 0:
                    logger.warning(f"Low temperature alert for {city}: {temp}°C")
                
                humidity = result['humidity']
                if humidity > 80:
                    logger.warning(f"High humidity alert for {city}: {humidity}%")
            
            # Random delay between 10-30 seconds
            time.sleep(random.uniform(10, 30))
            
        except Exception as e:
            logger.error(f"Error in weather monitor: {e}")
            time.sleep(30)

@app.route('/')
def home():
    """Home page with basic info"""
    return jsonify({
        "message": "Weather API Service is running",
        "description": "Fetches real weather data and logs API calls",
        "endpoints": {
            "home": "/",
            "status": "/status",
            "weather": "/weather",
            "weather_city": "/weather/<city>",
            "logs": "/logs"
        }
    })

@app.route('/status')
def status():
    """Application status"""
    return jsonify({
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "api_key": "demo (openweathermap)",
        "cities_monitored": CITIES
    })

@app.route('/weather')
def get_random_weather():
    """Get weather for a random city"""
    city = random.choice(CITIES)
    result = fetch_weather_data(city)
    return jsonify(result)

@app.route('/weather/<city>')
def get_weather_for_city(city):
    """Get weather for a specific city"""
    result = fetch_weather_data(city)
    return jsonify(result)

@app.route('/logs')
def get_logs():
    """Return log information"""
    return jsonify({
        "message": "Weather API logs are being collected by Grafana Loki",
        "view_logs": "Check Grafana at http://localhost:3000",
        "timestamp": datetime.now().isoformat(),
        "log_types": [
            "API requests and responses",
            "Temperature alerts (high/low)",
            "Humidity alerts",
            "Connection errors",
            "Timeout errors"
        ]
    })

if __name__ == '__main__':
    # Start the background weather monitor
    weather_thread = threading.Thread(target=weather_monitor, daemon=True)
    weather_thread.start()
    
    logger.info("Weather API Service starting...")
    logger.info("Access the service at http://localhost:5000")
    logger.info("Weather data will be fetched and logged continuously")
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=False) 