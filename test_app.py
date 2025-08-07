#!/usr/bin/env python3
"""
Test script for the Animal Chat Application
"""

import requests
import time
import json

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_query_endpoint(query, expected_intent=None):
    """Test a query endpoint"""
    try:
        response = requests.post(
            'http://localhost:5000/query',
            json={'query': query},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Query '{query}' -> Intent: {data.get('intent', 'Unknown')}")
            print(f"   Message: {data.get('message', 'No message')}")
            print(f"   Animals found: {len(data.get('animals', []))}")
            
            if expected_intent and data.get('intent') != expected_intent:
                print(f"⚠️  Expected intent '{expected_intent}', got '{data.get('intent')}'")
            
            return True
        else:
            print(f"❌ Query '{query}' failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Query '{query}' error: {e}")
        return False

def main():
    """Run all tests"""
    print("🐾 Testing Animal Chat Application")
    print("=" * 50)
    
    # Wait a moment for the server to start
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Test health endpoint
    if not test_health_endpoint():
        print("❌ Health check failed. Is the server running?")
        return False
    
    print()
    
    # Test various queries
    test_cases = [
        ("Which animals are wild?", "Wild Animals"),
        ("Which animal is easiest to train?", "Most Trainable Animals"),
        ("Which animals are most endangered?", "Most Endangered Animals"),
        ("Show me all animals", "All Animals"),
        ("Which animals are tame?", "Tame/Domestic Animals"),
        ("Random query", "General Search"),
    ]
    
    success_count = 0
    for query, expected_intent in test_cases:
        if test_query_endpoint(query, expected_intent):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"🎯 Test Results: {success_count}/{len(test_cases)} tests passed")
    
    if success_count == len(test_cases):
        print("✅ All tests passed! 🎉")
        return True
    else:
        print("❌ Some tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
