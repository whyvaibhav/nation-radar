#!/bin/bash
# VPS Deployment Script for Crestal Network Monitor
# Run this on your fresh Ubuntu VPS

set -e  # Exit on any error

echo "🚀 Starting Crestal Network Monitor VPS Deployment"

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
echo "🐍 Installing Python and tools..."
sudo apt install -y python3 python3-pip python3-venv git htop curl unzip

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /opt/crestal-monitor
sudo chown $USER:$USER /opt/crestal-monitor
cd /opt/crestal-monitor

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "📋 Installing Python dependencies..."
pip install --upgrade pip
pip install requests python-dotenv gspread oauth2client google-generativeai schedule pandas flask flask-cors

# Create directory structure
echo "📂 Creating directory structure..."
mkdir -p {fetchers,storage,frontend,logs,data}

echo "✅ VPS setup complete!"
echo ""
echo "Next steps:"
echo "1. Upload your project files to /opt/crestal-monitor/"
echo "2. Create .env file with your API keys"
echo "3. Run: ./start_monitoring.sh"
