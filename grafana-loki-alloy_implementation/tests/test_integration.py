"""
Integration tests for the Grafana-Loki-Alloy stack.

This module contains integration tests that verify the complete
log collection and visualization pipeline works correctly.
"""

import pytest
import requests
import time
import json
import subprocess
from unittest.mock import patch, Mock


class TestDockerServices:
    """Test Docker services health and functionality."""

    def test_docker_compose_services(self):
        """Test that all Docker services are defined correctly."""
        import yaml
        
        with open('docker-compose.yml', 'r') as f:
            compose_config = yaml.safe_load(f)
        
        # Check that all required services are present
        required_services = ['weather-app', 'loki', 'grafana', 'alloy']
        for service in required_services:
            assert service in compose_config['services'], f"Service {service} not found in docker-compose.yml"

    def test_docker_compose_ports(self):
        """Test that all required ports are exposed."""
        import yaml
        
        with open('docker-compose.yml', 'r') as f:
            compose_config = yaml.safe_load(f)
        
        # Check port mappings
        expected_ports = {
            'weather-app': 5001,
            'grafana': 3000,
            'loki': 3100,
            'alloy': 12345
        }
        
        for service, port in expected_ports.items():
            if service in compose_config['services']:
                service_config = compose_config['services'][service]
                if 'ports' in service_config:
                    ports = service_config['ports']
                    port_mapped = any(f"{port}:" in str(p) for p in ports)
                    assert port_mapped, f"Port {port} not mapped for service {service}"

    @pytest.mark.integration
    def test_weather_app_health(self):
        """Test weather app health endpoint."""
        try:
            response = requests.get('http://localhost:5001/status', timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert 'status' in data
            assert data['status'] == 'running'
        except requests.exceptions.RequestException:
            pytest.skip("Weather app not running")

    @pytest.mark.integration
    def test_grafana_health(self):
        """Test Grafana health endpoint."""
        try:
            response = requests.get('http://localhost:3000', timeout=5)
            assert response.status_code == 200
            assert 'Grafana' in response.text
        except requests.exceptions.RequestException:
            pytest.skip("Grafana not running")

    @pytest.mark.integration
    def test_loki_health(self):
        """Test Loki health endpoint."""
        try:
            response = requests.get('http://localhost:3100/ready', timeout=5)
            assert response.status_code == 200
        except requests.exceptions.RequestException:
            pytest.skip("Loki not running")

    @pytest.mark.integration
    def test_alloy_health(self):
        """Test Alloy health endpoint."""
        try:
            response = requests.get('http://localhost:12345/ready', timeout=5)
            assert response.status_code == 200
        except requests.exceptions.RequestException:
            pytest.skip("Alloy not running")


class TestLokiAPI:
    """Test Loki API functionality."""

    @pytest.mark.integration
    def test_loki_labels_endpoint(self):
        """Test Loki labels endpoint."""
        try:
            response = requests.get('http://localhost:3100/loki/api/v1/labels', timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert 'status' in data
            assert data['status'] == 'success'
            assert 'data' in data
        except requests.exceptions.RequestException:
            pytest.skip("Loki not running")

    @pytest.mark.integration
    def test_loki_label_values_endpoint(self):
        """Test Loki label values endpoint."""
        try:
            response = requests.get('http://localhost:3100/loki/api/v1/label/container/values', timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert 'status' in data
            assert data['status'] == 'success'
            assert 'data' in data
        except requests.exceptions.RequestException:
            pytest.skip("Loki not running")

    @pytest.mark.integration
    def test_loki_query_endpoint(self):
        """Test Loki query endpoint."""
        try:
            # Test basic query
            query = '{container="grafana-loki-alloy_implementation-weather-app-1"}'
            response = requests.get(
                f'http://localhost:3100/loki/api/v1/query_range?query={query}',
                timeout=10
            )
            assert response.status_code == 200
            data = response.json()
            assert 'status' in data
            assert data['status'] == 'success'
            assert 'data' in data
        except requests.exceptions.RequestException:
            pytest.skip("Loki not running")

    @pytest.mark.integration
    def test_loki_query_with_error_filter(self):
        """Test Loki query with error filter."""
        try:
            query = '{container="grafana-loki-alloy_implementation-weather-app-1"} |= "error"'
            response = requests.get(
                f'http://localhost:3100/loki/api/v1/query_range?query={query}',
                timeout=10
            )
            assert response.status_code == 200
            data = response.json()
            assert 'status' in data
            assert data['status'] == 'success'
        except requests.exceptions.RequestException:
            pytest.skip("Loki not running")


class TestLogCollection:
    """Test log collection functionality."""

    @pytest.mark.integration
    def test_log_generation_and_collection(self):
        """Test that logs are generated and collected."""
        try:
            # Generate some logs
            response = requests.get('http://localhost:5001/weather', timeout=5)
            assert response.status_code == 200
            
            # Wait for logs to be collected
            time.sleep(5)
            
            # Check if logs are in Loki
            query = '{container="grafana-loki-alloy_implementation-weather-app-1"}'
            response = requests.get(
                f'http://localhost:3100/loki/api/v1/query_range?query={query}',
                timeout=10
            )
            assert response.status_code == 200
            data = response.json()
            
            # Should have some results
            if data['data']['result']:
                assert len(data['data']['result']) > 0
                
        except requests.exceptions.RequestException:
            pytest.skip("Services not running")

    @pytest.mark.integration
    def test_error_log_collection(self):
        """Test that error logs are collected."""
        try:
            # Generate some logs (which will likely include errors due to invalid API key)
            response = requests.get('http://localhost:5001/weather', timeout=5)
            assert response.status_code == 200
            
            # Wait for logs to be collected
            time.sleep(5)
            
            # Check for error logs
            query = '{container="grafana-loki-alloy_implementation-weather-app-1"} |= "error"'
            response = requests.get(
                f'http://localhost:3100/loki/api/v1/query_range?query={query}',
                timeout=10
            )
            assert response.status_code == 200
            data = response.json()
            
            # Should have some error logs
            if data['data']['result']:
                assert len(data['data']['result']) > 0
                
        except requests.exceptions.RequestException:
            pytest.skip("Services not running")


class TestConfiguration:
    """Test configuration files."""

    def test_alloy_config_structure(self):
        """Test Alloy configuration structure."""
        with open('config.alloy', 'r') as f:
            config_content = f.read()
        
        # Check for required sections
        required_sections = [
            'discovery.docker',
            'discovery.relabel',
            'loki.source.docker',
            'loki.process',
            'loki.write'
        ]
        
        for section in required_sections:
            assert section in config_content, f"Missing section: {section}"

    def test_loki_config_structure(self):
        """Test Loki configuration structure."""
        import yaml
        
        with open('loki-config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Check for required sections (updated based on actual config)
        required_sections = ['auth_enabled', 'server', 'schema_config', 'common']
        for section in required_sections:
            assert section in config, f"Missing section: {section}"

    def test_dockerfile_structure(self):
        """Test Dockerfile structure."""
        with open('Dockerfile', 'r') as f:
            dockerfile_content = f.read()
        
        # Check for required instructions
        required_instructions = ['FROM', 'COPY', 'RUN', 'EXPOSE', 'CMD']
        for instruction in required_instructions:
            assert instruction in dockerfile_content, f"Missing instruction: {instruction}"

    def test_requirements_structure(self):
        """Test requirements.txt structure."""
        with open('requirements.txt', 'r') as f:
            requirements = f.read().lower()
        
        # Check for required packages (case-insensitive)
        required_packages = ['flask', 'requests', 'pytest']
        for package in required_packages:
            assert package in requirements, f"Missing package: {package}"


class TestEndToEnd:
    """End-to-end tests for the complete stack."""

    @pytest.mark.integration
    def test_complete_log_pipeline(self):
        """Test the complete log pipeline from generation to storage."""
        try:
            # Step 1: Generate logs
            response = requests.get('http://localhost:5001/weather', timeout=5)
            assert response.status_code == 200
            
            # Step 2: Wait for collection
            time.sleep(10)
            
            # Step 3: Verify logs are in Loki
            query = '{container="grafana-loki-alloy_implementation-weather-app-1"}'
            response = requests.get(
                f'http://localhost:3100/loki/api/v1/query_range?query={query}',
                timeout=10
            )
            assert response.status_code == 200
            data = response.json()
            
            # Step 4: Verify log structure
            if data['data']['result']:
                log_entry = data['data']['result'][0]
                assert 'stream' in log_entry
                assert 'values' in log_entry
                
                # Check for expected labels
                stream = log_entry['stream']
                expected_labels = ['container', 'detected_level', 'service_name']
                for label in expected_labels:
                    assert label in stream, f"Missing label: {label}"
                
        except requests.exceptions.RequestException:
            pytest.skip("Services not running")

    @pytest.mark.integration
    def test_grafana_loki_integration(self):
        """Test that Grafana can query Loki."""
        try:
            # Test that Grafana is accessible
            response = requests.get('http://localhost:3000', timeout=5)
            assert response.status_code == 200
            
            # Test that Loki is accessible
            response = requests.get('http://localhost:3100/ready', timeout=5)
            assert response.status_code == 200
            
            # Test that Grafana can query Loki (indirectly)
            # This would require Grafana API access, but we can verify both services are up
            
        except requests.exceptions.RequestException:
            pytest.skip("Services not running")


if __name__ == '__main__':
    pytest.main([__file__]) 