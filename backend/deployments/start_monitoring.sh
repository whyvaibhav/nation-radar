#!/bin/bash
# Start Script for VPS Deployment

# Get the script directory and go to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -d "venv/bin" ]; then
    source venv/bin/activate
elif [ -d "../venv/bin" ]; then
    source ../venv/bin/activate
fi

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "⚠️  Creating .env template - PLEASE UPDATE WITH YOUR API KEYS!"
    cat > .env << EOF
# Crestal Monitor Environment Variables
RAPIDAPI_KEY=your_rapidapi_key_here
NATION_AGENT_API_KEY=your_nation_agent_api_key_here
DEBUG_MODE=False
EOF
    echo "❌ Please edit .env file with your actual API keys!"
    echo "nano .env"
    exit 1
fi

# Check if API keys are configured (look for placeholder values)
if grep -q "your_rapidapi_key_here\|your_nation_agent_api_key_here\|YOUR_.*_KEY" .env; then
    echo "❌ Please configure your API keys in .env file first!"
    echo "nano .env"
    echo ""
    echo "Current .env contents:"
    cat .env
    exit 1
fi

# Create logs directory
mkdir -p logs

echo "🎯 Starting Crestal Network Monitor..."

# Start the scheduler in background with nohup
nohup python scheduler.py > logs/monitor.log 2>&1 &
SCHEDULER_PID=$!

# Start the web dashboard in background
nohup python app.py > logs/webapp.log 2>&1 &
WEBAPP_PID=$!

# Save PIDs for stopping later
echo $SCHEDULER_PID > logs/scheduler.pid
echo $WEBAPP_PID > logs/webapp.pid

echo "✅ Crestal Monitor started successfully!"
echo ""
echo "📊 Monitor logs:     tail -f logs/monitor.log"
echo "🌐 Web dashboard:    http://your-vps-ip:5000"
echo "📋 Scheduler logs:   tail -f logs/scheduler.log"
echo ""
echo "🛑 To stop:          ./stop_monitoring.sh"
echo "🔄 To restart:       ./restart_monitoring.sh"
