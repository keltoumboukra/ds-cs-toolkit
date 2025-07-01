#!/bin/bash

echo "🛑 Stopping Weather API Log Collection Stack..."
echo ""

# Stop the services
echo "📦 Stopping services..."
docker compose down

echo ""
echo "✅ Services stopped!"
echo "All containers have been stopped and removed." 