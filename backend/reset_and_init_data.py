#!/usr/bin/env python3
"""
Reset and initialize all data for the Warehouse Management System
This script safely clears existing data and reinitializes fresh sample data
"""

from app import create_app
from models import db
import subprocess
import sys
import os
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()



def reset_database():
    """Drop and recreate all tables with updated schema"""
    app = create_app()
    # show which database is being used
    print(f"Using database: {os.getenv('DATABASE_URL')}")

    with app.app_context():
        print("🗑️  Dropping all tables...")
        db.drop_all()

        print("🏗️  Creating fresh tables with updated schema...")
        db.create_all()

        print("✅ Database reset completed with updated Order schema!")


def create_views():
    """Create all database views from views.sql"""
    app = create_app()

    with app.app_context():
        try:
            print("\n🔍 Creating database views...")
            views_file = os.path.join(os.path.dirname(__file__), 'views.sql')

            if not os.path.exists(views_file):
                print(f"❌ Views file not found: {views_file}")
                return False

            with open(views_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()

            # Split the content by view creation statements
            statements = []
            current_statement = ""
            in_comment_block = False

            for line in sql_content.split('\n'):
                line = line.strip()

                # Handle multi-line comments
                if line.startswith('/*'):
                    in_comment_block = True
                if line.endswith('*/'):
                    in_comment_block = False
                    continue
                if in_comment_block:
                    continue

                # Skip single-line comments and empty lines
                if line.startswith('--') or not line:
                    continue

                current_statement += line + "\n"

                # Check if this line ends a view definition
                if line.endswith(';'):
                    if 'CREATE OR REPLACE VIEW' in current_statement:
                        statements.append(current_statement.strip())
                    current_statement = ""

            print(f"📊 Found {len(statements)} views to create")

            # Execute each view creation statement
            success_count = 0
            failed_views = []

            for i, statement in enumerate(statements, 1):
                try:
                    # Extract view name for logging
                    view_name = "unknown"
                    if "CREATE OR REPLACE VIEW" in statement:
                        parts = statement.split("CREATE OR REPLACE VIEW")[
                            1].split("AS")[0].strip()
                        view_name = parts.split()[0]

                    db.session.execute(text(statement))
                    db.session.commit()
                    success_count += 1
                    print(f"✅ Created view {i}/{len(statements)}: {view_name}")

                except Exception as e:
                    print(f"❌ Error creating view {view_name}: {str(e)}")
                    failed_views.append((view_name, str(e)))
                    db.session.rollback()
                    continue

            print(
                f"🎉 Successfully created {success_count}/{len(statements)} views!")

            if failed_views:
                print(f"⚠️ Failed to create {len(failed_views)} views:")
                for view_name, error in failed_views:
                    print(f"   - {view_name}: {error}")

            return len(failed_views) == 0

        except Exception as e:
            print(f"❌ Error creating views: {str(e)}")
            return False


def test_reports_functionality():
    """Test basic reports functionality to ensure everything works"""
    app = create_app()

    with app.app_context():
        try:
            print("\n🧪 Testing reports functionality...")

            # Import the reports function
            try:
                from reports import execute_view_query
            except ImportError:
                print("❌ Could not import reports module")
                return False

            # Test a few key views
            test_views = [
                ('v_inventory_expired', 'Expired inventory'),
                ('v_orders_pending', 'Pending orders'),
                ('v_sales_30d', '30-day sales'),
                ('v_scrap_cost_month', 'Monthly scrap cost'),
                ('v_locations_over_capacity', 'Over capacity locations')
            ]

            success_count = 0
            for view_name, description in test_views:
                try:
                    result = execute_view_query(view_name)
                    print(f"✅ {description}: {len(result)} records")
                    success_count += 1
                except Exception as e:
                    print(f"❌ {description}: {str(e)}")

            print(
                f"🎯 Reports test result: {success_count}/{len(test_views)} views working")
            return success_count == len(test_views)

        except Exception as e:
            print(f"❌ Error testing reports: {str(e)}")
            return False


def print_database_summary():
    """Print a summary of the database contents"""
    app = create_app()

    with app.app_context():
        try:
            print("\n📊 Database Summary:")
            print("=" * 40)

            # Get counts for each major table
            from models import User, Role, Product, Supplier, Customer, Location

            counts = {
                'Users': User.query.count(),
                'Roles': Role.query.count(),
                'Products': Product.query.count(),
                'Suppliers': Supplier.query.count(),
                'Customers': Customer.query.count(),
                'Locations': Location.query.count()
            }

            # Try to get counts for other models that might not always exist
            try:
                from models import InventoryLot, Scrap, Order, OrderItem, ShippingVendor, Shipment
                counts.update({
                    'Inventory Lots': InventoryLot.query.count(),
                    'Scrap Records': Scrap.query.count(),
                    'Orders': Order.query.count(),
                    'Order Items': OrderItem.query.count(),
                    'Shipping Vendors': ShippingVendor.query.count(),
                    'Shipments': Shipment.query.count()
                })
            except (ImportError, Exception):
                pass

            for item, count in counts.items():
                print(f"- {item}: {count}")

        except Exception as e:
            print(f"❌ Error getting database summary: {str(e)}")


def print_demo_accounts():
    """Print demo account information"""
    print("\n🔑 Demo Accounts:")
    print("=" * 40)
    print("Admin Accounts:")
    print("  - admin/admin")
    print("  - admin2/admin123")
    print("\nSales Accounts:")
    print("  - sales/sales")
    print("  - sales_manager/sales123")
    print("  - sales_rep1/sales123")
    print("  - sales_rep2/sales123")
    print("\nWarehouse Accounts:")
    print("  - warehouse/warehouse")
    print("  - warehouse_super/warehouse123")
    print("  - warehouse_staff1/warehouse123")
    print("  - warehouse_staff2/warehouse123")
    print("  - warehouse_staff3/warehouse123")


def print_available_endpoints():
    """Print available API endpoints"""
    print("\n🌐 Available API Endpoints:")
    print("=" * 40)
    print("Health Check:")
    print("  - GET /api/health")
    print("\nReports (Summary):")
    print("  - GET /api/reports/summary/inventory")
    print("  - GET /api/reports/summary/sales")
    print("  - GET /api/reports/summary/orders")
    print("  - GET /api/reports/summary/financial")
    print("\nInventory Reports:")
    print("  - GET /api/reports/inventory/expired")
    print("  - GET /api/reports/inventory/low-stock")
    print("  - GET /api/reports/inventory/out-of-stock")
    print("\nSales Reports:")
    print("  - GET /api/reports/sales/30d")
    print("  - GET /api/reports/sales/fast-moving-top10")
    print("\nOrder Reports:")
    print("  - GET /api/reports/orders/pending")
    print("  - GET /api/reports/orders/delayed-shipping")
    print(
        f"\n🖥️ Frontend URL: {os.getenv('FRONTEND_URL', 'http://localhost:5173')}")
    print(
        f"🔧 Backend URL: {os.getenv('BACKEND_URL', 'http://localhost:5000')}")


def main():
    """Main reset and initialization function"""
    print("🔄 Starting Database Reset and Initialization")
    print("=" * 60)

    try:
        # Reset the database
        reset_database()

        # Run the initialization script
        print("\n📦 Running data initialization...")
        result = subprocess.run([sys.executable, 'init_data.py'],
                                capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Data initialization completed successfully!")
            if result.stdout:
                # Print only the last few lines to avoid overwhelming output
                lines = result.stdout.strip().split('\n')
                if len(lines) > 10:
                    print("...")
                    for line in lines[-10:]:
                        print(line)
                else:
                    print(result.stdout)
        else:
            print("❌ Data initialization failed:")
            if result.stderr:
                print(result.stderr)
            return False

        # Create database views
        views_success = create_views()
        if not views_success:
            print("⚠️ Some views failed to create, but continuing...")

        # Test reports functionality
        test_success = test_reports_functionality()
        if not test_success:
            print("⚠️ Some reports may have issues, but setup completed")

        # Print summary information
        print_database_summary()
        print_demo_accounts()
        print_available_endpoints()

    except Exception as e:
        print(f"❌ Reset failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("🎉 Database reset and initialization complete!")
    print("📊 All tables, data, and views are ready!")
    print("🚀 You can now start the Flask server and test the reports functionality.")
    print("\nNext steps:")
    print("1. Start backend: cd backend && python app.py")
    print("2. Start frontend: cd frontend && npm run dev")
    print("3. Access reports: http://localhost:5173/reports")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
