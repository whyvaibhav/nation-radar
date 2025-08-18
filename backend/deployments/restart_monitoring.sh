#!/bin/bash
# Restart Crestal Monitor

# Get the script directory and go to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "🔄 Restarting Crestal Network Monitor..."

# Stop existing processes
./deployments/stop_monitoring.sh

# Wait a moment
sleep 2

# Start fresh
./deployments/start_monitoring.sh