# Nation Radar Intelligence Hub - Integrated Edition

A unified AI-powered social media monitoring system that combines backend data processing with a modern web frontend.

## 🏗️ **Project Structure**

```
nation-radar-integrated/
├── backend/                 # VPS Backend Pipeline
│   ├── fetchers/           # Twitter data fetchers
│   ├── storage/            # Data storage modules
│   ├── run_pipeline.py     # Main data collection script
│   ├── nation_agent.py     # AI scoring via IntentKit
│   ├── tweets.db           # SQLite database
│   └── tweets.csv          # CSV export
├── frontend/               # Railway Web Interface
│   ├── index.html          # Main dashboard
│   ├── styles.css          # Styling
│   └── script.js           # Frontend logic
├── shared/                 # Common utilities
├── app.py                  # Unified Flask application
└── requirements.txt        # Dependencies
```

## 🚀 **How It Works**

### **Backend (VPS)**
- **Continuous data collection** via `run_pipeline.py`
- **Twitter API integration** using RapidAPI
- **AI scoring** via Crestal's Nation Agent (IntentKit)
- **Data storage** in SQLite + CSV formats
- **Deduplication** and content filtering

### **Frontend (Railway)**
- **Modern web dashboard** for data visualization
- **Real-time data display** from backend database
- **Search and filtering** capabilities
- **Responsive design** for all devices

### **Integration**
- **Unified Flask app** serves both frontend and API
- **Database connectivity** between VPS and Railway
- **Real-time updates** as new data is processed

## 🔧 **Setup Instructions**

### **1. VPS Backend Setup**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt

# Set up environment variables
nano .env
# Add: RAPIDAPI_KEY=your_key_here

# Test the pipeline
python3 run_pipeline.py

# Set up continuous running (cron job)
crontab -e
# Add: 0 */2 * * * cd /path/to/backend && /path/to/venv/bin/python3 run_pipeline.py
```

### **2. Railway Frontend Deployment**
```bash
# Deploy to Railway
railway login
railway init
railway up

# Set environment variables in Railway dashboard
# PORT=5000
# DEBUG=0
```

### **3. Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the unified app
python3 app.py

# Access at http://localhost:5000
```

## 📊 **API Endpoints**

- **`/`** - Main dashboard
- **`/api/crestal-data`** - Latest Crestal-related tweets
- **`/api/leaderboard`** - Top tweets by score
- **`/api/system-status`** - System statistics
- **`/api/search?q=keyword`** - Search tweets

## 🔄 **Data Flow**

1. **VPS runs pipeline** every 2 hours
2. **Fetches tweets** about Crestal/$NATION
3. **Sends to Nation Agent** for AI scoring (0.0-2.0)
4. **Stores results** in SQLite database
5. **Railway frontend** displays real-time data
6. **Users interact** with beautiful dashboard

## 🎯 **Features**

- **Real-time monitoring** of social media mentions
- **AI-powered content scoring** via IntentKit
- **Beautiful web interface** for data visualization
- **Search and filtering** capabilities
- **Engagement metrics** (likes, retweets, views)
- **Responsive design** for all devices

## 🔑 **Environment Variables**

```env
RAPIDAPI_KEY=your_rapidapi_key
NATION_AGENT_API_KEY=your_intentkit_key
PORT=5000
DEBUG=0
```

## 📈 **Monitoring & Maintenance**

### **VPS Health Check**
```bash
# Check pipeline status
python3 run_pipeline.py

# Monitor database
sqlite3 tweets.db "SELECT COUNT(*) FROM tweets;"

# Check logs
tail -f logs/pipeline.log
```

### **Railway Health Check**
- **Dashboard status** in Railway console
- **API endpoint testing** at `/api/system-status`
- **Frontend accessibility** at root URL

## 🚨 **Troubleshooting**

### **Common Issues**
1. **Database connection errors** - Check file paths
2. **API quota exceeded** - Upgrade RapidAPI plan
3. **Frontend not loading** - Verify static file paths
4. **Pipeline failures** - Check API keys and network

### **Debug Mode**
```bash
# Enable debug logging
export DEBUG=1
python3 app.py
```

## 🔮 **Future Enhancements**

- **Real-time notifications** for high-scoring content
- **Advanced analytics** and trend detection
- **Multi-platform support** (Instagram, LinkedIn)
- **Custom scoring algorithms**
- **API rate limiting** and optimization

## 📞 **Support**

For issues or questions:
1. **Check logs** in VPS and Railway
2. **Verify API keys** and quotas
3. **Test endpoints** individually
4. **Review database** connectivity

---

**Built with ❤️ for the Crestal Network community**
