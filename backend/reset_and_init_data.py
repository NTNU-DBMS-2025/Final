#!/usr/bin/env python3
"""
Reset and initialize all data for the Warehouse Management System
This script safely clears existing data and reinitializes fresh sample data
"""

from app import create_app
from models import db
import subprocess
import sys


def reset_database():
    """Drop and recreate all tables with updated schema"""
    app = create_app()

    with app.app_context():
        print("🗑️  Dropping all tables...")
        db.drop_all()

        print("🏗️  Creating fresh tables with updated schema...")
        db.create_all()

        print("✅ Database reset completed with updated Order schema!")


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
            print(result.stdout)
        else:
            print("❌ Data initialization failed:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"❌ Reset failed: {e}")
        return False

    print("\n" + "=" * 50)
    print("🎉 Database reset and initialization complete!")
    print("You can now start the Flask server and test the application.")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
