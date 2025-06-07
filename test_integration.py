#!/usr/bin/env python3
"""
Integration test script for Warehouse Management System
Tests the connection between frontend and backend APIs
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:5001/api"
FRONTEND_URL = "http://localhost:5173"


def test_backend_health():
    """Test if backend is running and healthy"""
    try:
        response = requests.get("http://localhost:5001/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not reachable: {e}")
        return False


def test_cors_headers():
    """Test CORS configuration"""
    try:
        response = requests.options("http://localhost:5001/api/health",
                                    headers={'Origin': FRONTEND_URL})
        cors_headers = response.headers.get('Access-Control-Allow-Origin')
        if cors_headers:
            print("✅ CORS headers configured")
            return True
        else:
            print("❌ CORS headers missing")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ CORS test failed: {e}")
        return False


def test_api_endpoints():
    """Test key API endpoints"""
    endpoints = [
        ("/products", "Products API"),
        ("/suppliers", "Suppliers API"),
        ("/customers", "Customers API"),
        ("/orders", "Orders API"),
        ("/inventory", "Inventory API"),
        ("/locations", "Locations API"),
        ("/shipments", "Shipments API"),
        ("/scrap", "Scrap API"),
        ("/users", "Users API"),
        ("/users/roles", "Roles API")
    ]

    results = []
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            # 401 is expected for protected endpoints
            if response.status_code in [200, 401]:
                print(f"✅ {name} endpoint accessible")
                results.append(True)
            else:
                print(f"❌ {name} endpoint failed: {response.status_code}")
                results.append(False)
        except requests.exceptions.RequestException as e:
            print(f"❌ {name} endpoint error: {e}")
            results.append(False)

    return all(results)


def test_database_connection():
    """Test database initialization"""
    try:
        response = requests.get(
            "http://localhost:5001/api/init-db", timeout=10)
        if response.status_code == 200:
            print("✅ Database connection successful")
            return True
        else:
            print(f"❌ Database connection failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Database test failed: {e}")
        return False


def main():
    """Run all integration tests"""
    print("🧪 Running Warehouse Management System Integration Tests\n")

    tests = [
        ("Backend Health", test_backend_health),
        ("CORS Configuration", test_cors_headers),
        ("API Endpoints", test_api_endpoints),
        ("Database Connection", test_database_connection)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        result = test_func()
        results.append(result)

    print("\n" + "="*50)
    print("📊 Integration Test Results:")
    print("="*50)

    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{test_name}: {status}")

    overall_success = all(results)
    print(
        f"\nOverall Status: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")

    if overall_success:
        print("\n🎉 Frontend-Backend integration is ready!")
        print("You can now start both servers:")
        print("  Backend: cd backend && python app.py")
        print("  Frontend: cd frontend && npm run dev")
    else:
        print("\n🔧 Please fix the failing tests before proceeding.")

    return 0 if overall_success else 1


if __name__ == "__main__":
    sys.exit(main())
