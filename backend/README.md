# Warehouse Management System - Backend API

A comprehensive Flask-based REST API for warehouse management system with role-based authentication, inventory tracking, order management, and reporting capabilities.

## 🏗️ Architecture Overview

This backend provides a RESTful API built with Flask and SQLAlchemy, featuring:

- **Flask** - Lightweight web framework for API endpoints
- **SQLAlchemy** - ORM for database operations
- **JWT Authentication** - Secure token-based authentication
- **MySQL Database** - Persistent data storage
- **Modular Blueprint Structure** - Organized route handlers
- **Role-based Access Control** - Multi-level user permissions

## 📋 Features

### Core Modules
- **Authentication & Authorization** - JWT-based auth with role management
- **Product Management** - CRUD operations for products and suppliers
- **Customer Management** - Customer data and relationship tracking
- **Order Management** - Order processing and fulfillment
- **Inventory Management** - Stock tracking and location management
- **Shipment Tracking** - Shipping vendor integration
- **Scrap Management** - Waste and damaged goods tracking
- **Reporting** - Business intelligence and analytics
- **User Management** - Multi-role user administration

### User Roles
- **Admin** - Full system access and user management
- **Sales** - Customer and order management
- **Warehouse** - Inventory and location management
- **Shipping Vendor** - Shipment and delivery tracking

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- Virtual environment (recommended)

### Installation

1. **Clone and navigate to backend**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file
touch .env

# Add the following variables:
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://username:password@localhost/warehouse_db
JWT_SECRET_KEY=your-jwt-secret
FRONTEND_URL=http://localhost:5173
```

5. **Set up MySQL database**
```bash
# Create database
mysql -u root -p -e "CREATE DATABASE warehouse_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

6. **Reset and initialize everything with sample data**
```bash
python reset_and_init_data.py
```

This script will:
- Drop and recreate all tables with updated schema
- Load comprehensive sample data (users, products, customers, orders, etc.)
- Create database views for reporting
- Test reports functionality
- Display demo accounts and API endpoints

7. **Start the development server**
```bash
python app.py
```

The API will be available at: **http://localhost:5001**

## 📁 Project Structure

```
backend/
├── app.py                  # Main Flask application
├── models.py              # SQLAlchemy database models
├── auth.py                # Authentication & JWT handling
├── products.py            # Product management endpoints
├── suppliers.py           # Supplier management endpoints
├── customers.py           # Customer management endpoints
├── orders.py              # Order management endpoints
├── inventory.py           # Inventory management endpoints
├── locations.py           # Location management endpoints
├── shipments.py           # Shipment tracking endpoints
├── scrap.py               # Scrap management endpoints
├── users.py               # User management endpoints
├── reports.py             # Reporting and analytics endpoints
├── ddl.sql                # Database schema DDL
├── views.sql              # Database views for reporting
├── init_data.py           # Initial data seeding script
├── reset_and_init_data.py # Database reset and initialization
├── setup_reports.py       # Report views setup script
├── migrate_order_table.py # Database migration utility
├── recreate_db.py         # Database recreation utility
├── requirements.txt       # Python dependencies
└── test_api.py            # Comprehensive API testing
```

## 📊 Database Schema

### Core Tables
- **Product** - Product catalog with categories and warranty info
- **Supplier** - Supplier information and product relationships
- **Customer** - Customer data with types and levels
- **User & Role** - User accounts with role-based permissions
- **Order & Order_Item** - Order processing and line items
- **Shipment** - Shipping information and tracking
- **Location** - Warehouse locations and zones
- **Inventory_Lot** - Stock levels by product and location
- **Scrap** - Damaged or waste product tracking

### Key Relationships
- Many-to-many: Suppliers ↔ Products, Users ↔ Roles
- One-to-many: Customer → Orders, Order → Order_Items
- Foreign keys: Order → Customer, Order → User, Shipment → Order

## 🔐 Authentication

### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
    "account": "admin",
    "password": "admin"
}
```

### Response
```json
{
    "success": true,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "data": {
        "user_id": 1,
        "account": "admin",
        "role_id": 1,
        "role_name": "Admin"
    }
}
```

### Using JWT Token
Include in request headers:
```
Authorization: Bearer <your-jwt-token>
```

### Demo Accounts
| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin |
| Sales | sales | sales |
| Warehouse | warehouse | warehouse |

## 🛠️ API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/current-user` - Get current user info

### Products
- `GET /api/products` - List all products
- `POST /api/products` - Create new product
- `GET /api/products/{id}` - Get product details
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### Suppliers
- `GET /api/suppliers` - List all suppliers
- `POST /api/suppliers` - Create new supplier
- `GET /api/suppliers/{id}` - Get supplier details
- `PUT /api/suppliers/{id}` - Update supplier
- `DELETE /api/suppliers/{id}` - Delete supplier

### Customers
- `GET /api/customers` - List customers with filters
- `POST /api/customers` - Create new customer
- `GET /api/customers/{id}` - Get customer details
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer

### Orders
- `GET /api/orders` - List orders with filters
- `POST /api/orders` - Create new order
- `GET /api/orders/{id}` - Get order details
- `PUT /api/orders/{id}` - Update order
- `DELETE /api/orders/{id}` - Cancel order

### Inventory
- `GET /api/inventory` - Get inventory levels
- `POST /api/inventory/adjust` - Adjust stock levels
- `GET /api/inventory/low-stock` - Get low stock alerts
- `GET /api/inventory/locations` - Get stock by location

### Locations
- `GET /api/locations` - List all locations
- `POST /api/locations` - Create new location
- `GET /api/locations/{id}` - Get location details
- `PUT /api/locations/{id}` - Update location
- `DELETE /api/locations/{id}` - Delete location

### Shipments
- `GET /api/shipments` - List all shipments
- `POST /api/shipments` - Create new shipment
- `GET /api/shipments/{id}` - Get shipment details
- `PUT /api/shipments/{id}` - Update shipment
- `DELETE /api/shipments/{id}` - Delete shipment

### Scrap
- `GET /api/scrap` - List scrap records
- `POST /api/scrap` - Create new scrap record
- `GET /api/scrap/{id}` - Get scrap details
- `PUT /api/scrap/{id}` - Update scrap record
- `DELETE /api/scrap/{id}` - Delete scrap record

### Users
- `GET /api/users` - List all users
- `POST /api/users` - Create new user
- `GET /api/users/{id}` - Get user details
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

### Reports
- `GET /api/reports/dashboard` - Dashboard statistics
- `GET /api/reports/sales` - Sales reports
- `GET /api/reports/inventory` - Inventory reports
- `GET /api/reports/scrap` - Scrap reports

### System
- `GET /api/health` - API health check
- `GET /api/init-db` - Initialize database tables
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/dashboard/sales-stats` - Sales dashboard statistics

## 🧪 Testing

### Run API Tests
```bash
python test_api.py
```

### Test Coverage
The `test_api.py` file provides comprehensive API endpoint testing.

### Manual Testing with curl
```bash
# Health check
curl http://localhost:5001/api/health

# Login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"account":"admin","password":"admin"}'

# Get products (with auth)
curl -X GET http://localhost:5001/api/products \
  -H "Authorization: Bearer <your-token>"
```

## 🔧 Development

### Database Operations

**Reset and recreate database with full initialization (Recommended):**
```bash
python reset_and_init_data.py
```

This comprehensive script handles:
- Database schema reset
- Sample data loading
- Views creation
- Reports testing
- Demo account setup

**Individual operations:**
```bash
# Manual table creation (if needed)
python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all()"

# Load sample data only
python init_data.py

# Create database views only
python setup_reports.py

# Database migration (if needed)
python migrate_order_table.py
```

### Adding New Endpoints

1. Create new blueprint in separate file
2. Import and register in `app.py`
3. Add authentication decorators as needed
4. Update this README with new endpoints

### Code Style
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Document functions with docstrings
- Keep routes in separate blueprint files

## 🚀 Production Deployment

### Environment Setup
```bash
# Production environment variables
SECRET_KEY=strong-production-secret
DATABASE_URL=mysql+pymysql://user:pass@prod-host/warehouse_db
JWT_SECRET_KEY=strong-jwt-secret
FLASK_ENV=production
FRONTEND_URL=https://yourdomain.com
```

### Database Setup
```bash
# Create production database
mysql -u root -p -e "CREATE DATABASE warehouse_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Run DDL
mysql -u root -p warehouse_db < ddl.sql

# Set up views
mysql -u root -p warehouse_db < views.sql
```

### WSGI Deployment
```python
# wsgi.py
from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()
```

## 📈 Performance Considerations

- Database indexes on frequently queried columns
- Pagination for large result sets
- Caching for static data
- Connection pooling for high traffic
- Background tasks for heavy operations

## 🔍 Troubleshooting

### Common Issues

**Database Connection Error:**
```bash
# Check MySQL service
sudo service mysql status

# Verify credentials
mysql -u username -p
```

**JWT Token Issues:**
```bash
# Check JWT_SECRET_KEY in .env
# Verify token expiration (24 hours default)
```

**CORS Issues:**
```bash
# Verify FRONTEND_URL in .env
# Check CORS configuration in app.py
```

### Logging
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📝 API Documentation

For detailed API documentation, see the individual module files:
- Authentication: `auth.py`
- Products: `products.py`
- Suppliers: `suppliers.py`
- Customers: `customers.py`
- Orders: `orders.py`
- Inventory: `inventory.py`
- Locations: `locations.py`
- Shipments: `shipments.py`
- Scrap: `scrap.py`
- Users: `users.py`
- Reports: `reports.py`

## 📊 Database Views

Pre-built views for reporting (see `views.sql`):
- `ProductInventoryView` - Product stock summary
- `OrderSummaryView` - Order analytics
- `CustomerOrderView` - Customer order history
- `ScrapSummaryView` - Scrap tracking

## 🔒 Security Features

- JWT token-based authentication
- Role-based access control
- Password hashing with Werkzeug
- SQL injection protection via SQLAlchemy
- CORS configuration
- Input validation and sanitization

---

**License:** Educational/Academic Use Only  
**Course:** Database Management System  
**Version:** 1.0.0
