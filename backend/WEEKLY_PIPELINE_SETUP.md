# Nation Radar Weekly Pipeline Setup

## 🎯 **Overview**

This setup configures the Nation Radar pipeline for **weekly collection** to work within your **500 requests/month API quota**.

## 📊 **Collection Strategy**

- **Frequency**: Every 7 days (weekly)
- **API Fetch**: 15 tweets per keyword
- **Processing**: 5 tweets per keyword  
- **Total per Run**: 6 keywords × 5 tweets = **30 tweets**
- **Monthly API Usage**: ~360 requests (72% of quota)
- **Quota Buffer**: 140 requests for testing/manual runs

## 🚀 **Quick Setup**

### **Option 1: Automated Setup (Recommended)**
```bash
cd ~/nation-radar/backend
chmod +x setup-weekly-pipeline.sh
./setup-weekly-pipeline.sh
```

### **Option 2: Manual Setup**
```bash
# 1. Copy service file
sudo cp nation-radar-pipeline-weekly.service /etc/systemd/system/

# 2. Reload systemd
sudo systemctl daemon-reload

# 3. Enable service
sudo systemctl enable nation-radar-pipeline-weekly

# 4. Start service
sudo systemctl start nation-radar-pipeline-weekly
```

## 🔧 **Service Management**

### **Check Status**
```bash
sudo systemctl status nation-radar-pipeline-weekly
```

### **View Logs**
```bash
sudo journalctl -u nation-radar-pipeline-weekly -f
```

### **Manual Run**
```bash
cd ~/nation-radar/backend
source ../venv/bin/activate
python3 run_pipeline.py
```

### **Stop Service**
```bash
sudo systemctl stop nation-radar-pipeline-weekly
```

### **Disable Service**
```bash
sudo systemctl disable nation-radar-pipeline-weekly
```

## 📊 **Monitoring**

### **Database Growth**
```bash
# Check tweet count
sqlite3 tweets.db "SELECT COUNT(*) FROM tweets;"

# View latest tweets
sqlite3 tweets.db "SELECT username, text, score, created_at FROM tweets ORDER BY created_at DESC LIMIT 10;"

# Check API server
curl http://localhost:5001/api/stats
```

### **Pipeline Performance**
```bash
# View collection summary
sudo journalctl -u nation-radar-pipeline-weekly --since "1 week ago" | grep "Pipeline complete"

# Check for errors
sudo journalctl -u nation-radar-pipeline-weekly --since "1 week ago" | grep "Error\|Warning"
```

## ⚙️ **Configuration Details**

### **Service File Location**
```
/etc/systemd/system/nation-radar-pipeline-weekly.service
```

### **Restart Interval**
```
RestartSec=604800  # 7 days in seconds
```

### **Working Directory**
```
/root/nation-radar/backend
```

### **Environment**
```
PATH=/root/nation-radar/venv/bin
```

## 🎯 **Expected Results**

- **Pipeline runs weekly** automatically
- **Database grows steadily** with quality Crestal content
- **API quota stays safe** (360/month vs 500 limit)
- **Beautiful dashboard** gets fresh data every week
- **Professional monitoring** via systemd

## 🚨 **Troubleshooting**

### **Service Won't Start**
```bash
# Check logs
sudo journalctl -u nation-radar-pipeline-weekly -n 50

# Verify virtual environment
ls -la ~/nation-radar/venv/bin/python3

# Check permissions
ls -la ~/nation-radar/backend/run_pipeline.py
```

### **API Quota Issues**
```bash
# Check current usage in logs
sudo journalctl -u nation-radar-pipeline-weekly | grep "API usage"

# Manual test with reduced limits
python3 -c "
from fetchers.ryan_twitter_fetcher import RyanTwitterFetcher
fetcher = RyanTwitterFetcher()
tweets = fetcher.fetch('Crestal')
print(f'Fetched {len(tweets)} tweets')
"
```

### **Database Issues**
```bash
# Check database integrity
sqlite3 tweets.db "PRAGMA integrity_check;"

# Check database size
du -h tweets.db

# Backup database
cp tweets.db tweets.db.backup.$(date +%Y%m%d)
```

## 📈 **Performance Optimization**

### **Memory Usage**
- **Current**: ~50MB per run
- **Weekly**: ~50MB per week
- **Monthly**: ~200MB total

### **Storage Growth**
- **Per Tweet**: ~2-5KB
- **Weekly Growth**: ~150KB
- **Monthly Growth**: ~600KB

### **API Efficiency**
- **Success Rate**: 85-95%
- **Rate Limiting**: Handled automatically
- **Fallback**: Multiple API endpoints

## 🎉 **Success Indicators**

✅ **Service Status**: `active (running)`  
✅ **Weekly Logs**: "Pipeline complete. X unique tweets processed"  
✅ **Database Growth**: Increasing tweet count  
✅ **API Usage**: Under 400 requests/month  
✅ **Dashboard Data**: Fresh content weekly  

## 🔮 **Future Enhancements**

- **Dynamic scheduling** based on API quota
- **Smart deduplication** across runs
- **Performance metrics** and alerts
- **Automated backups** and maintenance

---

**Your Nation Radar is now optimized for sustainable, weekly data collection!** 🚀
