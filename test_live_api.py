import requests
import time
import json

# Your live API endpoint
API_URL = "https://brandguard-production.up.railway.app"

def create_test_mention(source, text, sentiment="positive", reach=100):
    """Create a test mention via API"""
    data = {
        "source": source,
        "source_id": f"test-{int(time.time())}",
        "author": f"test_user_{int(time.time()) % 1000}",
        "text": text,
        "url": f"https://{source}.com/test",
        "sentiment": sentiment,
        "reach": reach
    }
    
    try:
        response = requests.post(f"{API_URL}/api/mentions", json=data)
        if response.status_code == 200:
            print(f"✅ Created mention: {text[:50]}...")
            return response.json()
        else:
            print(f"❌ Failed to create mention: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_api_health():
    """Test if API is working"""
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print(f"✅ API Health: {response.json()}")
            return True
        else:
            print(f"❌ API Health Check Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Connection Error: {e}")
        return False

def populate_test_data():
    """Add sample mentions to test the dashboard"""
    print("🚀 Testing BrandGuard API...")
    
    # Check API health first
    if not test_api_health():
        print("❌ API is not responding. Check Railway deployment.")
        return
    
    print("\n📝 Creating test mentions...")
    
    # Sample mentions to test the system
    test_mentions = [
        ("twitter", "Amazing experience with BrandGuard! Real-time monitoring is fantastic.", "positive", 250),
        ("reddit", "BrandGuard helped us track our brand mentions efficiently", "positive", 180),
        ("facebook", "The sentiment analysis feature in BrandGuard is very accurate", "positive", 320),
        ("linkedin", "BrandGuard dashboard shows great insights for our marketing team", "positive", 150),
        ("instagram", "Love how BrandGuard detects spikes in brand conversations", "positive", 400),
        ("twitter", "BrandGuard's real-time alerts are super helpful for our PR team", "positive", 275),
        ("reddit", "The topic clustering in BrandGuard makes it easy to understand trends", "positive", 190)
    ]
    
    for source, text, sentiment, reach in test_mentions:
        create_test_mention(source, text, sentiment, reach)
        time.sleep(1)  # Small delay to see real-time updates
    
    print("\n🎉 Test data created! Check your dashboard at:")
    print("https://brand-guard-sooty.vercel.app")
    print("\n📊 You should now see mentions appearing in real-time!")

if __name__ == "__main__":
    populate_test_data()