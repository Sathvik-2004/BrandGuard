# BrandGuard - Quick Setup (No Node.js Required)

Since Node.js is not installed, use the HTML dashboard for immediate testing.

## Quick Start (5 minutes)

### 1. Start Backend (Terminal 1)
```powershell
cd services\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Open Dashboard
- Navigate to: `c:\Users\sathw\OneDrive\Desktop\BrandGuard\web\dashboard.html`
- Double-click to open in your web browser
- Or drag the file into a browser window

### 3. Generate Test Data (Terminal 2)
```powershell
cd services\backend
.\.venv\Scripts\Activate.ps1
python scripts\ingest_mock.py
```

### 4. Test Live Feed (Terminal 3)
```powershell
cd services\backend
.\.venv\Scripts\Activate.ps1
python scripts\send_ws_demo.py
```

## What You'll See

- **Dashboard**: Real-time mention cards with sentiment analysis
- **Live Feed**: WebSocket messages appearing instantly
- **API Data**: Recent mentions from the database

## Next Steps

### Install Node.js (Optional)
If you want the full React app:
1. Download Node.js from https://nodejs.org/
2. Restart VS Code terminal
3. Run:
```powershell
cd web
npm install
npm run dev
```

### Add Real Data Sources
- Edit `services\backend\scripts\ingest_rss.py` for RSS feeds
- Add Twitter API, Reddit API, etc.

### Production Deployment
```powershell
cd infra
docker compose up --build
```

## Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (need 3.11+)
- Install Python from https://python.org if missing

**Dashboard shows errors:**
- Ensure backend is running at http://localhost:8000
- Check browser console for errors (F12)
- Verify /health endpoint: http://localhost:8000/health

**No mentions appear:**
- Run `python scripts\ingest_mock.py` first
- Check API response: http://localhost:8000/api/mentions

The HTML dashboard provides the same features as the React app without requiring Node.js installation!