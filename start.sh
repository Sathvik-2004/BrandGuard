#!/bin/bash
cd services/backend
export PYTHONPATH="/app/services/backend:$PYTHONPATH"

# Create database tables if they don't exist
python -c "from app.db import engine; from app.models import Base; Base.metadata.create_all(bind=engine); print('Database initialized')"

# Start the FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1