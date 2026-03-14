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

# Login to GitHub Container Registry to pull the OpenClaw image
if [ -n "$GITHUB_REPO_OWNER" ] && [ -n "$GITHUB_PAT" ]; then
    echo "Attempting to log in to GitHub Container Registry (ghcr.io)..."
    echo "$GITHUB_PAT" | docker login ghcr.io -u "$GITHUB_REPO_OWNER" --password-stdin
else
    echo "Warning: GITHUB_REPO_OWNER and GITHUB_PAT are not set in .env. Pulling the OpenClaw image may fail if it's private."
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

# A simple check to see if OpenClaw is responding on its port
if curl -s http://localhost:8081/ > /dev/null; then
    echo "   - OpenClaw Executor: OK"
else
    echo "   - OpenClaw Executor: Waiting..."
fi

echo "--- ACES is Running ---"
echo "Orchestrator UI: http://localhost:5678"
echo "MCP Server API: http://localhost:8000"
echo "Kanban UI (Planka): http://localhost:3000"
echo "OpenClaw Executor: http://localhost:8081"
