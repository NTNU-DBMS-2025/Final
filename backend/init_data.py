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
            {
                'supplier_name': 'Tech Supplier Inc.',
                'contact_name': 'John Smith',
                'phone': '02-2123-4567',
                'email': 'tech@supplier.com',
                'address': '123 Tech Street, Taipei, Taiwan',
                'supplier_type': 'manufacturer',
                'status': 'active',
                'notes': 'Primary technology supplier for laptops and computers'
            },
            {
                'supplier_name': 'Electronics Wholesale',
                'contact_name': 'Sarah Chen',
                'phone': '04-2456-7890',
                'email': 'sales@electronics.com',
                'address': '456 Electronics Blvd, Taichung, Taiwan',
                'supplier_type': 'wholesaler',
                'status': 'active',
                'notes': 'Wholesale electronics and accessories'
            },
            {
                'supplier_name': 'Office Equipment Ltd.',
                'contact_name': 'Mike Wang',
                'phone': '07-789-0123',
                'email': 'orders@office-eq.com',
                'address': '789 Office Park, Kaohsiung, Taiwan',
                'supplier_type': 'distributor',
                'status': 'active',
                'notes': 'Office furniture and equipment distributor'
            },
            {
                'supplier_name': 'Global Components Co.',
                'contact_name': 'Lisa Liu',
                'phone': '03-321-6547',
                'email': 'info@globalcomp.com',
                'address': '321 Component Ave, Taoyuan, Taiwan',
                'supplier_type': 'manufacturer',
                'status': 'active',
                'notes': 'Global supplier of electronic components'
            },
            {
                'supplier_name': 'Premium Hardware Store',
                'contact_name': 'David Huang',
                'phone': '05-654-9870',
                'email': 'sales@premiumhw.com',
                'address': '654 Premium St, Chiayi, Taiwan',
                'supplier_type': 'distributor',
                'status': 'active',
                'notes': 'Premium hardware and gaming equipment'
            },
            {
                'supplier_name': 'Digital Solutions Provider',
                'contact_name': 'Emma Lin',
                'phone': '08-987-1234',
                'email': 'orders@digitalsol.com',
                'address': '987 Digital Road, Pingtung, Taiwan',
                'supplier_type': 'service',
                'status': 'active',
                'notes': 'Digital solutions and software services'
            }
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
                'name': 'Wireless Mouse Logitech',
                'category': 'Electronics',
                'warranty_years': 1,
                'image_url': 'https://example.com/mouse.jpg'
            },
            {
                'name': 'Monitor 24 inch LG',
                'category': 'Electronics',
                'warranty_years': 2,
                'image_url': 'https://example.com/monitor.jpg'
            },
            {
                'name': 'iPhone 15 Pro',
                'category': 'Electronics',
                'warranty_years': 1,
                'image_url': 'https://example.com/iphone15.jpg'
            },
            {
                'name': 'MacBook Pro M3',
                'category': 'Electronics',
                'warranty_years': 3,
                'image_url': 'https://example.com/macbook.jpg'
            },
            {
                'name': 'Standing Desk',
                'category': 'Furniture',
                'warranty_years': 5,
                'image_url': 'https://example.com/standing-desk.jpg'
            },
            {
                'name': 'Wireless Keyboard',
                'category': 'Electronics',
                'warranty_years': 2,
                'image_url': 'https://example.com/keyboard.jpg'
            },
            {
                'name': 'Conference Table',
                'category': 'Furniture',
                'warranty_years': 10,
                'image_url': 'https://example.com/conference-table.jpg'
            },
            {
                'name': 'Printer HP LaserJet',
                'category': 'Electronics',
                'warranty_years': 2,
                'image_url': 'https://example.com/printer.jpg'
            },
            {
                'name': 'Gaming Chair',
                'category': 'Furniture',
                'warranty_years': 3,
                'image_url': 'https://example.com/gaming-chair.jpg'
            },
            {
                'name': 'Tablet iPad Air',
                'category': 'Electronics',
                'warranty_years': 1,
                'image_url': 'https://example.com/ipad.jpg'
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
                'address': '123 Business St, New York, NY 10001'
            },
            {
                'name': 'XYZ Ltd.',
                'contact': 'orders@xyz-ltd.com',
                'address': '456 Commerce Ave, Los Angeles, CA 90210'
            },
            {
                'name': 'StartUp Inc.',
                'contact': 'admin@startup.com',
                'address': '789 Innovation Blvd, San Francisco, CA 94105'
            },
            {
                'name': 'Tech Solutions Corp',
                'contact': 'purchasing@techsol.com',
                'address': '321 Tech Park Dr, Austin, TX 78701'
            },
            {
                'name': 'Modern Office Systems',
                'contact': 'orders@modernoffice.com',
                'address': '654 Corporate Way, Seattle, WA 98101'
            },
            {
                'name': 'Digital Dynamics LLC',
                'contact': 'procurement@digitaldyn.com',
                'address': '987 Future Rd, Boston, MA 02101'
            },
            {
                'name': 'Green Energy Co.',
                'contact': 'supplies@greenenergy.com',
                'address': '147 Sustainability Ave, Portland, OR 97201'
            },
            {
                'name': 'Education First Academy',
                'contact': 'admin@edufirst.edu',
                'address': '258 Learning Lane, Chicago, IL 60601'
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
            {'zone': 'A', 'shelf': '03'},
            {'zone': 'B', 'shelf': '01'},
            {'zone': 'B', 'shelf': '02'},
            {'zone': 'B', 'shelf': '03'},
            {'zone': 'C', 'shelf': '01'},
            {'zone': 'C', 'shelf': '02'},
            {'zone': 'D', 'shelf': '01'},
            {'zone': 'D', 'shelf': '02'},
            {'zone': 'E', 'shelf': '01'},
            {'zone': 'E', 'shelf': '02'}
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

        # Create product-supplier relationships
        print("Creating product-supplier relationships...")
        try:
            # Get some products and suppliers to create relationships
            laptop_dell = Product.query.filter_by(
                name='Laptop Dell XPS 13').first()
            macbook = Product.query.filter_by(name='MacBook Pro M3').first()
            iphone = Product.query.filter_by(name='iPhone 15 Pro').first()
            mouse = Product.query.filter_by(
                name='Wireless Mouse Logitech').first()
            monitor = Product.query.filter_by(
                name='Monitor 24 inch LG').first()
            office_chair = Product.query.filter_by(
                name='Office Chair Ergonomic').first()

            tech_supplier = Supplier.query.filter_by(
                supplier_name='Tech Supplier Inc.').first()
            electronics_wholesale = Supplier.query.filter_by(
                supplier_name='Electronics Wholesale').first()
            office_equipment = Supplier.query.filter_by(
                supplier_name='Office Equipment Ltd.').first()
            global_components = Supplier.query.filter_by(
                supplier_name='Global Components Co.').first()

            # Create relationships
            if tech_supplier and laptop_dell:
                tech_supplier.products.append(laptop_dell)
            if tech_supplier and macbook:
                tech_supplier.products.append(macbook)
            if electronics_wholesale and iphone:
                electronics_wholesale.products.append(iphone)
            if electronics_wholesale and mouse:
                electronics_wholesale.products.append(mouse)
            if global_components and monitor:
                global_components.products.append(monitor)
            if office_equipment and office_chair:
                office_equipment.products.append(office_chair)

            db.session.commit()
            print("Product-supplier relationships created!")

        except Exception as e:
            print(f"Error creating relationships: {e}")
            db.session.rollback()

        # Create some inventory data
        print("Creating inventory data...")
        try:
            from models import InventoryLot
            from datetime import date, timedelta

            inventory_data = [
                {'product_name': 'Laptop Dell XPS 13', 'zone': 'A',
                    'shelf': '01', 'quantity': 25, 'days_to_expiry': 365},
                {'product_name': 'iPhone 15 Pro', 'zone': 'A',
                    'shelf': '02', 'quantity': 50, 'days_to_expiry': 180},
                {'product_name': 'MacBook Pro M3', 'zone': 'B',
                    'shelf': '01', 'quantity': 15, 'days_to_expiry': 365},
                {'product_name': 'Wireless Mouse Logitech', 'zone': 'B',
                    'shelf': '02', 'quantity': 100, 'days_to_expiry': 90},
                {'product_name': 'Monitor 24 inch LG', 'zone': 'C',
                    'shelf': '01', 'quantity': 30, 'days_to_expiry': 180},
                {'product_name': 'Office Chair Ergonomic', 'zone': 'D',
                    'shelf': '01', 'quantity': 8, 'days_to_expiry': None},
                {'product_name': 'Standing Desk', 'zone': 'D',
                    'shelf': '02', 'quantity': 5, 'days_to_expiry': None},
                {'product_name': 'Wireless Keyboard', 'zone': 'A',
                    'shelf': '03', 'quantity': 60, 'days_to_expiry': 120},
                {'product_name': 'Tablet iPad Air', 'zone': 'B',
                    'shelf': '03', 'quantity': 20, 'days_to_expiry': 90},
                {'product_name': 'Printer HP LaserJet', 'zone': 'E',
                    'shelf': '01', 'quantity': 12, 'days_to_expiry': 365}
            ]

            for inv_data in inventory_data:
                product = Product.query.filter_by(
                    name=inv_data['product_name']).first()
                location = Location.query.filter_by(
                    zone=inv_data['zone'], shelf=inv_data['shelf']).first()

                if product and location:
                    # Check if inventory lot already exists
                    existing_lot = InventoryLot.query.filter_by(
                        product_id=product.product_id,
                        location_id=location.location_id
                    ).first()

                    if not existing_lot:
                        expiry_date = None
                        if inv_data['days_to_expiry']:
                            expiry_date = date.today() + \
                                timedelta(days=inv_data['days_to_expiry'])

                        inventory_lot = InventoryLot(
                            product_id=product.product_id,
                            location_id=location.location_id,
                            quantity=inv_data['quantity'],
                            expiry_date=expiry_date
                        )
                        db.session.add(inventory_lot)

            db.session.commit()
            print("Inventory data created!")

        except Exception as e:
            print(f"Error creating inventory: {e}")
            db.session.rollback()

        print("\n🎉 Enhanced sample data initialized successfully!")
        print("\n📊 Database now contains:")
        print(f"- {User.query.count()} Users")
        print(f"- {Role.query.count()} Roles")
        print(f"- {Product.query.count()} Products")
        print(f"- {Supplier.query.count()} Suppliers")
        print(f"- {Customer.query.count()} Customers")
        print(f"- {Location.query.count()} Locations")
        try:
            from models import InventoryLot
            print(f"- {InventoryLot.query.count()} Inventory Lots")
        except:
            print("- Inventory lots: N/A")

        print("\n🔑 Demo accounts:")
        print("Admin: admin/admin")
        print("Sales: sales/sales")
        print("Warehouse: warehouse/warehouse")


if __name__ == "__main__":
    init_sample_data()
