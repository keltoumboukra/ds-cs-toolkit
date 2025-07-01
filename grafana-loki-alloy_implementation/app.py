#!/usr/bin/env python3
"""
Simple log generator application for testing Grafana Loki and Alloy
"""

import logging
import random
import time
import threading
from datetime import datetime
from flask import Flask, jsonify, request
import os

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

# Sample data for generating realistic logs
users = ["alice", "bob", "charlie", "diana", "eve"]
actions = ["login", "logout", "search", "download", "upload", "delete", "create"]
resources = ["document", "image", "video", "audio", "database", "file"]
errors = ["timeout", "permission denied", "not found", "server error", "network error"]

def generate_random_log():
    """Generate a random log entry"""
    log_type = random.choice(["info", "warning", "error"])
    user = random.choice(users)
    action = random.choice(actions)
    resource = random.choice(resources)
    
    if log_type == "info":
        message = f"User {user} performed {action} on {resource}"
        logger.info(message)
    elif log_type == "warning":
        message = f"Warning: {action} operation on {resource} took longer than expected"
        logger.warning(message)
    else:  # error
        error_type = random.choice(errors)
        message = f"Error: {error_type} occurred during {action} operation on {resource}"
        logger.error(message)

def log_generator():
    """Background thread that generates logs continuously"""
    while True:
        try:
            generate_random_log()
            # Random delay between 1-5 seconds
            time.sleep(random.uniform(1, 5))
        except Exception as e:
            logger.error(f"Error in log generator: {e}")
            time.sleep(5)

@app.route('/')
def home():
    """Home page with basic info"""
    return jsonify({
        "message": "Log Generator is running",
        "endpoints": {
            "home": "/",
            "status": "/status",
            "generate_log": "/generate_log",
            "logs": "/logs"
        }
    })

@app.route('/status')
def status():
    """Application status"""
    return jsonify({
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "log_level": os.getenv("LOG_LEVEL", "INFO")
    })

@app.route('/generate_log')
def generate_log():
    """Manually generate a log entry"""
    log_type = request.args.get('type', 'info')
    message = request.args.get('message', 'Manual log entry')
    
    if log_type == 'info':
        logger.info(message)
    elif log_type == 'warning':
        logger.warning(message)
    elif log_type == 'error':
        logger.error(message)
    else:
        logger.info(message)
    
    return jsonify({
        "message": "Log generated",
        "type": log_type,
        "content": message,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/logs')
def get_logs():
    """Return recent log entries (simulated)"""
    return jsonify({
        "message": "Logs are being collected by Grafana Loki",
        "view_logs": "Check Grafana at http://localhost:3000",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Start the background log generator
    log_thread = threading.Thread(target=log_generator, daemon=True)
    log_thread.start()
    
    logger.info("Log Generator application starting...")
    logger.info("Access the application at http://localhost:5000")
    logger.info("Logs will be automatically generated and sent to Loki")
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=False) 