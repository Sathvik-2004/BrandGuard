# 📘 BrandGuard — Real-time Brand Mention & Reputation Monitoring System

🚀 **LIVE DEMO**: 
- **🌐 Frontend Dashboard**: https://brand-guard-sooty.vercel.app
- **⚡ Backend API**: https://brandguard-production.up.railway.app
- **📚 API Documentation**: https://brandguard-production.up.railway.app/docs

BrandGuard is a full-stack real-time monitoring tool designed to help marketing teams track brand mentions, analyze sentiment, detect trending topics, and get alerts during sudden spikes in brand conversations.

This system includes:
- Real-time WebSockets
- NLP sentiment analysis
- Topic clustering using embeddings
- Spike detection logic
- Alerts system
- Full dashboard UI

---

# 🚀 Features

### ✅ Real-time Brand Mentions
- Live updates via WebSockets
- Recent mentions list
- Source, sentiment, reach, timestamp, URL

### ✅ Sentiment Analysis
- Automatically labels mentions as:
  - `positive`
  - `neutral`
  - `negative`

### ✅ Topic Clustering (NLP)
- Embeddings using SentenceTransformers
- MiniBatchKMeans clustering
- Topic IDs shown in UI

### ✅ Spike Detection + Alerts
Detects:
- Volume spikes (high activity)
- Negative sentiment spikes
- Broadcasts alerts to UI instantly

### ✅ Modern Dashboard UI
- React + Vite + TypeScript
- Dark theme
- Live updates + alert section

---

# 🏗 Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│  Frontend       │    │  Backend        │    │  Database       │
│  React + Vite   │◄──►│  FastAPI        │◄──►│  SQLite         │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │
         │                       │
         └───────────────────────┘
              WebSocket
           (Real-time updates)

┌─────────────────────────────────────────────────────────────────┐
│                    Background Tasks                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Topic Clustering│  │ Spike Detection │  │ Alert System    │ │
│  │ SentenceTransf. │  │ Statistical     │  │ WebSocket       │ │
│  │ MiniBatchKMeans │  │ Analysis        │  │ Broadcasting    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

# 📁 Project Structure

```
BrandGuard/
├── 📁 docs/
│   └── 📄 architecture.md          # Detailed architecture documentation
├── 📁 services/
│   └── 📁 backend/
│       ├── 📁 app/
│       │   ├── 📄 __init__.py       # Package initialization
│       │   ├── 📄 main.py           # FastAPI app with endpoints
│       │   ├── 📄 models.py         # SQLAlchemy models (Mention, Alert)
│       │   ├── 📄 db.py             # Database connection
│       │   ├── 📄 ws_manager.py     # WebSocket connection manager
│       │   ├── 📄 nlp.py            # NLP functions (embeddings, sentiment)
│       │   └── 📄 tasks.py          # Background tasks (clustering, spikes)
│       ├── 📁 scripts/
│       │   └── 📄 post_test_mention.py  # Test script for mentions
│       ├── 📄 requirements.txt      # Python dependencies
│       ├── 📄 dev.db               # SQLite database
│       ├── 📄 fix_db.py            # Database schema migration script
│       └── 📄 Dockerfile           # Container setup
├── 📁 web/
│   ├── 📁 src/
│   │   ├── 📄 App.tsx              # Main React component with real-time alerts
│   │   ├── 📄 index.css            # Styles including alert UI components
│   │   └── 📄 main.tsx             # Entry point
│   ├── 📄 package.json             # Node.js dependencies
│   ├── 📄 vite.config.ts           # Vite configuration
│   ├── 📄 index.html               # HTML template
│   └── 📄 dashboard.html           # Static dashboard template
├── 📁 infra/
│   └── 📄 docker-compose.yml       # Multi-container setup
├── 📄 README.md                    # This comprehensive documentation
├── 📄 QUICKSTART.md                # Quick setup guide
└── 📄 .gitignore                   # Git ignore rules
```

---

# 🛠 Quick Start

## Prerequisites
- Node.js 18+
- Python 3.11+
- Git

## 1. Clone Repository
```bash
git clone <repository-url>
cd BrandGuard
```

## 2. Backend Setup
```bash
cd services/backend

# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 3. Frontend Setup
```bash
cd web

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

## 4. Access Application
- **Frontend Dashboard**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

# 📊 API Endpoints

## Mentions
- `GET /api/mentions` - List all mentions
- `POST /api/mentions` - Create new mention

## Alerts
- `GET /api/alerts` - List all alerts

## WebSocket
- `WS /ws/mentions` - Real-time updates

## Health Check
- `GET /health` - Server status

---

# 🧪 Testing

## Create Test Mentions
```bash
cd services/backend
python scripts/post_test_mention.py
```

## Test Real-time Updates
```bash
# Create mention via API
curl -X POST "http://localhost:8000/api/mentions" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "twitter",
    "source_id": "test-123",
    "author": "test_user",
    "text": "Amazing product! Love it!",
    "sentiment": "positive",
    "reach": 1000
  }'
```

---

# 🎯 Features in Detail

## Real-time Monitoring
- **WebSocket Connections**: Instant updates without page refresh
- **Live Feed**: Shows recent mentions in real-time
- **Connection Status**: Visual indicator of WebSocket connection

## NLP & AI Features
- **Sentiment Analysis**: Automatic positive/negative/neutral classification
- **Topic Clustering**: Groups similar mentions using AI embeddings
- **Text Processing**: Uses SentenceTransformers for semantic understanding

## Spike Detection
- **Volume Spikes**: Detects unusual increases in mention volume
- **Sentiment Spikes**: Alerts when negative sentiment increases rapidly
- **Statistical Analysis**: Uses mean + 3σ threshold for spike detection

## Alert System
- **Real-time Alerts**: Instant notifications via WebSocket
- **Alert Types**: Volume spikes, negative sentiment spikes
- **Visual Alerts**: Color-coded alerts in dashboard UI

---

# 🔧 Configuration

## Backend Configuration
Edit `services/backend/app/tasks.py`:
```python
# Clustering settings
CLUSTER_WINDOW_MINUTES = 60    # Time window for clustering
CLUSTERS = 6                   # Number of topic clusters

# Spike detection settings
SPIKE_WINDOW_MINUTES = 30      # Lookback window
SPIKE_THRESHOLD_K = 3.0        # Sensitivity (higher = fewer alerts)
```

## Frontend Configuration
Edit `web/vite.config.ts` for proxy settings:
```typescript
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

---

# 🐳 Docker Deployment

## Start with Docker Compose
```bash
docker-compose up -d
```

This starts:
- Backend API on port 8000
- Frontend on port 5173
- Shared volume for database

---

# 🚀 Production Deployment

## Environment Variables
```bash
# Backend
DATABASE_URL=postgresql://user:pass@host:5432/brandguard
CORS_ORIGINS=https://yourdomain.com

# Frontend
VITE_API_BASE=https://api.yourdomain.com
```

## Build for Production
```bash
# Frontend build
cd web
npm run build

# Backend with production ASGI server
cd services/backend
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

# 📈 Monitoring & Observability

## Health Checks
- Backend: `GET /health`
- Database connection status
- WebSocket connection count

## Metrics
- Mention ingestion rate
- Alert frequency
- Topic cluster distribution
- Sentiment analysis accuracy

---

# 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

# 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# 🙋‍♂️ Support

For questions and support:
- 📧 Email: support@brandguard.com
- 📖 Documentation: [docs.brandguard.com](https://docs.brandguard.com)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/brandguard/issues)

---

# 🎉 Acknowledgments

- **FastAPI** for the excellent async web framework
- **React + Vite** for the modern frontend stack
- **SentenceTransformers** for NLP embeddings
- **scikit-learn** for machine learning algorithms
- **SQLAlchemy** for database ORM

---

**Built with ❤️ for marketing teams who need real-time brand insights.**