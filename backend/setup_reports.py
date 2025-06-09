#!/usr/bin/env python3
"""
Complete setup script for the Warehouse Management System Reports
This script initializes the database, creates tables, adds sample data, and creates all report views
"""

import subprocess
import sys
import os
from app import create_app
from models import db
from sqlalchemy import text


def run_database_setup():
    """Run the complete database setup process"""
    print("🚀 Starting Complete Database Setup for Reports System")
    print("=" * 60)

    try:
        # Step 1: Reset and initialize the database with sample data
        print("\n📦 Step 1: Resetting database and initializing sample data...")
        result = subprocess.run([sys.executable, 'reset_and_init_data.py'],
                                capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Database reset and data initialization completed!")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Database initialization failed:")
            if result.stderr:
                print(result.stderr)
            return False

        # Step 2: Create all report views
        print("\n🔍 Step 2: Creating all report views...")
        if create_all_views():
            print("✅ All report views created successfully!")
        else:
            print("⚠️ Some views failed to create")

        # Step 3: Test the reports API
        print("\n🧪 Step 3: Testing reports functionality...")
        if test_reports_api():
            print("✅ Reports API is working correctly!")
        else:
            print("⚠️ Some reports may have issues")

    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("🎉 Reports System Setup Complete!")
    print("\n📊 Available Report Endpoints:")
    print("- /api/reports/inventory/expired")
    print("- /api/reports/inventory/low-stock")
    print("- /api/reports/sales/30d")
    print("- /api/reports/orders/pending")
    print("- /api/reports/summary/inventory")
    print("- /api/reports/summary/sales")
    print("- /api/reports/summary/orders")
    print("- /api/reports/summary/financial")
    print("\n🌐 Frontend Reports: http://localhost:5173/reports")
    print("🔧 Backend API: http://localhost:5001/api/reports")

    return True


def create_all_views():
    """Create all database views from views.sql"""
    app = create_app()

    with app.app_context():
        try:
            views_file = os.path.join(os.path.dirname(__file__), 'views.sql')

            with open(views_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()

            # Split the content by view creation statements
            statements = []
            current_statement = ""

            for line in sql_content.split('\n'):
                line = line.strip()

                # Skip comments and empty lines
                if line.startswith('/*') or line.startswith('--') or not line:
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
                    db.session.rollback()
                    continue

            print(
                f"🎉 Successfully created {success_count}/{len(statements)} views!")
            return success_count == len(statements)

        except Exception as e:
            print(f"❌ Error creating views: {str(e)}")
            return False


def test_reports_api():
    """Test basic reports functionality"""
    app = create_app()

    with app.app_context():
        try:
            from reports import execute_view_query

            # Test a few key views
            test_views = [
                'v_inventory_expired',
                'v_orders_pending',
                'v_sales_30d',
                'v_scrap_cost_month'
            ]

            success_count = 0
            for view_name in test_views:
                try:
                    result = execute_view_query(view_name)
                    print(f"✅ {view_name}: {len(result)} records")
                    success_count += 1
                except Exception as e:
                    print(f"❌ {view_name}: {str(e)}")

            return success_count == len(test_views)

        except Exception as e:
            print(f"❌ Error testing reports: {str(e)}")
            return False


if __name__ == '__main__':
    run_database_setup()
