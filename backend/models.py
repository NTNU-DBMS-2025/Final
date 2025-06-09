from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Association table for Supplier_Product many-to-many relationship
supplier_product = db.Table('Supplier_Product',
                            db.Column('supplier_id', db.Integer, db.ForeignKey(
                                'Supplier.supplier_id'), primary_key=True),
                            db.Column('product_id', db.Integer, db.ForeignKey(
                                'Product.product_id'), primary_key=True)
                            )

# Association table for User_Role many-to-many relationship
user_role = db.Table('User_Role',
                     db.Column('user_id', db.Integer, db.ForeignKey(
                         'User.user_id'), primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey(
                         'Role.role_id'), primary_key=True)
                     )


class Product(db.Model):
    __tablename__ = 'Product'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    warranty_years = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    reorder_point = db.Column(db.Integer, nullable=False, default=10)

    # Relationships
    suppliers = db.relationship(
        'Supplier', secondary=supplier_product, back_populates='products')
    order_items = db.relationship('OrderItem', back_populates='product')
    inventory_lots = db.relationship('InventoryLot', back_populates='product')
    scraps = db.relationship('Scrap', back_populates='product')


class Supplier(db.Model):
    __tablename__ = 'Supplier'

    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_name = db.Column(db.String(100), nullable=False)
    contact_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))
    supplier_type = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    products = db.relationship(
        'Product', secondary=supplier_product, back_populates='suppliers')


class Customer(db.Model):
    __tablename__ = 'Customer'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))
    customer_type = db.Column(db.String(50), default='individual')
    customer_level = db.Column(db.String(50), default='bronze')
    tax_id = db.Column(db.String(20))
    status = db.Column(db.String(20), nullable=False, default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    orders = db.relationship('Order', back_populates='customer')

    def to_dict(self):
        """Convert Customer object to dictionary"""
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'contact': self.contact,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'customer_type': self.customer_type,
            'customer_level': self.customer_level,
            'tax_id': self.tax_id,
            'status': self.status,
            'notes': self.notes,
            'orders_count': len(self.orders) if self.orders else 0,
            'latest_order_date': max([order.order_date for order in self.orders], default=None).isoformat() if self.orders else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Role(db.Model):
    __tablename__ = 'Role'

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), nullable=False, unique=True)

    # Relationships
    users = db.relationship('User', secondary=user_role,
                            back_populates='roles')
    primary_users = db.relationship('User', back_populates='primary_role')


class User(db.Model):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(50), nullable=False, unique=True)
    pwd_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'Role.role_id'), nullable=False)

    # Relationships
    primary_role = db.relationship('Role', back_populates='primary_users')
    roles = db.relationship('Role', secondary=user_role,
                            back_populates='users')
    orders = db.relationship('Order', back_populates='user')
    shipping_vendor = db.relationship(
        'ShippingVendor', back_populates='user', uselist=False)


class ShippingVendor(db.Model):
    __tablename__ = 'Shipping_Vendor'

    user_id = db.Column(db.Integer, db.ForeignKey(
        'User.user_id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mode = db.Column(db.String(50), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='shipping_vendor')
    shipments = db.relationship('Shipment', back_populates='shipping_vendor')


class Order(db.Model):
    __tablename__ = 'Order'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_number = db.Column(db.String(50), nullable=False, unique=True)
    order_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    expected_delivery_date = db.Column(db.Date)
    status = db.Column(db.String(50), nullable=False, default='pending')
    priority = db.Column(db.String(20), nullable=False, default='normal')
    ship_to = db.Column(db.String(255), nullable=False)
    total_amount = db.Column(db.Numeric(12, 2), default=0.00)
    notes = db.Column(db.Text)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'Customer.customer_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'User.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = db.relationship('Customer', back_populates='orders')
    user = db.relationship('User', back_populates='orders')
    order_items = db.relationship('OrderItem', back_populates='order')
    shipments = db.relationship('Shipment', back_populates='order')

    def to_dict(self):
        """Convert Order object to dictionary"""
        return {
            'order_id': self.order_id,
            'order_number': self.order_number,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'expected_delivery_date': self.expected_delivery_date.isoformat() if self.expected_delivery_date else None,
            'status': self.status,
            'priority': self.priority,
            'ship_to': self.ship_to,
            'total_amount': float(self.total_amount) if self.total_amount else 0.0,
            'notes': self.notes,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else None,
            'user_id': self.user_id,
            'sales_rep': self.user.account if self.user else None,
            'items_count': len(self.order_items) if self.order_items else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class OrderItem(db.Model):
    __tablename__ = 'Order_Item'

    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'Order.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'Product.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)

    # Relationships
    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product', back_populates='order_items')

    def to_dict(self):
        """Convert OrderItem object to dictionary"""
        return {
            'order_item_id': self.order_item_id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'category': self.product.category if self.product else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price) if self.unit_price else 0.0,
            'subtotal': float(self.quantity * self.unit_price) if self.unit_price else 0.0
        }


class Shipment(db.Model):
    __tablename__ = 'Shipment'

    shipment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ship_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tracking_no = db.Column(db.String(100), nullable=False, unique=True)
    status = db.Column(db.String(50), nullable=False, default='pending')
    estimated_shipping_date = db.Column(db.Date)
    estimated_delivery_date = db.Column(db.Date)
    actual_delivery_date = db.Column(db.Date)
    shipping_address = db.Column(db.Text)
    shipping_method = db.Column(db.String(100))
    notes = db.Column(db.Text)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'Order.order_id'), nullable=False)
    shipping_vendor_id = db.Column(db.Integer, db.ForeignKey(
        'Shipping_Vendor.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    order = db.relationship('Order', back_populates='shipments')
    shipping_vendor = db.relationship(
        'ShippingVendor', back_populates='shipments')

    def to_dict(self):
        """Convert Shipment object to dictionary"""
        return {
            'shipment_id': self.shipment_id,
            'ship_date': self.ship_date.isoformat() if self.ship_date else None,
            'tracking_no': self.tracking_no,
            'tracking_number': self.tracking_no,  # Frontend compatibility
            'status': self.status,
            'estimated_shipping_date': self.estimated_shipping_date.isoformat() if self.estimated_shipping_date else None,
            'estimated_delivery_date': self.estimated_delivery_date.isoformat() if self.estimated_delivery_date else None,
            'actual_shipping_date': self.ship_date.strftime('%Y-%m-%d') if self.ship_date else None,
            'actual_delivery_date': self.actual_delivery_date.isoformat() if self.actual_delivery_date else None,
            'shipping_address': self.shipping_address,
            'shipping_method': self.shipping_method,
            'notes': self.notes,
            'order_id': self.order_id,
            'order_number': self.order.order_number if self.order else None,
            'customer_name': self.order.customer.name if self.order and self.order.customer else None,
            'shipping_vendor_id': self.shipping_vendor_id,
            'vendor_name': self.shipping_vendor.name if self.shipping_vendor else None,
            'shipping_mode': self.shipping_vendor.mode if self.shipping_vendor else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Location(db.Model):
    __tablename__ = 'Location'

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_code = db.Column(db.String(50), nullable=False, unique=True)
    location_name = db.Column(db.String(100), nullable=False)
    zone = db.Column(db.String(50), nullable=False)
    shelf = db.Column(db.String(50), nullable=False)
    location_type = db.Column(db.String(50), nullable=False, default='storage')
    capacity = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='active')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    inventory_lots = db.relationship('InventoryLot', back_populates='location')
    scraps = db.relationship('Scrap', back_populates='location')

    def get_current_stock(self):
        """Calculate total current stock in this location"""
        total = db.session.query(db.func.sum(InventoryLot.quantity)).filter_by(
            location_id=self.location_id).scalar()
        return int(total or 0)

    def get_utilization_rate(self):
        """Calculate utilization rate as percentage"""
        if self.capacity == 0:
            return 0.0
        current_stock = self.get_current_stock()
        return round((current_stock / self.capacity) * 100, 1)

    def to_dict(self):
        """Convert Location object to dictionary"""
        return {
            'location_id': self.location_id,
            'location_code': self.location_code,
            'location_name': self.location_name,
            'zone': self.zone,
            'shelf': self.shelf,
            'location_type': self.location_type,
            'capacity': self.capacity,
            'status': self.status,
            'notes': self.notes,
            'current_stock': self.get_current_stock(),
            'utilization_rate': self.get_utilization_rate(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class InventoryLot(db.Model):
    __tablename__ = 'Inventory_Lot'

    product_id = db.Column(db.Integer, db.ForeignKey(
        'Product.product_id'), primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey(
        'Location.location_id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    expiry_date = db.Column(db.Date)

    # Relationships
    product = db.relationship('Product', back_populates='inventory_lots')
    location = db.relationship('Location', back_populates='inventory_lots')


class Scrap(db.Model):
    __tablename__ = 'Scrap'

    scrap_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'Product.product_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey(
        'Location.location_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    scrap_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='待處理')
    estimated_value = db.Column(db.Numeric(10, 2), default=0.00)
    description = db.Column(db.Text)
    created_by = db.Column(db.String(100))
    processed_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = db.relationship('Product', back_populates='scraps')
    location = db.relationship('Location', back_populates='scraps')

    def to_dict(self):
        """Convert Scrap object to dictionary"""
        return {
            'scrap_id': self.scrap_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'category': self.product.category if self.product else None,
            'location_id': self.location_id,
            'location_zone': self.location.zone if self.location else None,
            'location_shelf': self.location.shelf if self.location else None,
            'location_code': self.location.location_code if self.location else None,
            'quantity': self.quantity,
            'scrap_date': self.scrap_date.isoformat() if self.scrap_date else None,
            'reason': self.reason,
            'status': self.status,
            'estimated_value': float(self.estimated_value) if self.estimated_value else 0.0,
            'description': self.description,
            'created_by': self.created_by,
            'processed_date': self.processed_date.isoformat() if self.processed_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
