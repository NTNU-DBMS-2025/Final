#!/usr/bin/env python3
"""
Database Migration Script for Scrap Table
Adds new columns to existing Scrap table
"""

from app import create_app
from models import db
import pymysql


def migrate_scrap_table():
    """Add new columns to the Scrap table"""
    app = create_app()

    with app.app_context():
        try:
            # Get database connection
            connection = db.engine.raw_connection()
            cursor = connection.cursor()

            print("🔄 Migrating Scrap table...")

            # Check if columns already exist
            cursor.execute("DESCRIBE Scrap")
            existing_columns = [row[0] for row in cursor.fetchall()]

            # Add missing columns
            migrations = [
                ("status", "ALTER TABLE Scrap ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT '待處理'"),
                ("estimated_value",
                 "ALTER TABLE Scrap ADD COLUMN estimated_value DECIMAL(10,2) DEFAULT 0.00"),
                ("description", "ALTER TABLE Scrap ADD COLUMN description TEXT"),
                ("created_by", "ALTER TABLE Scrap ADD COLUMN created_by VARCHAR(100)"),
                ("processed_date", "ALTER TABLE Scrap ADD COLUMN processed_date DATE"),
                ("created_at", "ALTER TABLE Scrap ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"),
                ("updated_at", "ALTER TABLE Scrap ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
            ]

            for column_name, sql in migrations:
                if column_name not in existing_columns:
                    print(f"   Adding column: {column_name}")
                    cursor.execute(sql)
                else:
                    print(f"   Column {column_name} already exists, skipping")

            # Add indexes
            try:
                cursor.execute(
                    "CREATE INDEX idx_scrap_status ON Scrap(status)")
                print("   Added index: idx_scrap_status")
            except pymysql.err.OperationalError as e:
                if "Duplicate key name" in str(e):
                    print("   Index idx_scrap_status already exists, skipping")
                else:
                    print(f"   Error adding index: {e}")

            try:
                cursor.execute(
                    "CREATE INDEX idx_scrap_date ON Scrap(scrap_date)")
                print("   Added index: idx_scrap_date")
            except pymysql.err.OperationalError as e:
                if "Duplicate key name" in str(e):
                    print("   Index idx_scrap_date already exists, skipping")
                else:
                    print(f"   Error adding index: {e}")

            connection.commit()
            print("✅ Scrap table migration completed successfully!")

            # Show updated table structure
            cursor.execute("DESCRIBE Scrap")
            columns = cursor.fetchall()
            print("\n📋 Updated Scrap table structure:")
            for column in columns:
                print(f"   {column[0]}: {column[1]}")

            cursor.close()
            connection.close()

        except Exception as e:
            print(f"❌ Migration failed: {e}")
            raise


def main():
    """Main migration function"""
    print("🛠️  Starting Database Migration")
    print("=" * 40)

    migrate_scrap_table()

    print("\n" + "=" * 40)
    print("🎉 Migration completed!")
    print("Now you can run: python init_data.py")


if __name__ == "__main__":
    main()
