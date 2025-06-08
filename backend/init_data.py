#!/usr/bin/env python3
"""
Initialize sample data for the Warehouse Management System
"""

from app import create_app
from models import db, Role, User, Product, Supplier, Customer, Location, InventoryLot
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
                'name': '台積電股份有限公司',
                'contact': '林經理',
                'phone': '03-5636688',
                'email': 'manager@tsmc.com',
                'address': '新竹市力行三路8號',
                'customer_type': 'business',
                'customer_level': 'platinum',
                'tax_id': '11883105',
                'status': 'active',
                'notes': 'VIP客戶，半導體龍頭企業'
            },
            {
                'name': '鴻海精密工業股份有限公司',
                'contact': '陳副理',
                'phone': '02-22680013',
                'email': 'procurement@foxconn.com',
                'address': '新北市土城區中山路66號',
                'customer_type': 'business',
                'customer_level': 'gold',
                'tax_id': '04128089',
                'status': 'active',
                'notes': '長期合作夥伴，電子製造服務'
            },
            {
                'name': '張小明',
                'contact': '張小明',
                'phone': '0912-345-678',
                'email': 'xiaoming@gmail.com',
                'address': '台北市大安區敦化南路二段77號',
                'customer_type': 'individual',
                'customer_level': 'silver',
                'tax_id': '',
                'status': 'active',
                'notes': '個人客戶，定期採購辦公用品'
            },
            {
                'name': '台灣大學',
                'contact': '王教授',
                'phone': '02-33662001',
                'email': 'admin@ntu.edu.tw',
                'address': '台北市大安區羅斯福路四段一號',
                'customer_type': 'educational',
                'customer_level': 'gold',
                'tax_id': '03722103',
                'status': 'active',
                'notes': '教育採購，研究設備需求'
            },
            {
                'name': '台北市政府',
                'contact': '李科長',
                'phone': '02-27208889',
                'email': 'procurement@gov.taipei',
                'address': '台北市信義區市府路1號',
                'customer_type': 'government',
                'customer_level': 'gold',
                'tax_id': '03722103',
                'status': 'active',
                'notes': '政府採購，需要完整發票'
            },
            {
                'name': '聯發科技股份有限公司',
                'contact': '黃經理',
                'phone': '03-5670766',
                'email': 'supply@mediatek.com',
                'address': '新竹市東區力行路1號',
                'customer_type': 'business',
                'customer_level': 'platinum',
                'tax_id': '12345678',
                'status': 'active',
                'notes': 'IC設計公司，高科技設備需求'
            },
            {
                'name': '王美麗',
                'contact': '王美麗',
                'phone': '0987-654-321',
                'email': 'meili.wang@email.com',
                'address': '高雄市前金區中正四路211號',
                'customer_type': 'individual',
                'customer_level': 'bronze',
                'tax_id': '',
                'status': 'active',
                'notes': '新客戶，小量採購'
            },
            {
                'name': '停用測試公司',
                'contact': '測試聯絡人',
                'phone': '02-12345678',
                'email': 'test@inactive.com',
                'address': '測試地址',
                'customer_type': 'business',
                'customer_level': 'bronze',
                'tax_id': '99999999',
                'status': 'inactive',
                'notes': '測試用停用客戶'
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
            {
                'location_code': 'A1-01',
                'location_name': 'A區第1排第1位',
                'zone': 'A',
                'shelf': '01',
                'location_type': 'storage',
                'capacity': 100,
                'status': 'active',
                'notes': '主要儲存區域'
            },
            {
                'location_code': 'A1-02',
                'location_name': 'A區第1排第2位',
                'zone': 'A',
                'shelf': '02',
                'location_type': 'storage',
                'capacity': 100,
                'status': 'active',
                'notes': '標準儲存位置'
            },
            {
                'location_code': 'A1-03',
                'location_name': 'A區第1排第3位',
                'zone': 'A',
                'shelf': '03',
                'location_type': 'storage',
                'capacity': 80,
                'status': 'active',
                'notes': '小型物品儲存'
            },
            {
                'location_code': 'B2-01',
                'location_name': 'B區第2排第1位',
                'zone': 'B',
                'shelf': '01',
                'location_type': 'picking',
                'capacity': 60,
                'status': 'active',
                'notes': '揀貨專用區域'
            },
            {
                'location_code': 'B2-02',
                'location_name': 'B區第2排第2位',
                'zone': 'B',
                'shelf': '02',
                'location_type': 'storage',
                'capacity': 90,
                'status': 'active',
                'notes': '中型物品儲存'
            },
            {
                'location_code': 'B2-15',
                'location_name': 'B區第2排第15位',
                'zone': 'B',
                'shelf': '15',
                'location_type': 'picking',
                'capacity': 50,
                'status': 'occupied',
                'notes': '揀貨專用區'
            },
            {
                'location_code': 'C3-01',
                'location_name': 'C區第3排第1位',
                'zone': 'C',
                'shelf': '01',
                'location_type': 'receiving',
                'capacity': 120,
                'status': 'active',
                'notes': '收貨暫存區'
            },
            {
                'location_code': 'C3-02',
                'location_name': 'C區第3排第2位',
                'zone': 'C',
                'shelf': '02',
                'location_type': 'storage',
                'capacity': 110,
                'status': 'maintenance',
                'notes': '維護中，暫停使用'
            },
            {
                'location_code': 'D4-01',
                'location_name': 'D區第4排第1位',
                'zone': 'D',
                'shelf': '01',
                'location_type': 'shipping',
                'capacity': 150,
                'status': 'active',
                'notes': '出貨準備區'
            },
            {
                'location_code': 'D4-02',
                'location_name': 'D區第4排第2位',
                'zone': 'D',
                'shelf': '02',
                'location_type': 'storage',
                'capacity': 95,
                'status': 'active',
                'notes': '大型物品儲存'
            },
            {
                'location_code': 'E5-01',
                'location_name': 'E區第5排第1位',
                'zone': 'E',
                'shelf': '01',
                'location_type': 'staging',
                'capacity': 75,
                'status': 'active',
                'notes': '暫存中轉區'
            },
            {
                'location_code': 'E5-02',
                'location_name': 'E區第5排第2位',
                'zone': 'E',
                'shelf': '02',
                'location_type': 'storage',
                'capacity': 85,
                'status': 'active',
                'notes': '高價值物品儲存'
            }
        ]

        for location_data in locations_data:
            location = Location.query.filter_by(
                location_code=location_data['location_code']
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

            # Create relationships with duplicate checking
            relationships = [
                (tech_supplier, laptop_dell),
                (tech_supplier, macbook),
                (electronics_wholesale, iphone),
                (electronics_wholesale, mouse),
                (global_components, monitor),
                (office_equipment, office_chair)
            ]

            for supplier, product in relationships:
                if supplier and product:
                    # Check if relationship already exists
                    if product not in supplier.products:
                        supplier.products.append(product)
                        print(
                            f"   Added relationship: {supplier.supplier_name} -> {product.name}")
                    else:
                        print(
                            f"   Relationship already exists: {supplier.supplier_name} -> {product.name}")

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
                {'product_name': 'Laptop Dell XPS 13', 'location_code': 'A1-01',
                    'quantity': 25, 'days_to_expiry': 365},
                {'product_name': 'iPhone 15 Pro', 'location_code': 'A1-02',
                    'quantity': 50, 'days_to_expiry': 180},
                {'product_name': 'MacBook Pro M3', 'location_code': 'B2-01',
                    'quantity': 15, 'days_to_expiry': 365},
                {'product_name': 'Wireless Mouse Logitech',
                    'location_code': 'B2-02', 'quantity': 100, 'days_to_expiry': 90},
                {'product_name': 'Monitor 24 inch LG', 'location_code': 'C3-01',
                    'quantity': 30, 'days_to_expiry': 180},
                {'product_name': 'Office Chair Ergonomic',
                    'location_code': 'D4-01', 'quantity': 8, 'days_to_expiry': None},
                {'product_name': 'Standing Desk', 'location_code': 'D4-02',
                    'quantity': 5, 'days_to_expiry': None},
                {'product_name': 'Wireless Keyboard', 'location_code': 'A1-03',
                    'quantity': 60, 'days_to_expiry': 120},
                {'product_name': 'Tablet iPad Air', 'location_code': 'B2-15',
                    'quantity': 20, 'days_to_expiry': 90},
                {'product_name': 'Printer HP LaserJet', 'location_code': 'E5-01',
                    'quantity': 12, 'days_to_expiry': 365},
                {'product_name': 'Gaming Chair', 'location_code': 'E5-02',
                    'quantity': 6, 'days_to_expiry': None},
                {'product_name': 'Conference Table', 'location_code': 'C3-02',
                    'quantity': 2, 'days_to_expiry': None}
            ]

            for inv_data in inventory_data:
                product = Product.query.filter_by(
                    name=inv_data['product_name']).first()
                location = Location.query.filter_by(
                    location_code=inv_data['location_code']).first()

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

        # Create some scrap data
        print("Creating scrap data...")
        try:
            from models import Scrap
            from datetime import date, timedelta

            scrap_data = [
                {
                    'product_name': 'Laptop Dell XPS 13',
                    'location_code': 'A1-01',
                    'quantity': 3,
                    'scrap_date': date.today() - timedelta(days=10),
                    'reason': '過期',
                    'status': '已處理',
                    'estimated_value': 45000.00,
                    'description': '保固期已過，無法銷售',
                    'created_by': '張倉管',
                    'processed_date': date.today() - timedelta(days=8)
                },
                {
                    'product_name': 'Office Chair Ergonomic',
                    'location_code': 'D4-01',
                    'quantity': 5,
                    'scrap_date': date.today() - timedelta(days=5),
                    'reason': '損壞',
                    'status': '待處理',
                    'estimated_value': 8000.00,
                    'description': '運送過程中損壞，無法修復',
                    'created_by': '王管理員',
                    'processed_date': None
                },
                {
                    'product_name': 'Wireless Mouse Logitech',
                    'location_code': 'B2-02',
                    'quantity': 12,
                    'scrap_date': date.today() - timedelta(days=15),
                    'reason': '品質不良',
                    'status': '處理中',
                    'estimated_value': 3600.00,
                    'description': '批次品質問題，滑鼠按鍵失靈',
                    'created_by': '李品管',
                    'processed_date': None
                },
                {
                    'product_name': 'iPhone 15 Pro',
                    'location_code': 'A1-02',
                    'quantity': 2,
                    'scrap_date': date.today() - timedelta(days=3),
                    'reason': '損壞',
                    'status': '已處理',
                    'estimated_value': 60000.00,
                    'description': '螢幕破裂，無法修復',
                    'created_by': '陳技術員',
                    'processed_date': date.today() - timedelta(days=1)
                },
                {
                    'product_name': 'Monitor 24 inch LG',
                    'location_code': 'C3-01',
                    'quantity': 1,
                    'scrap_date': date.today() - timedelta(days=7),
                    'reason': '其他',
                    'status': '待處理',
                    'estimated_value': 8000.00,
                    'description': '客戶退貨，包裝已拆封無法重新銷售',
                    'created_by': '劉客服',
                    'processed_date': None
                }
            ]

            for scrap_info in scrap_data:
                product = Product.query.filter_by(
                    name=scrap_info['product_name']).first()
                location = Location.query.filter_by(
                    location_code=scrap_info['location_code']).first()

                if product and location:
                    # Check if scrap record already exists
                    existing_scrap = Scrap.query.filter_by(
                        product_id=product.product_id,
                        location_id=location.location_id,
                        scrap_date=scrap_info['scrap_date']
                    ).first()

                    if not existing_scrap:
                        scrap_record = Scrap(
                            product_id=product.product_id,
                            location_id=location.location_id,
                            quantity=scrap_info['quantity'],
                            scrap_date=scrap_info['scrap_date'],
                            reason=scrap_info['reason'],
                            status=scrap_info['status'],
                            estimated_value=scrap_info['estimated_value'],
                            description=scrap_info['description'],
                            created_by=scrap_info['created_by'],
                            processed_date=scrap_info['processed_date']
                        )
                        db.session.add(scrap_record)

            db.session.commit()
            print("Scrap data created!")

        except Exception as e:
            print(f"Error creating scrap data: {e}")
            db.session.rollback()

        # Create sample orders
        print("Creating sample orders...")
        try:
            from models import Order, OrderItem
            from datetime import datetime, date, timedelta
            import random

            orders_data = [
                {
                    'order_number': 'ORD202412150001',
                    'order_date': datetime.now() - timedelta(days=5),
                    'expected_delivery_date': date.today() + timedelta(days=10),
                    'status': 'confirmed',
                    'priority': 'normal',
                    'ship_to': '台北市信義區信義路五段7號',
                    'total_amount': 129900.00,
                    'notes': '緊急訂單，請優先處理',
                    'customer_name': '台積電股份有限公司',
                    'user_account': 'sales',
                    'items': [
                        {'product_name': 'Laptop Dell XPS 13',
                            'quantity': 2, 'unit_price': 39950.00},
                        {'product_name': 'MacBook Pro M3',
                            'quantity': 1, 'unit_price': 50000.00}
                    ]
                },
                {
                    'order_number': 'ORD202412150002',
                    'order_date': datetime.now() - timedelta(days=3),
                    'expected_delivery_date': date.today() + timedelta(days=7),
                    'status': 'processing',
                    'priority': 'high',
                    'ship_to': '新北市板橋區縣民大道二段7號',
                    'total_amount': 95800.00,
                    'notes': '客戶要求週五前交貨',
                    'customer_name': '鴻海精密工業股份有限公司',
                    'user_account': 'admin',
                    'items': [
                        {'product_name': 'iPhone 15 Pro',
                            'quantity': 3, 'unit_price': 29900.00},
                        {'product_name': 'Wireless Mouse Logitech',
                            'quantity': 5, 'unit_price': 1200.00}
                    ]
                },
                {
                    'order_number': 'ORD202412150003',
                    'order_date': datetime.now() - timedelta(days=2),
                    'expected_delivery_date': date.today() + timedelta(days=14),
                    'status': 'pending',
                    'priority': 'normal',
                    'ship_to': '新竹市科學園區力行路3號',
                    'total_amount': 88000.00,
                    'notes': '辦公室設備採購',
                    'customer_name': '聯發科技股份有限公司',
                    'user_account': 'sales',
                    'items': [
                        {'product_name': 'Monitor 24 inch LG',
                            'quantity': 4, 'unit_price': 12000.00},
                        {'product_name': 'Office Chair Ergonomic',
                            'quantity': 2, 'unit_price': 20000.00}
                    ]
                },
                {
                    'order_number': 'ORD202412150004',
                    'order_date': datetime.now() - timedelta(days=1),
                    'expected_delivery_date': date.today() + timedelta(days=5),
                    'status': 'shipped',
                    'priority': 'urgent',
                    'ship_to': '台北市大安區羅斯福路四段1號',
                    'total_amount': 67600.00,
                    'notes': '教育用途設備',
                    'customer_name': '國立台灣大學',
                    'user_account': 'admin',
                    'items': [
                        {'product_name': 'Tablet iPad Air',
                            'quantity': 4, 'unit_price': 15900.00},
                        {'product_name': 'Wireless Keyboard',
                            'quantity': 4, 'unit_price': 1500.00}
                    ]
                },
                {
                    'order_number': 'ORD202412150005',
                    'order_date': datetime.now(),
                    'expected_delivery_date': date.today() + timedelta(days=12),
                    'status': 'pending',
                    'priority': 'low',
                    'ship_to': '台中市南屯區市政路2號',
                    'total_amount': 156000.00,
                    'notes': '大宗採購，可議價',
                    'customer_name': '友達光電股份有限公司',
                    'user_account': 'sales',
                    'items': [
                        {'product_name': 'Standing Desk',
                            'quantity': 3, 'unit_price': 25000.00},
                        {'product_name': 'Gaming Chair',
                            'quantity': 2, 'unit_price': 30000.00},
                        {'product_name': 'Conference Table',
                            'quantity': 1, 'unit_price': 51000.00}
                    ]
                },
                {
                    'order_number': 'ORD202412150006',
                    'order_date': datetime.now() - timedelta(days=7),
                    'expected_delivery_date': date.today() + timedelta(days=3),
                    'status': 'delivered',
                    'priority': 'normal',
                    'ship_to': '台北市中正區忠孝東路一段150號',
                    'total_amount': 45000.00,
                    'notes': '訂單已完成交付',
                    'customer_name': '台北市政府',
                    'user_account': 'warehouse',
                    'items': [
                        {'product_name': 'Printer HP LaserJet',
                            'quantity': 3, 'unit_price': 15000.00}
                    ]
                }
            ]

            for order_data in orders_data:
                # Find customer and user
                customer = Customer.query.filter_by(
                    name=order_data['customer_name']).first()
                user = User.query.filter_by(
                    account=order_data['user_account']).first()

                if customer and user:
                    # Check if order already exists
                    existing_order = Order.query.filter_by(
                        order_number=order_data['order_number']).first()
                    if not existing_order:
                        order = Order(
                            order_number=order_data['order_number'],
                            order_date=order_data['order_date'],
                            expected_delivery_date=order_data['expected_delivery_date'],
                            status=order_data['status'],
                            priority=order_data['priority'],
                            ship_to=order_data['ship_to'],
                            total_amount=order_data['total_amount'],
                            notes=order_data['notes'],
                            customer_id=customer.customer_id,
                            user_id=user.user_id
                        )
                        db.session.add(order)
                        db.session.flush()  # Get order_id

                        # Create order items
                        for item_data in order_data['items']:
                            product = Product.query.filter_by(
                                name=item_data['product_name']).first()
                            if product:
                                order_item = OrderItem(
                                    order_id=order.order_id,
                                    product_id=product.product_id,
                                    quantity=item_data['quantity'],
                                    unit_price=item_data['unit_price']
                                )
                                db.session.add(order_item)

            db.session.commit()
            print("Sample orders created!")

        except Exception as e:
            print(f"Error creating orders: {e}")
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
            from models import InventoryLot, Scrap, Order, OrderItem
            print(f"- {InventoryLot.query.count()} Inventory Lots")
            print(f"- {Scrap.query.count()} Scrap Records")
            print(f"- {Order.query.count()} Orders")
            print(f"- {OrderItem.query.count()} Order Items")
        except:
            print("- Inventory lots: N/A")
            print("- Scrap records: N/A")
            print("- Orders: N/A")

        print("\n🔑 Demo accounts:")
        print("Admin: admin/admin")
        print("Sales: sales/sales")
        print("Warehouse: warehouse/warehouse")


if __name__ == "__main__":
    init_sample_data()
