# 🌐 VPS Frontend Integration Guide

## 🎯 How VPS Data Flows to Your Frontend Leaderboard

### **Data Flow Overview:**
```
VPS Pipeline → groktweets.csv → Flask API → Frontend Leaderboard
```

## 🚀 **Option 1: All-in-One VPS (Recommended)**

Run everything on your VPS - both data collection and web frontend:

### **Setup:**
```bash
# On your VPS
cd /opt/crestal-monitor

# Start both pipeline and web dashboard
./start_monitoring.sh

# Your frontend is now live at:
http://your-vps-ip:5000
```

### **What happens:**
1. ✅ **Pipeline runs every hour** → Updates `groktweets.csv`
2. ✅ **Web dashboard serves data** → Reads from `groktweets.csv`
3. ✅ **Frontend shows live data** → Real-time leaderboard
4. ✅ **Automatic updates** → New tweets appear automatically

### **Access your leaderboard:**
- Visit `http://your-vps-ip:5000`
- Data updates every hour
- Shows real Crestal tweets with AI scores

---

## 🔄 **Option 2: Separate VPS + Local Frontend**

VPS collects data, local computer runs frontend:

### **VPS Side (Data Collection):**
```bash
# Only run the pipeline on VPS
python scheduler.py  # Collects data only
```

### **Local Side (Frontend):**
```bash
# Download data from VPS periodically
scp root@your-vps-ip:/opt/crestal-monitor/groktweets.csv ./

# Run local web dashboard
python app.py
```

### **Automation script for local:**
```bash
#!/bin/bash
# sync_vps_data.sh - Run this every hour locally

# Download latest data from VPS
scp root@your-vps-ip:/opt/crestal-monitor/groktweets.csv ./
scp root@your-vps-ip:/opt/crestal-monitor/tweets.db ./

echo "✅ Data synced from VPS"
```

---

## 🌍 **Option 3: Cloud Frontend + VPS Backend**

VPS collects data, cloud frontend (Vercel/Netlify):

### **VPS API Endpoint:**
```bash
# Expose API publicly (add to start_monitoring.sh)
python app.py --host=0.0.0.0 --port=5000
```

### **Cloud Frontend Config:**
```javascript
// In your cloud frontend
const VPS_API_URL = 'http://your-vps-ip:5000';

fetch(`${VPS_API_URL}/api/crestal-data`)
    .then(response => response.json())
    .then(data => updateLeaderboard(data));
```

### **Security considerations:**
```bash
# Add API key protection
CRESTAL_API_KEY=your_secret_key

# Or use VPN/reverse proxy
```

---

## 📊 **Leaderboard Features You Get**

### **Real-time Data:**
- Live tweet scores from Nation Agent
- Automatic hourly updates
- Quality statistics

### **Leaderboard Display:**
```
🏆 Top Crestal Contributors
┌─────────────────────────────────────┐
│ @username1  │ 1.85 │ 🌟 Excellent  │
│ @username2  │ 1.65 │ 👍 Good       │  
│ @username3  │ 1.45 │ 👍 Good       │
│ @username4  │ 0.85 │ 😐 Average    │
└─────────────────────────────────────┘

📈 Stats: 45 tweets, avg 1.2, 12 high-quality
```

### **Interactive Features:**
- Click tweets to view full content
- Filter by score range
- Sort by date/score
- Real-time updates

---

## ⚙️ **Configuration Options**

### **Update Frequency:**
```python
# In scheduler.py - change from hourly to:
schedule.every(30).minutes.do(run_pipeline)  # 30 min
schedule.every(15).minutes.do(run_pipeline)  # 15 min
```

### **Leaderboard Size:**
```python
# In app.py - limit results
df = df.nlargest(50, 'score')  # Top 50 tweets
```

### **Score Thresholds:**
```javascript
// In frontend/script.js
function getScoreClass(score) {
    if (score >= 1.8) return 'score-legendary';
    if (score >= 1.5) return 'score-excellent';
    if (score >= 1.0) return 'score-good';
    // ... customize as needed
}
```

---

## 🎯 **Recommended Setup**

**For Simplicity:** Use **Option 1** (All-in-One VPS)
- Single server handles everything
- No data syncing needed
- Always up-to-date
- Cost: ~$5/month VPS

**For Scale:** Use **Option 3** (Cloud Frontend)
- Faster frontend loading
- Better uptime
- Professional domain
- Cost: VPS + cloud hosting

---

## 🚀 **Quick Start (Option 1)**

```bash
# 1. Deploy to VPS
cd Install/
./deploy_vps.sh

# 2. Upload your code
scp -r ../* root@your-vps-ip:/opt/crestal-monitor/

# 3. Configure & start
ssh root@your-vps-ip
cd /opt/crestal-monitor
nano .env  # Add your API keys
./start_monitoring.sh

# 4. Access leaderboard
# Open: http://your-vps-ip:5000
```

Your Crestal leaderboard is now live with real AI-scored data! 🎉
