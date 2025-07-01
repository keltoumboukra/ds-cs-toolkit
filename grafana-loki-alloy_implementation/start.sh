#!/bin/bash

echo "🚀 Starting Mac Log Collection Stack..."
echo "This will start Grafana Loki, Grafana, and Alloy to collect your Mac logs"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start the services
echo "📦 Starting services..."
docker compose up -d

# Wait a moment for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
if docker compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Services are running!"
    echo ""
    echo "🌐 Access your logs at:"
    echo "   Grafana:     http://localhost:3000"
    echo "   Alloy UI:    http://localhost:12345/graph"
    echo "   Loki API:    http://localhost:3100"
    echo ""
    echo "📊 To view logs:"
    echo "   1. Open http://localhost:3000"
    echo "   2. Click 'Explore'"
    echo "   3. Select 'Loki' data source"
    echo "   4. Try queries like: {source=\"system\"} or {platform=\"macos\"}"
    echo ""
    echo "🛑 To stop services: docker compose down"
else
    echo "❌ Some services failed to start. Check logs with: docker compose logs"
    exit 1
fi 