#!/usr/bin/env python3
"""
Initialize sample data for the Warehouse Management System
"""

from app import create_app
from models import db, Role, User, Product, Supplier, Customer, Location, InventoryLot, InventoryMovement
from werkzeug.security import generate_password_hash


def init_sample_data():
    """Initialize sample data for testing"""
    app = create_app()

    with app.app_context():
        print("Creating database tables...")
        db.create_all()

        print("Creating roles...")
        roles_data = [
            {'role_name': 'Owner'},
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
            {'account': 'owner', 'password': 'owner', 'role_name': 'Owner'},
            {'account': 'admin', 'password': 'admin', 'role_name': 'Admin'},
            {'account': 'sales', 'password': 'sales', 'role_name': 'Sales'},
            {'account': 'warehouse', 'password': 'warehouse',
                'role_name': 'Warehouse'},
            {'account': 'admin2', 'password': 'admin123', 'role_name': 'Admin'},
            {'account': 'sales_manager', 'password': 'sales123', 'role_name': 'Sales'},
            {'account': 'sales_rep1', 'password': 'sales123', 'role_name': 'Sales'},
            {'account': 'sales_rep2', 'password': 'sales123', 'role_name': 'Sales'},
            {'account': 'warehouse_super',
                'password': 'warehouse123', 'role_name': 'Warehouse'},
            {'account': 'warehouse_staff1',
                'password': 'warehouse123', 'role_name': 'Warehouse'},
            {'account': 'warehouse_staff2',
                'password': 'warehouse123', 'role_name': 'Warehouse'},
            {'account': 'warehouse_staff3',
                'password': 'warehouse123', 'role_name': 'Warehouse'}
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
            },
            {
                'supplier_name': 'Mobile Tech Solutions',
                'contact_name': 'Alex Chen',
                'phone': '02-8765-4321',
                'email': 'sales@mobiletech.com',
                'address': '456 Mobile Street, Taipei, Taiwan',
                'supplier_type': 'manufacturer',
                'status': 'active',
                'notes': 'Mobile devices and accessories manufacturer'
            },
            {
                'supplier_name': 'Smart Home Electronics',
                'contact_name': 'Jenny Wu',
                'phone': '07-123-9876',
                'email': 'contact@smarthome.com',
                'address': '789 Smart Ave, Kaohsiung, Taiwan',
                'supplier_type': 'distributor',
                'status': 'active',
                'notes': 'Smart home and IoT devices distributor'
            },
            {
                'supplier_name': 'Gaming Hardware Co.',
                'contact_name': 'Tom Lin',
                'phone': '04-567-8901',
                'email': 'orders@gaminghw.com',
                'address': '123 Gaming Road, Taichung, Taiwan',
                'supplier_type': 'wholesaler',
                'status': 'active',
                'notes': 'Gaming hardware and peripherals wholesaler'
            },
            {
                'supplier_name': 'Enterprise Systems Ltd.',
                'contact_name': 'Grace Wang',
                'phone': '03-456-7890',
                'email': 'enterprise@systems.com',
                'address': '678 Enterprise Blvd, Taoyuan, Taiwan',
                'supplier_type': 'manufacturer',
                'status': 'active',
                'notes': 'Enterprise hardware and server solutions'
            },
            {
                'supplier_name': 'Budget Electronics Store',
                'contact_name': 'Kevin Zhang',
                'phone': '06-789-0123',
                'email': 'budget@electronics.com',
                'address': '234 Budget St, Tainan, Taiwan',
                'supplier_type': 'wholesaler',
                'status': 'inactive',
                'notes': 'Budget electronics supplier - currently inactive'
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
                'price': 45000.00,
                'image_url': 'https://example.com/dell-xps13.jpg'
            },
            {
                'name': 'Office Chair Ergonomic',
                'category': 'Furniture',
                'warranty_years': 2,
                'price': 8500.00,
                'image_url': 'https://example.com/office-chair.jpg'
            },
            {
                'name': 'Wireless Mouse Logitech',
                'category': 'Electronics',
                'warranty_years': 1,
                'price': 1200.00,
                'image_url': 'https://example.com/mouse.jpg'
            },
            {
                'name': 'Monitor 24 inch LG',
                'category': 'Electronics',
                'warranty_years': 2,
                'price': 8900.00,
                'image_url': 'https://example.com/monitor.jpg'
            },
            {
                'name': 'iPhone 15 Pro',
                'category': 'Electronics',
                'warranty_years': 1,
                'price': 29900.00,
                'image_url': 'https://example.com/iphone15.jpg'
            },
            {
                'name': 'MacBook Pro M3',
                'category': 'Electronics',
                'warranty_years': 3,
                'price': 65000.00,
                'image_url': 'https://example.com/macbook.jpg'
            },
            {
                'name': 'Standing Desk',
                'category': 'Furniture',
                'warranty_years': 5,
                'price': 15000.00,
                'image_url': 'https://example.com/standing-desk.jpg'
            },
            {
                'name': 'Wireless Keyboard',
                'category': 'Electronics',
                'warranty_years': 2,
                'price': 2500.00,
                'image_url': 'https://example.com/keyboard.jpg'
            },
            {
                'name': 'Conference Table',
                'category': 'Furniture',
                'warranty_years': 10,
                'price': 25000.00,
                'image_url': 'https://example.com/conference-table.jpg'
            },
            {
                'name': 'Printer HP LaserJet',
                'category': 'Electronics',
                'warranty_years': 2,
                'price': 12000.00,
                'image_url': 'https://example.com/printer.jpg'
            },
            {
                'name': 'Gaming Chair',
                'category': 'Furniture',
                'warranty_years': 3,
                'price': 18000.00,
                'image_url': 'https://example.com/gaming-chair.jpg'
            },
            {
                'name': 'Tablet iPad Air',
                'category': 'Electronics',
                'warranty_years': 1,
                'price': 22000.00,
                'image_url': 'https://example.com/ipad.jpg'
            },
            {
                'name': 'Samsung Galaxy S24',
                'category': 'Electronics',
                'warranty_years': 2,
                'price': 28000.00,
                'image_url': 'https://example.com/galaxy-s24.jpg'
            },
            {
                'name': 'Dell OptiPlex Desktop',
                'category': 'Electronics',
                'warranty_years': 3,
                'price': 32000.00,
                'image_url': 'https://example.com/dell-desktop.jpg'
            },
            {
                'name': 'ASUS Gaming Monitor 27"',
                'category': 'Electronics',
                'warranty_years': 3,
                'price': 16500.00,
                'image_url': 'https://example.com/asus-monitor.jpg'
            },
            {
                'name': 'Logitech Webcam HD',
                'category': 'Electronics',
                'warranty_years': 2,
                'price': 3200.00,
                'image_url': 'https://example.com/webcam.jpg'
            },
            {
                'name': 'Microsoft Surface Pro',
                'category': 'Electronics',
                'warranty_years': 2,
                'price': 38000.00,
                'image_url': 'https://example.com/surface-pro.jpg'
            },
            {
                'name': 'Executive Desk',
                'category': 'Furniture',
                'warranty_years': 7,
                'price': 35000.00,
                'image_url': 'https://example.com/executive-desk.jpg'
            },
            {
                'name': 'Bookshelf Unit',
                'category': 'Furniture',
                'warranty_years': 5,
                'price': 12000.00,
                'image_url': 'https://example.com/bookshelf.jpg'
            },
            {
                'name': 'Storage Cabinet',
                'category': 'Furniture',
                'warranty_years': 8,
                'price': 8800.00,
                'image_url': 'https://example.com/storage-cabinet.jpg'
            },
            {
                'name': 'Wireless Headphones',
                'category': 'Electronics',
                'warranty_years': 2,
                'price': 4500.00,
                'image_url': 'https://example.com/headphones.jpg'
            },
            {
                'name': 'Smart Watch Apple',
                'category': 'Electronics',
                'warranty_years': 1,
                'price': 12900.00,
                'image_url': 'https://example.com/apple-watch.jpg'
            },
            {
                'name': 'Bluetooth Speaker',
                'category': 'Electronics',
                'warranty_years': 2,
                'price': 2800.00,
                'image_url': 'https://example.com/speaker.jpg'
            },
            {
                'name': 'Desk Lamp LED',
                'category': 'Office Supplies',
                'warranty_years': 3,
                'price': 1800.00,
                'image_url': 'https://example.com/desk-lamp.jpg'
            },
            {
                'name': 'Ergonomic Footrest',
                'category': 'Office Supplies',
                'warranty_years': 2,
                'price': 2200.00,
                'image_url': 'https://example.com/footrest.jpg'
            },
            {
                'name': 'Router Wi-Fi 6',
                'category': 'Electronics',
                'warranty_years': 3,
                'price': 5800.00,
                'image_url': 'https://example.com/router.jpg'
            },
            {
                'name': 'External Hard Drive 2TB',
                'category': 'Electronics',
                'warranty_years': 3,
                'price': 3500.00,
                'image_url': 'https://example.com/hard-drive.jpg'
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
            },
            {
                'name': '宏碁股份有限公司',
                'contact': '劉總監',
                'phone': '02-8691-3000',
                'email': 'procurement@acer.com',
                'address': '新北市汐止區新台五路一段88號',
                'customer_type': 'business',
                'customer_level': 'platinum',
                'tax_id': '20266989',
                'status': 'active',
                'notes': '電腦製造商，大量IT設備需求'
            },
            {
                'name': '華碩電腦股份有限公司',
                'contact': '張協理',
                'phone': '02-2894-3447',
                'email': 'orders@asus.com',
                'address': '台北市北投區立德路150號',
                'customer_type': 'business',
                'customer_level': 'gold',
                'tax_id': '23638777',
                'status': 'active',
                'notes': '3C產品製造商，定期採購辦公設備'
            },
            {
                'name': '李大華',
                'contact': '李大華',
                'phone': '0955-123-456',
                'email': 'dahua.li@email.com',
                'address': '台中市西屯區台灣大道三段99號',
                'customer_type': 'individual',
                'customer_level': 'silver',
                'tax_id': '',
                'status': 'active',
                'notes': '個人客戶，經常購買電子產品'
            },
            {
                'name': '成功大學',
                'contact': '陳主任',
                'phone': '06-275-7575',
                'email': 'purchasing@ncku.edu.tw',
                'address': '台南市東區大學路1號',
                'customer_type': 'educational',
                'customer_level': 'gold',
                'tax_id': '69219131',
                'status': 'active',
                'notes': '國立大學，研究設備採購'
            },
            {
                'name': '台中市政府',
                'contact': '楊科長',
                'phone': '04-2228-9111',
                'email': 'procurement@taichung.gov.tw',
                'address': '台中市西屯區台灣大道三段99號',
                'customer_type': 'government',
                'customer_level': 'gold',
                'tax_id': '52282203',
                'status': 'active',
                'notes': '地方政府採購'
            },
            {
                'name': '中小企業發展中心',
                'contact': '林副理',
                'phone': '07-331-0668',
                'email': 'info@sme.org.tw',
                'address': '高雄市苓雅區四維三路6號',
                'customer_type': 'business',
                'customer_level': 'silver',
                'tax_id': '91763982',
                'status': 'active',
                'notes': '中小企業服務機構'
            },
            {
                'name': '陳小芳',
                'contact': '陳小芳',
                'phone': '0933-555-777',
                'email': 'xiaofang.chen@gmail.com',
                'address': '新竹市東區光復路二段101號',
                'customer_type': 'individual',
                'customer_level': 'bronze',
                'tax_id': '',
                'status': 'active',
                'notes': '新客戶，首次購買'
            },
            {
                'name': '遠傳電信股份有限公司',
                'contact': '黃經理',
                'phone': '02-6632-6888',
                'email': 'b2b@fetnet.net',
                'address': '台北市內湖區瑞光路188號',
                'customer_type': 'business',
                'customer_level': 'platinum',
                'tax_id': '97176270',
                'status': 'active',
                'notes': '電信業者，通訊設備採購'
            },
            {
                'name': '誠品書店股份有限公司',
                'contact': '吳店長',
                'phone': '02-6636-5888',
                'email': 'procurement@eslite.com',
                'address': '台北市信義區菸廠路88號',
                'customer_type': 'business',
                'customer_level': 'silver',
                'tax_id': '12346789',
                'status': 'active',
                'notes': '零售業，門市設備需求'
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
            },
            {
                'location_code': 'F6-01',
                'location_name': 'F區第6排第1位',
                'zone': 'F',
                'shelf': '01',
                'location_type': 'storage',
                'capacity': 120,
                'status': 'active',
                'notes': '大型設備儲存區'
            },
            {
                'location_code': 'F6-02',
                'location_name': 'F區第6排第2位',
                'zone': 'F',
                'shelf': '02',
                'location_type': 'storage',
                'capacity': 100,
                'status': 'active',
                'notes': '標準儲存位置'
            },
            {
                'location_code': 'F6-03',
                'location_name': 'F區第6排第3位',
                'zone': 'F',
                'shelf': '03',
                'location_type': 'picking',
                'capacity': 80,
                'status': 'occupied',
                'notes': '快速揀貨區域'
            },
            {
                'location_code': 'G7-01',
                'location_name': 'G區第7排第1位',
                'zone': 'G',
                'shelf': '01',
                'location_type': 'receiving',
                'capacity': 150,
                'status': 'active',
                'notes': '新貨收貨區'
            },
            {
                'location_code': 'G7-02',
                'location_name': 'G區第7排第2位',
                'zone': 'G',
                'shelf': '02',
                'location_type': 'storage',
                'capacity': 90,
                'status': 'active',
                'notes': '電子產品專用區'
            },
            {
                'location_code': 'H8-01',
                'location_name': 'H區第8排第1位',
                'zone': 'H',
                'shelf': '01',
                'location_type': 'shipping',
                'capacity': 130,
                'status': 'active',
                'notes': '急件出貨區'
            },
            {
                'location_code': 'H8-02',
                'location_name': 'H區第8排第2位',
                'zone': 'H',
                'shelf': '02',
                'location_type': 'storage',
                'capacity': 110,
                'status': 'maintenance',
                'notes': '設備維修中'
            },
            {
                'location_code': 'I9-01',
                'location_name': 'I區第9排第1位',
                'zone': 'I',
                'shelf': '01',
                'location_type': 'storage',
                'capacity': 95,
                'status': 'active',
                'notes': '辦公家具專區'
            },
            {
                'location_code': 'I9-02',
                'location_name': 'I區第9排第2位',
                'zone': 'I',
                'shelf': '02',
                'location_type': 'staging',
                'capacity': 70,
                'status': 'active',
                'notes': '品質檢驗暫存區'
            },
            {
                'location_code': 'J10-01',
                'location_name': 'J區第10排第1位',
                'zone': 'J',
                'shelf': '01',
                'location_type': 'storage',
                'capacity': 85,
                'status': 'active',
                'notes': '小件物品儲存'
            },
            {
                'location_code': 'J10-02',
                'location_name': 'J區第10排第2位',
                'zone': 'J',
                'shelf': '02',
                'location_type': 'storage',
                'capacity': 105,
                'status': 'active',
                'notes': '配件專用儲存區'
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
                    'quantity': 2, 'days_to_expiry': None},
                {'product_name': 'Samsung Galaxy S24', 'location_code': 'F6-01',
                    'quantity': 45, 'days_to_expiry': 120},
                {'product_name': 'Dell OptiPlex Desktop', 'location_code': 'F6-02',
                    'quantity': 18, 'days_to_expiry': 365},
                {'product_name': 'ASUS Gaming Monitor 27"', 'location_code': 'G7-01',
                    'quantity': 22, 'days_to_expiry': 180},
                {'product_name': 'Logitech Webcam HD', 'location_code': 'G7-02',
                    'quantity': 35, 'days_to_expiry': 90},
                {'product_name': 'Microsoft Surface Pro', 'location_code': 'H8-01',
                    'quantity': 12, 'days_to_expiry': 180},
                {'product_name': 'Executive Desk', 'location_code': 'I9-01',
                    'quantity': 4, 'days_to_expiry': None},
                {'product_name': 'Bookshelf Unit', 'location_code': 'I9-02',
                    'quantity': 8, 'days_to_expiry': None},
                {'product_name': 'Storage Cabinet', 'location_code': 'J10-01',
                    'quantity': 6, 'days_to_expiry': None},
                {'product_name': 'Wireless Headphones', 'location_code': 'J10-02',
                    'quantity': 75, 'days_to_expiry': 60},
                {'product_name': 'Smart Watch Apple', 'location_code': 'F6-03',
                    'quantity': 28, 'days_to_expiry': 90},
                {'product_name': 'Bluetooth Speaker', 'location_code': 'E5-01',
                    'quantity': 40, 'days_to_expiry': 120},
                {'product_name': 'Desk Lamp LED', 'location_code': 'A1-01',
                    'quantity': 55, 'days_to_expiry': 365},
                {'product_name': 'Ergonomic Footrest', 'location_code': 'B2-01',
                    'quantity': 25, 'days_to_expiry': 180},
                {'product_name': 'Router Wi-Fi 6', 'location_code': 'C3-01',
                    'quantity': 30, 'days_to_expiry': 365},
                {'product_name': 'External Hard Drive 2TB', 'location_code': 'D4-01',
                    'quantity': 65, 'days_to_expiry': 180}
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
                },
                {
                    'product_name': 'Samsung Galaxy S24',
                    'location_code': 'F6-01',
                    'quantity': 5,
                    'scrap_date': date.today() - timedelta(days=12),
                    'reason': '損壞',
                    'status': '已處理',
                    'estimated_value': 120000.00,
                    'description': '運送途中受潮，螢幕出現水漬',
                    'created_by': '張倉管',
                    'processed_date': date.today() - timedelta(days=9)
                },
                {
                    'product_name': 'Wireless Headphones',
                    'location_code': 'J10-02',
                    'quantity': 8,
                    'scrap_date': date.today() - timedelta(days=6),
                    'reason': '品質不良',
                    'status': '處理中',
                    'estimated_value': 12000.00,
                    'description': '批次品質問題，左右聲道不平衡',
                    'created_by': '李品管',
                    'processed_date': None
                },
                {
                    'product_name': 'Desk Lamp LED',
                    'location_code': 'A1-01',
                    'quantity': 3,
                    'scrap_date': date.today() - timedelta(days=4),
                    'reason': '過期',
                    'status': '待處理',
                    'estimated_value': 2700.00,
                    'description': 'LED燈珠老化，亮度不足',
                    'created_by': '王管理員',
                    'processed_date': None
                },
                {
                    'product_name': 'Router Wi-Fi 6',
                    'location_code': 'C3-01',
                    'quantity': 2,
                    'scrap_date': date.today() - timedelta(days=2),
                    'reason': '損壞',
                    'status': '已處理',
                    'estimated_value': 8000.00,
                    'description': '天線斷裂，訊號接收不良',
                    'created_by': '陳技術員',
                    'processed_date': date.today() - timedelta(days=1)
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

        # Create sample shipping vendors first
        print("Creating sample shipping vendors...")
        try:
            from models import ShippingVendor

            shipping_vendors_data = [
                {'user_account': 'admin', 'name': '快遞通運輸', 'mode': '標準配送'},
                {'user_account': 'warehouse', 'name': '台灣宅配通', 'mode': '快速配送'},
                {'user_account': 'sales', 'name': '新竹物流', 'mode': '特殊配送'},
                {'user_account': 'warehouse_super',
                    'name': '黑貓宅急便', 'mode': '快速配送'},
                {'user_account': 'sales_manager', 'name': '統一速達', 'mode': '標準配送'},
                {'user_account': 'warehouse_staff1',
                    'name': '7-ELEVEN交貨便', 'mode': '便利商店取貨'},
                {'user_account': 'sales_rep1', 'name': '嘉里大榮物流', 'mode': '大宗貨運'},
                {'user_account': 'admin2', 'name': '中華郵政', 'mode': '郵政宅配'}
            ]

            for vendor_data in shipping_vendors_data:
                user = User.query.filter_by(
                    account=vendor_data['user_account']).first()
                if user:
                    existing_vendor = ShippingVendor.query.filter_by(
                        user_id=user.user_id).first()
                    if not existing_vendor:
                        shipping_vendor = ShippingVendor(
                            user_id=user.user_id,
                            name=vendor_data['name'],
                            mode=vendor_data['mode']
                        )
                        db.session.add(shipping_vendor)

            db.session.commit()
            print("Sample shipping vendors created!")

        except Exception as e:
            print(f"Error creating shipping vendors: {e}")
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
                    'notes': '緊急訂單，請優先處理',
                    'customer_name': '台積電股份有限公司',
                    'user_account': 'sales',
                    'items': [
                        {'product_name': 'Laptop Dell XPS 13', 'quantity': 2},
                        {'product_name': 'MacBook Pro M3', 'quantity': 1}
                    ]
                },
                {
                    'order_number': 'ORD202412150002',
                    'order_date': datetime.now() - timedelta(days=3),
                    'expected_delivery_date': date.today() + timedelta(days=7),
                    'status': 'processing',
                    'priority': 'high',
                    'ship_to': '新北市板橋區縣民大道二段7號',
                    'notes': '客戶要求週五前交貨',
                    'customer_name': '鴻海精密工業股份有限公司',
                    'user_account': 'admin',
                    'items': [
                        {'product_name': 'iPhone 15 Pro', 'quantity': 3},
                        {'product_name': 'Wireless Mouse Logitech', 'quantity': 5}
                    ]
                },
                {
                    'order_number': 'ORD202412150003',
                    'order_date': datetime.now() - timedelta(days=2),
                    'expected_delivery_date': date.today() + timedelta(days=14),
                    'status': 'pending',
                    'priority': 'normal',
                    'ship_to': '新竹市科學園區力行路3號',
                    'notes': '辦公室設備採購',
                    'customer_name': '聯發科技股份有限公司',
                    'user_account': 'sales',
                    'items': [
                        {'product_name': 'Monitor 24 inch LG', 'quantity': 4},
                        {'product_name': 'Office Chair Ergonomic', 'quantity': 2}
                    ]
                },
                {
                    'order_number': 'ORD202412150004',
                    'order_date': datetime.now() - timedelta(days=1),
                    'expected_delivery_date': date.today() + timedelta(days=5),
                    'status': 'shipped',
                    'priority': 'urgent',
                    'ship_to': '台北市大安區羅斯福路四段1號',
                    'notes': '教育用途設備',
                    'customer_name': '台灣大學',
                    'user_account': 'admin',
                    'items': [
                        {'product_name': 'Tablet iPad Air', 'quantity': 4},
                        {'product_name': 'Wireless Keyboard', 'quantity': 4}
                    ]
                },
                {
                    'order_number': 'ORD202412150005',
                    'order_date': datetime.now(),
                    'expected_delivery_date': date.today() + timedelta(days=12),
                    'status': 'pending',
                    'priority': 'low',
                    'ship_to': '台中市南屯區市政路2號',
                    'notes': '大宗採購，可議價',
                    'customer_name': '遠傳電信股份有限公司',
                    'user_account': 'sales',
                    'items': [
                        {'product_name': 'Standing Desk', 'quantity': 3},
                        {'product_name': 'Gaming Chair', 'quantity': 2},
                        {'product_name': 'Conference Table', 'quantity': 1}
                    ]
                },
                {
                    'order_number': 'ORD202412150006',
                    'order_date': datetime.now() - timedelta(days=7),
                    'expected_delivery_date': date.today() + timedelta(days=3),
                    'status': 'delivered',
                    'priority': 'normal',
                    'ship_to': '台北市中正區忠孝東路一段150號',
                    'notes': '訂單已完成交付',
                    'customer_name': '台北市政府',
                    'user_account': 'warehouse',
                    'items': [
                        {'product_name': 'Printer HP LaserJet', 'quantity': 3}
                    ]
                },
                {
                    'order_number': 'ORD202412150007',
                    'order_date': datetime.now() - timedelta(days=4),
                    'expected_delivery_date': date.today() + timedelta(days=8),
                    'status': 'processing',
                    'priority': 'normal',
                    'ship_to': '新北市汐止區新台五路一段88號',
                    'notes': 'Acer公司大量採購',
                    'customer_name': '宏碁股份有限公司',
                    'user_account': 'sales_manager',
                    'items': [
                        {'product_name': 'Samsung Galaxy S24', 'quantity': 10},
                        {'product_name': 'Wireless Headphones', 'quantity': 5},
                        {'product_name': 'Smart Watch Apple', 'quantity': 3}
                    ]
                },
                {
                    'order_number': 'ORD202412150008',
                    'order_date': datetime.now() - timedelta(days=6),
                    'expected_delivery_date': date.today() + timedelta(days=4),
                    'status': 'shipped',
                    'priority': 'high',
                    'ship_to': '台北市北投區立德路150號',
                    'notes': 'ASUS辦公設備更新',
                    'customer_name': '華碩電腦股份有限公司',
                    'user_account': 'sales_rep1',
                    'items': [
                        {'product_name': 'Dell OptiPlex Desktop', 'quantity': 3},
                        {'product_name': 'ASUS Gaming Monitor 27"', 'quantity': 2},
                        {'product_name': 'Router Wi-Fi 6', 'quantity': 4}
                    ]
                },
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
                        # Calculate total amount from product prices
                        total_amount = 0
                        order_items_data = []
                        for item_data in order_data['items']:
                            product = Product.query.filter_by(
                                name=item_data['product_name']).first()

                            # If product doesn't exist, create it with default values
                            if not product:
                                print(
                                    f"   Creating missing product: {item_data['product_name']}")
                                # Determine category based on product name
                                product_name = item_data['product_name'].lower(
                                )
                                if any(keyword in product_name for keyword in ['chair', 'desk', 'table', 'cabinet', 'shelf']):
                                    category = 'Furniture'
                                elif any(keyword in product_name for keyword in ['lamp', 'footrest']):
                                    category = 'Office Supplies'
                                else:
                                    category = 'Electronics'

                                # Create new product with reasonable defaults
                                product = Product(
                                    name=item_data['product_name'],
                                    category=category,
                                    warranty_years=2,  # Default warranty
                                    price=10000.00,    # Default price
                                    image_url=f'https://example.com/{item_data["product_name"].lower().replace(" ", "-")}.jpg',
                                    reorder_point=10
                                )
                                db.session.add(product)
                                db.session.flush()  # Get product_id

                            unit_price = float(product.price)
                            subtotal = unit_price * item_data['quantity']
                            total_amount += subtotal
                            order_items_data.append({
                                'product': product,
                                'quantity': item_data['quantity'],
                                'unit_price': unit_price
                            })

                        order = Order(
                            order_number=order_data['order_number'],
                            order_date=order_data['order_date'],
                            expected_delivery_date=order_data['expected_delivery_date'],
                            status=order_data['status'],
                            priority=order_data['priority'],
                            ship_to=order_data['ship_to'],
                            total_amount=total_amount,
                            notes=order_data['notes'],
                            customer_id=customer.customer_id,
                            user_id=user.user_id
                        )
                        db.session.add(order)
                        db.session.flush()  # Get order_id

                        # Create order items with product prices
                        for item_info in order_items_data:
                            order_item = OrderItem(
                                order_id=order.order_id,
                                product_id=item_info['product'].product_id,
                                quantity=item_info['quantity'],
                                unit_price=item_info['unit_price']
                            )
                            db.session.add(order_item)

            db.session.commit()
            print("Sample orders created!")

        except Exception as e:
            print(f"Error creating orders: {e}")
            db.session.rollback()

        # Create sample shipments
        print("Creating sample shipments...")
        try:
            from models import Shipment, ShippingVendor
            from datetime import date, timedelta

            # Get orders and shipping vendors
            orders = Order.query.limit(3).all()
            shipping_vendors = ShippingVendor.query.all()

            if orders and shipping_vendors:
                shipments_data = [
                    {
                        'order': orders[0],
                        'shipping_vendor': shipping_vendors[0],
                        'tracking_no': 'TRK20240115001',
                        'status': 'in_transit',
                        'estimated_shipping_date': date.today() - timedelta(days=2),
                        'estimated_delivery_date': date.today() + timedelta(days=1),
                        'shipping_address': '台北市信義區信義路五段7號',
                        'shipping_method': '標準配送',
                        'notes': '請於上班時間送達'
                    },
                    {
                        'order': orders[1],
                        'shipping_vendor': shipping_vendors[1] if len(shipping_vendors) > 1 else shipping_vendors[0],
                        'tracking_no': 'TRK20240114002',
                        'status': 'delivered',
                        'estimated_shipping_date': date.today() - timedelta(days=3),
                        'estimated_delivery_date': date.today() - timedelta(days=1),
                        'actual_delivery_date': date.today() - timedelta(days=1),
                        'shipping_address': '新北市板橋區中山路一段152號',
                        'shipping_method': '快速配送',
                        'notes': '客戶要求下午送達'
                    },
                    {
                        'order': orders[2],
                        'shipping_vendor': shipping_vendors[2] if len(shipping_vendors) > 2 else shipping_vendors[0],
                        'tracking_no': 'TRK20240116003',
                        'status': 'pending',
                        'estimated_shipping_date': date.today() + timedelta(days=1),
                        'estimated_delivery_date': date.today() + timedelta(days=3),
                        'shipping_address': '台中市西屯區台灣大道四段1727號',
                        'shipping_method': '特殊配送',
                        'notes': '大型物品需使用貨梯'
                    }
                ]

                for shipment_data in shipments_data:
                    existing_shipment = Shipment.query.filter_by(
                        tracking_no=shipment_data['tracking_no']
                    ).first()

                    if not existing_shipment:
                        shipment = Shipment(
                            order_id=shipment_data['order'].order_id,
                            shipping_vendor_id=shipment_data['shipping_vendor'].user_id,
                            tracking_no=shipment_data['tracking_no'],
                            status=shipment_data['status'],
                            estimated_shipping_date=shipment_data.get(
                                'estimated_shipping_date'),
                            estimated_delivery_date=shipment_data.get(
                                'estimated_delivery_date'),
                            actual_delivery_date=shipment_data.get(
                                'actual_delivery_date'),
                            shipping_address=shipment_data['shipping_address'],
                            shipping_method=shipment_data['shipping_method'],
                            notes=shipment_data['notes']
                        )
                        db.session.add(shipment)

                db.session.commit()
                print("Sample shipments created!")

        except Exception as e:
            print(f"Error creating shipments: {e}")
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
            from models import InventoryLot, Scrap, Order, OrderItem, ShippingVendor
            print(f"- {InventoryLot.query.count()} Inventory Lots")
            print(f"- {InventoryMovement.query.count()} Inventory Movements")
            print(f"- {Scrap.query.count()} Scrap Records")
            print(f"- {Order.query.count()} Orders")
            print(f"- {OrderItem.query.count()} Order Items")
            print(f"- {ShippingVendor.query.count()} Shipping Vendors")
        except:
            print("- Inventory lots: N/A")
            print("- Inventory movements: N/A")
            print("- Scrap records: N/A")
            print("- Orders: N/A")
            print("- Shipping vendors: N/A")

        print("\n Demo accounts:")
        print("Admin: admin/admin, admin2/admin123")
        print("Sales: sales/sales, sales_manager/sales123, sales_rep1/sales123, sales_rep2/sales123")
        print("Warehouse: warehouse/warehouse, warehouse_super/warehouse123, warehouse_staff1/warehouse123, etc.")

        print("\n Enhanced features added:")
        print("- 11 total users across different roles")
        print("- 28 products in Electronics, Furniture, and Office Supplies")
        print("- 12 suppliers with various types and statuses")
        print("- 18 customers including major Taiwan companies")
        print("- 24 warehouse locations across zones A-J")
        print("- Comprehensive inventory data with expiry dates")
        print("- 10 scrap records with different statuses")
        print("- 10 sample orders with realistic scenarios")
        print("- 8 shipping vendors with different delivery modes")


if __name__ == "__main__":
    init_sample_data()
