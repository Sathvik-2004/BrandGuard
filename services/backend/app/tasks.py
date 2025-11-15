# services/backend/app/tasks.py
import asyncio
import time
from datetime import datetime, timedelta
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Mention, Alert
from app.nlp import embed_texts
from app.ws_manager import ConnectionManager

# parameters (tweak as needed)
CLUSTER_WINDOW_MINUTES = 60   # cluster mentions from last 60 minutes
CLUSTERS = 6                  # number of clusters/topics
SPIKE_WINDOW_MINUTES = 30     # lookback window for spike detection
SPIKE_THRESHOLD_K = 3.0       # trigger if current count > mean + K*std

# This manager is imported from main (we will set it in main)
manager: ConnectionManager = None

async def run_periodic_tasks(interval_seconds: int = 60):
    """Main background loop: cluster and detect spikes every `interval_seconds`."""
    while True:
        try:
            await cluster_recent_mentions()
            await detect_spikes_and_create_alerts()
        except Exception as e:
            print("Task loop error:", e)
        await asyncio.sleep(interval_seconds)

async def cluster_recent_mentions():
    db: Session = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(minutes=CLUSTER_WINDOW_MINUTES)
        rows = db.query(Mention).filter(Mention.published_at >= cutoff).all()
        if not rows:
            return
        texts = [r.text or "" for r in rows]
        embeddings = embed_texts(texts)  # numpy array
        # clustering
        k = min(len(rows), CLUSTERS)
        if k <= 1:
            # assign all to cluster 0
            for r in rows:
                r.cluster_id = 0
            db.commit()
            return
        model = MiniBatchKMeans(n_clusters=k, random_state=42, batch_size=32)
        labels = model.fit_predict(embeddings)
        # write labels back
        for r, lab in zip(rows, labels):
            r.cluster_id = int(lab)
        db.commit()
        # optional: broadcast cluster info for UI (we'll skip heavy payloads)
        print(f"[{datetime.utcnow().isoformat()}] clustered {len(rows)} mentions into {k} topics.")
    finally:
        db.close()

async def detect_spikes_and_create_alerts():
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=SPIKE_WINDOW_MINUTES)
        # fetch counts per minute in window
        mentions = db.query(Mention).filter(Mention.published_at >= window_start).all()
        if not mentions:
            return
        # bucket counts by minute
        buckets = {}
        for m in mentions:
            minute = m.published_at.replace(second=0, microsecond=0)
            buckets.setdefault(minute, []).append(m)
        # sort minutes
        minutes_sorted = sorted(buckets.keys())
        counts = np.array([len(buckets[m]) for m in minutes_sorted])
        if len(counts) < 2:
            return
        mean = float(np.mean(counts))
        std = float(np.std(counts))
        current_count = counts[-1]
        # volume spike detection
        if current_count > mean + SPIKE_THRESHOLD_K * std:
            msg = f"Volume spike detected: {current_count} mentions in last minute (mean={mean:.1f}, std={std:.1f})"
            create_alert(db, "volume_spike", msg)
        # negative sentiment spike detection: compute fraction negative in last minute vs baseline
        last_minute = minutes_sorted[-1]
        last_mentions = buckets[last_minute]
        neg_count = sum(1 for m in last_mentions if (m.sentiment or "").lower() == "negative")
        frac_neg = neg_count / max(1, len(last_mentions))
        # baseline fraction: compute excluding last minute
        baseline_counts = []
        baseline_neg = []
        for mtime in minutes_sorted[:-1]:
            ms = buckets[mtime]
            baseline_counts.append(len(ms))
            baseline_neg.append(sum(1 for mm in ms if (mm.sentiment or "").lower() == "negative"))
        if baseline_counts:
            base_frac = (sum(baseline_neg) / sum(baseline_counts)) if sum(baseline_counts) > 0 else 0.0
            # trigger if fraction increased by > 3x and at least 3 negatives
            if frac_neg > max(0.05, 3 * base_frac) and neg_count >= 3:
                msg = f"Negative sentiment spike: {neg_count}/{len(last_mentions)} negative mentions in last minute (baseline {base_frac:.2f})"
                create_alert(db, "negative_spike", msg)
    finally:
        db.close()

def create_alert(db: Session, alert_type: str, message: str):
    # add entry to DB and broadcast via WS
    a = Alert(alert_type=alert_type, message=message)
    db.add(a)
    db.commit()
    db.refresh(a)
    # broadcast to WS clients (if manager set)
    payload = {"type": "alert", "alert": {"id": a.id, "alert_type": a.alert_type, "message": a.message, "created_at": a.created_at.isoformat()}}
    try:
        if manager:
            # ensure async broadcast; manager.broadcast is async
            asyncio.create_task(manager.broadcast(__import__("json").dumps(payload)))
        else:
            print("Alert created (no WS manager):", payload)
    except Exception as e:
        print("Broadcast error:", e)
    print("Created alert:", message)