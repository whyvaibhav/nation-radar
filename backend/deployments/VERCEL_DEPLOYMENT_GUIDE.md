# 🚀 Vercel Deployment Guide - Crestal Monitor

## 🎯 Why Vercel?

✅ **Perfect for Your Project:**
- Python/Flask serverless functions
- Global CDN for fast loading
- Auto-scaling and zero maintenance
- Free tier with generous limits
- GitHub integration for auto-deploys

## 📋 Prerequisites

1. **GitHub Account** - For code hosting
2. **Vercel Account** - Sign up at vercel.com (free)
3. **Your Project** - Push to GitHub repository

## 🚀 Quick Deployment (5 minutes)

### **Step 1: Prepare Your Repository**

```bash
# 1. Copy Vercel files to your project root
cp Install/vercel.json ./
cp Install/requirements_vercel.txt ./requirements.txt
cp Install/app_vercel.py ./app.py

# 2. Commit to GitHub
git add .
git commit -m "Add Vercel deployment config"
git push origin main
```

### **Step 2: Deploy to Vercel**

1. **Visit**: https://vercel.com/new
2. **Import**: Select your GitHub repository
3. **Configure**: 
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `frontend`

### **Step 3: Add Environment Variables**

In Vercel dashboard → Settings → Environment Variables:

```
RAPIDAPI_KEY = your_rapidapi_key_here
NATION_AGENT_API_KEY = your_nation_agent_key_here
DEBUG_MODE = False
```

### **Step 4: Deploy & Access**

✅ **Your site is live!** 
- URL: `https://your-project.vercel.app`
- API: `https://your-project.vercel.app/api/crestal-data`

---

## 🔄 Data Integration Options

### **Option A: Static Demo (Current Setup)**
- **Pro**: Works immediately, no backend needed
- **Con**: Shows mock data only
- **Use Case**: Portfolio, demo, proof of concept

### **Option B: Webhook Integration**
```python
# VPS sends data to Vercel via webhook
import requests

def send_to_vercel(tweets_data):
    webhook_url = "https://your-project.vercel.app/api/webhook"
    requests.post(webhook_url, json=tweets_data)
```

### **Option C: External Database**
```python
# Connect to external database (Supabase, MongoDB)
from supabase import create_client

supabase = create_client(url, key)
data = supabase.table('crestal_tweets').select('*').execute()
```

### **Option D: GitHub Pages Data**
```bash
# VPS commits data to GitHub, Vercel auto-deploys
git add groktweets.csv
git commit -m "Update tweet data"
git push origin main  # Triggers Vercel rebuild
```

---

## 🌐 Production Architecture

### **Recommended Setup:**

```
VPS (Data Collection) → GitHub (Data Storage) → Vercel (Frontend)
```

**How it works:**
1. **VPS**: Runs your pipeline, collects tweets
2. **GitHub**: Stores data files (CSV/JSON)
3. **Vercel**: Serves frontend with latest data

### **Implementation:**

**1. VPS Automation Script:**
```bash
#!/bin/bash
# vps_to_github.sh - Run after each pipeline

cd /opt/crestal-monitor

# Convert CSV to JSON for web consumption
python3 -c "
import pandas as pd
import json

df = pd.read_csv('groktweets.csv', header=None)
df.columns = ['id', 'username', 'text', 'score', 'profile_url']
data = df.to_dict('records')

with open('data/crestal_tweets.json', 'w') as f:
    json.dump(data, f, indent=2)
"

# Commit to GitHub
git add data/crestal_tweets.json
git commit -m "Update Crestal data - $(date)"
git push origin main

echo "✅ Data pushed to GitHub - Vercel will auto-deploy"
```

**2. Vercel App Reads GitHub Data:**
```python
# In app_vercel.py
import requests

def get_latest_data():
    # Read from your GitHub repository
    url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/data/crestal_tweets.json"
    response = requests.get(url)
    return response.json()
```

---

## 🎨 Custom Domain Setup

### **Free Custom Domain:**
1. **Buy domain** (Namecheap, GoDaddy: ~$10/year)
2. **In Vercel**: Settings → Domains → Add Domain
3. **DNS Setup**: Point your domain to Vercel
4. **SSL**: Automatic HTTPS certificate

**Result**: `https://crestal-monitor.yourname.com`

---

## 📊 Vercel Features You Get

### **Performance:**
- **Global CDN** - Fast loading worldwide
- **Edge Functions** - API responses in <50ms
- **Automatic Scaling** - Handles traffic spikes
- **Optimized Images** - Automatic compression

### **Developer Experience:**
- **Git Integration** - Auto-deploy on push
- **Preview Deployments** - Test before going live
- **Analytics** - Built-in traffic insights
- **Zero Config** - Works out of the box

### **Monitoring:**
- **Function Logs** - Debug API issues
- **Performance Metrics** - Response times
- **Error Tracking** - Automatic alerts
- **Usage Analytics** - Traffic patterns

---

## 💰 Cost Breakdown

### **Free Tier (Perfect for you):**
- **100GB Bandwidth** - ~100K page views/month
- **100 Function Executions/day** - API calls
- **6h Build Time** - Deployment time
- **Custom Domains** - Unlimited

### **Paid Plans** (if you scale):
- **Pro**: $20/month - More bandwidth & functions
- **Team**: $40/month - Collaboration features

---

## 🔧 Advanced Configuration

### **Custom Build Process:**
```json
{
  "buildCommand": "pip install -r requirements.txt && python build.py",
  "outputDirectory": "dist",
  "installCommand": "pip install -r requirements.txt"
}
```

### **Environment-Specific Config:**
```json
{
  "env": {
    "NODE_ENV": "production",
    "API_URL": "https://your-api.vercel.app"
  },
  "preview": {
    "API_URL": "https://preview-api.vercel.app"
  }
}
```

### **Multiple Environments:**
- **Production**: `main` branch → `yourproject.vercel.app`
- **Staging**: `develop` branch → `develop-yourproject.vercel.app`
- **Preview**: Any PR → Unique preview URL

---

## 🎯 Quick Start Commands

```bash
# 1. Prepare for Vercel
cp Install/vercel.json ./
cp Install/app_vercel.py ./app.py

# 2. Install Vercel CLI (optional)
npm i -g vercel

# 3. Deploy from command line
vercel

# 4. Set environment variables
vercel env add RAPIDAPI_KEY
vercel env add NATION_AGENT_API_KEY
```

---

## 🏆 Your Live Crestal Leaderboard

**What you'll have:**
- ✅ **Global Access**: `https://yourproject.vercel.app`
- ✅ **Fast Loading**: <100ms response times
- ✅ **Auto-Deploy**: Push to GitHub = instant updates
- ✅ **Professional URL**: Custom domain support
- ✅ **Mobile Optimized**: Works on all devices
- ✅ **Analytics**: Built-in traffic monitoring

**Perfect for:**
- Showcasing Crestal community
- Sharing with $NATION holders
- Demo for potential projects
- Portfolio piece

---

🚀 **Ready to deploy? Follow Step 1-4 above and your Crestal monitor will be live in 5 minutes!**
