#!/usr/bin/env python3
"""
Test script for the Warehouse Management System API
"""

import requests
import json

BASE_URL = "http://localhost:5001/api"


def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)


def test_init_db():
    """Test database initialization"""
    print("Testing database initialization...")
    response = requests.get(f"{BASE_URL}/init-db")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)


def test_login():
    """Test login endpoint"""
    print("Testing login...")

    # Test with admin credentials
    login_data = {
        "account": "admin",
        "password": "admin"
    }

    session = requests.Session()
    response = session.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login Status: {response.status_code}")
    print(f"Login Response: {response.json()}")

    if response.status_code == 200:
        # Test current user endpoint
        response = session.get(f"{BASE_URL}/auth/current-user")
        print(f"Current User Status: {response.status_code}")
        print(f"Current User Response: {response.json()}")

    print("-" * 50)
    return session


def test_products(session):
    """Test products endpoints"""
    print("Testing products endpoints...")

    # Test getting products (should be empty initially)
    response = session.get(f"{BASE_URL}/products")
    print(f"Get Products Status: {response.status_code}")
    print(f"Get Products Response: {response.json()}")

    # Test creating a product
    product_data = {
        "name": "Test Laptop",
        "category": "Electronics",
        "warranty_years": 2,
        "image_url": "https://example.com/laptop.jpg"
    }

    response = session.post(f"{BASE_URL}/products", json=product_data)
    print(f"Create Product Status: {response.status_code}")
    print(f"Create Product Response: {response.json()}")

    if response.status_code == 201:
        product_id = response.json()['data']['product_id']

        # Test getting the specific product
        response = session.get(f"{BASE_URL}/products/{product_id}")
        print(f"Get Product Status: {response.status_code}")
        print(f"Get Product Response: {response.json()}")

        # Test updating the product
        update_data = {
            "name": "Updated Test Laptop",
            "warranty_years": 3
        }
        response = session.put(
            f"{BASE_URL}/products/{product_id}", json=update_data)
        print(f"Update Product Status: {response.status_code}")
        print(f"Update Product Response: {response.json()}")

    print("-" * 50)


def test_suppliers(session):
    """Test suppliers endpoints"""
    print("Testing suppliers endpoints...")

    # Test getting suppliers
    response = session.get(f"{BASE_URL}/suppliers")
    print(f"Get Suppliers Status: {response.status_code}")
    print(f"Get Suppliers Response: {response.json()}")

    # Test creating a supplier
    supplier_data = {
        "supplier_name": "Test Supplier API",
        "contact": "test@supplier.com"
    }

    response = session.post(f"{BASE_URL}/suppliers", json=supplier_data)
    print(f"Create Supplier Status: {response.status_code}")
    print(f"Create Supplier Response: {response.json()}")

    if response.status_code == 201:
        supplier_id = response.json()['data']['supplier_id']

        # Test getting the specific supplier
        response = session.get(f"{BASE_URL}/suppliers/{supplier_id}")
        print(f"Get Supplier Status: {response.status_code}")
        print(f"Get Supplier Response: {response.json()}")

    print("-" * 50)


def test_customers(session):
    """Test customers endpoints"""
    print("Testing customers endpoints...")

    # Test getting customers
    response = session.get(f"{BASE_URL}/customers")
    print(f"Get Customers Status: {response.status_code}")
    print(f"Get Customers Response: {response.json()}")

    # Test creating a customer
    customer_data = {
        "name": "Test Customer API",
        "contact": "test@customer.com",
        "address": "123 Test Street, Test City"
    }

    response = session.post(f"{BASE_URL}/customers", json=customer_data)
    print(f"Create Customer Status: {response.status_code}")
    print(f"Create Customer Response: {response.json()}")

    if response.status_code == 201:
        customer_id = response.json()['data']['customer_id']

        # Test getting the specific customer
        response = session.get(f"{BASE_URL}/customers/{customer_id}")
        print(f"Get Customer Status: {response.status_code}")
        print(f"Get Customer Response: {response.json()}")

    print("-" * 50)


def main():
    """Run all tests"""
    print("=== Warehouse Management System API Test ===\n")

    try:
        # Test basic endpoints
        test_health()
        test_init_db()

        # Test authentication and CRUD operations
        session = test_login()
        test_products(session)
        test_suppliers(session)
        test_customers(session)

        print("✅ All tests completed!")

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
