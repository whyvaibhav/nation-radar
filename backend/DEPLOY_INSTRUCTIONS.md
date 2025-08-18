# 🚀 Nation Radar VPS Deployment Instructions

## Quick Deployment (15 minutes)

### Prerequisites
- ✅ VPS with Ubuntu 22.04 (DigitalOcean/Linode/Vultr)
- ✅ SSH access to your VPS
- ✅ Your API keys ready (RAPIDAPI_KEY, NATION_AGENT_API_KEY)

### Step 1: Connect to Your VPS
```bash
# Replace with your VPS IP
ssh root@YOUR_VPS_IP
```

### Step 2: Quick Setup Script
```bash
# Run the automated setup
curl -sSL https://raw.githubusercontent.com/yourusername/nation-radar/main/deployments/deploy_vps.sh | bash

# Or manual download:
wget https://raw.githubusercontent.com/yourusername/nation-radar/main/deployments/deploy_vps.sh
chmod +x deploy_vps.sh
./deploy_vps.sh
```

### Step 3: Deploy Nation Radar
```bash
# Clone your project
cd /opt/nation-radar
git clone https://github.com/yourusername/nation-radar.git .

# Install dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Create environment file
cp .env.example .env
nano .env

# Add your API keys:
RAPIDAPI_KEY=your_actual_rapidapi_key_here
NATION_AGENT_API_KEY=your_actual_nation_agent_key_here
DEBUG_MODE=False
```

### Step 5: Start Nation Radar
```bash
# Make scripts executable
chmod +x deployments/*.sh

# Start 24/7 monitoring
./deployments/start_monitoring.sh
```

### Step 6: Access Your Dashboard
```
🌐 Web Dashboard: http://YOUR_VPS_IP:5000
📊 Live Leaderboard: Real-time updates
🔄 Pipeline: Runs every hour automatically
```

## Management Commands

```bash
# Check status
./deployments/status.sh

# View logs
tail -f logs/monitor.log

# Restart services
./deployments/restart_monitoring.sh

# Stop monitoring
./deployments/stop_monitoring.sh
```

## Firewall Setup (Important!)
```bash
# Allow SSH and web dashboard
sudo ufw allow 22
sudo ufw allow 5000
sudo ufw enable
```

## What Happens After Deployment

✅ **Pipeline runs every hour** collecting tweets
✅ **Nation Agent scores** content quality  
✅ **Web dashboard** available at your VPS IP
✅ **Data stored** in tweets.csv and tweets.db
✅ **Logs tracked** for monitoring and debugging

## Troubleshooting

### Check if services are running:
```bash
./deployments/status.sh
```

### View recent logs:
```bash
tail -20 logs/monitor.log
tail -20 logs/scheduler.log
```

### Test Nation Agent connection:
```bash
python tests/test_nation_agent_local.py
```

### Restart everything:
```bash
./deployments/restart_monitoring.sh
```

---

🎯 **Your Nation Radar will be live and monitoring the Crestal ecosystem 24/7!**
