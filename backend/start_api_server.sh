#!/bin/bash

# Nation Radar VPS API Server Startup Script

echo "🚀 Starting Nation Radar VPS API Server..."

# Navigate to the backend directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "../venv" ]; then
    echo "📦 Activating virtual environment..."
    source ../venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv ../venv
    source ../venv/bin/activate
    pip install -r ../requirements.txt
fi

# Check if database exists
if [ ! -f "tweets.db" ]; then
    echo "❌ Database not found. Please run the pipeline first:"
    echo "   python3 run_pipeline.py"
    exit 1
fi

# Set environment variables
export VPS_API_PORT=5001

# Start the API server
echo "🌐 Starting API server on port $VPS_API_PORT..."
echo "📊 Database: $(pwd)/tweets.db"
echo "🔗 API endpoints:"
echo "   - http://localhost:$VPS_API_PORT/"
echo "   - http://localhost:$VPS_API_PORT/api/tweets"
echo "   - http://localhost:$VPS_API_PORT/api/leaderboard"
echo "   - http://localhost:$VPS_API_PORT/api/stats"
echo "   - http://localhost:$VPS_API_PORT/api/search?q=keyword"

# Start the server
python3 api_server.py
