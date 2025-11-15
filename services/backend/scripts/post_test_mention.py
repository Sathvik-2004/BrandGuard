#!/usr/bin/env python3
"""Test script to post a new mention and verify real-time broadcasting."""

import requests
import json
import sys
from datetime import datetime

API_BASE = "http://localhost:8000"

def post_test_mention():
    """Create a new mention via POST API and test real-time broadcasting."""
    
    # Test mention data
    test_mention = {
        "source": "test_script",
        "source_id": f"test_{int(datetime.now().timestamp())}",
        "author": "test_user",
        "text": f"This is a test mention created at {datetime.now().strftime('%H:%M:%S')}",
        "url": "https://example.com/test",
        "published_at": datetime.now().isoformat(),
        "sentiment": "positive",
        "reach": 100
    }
    
    try:
        print(f"Posting test mention to {API_BASE}/api/mentions")
        print(f"Data: {json.dumps(test_mention, indent=2)}")
        
        response = requests.post(
            f"{API_BASE}/api/mentions",
            json=test_mention,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Success!")
            print(f"Created mention ID: {result['id']}")
            print(f"Text: {result['text']}")
            print(f"Sentiment: {result['sentiment']}")
            print("\n🔴 Check your frontend at http://localhost:5173")
            print("The new mention should appear instantly in the Live Feed!")
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the backend is running:")
        print("cd services/backend && uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    post_test_mention()