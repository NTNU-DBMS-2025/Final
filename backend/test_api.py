#!/usr/bin/env python3
"""
Comprehensive Test Suite for the Warehouse Management System API
Tests all endpoints from all backend modules
"""

import requests
import json
import time
from datetime import datetime, date

BASE_URL = "http://localhost:5001/api"


class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        self.test_data = {}

    def log_test(self, test_name, status_code, response_data, expected_status=200):
        """Log test results"""
        status = "✅" if status_code == expected_status else "❌"
        print(f"{status} {test_name} - Status: {status_code}")
        if status_code != expected_status:
            print(f"   Expected: {expected_status}, Got: {status_code}")
            print(f"   Response: {response_data}")
        print("-" * 60)

    def safe_get_json(self, response):
        """Safely get JSON from response, handling empty or invalid responses"""
        try:
            if response.content:
                return response.json()
            else:
                return {"message": "Empty response"}
        except ValueError:
            return {"error": "Invalid JSON response", "content": response.text[:200]}

    def test_health(self):
        """Test health endpoint"""
        print("🏥 Testing Health Endpoint")
        response = self.session.get(f"{BASE_URL}/health")
        self.log_test("Health Check", response.status_code,
                      self.safe_get_json(response))
        return response.status_code == 200

    def test_authentication(self):
        """Test authentication endpoints"""
        print("🔐 Testing Authentication Endpoints")

        # Test login with admin credentials
        login_data = {"account": "admin", "password": "admin"}
        response = self.session.post(f"{BASE_URL}/auth/login", json=login_data)
        response_data = self.safe_get_json(response)
        self.log_test("Admin Login", response.status_code, response_data)

        if response.status_code == 200 and 'token' in response_data:
            token = response_data['token']
            self.admin_token = token
            self.session.headers.update({'Authorization': f'Bearer {token}'})

            # Test current user
            response = self.session.get(f"{BASE_URL}/auth/current-user")
            self.log_test("Get Current User",
                          response.status_code, self.safe_get_json(response))

            return True
        return False

    def test_users(self):
        """Test user management endpoints"""
        print("👥 Testing User Management Endpoints")

        # Get all users
        response = self.session.get(f"{BASE_URL}/users")
        self.log_test("Get All Users", response.status_code,
                      self.safe_get_json(response))

        # Get all roles
        response = self.session.get(f"{BASE_URL}/users/roles")
        self.log_test("Get All Roles", response.status_code,
                      self.safe_get_json(response))

        # Create a test user
        user_data = {
            "account": "test_user_api",
            "password": "test123",
            "role_id": 2,  # Sales role
            "status": "active"
        }
        response = self.session.post(f"{BASE_URL}/users", json=user_data)
        response_data = self.safe_get_json(response)
        self.log_test("Create User", response.status_code, response_data, 201)

        if response.status_code == 201 and 'data' in response_data:
            user_id = response_data['data']['user_id']
            self.test_data['user_id'] = user_id

            # Get specific user
            response = self.session.get(f"{BASE_URL}/users/{user_id}")
            self.log_test("Get Specific User",
                          response.status_code, self.safe_get_json(response))

    def test_products(self):
        """Test product management endpoints"""
        print("📦 Testing Product Management Endpoints")

        # Get all products
        response = self.session.get(f"{BASE_URL}/products")
        self.log_test("Get All Products",
                      response.status_code, self.safe_get_json(response))

        # Create a test product
        product_data = {
            "name": "Test Laptop API",
            "category": "Electronics",
            "warranty_years": 2,
            "image_url": "https://example.com/laptop.jpg",
            "reorder_point": 10
        }
        response = self.session.post(f"{BASE_URL}/products", json=product_data)
        response_data = self.safe_get_json(response)
        self.log_test("Create Product", response.status_code,
                      response_data, 201)

        if response.status_code == 201 and 'data' in response_data:
            product_id = response_data['data']['product_id']
            self.test_data['product_id'] = product_id

            # Get specific product
            response = self.session.get(f"{BASE_URL}/products/{product_id}")
            self.log_test("Get Specific Product",
                          response.status_code, self.safe_get_json(response))

            # Update product
            update_data = {
                "name": "Updated Test Laptop API", "warranty_years": 3}
            response = self.session.put(
                f"{BASE_URL}/products/{product_id}", json=update_data)
            self.log_test("Update Product",
                          response.status_code, self.safe_get_json(response))

    def test_suppliers(self):
        """Test supplier management endpoints"""
        print("🏭 Testing Supplier Management Endpoints")

        # Get all suppliers
        response = self.session.get(f"{BASE_URL}/suppliers")
        self.log_test("Get All Suppliers",
                      response.status_code, self.safe_get_json(response))

        # Create a test supplier
        supplier_data = {
            "supplier_name": "Test Supplier API",
            "contact_name": "John Doe",
            "phone": "123-456-7890",
            "email": "test@supplier.com",
            "address": "123 Supplier St",
            "supplier_type": "manufacturer",
            "status": "active"
        }
        response = self.session.post(
            f"{BASE_URL}/suppliers", json=supplier_data)
        response_data = self.safe_get_json(response)
        self.log_test("Create Supplier", response.status_code,
                      response_data, 201)

        if response.status_code == 201 and 'data' in response_data:
            supplier_id = response_data['data']['supplier_id']
            self.test_data['supplier_id'] = supplier_id

            # Get specific supplier
            response = self.session.get(f"{BASE_URL}/suppliers/{supplier_id}")
            self.log_test("Get Specific Supplier",
                          response.status_code, self.safe_get_json(response))

    def test_customers(self):
        """Test customer management endpoints"""
        print("👤 Testing Customer Management Endpoints")

        # Get all customers
        response = self.session.get(f"{BASE_URL}/customers")
        self.log_test("Get All Customers",
                      response.status_code, self.safe_get_json(response))

        # Create a test customer
        customer_data = {
            "name": "Test Customer API",
            "contact": "Jane Smith",
            "phone": "987-654-3210",
            "email": "test@customer.com",
            "address": "456 Customer Ave",
            "customer_type": "individual",
            "customer_level": "silver",
            "status": "active"
        }
        response = self.session.post(
            f"{BASE_URL}/customers", json=customer_data)
        response_data = self.safe_get_json(response)
        self.log_test("Create Customer", response.status_code,
                      response_data, 201)

        if response.status_code == 201 and 'data' in response_data:
            customer_id = response_data['data']['customer_id']
            self.test_data['customer_id'] = customer_id

            # Get specific customer
            response = self.session.get(f"{BASE_URL}/customers/{customer_id}")
            self.log_test("Get Specific Customer",
                          response.status_code, self.safe_get_json(response))

    def test_locations(self):
        """Test location management endpoints"""
        print("📍 Testing Location Management Endpoints")

        # Get all locations
        response = self.session.get(f"{BASE_URL}/locations")
        self.log_test("Get All Locations",
                      response.status_code, self.safe_get_json(response))

        # Create a test location
        location_data = {
            "location_code": "TEST-A1-01",
            "location_name": "Test Location API",
            "zone": "A",
            "shelf": "1",
            "location_type": "storage",
            "capacity": 100,
            "status": "active"
        }
        response = self.session.post(
            f"{BASE_URL}/locations", json=location_data)
        response_data = self.safe_get_json(response)
        self.log_test("Create Location", response.status_code,
                      response_data, 201)

        if response.status_code == 201 and 'data' in response_data:
            location_id = response_data['data']['location_id']
            self.test_data['location_id'] = location_id

            # Get specific location
            response = self.session.get(f"{BASE_URL}/locations/{location_id}")
            self.log_test("Get Specific Location",
                          response.status_code, self.safe_get_json(response))

    def test_inventory(self):
        """Test inventory management endpoints"""
        print("📊 Testing Inventory Management Endpoints")

        # Get all inventory
        response = self.session.get(f"{BASE_URL}/inventory")
        self.log_test("Get All Inventory",
                      response.status_code, self.safe_get_json(response))

        # Get low stock items
        response = self.session.get(f"{BASE_URL}/inventory/low-stock")
        self.log_test("Get Low Stock Items",
                      response.status_code, self.safe_get_json(response))

        # Test inventory creation/addition (if we have product and location)
        if 'product_id' in self.test_data and 'location_id' in self.test_data:
            # First, add some inventory (using POST to /inventory endpoint)
            inventory_data = {
                "product_id": self.test_data['product_id'],
                "location_id": self.test_data['location_id'],
                "quantity": 100,
                "expiry_date": "2025-12-31"
            }
            response = self.session.post(
                f"{BASE_URL}/inventory", json=inventory_data)
            self.log_test("Add Inventory",
                          response.status_code, self.safe_get_json(response))

    def test_orders(self):
        """Test order management endpoints"""
        print("🛒 Testing Order Management Endpoints")

        # Get all orders
        response = self.session.get(f"{BASE_URL}/orders")
        self.log_test("Get All Orders", response.status_code,
                      self.safe_get_json(response))

        # Create a test order (if we have customer and product)
        if 'customer_id' in self.test_data and 'product_id' in self.test_data:
            order_data = {
                "customer_id": self.test_data['customer_id'],
                "user_id": 1,  # Use admin user ID
                "ship_to": "Test Address for API Order",
                "priority": "normal",
                "notes": "API Test Order",
                "items": [
                    {
                        "product_id": self.test_data['product_id'],
                        "quantity": 2,
                        "unit_price": 999.99
                    }
                ]
            }
            response = self.session.post(f"{BASE_URL}/orders", json=order_data)
            response_data = self.safe_get_json(response)
            self.log_test("Create Order", response.status_code,
                          response_data, 201)

            if response.status_code == 201 and 'data' in response_data:
                order_id = response_data['data']['order_id']
                self.test_data['order_id'] = order_id

                # Get specific order
                response = self.session.get(f"{BASE_URL}/orders/{order_id}")
                self.log_test("Get Specific Order",
                              response.status_code, self.safe_get_json(response))

    def test_shipments(self):
        """Test shipment management endpoints"""
        print("🚚 Testing Shipment Management Endpoints")

        # Get all shipments
        response = self.session.get(f"{BASE_URL}/shipments")
        self.log_test("Get All Shipments",
                      response.status_code, self.safe_get_json(response))

        # Create a test shipment (if we have an order)
        if 'order_id' in self.test_data:
            shipment_data = {
                "order_id": self.test_data['order_id'],
                "tracking_no": f"TEST-TRACK-{int(time.time())}",
                "shipping_method": "Ground",
                "shipping_address": "Test Shipping Address",
                "estimated_delivery_date": "2024-12-31",
                "notes": "API Test Shipment"
            }
            response = self.session.post(
                f"{BASE_URL}/shipments", json=shipment_data)
            self.log_test("Create Shipment", response.status_code,
                          self.safe_get_json(response), 201)

    def test_scrap(self):
        """Test scrap management endpoints"""
        print("♻️ Testing Scrap Management Endpoints")

        # Get all scrap records
        response = self.session.get(f"{BASE_URL}/scrap")
        self.log_test("Get All Scrap Records",
                      response.status_code, self.safe_get_json(response))

        # Create a test scrap record (if we have product and location with inventory)
        if 'product_id' in self.test_data and 'location_id' in self.test_data:
            # Only create scrap if we successfully added inventory earlier
            scrap_data = {
                "product_id": self.test_data['product_id'],
                "location_id": self.test_data['location_id'],
                "quantity": 5,  # Less than the 100 we added in inventory test
                "reason": "API Test - Damaged during testing",
                "estimated_value": 50.00,
                "description": "Items damaged during API testing"
            }
            response = self.session.post(f"{BASE_URL}/scrap", json=scrap_data)
            self.log_test("Create Scrap Record",
                          response.status_code, self.safe_get_json(response), 201)

    def test_reports(self):
        """Test reporting endpoints"""
        print("📈 Testing Reporting Endpoints")

        # Test dashboard stats
        response = self.session.get(f"{BASE_URL}/dashboard/stats")
        self.log_test("Get Dashboard Stats",
                      response.status_code, self.safe_get_json(response))

        # Test sales dashboard stats
        response = self.session.get(f"{BASE_URL}/dashboard/sales-stats")
        self.log_test("Get Sales Dashboard Stats",
                      response.status_code, self.safe_get_json(response))

        # Test various reports (using actual available endpoints)
        report_endpoints = [
            # Summary reports
            "/reports/summary/inventory",
            "/reports/summary/sales",
            "/reports/summary/orders",
            "/reports/summary/financial",

            # Inventory reports
            "/reports/inventory/expired",
            "/reports/inventory/low-stock",
            "/reports/inventory/out-of-stock",
            "/reports/inventory/by-category",
            "/reports/inventory/days-of-supply",
            "/reports/inventory/idle-60d",
            "/reports/inventory/expiry-alert",

            # Sales reports
            "/reports/sales/30d",
            "/reports/sales/fast-moving-top10",
            "/reports/sales/avg-order-value-by-customer-type",

            # Order reports
            "/reports/orders/pending",
            "/reports/orders/delayed-shipping",
            "/reports/orders/unshipped-today",
            "/reports/orders/arrived-today",
            "/reports/orders/status-7d",
            "/reports/orders/to-ship-this-week",
            "/reports/orders/processing-time",

            # Shipment reports
            "/reports/shipments/today",
            "/reports/shipments/vendor-delays",

            # Location reports
            "/reports/locations/over-capacity",

            # Scrap reports (using correct endpoints)
            "/reports/scrap/cost-month",
            "/reports/scrap/product-scrap-rate",

            # Customer and supplier reports
            "/reports/customers/last-order",
            "/reports/suppliers/product-variants"
        ]

        for endpoint in report_endpoints:
            response = self.session.get(f"{BASE_URL}{endpoint}")
            response_data = self.safe_get_json(response)
            if response.status_code == 200 and isinstance(response_data, dict) and 'data' in response_data:
                if isinstance(response_data['data'], list):
                    summary = {"count": len(response_data['data'])}
                elif isinstance(response_data['data'], dict):
                    # For summary reports with nested structure
                    summary = {"status": "success", "type": "summary"}
                else:
                    summary = {"status": "success"}
            else:
                summary = response_data
            self.log_test(f"Report: {endpoint}", response.status_code, summary)

    def cleanup_test_data(self):
        """Clean up test data (optional)"""
        print("🧹 Cleaning up test data...")

        # Note: In a real scenario, you might want to delete test records
        # For now, we'll just log what we created
        print(f"Created test data: {self.test_data}")

    def run_all_tests(self):
        """Run the complete test suite"""
        print("=" * 80)
        print("🚀 COMPREHENSIVE WAREHOUSE MANAGEMENT SYSTEM API TEST SUITE")
        print("=" * 80)

        try:
            # Core system tests
            if not self.test_health():
                print("❌ Health check failed. Aborting tests.")
                return False

            if not self.test_authentication():
                print("❌ Authentication failed. Aborting tests.")
                return False

            # User and access management
            self.test_users()

            # Core business entity tests
            self.test_products()
            self.test_suppliers()
            self.test_customers()
            self.test_locations()

            # Operational tests
            self.test_inventory()
            self.test_orders()
            self.test_shipments()
            self.test_scrap()

            # Reporting and analytics
            self.test_reports()

            # Cleanup
            self.cleanup_test_data()

            print("=" * 80)
            print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
            print("📊 Check individual test results above for any specific failures.")
            print("=" * 80)

            return True

        except requests.exceptions.ConnectionError:
            print("❌ ERROR: Could not connect to the API server.")
            print("🔧 Make sure the Flask server is running on http://localhost:5001")
            print("💡 Start server with: python app.py")
            return False

        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {e}")
            return False


def main():
    """Main test runner"""
    tester = APITester()
    success = tester.run_all_tests()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
