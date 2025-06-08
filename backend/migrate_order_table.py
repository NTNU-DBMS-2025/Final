import mysql.connector
from datetime import datetime
import random
import string


def generate_order_number():
    """Generate a unique order number"""
    timestamp = datetime.now().strftime("%Y%m%d")
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"ORD{timestamp}{random_suffix}"


def migrate_order_table():
    # Database connection
    config = {
        'user': 'root',
        'password': 'password',
        'host': 'localhost',
        'database': 'DBMS',
        'raise_on_warnings': True
    }

    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        print("🔄 Starting Order table migration...")

        # 1. Add new columns to Order table
        print("📝 Adding new columns to Order table...")

        # Add order_number column
        try:
            cursor.execute(
                "ALTER TABLE `Order` ADD COLUMN order_number VARCHAR(50) UNIQUE AFTER order_id;")
            print("✅ Added order_number column")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e):
                print("⚠️ order_number column already exists")
            else:
                raise e

        # Add expected_delivery_date column
        try:
            cursor.execute(
                "ALTER TABLE `Order` ADD COLUMN expected_delivery_date DATE AFTER order_date;")
            print("✅ Added expected_delivery_date column")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e):
                print("⚠️ expected_delivery_date column already exists")
            else:
                raise e

        # Add priority column
        try:
            cursor.execute(
                "ALTER TABLE `Order` ADD COLUMN priority VARCHAR(20) NOT NULL DEFAULT 'normal' AFTER status;")
            print("✅ Added priority column")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e):
                print("⚠️ priority column already exists")
            else:
                raise e

        # Add total_amount column
        try:
            cursor.execute(
                "ALTER TABLE `Order` ADD COLUMN total_amount DECIMAL(12,2) DEFAULT 0.00 AFTER ship_to;")
            print("✅ Added total_amount column")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e):
                print("⚠️ total_amount column already exists")
            else:
                raise e

        # Add notes column
        try:
            cursor.execute(
                "ALTER TABLE `Order` ADD COLUMN notes TEXT AFTER total_amount;")
            print("✅ Added notes column")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e):
                print("⚠️ notes column already exists")
            else:
                raise e

        # Add created_at column
        try:
            cursor.execute(
                "ALTER TABLE `Order` ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP AFTER user_id;")
            print("✅ Added created_at column")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e):
                print("⚠️ created_at column already exists")
            else:
                raise e

        # Add updated_at column
        try:
            cursor.execute(
                "ALTER TABLE `Order` ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER created_at;")
            print("✅ Added updated_at column")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e):
                print("⚠️ updated_at column already exists")
            else:
                raise e

        # 2. Update existing orders with order_number if null
        print("📝 Updating existing orders with order numbers...")
        cursor.execute(
            "SELECT order_id FROM `Order` WHERE order_number IS NULL")
        orders_without_number = cursor.fetchall()

        for (order_id,) in orders_without_number:
            order_number = generate_order_number()
            cursor.execute(
                "UPDATE `Order` SET order_number = %s WHERE order_id = %s", (order_number, order_id))

        if orders_without_number:
            print(
                f"✅ Updated {len(orders_without_number)} orders with order numbers")

        # 3. Add indexes
        print("📝 Adding indexes...")
        indexes = [
            ("idx_order_number", "order_number"),
            ("idx_order_status", "status"),
            ("idx_order_priority", "priority"),
            ("idx_order_date", "order_date")
        ]

        for index_name, column in indexes:
            try:
                cursor.execute(
                    f"CREATE INDEX {index_name} ON `Order` ({column});")
                print(f"✅ Added index {index_name}")
            except mysql.connector.Error as e:
                if "Duplicate key name" in str(e):
                    print(f"⚠️ Index {index_name} already exists")
                else:
                    raise e

        # 4. Add unit_price column to Order_Item table
        print("📝 Adding unit_price column to Order_Item table...")
        try:
            cursor.execute(
                "ALTER TABLE Order_Item ADD COLUMN unit_price DECIMAL(10,2) NOT NULL DEFAULT 0.00 AFTER quantity;")
            print("✅ Added unit_price column to Order_Item")
        except mysql.connector.Error as e:
            if "Duplicate column name" in str(e):
                print("⚠️ unit_price column already exists in Order_Item")
            else:
                raise e

        # 5. Update status default value
        try:
            cursor.execute(
                "ALTER TABLE `Order` MODIFY COLUMN status VARCHAR(50) NOT NULL DEFAULT 'pending';")
            print("✅ Updated status column default value")
        except mysql.connector.Error as e:
            print(f"⚠️ Could not update status default: {e}")

        connection.commit()
        print("✅ Order table migration completed successfully!")

        # Display current table structure
        print("\n📋 Current Order table structure:")
        cursor.execute("DESCRIBE `Order`;")
        for row in cursor.fetchall():
            print(
                f"  {row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]}")

        print("\n📋 Current Order_Item table structure:")
        cursor.execute("DESCRIBE Order_Item;")
        for row in cursor.fetchall():
            print(
                f"  {row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]}")

    except mysql.connector.Error as error:
        print(f"❌ Migration failed: {error}")
        if connection:
            connection.rollback()
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        if connection:
            connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Database connection closed.")


if __name__ == "__main__":
    migrate_order_table()
