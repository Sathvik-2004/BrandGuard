# BrandGuard Architecture

## System Overview

BrandGuard is a real-time brand monitoring platform with advanced NLP capabilities for sentiment analysis, topic clustering, and intelligent alerting.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                             │
│              React + Vite + TypeScript                     │
│       WebSocket (Live Feed) + REST APIs                    │
└─────────────────┬───────────────────────────────────────────┘
                  │ WebSocket + REST
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                          │
│            /api/mentions  /api/alerts                      │
│         /ws/mentions (WebSocket hub)                       │
└─────────────┬───────────────────────┬─────────────────────┘
              │ SQLAlchemy ORM        │ Background Jobs
              ▼                       ▼
┌─────────────────────────┐  ┌─────────────────────────────┐
│        Database         │  │      Background Tasks      │
│    SQLite / Postgres    │  │ SentenceTransformers embed │
│   Mentions  Alerts      │  │   Topic clustering (KMeans) │
│                         │  │   Spike detection & Alerts  │
└─────────────────────────┘  └─────────────────────────────┘
```

## Component Details

### Frontend (React + TypeScript)
- **Real-time Dashboard**: Live feed of brand mentions via WebSocket
- **Alert System**: Visual notifications for spikes and sentiment changes
- **Topic Visualization**: Cluster-based organization of mentions
- **Interactive UI**: Filtering, sorting, and detailed view of mentions

### Backend (FastAPI)
- **REST API Endpoints**:
  - `GET /api/mentions` - Fetch recent mentions
  - `POST /api/mentions` - Create new mentions
  - `GET /api/alerts` - Fetch active alerts
- **WebSocket Hub**: Real-time broadcasting of mentions and alerts
- **Background Processing**: Async tasks for NLP and analytics

### Database Layer
- **Mentions Table**: Core data storage with sentiment and clustering fields
- **Alerts Table**: Spike detection and notification management
- **SQLAlchemy ORM**: Type-safe database interactions

### Background Tasks & NLP
- **SentenceTransformers**: Text embeddings for semantic analysis
- **Topic Clustering**: MiniBatchKMeans for grouping related mentions
- **Spike Detection**: Statistical analysis for volume and sentiment anomalies
- **Real-time Alerts**: Automated notification system

## Data Flow

1. **Mention Ingestion**: New mentions arrive via REST API
2. **Real-time Broadcast**: WebSocket immediately pushes to connected clients
3. **NLP Processing**: Background tasks analyze sentiment and generate embeddings
4. **Topic Clustering**: Recent mentions grouped by semantic similarity
5. **Spike Detection**: Statistical analysis triggers alerts for anomalies
6. **Alert Broadcasting**: Critical alerts pushed to frontend in real-time

## Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Axios, WebSocket API
- **Backend**: FastAPI, Python 3.11, SQLAlchemy, asyncio
- **NLP**: SentenceTransformers, Transformers (Hugging Face), scikit-learn
- **Database**: SQLite (development), PostgreSQL (production)
- **Real-time**: WebSocket connections with connection management
- **Background**: Async task scheduling with periodic execution