#!/usr/bin/env python3
"""
Initialize sample data for the Warehouse Management System
"""

from app import create_app
from models import db, Role, User, Product, Supplier, Customer, Location
from werkzeug.security import generate_password_hash


def init_sample_data():
    """Initialize sample data for testing"""
    app = create_app()

    with app.app_context():
        print("Creating database tables...")
        db.create_all()

        print("Creating roles...")
        roles_data = [
            {'role_name': 'Admin'},
            {'role_name': 'Sales'},
            {'role_name': 'Warehouse'}
        ]

        for role_data in roles_data:
            role = Role.query.filter_by(
                role_name=role_data['role_name']).first()
            if not role:
                role = Role(**role_data)
                db.session.add(role)

        db.session.commit()

        print("Creating users...")
        users_data = [
            {'account': 'admin', 'password': 'admin', 'role_name': 'Admin'},
            {'account': 'sales', 'password': 'sales', 'role_name': 'Sales'},
            {'account': 'warehouse', 'password': 'warehouse', 'role_name': 'Warehouse'}
        ]

        for user_data in users_data:
            user = User.query.filter_by(account=user_data['account']).first()
            if not user:
                role = Role.query.filter_by(
                    role_name=user_data['role_name']).first()
                user = User(
                    account=user_data['account'],
                    pwd_hash=generate_password_hash(user_data['password']),
                    role_id=role.role_id
                )
                db.session.add(user)

        db.session.commit()

        print("Creating suppliers...")
        suppliers_data = [
            {'supplier_name': 'Tech Supplier Inc.',
                'contact': 'tech@supplier.com'},
            {'supplier_name': 'Electronics Wholesale',
                'contact': 'sales@electronics.com'},
            {'supplier_name': 'Office Equipment Ltd.',
                'contact': 'orders@office-eq.com'}
        ]

        for supplier_data in suppliers_data:
            supplier = Supplier.query.filter_by(
                supplier_name=supplier_data['supplier_name']).first()
            if not supplier:
                supplier = Supplier(**supplier_data)
                db.session.add(supplier)

        db.session.commit()

        print("Creating products...")
        products_data = [
            {
                'name': 'Laptop Dell XPS 13',
                'category': 'Electronics',
                'warranty_years': 3,
                'image_url': 'https://example.com/dell-xps13.jpg'
            },
            {
                'name': 'Office Chair Ergonomic',
                'category': 'Furniture',
                'warranty_years': 2,
                'image_url': 'https://example.com/office-chair.jpg'
            },
            {
                'name': 'Wireless Mouse',
                'category': 'Electronics',
                'warranty_years': 1,
                'image_url': 'https://example.com/mouse.jpg'
            },
            {
                'name': 'Monitor 24 inch',
                'category': 'Electronics',
                'warranty_years': 2,
                'image_url': 'https://example.com/monitor.jpg'
            }
        ]

        for product_data in products_data:
            product = Product.query.filter_by(
                name=product_data['name']).first()
            if not product:
                product = Product(**product_data)
                db.session.add(product)

        db.session.commit()

        print("Creating customers...")
        customers_data = [
            {
                'name': 'ABC Corporation',
                'contact': 'procurement@abc-corp.com',
                'address': '123 Business St, City, State'
            },
            {
                'name': 'XYZ Ltd.',
                'contact': 'orders@xyz-ltd.com',
                'address': '456 Commerce Ave, City, State'
            },
            {
                'name': 'StartUp Inc.',
                'contact': 'admin@startup.com',
                'address': '789 Innovation Blvd, City, State'
            }
        ]

        for customer_data in customers_data:
            customer = Customer.query.filter_by(
                name=customer_data['name']).first()
            if not customer:
                customer = Customer(**customer_data)
                db.session.add(customer)

        db.session.commit()

        print("Creating locations...")
        locations_data = [
            {'zone': 'A', 'shelf': '01'},
            {'zone': 'A', 'shelf': '02'},
            {'zone': 'B', 'shelf': '01'},
            {'zone': 'B', 'shelf': '02'},
            {'zone': 'C', 'shelf': '01'}
        ]

        for location_data in locations_data:
            location = Location.query.filter_by(
                zone=location_data['zone'],
                shelf=location_data['shelf']
            ).first()
            if not location:
                location = Location(**location_data)
                db.session.add(location)

        db.session.commit()

        print("Sample data initialized successfully!")
        print("\nDemo accounts:")
        print("Admin: admin/admin")
        print("Sales: sales/sales")
        print("Warehouse: warehouse/warehouse")


if __name__ == "__main__":
    init_sample_data()
