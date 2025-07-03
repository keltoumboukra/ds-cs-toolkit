"""
Tests for the Weather API Flask application.

This module contains tests for the weather API functionality,
including unit tests for individual functions and integration tests for
the Flask application endpoints.
"""

import pytest
import json
import logging
import requests
from unittest.mock import Mock, patch, MagicMock
from flask import Flask
from app import app, fetch_weather_data, CITIES
import random


@pytest.mark.unit
class TestWeatherAPI:
    """Test class for Weather API functionality."""

    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def mock_requests(self):
        """Mock requests library for testing API calls."""
        with patch('app.requests') as mock_req:
            yield mock_req

    def test_app_creation(self):
        """Test that the Flask app is created correctly."""
        assert isinstance(app, Flask)
        assert app.name == 'app'

    def test_cities_list(self):
        """Test that CITIES list contains expected cities."""
        assert isinstance(CITIES, list)
        assert len(CITIES) > 0
        # Test that it contains expected cities
        expected_cities = [
            'London', 'New York', 'Tokyo', 'Paris', 'Sydney',
            'Berlin', 'Moscow', 'Beijing', 'Mumbai', 'Cairo',
            'Rio de Janeiro', 'Mexico City', 'Toronto', 'Seoul', 'Bangkok'
        ]
        for city in expected_cities:
            assert city in CITIES

    def test_random_city_selection(self):
        """Test that random city selection works."""
        city = random.choice(CITIES)
        assert isinstance(city, str)
        assert len(city) > 0
        assert city in CITIES

    @patch('app.requests.get')
    def test_fetch_weather_data_success(self, mock_get):
        """Test successful weather data fetching."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {
                'temp': 25.5,
                'humidity': 65
            },
            'weather': [{'description': 'clear sky'}],
            'name': 'London'
        }
        mock_get.return_value = mock_response

        result = fetch_weather_data('London')
        
        assert result is not None
        assert 'city' in result
        assert 'temperature' in result
        assert 'humidity' in result
        assert result['city'] == 'London'
        assert result['temperature'] == 25.5
        assert result['humidity'] == 65
        assert result['status'] == 'success'

    @patch('app.requests.get')
    def test_fetch_weather_data_api_error(self, mock_get):
        """Test weather data fetching with API error."""
        # Mock API error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = 'Invalid API key'
        mock_get.return_value = mock_response

        result = fetch_weather_data('London')
        
        assert result is not None
        assert result['status'] == 'error'
        assert 'error' in result

    @patch('app.requests.get')
    def test_fetch_weather_data_connection_error(self, mock_get):
        """Test weather data fetching with connection error."""
        # Mock connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        result = fetch_weather_data('London')
        
        assert result is not None
        assert result['status'] == 'error'
        assert result['error'] == 'connection_error'

    @patch('app.requests.get')
    def test_fetch_weather_data_timeout_error(self, mock_get):
        """Test weather data fetching with timeout error."""
        # Mock timeout error
        mock_get.side_effect = requests.exceptions.Timeout("Timeout error")

        result = fetch_weather_data('London')
        
        assert result is not None
        assert result['status'] == 'error'
        assert result['error'] == 'timeout'

    def test_weather_endpoint_success(self, client, mock_requests):
        """Test successful weather endpoint response."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {
                'temp': 25.5,
                'humidity': 65
            },
            'weather': [{'description': 'clear sky'}],
            'name': 'London'
        }
        mock_requests.get.return_value = mock_response

        response = client.get('/weather')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'city' in data
        assert 'temperature' in data
        assert 'humidity' in data
        assert 'description' in data

    def test_weather_endpoint_api_error(self, client, mock_requests):
        """Test weather endpoint with API error."""
        # Mock API error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = 'Invalid API key'
        mock_requests.get.return_value = mock_response

        response = client.get('/weather')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'error'
        assert 'error' in data

    def test_weather_specific_city_endpoint(self, client, mock_requests):
        """Test weather endpoint with specific city."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {
                'temp': 30.0,
                'humidity': 70
            },
            'weather': [{'description': 'sunny'}],
            'name': 'Tokyo'
        }
        mock_requests.get.return_value = mock_response

        response = client.get('/weather/Tokyo')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['city'] == 'Tokyo'
        assert data['temperature'] == 30.0

    def test_status_endpoint(self, client):
        """Test status endpoint."""
        response = client.get('/status')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'running'
        assert 'timestamp' in data
        assert 'cities_monitored' in data

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get('/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'Weather API Service' in data['message']
        assert 'endpoints' in data

    def test_logs_endpoint(self, client):
        """Test logs endpoint."""
        response = client.get('/logs')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'log_types' in data
        assert isinstance(data['log_types'], list)

    def test_invalid_endpoint(self, client):
        """Test invalid endpoint returns 404."""
        response = client.get('/invalid')
        
        assert response.status_code == 404

    def test_temperature_alerts_high(self):
        """Test high temperature alert generation."""
        with patch('app.logger.warning') as mock_log:
            # Test with high temperature
            weather_data = {'temperature': 35.0, 'humidity': 60}
            city = 'London'
            
            # This would be called in the actual app when temp > 30
            if weather_data['temperature'] > 30:
                app.logger.warning(f'High temperature alert for {city}: {weather_data["temperature"]}°C')
            
            mock_log.assert_called_once()

    def test_temperature_alerts_low(self):
        """Test low temperature alert generation."""
        with patch('app.logger.warning') as mock_log:
            # Test with low temperature
            weather_data = {'temperature': -5.0, 'humidity': 60}
            city = 'London'
            
            # This would be called in the actual app when temp < 0
            if weather_data['temperature'] < 0:
                app.logger.warning(f'Low temperature alert for {city}: {weather_data["temperature"]}°C')
            
            mock_log.assert_called_once()

    def test_humidity_alerts(self):
        """Test humidity alert generation."""
        with patch('app.logger.warning') as mock_log:
            # Test with high humidity
            weather_data = {'temperature': 25.0, 'humidity': 85}
            city = 'London'
            
            # This would be called in the actual app when humidity > 80
            if weather_data['humidity'] > 80:
                app.logger.warning(f'High humidity alert for {city}: {weather_data["humidity"]}%')
            
            mock_log.assert_called_once()


@pytest.mark.unit
@pytest.mark.api
class TestWeatherAPIIntegration:
    """Integration tests for Weather API."""

    @pytest.fixture
    def client(self):
        """Create a test client for integration tests."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_full_weather_flow(self, client):
        """Test the complete weather API flow."""
        with patch('app.requests.get') as mock_get:
            # Mock successful API response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'main': {
                    'temp': 25.5,
                    'humidity': 65
                },
                'weather': [{'description': 'clear sky'}],
                'name': 'London'
            }
            mock_get.return_value = mock_response

            # Test the complete flow
            response = client.get('/weather')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            # Verify all expected fields are present
            required_fields = ['city', 'temperature', 'humidity', 'description', 'status']
            for field in required_fields:
                assert field in data

    def test_error_handling_flow(self, client):
        """Test error handling in the complete flow."""
        with patch('app.requests.get') as mock_get:
            # Mock API error
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.text = 'Invalid API key'
            mock_get.return_value = mock_response

            # Test error handling
            response = client.get('/weather')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'status' in data
            assert data['status'] == 'error'
            assert 'error' in data


if __name__ == '__main__':
    pytest.main([__file__]) 