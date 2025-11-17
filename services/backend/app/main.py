import json
import asyncio
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .ws_manager import ConnectionManager
from .db import SessionLocal, engine
from .models import Base, Mention, Alert

# Disable NLP tasks for production deployment stability
TASKS_ENABLED = False
print("NLP tasks disabled for production deployment stability")

# create tables (dev convenience)
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Database initialization warning: {e}")
    # Continue anyway - tables might already exist

app = FastAPI(title="BrandGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:3000", 
        "http://localhost:5174", 
        "http://localhost",
        "https://*.railway.app",
        "https://*.up.railway.app",
        "https://brand-guard-sooty.vercel.app",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()

# expose manager to tasks module only if tasks are enabled
if TASKS_ENABLED:
    tasks.manager = manager

@app.on_event("startup")
async def startup_event():
    # start background periodic tasks only if enabled
    if TASKS_ENABLED:
        loop = asyncio.get_event_loop()
        # run tasks.run_periodic_tasks in background
        loop.create_task(tasks.run_periodic_tasks(interval_seconds=60))
        print("Background tasks started.")
    else:
        print("Background tasks disabled - running in minimal mode")

@app.get("/")
async def root():
    return {
        "message": "🚀 BrandGuard API - Real-time Brand Monitoring System",
        "version": "1.0.0",
        "status": "active",
        "features": {
            "real_time_monitoring": True,
            "sentiment_analysis": TASKS_ENABLED,
            "topic_clustering": TASKS_ENABLED,
            "spike_detection": TASKS_ENABLED
        },
        "endpoints": {
            "health": "/health",
            "api_docs": "/docs",
            "mentions": "/api/mentions",
            "alerts": "/api/alerts",
            "websocket": "/ws/mentions"
        },
        "repository": "https://github.com/Sathvik-2004/BrandGuard",
        "deployed_on": "Railway"
    }

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": "2025-11-17", "service": "BrandGuard API"}

# Simple REST list mentions
@app.get("/api/mentions")
def list_mentions(limit: int = 50):
    db = SessionLocal()
    try:
        q = db.query(Mention).order_by(Mention.published_at.desc()).limit(limit).all()
        # basic serialization
        out = []
        for m in q:
            out.append({
                "id": m.id,
                "source": m.source,
                "source_id": m.source_id,
                "author": m.author,
                "text": m.text,
                "url": m.url,
                "published_at": m.published_at.isoformat() if m.published_at else None,
                "sentiment": m.sentiment,
                "reach": m.reach,
                "cluster_id": m.cluster_id,
            })
        return out
    finally:
        db.close()

# POST endpoint to create mention (saves and broadcasts)
@app.post("/api/mentions")
async def create_mention(payload: dict):
    """
    payload example:
    {
      "source": "twitter",
      "source_id": "mock-10",
      "author": "user_1",
      "text": "This is a live test mention",
      "url": "https://twitter.com/mock/1",
      "published_at": "2025-11-14T18:30:00",
      "sentiment": "positive",
      "reach": 500
    }
    """
    db = SessionLocal()
    try:
        # Parse published_at if provided as string
        published_at = payload.get("published_at")
        if published_at and isinstance(published_at, str):
            from datetime import datetime
            try:
                published_at = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            except ValueError:
                published_at = None
        
        m = Mention(
            source=payload.get("source", "mock"),
            source_id=payload.get("source_id"),
            author=payload.get("author"),
            text=payload.get("text"),
            url=payload.get("url"),
            published_at=published_at,
            sentiment=payload.get("sentiment"),
            reach=payload.get("reach"),
        )
        db.add(m)
        db.commit()
        db.refresh(m)
        # prepare broadcast message (stringified JSON)
        msg = {
            "type": "mention",
            "mention": {
                "id": m.id,
                "source": m.source,
                "source_id": m.source_id,
                "author": m.author,
                "text": m.text,
                "url": m.url,
                "published_at": m.published_at.isoformat() if m.published_at else None,
                "sentiment": m.sentiment,
                "reach": m.reach,
                "cluster_id": m.cluster_id,
            }
        }
        await manager.broadcast(json.dumps(msg))
        return {"status": "ok", "id": m.id}
    finally:
        db.close()

# REST endpoint to list alerts  
@app.get("/api/alerts")
def list_alerts(limit: int = 50):
    """Get recent alerts"""
    db = SessionLocal()
    try:
        alerts = db.query(Alert).order_by(Alert.created_at.desc()).limit(limit).all()
        result = []
        for alert in alerts:
            result.append({
                "id": alert.id,
                "alert_type": alert.alert_type,
                "message": alert.message,
                "created_at": alert.created_at.isoformat() if alert.created_at else None,
                "resolved": alert.resolved
            })
        return result
    finally:
        db.close()

@app.get("/api/alerts")
def list_alerts(limit: int = 50):
    db = SessionLocal()
    try:
        rows = db.query(Alert).order_by(Alert.created_at.desc()).limit(limit).all()
        return [{"id":r.id, "alert_type":r.alert_type, "message": r.message, "created_at": r.created_at.isoformat(), "resolved": r.resolved} for r in rows]
    finally:
        db.close()

# websocket endpoint for live clients
@app.websocket("/ws/mentions")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # we don't expect clients to send data; but we keep loop to detect disconnects
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)