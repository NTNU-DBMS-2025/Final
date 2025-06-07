# 🔗 Frontend-Backend Integration Setup Guide

## 📋 Overview

This guide will help you set up and test the complete integration between the Vue.js frontend and Flask backend for the Warehouse Management System.

## ✅ Completed Integration Tasks

### 🔧 API Layer Updates
- ✅ Updated `axios.js` base URL configuration
- ✅ Implemented complete **Shipments API** (`shipments.js`)
- ✅ Implemented complete **Scrap Management API** (`scrap.js`)
- ✅ Implemented complete **Customers API** (`customers.js`)
- ✅ Implemented complete **Locations API** (`locations.js`)
- ✅ Implemented complete **Users API** (`users.js`)
- ✅ Updated **Orders API** to use real backend calls
- ✅ Updated **Auth API** to remove mock data
- ✅ Added compatibility aliases for existing frontend code

### 🎯 Key Modules Connected
- **儲位管理 (Locations Management)** - Full CRUD operations
- **報廢管理 (Scrap Management)** - Analytics and tracking
- **客戶管理 (Customer Management)** - Customer data and orders
- **訂單管理 (Order Management)** - Order processing and items
- **出貨管理 (Shipment Management)** - Shipping and vendors

## 🚀 Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (if not exists)
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your database configuration
echo "SECRET_KEY=your-secret-key-here" > .env
echo "DATABASE_URL=mysql+pymysql://root:password@localhost/warehouse_db" >> .env

# Create MySQL database
mysql -u root -p -e "CREATE DATABASE warehouse_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Initialize sample data
python init_data.py

# Start the backend server
python app.py
```

The backend will be available at `http://localhost:5001`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not done)
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 3. Test Integration

```bash
# Run the integration test script
python test_integration.py
```

## 📡 API Endpoints Summary

### Core Modules
| Module | Endpoint | Status |
|--------|----------|--------|
| 認證 (Auth) | `/api/auth/*` | ✅ Connected |
| 產品 (Products) | `/api/products/*` | ✅ Connected |
| 供應商 (Suppliers) | `/api/suppliers/*` | ✅ Connected |
| 客戶 (Customers) | `/api/customers/*` | ✅ Connected |
| 訂單 (Orders) | `/api/orders/*` | ✅ Connected |
| 庫存 (Inventory) | `/api/inventory/*` | ✅ Connected |
| 儲位 (Locations) | `/api/locations/*` | ✅ Connected |
| 出貨 (Shipments) | `/api/shipments/*` | ✅ Connected |
| 報廢 (Scrap) | `/api/scrap/*` | ✅ Connected |
| 使用者 (Users) | `/api/users/*` | ✅ Connected |

### New API Features Added

#### 🏢 Customers API (`/api/customers`)
- `GET /customers` - List customers with pagination/search
- `POST /customers` - Create new customer
- `PUT /customers/{id}` - Update customer
- `DELETE /customers/{id}` - Delete customer
- `GET /customers/{id}/orders` - Get customer order history

#### 📦 Orders API (`/api/orders`)
- `GET /orders` - List orders with filters
- `POST /orders` - Create new order
- `PUT /orders/{id}` - Update order
- `PATCH /orders/{id}/status` - Update order status
- `GET /orders/{id}/items` - Get order items
- `POST /orders/{id}/items` - Add order item

#### 🚚 Shipments API (`/api/shipments`)
- `GET /shipments` - List shipments with filters
- `POST /shipments` - Create new shipment
- `PUT /shipments/{id}` - Update shipment
- `PATCH /shipments/{id}/status` - Update shipment status
- `GET /shipping-vendors` - List shipping vendors

#### 🗑️ Scrap API (`/api/scrap`)
- `GET /scrap` - List scrap records with filters
- `POST /scrap` - Create scrap record
- `GET /scrap/analytics` - Get scrap analytics
- `GET /scrap/stats` - Get scrap statistics

#### 📍 Locations API (`/api/locations`)
- `GET /locations` - List storage locations
- `POST /locations` - Create new location
- `GET /locations/zones` - Get location zones
- `GET /locations/{id}/inventory` - Get location inventory

#### 👥 Users API (`/api/users`)
- `GET /users` - List users with role filtering
- `POST /users` - Create new user
- `GET /users/{id}/roles` - Get user roles
- `POST /users/{id}/roles` - Assign role to user

#### 🔐 Roles API (`/api/users/roles`)
- `GET /users/roles` - List all roles
- `POST /users/roles` - Create new role
- `PUT /users/roles/{id}` - Update role
- `DELETE /users/roles/{id}` - Delete role

## 🔧 Configuration Details

### Frontend API Configuration
```javascript
// frontend/src/api/axios.js
const apiClient = axios.create({
    baseURL: 'http://localhost:5001/api',  // Includes /api prefix
    timeout: 10000,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json'
    }
})
```

### Backend CORS Configuration
```python
# backend/app.py
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
```

## 🧪 Testing the Integration

### Manual Testing Steps

1. **Start both servers** (backend on :5001, frontend on :5173)

2. **Test Authentication:**
   - Login with demo accounts (admin/admin, sales/sales, warehouse/warehouse)
   - Verify session persistence

3. **Test Core Modules:**
   - Navigate to each management page
   - Test CRUD operations
   - Verify data persistence

4. **Test API Responses:**
   - Check browser network tab for API calls
   - Verify proper error handling
   - Test pagination and search

### Automated Testing
```bash
# Run the integration test script
python test_integration.py
```

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors:**
   - Ensure backend CORS is configured for `http://localhost:5173`
   - Check that `withCredentials: true` is set in axios

2. **Database Connection:**
   - Verify MySQL is running
   - Check database credentials in `.env`
   - Run `python init_data.py` to initialize data

3. **API Endpoint Errors:**
   - Check backend logs for detailed error messages
   - Verify all Flask blueprints are registered
   - Ensure proper route prefixes

4. **Frontend API Calls:**
   - Check browser console for JavaScript errors
   - Verify API function names match exports
   - Test with browser dev tools network tab

## 📈 Next Steps

With the integration complete, you can now:

1. **Add more advanced features:**
   - Real-time notifications
   - File upload functionality
   - Advanced reporting

2. **Enhance security:**
   - Implement JWT tokens
   - Add rate limiting
   - Enhance input validation

3. **Optimize performance:**
   - Add caching layers
   - Implement database indexing
   - Add API response compression

4. **Deploy to production:**
   - Set up production database
   - Configure environment variables
   - Set up reverse proxy (nginx)

## 🎉 Success!

Your Warehouse Management System frontend and backend are now fully integrated! All the key modules (儲位管理、報廢管理、客戶管理、訂單管理、出貨管理) are connected and ready for use. 