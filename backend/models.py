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
    address = db.Column(db.String(255))

    # Relationships
    orders = db.relationship('Order', back_populates='customer')


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
    order_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    ship_to = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'Customer.customer_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'User.user_id'), nullable=False)

    # Relationships
    customer = db.relationship('Customer', back_populates='orders')
    user = db.relationship('User', back_populates='orders')
    order_items = db.relationship('OrderItem', back_populates='order')
    shipments = db.relationship('Shipment', back_populates='order')


class OrderItem(db.Model):
    __tablename__ = 'Order_Item'

    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'Order.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'Product.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Relationships
    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product', back_populates='order_items')


class Shipment(db.Model):
    __tablename__ = 'Shipment'

    shipment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ship_date = db.Column(db.DateTime, nullable=False)
    tracking_no = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'Order.order_id'), nullable=False)
    shipping_vendor_id = db.Column(db.Integer, db.ForeignKey(
        'Shipping_Vendor.user_id'), nullable=False)

    # Relationships
    order = db.relationship('Order', back_populates='shipments')
    shipping_vendor = db.relationship(
        'ShippingVendor', back_populates='shipments')


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

    # Relationships
    product = db.relationship('Product', back_populates='scraps')
    location = db.relationship('Location', back_populates='scraps')
