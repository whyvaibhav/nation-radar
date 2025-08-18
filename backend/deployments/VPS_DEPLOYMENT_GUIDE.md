# 🚀 VPS Deployment Guide - Crestal Network Monitor

## Quick Setup (5 minutes)

### 1. Get a VPS
- **DigitalOcean**: Create $5 droplet with Ubuntu 22.04
- **Linode**: $5 Nanode with Ubuntu 22.04  
- **Vultr**: $3.50 instance with Ubuntu 22.04

### 2. Initial Server Setup
```bash
# SSH into your VPS
ssh root@your-vps-ip

# Download and run deployment script
wget https://raw.githubusercontent.com/your-repo/deploy_vps.sh
chmod +x deploy_vps.sh
./deploy_vps.sh
```

### 3. Upload Your Project
```bash
# On your local machine, upload files to VPS
scp -r * root@your-vps-ip:/opt/crestal-monitor/

# Or use git (recommended)
cd /opt/crestal-monitor
git clone https://github.com/your-username/your-repo.git .
```

### 4. Configure Environment
```bash
cd /opt/crestal-monitor

# Edit .env file with your API keys
nano .env

# Add your keys:
RAPIDAPI_KEY=your_actual_rapidapi_key
NATION_AGENT_API_KEY=your_actual_nation_agent_key
DEBUG_MODE=False
```

### 5. Start Monitoring
```bash
# Make scripts executable
chmod +x *.sh

# Start the monitor
./start_monitoring.sh
```

## 🎛️ Management Commands

```bash
# Check status
./status.sh

# View live logs
tail -f logs/monitor.log
tail -f logs/scheduler.log

# Stop monitoring
./stop_monitoring.sh

# Restart monitoring
./restart_monitoring.sh
```

## 🌐 Access Web Dashboard

Visit: `http://your-vps-ip:5000`

To make it accessible, ensure your VPS firewall allows port 5000:
```bash
# Ubuntu/Debian
sudo ufw allow 5000

# Or use VPS provider dashboard to open port 5000
```

## 📊 Monitoring & Maintenance

### Check System Health
```bash
# Overall status
./status.sh

# System resources
htop

# Disk space
df -h

# Recent activity
tail -f logs/scheduler.log
```

### Scheduled Tasks
The system automatically:
- ✅ Runs every hour to collect Crestal tweets
- ✅ Scores tweets using Nation Agent API
- ✅ Stores results in SQLite + CSV
- ✅ Handles errors gracefully
- ✅ Logs all activity

### Data Locations
- **Tweet Data**: `/opt/crestal-monitor/groktweets.csv`
- **Database**: `/opt/crestal-monitor/tweets.db`
- **Logs**: `/opt/crestal-monitor/logs/`

## 🔧 Troubleshooting

### Monitor Not Running
```bash
# Check what's wrong
./status.sh

# Restart everything
./restart_monitoring.sh

# Check logs for errors
tail -20 logs/monitor.log
```

### API Key Issues
```bash
# Test Nation Agent API
python3 test_nation_agent_local.py

# Check environment
cat .env
```

### Web Dashboard Not Accessible
```bash
# Check if app is running
./status.sh

# Check firewall
sudo ufw status

# Restart web dashboard
./restart_monitoring.sh
```

## 💰 Cost Breakdown

**Monthly VPS Costs:**
- **DigitalOcean**: $5/month
- **Linode**: $5/month  
- **Vultr**: $3.50/month

**API Costs:**
- **RapidAPI (Ryan's Twitter)**: ~$10/month for moderate usage
- **Crestal Nation Agent**: Varies by usage

**Total**: ~$15-20/month for 24/7 operation

## 🔄 Auto-Start on Boot

To ensure monitoring starts automatically if VPS reboots:

```bash
# Add to crontab
crontab -e

# Add this line:
@reboot cd /opt/crestal-monitor && ./start_monitoring.sh
```

## 📈 Scaling Up

As your monitoring grows:
- **More Keywords**: Edit `config.yaml`
- **Higher Frequency**: Modify `scheduler.py`
- **Better VPS**: Upgrade to 2GB RAM for more parallel processing
- **Multiple Regions**: Deploy to multiple VPS for redundancy

## 🎯 Quick Commands Reference

```bash
# Start
./start_monitoring.sh

# Stop  
./stop_monitoring.sh

# Status
./status.sh

# Logs
tail -f logs/monitor.log

# Restart
./restart_monitoring.sh
```

---

🚀 **Your Crestal Monitor is now running 24/7!** 

Access your dashboard at `http://your-vps-ip:5000` and monitor those Crestal tweets around the clock! 🎯
