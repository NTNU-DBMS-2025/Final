# 倉儲管理系統 (Warehouse Management System)

A modern warehouse management system built with Vue.js frontend, Flask backend, and MySQL database.

## Project Overview

This is a complete warehouse management system featuring:

- **Frontend**: Vue.js 3 with Tailwind CSS
- **Backend**: Flask API with SQLAlchemy (to be implemented)
- **Database**: MySQL with provided DDL schema
- **Authentication**: JWT-based role management

## Features

- **Role-based Access Control**: Admin, Sales, Warehouse, and Shipping Vendor roles
- **Product Management**: Complete CRUD operations for products and suppliers
- **Order Management**: Track and manage customer orders and shipments
- **Inventory Management**: Real-time inventory tracking and low stock alerts
- **Responsive Design**: Built with Tailwind CSS for mobile and desktop
- **Modern UI**: Clean and intuitive user interface

## Prerequisites

Before running this project on another computer, ensure you have:

- **Node.js** (version 16.0 or higher) - [Download here](https://nodejs.org/)
- **npm** (comes with Node.js) or **yarn**
- **Git** (for cloning the repository)
- **Python 3.8+** (for backend, when implemented)
- **MySQL** (for database, when implemented)

## Quick Start - Frontend Only

### 1. Transfer the Project

**Option A: Using Git (Recommended)**
```bash
# Clone the repository
git clone <your-repository-url>
cd <project-name>
```

**Option B: Copy Files**
- Copy the entire project folder to your new computer
- Open terminal/command prompt and navigate to the project directory

### 2. Install Frontend Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install all dependencies
npm install
```

This will install all the required packages:
- Vue 3
- Vue Router 4
- Vuex 4
- Axios
- Tailwind CSS
- Vite

### 3. Start Development Server

```bash
npm run dev
```

The application will be available at: **http://localhost:5173**

### 4. Test Login Credentials

Use these test accounts to log in:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin |
| Sales | sales | sales |
| Warehouse | warehouse | warehouse |

## Project Structure

```
/
├── frontend/              # Vue.js frontend application
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── views/         # Page components
│   │   ├── router/        # Vue Router configuration
│   │   ├── store/         # Vuex store
│   │   ├── api/           # API functions (currently mocked)
│   │   └── main.js        # Application entry point
│   ├── public/            # Static assets
│   ├── tailwind.config.js # Tailwind CSS configuration
│   ├── vite.config.js     # Vite configuration
│   └── package.json       # Frontend dependencies
├── backend/               # Flask backend (to be implemented)
├── ddl.sql               # Database schema
└── README.md             # This file
```

## Available Scripts (Frontend)

```bash
cd frontend

# Development
npm run dev          # Start development server with hot reload
npm run build        # Build for production
npm run preview      # Preview production build locally
npm run serve        # Alternative dev server command
```

## Development Tips

### Hot Reload
The development server includes hot reload - changes to your code will automatically update in the browser.

### Browser Developer Tools
- Install Vue.js devtools browser extension for debugging
- Use browser's developer tools for inspecting network requests and console logs

### Code Editing
Recommended VS Code extensions:
- Volar (Vue Language Features)
- Tailwind CSS IntelliSense
- Auto Rename Tag
- Bracket Pair Colorizer

## Troubleshooting

### Port Already in Use
If port 5173 is busy, Vite will automatically use the next available port (5174, 5175, etc.)

### Dependencies Issues
```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Build Issues
```bash
# Check for syntax errors
cd frontend
npm run build
```

## Production Build

To build the frontend for production:

```bash
cd frontend
npm run build
```

This creates a `dist/` folder with optimized files ready for deployment.

## Backend Setup (Future Implementation)

The backend Flask API and MySQL database will be implemented in future phases:

1. **Flask API**: RESTful endpoints matching the frontend requirements
2. **SQLAlchemy Models**: Based on the provided DDL schema
3. **JWT Authentication**: Real authentication replacing mock system
4. **Database Integration**: MySQL connection with proper migrations

## Current Implementation Status

### ✅ Completed
- Complete Vue.js frontend with all UI components
- Role-based navigation and access control
- CRUD operations with mock data
- Responsive design with Tailwind CSS
- Authentication flow (mocked)
- Product and supplier management
- Order and inventory management interfaces
- Dashboard views for all user roles

### ⏳ To Do
- Flask backend API implementation
- MySQL database integration
- Real JWT authentication
- API endpoint integration
- Data persistence
- Production deployment

## Database Schema

The project includes a complete DDL schema (`ddl.sql`) with tables for:
- Users and Roles
- Products and Suppliers
- Customers and Orders
- Inventory and Locations
- Shipments and Scrap management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of a database management system course assignment.

---

For questions or issues, refer to the documentation:
- [Vue.js Guide](https://vuejs.org/guide/)
- [Vite Documentation](https://vitejs.dev/guide/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/) (for future backend work)
