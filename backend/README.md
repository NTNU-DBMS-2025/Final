# Warehouse Management System - Backend

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL server running
- Virtual environment (recommended)

### Setup

1. **Create and activate virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create `.env` file:**
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://username:password@localhost/warehouse_db
```

4. **Create MySQL database:**
```sql
CREATE DATABASE warehouse_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. **Initialize sample data:**
```bash
python init_data.py
```

6. **Run the server:**
```bash
python app.py
```

The API will be available at `http://localhost:5001`

## 📊 Checkpoints Completed

### ✅ Checkpoint 1: Basic Flask Setup
- Flask application with CORS
- SQLAlchemy configuration
- Environment variables support
- Health check endpoint

### ✅ Checkpoint 2: Database Models
- Complete SQLAlchemy models matching ddl.sql
- Proper relationships and foreign keys
- Association tables for many-to-many relationships

### ✅ Checkpoint 3: Authentication System
- Session-based authentication (no JWT yet)
- User login/logout endpoints
- Role-based access control decorators
- Demo user creation

### ✅ Checkpoint 4: Products API
- Full CRUD operations for products
- Pagination and search support
- Role-based permissions
- Supplier relationship management

### ✅ Checkpoint 5: Suppliers & Customers APIs
- Full CRUD operations for suppliers and customers
- Pagination and search functionality
- Product-supplier relationship management
- Customer order history tracking
- Role-based permissions (Admin/Warehouse for suppliers, Admin/Sales for customers)

## 🧪 Testing

### Run API tests:
```bash
python test_api.py
```

### Demo Accounts:
- **Admin:** admin/admin
- **Sales:** sales/sales  
- **Warehouse:** warehouse/warehouse

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/current-user` - Get current user info

### Products
- `GET /api/products` - List products (with pagination/search)
- `GET /api/products/{id}` - Get specific product
- `POST /api/products` - Create product (Admin/Warehouse)
- `PUT /api/products/{id}` - Update product (Admin/Warehouse)
- `DELETE /api/products/{id}` - Delete product (Admin only)

### Suppliers
- `GET /api/suppliers` - List suppliers (with pagination/search)
- `GET /api/suppliers/{id}` - Get specific supplier
- `POST /api/suppliers` - Create supplier (Admin/Warehouse)
- `PUT /api/suppliers/{id}` - Update supplier (Admin/Warehouse)
- `DELETE /api/suppliers/{id}` - Delete supplier (Admin only)
- `GET /api/suppliers/{id}/products` - Get supplier's products
- `POST /api/suppliers/{id}/products/{product_id}` - Add product to supplier
- `DELETE /api/suppliers/{id}/products/{product_id}` - Remove product from supplier

### Customers
- `GET /api/customers` - List customers (with pagination/search)
- `GET /api/customers/{id}` - Get specific customer
- `POST /api/customers` - Create customer (Admin/Sales)
- `PUT /api/customers/{id}` - Update customer (Admin/Sales)
- `DELETE /api/customers/{id}` - Delete customer (Admin only)
- `GET /api/customers/{id}/orders` - Get customer's order history

### System
- `GET /api/health` - Health check
- `GET /api/init-db` - Initialize database tables

## 🔄 Next Steps

- [x] Suppliers API endpoints
- [x] Customers API endpoints  
- [ ] Orders and OrderItems API
- [ ] Inventory management API
- [ ] Shipments API
- [ ] Locations API
- [ ] Scrap management API
- [ ] Reporting endpoints
- [ ] JWT authentication (optional)

## 🗄️ Database Schema

The database follows the schema defined in `ddl.sql` with tables for:
- Users and Roles
- Products and Suppliers
- Customers and Orders
- Inventory and Locations
- Shipments and Scrap records

All relationships and constraints are properly implemented in SQLAlchemy models. 