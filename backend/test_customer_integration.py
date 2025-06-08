#!/usr/bin/env python3
"""
Customer Management Integration Test
Tests all customer API endpoints and data integrity
"""

import requests
import json
import sys
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:5000/api"
TEST_EMAIL = "admin"
TEST_PASSWORD = "admin"


class CustomerAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.test_customer_id = None

    def authenticate(self):
        """Authenticate and get JWT token"""
        print("🔐 Authenticating...")

        response = self.session.post(f"{BASE_URL}/auth/login", json={
            "account": TEST_EMAIL,
            "password": TEST_PASSWORD
        })

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                self.token = data['data']['access_token']
                self.session.headers.update({
                    'Authorization': f'Bearer {self.token}'
                })
                print("✅ Authentication successful")
                return True

        print(f"❌ Authentication failed: {response.text}")
        return False

    def test_get_customers(self):
        """Test GET /customers endpoint"""
        print("\n📋 Testing customer list...")

        response = self.session.get(f"{BASE_URL}/customers")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                customers = data['data']
                print(f"✅ Retrieved {len(customers)} customers")

                # Check if customers have new fields
                if customers:
                    sample_customer = customers[0]
                    required_fields = ['customer_id', 'name', 'contact', 'phone', 'email',
                                       'customer_type', 'customer_level', 'status', 'created_at']

                    missing_fields = [
                        field for field in required_fields if field not in sample_customer]
                    if missing_fields:
                        print(f"❌ Missing fields: {missing_fields}")
                        return False

                    print("✅ All required fields present")
                    print(f"   Sample customer: {sample_customer['name']}")
                    print(f"   Type: {sample_customer['customer_type']}")
                    print(f"   Level: {sample_customer['customer_level']}")
                    print(f"   Status: {sample_customer['status']}")
                return True

        print(f"❌ Failed to retrieve customers: {response.text}")
        return False

    def test_get_customer_stats(self):
        """Test GET /customers/stats endpoint"""
        print("\n📊 Testing customer statistics...")

        response = self.session.get(f"{BASE_URL}/customers/stats")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                stats = data['data']
                print("✅ Statistics retrieved successfully")
                print(f"   Total customers: {stats.get('total_customers', 0)}")
                print(
                    f"   Active customers: {stats.get('active_customers', 0)}")
                print(
                    f"   New this month: {stats.get('new_customers_month', 0)}")

                if 'customer_by_type' in stats:
                    print(f"   By type: {stats['customer_by_type']}")
                if 'customer_by_level' in stats:
                    print(f"   By level: {stats['customer_by_level']}")

                return True

        print(f"❌ Failed to retrieve statistics: {response.text}")
        return False

    def test_create_customer(self):
        """Test POST /customers endpoint"""
        print("\n➕ Testing customer creation...")

        test_customer = {
            "name": "測試客戶公司",
            "contact": "測試聯絡人",
            "phone": "02-12345678",
            "email": "test@example.com",
            "address": "台北市信義區測試路123號",
            "customer_type": "business",
            "customer_level": "silver",
            "tax_id": "12345678",
            "status": "active",
            "notes": "API測試建立的客戶"
        }

        response = self.session.post(
            f"{BASE_URL}/customers", json=test_customer)

        if response.status_code == 201:
            data = response.json()
            if data.get('success'):
                customer = data['data']
                self.test_customer_id = customer['customer_id']
                print(
                    f"✅ Customer created successfully (ID: {self.test_customer_id})")
                print(f"   Name: {customer['name']}")
                print(f"   Email: {customer['email']}")
                print(f"   Type: {customer['customer_type']}")
                return True

        print(f"❌ Failed to create customer: {response.text}")
        return False

    def test_update_customer(self):
        """Test PUT /customers/{id} endpoint"""
        if not self.test_customer_id:
            print("❌ No test customer ID available for update test")
            return False

        print(
            f"\n✏️  Testing customer update (ID: {self.test_customer_id})...")

        update_data = {
            "notes": "API測試更新的客戶資料",
            "customer_level": "gold",
            "phone": "02-87654321"
        }

        response = self.session.put(
            f"{BASE_URL}/customers/{self.test_customer_id}", json=update_data)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                customer = data['data']
                print("✅ Customer updated successfully")
                print(f"   Updated notes: {customer['notes']}")
                print(f"   Updated level: {customer['customer_level']}")
                print(f"   Updated phone: {customer['phone']}")
                return True

        print(f"❌ Failed to update customer: {response.text}")
        return False

    def test_get_single_customer(self):
        """Test GET /customers/{id} endpoint"""
        if not self.test_customer_id:
            print("❌ No test customer ID available for single customer test")
            return False

        print(
            f"\n👤 Testing single customer retrieval (ID: {self.test_customer_id})...")

        response = self.session.get(
            f"{BASE_URL}/customers/{self.test_customer_id}")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                customer = data['data']
                print("✅ Single customer retrieved successfully")
                print(f"   Name: {customer['name']}")
                print(f"   Total orders: {customer.get('total_orders', 0)}")
                return True

        print(f"❌ Failed to retrieve single customer: {response.text}")
        return False

    def test_search_customers(self):
        """Test customer search functionality"""
        print("\n🔍 Testing customer search...")

        response = self.session.get(f"{BASE_URL}/customers?search=台積電")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                customers = data['data']
                print(f"✅ Search returned {len(customers)} results")
                if customers:
                    print(f"   Found: {customers[0]['name']}")
                return True

        print(f"❌ Search failed: {response.text}")
        return False

    def test_delete_customer(self):
        """Test DELETE /customers/{id} endpoint"""
        if not self.test_customer_id:
            print("❌ No test customer ID available for deletion test")
            return False

        print(
            f"\n🗑️  Testing customer deletion (ID: {self.test_customer_id})...")

        response = self.session.delete(
            f"{BASE_URL}/customers/{self.test_customer_id}")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Customer deleted successfully")
                self.test_customer_id = None
                return True

        print(f"❌ Failed to delete customer: {response.text}")
        return False

    def run_all_tests(self):
        """Run all customer API tests"""
        print("🧪 Starting Customer API Integration Tests")
        print("=" * 50)

        tests = [
            ("Authentication", self.authenticate),
            ("Get Customers List", self.test_get_customers),
            ("Get Customer Stats", self.test_get_customer_stats),
            ("Create Customer", self.test_create_customer),
            ("Update Customer", self.test_update_customer),
            ("Get Single Customer", self.test_get_single_customer),
            ("Search Customers", self.test_search_customers),
            ("Delete Customer", self.test_delete_customer)
        ]

        passed = 0
        total = len(tests)

        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                else:
                    print(f"❌ {test_name} FAILED")
            except Exception as e:
                print(f"❌ {test_name} ERROR: {e}")

        print("\n" + "=" * 50)
        print(f"🎯 Test Results: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed! Customer API integration is working perfectly!")
        else:
            print("⚠️  Some tests failed. Please check the backend server and database.")

        return passed == total


def main():
    """Main test function"""
    tester = CustomerAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
