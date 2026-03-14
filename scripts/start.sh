#!/bin/bash

# Autonomous Code Evolution System - Startup Script

echo "--- ACES: Starting System ---"

# Check for Docker
if ! command -v docker &> /dev/null
then
    echo "Error: Docker could not be found. Please install Docker first."
    exit 1
fi

# Load Environment Variables (optional)
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

echo "1. Building and Starting Containers..."
docker-compose up -d --build

echo "2. Waiting for Services..."
sleep 10

echo "3. Checking System Health..."
# Simple health check (assuming curl is available)
if curl -s http://localhost:5678/healthz > /dev/null; then
    echo "   - Orchestrator (n8n): OK"
else
    echo "   - Orchestrator (n8n): Waiting..."
fi

if curl -s http://localhost:8000/health > /dev/null; then
    echo "   - MCP Server: OK"
else
    echo "   - MCP Server: Waiting..."
fi

if curl -s http://localhost:8081/api/v1/god-mode > /dev/null; then
    echo "   - Plane Backend: OK"
else
    echo "   - Plane Backend: Waiting..."
fi

echo "--- ACES is Running ---"
echo "Orchestrator UI: http://localhost:5678"
echo "MCP Server API: http://localhost:8000"
echo "Plane API: http://localhost:8081"
