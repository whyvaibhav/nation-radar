# 🚀 Railway Frontend Deployment Checklist

## ✅ Architecture Overview

### **Backend**: VPS (143.198.226.161:5000)
- ✅ Flask API running on VPS
- ✅ Database and pipeline on VPS
- ✅ Environment variables configured on VPS
- ✅ API endpoints accessible

### **Frontend**: Railway (Static Hosting)
- ✅ Next.js static export
- ✅ Serves React dashboard
- ✅ Calls VPS backend API

## ✅ Pre-Deployment Checks

### 1. VPS Backend (Already Running)
- [x] Flask API running on `143.198.226.161:5000`
- [x] Environment variables set on VPS
- [x] Database and pipeline working
- [x] API endpoints responding

### 2. Frontend Configuration
- [x] `frontend/env.local` updated to use VPS IP
- [x] `NEXT_PUBLIC_API_URL=http://143.198.226.161:5000`

### 3. Railway Configuration
- [x] `railway.json` configured for frontend-only deployment
- [x] Static export build command
- [x] No environment variables needed

### 4. Dependencies
- [x] `frontend/package.json` has all required dependencies
- [x] Next.js configured for static export

## 🚀 Deployment Steps

### 1. Railway Frontend Setup
1. Connect your GitHub repository to Railway
2. Deploy the project (no environment variables needed)
3. Railway will build and serve the frontend

### 2. Post-Deployment Verification
- [ ] Frontend loads at Railway URL
- [ ] Frontend connects to VPS backend at `143.198.226.161:5000`
- [ ] Dashboard displays real data from VPS
- [ ] API calls work correctly

## 🔧 Troubleshooting

### Common Issues:
1. **CORS Issues**: Ensure VPS backend has CORS enabled for Railway domain
2. **API Connection**: Check if VPS API is accessible from Railway
3. **Build Issues**: Check Next.js build logs in Railway

### Debug Endpoints:
- VPS Backend: `http://143.198.226.161:5000/api/crestal-data`
- VPS Health: `http://143.198.226.161:5000/health`
- Railway Frontend: `https://nation-radar.up.railway.app`

## 📊 Expected Results

After successful deployment:
- ✅ Dashboard shows real Crestal Network data from VPS
- ✅ Agent scoring working (VPS backend)
- ✅ Auto-refresh every 30 seconds
- ✅ Leaderboard with real user rankings
- ✅ System stats displaying correctly

## 🔐 Security Notes

- ✅ API keys stored on VPS (not in Railway)
- ✅ No sensitive data in git repository
- ✅ Frontend only serves static files
- ✅ Backend API protected on VPS
