#!/usr/bin/env python3
"""
Quick test for authentication API fix
"""

import requests
import json


def test_auth_endpoint():
    """Test if the auth endpoint is accessible"""
    print("🧪 Testing Authentication Endpoint Fix\n")

    # Test OPTIONS request (CORS preflight)
    try:
        print("1. Testing CORS preflight...")
        response = requests.options(
            "http://localhost:5001/api/auth/login",
            headers={'Origin': 'http://localhost:5173'},
            timeout=5
        )
        print(f"   OPTIONS /api/auth/login: {response.status_code}")

        if response.status_code == 200:
            print("   ✅ CORS preflight successful")
        else:
            print("   ❌ CORS preflight failed")

    except Exception as e:
        print(f"   ❌ CORS test error: {e}")

    # Test actual login endpoint accessibility
    try:
        print("\n2. Testing login endpoint accessibility...")
        response = requests.post(
            "http://localhost:5001/api/auth/login",
            json={"account": "test", "password": "test"},
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        print(f"   POST /api/auth/login: {response.status_code}")

        # Bad credentials, but endpoint works
        if response.status_code in [400, 401]:
            print("   ✅ Login endpoint accessible")
        elif response.status_code == 404:
            print("   ❌ Login endpoint not found (still 404)")
        else:
            print(f"   ℹ️  Unexpected response: {response.status_code}")

    except Exception as e:
        print(f"   ❌ Login test error: {e}")

    print("\n" + "="*50)
    print("📝 Summary:")
    print("If you see 200 for OPTIONS and 400/401 for POST,")
    print("the authentication fix is working correctly!")
    print("You can now try logging in from the frontend.")


if __name__ == "__main__":
    test_auth_endpoint()
