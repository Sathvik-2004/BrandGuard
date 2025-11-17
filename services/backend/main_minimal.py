from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

# Simple FastAPI app for Railway
app = FastAPI(title="BrandGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🚀 BrandGuard API - Real-time Brand Monitoring System",
        "version": "1.0.0",
        "status": "active",
        "mode": "minimal"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": "2024-01-15T10:00:00Z",
        "mode": "minimal"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)