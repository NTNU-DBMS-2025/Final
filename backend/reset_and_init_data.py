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


def reset_database():
    """Drop and recreate all tables with updated schema"""
    app = create_app()

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
            return True

        except Exception as e:
            print(f"❌ Error creating views: {str(e)}")
            return False


def main():
    """Main reset and initialization function"""
    print("🔄 Starting Database Reset and Initialization")
    print("=" * 50)

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
                print(result.stdout)
        else:
            print("❌ Data initialization failed:")
            print(result.stderr)
            return False

        # Create database views
        if not create_views():
            print("⚠️ Some views failed to create, but continuing...")

    except Exception as e:
        print(f"❌ Reset failed: {e}")
        return False

    print("\n" + "=" * 50)
    print("🎉 Database reset and initialization complete!")
    print("📊 All tables, data, and views are ready!")
    print("You can now start the Flask server and test the reports functionality.")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
