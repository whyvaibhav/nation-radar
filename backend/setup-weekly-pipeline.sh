#!/bin/bash

# Nation Radar Weekly Pipeline Setup Script
# This script sets up the weekly collection pipeline for the 500/month API quota

echo "🚀 Setting up Nation Radar Weekly Pipeline..."
echo "📊 API Quota: 500 requests/month"
echo "⏰ Collection Frequency: Weekly (every 7 days)"
echo "📈 Expected Collection: 30 tweets per run"

# Navigate to the backend directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "❌ Virtual environment not found. Please create it first:"
    echo "   python3 -m venv ../venv"
    echo "   source ../venv/bin/activate"
    echo "   pip install -r ../requirements.txt"
    exit 1
fi

# Copy the weekly service file
echo "📋 Installing weekly pipeline service..."
sudo cp nation-radar-pipeline-weekly.service /etc/systemd/system/

# Reload systemd
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

# Enable the service
echo "✅ Enabling weekly pipeline service..."
sudo systemctl enable nation-radar-pipeline-weekly

# Start the service
echo "🚀 Starting weekly pipeline service..."
sudo systemctl start nation-radar-pipeline-weekly

# Check status
echo "📊 Checking service status..."
sudo systemctl status nation-radar-pipeline-weekly

echo ""
echo "🎯 Weekly Pipeline Setup Complete!"
echo ""
echo "📋 Service Information:"
echo "   • Service Name: nation-radar-pipeline-weekly"
echo "   • Frequency: Every 7 days (604,800 seconds)"
echo "   • Collection: 6 keywords × 5 tweets = 30 tweets per run"
echo "   • Monthly API Usage: ~360 requests (72% of quota)"
echo "   • Quota Buffer: 140 requests for testing/manual runs"
echo ""
echo "🔧 Management Commands:"
echo "   • Check Status: sudo systemctl status nation-radar-pipeline-weekly"
echo "   • View Logs: sudo journalctl -u nation-radar-pipeline-weekly -f"
echo "   • Manual Run: cd ~/nation-radar/backend && source ../venv/bin/activate && python3 run_pipeline.py"
echo "   • Stop Service: sudo systemctl stop nation-radar-pipeline-weekly"
echo "   • Disable Service: sudo systemctl disable nation-radar-pipeline-weekly"
echo ""
echo "📊 Monitor Database Growth:"
echo "   • Tweet Count: sqlite3 tweets.db 'SELECT COUNT(*) FROM tweets;'"
echo "   • Latest Tweets: sqlite3 tweets.db 'SELECT username, text, score, created_at FROM tweets ORDER BY created_at DESC LIMIT 10;'"
echo ""
echo "🎉 Your Nation Radar is now set for weekly, sustainable data collection!"
