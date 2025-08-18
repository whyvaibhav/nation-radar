# Nation Radar API Setup Guide

## 🚀 **Professional API-Based Architecture**

This guide sets up a professional system where:
- **VPS**: Runs data pipeline + API server
- **Railway**: Fetches data via HTTP API calls
- **Real-time**: Live data updates without Git sync

## 🏗️ **System Architecture**

```
VPS (Backend)                    Railway (Frontend)
┌─────────────────┐             ┌─────────────────┐
│ run_pipeline.py │             │ app.py          │
│ ↓               │             │ ↓               │
│ tweets.db       │             │ HTTP Requests   │
│ ↓               │             │ ↓               │
│ api_server.py   │◄────────────┤ Frontend        │
│ (Port 5001)     │             │ Dashboard       │
└─────────────────┘             └─────────────────┘
```

## 🔧 **VPS Setup Steps**

### **Step 1: Start the API Server**
```bash
cd ~/nation-radar/backend

# Make startup script executable
chmod +x start_api_server.sh

# Start the API server
./start_api_server.sh
```

### **Step 2: Test the API Server**
```bash
# Test if API is working
curl http://localhost:5001/

# Test tweets endpoint
curl http://localhost:5001/api/tweets

# Test stats endpoint
curl http://localhost:5001/api/stats
```

### **Step 3: Set Up as System Service (Optional)**
```bash
# Copy service file
sudo cp nation-radar-api.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable nation-radar-api
sudo systemctl start nation-radar-api

# Check status
sudo systemctl status nation-radar-api
```

### **Step 4: Configure Firewall (if needed)**
```bash
# Allow port 5001 (if using UFW)
sudo ufw allow 5001

# Or for iptables
sudo iptables -A INPUT -p tcp --dport 5001 -j ACCEPT
```

## 🌐 **Railway Configuration**

### **Step 1: Set Environment Variable**
In your Railway dashboard, add this environment variable:

```env
VPS_API_URL=http://143.198.226.161:5001
```

**Your VPS IP is already configured in the code.**

### **Step 2: Deploy Updated Code**
```bash
# Commit and push the API changes
git add .
git commit -m "Implement API-based architecture"
git push origin main
```

Railway will automatically redeploy with the new API-based system.

## 🔍 **Testing the Integration**

### **Test VPS API:**
```bash
# On your VPS
curl http://localhost:5001/api/stats
```

### **Test Railway Frontend:**
Visit your Railway URL and check:
- `/api/system-status` - Should show VPS connection status
- `/api/crestal-data` - Should fetch data from VPS
- `/api/leaderboard` - Should show top tweets

## 📊 **Monitoring & Health Checks**

### **VPS API Status:**
```bash
# Check if API is running
curl http://localhost:5001/

# Check systemd status
sudo systemctl status nation-radar-api

# View logs
sudo journalctl -u nation-radar-api -f
```

### **Railway Health Check:**
Visit: `https://your-railway-url.railway.app/api/system-status`

Should show:
```json
{
  "success": true,
  "status": "operational",
  "railway_status": "operational",
  "vps_connection": "connected",
  "statistics": { ... }
}
```

## 🚨 **Troubleshooting**

### **VPS API Not Starting:**
1. Check if port 5001 is available: `netstat -tlnp | grep 5001`
2. Check logs: `sudo journalctl -u nation-radar-api -f`
3. Verify database exists: `ls -la tweets.db`

### **Railway Can't Connect to VPS:**
1. Check VPS firewall settings
2. Verify VPS IP is correct in Railway environment
3. Test connectivity: `curl http://VPS_IP:5001/` from Railway

### **Data Not Updating:**
1. Ensure VPS pipeline is running: `python3 run_pipeline.py`
2. Check API server logs
3. Verify database has new data: `sqlite3 tweets.db "SELECT COUNT(*) FROM tweets;"`

## 🎯 **Benefits of This Architecture**

✅ **Real-time updates** - No Git sync delays  
✅ **Professional** - Industry standard API approach  
✅ **Scalable** - Can add more consumers later  
✅ **Reliable** - Direct HTTP communication  
✅ **Monitorable** - Clear connection status  

## 🔮 **Next Steps**

1. **Start VPS API server**
2. **Configure Railway environment variables**
3. **Deploy updated code**
4. **Test the integration**
5. **Monitor data flow**

---

**Your Nation Radar is now a professional, scalable system!** 🚀
