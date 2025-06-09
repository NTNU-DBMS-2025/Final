# 倉儲管理系統 (Warehouse Management System)
# 2025 Database Theories (Team 14)
A complete warehouse management system with Vue.js frontend, Flask backend, and MySQL database integration.

## Project Overview

This is a fully functional warehouse management system featuring:

- **Frontend**: Vue.js 3 with Tailwind CSS for responsive UI
- **Backend**: Flask REST API with SQLAlchemy ORM 
- **Database**: MySQL with comprehensive schema and sample data
- **Authentication**: JWT-based authentication with role management
- **Integration**: Fully integrated frontend-backend communication

## Features

- **Role-based Access Control**: Admin, Sales, Warehouse, and Shipping Vendor roles
- **Product Management**: Complete CRUD operations for products and suppliers
- **Order Management**: Full order lifecycle management with item tracking
- **Inventory Management**: Real-time inventory tracking and location management
- **Customer Management**: Customer profiles and order history tracking
- **Shipment Management**: Shipping vendor integration and tracking
- **Scrap Management**: Waste tracking and analytics
- **User Management**: Role assignment and user administration
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **Dashboard Analytics**: Real-time statistics and reporting

## Prerequisites

Ensure you have the following installed:

- **Node.js** (version 16.0 or higher) - [Download here](https://nodejs.org/)
- **Python 3.8+** - [Download here](https://python.org/)
- **MySQL 8.0+** - [Download here](https://dev.mysql.com/downloads/)
- **Git** (for cloning the repository)

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone git@github.com:NTNU-DBMS-2025/Final.git
cd Final
```

### 2. Database Setup

```bash
# Create MySQL database
mysql -u root -p -e "CREATE DATABASE warehouse_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your database configuration
cp .env.example .env

# Initialize database with sample data
python reset_and_init_data.py

# Start the backend server
python app.py
```

The backend API will be available at: **http://localhost:5001**

### 4. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at: **http://localhost:5173**

### 5. Test Login Credentials

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
|Owner | owner | owner | Full system access |
| Admin | admin | admin | Full system access |
| Sales | sales | sales | Orders, customers, products |
| Warehouse | warehouse | warehouse | Inventory, locations, scrap |


## Project Structure

```
/
├── frontend/              # Vue.js frontend application
│   ├── src/
│   │   ├── components/    # Reusable Vue components
│   │   ├── views/         # Page components (dashboards, forms)
│   │   ├── api/           # API integration layer
│   │   ├── store/         # Vuex state management
│   │   ├── utils/         # Utility functions
│   │   ├── assets/        # Static assets
│   │   ├── router.js      # Vue Router configuration
│   │   └── main.js        # Application entry point
│   ├── public/            # Static public assets
│   ├── tailwind.config.js # Tailwind CSS configuration
│   ├── vite.config.js     # Vite build configuration
│   └── package.json       # Frontend dependencies
├── backend/               # Flask backend API
│   ├── models.py          # SQLAlchemy database models
│   ├── app.py             # Main Flask application
│   ├── auth.py            # Authentication endpoints
│   ├── products.py        # Product management API
│   ├── suppliers.py       # Supplier management API
│   ├── customers.py       # Customer management API
│   ├── orders.py          # Order management API
│   ├── inventory.py       # Inventory management API
│   ├── locations.py       # Location management API
│   ├── shipments.py       # Shipment management API
│   ├── scrap.py           # Scrap management API
│   ├── users.py           # User management API
│   ├── reports.py         # Reporting and analytics API
│   ├── init_data.py       # Database initialization script
│   ├── ddl.sql            # Database schema
│   └── requirements.txt   # Python dependencies
├── INTEGRATION_SETUP.md   # Detailed setup and API documentation
└── README.md              # This file
```

## API Endpoints

The system provides comprehensive REST API endpoints:

### Core Modules
| Module | Base Endpoint | Features |
|--------|---------------|----------|
| Authentication | `/api/auth/*` | Login, logout, session management |
| Products | `/api/products/*` | CRUD operations, search, categories |
| Suppliers | `/api/suppliers/*` | Supplier management and relationships |
| Customers | `/api/customers/*` | Customer profiles and order history |
| Orders | `/api/orders/*` | Order lifecycle, items, status updates |
| Inventory | `/api/inventory/*` | Stock levels, lot tracking, movements |
| Locations | `/api/locations/*` | Storage locations and zone management |
| Shipments | `/api/shipments/*` | Shipping vendors and tracking |
| Scrap | `/api/scrap/*` | Waste management and analytics |
| Users | `/api/users/*` | User administration and roles |
| Reports | `/api/reports/*` | Dashboard statistics and analytics |

## Available Scripts

### Frontend
```bash
cd frontend

npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend
```bash
cd backend

python app.py                    # Start Flask development server
python init_data.py             # Initialize database with sample data
python test_api.py              # Run API tests
python reset_and_init_data.py   # Reset and reinitialize database
```

## Development

### Frontend Development
- Hot reload enabled for rapid development
- Vue.js DevTools browser extension recommended
- Tailwind CSS for styling with built-in responsive design
- Axios for API communication with automatic error handling

### Backend Development
- Flask development server with auto-reload
- SQLAlchemy ORM for database operations
- Comprehensive error handling and logging
- JWT authentication with role-based access control

### Database Management
- MySQL with Unicode support
- Automated migrations and seeding
- Comprehensive schema with foreign key constraints
- Sample data for development and testing

## Testing

### Integration Testing
```bash
# Run comprehensive integration tests
python verify_integration.js
```

### Manual Testing
1. Start both frontend and backend servers
2. Login with different role accounts
3. Test CRUD operations in each module
4. Verify role-based access restrictions
5. Check dashboard analytics and reports

## Production Deployment

### Frontend Build
```bash
cd frontend
npm run build
# Deploy dist/ folder to web server
```

### Backend Deployment
- Configure production database connection
- Set secure SECRET_KEY in environment
- Use production WSGI server (e.g., Gunicorn)
- Configure reverse proxy (e.g., Nginx)

## Implementation Status

### ✅ Completed Features
- ✅ Complete Vue.js frontend with all UI components
- ✅ Full Flask backend API with database integration
- ✅ JWT authentication and role-based access control
- ✅ All CRUD operations for core entities
- ✅ Real-time dashboard with analytics
- ✅ Responsive design for mobile and desktop
- ✅ Database schema with comprehensive relationships
- ✅ Sample data initialization
- ✅ Integration testing and documentation
- ✅ Error handling and validation
- ✅ Search and filtering capabilities
- ✅ Pagination for large datasets

### 🔧 Architecture Features
- RESTful API design with consistent response formats
- Modular Flask blueprints for maintainability
- Vue.js composition API with reactive state management
- SQLAlchemy models with relationships and constraints
- Comprehensive input validation and sanitization
- CORS configuration for development and production

## Database Schema

The system includes a complete database schema with tables for:

- **Users and Roles**: Authentication and authorization
- **Products and Categories**: Product catalog management
- **Suppliers**: Vendor relationship management
- **Customers**: Customer relationship management
- **Orders and Order Items**: Sales order processing
- **Inventory and Lots**: Stock level tracking
- **Locations and Zones**: Warehouse organization
- **Shipments**: Logistics and shipping management
- **Scrap Records**: Waste and loss tracking

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify MySQL is running
   - Check database credentials in .env file
   - Ensure database exists and has proper permissions

2. **CORS Errors**
   - Verify backend is running on port 5001
   - Check CORS configuration in app.py
   - Ensure frontend uses correct API base URL

3. **Authentication Issues**
   - Clear browser cookies and local storage
   - Verify JWT secret key configuration
   - Check user credentials in database

For detailed troubleshooting, refer to `INTEGRATION_SETUP.md`.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes and add tests
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/new-feature`)
6. Create a Pull Request

---

**Note**: This is a fully functional warehouse management system with integrated frontend and backend. Both components are required for the complete application experience.
Also, all data is mocked.
