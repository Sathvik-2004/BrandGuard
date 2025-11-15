from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Mention(Base):
    __tablename__ = "mentions"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    source_id = Column(String, unique=True, index=True)
    author = Column(String)
    text = Column(Text)
    url = Column(String)
    published_at = Column(DateTime, default=datetime.datetime.utcnow)
    sentiment = Column(String, nullable=True)
    reach = Column(Float, nullable=True)
    cluster_id = Column(Integer, nullable=True)   # new field

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    alert_type = Column(String)     # e.g. "volume_spike" or "negative_spike"
    message = Column(Text)
    resolved = Column(Boolean, default=False)