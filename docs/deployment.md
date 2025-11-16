# 🚀 BrandGuard Deployment Guide

This guide provides multiple deployment options for the BrandGuard application, from local Docker deployment to cloud platforms.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Docker Deployment](#local-docker-deployment)
3. [Cloud Deployment Options](#cloud-deployment-options)
4. [Environment Configuration](#environment-configuration)
5. [Monitoring & Maintenance](#monitoring--maintenance)
6. [Troubleshooting](#troubleshooting)

---

## 🛠️ Prerequisites

### Required Software
- **Docker Desktop** (latest version)
- **Git** for version control
- **Node.js 18+** (for local development)
- **Python 3.11+** (for local development)

### System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space
- **Network**: Stable internet connection

---

## 🐳 Local Docker Deployment

### Quick Start (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sathvik-2004/BrandGuard.git
   cd BrandGuard
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Deploy with script**:
   
   **Windows**:
   ```powershell
   .\scripts\deploy.ps1
   ```
   
   **Linux/macOS**:
   ```bash
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh
   ```

### Manual Docker Deployment

1. **Build and start services**:
   ```bash
   docker compose build
   docker compose up -d
   ```

2. **Check service status**:
   ```bash
   docker compose ps
   docker compose logs
   ```

3. **Access application**:
   - **Frontend**: http://localhost
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

### Docker Services

| Service | Port | Purpose |
|---------|------|---------|
| Frontend (Nginx) | 80 | Web interface |
| Backend (FastAPI) | 8000 | API server |
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Caching |

---

## ☁️ Cloud Deployment Options

### 1. Railway (Recommended for Full-Stack)

**Pros**: Easy PostgreSQL setup, automatic HTTPS, great for Python/Node.js
**Cost**: Free tier available, $5/month for hobby plan

#### Steps:
1. **Create Railway account**: https://railway.app
2. **Connect GitHub repository**
3. **Deploy from template**:
   ```bash
   railway login
   railway link
   railway up
   ```
4. **Configure environment variables** in Railway dashboard
5. **Set custom domain** (optional)

### 2. Render.com

**Pros**: Great free tier, easy database management
**Cost**: Free tier with limitations, $7/month for starter plan

#### Steps:
1. **Create Render account**: https://render.com
2. **Import from GitHub**
3. **Use provided configuration**: `deploy/render.yaml`
4. **Configure environment variables**
5. **Deploy services**

### 3. Vercel + Railway (Frontend + Backend Split)

**Pros**: Excellent frontend performance, free tier
**Cost**: Free for frontend, Railway for backend

#### Steps:
1. **Deploy backend to Railway** (follow Railway steps above)
2. **Deploy frontend to Vercel**:
   ```bash
   npm i -g vercel
   cd web
   vercel --prod
   ```
3. **Configure frontend environment variables** with Railway backend URL

### 4. AWS/GCP/Azure (Enterprise)

For enterprise deployments, use the provided `docker-compose.yml` with:
- **AWS**: ECS, RDS, ElastiCache
- **GCP**: Cloud Run, Cloud SQL, Memorystore
- **Azure**: Container Instances, Azure Database, Redis Cache

---

## ⚙️ Environment Configuration

### Required Environment Variables

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# CORS
CORS_ORIGINS=https://yourdomain.com

# Security
SECRET_KEY=your-super-secret-key

# Environment
ENVIRONMENT=production
LOG_LEVEL=INFO
```

#### Frontend
```bash
VITE_API_URL=https://your-backend-url
VITE_WS_URL=wss://your-backend-url
```

### Platform-Specific Configuration

#### Railway
- Set `RAILWAY_STATIC_URL` for frontend
- PostgreSQL automatically configured
- Environment variables in dashboard

#### Render
- Use `render.yaml` configuration
- PostgreSQL connection string auto-injected
- Static site for frontend

#### Vercel
- Configure build settings: `npm run build`
- Output directory: `dist`
- Environment variables in dashboard

---

## 📊 Monitoring & Maintenance

### Health Checks

- **Backend Health**: `GET /health`
- **Database**: Built-in health checks
- **Frontend**: Nginx health endpoints

### Logging

**Docker Logs**:
```bash
docker compose logs -f
docker compose logs backend
docker compose logs frontend
```

**Application Logs**:
- Backend: FastAPI structured logging
- Frontend: Browser console + nginx logs
- Database: PostgreSQL logs

### Monitoring Tools

- **Built-in**: Health check endpoints
- **External**: Uptime Robot, Pingdom
- **APM**: New Relic, DataDog (enterprise)

### Backup Strategy

**Database Backup**:
```bash
# PostgreSQL backup
docker compose exec postgres pg_dump -U brandguard brandguard > backup.sql

# Restore
docker compose exec -T postgres psql -U brandguard brandguard < backup.sql
```

**Volume Backup**:
```bash
docker run --rm -v brandguard_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Conflicts
```bash
# Check ports in use
netstat -tulpn | grep :80
netstat -tulpn | grep :8000

# Change ports in docker-compose.yml
ports:
  - "8080:80"  # Frontend
  - "8001:8000"  # Backend
```

#### 2. Database Connection Issues
```bash
# Check database logs
docker compose logs postgres

# Reset database
docker compose down -v
docker compose up -d
```

#### 3. Memory Issues
```bash
# Check container resources
docker stats

# Increase memory limits in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G
```

#### 4. CORS Issues
- Update `CORS_ORIGINS` in backend environment
- Ensure frontend URL matches CORS configuration
- Check browser network tab for CORS errors

#### 5. WebSocket Connection Issues
- Verify WebSocket URL in frontend
- Check proxy configuration (nginx)
- Ensure backend WebSocket endpoint is accessible

### Performance Optimization

#### 1. Database
- Enable PostgreSQL connection pooling
- Add database indexes for frequent queries
- Monitor query performance

#### 2. Backend
- Increase uvicorn workers: `--workers 4`
- Enable Redis caching
- Optimize NLP model loading

#### 3. Frontend
- Enable gzip compression (nginx)
- Optimize bundle size (Vite)
- Use CDN for static assets

### Recovery Commands

**Full Reset**:
```bash
docker compose down -v --remove-orphans
docker compose build --no-cache
docker compose up -d
```

**Service Restart**:
```bash
docker compose restart backend
docker compose restart frontend
```

**Logs Investigation**:
```bash
docker compose logs --tail=100 backend
docker compose logs --since="1h" frontend
```

---

## 📞 Support

- **Documentation**: Check README.md and architecture.md
- **Issues**: GitHub Issues for bug reports
- **Monitoring**: Built-in health checks and logs
- **Updates**: `git pull` and `docker compose pull`

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Start all services | `docker compose up -d` |
| View logs | `docker compose logs -f` |
| Stop services | `docker compose down` |
| Rebuild | `docker compose build --no-cache` |
| Health check | `curl http://localhost:8000/health` |
| Database backup | `docker compose exec postgres pg_dump...` |

---

**🚀 Happy Deploying!**

Your BrandGuard application is now ready for production deployment with enterprise-grade monitoring, real-time capabilities, and AI-powered analytics!